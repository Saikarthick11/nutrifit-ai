"""Validate annotations and split integrity without invoking either extractor."""
import hashlib,json,sys
from pathlib import Path
from collections import Counter,defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
from models import Extraction
from extraction import missing_slots

def validate(root):
    manifest=json.loads((root/'manifest.json').read_text())
    groups=defaultdict(set);ids=set();texts=set();all_cases=[]
    for split,name,n in [('development','development.json',30),('test','test_candidate.json',70)]:
        data=(root/name).read_bytes()
        assert hashlib.sha256(data).hexdigest()==manifest['files'][name],f'{name}: hash mismatch; regenerate manifest after reviewed edits'
        cases=json.loads(data);assert len(cases)==n
        for c in cases:
            assert c['id'] not in ids,f'Duplicate id {c["id"]}';ids.add(c['id'])
            text=' '.join(c['text'].casefold().split()).rstrip('.!?')
            assert text not in texts,f'Duplicate input {c["id"]}';texts.add(text)
            assert c['split']==split and c['reference_date']=='2026-11-25'
            groups[c['family_id']].add(split)
            initial=Extraction.model_validate(c['initial_expected']);final=Extraction.model_validate(c['expected'])
            assert initial.model_dump(mode='json')==c['initial_expected']
            assert final.model_dump(mode='json')==c['expected']
            for value in [initial,final]:
                if value.date and value.end_date:assert value.end_date>=value.date
                if value.date:assert value.date.isoformat()<=c['reference_date']
                if value.end_date:assert value.end_date.isoformat()<=c['reference_date']
            assert set(c['answers']).issubset(set(missing_slots(initial))),f'{c["id"]}: answer for a nonmissing initial slot'
            assert all(isinstance(a,str) and a.strip() for a in c['answers'].values())
            if c['category']=='complete_meal':assert initial.intent=='meal_log' and not missing_slots(initial)
            if c['category']=='missing_meal':assert initial.intent=='meal_log' and missing_slots(initial)
            if c['category']=='workout':assert initial.intent=='workout_log'
            if c['category']=='history':assert initial.intent=='history'
            if c['answers']:assert not missing_slots(final),f'{c["id"]}: answered case still missing final fields'
            assert c['label_note'] and c['review_status']=='pending_human_review'
            all_cases.append(c)
    assert all(len(s)==1 for s in groups.values()),'A family crosses splits'
    assert Counter(c['category'] for c in all_cases)==dict(complete_meal=25,missing_meal=25,workout=20,history=15,challenge=15)
    assert len(all_cases)==100
    print('PASS: 100 schema-valid cases; 30 development / 70 proposed test; unique IDs and inputs; family separation; answer keys; dates; SHA-256 hashes.')
    print('Human label and semantic near-duplicate review remains required. No models were run.')

if __name__=='__main__':validate(Path(__file__).with_name('datasets')/'v1')
