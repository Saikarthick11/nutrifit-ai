from datetime import date
import pytest
from fastapi.testclient import TestClient
from main import create_app
from storage import Store
from models import Extraction,Food
import main,personal,nutrition
from test_workflow import DATA,client

@pytest.fixture
def c(monkeypatch,client):
    monkeypatch.setattr(main,'today',lambda:date(2026,11,18))
    monkeypatch.setattr(nutrition,'detail',lambda _:DATA)
    yield client

def send(c,s,text):
    r=c.post(f'/conversations/{s["id"]}/messages',json={'version':s['version'],'text':text});assert r.status_code==200,r.text;return r.json()
def start(c):return c.post('/conversations',json={'mode':'baseline'}).json()
def confirm(c,s):return c.post(f'/conversations/{s["id"]}/confirm',json={'version':s['version']})
def meal(c):
    s=send(c,start(c),'I ate 200 grams rice today')
    r=c.post(f'/conversations/{s["id"]}/nutrition',json={'version':s['version'],'food_index':0,'fdc_id':123,'grams':200});assert r.status_code==200;return r.json()
def hist(c):return c.get('/history?start=2026-01-01&end=2026-12-31').json()

def test_half_correction_scales_verified_portion_then_confirms(c):
    s=meal(c);s=send(c,s,'Actually, I ate half of that rice')
    assert s['extraction']['foods'][0]['quantity']==100
    assert s['nutrition']['0']['grams']==100
    assert s['nutrition']['0']['nutrients']['kcal']==150
    assert hist(c)['records']==[]
    assert confirm(c,s).status_code==200
    assert hist(c)['known_totals']['kcal']==150

def test_ambiguous_fraction_and_invalid_fraction_do_not_change(c):
    s=send(c,start(c),'I ate 200 grams rice and 100 grams chicken today')
    for text in ['Actually half of that','Actually 1/0 of the rice','Actually half of the rice and chicken']:
        result=send(c,s,text);assert result['extraction']==s['extraction'];assert result['status']=='nutrition';s=result

def test_single_ambiguous_food_name_does_not_choose_between_two():
    e=Extraction(intent='meal_log',date=date(2026,11,18),foods=[Food(name='white rice',quantity=2,unit='cups'),Food(name='brown rice',quantity=1,unit='cups')])
    assert personal.fraction_correction('Actually half of the rice',e)[3]

def test_scaled_edit_preserves_original_until_confirm(c):
    original=confirm(c,meal(c)).json()
    draft=c.post(f'/records/{original["id"]}/edit',json={'mode':'baseline'}).json()
    draft=send(c,draft,'Actually half of the rice')
    assert hist(c)['known_totals']['kcal']==300
    assert confirm(c,draft).status_code==200
    assert len(hist(c)['records'])==1 and hist(c)['known_totals']['kcal']==150

def test_goals_validate_persist_and_clear(c):
    assert c.get('/goals').json()['kcal'] is None
    assert c.post('/goals',json={'kcal':2000,'protein_g':100}).json()['protein_g']==100
    assert c.get('/goals').json()['kcal']==2000
    assert c.post('/goals',json={'kcal':-1}).status_code==422
    assert c.post('/goals',json={'kcal':20001}).status_code==422
    assert c.post('/goals',json={}).json()['kcal'] is None

def test_favorite_only_from_confirmed_meal_and_unique(c):
    s=meal(c)
    assert c.post('/favorites',json={'record_id':s['id'],'name':'breakfast'}).status_code==422
    confirm(c,s)
    body={'record_id':s['id'],'name':' Breakfast '}
    r=c.post('/favorites',json=body);assert r.status_code==200;f=r.json();assert f['name']=='breakfast'
    assert c.post('/favorites',json=body).status_code==409
    draft=c.post(f'/favorites/{f["id"]}/use',json={'date':'2026-11-17'}).json()
    assert draft['status']=='ready' and draft['extraction']['date']=='2026-11-17'
    assert len(hist(c)['records'])==1
    assert confirm(c,draft).status_code==200
    assert len(hist(c)['records'])==2
    assert c.post(f'/favorites/{f["id"]}/use',json={'date':'2026-11-19'}).status_code==422
    assert c.post(f'/favorites/{f["id"]}/remove',json={}).status_code==200
    assert c.get('/favorites').json()==[]
    assert len(hist(c)['records'])==2

