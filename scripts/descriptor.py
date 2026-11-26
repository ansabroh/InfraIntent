"""Print a descriptor for exact committed file bytes. Never hashes reformatted JSON."""
import argparse
import hashlib
import json
import re
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('commit', help='Full 40-character lowercase Git commit SHA')
p.add_argument('path', help='Repository-relative evidence file path')
a=p.parse_args()
if not re.fullmatch('[0-9a-f]{40}',a.commit): p.error('full lowercase commit SHA required')
f=Path(a.path)
if f.is_absolute() or any(x in ('','.','..') for x in a.path.split('/')): p.error('unsafe path')
b=f.read_bytes()
if not 0<len(b)<=24000: p.error('evidence must be 1..24000 bytes')
print(json.dumps({'commit':a.commit,'path':a.path,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)},sort_keys=True))
