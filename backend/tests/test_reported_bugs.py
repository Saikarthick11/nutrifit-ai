from datetime import date
import pytest
import main
import nutrition
from models import Extraction
from extraction import clarification_help
from test_workflow import client,turn

@pytest.mark.parametrize('mode',['baseline','llm'])
def test_confusion_preserves_slots_and_explains(client,monkeypatch,mode):
 draft=Extraction(intent='meal_log',date=date(2026,11,16),foods=[{'name':'chicken fried rice'}])
 calls=[]
 def extractor(*args):
  calls.append(args)
  return draft
 monkeypatch.setattr(main,'llm' if mode=='llm' else 'baseline',extractor)
 s=client.post('/conversations',json={'mode':mode}).json()
 s=turn(client,s,"I ate chicken fried rice for today's lunch")
 original=s['extraction'];q=s['reply']
 s=turn(client,s,'what?')
 assert s['extraction']==original and s['extraction']['foods'][0]['quantity'] is None
 assert s['reply']!=q and '1 cup or 200 grams' in s['reply']
 assert len(calls)==1 and s['status']=='draft'
 assert client.post('/conversations/'+s['id']+'/confirm',json={'version':s['version']}).status_code==422
 assert client.get('/history?start=2026-01-01&end=2026-12-31').json()['records']==[]
 draft.foods[0].quantity=1;draft.foods[0].unit='cups'
 s=turn(client,s,'1 cup')
 assert s['status']=='nutrition' and len(calls)==2

def test_help_is_narrow_and_slot_specific():
 e=Extraction(intent='workout_log',workouts=[{'name':'running'}],date=date(2026,11,16))
 assert '20 minutes' in clarification_help('What do you mean?',e)
 assert clarification_help('What did I eat yesterday?',e) is None
 assert clarification_help('200 grams',e) is None
 e=Extraction(intent='meal_log',foods=[{'name':'rice','quantity':1}])
 assert 'unit' in clarification_help('what?',e)

PORTIONS={'fdcId':123,'description':'Fried rice','dataType':'Survey (FNDDS)','foodPortions':[
 {'id':1,'gramWeight':198,'measureUnit':{'name':'undetermined'},'modifier':'10205','portionDescription':'1 cup'},
 {'id':2,'gramWeight':198,'measureUnit':{'name':'undetermined'},'modifier':'90000','portionDescription':'Quantity not specified'},
 {'id':3,'gramWeight':100,'amount':2,'modifier':'large eggs'},
 {'id':4,'gramWeight':5,'measureUnit':{'name':'undetermined'},'modifier':'90000'}],
 'foodNutrients':[{'nutrient':{'id':1008,'unitName':'kcal'},'amount':175}]}

def test_portion_labels_and_unchanged_calculation():
 rows=nutrition.portions(PORTIONS)
 assert [r['id'] for r in rows]==[1,3]
 assert rows[0]['label']=='1 cup' and rows[0]['grams']==198
 assert rows[1]['label']=='2 large eggs'
 assert nutrition.calculate(PORTIONS,portion_id=1,portion_count=1.5)['grams']==297
 assert nutrition.calculate(PORTIONS,portion_id=1,portion_count=1.5)['nutrients']['kcal']==519.75
 with pytest.raises(ValueError):nutrition.calculate(PORTIONS,portion_id=2,portion_count=1)

def test_clean_labels_in_api(client,monkeypatch):
 monkeypatch.setattr(nutrition,'detail',lambda _:PORTIONS)
 rows=client.get('/foods/123').json()['portions']
 assert rows[0]['label']=='1 cup'
 assert 'undetermined' not in str(rows) and '90000' not in str(rows)
