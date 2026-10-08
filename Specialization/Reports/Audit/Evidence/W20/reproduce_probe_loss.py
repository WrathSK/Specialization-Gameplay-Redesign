"""Audit-only actual InspirationProbe, controlled native/facts/Store-exit stubs.
No DB, permanent Property, formal tests, game, deployment or source writes.
Requires existing lupa.lua55; source-shaped loss is pinned to Store evidence.
"""
import argparse,hashlib,json
from pathlib import Path
from lupa.lua55 import LuaRuntime
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
repo=args.repo.resolve();source=repo/'Mod/CultureInspirationProbe.lua'
FIXTURE=r'''
local all={};local hooks={};local rows={};local arguments={};local attachments={};local values={1,3,6,10}
Locale={Lookup=function(k,...) local o={k};for _,v in ipairs({...})do o[#o+1]=tostring(v)end;return table.concat(o,'|')end}
for i,v in ipairs(values)do
 local name='BUILDING_SPC_INSPIRE_PROBE_'..v;local mid='SPC_INSPIRE_PROBE_'..v
 rows[name]={Index=i,InternalOnly=1,PrereqDistrict='DISTRICT_CITY_CENTER',CitizenSlots=0,Housing=0}
 rows[mid]={ModifierType='MODIFIER_SINGLE_CITY_ADJUST_GREAT_PERSON_POINT'}
 arguments[#arguments+1]={ModifierId=mid,Name='Amount',Value=v/10}
 arguments[#arguments+1]={ModifierId=mid,Name='GreatPersonClassType',Value='GREAT_PERSON_CLASS_SCIENTIST'}
 attachments[#attachments+1]={BuildingType=name,ModifierId=mid}
end
local function city(id,x)
 local c={owner=0,id=id,x=x,y=1,present={},token='native:'..id}
 function c:GetOwner()return self.owner end;function c:GetID()return self.id end
 function c:GetBuildings()return self end;function c:GetBuildQueue()return {city=self}end
 all[#all+1]=c;return c
end
a=city(1,1);b=city(2,2);Players={};Events={};writes=0;removed=0;exits={};shared={}
for _,pid in ipairs({0,3})do
 Players[pid]={GetCities=function()return {
 FindID=function(_,id)for _,c in ipairs(all)do if c.owner==pid and c.id==id then return c end end end,
 Members=function()local i=0;return function()repeat i=i+1;local c=all[i];if not c then return nil end;if c.owner==pid then return i,c end until false end end}end}
end
P={Info=function(_,k)return rows[k]end,Rows=function(t)return t=='ModifierArguments' and arguments or attachments end,
 IsTestPlayer=function(pid)return pid==0 end,HasBuilding=function(c,id)return c.present[id]==true end,
 RemoveBuilding=function(c,id)c.present[id]=nil;writes=writes+1 end,
 CreateBuilding=function(q,id)q.city.present[id]=true;writes=writes+1 end,
 Field=function(t,n)if not t[n]then hooks[n]={};t[n]={Add=function(fn)hooks[n][#hooks[n]+1]=fn end}end;return t[n]end}
shared.CityProgressionStore={RegisterExit=function(n,fn)exits[n]=fn end,
 IsExitTarget=function(c,l)return l.target~=nil and c.owner==l.target.owner and c.id==l.target.cityID and c.x==l.target.x and c.y==l.target.y end,
 RemoveOwned=function(c,l,names)assert(shared.CityProgressionStore.IsExitTarget(c,l));for _,n in ipairs(names)do local id=rows[n].Index;if c.present[id]then P.RemoveBuilding(c,id);removed=removed+1 end end end}
function fire(n,...)for _,fn in ipairs(hooks[n]or {})do fn(...)end end
function amount(c)local sum=0;for i,v in ipairs(values)do if c.present[i]then sum=sum+v/10 end end;return sum end
function prepare()SPCCultureInspirationProbe.Start(P,shared);ip=shared.CultureInspirationProbe;assert(ip.Request(0,a,'INSPIRE_NEXT','r1'));assert(ip.Request(0,a,'INSPIRE_NEXT','r2'));assert(ip.stage==1 and amount(a)==.1, tostring(ip.stage)..':'..tostring(ip.error))end
'''
BODY=r'''
prepare();local ordinary=99;a.present[ordinary]=true
local loss={origin={owner=0,cityID=1,x=1,y=1},target={owner=3,cityID=8,x=1,y=1},evidence='CityTransfered+live_reference'}
if MODE=='SYNTHETIC_TARGET_ID' then loss.targetID=1 end
if MODE=='UNKNOWN_CONTROL' then loss.target=nil else a.owner=3;a.id=8 end
exits.CultureInspirationProbe(a,loss)
local stageAtExit=ip.stage;local amountAtExit=amount(a)
local stageAfterAudit=ip.stage;local endStopped=false;local nextStopped=false;local auditError=''
if MODE=='PRODUCTION_SHAPE' then
 ip.Audit(0);stageAfterAudit=ip.stage;auditError=ip.error or ''
 endStopped=ip.Request(0,b,'INSPIRE_END','end'):find('INSPIRE_CITY_UNKNOWN')~=nil
 nextStopped=ip.Request(0,b,'INSPIRE_NEXT','next'):find('INSPIRE_FINISH_PREVIOUS_CITY')~=nil
 assert(stageAtExit==1 and amountAtExit==0 and stageAfterAudit==1 and endStopped and nextStopped)
elseif MODE=='SYNTHETIC_TARGET_ID' then assert(stageAtExit==-1 and amountAtExit==0)
else assert(stageAtExit==1 and amountAtExit==.1 and removed==0)end
local ordinaryRetained=a.present[ordinary]==true
fire('LoadScreenClose');assert(ip.ready and ip.stage==-1 and amount(a)==0)
ip.Request(0,b,'INSPIRE_NEXT','after-load');assert(ip.stage==0)
result={mode=MODE,stage_at_exit=stageAtExit,carrier_amount_at_exit=amountAtExit,stage_after_audit=stageAfterAudit,
 audit_error=auditError,end_blocked=endStopped,new_city_blocked=nextStopped,ordinary_retained=ordinaryRetained,
 cold_cleanup_stage=-1,new_city_stage_after_cleanup=ip.stage,carrier_removals_at_exit=removed}
'''
out=[]
for mode in ['PRODUCTION_SHAPE','SYNTHETIC_TARGET_ID','UNKNOWN_CONTROL']:
 l=LuaRuntime(unpack_returned_tuples=True)
 def include(name):
  if name=='NetworkInput':l.execute("SPCNetworkInput={Reference=function(c)return c.token..':'..c.owner..':'..c.id end}")
  elif name=='CurrentSpecializationFacts':l.execute("SPCCurrentSpecializationFacts={Read=function()return {validity='VERIFIED',identity='CULTURE',potential=4,activeStatus='KNOWN',active=4}end}")
  else:raise AssertionError(name)
 l.globals().include=include;l.execute(FIXTURE);l.execute(source.read_text());l.globals().MODE=mode;l.execute(BODY)
 out.append({k:v for k,v in l.globals().result.items()})
raw={'lua_version':l.eval('_VERSION'),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sources':{str(f.relative_to(repo)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [source,repo/'Mod/CityProgressionStore.lua',repo/'DevelopmentTests/test_culture_inspiration_probe.py']},'limits':['Actual unmodified Probe; native/facts/Store RemoveOwned are controlled stubs, not full Store integration or engine evidence.','Source-shaped loss matches CityProgressionStore:602; synthetic targetID matches current local-test shape only.','No permanent writes, native effect reads, memory measurement or native lifecycle PASS.'],'scenarios':out}
args.output.write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
