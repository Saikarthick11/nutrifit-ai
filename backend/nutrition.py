import math
import re
import os
import httpx

BASE = 'https://api.nal.usda.gov/fdc/v1'
SUPPORTED = ['Foundation', 'SR Legacy', 'Survey (FNDDS)']

def request(path, params=None):
    key = os.getenv('USDA_API_KEY')
    if not key: raise RuntimeError('Set USDA_API_KEY in backend/.env for nutrition lookup.')
    with httpx.Client(timeout=20) as client:
        response = client.get(BASE+path,params={'api_key':key,**(params or {})})
        response.raise_for_status()
        return response.json()

def search(query):
    data = request('/foods/search',{'query':query,'pageSize':8,'dataType':','.join(SUPPORTED)})
    return [{'fdc_id':f['fdcId'],'description':f['description'],'data_type':f['dataType']} for f in data.get('foods',[]) if f.get('dataType') in SUPPORTED]

def detail(fdc_id):
    data = request(f'/food/{fdc_id}')
    if data.get('dataType') not in SUPPORTED:
        raise ValueError('Select a Foundation, SR Legacy, or FNDDS food; branded serving bases are outside this MVP.')
    return data

def portions(data):
    result=[]
    for p in data.get('foodPortions',[]):
        grams=p.get('gramWeight')
        if p.get('id') is None or not isinstance(grams,(int,float)) or not math.isfinite(grams) or grams<=0: continue
        unit=str((p.get('measureUnit') or {}).get('name') or '').strip()
        modifier=str(p.get('modifier') or '').strip()
        description=str(p.get('portionDescription') or '').strip()
        # FNDDS modifiers can be internal codes, with the real serving in the description.
        if modifier.isdigit(): modifier=''
        if unit.lower() in ('undetermined','unknown','not applicable'): unit=''
        if re.search(r'quantity not specified|amount not specified|not specified|^unspecified$',description+' '+modifier,re.I): continue
        amount=p.get('amount')
        prefix=f'{amount:g}' if isinstance(amount,(int,float)) and math.isfinite(amount) and amount>0 else ''
        if description:
            label=description
            # A description such as "1 cup" already carries its own amount.
            if not re.match(r'^\d',label) and prefix: label=' '.join(x for x in (prefix,unit,label) if x)
        else:
            label=' '.join(x for x in (prefix,unit,modifier) if x)
        if not label or not re.search(r'[a-zA-Z]',label): continue
        result.append({'id':p['id'],'amount':amount,'grams':grams,'label':label})
    return result

def calculate(data, grams=None, portion_id=None, portion_count=None):
    source = 'user-provided gram weight'
    if grams is not None:
        if portion_id is not None or portion_count is not None: raise ValueError('Choose either grams or a USDA portion, not both.')
    else:
        p = next((p for p in portions(data) if p['id']==portion_id),None)
        if not p or portion_count is None: raise ValueError('Provide grams or select a USDA portion and its number of servings.')
        # Each selected portion row is a complete USDA serving, including its amount.
        grams = p['grams'] * portion_count
        source = f'USDA portion {portion_id}: {p["label"]}; {portion_count} servings × {p["grams"]} g'
    if not math.isfinite(grams) or not 0 < grams <= 100000: raise ValueError('Invalid gram weight.')
    by_id = {n.get('nutrient',{}).get('id'):n for n in data.get('foodNutrients',[])}
    ids = {'kcal':[1008,2048,2047],'protein_g':[1003],'carbs_g':[1005],'fat_g':[1004]}
    totals = {}
    for key, choices in ids.items():
        n = next((by_id[i] for i in choices if i in by_id and by_id[i].get('amount') is not None),None)
        expected = 'kcal' if key=='kcal' else 'g'
        totals[key] = round(n['amount']*grams/100,3) if n and n['nutrient'].get('unitName','').lower()==expected else None
    return {'fdc_id':data['fdcId'],'description':data['description'],'data_type':data['dataType'],'grams':grams,'portion_source':source,'nutrients':totals,'source_url':f'https://fdc.nal.usda.gov/food-details/{data["fdcId"]}/nutrients'}
