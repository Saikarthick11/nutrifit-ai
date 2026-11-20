import os
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from models import Message, Turn, Start, Selection, Confirm, Extraction
from extraction import baseline, llm, missing_slots, question, gemini_model, clarification_help
from storage import Store, Conflict
import nutrition
import label_ocr
import personal
import re
from copy import deepcopy

load_dotenv(Path(__file__).with_name('.env'))

def today(): return datetime.now(ZoneInfo(os.getenv('APP_TIMEZONE','America/New_York'))).date()

def create_app(store=None):
    @asynccontextmanager
    async def lifespan(app):
        app.state.store = store or Store()
        yield
    app = FastAPI(title='NutriFit AI',lifespan=lifespan)
    app.add_middleware(CORSMiddleware,allow_origins=[os.getenv('FRONTEND_ORIGIN','http://localhost:5173')],allow_methods=['GET','POST'],allow_headers=['Content-Type'])
    def get(id,version=None):
        state = app.state.store.get(id)
        if state is None: raise HTTPException(404,'Conversation not found')
        if version is not None and version!=state['version']: raise HTTPException(409,'Conversation changed. Reload and try again.')
        return state
    def save(state,version,record=None):
        try: return app.state.store.save(state,version,record)
        except Conflict as e: raise HTTPException(409,str(e)) from None
    def external(fn,*args,**kwargs):
        try: return fn(*args,**kwargs)
        except (ValueError,RuntimeError) as e: raise HTTPException(422,str(e)) from None
        except Exception:
            # Provider exception strings may contain keys or request content.
            raise HTTPException(502,'External service failed. Check credentials/network and retry.') from None
    def active(s):
        if s['status']=='confirmed': raise HTTPException(409,'This entry is already saved. Start a new conversation.')
    @app.get('/')
    def home(): return {'message':'Welcome to NutriFit AI','docs':'/docs'}
    @app.get('/health')
    def health(): return {'status':'ok'}
    @app.get('/config')
    def config(): return {'llm_provider':'gemini','llm_model':gemini_model(),'llm_configured':bool(os.getenv('GEMINI_API_KEY', '').strip()),'usda_configured':bool(os.getenv('USDA_API_KEY')),'database':app.state.store.engine.dialect.name,'timezone':os.getenv('APP_TIMEZONE','America/New_York')}
    @app.post('/baseline/extract')
    def extract(message:Message):
        e=external(baseline,message.text,today())
        missing=[f'quantity:{f.name}' for f in e.foods if f.quantity is None]
        # Preserve the original baseline endpoint contract for the initial experiment.
        return {'intent':e.intent,'foods':[f.model_dump() for f in e.foods],'missing_fields':missing,'clarification_question':f'How many {missing[0].split(":")[1]} did you eat?' if missing else None}
    @app.post('/extract')
    def extract_llm(message:Message): return external(llm,[{'role':'user','content':message.text}],today())
    @app.post('/labels/extract')
    async def extract_label(request:Request):
        from starlette.concurrency import run_in_threadpool
        data=bytearray()
        async for chunk in request.stream():
            data.extend(chunk)
            if len(data)>label_ocr.MAX_IMAGE_BYTES: raise HTTPException(413,'Choose an image smaller than 6 MB.')
        result=await run_in_threadpool(external,label_ocr.extract,bytes(data),request.headers.get('content-type','').split(';')[0])
        return result.model_dump(mode='json')
    def review_values(body):
        if body.date>today(): raise HTTPException(422,'Only completed meals can be logged.')
        return label_ocr.build_review(body)
    @app.post('/labels/draft')
    def label_draft(body:label_ocr.Review):
        extraction,values=review_values(body)
        reply='Label values reviewed. Check the consumed amount and date, then Confirm and save.'
        return app.state.store.create({'id':str(uuid4()),'version':0,'mode':'llm','status':'ready',
            'messages':[{'role':'assistant','content':reply}],'extraction':extraction,'nutrition':values,
            'label_review':body.model_dump(mode='json'),'missing_fields':[],'reply':reply})
    @app.post('/conversations/{id}/label-review')
    def update_label(id:str,body:label_ocr.UpdateReview):
        s=get(id,body.version);active(s)
        if not s.get('label_review'): raise HTTPException(422,'This is not a label entry.')
        extraction,values=review_values(body)
        s.update(extraction=extraction,nutrition=values,label_review=body.model_dump(mode='json',exclude={'version'}),status='ready')
        return save(s,body.version)
    @app.post('/conversations')
    def start(body:Start):
        return app.state.store.create({'id':str(uuid4()),'version':0,'mode':body.mode,'status':'draft','messages':[],'extraction':None,'nutrition':{},'missing_fields':[],'reply':'Tell me what you ate or how you exercised, including the date.'})
    @app.post('/records/{id}/edit')
    def edit_record(id:str,body:Start):
        source=get(id)
        if source['status']!='confirmed' or not app.state.store.record_exists(id):
            raise HTTPException(404,'Saved entry not found.')
        reply=('Editing a saved label entry. Choose Review label values to change the amount, date or nutrition.' if source.get('label_review') else 'Editing a saved entry. Tell me what to change, then review and save changes.')+' Your original entry stays unchanged until confirmation.'
        return app.state.store.create({'id':str(uuid4()),'version':0,'mode':body.mode,
            'status':'ready','messages':[{'role':'assistant','content':reply}],
            'extraction':source['extraction'],'nutrition':source['nutrition'],'missing_fields':[],
            'reply':reply,'edit_source':id,'edit_source_version':source['version'],**({'label_review':source['label_review']} if source.get('label_review') else {})})
    @app.get('/conversations/{id}')
    def conversation(id:str): return get(id)
    @app.post('/conversations/{id}/messages')
    def message(id:str,body:Turn):
        s=get(id,body.version); active(s)
        if s.get('label_review'): raise HTTPException(422,'Use Review label values to correct this label entry.')
        if len(s['messages'])>=40: raise HTTPException(422,'Please start a new conversation; the 20-turn limit has been reached.')
        previous=Extraction.model_validate(s['extraction']) if s['extraction'] else None
        messages=s['messages']+[{'role':'user','content':body.text}]
        help_reply=clarification_help(body.text,previous)
        if help_reply:
            s['reply']=help_reply
            s['messages']=messages+[{'role':'assistant','content':help_reply}]
            return save(s,body.version)
        def reply_only(reply):
            s['reply']=reply;s['messages']=messages+[{'role':'assistant','content':reply}]
            return save(s,body.version)
        normalized=body.text.lower()
        weekly_request=bool(re.search(r'\b(compare|summary|summarize)\b',normalized) and re.search(r'\bweek(?:ly)?\b',normalized))
        if weekly_request:
            if s.get('edit_source') or (previous and previous.intent in ['meal_log','workout_log']):
                return reply_only('Please finish or cancel this entry, then start a new chat for your weekly summary.')
            report=personal.weekly_summary(app.state.store,today(),calendar='this week' in normalized or 'last week' in normalized)
            s.update(status='history',weekly_summary=report,extraction=None,nutrition={},missing_fields=[])
            return reply_only(personal.summary_reply(report))
        request=personal.favorite_request(body.text)
        correction=external(personal.fraction_correction,body.text,previous)
        nutrition_override=None
        if request:
            if s.get('edit_source') or (previous and previous.intent in ['meal_log','workout_log']):
                return reply_only('Please finish or cancel this entry, then start a new chat to use a usual meal.')
            name,date_text=request
            favorite=next((f for f in app.state.store.favorites() if f['name']==name),None)
            if not favorite:
                return reply_only(f'No shortcut named “{name}” is saved. In My journal, open a confirmed meal and save it with that name.')
            day=today() if date_text=='today' else today()-timedelta(days=1) if date_text=='yesterday' else external(date.fromisoformat,date_text) if date_text else None
            e,nutrition_override=favorite_draft(favorite,day)
        elif correction:
            e,index,factor,help_text=correction
            if help_text: return reply_only(help_text)
            nutrition_override=deepcopy(s['nutrition'])
            if str(index) in nutrition_override:
                nutrition_override[str(index)]=external(personal.scale_nutrition,nutrition_override[str(index)],factor)
        else:
            e=external(llm,messages,today(),previous) if s['mode']=='llm' else external(baseline,body.text,today(),previous)
        s.pop('weekly_summary',None)
        if s.get('edit_source') and e.intent not in ['meal_log','workout_log']:
            raise HTTPException(422,'An edit must remain a meal or workout. Describe the corrected entry.')
        if e.date and e.end_date and e.end_date<e.date: raise HTTPException(422,'End date must be on or after start date.')
        if e.intent in ['meal_log','workout_log'] and e.date and e.date>today(): raise HTTPException(422,'Only completed meals and workouts can be logged.')
        if nutrition_override is not None: s['nutrition']=nutrition_override
        elif previous is None or previous.foods!=e.foods: s['nutrition']={}
        s.pop('history',None)
        s.update(extraction=e.model_dump(mode='json'),missing_fields=missing_slots(e),status='draft')
        reply=question(e)
        if not reply and e.intent=='history':
            s['history']=app.state.store.history(e.date,e.end_date)
            s['status']='history'
            reply='Here are your confirmed records and known nutrient totals for that date range.'
        elif not reply and e.intent=='meal_log' and len(s['nutrition'])!=len(e.foods):
            s['status']='nutrition'; reply='Choose a USDA match and verify the portion for each food below.'
        elif not reply:
            s['status']='ready'; reply=('The corrected portion uses the same reviewed food and proportional nutrition. ' if correction else 'Loaded the saved meal and portions. ' if request else '')+'Review the draft below, then select Confirm and save.'
        s['reply']=reply; s['messages']=messages+[{'role':'assistant','content':reply}]
        return save(s,body.version)
    @app.get('/goals')
    def goals(): return app.state.store.goals()
    @app.post('/goals')
    def set_goals(body:personal.Goals): return app.state.store.set_goals(body.model_dump())
    @app.get('/favorites')
    def favorites(): return app.state.store.favorites()
    @app.post('/favorites')
    def add_favorite(body:personal.FavoriteSave):
        try: return app.state.store.add_favorite(str(uuid4()),body.name,body.record_id)
        except ValueError as exc: raise HTTPException(422,str(exc)) from None
        except Conflict as exc: raise HTTPException(409,str(exc)) from None
    @app.post('/favorites/{id}/remove')
    def remove_favorite(id:str):
        if not app.state.store.remove_favorite(id): raise HTTPException(404,'Shortcut not found.')
        return {'removed':True}
    def favorite_draft(favorite,day):
        if day and day>today(): raise HTTPException(422,'Only completed meals can be logged.')
        e=Extraction.model_validate(deepcopy(favorite['payload']['extraction']))
        e.date=day;e.end_date=None
        return e,deepcopy(favorite['payload']['nutrition'])
    @app.post('/favorites/{id}/use')
    def use_favorite(id:str,body:personal.FavoriteUse):
        f=next((f for f in app.state.store.favorites() if f['id']==id),None)
        if not f: raise HTTPException(404,'Shortcut not found.')
        e,n=favorite_draft(f,body.date)
        reply=f'Loaded your usual {f["name"]} with its saved portions. Review the amount and date, then confirm to save.'
        return app.state.store.create({'id':str(uuid4()),'version':0,'mode':'llm','status':'ready','messages':[{'role':'assistant','content':reply}],
            'extraction':e.model_dump(mode='json'),'nutrition':n,'missing_fields':[],'reply':reply})
    @app.get('/summary/weekly')
    def weekly(end:date,calendar:bool=False):
        if end>today(): raise HTTPException(422,'Choose today or a past date.')
        return personal.weekly_summary(app.state.store,end,calendar)
    @app.get('/foods/search')
    def foods(q:str=Query(min_length=1,max_length=200)): return external(nutrition.search,q)
    @app.get('/foods/{fdc_id}')
    def food(fdc_id:int):
        d=external(nutrition.detail,fdc_id)
        return {'fdc_id':d['fdcId'],'description':d['description'],'portions':nutrition.portions(d)}
    @app.post('/conversations/{id}/nutrition')
    def select_food(id:str,body:Selection):
        s=get(id,body.version); active(s)
        if s.get('label_review'): raise HTTPException(422,'Use the label review form for this entry.')
        e=Extraction.model_validate(s['extraction']) if s['extraction'] else None
        if not e or e.intent!='meal_log' or missing_slots(e) or body.food_index>=len(e.foods): raise HTTPException(422,'Complete the meal draft before selecting nutrition.')
        d=external(nutrition.detail,body.fdc_id)
        n=external(nutrition.calculate,d,body.grams,body.portion_id,body.portion_count)
        s['nutrition'][str(body.food_index)]=n
        if len(s['nutrition'])==len(e.foods):
            s['status']='ready';s['reply']='All portions verified. Review the food matches and gram weights, then Confirm and save.'
        return save(s,body.version)
    @app.post('/conversations/{id}/confirm')
    def confirm(id:str,body:Confirm):
        s=get(id)
        if s['status']=='confirmed': return s  # Retry is idempotent; never duplicates a record.
        if s['version']!=body.version: raise HTTPException(409,'Draft changed; review it again.')
        if s['status']!='ready': raise HTTPException(422,'Complete all missing slots and nutrition portions before confirmation.')
        s['status']='confirmed';s['reply']='Changes saved. Your history has been updated.' if s.get('edit_source') else 'Saved. This entry is now included in your history.'
        return save(s,body.version,{'extraction':s['extraction'],'nutrition':s['nutrition']})
    @app.get('/history')
    def history(start:date,end:date):
        if end<start: raise HTTPException(422,'End date must be on or after start date.')
        return app.state.store.history(start,end)
    return app

app=create_app()
