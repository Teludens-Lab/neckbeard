#!/usr/bin/env python3
"""Score human-reviewed eval submissions; does not infer correctness from keywords."""
import argparse,json,sys
from pathlib import Path

def score(rubric,submission):
    expected={c['id']:c for c in rubric['criteria']}
    scores=submission['criteria']
    if set(scores)!=set(expected):raise ValueError('Every rubric criterion must be scored exactly once')
    if not submission.get('reviewer') or not submission.get('artifact') or not submission.get('case_id'):raise ValueError('Reviewer, case_id and artifact required')
    total=0
    for key,c in expected.items():
        row=scores[key];value=row['score']
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not 0<=value<=4 or not row.get('evidence'):raise ValueError('Each criterion needs a 0–4 score and artifact evidence')
        total+=c['weight']*value/4
    failures=submission.get('critical_failures')
    if not isinstance(failures,list) or not set(failures)<=set(rubric['critical_failures']):raise ValueError('Explicit recognized critical_failures list required')
    return {'case_id':submission['case_id'],'score':round(total,2),'passed':total>=rubric['pass_score'] and not failures,'critical_failures':failures,'reviewer':submission['reviewer'],'artifact':submission['artifact']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('submission',type=Path);a=p.parse_args()
    try:
        result=score(json.loads((Path(__file__).parent/'rubric.json').read_text()),json.loads(a.submission.read_text()));print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
    except (ValueError,KeyError,TypeError) as e:print(json.dumps({'error':str(e)}));return 2
if __name__=='__main__':sys.exit(main())
