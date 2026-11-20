from datetime import date
import pytest
from sqlalchemy import select
from storage import Store,conversations,records
from migrate_sqlite import copy_rows

def test_migration_preserves_json_versions_dates_and_nulls():
 source=Store('sqlite:///:memory:');target=Store('sqlite:///:memory:')
 state={'id':'example','version':0,'status':'confirmed','messages':[{'content':'eggs'}]}
 source.create(state)
 payload={'extraction':{'date':'2026-11-14','intent':'meal_log'},'nutrition':{'0':{'nutrients':{'kcal':150,'fat_g':None}}}}
 source.save(state,0,payload)
 assert copy_rows(source.engine,target.engine)=={'conversations':1,'records':1}
 assert target.get('example')==source.get('example')
 assert target.history(date(2026,11,14),date(2026,11,14))==source.history(date(2026,11,14),date(2026,11,14))
 with pytest.raises(ValueError,match='not empty'):copy_rows(source.engine,target.engine)
 assert target.get('example')['version']==1

def test_migration_rejects_destination_with_only_records():
 source=Store('sqlite:///:memory:');target=Store('sqlite:///:memory:')
 with target.engine.begin() as c:c.execute(records.insert().values(id='existing',date=date(2026,1,1),kind='workout_log',payload={}))
 with pytest.raises(ValueError,match='not empty'):copy_rows(source.engine,target.engine)
 with target.engine.connect() as c:assert len(c.execute(select(records)).all())==1