def test_usual_meal_chat_needs_date_and_confirmation(c):
    saved=confirm(c,meal(c)).json();c.post('/favorites',json={'record_id':saved['id'],'name':'lunch'})
    s=send(c,start(c),'I had my usual lunch')
    assert s['missing_fields']==['date']
    assert confirm(c,s).status_code==422
    s=send(c,s,'yesterday');assert s['status']=='ready'
    assert s['nutrition']['0']['grams']==200
    assert confirm(c,s).status_code==200
    s=send(c,start(c),'I had my usual lunch today');assert s['status']=='ready'
    missing=send(c,start(c),'I had my usual breakfast today');assert missing['extraction'] is None

def test_summary_dates_and_missing_data(c):
    empty=c.get('/summary/weekly?end=2026-11-18').json()
    assert empty['current']['start']=='2026-11-12'
    assert empty['previous']['end']=='2026-11-11'
    assert empty['changes']['kcal']=={'difference':None,'percent':None}
    confirm(c,meal(c))
    r=c.get('/summary/weekly?end=2026-11-18&calendar=true').json()
    assert r['current']['start']=='2026-11-16'
    assert r['previous']['start']=='2026-11-09' and r['previous']['end']=='2026-11-11'
    assert r['current']['logged_days']==1 and r['current']['known_totals']['kcal']==300
    assert c.get('/summary/weekly?end=2026-12-01').status_code==422
    s=send(c,start(c),'Compare my protein intake this week and last week')
    assert s['status']=='history' and '300 kcal' in s['reply'] and 'no meals logged' in s['reply']
    assert len(hist(c)['records'])==1

def test_summary_cannot_discard_pending_meal(c):
    s=meal(c);result=send(c,s,'Show weekly summary')
    assert result['extraction']==s['extraction'] and result['nutrition']==s['nutrition']

def test_scaled_unknown_nutrients_stay_unknown():
    n=personal.scale_nutrition({'grams':100,'portion_source':'reviewed','nutrients':{'kcal':None,'protein_g':10}},.5)
    assert n['nutrients']=={'kcal':None,'protein_g':5}


def test_wrong_named_food_does_not_change_only_food(c):
    s=meal(c);result=send(c,s,'Actually half of the chicken')
    assert result['extraction']==s['extraction']
    assert result['nutrition']==s['nutrition']


def test_weekly_comparison_math_and_unknowns(c):
    s=confirm(c,meal(c)).json()
    f=c.post('/favorites',json={'record_id':s['id'],'name':'rice'}).json()
    old=c.post(f'/favorites/{f["id"]}/use',json={'date':'2026-11-11'}).json()
    old=send(c,old,'Actually half of the rice')
    assert confirm(c,old).status_code==200
    report=c.get('/summary/weekly?end=2026-11-18').json()
    assert report['changes']['kcal']=={'difference':150,'percent':100}
    assert report['changes']['carbs_g']=={'difference':None,'percent':None}


def test_correction_rejects_stale_version(c):
    s=meal(c);send(c,s,'Actually half of the rice')
    r=c.post(f'/conversations/{s["id"]}/messages',json={'version':s['version'],'text':'Actually double the rice'})
    assert r.status_code==409


def test_fraction_does_not_silently_ignore_date_correction(c):
    s=meal(c);result=send(c,s,'Actually half of the rice yesterday')
    assert result['extraction']==s['extraction']
    assert 'separately' in result['reply']
