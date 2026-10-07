"""P06a audit-only actual Store reproduction. Stdout JSON, no project writes.
Requires existing lupa.lua55. Reuses fixture declarations only, not old test cases.
Native objects/events are mocked. Counts are not engine timing/memory evidence.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
from lupa.lua55 import LuaRuntime


def literal(path, marker):
    tree=ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value,str) and marker in node.value:
            return node.value
    raise AssertionError('Fixture literal missing: '+marker)


def runtime(root, body):
    lua=LuaRuntime(unpack_returned_tuples=True)
    loader=lua.eval('function(code,name) assert(load(code,name))() end')
    def include(name): loader((root/'Mod'/f'{name}.lua').read_text(),'@Mod/'+name+'.lua')
    lua.globals().include=include
    lua.execute('print=function()end')
    for name in ['Probe','CityIdentityRead','CityProgressionStore','BindingProbe','CompletionRecordProbe',
                 'CityJournalProbe','FreshBindingHook','CityFlowProbe','EffectiveFacts','InvestmentAction','NetworkInput','Standardization']:
        include(name)
    tests=root/'DevelopmentTests'
    e1=(tests/'test_p0_e1.py').read_text()
    lua.execute('M=SPCCityIdentityRead\n'+e1[e1.index('function fixture()'):e1.index('function expect(')])
    fixture=literal(tests/'test_p0_e2.py','local function event()').split("for _,kind in ipairs({'RESEARCH'",1)[0]
    fixture=fixture.replace('SPCCityProgressionStore.StartLegacyTest(P,shared)','SPCCityProgressionStore.Start(P,shared)')
    fixture=fixture.replace('SPCBindingProbe.Start(P,shared);SPCCityJournalProbe','SPCBindingProbe.Start(P,shared);SPCCompletionRecordProbe.Start(P,shared);SPCCityJournalProbe')
    old="CityRoleFacts=function(c)return {owner=c:GetOwner(),cityID=c:GetID(),governorGateStatus='KNOWN',governorLevelCeiling=governor}end,"
    assert fixture.count(old)==1
    fixture=fixture.replace(old,'GovernorGate=SPCP0.GovernorGate,')
    old='function c:GetProperty(k)for n,key in pairs(M.Keys)do'
    new="""function c:GetProperty(k)
 if k=='SPC_P0_GOV_CONTROL_A007' then return governor~=nil and 1 or nil end
 if k=='SPC_P0_GOV_PRESENT' or k=='SPC_P0_GOV_ESTABLISHED' then return governor and governor>=2 and 1 or 0 end
 for level=2,4 do if k=='SPC_P0_GOV_REQ_'..level then return governor and governor>=level and 1 or 0 end end
 for n,key in pairs(M.Keys)do"""
    assert fixture.count(old)==1; fixture=fixture.replace(old,new)
    lua.execute('SPCP0.IsTestPlayer=function(pid)return pid==0 end')
    helpers=literal(tests/'test_b108_e2_multicity.py','local INDEX=SPCCityProgressionStore.INDEX').split('-- Scale and write locality',1)[0]
    lua.execute(fixture+helpers+body)
    def convert(v):
        if hasattr(v,'items'): return {str(k):convert(x) for k,x in v.items()}
        return v
    return convert(lua.globals().auditResult)


SCALE=r'''
start();local group={}
for i=1,N do
 local c=fresh(i);group[i]=c;register(c);complete(c,'DISTRICT_CAMPUS')
 if i<=T then for j=1,3 do invest(c,i*10+j)end end
end
governor=1 -- Tradition accumulates without ACTIVE IV; no governor-count assumption.
local originalPairs=pairs;local visits,checks,sweeps=0,0,0
pairs=function(t)
 local info=debug.getinfo(2,'Sl')
 if info.source=='@Mod/CityProgressionStore.lua' and info.currentline==SCAN_LINE then
  sweeps=sweeps+1
  local iter,state,key=originalPairs(t)
  return function(s,k)local nk,nv=iter(s,k);if nk~=nil then visits=visits+1 end;return nk,nv end,state,key
 end
 return originalPairs(t)
end
local before=writes;turn=turn+1;Events.PlayerTurnActivated.Fire(0)
local delta=writes-before;local firstVisits=visits;local firstSweeps=sweeps
for i=1,T do assert(d.ReadTradition(0,group[i]).age==1 and shared.EffectiveFacts.Read(0,group[i]).active==1)end
Events.PlayerTurnActivated.Fire(0)
assert(writes-before==delta and visits==firstVisits and sweeps==firstSweeps,'duplicate turn changed state')
assert(delta==T and firstSweeps==T and firstVisits==N*T)
auditResult={records=N,tradition_records=T,active_ceiling=1,record_writes=delta,
 uniqueness_sweeps=firstSweeps,record_visits=firstVisits,other_reference_comparisons=T*(N-1),
 duplicate_turn_extra_writes=0,duplicate_turn_extra_uniqueness_scans=0,age=1}
'''

CORRUPT=r'''
start();local aCity=fresh(1);register(aCity);complete(aCity,'DISTRICT_CAMPUS')
local bCity=fresh(2);register(bCity);complete(bCity,'DISTRICT_THEATER')
local key=PREFIX..aCity.s.values.TOKEN;local bKey=PREFIX..bCity.s.values.TOKEN
local frozenB=encode(props[bKey])
if MODE=='revision' then props[key].revision=-1 elseif MODE=='current_boolean' then props[key].current=true else error('mode')end
local before=writes;saved=true;boot()
local aOK=pcall(shared.EffectiveFacts.Read,0,aCity)
local bOK=pcall(shared.EffectiveFacts.Read,0,bCity)
local failure=d.FailureReport()
assert(not aOK and encode(props[bKey])==frozenB and writes==before)
if MODE=='revision' then assert(bOK and failure==nil)else assert(not bOK and failure~=nil)end
auditResult={mode=MODE,broken_city_readable=aOK,control_city_readable=bOK,
 collection_fault=failure~=nil,control_mock_record_unchanged=true,load_writes=writes-before}
'''

REENTRANT=r'''
start();local c=fresh(1);register(c);complete(c,'DISTRICT_INDUSTRIAL_ZONE')
local token=c.s.values.TOKEN;local key=PREFIX..token
local old=d.ReadTemplates(c);assert(old==nil)
local value={schema=1,initialized=true,uid='STD:'..token,foundation=token,x=c:GetX(),y=c:GetY(),revision=2,
 learned={BUILDING_WORKSHOP={district='DISTRICT_INDUSTRIAL_ZONE',tier=1,turn=turn,evidence='COMPLETE'}}}
local callbackRead,callbackOK,storedDuring
failKey=key
hook=function(k,v)
 if k==key then
  callbackOK,callbackRead=pcall(d.ReadTemplates,c)
  storedDuring=props[key].templates~=nil
 end
end
local writeOK=pcall(d.WriteTemplates,c,old,value)
hook=nil;failKey=nil
local afterOK=pcall(d.ReadTemplates,c)
assert(not writeOK and callbackOK and callbackRead.learned.BUILDING_WORKSHOP and not storedDuring and not afterOK)
auditResult={write_confirmed=writeOK,callback_readable=callbackOK,
 callback_saw_proposed_template=callbackRead.learned.BUILDING_WORKSHOP~=nil,
 persisted_template_during_callback=storedDuring,post_failure_readable=afterOK,
 native_setter_callback_reachability='NOT_ESTABLISHED'}
'''


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path);args=ap.parse_args()
    root=args.repo or Path(__file__).resolve().parents[5]
    source=(root/'Mod/CityProgressionStore.lua').read_text()
    scan_lines=[i for i,line in enumerate(source.splitlines(),1) if 'for other,r in pairs(envelope.records)do if other~=token then' in line]
    assert len(scan_lines)==1
    result={'evidence':'LOCAL_STRUCTURAL_REPRODUCTION','store_sha256':hashlib.sha256(source.encode()).hexdigest(),
      'limits':['Native API/events mocked; no game/save/runtime accessed.','No engine latency, allocation or memory inference.',
                'Existing fixture declarations reused; historical test cases not executed.'],
      'scaling':[],'corruption':[]}
    for n,t in [(8,8),(20,20),(40,40),(40,1)]:
        body=f'local N,T,SCAN_LINE={n},{t},{scan_lines[0]}\n'+SCALE
        result['scaling'].append(runtime(root,body))
    for mode in ['revision','current_boolean']:
        result['corruption'].append(runtime(root,"local MODE='"+mode+"'\n"+CORRUPT))
    result['reentrant']=runtime(root,REENTRANT)
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
