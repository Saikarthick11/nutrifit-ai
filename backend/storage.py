import os
from datetime import date
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, JSON, Date, select, update
from sqlalchemy.pool import StaticPool

metadata = MetaData()
conversations = Table('conversations',metadata,Column('id',String,primary_key=True),Column('version',Integer,nullable=False),Column('state',JSON,nullable=False))
records = Table('records',metadata,Column('id',String,primary_key=True),Column('date',Date,nullable=False),Column('kind',String,nullable=False),Column('payload',JSON,nullable=False))

preferences = Table('preferences',metadata,Column('id',String,primary_key=True),Column('value',JSON,nullable=False))
favorites = Table('favorites',metadata,Column('id',String,primary_key=True),Column('name',String,nullable=False,unique=True),Column('payload',JSON,nullable=False))

class Conflict(Exception): pass

class Store:
    def __init__(self,url=None):
        url = url or os.getenv('DATABASE_URL','sqlite:///nutrifit.db')
        if url.startswith('postgresql://'): url = url.replace('postgresql://','postgresql+psycopg://',1)
        options = {'connect_args':{'check_same_thread':False}} if url.startswith('sqlite') else {}
        if url.endswith(':memory:'): options['poolclass']=StaticPool
        self.engine = create_engine(url,**options)
        metadata.create_all(self.engine)
    def create(self,state):
        with self.engine.begin() as c: c.execute(conversations.insert().values(id=state['id'],version=0,state=state))
        return state
    def get(self,id):
        with self.engine.connect() as c:
            row = c.execute(select(conversations.c.state).where(conversations.c.id==id)).first()
            return row[0] if row else None
    def save(self,state,version,record=None):
        state['version']=version+1
        with self.engine.begin() as c:
            changed = c.execute(update(conversations).where(conversations.c.id==state['id'],conversations.c.version==version).values(version=version+1,state=state))
            if changed.rowcount != 1: raise Conflict('Conversation changed. Reload it and try again.')
            if record and state.get('edit_source'):
                source_id=state['edit_source']
                source=c.execute(select(conversations.c.state).where(conversations.c.id==source_id)).scalar_one()
                expected=state['edit_source_version']
                source.update(extraction=state['extraction'],nutrition=state['nutrition'],version=expected+1)
                if state.get('label_review'): source['label_review']=state['label_review']
                else: source.pop('label_review',None)
                changed=c.execute(update(conversations).where(conversations.c.id==source_id,conversations.c.version==expected).values(version=expected+1,state=source))
                if changed.rowcount!=1: raise Conflict('This saved entry was edited elsewhere. Start a new edit from the journal.')
                changed=c.execute(update(records).where(records.c.id==source_id).values(date=date.fromisoformat(record['extraction']['date']),kind=record['extraction']['intent'],payload=record))
                if changed.rowcount!=1: raise Conflict('Saved entry no longer exists.')
            elif record:
                c.execute(records.insert().values(id=state['id'],date=date.fromisoformat(record['extraction']['date']),kind=record['extraction']['intent'],payload=record))
        return state
    def record_exists(self,id):
        with self.engine.connect() as c:
            return c.execute(select(records.c.id).where(records.c.id==id)).first() is not None
    def history(self,start,end):
        with self.engine.connect() as c:
            rows = c.execute(select(records.c.id,records.c.date,records.c.payload).where(records.c.date>=start,records.c.date<=end).order_by(records.c.date,records.c.id)).all()
        items = [{'id':r.id,'date':r.date.isoformat(),**r.payload} for r in rows]
        totals = {k:0.0 for k in ['kcal','protein_g','carbs_g','fat_g']}
        unknown = {k:0 for k in totals}
        for r in items:
            for food in r.get('nutrition',{}).values():
                for k in totals:
                    value=food['nutrients'].get(k)
                    if value is None: unknown[k]+=1
                    else: totals[k]+=value
        return {'start':start.isoformat(),'end':end.isoformat(),'records':items,'known_totals':{k:round(v,3) for k,v in totals.items()},'foods_missing_nutrients':unknown}

    def goals(self):
        with self.engine.connect() as c:
            return c.execute(select(preferences.c.value).where(preferences.c.id=='goals')).scalar_one_or_none() or {k:None for k in ('kcal','protein_g','carbs_g','fat_g')}
    def set_goals(self,value):
        # Atomic upsert for both supported databases.
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        from sqlalchemy.dialects.sqlite import insert as sqlite_insert
        insert=pg_insert if self.engine.dialect.name=='postgresql' else sqlite_insert
        with self.engine.begin() as c:
            stmt=insert(preferences).values(id='goals',value=value)
            c.execute(stmt.on_conflict_do_update(index_elements=['id'],set_={'value':value}))
        return value
    def favorites(self):
        with self.engine.connect() as c:
            return [dict(r._mapping) for r in c.execute(select(favorites).order_by(favorites.c.name))]
    def add_favorite(self,id,name,record_id):
        from sqlalchemy.exc import IntegrityError
        with self.engine.begin() as c:
            payload=c.execute(select(records.c.payload).where(records.c.id==record_id)).scalar_one_or_none()
            if not payload or payload['extraction']['intent']!='meal_log': raise ValueError('Choose a confirmed meal to save as a shortcut.')
            try: c.execute(favorites.insert().values(id=id,name=name,payload=payload))
            except IntegrityError: raise Conflict('That shortcut name already exists. Choose another name or remove the old shortcut.') from None
        return {'id':id,'name':name,'payload':payload}
    def remove_favorite(self,id):
        with self.engine.begin() as c: return c.execute(favorites.delete().where(favorites.c.id==id)).rowcount>0
