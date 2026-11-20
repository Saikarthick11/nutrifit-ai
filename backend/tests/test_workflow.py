from datetime import date
from types import SimpleNamespace
import pytest
from fastapi.testclient import TestClient
from main import create_app
from storage import Store
from extraction import baseline, llm, missing_slots
from models import Extraction
import nutrition

@pytest.fixture
def client():
    import os
    from uuid import uuid4
    from dotenv import dotenv_values
    from sqlalchemy import text
    from storage import metadata
    config=os.getenv('NUTRIFIT_TEST_POSTGRES_ENV')
    if not config:
        with TestClient(create_app(Store('sqlite:///:memory:'))) as c: yield c
        return
    url=dotenv_values(config).get('DATABASE_URL','')
    assert url.startswith(('postgresql://','postgresql+psycopg://'))
    store=Store(url)
    engine=store.engine
    schema='test_'+uuid4().hex
    with engine.begin() as c: c.execute(text('CREATE SCHEMA '+schema))
    store.engine=engine.execution_options(schema_translate_map={None:schema})
    try:
        metadata.create_all(store.engine)
        with TestClient(create_app(store)) as c: yield c
    finally:
        with engine.begin() as c: c.execute(text('DROP SCHEMA '+schema+' CASCADE'))
        engine.dispose()

def start(c): return c.post('/conversations',json={}).json()
def turn(c,s,text):
    r=c.post(f'/conversations/{s["id"]}/messages',json={'text':text,'version':s['version']})
    assert r.status_code==200,r.text
    return r.json()

DATA={'fdcId':123,'description':'Test eggs','dataType':'SR Legacy','foodPortions':[{'id':10,'amount':2,'gramWeight':100,'modifier':'large eggs'}],'foodNutrients':[{'nutrient':{'id':1008,'unitName':'kcal'},'amount':150},{'nutrient':{'id':1003,'unitName':'g'},'amount':12}]}

def test_original_endpoints(client):
    assert client.get('/health').json()=={'status':'ok'}
    assert client.get('/').status_code==200
    d=client.post('/baseline/extract',json={'text':'I ate 2 slices of toast and eggs'}).json()
    assert d['foods']==[{'name':'toast','quantity':2,'unit':'slices'},{'name':'eggs','quantity':None,'unit':'count'}]
    assert d['missing_fields']==['quantity:eggs']

def test_clarification_workout_confirmation_and_history(client):
    s=turn(client,start(client),'I ran yesterday')
    assert s['missing_fields']==['workouts.0.duration_minutes']
    assert client.post(f'/conversations/{s["id"]}/confirm',json={'version':s['version']}).status_code==422
    s=turn(client,s,'30 minutes')
    assert s['status']=='ready'
    path=f'/conversations/{s["id"]}/confirm'
    assert client.post(path,json={'version':s['version']}).json()['status']=='confirmed'
    assert client.post(path,json={'version':s['version']}).status_code==200
    h=client.get('/history?start=2000-01-01&end=2099-01-01').json()
    assert len(h['records'])==1
    assert h['records'][0]['extraction']['workouts'][0]['duration_minutes']==30
    s=turn(client,start(client),'Show nutrition yesterday')
    assert s['status']=='history' and len(s['history']['records'])==1

def test_meal_confirmation_portions_and_correction(client,monkeypatch):
    monkeypatch.setattr(nutrition,'detail',lambda _: DATA)
    s=turn(client,start(client),'I ate eggs today')
    s=turn(client,s,'2')
    assert s['status']=='nutrition'
    r=client.post(f'/conversations/{s["id"]}/nutrition',json={'version':s['version'],'food_index':0,'fdc_id':123,'portion_id':10,'portion_count':1})
    assert r.status_code==200,r.text
    s=r.json(); assert s['nutrition']['0']['grams']==100
    assert s['nutrition']['0']['nutrients']['kcal']==150
    assert s['nutrition']['0']['nutrients']['carbs_g'] is None
    s=turn(client,s,'I ate 3 eggs today')
    assert s['nutrition']=={} and s['status']=='nutrition'
    s=client.post(f'/conversations/{s["id"]}/nutrition',json={'version':s['version'],'food_index':0,'fdc_id':123,'grams':150}).json()
    assert client.post(f'/conversations/{s["id"]}/confirm',json={'version':s['version']}).status_code==200
    h=client.get('/history?start=2000-01-01&end=2099-01-01').json()
    assert h['known_totals']['kcal']==225
    assert h['foods_missing_nutrients']['carbs_g']==1

def test_stale_version_and_persistence(client):
    s=start(client); updated=turn(client,s,'I ate 2 eggs today')
    assert client.get('/conversations/'+s['id']).json()==updated
    assert client.post(f'/conversations/{s["id"]}/messages',json={'text':'3','version':0}).status_code==409

