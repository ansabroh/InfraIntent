"""Actual GenVM SDK/storage in direct mode; web and LLM calls are mocked."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import pytest
from gltest.direct import VMContext, deploy_contract, create_address

ROOT = Path(__file__).resolve().parents[1]

def canon(v):
    return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=True)

def fixture(name):
    return json.loads((ROOT / 'fixtures' / (name + '.json')).read_text())

def desc(b, path='fixtures/compliant.json'):
    body = canon(b).encode()
    return {'commit': 'a' * 40, 'path': path, 'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}

def answer(b, statuses=('PASS','PASS','PASS'), coherent=True):
    return {'coherent': coherent, 'checks': [
        {'id': rid, 'status': status, 'source': 'observed', 'quote': b['audit'][:450]}
        for rid, status in zip(('private-api','least-privilege','owner-label'), statuses)]}

@pytest.fixture
def env():
    vm = VMContext()
    with vm.activate():
        c = deploy_contract(ROOT / 'contracts/infra_intent.py', vm, sdk_version='v0.2.16')
        owner = vm.sender
        reviewer = create_address('0x' + '22' * 20)
        submitter = create_address('0x' + '33' * 20)
        stranger = create_address('0x' + '44' * 20)
        p,b = fixture('policy'), fixture('baseline')
        d = desc(b, 'fixtures/baseline.json')
        vm.mock_web(r'.*/fixtures/baseline.json$', {'status':200,'body':canon(b)})
        cid = c.create('ansabroh/InfraIntent', canon(p), canon(d), str(submitter), str(reviewer))
        yield vm,c,cid,p,b,owner,reviewer,submitter,stranger

def stage(env, name='compliant', statuses=('PASS','PASS','PASS'), coherent=True):
    vm,c,cid,p,b,*_ = env
    c.lock(cid)
    obs = fixture(name)
    d = desc(obs)
    vm.mock_web(r'.*/fixtures/compliant.json$', {'status':200,'body':canon(obs)})
    vm.mock_llm('.*', canon(answer(obs,statuses,coherent)))
    c.submit(cid,canon(d))
    return obs,d

def state(env):
    return json.loads(env[1].get_case(env[2]))

@pytest.mark.parametrize('name,statuses,coherent,outcome',[
 ('compliant',('PASS','PASS','PASS'),True,'COMPLIANT'),
 ('conditional',('PASS','PASS','FAIL'),True,'CONDITIONAL'),
 ('drift',('PASS','PASS','PASS'),True,'DRIFT'),
 ('unknown',('PASS','PASS','PASS'),True,'INCONCLUSIVE'),
 ('compliant',('UNKNOWN','PASS','PASS'),True,'INCONCLUSIVE'),
 ('compliant',('FAIL','PASS','PASS'),True,'DRIFT'),
 ('compliant',('PASS','PASS','PASS'),False,'INCONCLUSIVE')])
def test_outcomes(env,name,statuses,coherent,outcome):
    stage(env,name,statuses,coherent)
    env[1].assess(env[2])
    assert state(env)['latest']['outcome'] == outcome

def test_receipt_and_chain(env):
    stage(env)
    vm,c,cid,*_ = env
    c.assess(cid)
    s=state(env)
    previous=''
    for i in range(s['events']):
        e=json.loads(c.get_event(cid,i))
        h=e.pop('hash')
        assert e['sequence']==i and e['previous']==previous
        assert hashlib.sha256(canon(e).encode()).hexdigest()==h
        previous=h
    assert s['head']==previous
    receipt=s['latest'];h=receipt.pop('decision_hash')
    assert h==hashlib.sha256(canon(receipt).encode()).hexdigest()

def test_independent_validator_agrees(env):
    stage(env);env[1].assess(env[2])
    assert env[0].run_validator() is True

@pytest.mark.parametrize('change',['hard','advisory','unknown','coherence','quote','coverage','baseline-pass'])
def test_independent_validator_rejects(env,change):
    obs,_=stage(env);vm,c,cid,*_=env
    c.assess(cid)
    result=answer(obs)
    if change=='hard': result['checks'][0]['status']='FAIL'
    if change=='advisory': result['checks'][2]['status']='FAIL'
    if change=='unknown': result['checks'][0]['status']='UNKNOWN'
    if change=='coherence': result['coherent']=False
    if change=='quote': result['checks'][0]['quote']='invented evidence'
    if change=='coverage': result['checks'].pop()
    if change=='baseline-pass': result['checks'][0]['source']='baseline'
    vm.clear_mocks()
    vm.mock_llm('.*',canon(result))
    assert vm.run_validator() is False

@pytest.mark.parametrize('method',['lock','submit','dispute'])
def test_access_control(env,method):
    vm,c,cid,p,b,owner,reviewer,submitter,stranger=env
    if method!='lock': stage(env)
    if method=='dispute': c.assess(cid)
    vm.sender=stranger
    with vm.expect_revert('only'):
        if method=='lock': c.lock(cid)
        if method=='submit': c.submit(cid,canon(desc(b)))
        if method=='dispute': c.dispute(cid,canon(desc(b)),'recheck')

def test_submitter_and_permissionless_assess(env):
    vm,c,cid,p,b,owner,reviewer,submitter,stranger=env
    c.lock(cid);vm.sender=submitter
    vm.mock_web(r'.*/fixtures/compliant.json$',{'status':200,'body':canon(b)})
    vm.mock_llm('.*',canon(answer(b)))
    c.submit(cid,canon(desc(b)));vm.sender=stranger;c.assess(cid)
    assert state(env)['latest']['outcome']=='COMPLIANT'

@pytest.mark.parametrize('bad',['hash','bytes','404','schema','duplicate','environment','oversize'])
def test_unverifiable_evidence(env,bad):
    obs,d=stage(env);vm,c,cid,*_=env
    if bad=='hash': body=canon(obs)+' '
    elif bad=='bytes': body=canon(obs)[:-1]
    elif bad=='schema': body=canon({'wrong':True})
    elif bad=='duplicate': body='{"environment":"a","environment":"b"}'
    elif bad=='environment': obs['environment']='other';body=canon(obs)
    elif bad=='oversize': body='x'*24001
    else: body=canon(obs)
    if bad in ('schema','duplicate','environment'):
        c.assess(cid)
        d['bytes']=len(body.encode())
        d['sha256']=hashlib.sha256(body.encode()).hexdigest()
        c.submit(cid,canon(d))
    vm.clear_mocks()
    vm.mock_web(r'.*/fixtures/baseline.json$', {'status':200,'body':canon(fixture('baseline'))})
    vm.mock_web(r'.*/fixtures/compliant.json$',{'status':404 if bad=='404' else 200,'body':body})
    c.assess(cid)
    assert state(env)['latest']['outcome']=='INCONCLUSIVE'

@pytest.mark.parametrize('path',['../secret','a/../b','/etc/passwd','a//b','a?url=http://localhost','a#b','a%2fb'])
def test_unsafe_descriptor(env,path):
    vm,c,cid,p,b,*_=env;c.lock(cid);d=desc(b);d['path']=path
    with vm.expect_revert(): c.submit(cid,canon(d))

@pytest.mark.parametrize('commit',['main','a'*39,'a'*41,'A'*40])
def test_mutable_refs_rejected(env,commit):
    vm,c,cid,p,b,*_=env;c.lock(cid);d=desc(b);d['commit']=commit
    with vm.expect_revert('commit'): c.submit(cid,canon(d))

def test_dispute_adjudication_preserves_history(env):
    obs,d=stage(env,'drift');vm,c,cid,p,b,owner,reviewer,*_=env
    c.assess(cid)
    old=c.get_event(cid,3)
    vm.sender=reviewer
    c.dispute(cid,canon(d),'Review exposure against the fixed baseline')
    c.adjudicate(cid)
    assert state(env)['latest']['adjudication'] is True
    assert c.get_event(cid,3)==old
    with vm.expect_revert('dispute unavailable'): c.dispute(cid,canon(d),'again')

def test_revision_limit_and_replay(env):
    obs,d=stage(env);vm,c,cid,*_=env
    for _ in range(15):
        c.assess(cid);c.submit(cid,canon(d))
    c.assess(cid)
    with vm.expect_revert('revision limit'): c.submit(cid,canon(d))
    with vm.expect_revert('invalid state'): c.assess(cid)

def test_locked_policy_cannot_change(env):
    stage(env)
    with env[0].expect_revert('already locked'): env[1].lock(env[2])

def test_malformed_model_fail_closed(env):
    stage(env);vm,c,cid,*_=env
    vm.clear_mocks()
    vm.mock_web(r'.*/fixtures/baseline.json$', {'status':200,'body':canon(fixture('baseline'))})
    vm.mock_web(r'.*/fixtures/compliant.json$', {'status':200,'body':canon(fixture('compliant'))})
    vm.mock_llm('.*','not json');c.assess(cid)
    assert state(env)['latest']['outcome']=='INCONCLUSIVE'

def test_deterministic_drift_cannot_be_overridden(env):
    stage(env,'drift');vm,c,cid,*_=env
    vm.clear_mocks()
    vm.mock_web(r'.*/fixtures/baseline.json$', {'status':200,'body':canon(fixture('baseline'))})
    vm.mock_web(r'.*/fixtures/compliant.json$', {'status':200,'body':canon(fixture('drift'))})
    vm.mock_llm('.*','not json');c.assess(cid)
    assert state(env)['latest']['outcome']=='DRIFT'

def test_invalid_policy_does_not_create(env):
    vm,c,cid,p,b,owner,reviewer,submitter,*_=env
    for value in [True,0,-1,1.5,'2000']:
        p['max_cpu_millis']=value
        with vm.expect_revert('integer'):
            c.create('ansabroh/InfraIntent',canon(p),canon(desc(b)),str(submitter),str(reviewer))
    assert c.get_count()==1

@pytest.mark.parametrize('role', [123, '', '0x123', '0x'+'0'*40, '0x'+'z'*40])
def test_invalid_role_addresses(env,role):
    vm,c,cid,p,b,owner,reviewer,submitter,*_=env
    with vm.expect_revert():
        c.create('ansabroh/InfraIntent',canon(p),canon(desc(b)),role,str(reviewer))

def test_mixed_case_role_address(env):
    vm,c,cid,p,b,owner,reviewer,submitter,*_=env
    role=create_address('0x'+'aB'*20)
    new=c.create('ansabroh/InfraIntent',canon(p),canon(desc(b,'fixtures/baseline.json')),str(role).upper().replace('0X','0x'),str(reviewer))
    c.lock(new)
    vm.sender=role
    c.submit(new,canon(desc(b)))
    assert json.loads(c.get_case(new))['state']=='SUBMITTED'
