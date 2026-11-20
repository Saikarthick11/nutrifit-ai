from test_workflow import client,start,turn,DATA
import nutrition

def history(c): return c.get('/history?start=2000-01-01&end=2099-01-01').json()
def confirm(c,s): return c.post('/conversations/'+s['id']+'/confirm',json={'version':s['version']})
def saved_workout(c):
 s=turn(c,start(c),'I ran 30 minutes today')
 return confirm(c,s).json()
def edit(c,s):
 r=c.post('/records/'+s['id']+'/edit',json={'mode':'baseline'})
 assert r.status_code==200,r.text
 return r.json()
def test_edit_is_draft_and_replaces_once(client):
 original=saved_workout(client);draft=edit(client,original)
 draft=turn(client,draft,'I walked 45 minutes yesterday')
 assert history(client)['records'][0]['extraction']==original['extraction']
 result=confirm(client,draft);assert result.status_code==200,result.text
 assert confirm(client,draft).status_code==200
 records=history(client)['records'];assert len(records)==1
 assert records[0]['id']==original['id']
 assert records[0]['extraction']['workouts'][0]['duration_minutes']==45
 assert records[0]['date']==draft['extraction']['date']
 assert client.get('/conversations/'+original['id']).json()['extraction']==draft['extraction']
def test_two_edits_cannot_overwrite(client):
 original=saved_workout(client);a=edit(client,original);b=edit(client,original)
 a=turn(client,a,'I ran 40 minutes today');b=turn(client,b,'I ran 60 minutes today')
 assert confirm(client,a).status_code==200
 assert confirm(client,b).status_code==409
 assert history(client)['records'][0]['extraction']['workouts'][0]['duration_minutes']==40
 assert client.get('/conversations/'+b['id']).json()['status']=='ready'
 fresh=edit(client,original)
 assert fresh['extraction']['workouts'][0]['duration_minutes']==40
 assert confirm(client,fresh).status_code==200
 assert len(history(client)['records'])==1

def test_edit_meal_requires_reverification_and_recalculates(client,monkeypatch):
 monkeypatch.setattr(nutrition,'detail',lambda _:DATA)
 s=turn(client,start(client),'I ate 2 eggs today')
 def portion(s,grams):return client.post('/conversations/'+s['id']+'/nutrition',json={'version':s['version'],'food_index':0,'fdc_id':123,'grams':grams}).json()
 s=confirm(client,portion(s,100)).json();draft=turn(client,edit(client,s),'I ate 3 eggs today')
 assert draft['nutrition']=={}
 assert confirm(client,draft).status_code==422
 assert history(client)['known_totals']['kcal']==150
 assert confirm(client,portion(draft,150)).status_code==200
 assert history(client)['known_totals']['kcal']==225
 assert len(history(client)['records'])==1

def test_only_saved_entries_can_be_edited(client):
 assert client.post('/records/missing/edit',json={}).status_code==404
 s=start(client)
 assert client.post('/records/'+s['id']+'/edit',json={}).status_code==404
 s=saved_workout(client);draft=edit(client,s)
 assert client.post('/conversations/'+draft['id']+'/messages',json={'version':draft['version'],'text':'Show nutrition yesterday'}).status_code==422
 assert len(history(client)['records'])==1