def test_validation(client):
    assert client.post('/baseline/extract',json={'text':''}).status_code==422
    assert client.get('/history?start=2026-11-12&end=2026-11-01').status_code==422
    s=start(client)
    assert client.post(f'/conversations/{s["id"]}/messages',json={'text':'I ate eggs 2026-99-99','version':0}).status_code==422
    with pytest.raises(ValueError): nutrition.calculate(DATA,grams=20,portion_id=10)
    with pytest.raises(ValueError): nutrition.calculate(DATA,portion_id=999,portion_count=2)
    with pytest.raises(ValueError): nutrition.calculate(DATA,grams=float('nan'))

def test_baseline_fraction_and_negation():
    e=baseline('I ate 1.5 slices of toast today',date(2026,11,12))
    assert e.foods[0].quantity==1.5
    assert baseline("I didn't eat eggs",date(2026,11,12)).intent=='unknown'
    assert baseline('I will eat eggs',date(2026,11,12)).intent=='unknown'
    e=baseline('I ate 2 rice today',date(2026,11,12))
    assert missing_slots(e)==['foods.0.unit']
    assert baseline('cups',date(2026,11,12),e).foods[0].unit=='cups'

def fake_gemini(monkeypatch, text, finish='STOP', actual='gemini-3.5-flash-lite', fail=None, capture=None):
    from google import genai
    monkeypatch.setenv('GEMINI_API_KEY','test-not-a-key')
    monkeypatch.delenv('GEMINI_MODEL',raising=False)
    class Client:
        def __init__(self,**kwargs):
            self.models=self
            assert kwargs['api_key']=='test-not-a-key'
            assert kwargs['http_options'].timeout==30000
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def generate_content(self,**kwargs):
            if capture is not None: capture.update(kwargs)
            if fail: raise fail
            return SimpleNamespace(text=text,model_version=actual,candidates=[SimpleNamespace(finish_reason=finish)] if finish else [])
    monkeypatch.setattr(genai,'Client',Client)

def test_llm_schema_contract(monkeypatch):
    import json
    previous=Extraction(intent='meal_log',foods=[{'name':'eggs','quantity':None,'unit':'count'}],date=date(2026,11,12))
    expected=previous.model_copy(deep=True);expected.foods[0].quantity=2
    capture={};fake_gemini(monkeypatch,expected.model_dump_json(),capture=capture)
    assert llm([{'role':'user','content':'2'}],date(2026,11,12),previous)==expected
    assert capture['model']=='gemini-3.5-flash-lite'
    assert capture['config'].response_json_schema==Extraction.model_json_schema()
    assert capture['config'].response_mime_type=='application/json'
    context=json.loads(capture['contents'])
    assert context['pending_slot']=='foods.0.quantity'
    assert context['draft']==previous.model_dump(mode='json')
    assert context['reference_date']=='2026-11-12'

@pytest.mark.parametrize('text,finish,actual',[
    ('not json','STOP','gemini-3.5-flash-lite'),
    ('{"intent":"meal_log","foods":[{"name":"eggs","quantity":-2}]}','STOP','gemini-3.5-flash-lite'),
    ('{"intent":"unknown","unexpected":1}','STOP','gemini-3.5-flash-lite'),
    ('','STOP','gemini-3.5-flash-lite'),
    ('{}',None,'gemini-3.5-flash-lite'),
    ('{}','MAX_TOKENS','gemini-3.5-flash-lite'),
    ('{"intent":"unknown"}','STOP','gemini-3.8-flash'),
])
def test_gemini_rejects_invalid_blocked_or_rerouted(monkeypatch,text,finish,actual):
    fake_gemini(monkeypatch,text,finish,actual)
    with pytest.raises(RuntimeError): llm([{'role':'user','content':'eggs'}],date(2026,11,12))

@pytest.mark.parametrize('code',[400,401,403,404,429,500])
def test_gemini_provider_errors_are_sanitized(monkeypatch,code):
    from google.genai import errors
    fake_gemini(monkeypatch,'',fail=errors.APIError(code,{'message':'secret-provider-payload'}))
    with pytest.raises(RuntimeError) as exc: llm([],date(2026,11,12))
    assert 'secret-provider-payload' not in str(exc.value)

def test_gemini_config_ignores_openai_key(client,monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY',raising=False)
    monkeypatch.delenv('GEMINI_MODEL',raising=False)
    monkeypatch.setenv('OPENAI_API_KEY','old-unused-key')
    config=client.get('/config').json()
    assert not config['llm_configured']
    assert config['llm_provider']=='gemini' and config['llm_model']=='gemini-3.5-flash-lite'

def test_missing_credentials_and_provider_failure(client,monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY',raising=False)
    assert client.post('/extract',json={'text':'eggs'}).status_code==422
    def failure(*a): raise Exception('secret should never appear')
    monkeypatch.setattr(nutrition,'search',failure)
    r=client.get('/foods/search?q=eggs')
    assert r.status_code==502 and 'secret' not in r.text

def test_sqlite_restart(tmp_path):
    url=f'sqlite:///{tmp_path}/test.db'
    with TestClient(create_app(Store(url))) as c: s=start(c)
    with TestClient(create_app(Store(url))) as c: assert c.get('/conversations/'+s['id']).json()==s
