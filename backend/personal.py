"""Validated personal features; no generated nutrient totals or assumed portions."""
import re
from copy import deepcopy
from datetime import timedelta, date
from pydantic import Field, field_validator
from models import StrictModel, Extraction

KEYS=('kcal','protein_g','carbs_g','fat_g')
class Goals(StrictModel):
    kcal: float | None = Field(default=None, gt=0, le=20000)
    protein_g: float | None = Field(default=None, gt=0, le=2000)
    carbs_g: float | None = Field(default=None, gt=0, le=3000)
    fat_g: float | None = Field(default=None, gt=0, le=2000)

class FavoriteSave(StrictModel):
    record_id: str = Field(min_length=1,max_length=100)
    name: str = Field(min_length=1,max_length=60)
    @field_validator('name')
    @classmethod
    def clean_name(cls,v):
        v=' '.join(v.lower().split())
        if not re.fullmatch(r'[a-z0-9][a-z0-9 -]*',v):
            raise ValueError('Use letters, numbers, spaces or hyphens for the shortcut name.')
        return v

class FavoriteUse(StrictModel):
    date: date


def fraction_correction(text, previous):
    """Return (extraction, index, factor, question) or None for ordinary extraction.

    Only complete explicit fraction corrections are accepted. Ambiguity never
    falls through to a model that might pick a food or overwrite the draft.
    """
    if not previous or previous.intent!='meal_log': return None
    t=text.lower().strip().rstrip('.!')
    marker=re.search(r'\b(half|quarter|double|twice|three quarters|\d+\s*/\s*\d+)\b',t)
    if not marker: return None
    # New meals with fractional portions belong to normal extraction.
    if not re.search(r'\b(actually|instead|make|change|only|that|the|it)\b',t): return None
    m=re.fullmatch(r'(?:(?:actually[, ]*|i (?:only )?ate |only |make (?:it )?|change (?:it )?to )*)(half|a quarter|quarter|double|twice|three quarters|\d+\s*/\s*\d+)(?: (?:of )?(?:that|the|my|it|amount|portion|rice|[a-z -]+))?',t)
    if not m: return (previous,None,None,'Please correct one food at a time, for example “Actually, half of the rice.”')
    ratio=m[1]
    if '/' in ratio:
        a,b=map(int,ratio.replace(' ','').split('/')); factor=a/b if b else 0
    else: factor={'half':.5,'quarter':.25,'a quarter':.25,'double':2,'twice':2,'three quarters':.75}[ratio]
    if not 0<factor<=10: return (previous,None,None,'Please use a positive amount no more than ten times the current portion.')
    # Match a whole food name or distinctive words. Multiple matches ask, never guess.
    targets=[i for i,f in enumerate(previous.foods) if re.search(r'\b'+re.escape(f.name.lower())+r'\b',t)]
    if not targets:
        targets=[i for i,f in enumerate(previous.foods) if any(re.search(r'\b'+re.escape(w)+r'\b',t) for w in f.name.lower().split() if len(w)>2)]
    tail=t[m.end(1):].strip()
    if not targets and len(previous.foods)==1 and re.fullmatch(r'(?:of )?(?:(?:that|the|my) )?(?:it|amount|portion|that)?(?: instead)?',tail): targets=[0]
    if len(targets)!=1: return (previous,None,None,'Which food should I change? Include its name, such as “half of the rice instead.”')
    i=targets[0]; food=previous.foods[i]
    remainder=re.sub(r'^(?:of )?(?:(?:that|the|my) )?', '', tail)
    remainder=re.sub(r' instead$', '', remainder).strip()
    allowed={'','it','that','amount','portion',food.name.lower(),*food.name.lower().split()}
    if remainder not in allowed:
        return (previous,None,None,'Please change one portion at a time. Say “half of the rice”, then send any date or other changes separately.')
    if food.quantity is None: return (previous,None,None,f'I do not yet have an amount for {food.name}. How much did you eat, including the unit?')
    e=previous.model_copy(deep=True);e.foods[i].quantity*=factor
    e=Extraction.model_validate(e.model_dump())
    return (e,i,factor,None)


def scale_nutrition(value,factor):
    n=deepcopy(value)
    if n.get('grams') is not None:
        n['grams']=round(n['grams']*factor,3)
        if not 0<n['grams']<=100000: raise ValueError('Corrected portion is outside the supported weight range.')
    n['nutrients']={k:round(v*factor,3) if v is not None else None for k,v in n['nutrients'].items()}
    n['portion_source']=f'{factor:g} × previously reviewed amount ({value["portion_source"]})'
    return n


def weekly_summary(store,end,calendar=False):
    start=end-timedelta(days=end.weekday() if calendar else 6)
    previous_start=start-timedelta(days=7);previous_end=end-timedelta(days=7)
    def period(a,b):
        h=store.history(a,b)
        meals=[r for r in h['records'] if r['extraction']['intent']=='meal_log']
        return {k:v for k,v in h.items() if k!='records'} | {'meal_count':len(meals),'logged_days':len({r['date'] for r in meals})}
    current=period(start,end);previous=period(previous_start,previous_end)
    changes={}
    for k in KEYS:
        a=current['known_totals'][k];b=previous['known_totals'][k]
        comparable=bool(current['meal_count'] and previous['meal_count'] and not current['foods_missing_nutrients'][k] and not previous['foods_missing_nutrients'][k])
        changes[k]={'difference':round(a-b,3) if comparable else None,'percent':round((a-b)/b*100,1) if comparable and b else None}
    return {'current':current,'previous':previous,'changes':changes,'basis':'week_to_date' if calendar else 'rolling_seven_days','note':'Confirmed logs only. Days without meals are unlogged, not zero-intake days. Comparisons describe recorded totals, not complete dietary intake.'}


def summary_reply(s):
    a,b=s['current'],s['previous']
    lines=[f'Comparing {a["start"]}–{a["end"]} with {b["start"]}–{b["end"]}.',f'Meals logged on {a["logged_days"]} days versus {b["logged_days"]} days.']
    for k,label in zip(KEYS,['Calories','Protein','Carbs','Fat']):
        unit='kcal' if k=='kcal' else 'g'
        def value(p):
            if not p['meal_count']: return 'no meals logged'
            return f'{p["known_totals"][k]:g} {unit}'+(' known (incomplete)' if p['foods_missing_nutrients'][k] else ' logged')
        lines.append(f'{label}: {value(a)} versus {value(b)}.')
    return '\n'.join(lines)+'\n'+s['note']


def favorite_request(text):
    # Exact shortcut grammar prevents fuzzy names from logging an unintended meal.
    t=' '.join(text.lower().strip().rstrip('.!').split())
    m=re.fullmatch(r'(?:i (?:had|ate) |log |use )?(?:my )?usual (.+?)(?: (today|yesterday|\d{4}-\d{2}-\d{2}))?',t)
    return (m[1],m[2]) if m else None
