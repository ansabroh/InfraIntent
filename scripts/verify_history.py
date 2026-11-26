"""Verify an exported array of get_event JSON objects, including decision hashes."""
import argparse
import hashlib
import json
from pathlib import Path

def hash_of(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()

p=argparse.ArgumentParser()
p.add_argument('events',type=Path,help='JSON array of decoded event objects in ascending order')
p.add_argument('--head',help='Expected case head hash')
a=p.parse_args()
events=json.loads(a.events.read_text());previous='';case=None
if not events: p.error('empty history')
for i,event in enumerate(events):
    event=dict(event)
    h=event.pop('hash')
    assert event['sequence']==i and event['previous']==previous, 'broken event sequence'
    if case is None: case=event['case_id']
    assert event['case_id']==case, 'mixed case ids'
    assert hash_of(event)==h, 'event hash mismatch'
    if event['kind'] in ('ASSESSED','ADJUDICATED'):
        receipt=dict(event['data']);decision=receipt.pop('decision_hash')
        assert hash_of(receipt)==decision, 'decision hash mismatch'
    previous=h
if a.head: assert previous==a.head, 'case head mismatch'
print(json.dumps({'ok':True,'case_id':case,'events':len(events),'head':previous}))
