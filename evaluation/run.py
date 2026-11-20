"""Paired 2x2 smoke benchmark. No nutrition calls and no records saved."""
import argparse
import hashlib
import json
import os
import platform
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
from dotenv import load_dotenv
from extraction import baseline, llm, missing_slots, question, PROMPT_VERSION, PROMPT, gemini_model
from models import Extraction
load_dotenv(Path(__file__).resolve().parents[1]/'backend'/'.env')

def flatten(value,prefix=''):
    if isinstance(value,dict):
        return {p:v for k,x in value.items() for p,v in flatten(x,f'{prefix}.{k}' if prefix else k).items()}
    if isinstance(value,list):
        return {p:v for i,x in enumerate(value) for p,v in flatten(x,f'{prefix}.{i}').items()} if value else {prefix:[]}
    return {prefix:value}

def run_case(case,mode,clarify):
    start=time.perf_counter(); messages=[]; draft=None; error=None; turns=0
    try:
        text=case['text']
        for _ in range(8):
            turns+=1; messages.append({'role':'user','content':text})
            draft=llm(messages,date.fromisoformat(case['reference_date']),draft) if mode=='llm' else baseline(text,date.fromisoformat(case['reference_date']),draft)
            missing=missing_slots(draft)
            if not clarify or not missing: break
            text=case.get('answers',{}).get(missing[0])
            if text is None: break
            messages.append({'role':'assistant','content':question(draft)})
    except Exception as e: error=type(e).__name__  # Do not log provider request URLs or credentials.
    predicted=draft.model_dump(mode='json') if draft and not error else {}
    expected=Extraction.model_validate(case['expected']).model_dump(mode='json')
    gold=flatten(expected); actual=flatten(predicted)
    return {'id':case['id'],'mode':mode,'clarification':clarify,'valid_output':error is None and draft is not None,'intent_correct':predicted.get('intent')==expected['intent'],'exact_match':predicted==expected,'slot_correct':sum(actual.get(k,object())==v for k,v in gold.items()),'slot_count':len(gold),'extra_slots':len(set(actual)-set(gold)),'complete':bool(draft and not error and not missing_slots(draft)),'turns':turns,'seconds':round(time.perf_counter()-start,4),'error':error,'prediction':predicted}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--modes',nargs='+',choices=['baseline','llm'],default=['baseline']);parser.add_argument('--output',default='results/run.json');args=parser.parse_args()
    data_path=Path(__file__).with_name('smoke_cases.json');cases=json.loads(data_path.read_text());rows=[]
    for mode in args.modes:
        for clarify in [False,True]:
            for case in cases: rows.append(run_case(case,mode,clarify))
    summaries=[]
    for mode in args.modes:
        for clarify in [False,True]:
            group=[r for r in rows if r['mode']==mode and r['clarification']==clarify]
            summaries.append({'mode':mode,'clarification':clarify,'n':len(group),**{metric:round(sum(r[metric] for r in group)/len(group),4) for metric in ['valid_output','intent_correct','exact_match','complete','turns','seconds']},'slot_accuracy':round(sum(r['slot_correct'] for r in group)/sum(r['slot_count'] for r in group),4)})
    report={'created_utc':datetime.now(timezone.utc).isoformat(),'dataset_sha256':hashlib.sha256(data_path.read_bytes()).hexdigest(),'prompt_version':PROMPT_VERSION,'prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest(),'provider':'gemini','model':gemini_model(),'python':platform.python_version(),'note':'Synthetic development smoke set, not a held-out final evaluation. Completeness is not correctness. Latency is whole-dialogue wall time. No paid calls in baseline-only mode.','summary':summaries,'cases':rows}
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(report,indent=2));print(json.dumps(summaries,indent=2))
if __name__=='__main__': main()
