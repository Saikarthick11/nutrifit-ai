import io
import pytest
from PIL import Image
from test_workflow import client
import label_ocr
VALUES={'product_name':'Test crackers','serving_description':'2 crackers (30 g)','serving_grams':30,'basis':'per_serving','kcal':120,'protein_g':3,'carbs_g':20,'fat_g':None,'amount':2,'date':'2026-01-01','reviewed':True}
def test_image_validation():
 for data,mime in [(b'not-image','image/png'),(b'x','text/html'),(b'x'*(label_ocr.MAX_IMAGE_BYTES+1),'image/jpeg')]:
  with pytest.raises(ValueError):label_ocr.normalize_image(data,mime)
 out=io.BytesIO();Image.new('RGB',(20,20),'white').save(out,format='PNG')
 assert Image.open(io.BytesIO(label_ocr.normalize_image(out.getvalue(),'image/png'))).format=='JPEG'
def test_label_draft_confirm_history_and_edit(client):
 s=client.post('/labels/draft',json=VALUES).json()
 assert s['status']=='ready' and s['nutrition']['0']['nutrients']['kcal']==240
 assert s['nutrition']['0']['nutrients']['fat_g'] is None
 assert client.get('/history?start=2026-01-01&end=2026-01-01').json()['records']==[]
 assert client.post('/conversations/'+s['id']+'/messages',json={'version':s['version'],'text':'3'}).status_code==422
 path='/conversations/'+s['id']+'/confirm'
 assert client.post(path,json={'version':s['version']}).status_code==200
 assert client.post(path,json={'version':s['version']}).status_code==200
 edited=client.post('/records/'+s['id']+'/edit',json={'mode':'llm'}).json()
 assert edited['label_review']['amount']==2
 updated=client.post('/conversations/'+edited['id']+'/label-review',json={**VALUES,'amount':3,'version':edited['version']}).json()
 assert updated['nutrition']['0']['nutrients']['kcal']==360
 assert client.post('/conversations/'+edited['id']+'/confirm',json={'version':updated['version']}).status_code==200
 h=client.get('/history?start=2026-01-01&end=2026-01-01').json()
 assert len(h['records'])==1 and h['known_totals']['kcal']==360
 assert client.get('/conversations/'+s['id']).json()['label_review']['amount']==3

def test_per_100g_arithmetic_and_unknown_weight(client):
 s=client.post('/labels/draft',json={**VALUES,'basis':'per_100g','amount':45}).json()
 assert s['nutrition']['0']['nutrients']['kcal']==54 and s['nutrition']['0']['grams']==45
 s=client.post('/labels/draft',json={**VALUES,'serving_grams':None}).json()
 assert s['nutrition']['0']['grams'] is None
@pytest.mark.parametrize('change',[{'reviewed':False},{'basis':'unknown'},{'amount':0},{'kcal':-1},{'date':'2099-01-01'},{'kcal':None,'protein_g':None,'carbs_g':None,'fat_g':None},{'product_name':' '}])
def test_invalid_reviews(client,change):assert client.post('/labels/draft',json={**VALUES,**change}).status_code==422

def test_upload_bound_and_no_persistence(client,monkeypatch):
 monkeypatch.setattr(label_ocr,'extract',lambda data,mime:label_ocr.Label(readable=False,warnings=['No nutrition label']))
 r=client.post('/labels/extract',content=b'image-placeholder',headers={'Content-Type':'image/png'})
 assert r.status_code==200 and not r.json()['readable']
 r=client.post('/labels/extract',content=b'x'*(label_ocr.MAX_IMAGE_BYTES+1),headers={'Content-Type':'image/png'})
 assert r.status_code==413
 assert client.get('/history?start=2000-01-01&end=2099-01-01').json()['records']==[]

def test_ocr_provider_contract(monkeypatch):
 from test_workflow import fake_gemini
 capture={};fake_gemini(monkeypatch,label_ocr.Label(readable=True,basis='per_serving',kcal=120).model_dump_json(),capture=capture)
 out=io.BytesIO();Image.new('RGB',(30,30),'white').save(out,format='PNG')
 assert label_ocr.extract(out.getvalue(),'image/png').kcal==120
 assert capture['contents'][0].inline_data.mime_type=='image/jpeg'
 assert capture['config'].response_json_schema==label_ocr.Label.model_json_schema()
 fake_gemini(monkeypatch,'{"readable":true,"kcal":-10}')
 with pytest.raises(RuntimeError):label_ocr.extract(out.getvalue(),'image/png')
