"""Audit-only actual Lua network boundary cases; mocked native/UI surfaces.
No project writes, existing fixture declarations only, no old tests executed.
"""
from pathlib import Path
import ast, hashlib, json, argparse
import sys
sys.dont_write_bytecode = True
from lupa.lua55 import LuaRuntime
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path)
args=parser.parse_args()
ROOT=args.repo.resolve() if args.repo else Path(__file__).resolve().parents[5]

def runtime():
    tree=ast.parse((ROOT/'DevelopmentTests/test_arch_v2_batch_a.py').read_text())
    fixture=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIXTURE' for t in n.targets))
    lua=LuaRuntime(unpack_returned_tuples=True)
    loader=lua.eval('function(code,name)assert(load(code,name))()end')
    lua.globals().include=lambda name:loader((ROOT/'Mod'/f'{name}.lua').read_text(),'@Mod/'+name+'.lua')
    lua.execute(fixture)
    lua.globals().include('NetworkBridge')
    lua.execute('SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true')
    return lua

def plain(v):
    if hasattr(v,'items'):return {str(k):plain(x) for k,x in v.items()}
    return v

alias=runtime()
alias.execute(r'''
 send('0,1,0,2,10',1)
 local bucket=shared.NetworkBridge.players[0]
 local accepted=bucket.input
 local beforeVersion=net.Input(0).inputVersion
 local beforeLevel=net.CurrentNational(0).RESEARCH.level
 assert(beforeLevel==3 and cities[1].active==3)
 -- Mutate the publicly reachable accepted input, with native source left unchanged.
 shared.NetworkBridge.players[0].input.cities[1].active=4
 assert(accepted.cities[1].active==4 and bucket.input==accepted)
 local beforeRefreshLevel=net.CurrentNational(0).RESEARCH.level
 assert(beforeRefreshLevel==3 and net.Input(0).inputVersion==beforeVersion)
 cities[1].fail=true
 net.Refresh(0)
 local afterVersion=net.Input(0).inputVersion
 local afterLevel=net.CurrentNational(0).RESEARCH.level
 local afterAvailability=net.Input(0).availability
 assert(cities[1].active==3 and afterLevel==4 and afterVersion==beforeVersion+1 and afterAvailability=='NEEDS_REVALIDATION')
 cities[1].fail=false;net.Refresh(0)
 local recoveryLevel=net.CurrentNational(0).RESEARCH.level
 assert(recoveryLevel==3 and net.Input(0).inputVersion==afterVersion+1)
 auditResult={public_input_same_object=true,native_source_active=3,before_level=beforeLevel,
  before_refresh_private_level=beforeRefreshLevel,unknown_fallback_level=afterLevel,
  unknown_fallback_availability=afterAvailability,input_versions={beforeVersion,afterVersion,net.Input(0).inputVersion},
  fresh_recovery_level=recoveryLevel,actual_current_caller_mutation='NOT_ESTABLISHED'}
''')
sender=runtime()
sender.globals().include('PerformanceCounters')
sender.globals().include('NetworkSender')
sender.execute(r'''
 shared.Version=P.VERSION;ExposedMembers.SPC_P0=shared
 ExposedMembers.SPC_Performance=SPCPerformance.New()
 Game.GetLocalPlayer=function()return 0 end
 PlayerOperations={EXECUTE_SCRIPT=1}
 local requests=0
 UI={RequestPlayerOperation=function(pid,op,p)requests=requests+1;net.Receive(pid,p)end}
 local function sample(n)
  local rows,keys={},{}
  for i=1,n do local trader=9+i;units[trader]={};local key='0:'..trader..'|0:1>0:2'
   rows[key]={originPlayer=0,originCityID=1,destinationPlayer=0,destinationCityID=2,traderUnitID=trader};keys[#keys+1]=key
  end
  table.sort(keys);routeCount=n
  return {status='COMPLETE_UI_SHADOW',revalidation='VERIFIED',snapshot={count=n,turn=turn,
   signal=shared.RouteSignalRevision,keys=keys,routes=rows,fingerprint=table.concat(keys,'\n')}}
 end
 local pump=SPCNetworkSender.New(P)
 local atLimit=sample(128);pump(atLimit);pump(atLimit)
 assert(requests==1 and #net.players[0].routes==128 and not atLimit.awaitingNetwork)
 local beforeVersion=net.Input(0).inputVersion;local fingerprint=net.players[0].fingerprint
 local tooMany=sample(129);local sentBefore=requests
 pump(tooMany);pump(tooMany)
 assert(requests==sentBefore and not tooMany.awaitingNetwork and tooMany.error==nil and tooMany.status=='COMPLETE_UI_SHADOW' and tooMany.revalidation=='VERIFIED')
 assert(#net.players[0].routes==128 and net.players[0].fingerprint==fingerprint and net.Input(0).inputVersion==beforeVersion)
 auditResult={at_128_requests=sentBefore,at_128_accepted_routes=128,at_129_extra_requests=requests-sentBefore,
  ui_status=tooMany.status,ui_revalidation=tooMany.revalidation,ui_awaiting_network=tooMany.awaitingNetwork,
  ui_explicit_error=tooMany.error~=nil,retained_accepted_routes=#net.players[0].routes,
  retained_input_version=net.Input(0).inputVersion,before_overflow_input_version=beforeVersion,
  real_native_route_capacity='NOT_ESTABLISHED'}
''')
notification=runtime()
notification.execute(r'''
 local seen={};local committed=true
 for _,name in ipairs({'Lv3Effects','StandardizationDiscount','NetworkBoost','CommerceConvergence','CopyYields'})do
  shared[name]={Audit=function(publication)
   seen[#seen+1]=name
   committed=committed and publication.inputVersion==1 and net.CurrentNational(0).RESEARCH.level==3
   if name=='Lv3Effects' then error('INJECTED_FIRST_CONSUMER')end
  end}
 end
 send('0,1,0,2,10',1)
 assert(#seen==5 and committed and net.Input(0).inputVersion==1)
 assert(net.players[0].consumerError:find('INJECTED_FIRST_CONSUMER',1,true))
 auditResult={consumer_calls=#seen,first_failed_later_consumers_called=true,
  committed_view_visible_to_all=committed,accepted_input_version=net.Input(0).inputVersion,
  real_consumer_effect_bodies='STUBBED'}
''')
result={'evidence':'LOCAL_STRUCTURAL_REPRODUCTION','limits':['Native facts, route counts, traders, request/event transport are mocked.','No current consumer is shown mutating accepted input; deliberate mutation tests the boundary.','No actual game route count or native performance claim.'],
 'source_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('Mod/NetworkBridge.lua','Mod/NetworkInput.lua','Mod/NetworkSender.lua','Mod/PerformanceCounters.lua','DevelopmentTests/test_arch_v2_batch_a.py')},
 'accepted_input_alias_unknown_fallback':plain(alias.globals().auditResult),'sender_route_limit':plain(sender.globals().auditResult),'network_consumer_failure_isolation':plain(notification.globals().auditResult)}
print(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True))
