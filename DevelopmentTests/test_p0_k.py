"""Targeted P0-K L3 simulations of the real Lua modules.

No game, deployment, database, historical test runner, or persistent writes.
Fixture metadata describes explicit supported examples, not the live database.
UI tests mock only the engine and existing transport endpoints. Catalog/Facts,
NetworkInput, the slot collector, and legacy Dialogue/GWA execute real source.
Results are LOCAL_SIMULATION_PASS, never native event/persistence certification.
"""
from pathlib import Path
import os
import unittest

from lupa.lua55 import LuaRuntime

r = Path(__file__).resolve().parents[1]
if os.environ.get("SPC_P0_K_ROOT"):
    r = Path(os.environ["SPC_P0_K_ROOT"]).resolve()
m = r / "Mod"
assert (m / "GreatWorkFacts.lua").is_file(), "Run from DevelopmentTests or set SPC_P0_K_ROOT"


BASE = r"""
function iter(rows)
 return function()local i=0;return function()i=i+1;return rows[i]end end
end
function members(rows)
 return function()local i=0;return function()i=i+1;if rows[i]then return i,rows[i]end end end
end
function encode(v)
 if type(v)~='table'then return type(v)..':'..tostring(v)end
 local out={};for k,x in pairs(v)do out[#out+1]=encode(k)..'='..encode(x)end
 table.sort(out);return '{'..table.concat(out,';')..'}'
end
turn=10; propertyWrites=0; scans={}; carrierWrites=0
Game={GetCurrentGameTurn=function()return turn end,GetLocalPlayer=function()return 0 end,
 SetProperty=function()propertyWrites=propertyWrites+1;error('PERSISTENT_WRITE')end}
Locale={Lookup=function(s)return s end}
works={};gps={};eras={};buildings={
 [10]={Index=10,BuildingType='BUILDING_MUSEUM'},[20]={Index=20,BuildingType='BUILDING_SHELF'}}
local examples={'GREATWORK_BHASA_1','GREATWORK_BACH_1','GREATWORK_ANGUISSOLA_1',
 'GREATWORK_COLLOT_1','GREATWORK_YING_1','GREATWORK_BOSCH_1','GREATWORK_ARTIFACT_1'}
for _,kind in ipairs(examples)do
 local e=SPCGreatWorkCatalog.entries[kind]
 assert(e,'FIXTURE_SUPPORTED_EXAMPLE_MISSING '..kind)
 works[kind]={GreatWorkType=kind,Name=kind,GreatWorkObjectType=e[1],
  GreatPersonIndividualType=e[2],EraType=e[3]}
 eras[e[3]]={EraType=e[3],Name=e[3]}
 if e[2]~=''then
  local era=e[4]~=''and e[4]or e[3]
  gps[e[2]]={EraType=era};eras[era]={EraType=era,Name=era}
 end
end
works.UNKNOWN_WRITING={GreatWorkType='UNKNOWN_WRITING',Name='unknown',
 GreatWorkObjectType='GREATWORKOBJECT_WRITING',GreatPersonIndividualType='UNKNOWN_CREATOR',EraType='ERA_CLASSICAL'}
gps.UNKNOWN_CREATOR={EraType='ERA_CLASSICAL'}
works.RELIC={GreatWorkType='RELIC',Name='relic',GreatWorkObjectType='GREATWORKOBJECT_RELIC'}
works.PRODUCT={GreatWorkType='PRODUCT',Name='product',GreatWorkObjectType='GREATWORKOBJECT_PRODUCT'}
local erarows={};for _,e in pairs(eras)do erarows[#erarows+1]=e end
GameInfo={Buildings=iter({buildings[10],buildings[20]}),Eras=iter(erarows)}
P={VERSION='P0-K-TEST',IsTestPlayer=function(pid)return pid==0 end,
 Field=function(t,k)return t and t[k]end,
 Count=function(k)scans[k]=(scans[k]or 0)+1 end,
 Info=function(t,k)
  if t=='GreatWorks'then return works[k]end
  if t=='GreatPersonIndividuals'then return gps[k]end
  if t=='Eras'then return eras[k]end
  if t=='Buildings'then
   if buildings[k]then return buildings[k]end
   if type(k)=='string'and(k:match('^BUILDING_SPC_B059_')or k:match('^BUILDING_SPC_B055_')
     or k:match('^BUILDING_SPC_B060_'))then return {Index=k,BuildingType=k}end
  end
  if t=='Districts'and k=='DISTRICT_THEATER'then
   return {Index=k,DistrictType=k,RequiresPopulation=true}
  end
  if t=='Yields'then
   local names={'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'}
   for i,y in ipairs(names)do if k=='YIELD_'..y then return {Index=i}end end
  end
 end,
 HasBuilding=function(b,id)return b.present[id]==true end,
 CreateBuilding=function(q,id)q.city.present[id]=true;carrierWrites=carrierWrites+1 end,
 RemoveBuilding=function(b,id)b.present[id]=nil;carrierWrites=carrierWrites+1 end}
SPCP0=P
instances={[100]='GREATWORK_BHASA_1',[101]='GREATWORK_BHASA_1',
 [102]='GREATWORK_YING_1',[103]='GREATWORK_BACH_1',[104]='GREATWORK_ARTIFACT_1',
 [105]='UNKNOWN_WRITING',[106]='RELIC',[107]='PRODUCT'}
function city(id,name,kind)
 local c={id=id,owner=0,x=id,y=3,name=name,kind=kind,active=4,
  slots={[10]={},[20]={}},present={[10]=true,[20]=true,KEEP_LIBRARY=true},slotCalls=0,
  properties={SPC_DEV_BINDING_B013_TOKEN='binding:'..id,PERMANENT_INVESTMENT=250}}
 function c:GetID()return self.id end
 function c:GetOwner()if self.failOwner then error('TEMPORARY_OWNER_READ')end;if self.nilOwner then return nil end;return self.owner end
 function c:GetX()return self.x end;function c:GetY()return self.y end
 function c:GetName()return self.name end
 function c:GetProperty(k)return self.properties[k]end
 function c:SetProperty()propertyWrites=propertyWrites+1;error('PERSISTENT_CITY_WRITE')end
 function c:GetBuildQueue()return {city=self}end
 function c:GetBuildings()
  local b={present=self.present}
  function b:GetNumGreatWorkSlots(bid)
   if c.failSlots then error('TEMPORARY_SLOT_READ')end
   return #(c.slots[bid]or {})
  end
  function b:GetGreatWorkInSlot(bid,slot)
   c.slotCalls=c.slotCalls+1;return (c.slots[bid]or {})[slot+1]
  end
  function b:GetGreatWorkTypeFromIndex(id)return instances[id]end
  return b
 end
 return c
end
a=city(7,'A','CULTURE');b=city(8,'B','INDUSTRY');c=city(9,'C','NONE')
citylist={a,b,c};districtlist={}
collection={Members=members(citylist),FindID=function(_,id)
 for _,v in ipairs(citylist)do if v.id==id then return v end end
end}
Players={[0]={GetCities=function()return collection end,
 GetDistricts=function()return {Members=members(districtlist)}end}}
CityManager={GetCityAt=function(x,y)
 for _,v in ipairs(citylist)do if v.x==x and v.y==y then return v end end
end}
shared={Version=P.VERSION,EffectiveFacts={Read=function(pid,c)
 assert(pid==0);return {specialization=c.kind,active=c.active}end}}
ExposedMembers={SPC_P0=shared}
Events=setmetatable({}, {__index=function(t,k)
 local e={list={}};e.Add=function(f)e.list[#e.list+1]=f end
 e.Remove=function(f)for i=#e.list,1,-1 do if e.list[i]==f then table.remove(e.list,i)end end end
 rawset(t,k,e);return e
end})
function fire(name,...)for _,f in ipairs(Events[name].list)do f(...)end end
exits={};returns={};permanentStore={investment=250,insights={R=1},binding='immutable'}
shared.CityProgressionStore={
 RegisterExit=function(name,fn)assert(not exits[name]);exits[name]=fn end,
 RegisterReturn=function(name,fn)assert(not returns[name]);returns[name]=fn end,
 IsExitTarget=function(target,loss)return loss.confirmed==true and target.id==loss.targetID end,
 RemoveOwned=function()error('FACTS_MUST_NOT_REMOVE_CARRIERS')end}
function packet(seq,rows,status)
 local p={Seq=seq,Turn=turn,FactsEpoch=shared.GreatWorkFacts.epoch,FactsInput=shared.GreatWorkFacts.inputRevision,
  FactsRefs='',FactsData='',FactsCount=0,FactsCities=0}
 local ordered={};for _,v in ipairs(citylist)do ordered[#ordered+1]=v end
 table.sort(ordered,function(x,y)return x.id<y.id end)
 for _,v in ipairs(ordered)do
  p.FactsRefs=p.FactsRefs..v.id..','..SPCGreatWorkFacts.Hex(SPCNetworkInput.Reference(v))..','
   ..((not status or status[v.id]~=false)and'1'or'0')..';'
  p.FactsCities=p.FactsCities+1
 end
 for _,w in ipairs(rows or {})do
  p.FactsData=p.FactsData..table.concat(w,',')..';';p.FactsCount=p.FactsCount+1
 end
 return p
end
function receive(seq,rows,status)return shared.GreatWorkFacts.Receive(0,packet(seq,rows,status))end
function reject(p,why)
 local ok,err=shared.GreatWorkFacts.Receive(0,p)
 assert(ok==false and err==why,tostring(ok)..':'..tostring(err)..' expected '..why)
end
function sampleRows()
 return {{7,10,0,100,'GREATWORK_BHASA_1'},{7,10,1,101,'GREATWORK_BHASA_1'},
  {7,10,2,102,'GREATWORK_YING_1'},{8,20,0,103,'GREATWORK_BACH_1'},
  {7,20,0,105,'UNKNOWN_WRITING'},{7,20,1,106,'RELIC'},{7,20,2,107,'PRODUCT'}}
end
"""


PRODUCER = r"""
-- Gameplay facts is real; only the existing legacy endpoint ACK is stubbed.
shared.Dialogue={ready=true,generation=1,seq={}}
shared.GreatWorkAdjacency={}
requestLog={};ackMode='both'
factsHookCounts={};for name,e in pairs(Events)do factsHookCounts[name]=#e.list end
ContextPtr={SetInitHandler=function(_,f)init=f end,SetShutdown=function(_,f)shutdown=f end}
PlayerOperations={EXECUTE_SCRIPT=1}
UI={RequestPlayerOperation=function(pid,op,p)
 assert(pid==0 and op==1);requestLog[#requestLog+1]=p;lastPacket=p
 if ackMode=='both'then
  shared.GreatWorkFacts.Receive(pid,p);shared.Dialogue.seq[pid]=p.Seq
 end
 return true
end}
Map={GetPlotIndex=function(x,y)return x*1000+y end,
 GetPlot=function()return {GetAdjacencyYield=function()return 0 end}end}
Cities={GetCityInPlot=function(index)
 for _,v in ipairs(citylist)do if v.x*1000+v.y==index then return v end end
end}
"""


class Fixture:
    def __init__(self, producer=False):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.loaded = set()

        def include(name):
            # The test owns P and engine stubs; the production Probe has unrelated
            # game APIs. DiagnosticLog is not required for assertions here.
            if name in {"Probe", "DiagnosticLog"} or name in self.loaded:
                return
            self.loaded.add(name)
            self.lua.execute((m / (name + ".lua")).read_text())

        self.include = include
        self.lua.globals().include = include
        include("GreatWorkFacts")
        self.lua.execute(BASE)
        self.lua.execute("SPCGreatWorkFacts.Start(P,shared)")
        if producer:
            self.lua.execute(PRODUCER)
            self.lua.execute((m / "UI/DialogueRefresh.lua").read_text())
            self.lua.execute("init()")

    def check(self, text):
        self.lua.execute(text)


class CatalogTests(unittest.TestCase):
    def test_seven_categories_known_era_and_unknown_same_category(self):
        Fixture().check(r"""
        local cat=SPCGreatWorkCatalog.Build(P)
        assert(cat.count==7 and cat.complete)
        local categories={};for _,w in pairs(cat.works)do categories[w.category]=true end
        for _,kind in ipairs({'WRITING','MUSIC','SCULPTURE','PORTRAIT','LANDSCAPE','RELIGIOUS','ARTIFACT'})do
         assert(categories['GREATWORKOBJECT_'..kind],kind)
        end
        for _,kind in ipairs({'UNKNOWN_WRITING','RELIC','PRODUCT','GREATWORK_ABSENT'})do
         local w,why=SPCGreatWorkCatalog.Resolve(P,kind)
         assert(w==nil and why=='UNSUPPORTED_TYPE',kind)
        end
        local ying=assert(SPCGreatWorkCatalog.Resolve(P,'GREATWORK_YING_1'))
        assert(ying.era=='ERA_RENAISSANCE' and ying.eraSource=='WORK_ERA')
        assert(gps.GREAT_PERSON_INDIVIDUAL_QIU_YING.EraType=='ERA_INDUSTRIAL')
        local artifact=assert(SPCGreatWorkCatalog.Resolve(P,'GREATWORK_ARTIFACT_1'))
        assert(artifact.era=='ERA_ANCIENT' and artifact.eraSource=='WORK_ERA')
        """)

    def test_metadata_rejection_and_verified_fallback(self):
        Fixture().check(r"""
        local kind='GREATWORK_BHASA_1';local w=works[kind]
        w.GreatWorkObjectType='GREATWORKOBJECT_PRODUCT'
        local _,why=SPCGreatWorkCatalog.Resolve(P,kind);assert(why=='CATEGORY_METADATA')
        assert(not SPCGreatWorkCatalog.Build(P).complete)
        w.GreatWorkObjectType='GREATWORKOBJECT_WRITING';w.EraType='ERA_FUTURE'
        _,why=SPCGreatWorkCatalog.Resolve(P,kind);assert(why=='UNREVIEWED_ERA')
        w.EraType=nil
        local meta=assert(SPCGreatWorkCatalog.Resolve(P,kind))
        assert(meta.era=='ERA_CLASSICAL' and meta.eraSource=='VERIFIED_NATIVE_CREATOR')
        gps[w.GreatPersonIndividualType].EraType='ERA_ATOMIC'
        _,why=SPCGreatWorkCatalog.Resolve(P,kind);assert(why=='ERA_UNAVAILABLE')
        w.EraType='ERA_CLASSICAL';eras.ERA_CLASSICAL=nil
        _,why=SPCGreatWorkCatalog.Resolve(P,kind);assert(why=='ERA_UNAVAILABLE')
        works.GREATWORK_ARTIFACT_1.EraType=nil
        _,why=SPCGreatWorkCatalog.Resolve(P,'GREATWORK_ARTIFACT_1');assert(why=='ERA_UNAVAILABLE')
        """)


class FactsTests(unittest.TestCase):
    def test_pure_plan_and_first_unknown_are_not_reliable_zero(self):
        Fixture().check(r"""
        local cat=SPCGreatWorkCatalog.Build(P)
        local raw={{id=100,type='GREATWORK_BHASA_1',building=10,slot=0},
         {id=101,type='GREATWORK_BHASA_1',building=10,slot=1},
         {id=104,type='GREATWORK_ARTIFACT_1',building=20,slot=0},
         {id=105,type='UNKNOWN_WRITING',building=20,slot=1}}
        local before=encode(raw);local plan=SPCGreatWorkFacts.Plan(cat,raw)
        assert(plan.count==3 and plan.eraCount==2 and plan.eras.ERA_CLASSICAL==2 and plan.eras.ERA_ANCIENT==1)
        assert(#plan.excluded==1 and plan.excluded[1].reason=='UNSUPPORTED_TYPE' and encode(raw)==before)
        assert(receive(1,{},{[7]=false}))
        local f=shared.GreatWorkFacts;local unknown=f.Read(0,7)
        assert(unknown.availability=='UNKNOWN' and not unknown.hasConfirmed and unknown.count==nil)
        assert(f.Describe(0,7):find('UNKNOWN不是0',1,true))
        assert(not f.Describe(0,7):find('合格 0 件',1,true))
        assert(f.Read(0,8).count==0 and f.Read(0,8).availability=='KNOWN')
        """)

    def test_plan_counts_exclusions_and_non_culture_domestic_index(self):
        Fixture().check(r"""
        local f=shared.GreatWorkFacts
        assert(f.state=='UNKNOWN' and f.ack==0 and f.revision==0)
        assert(f.Read(0,7)==nil and f.Describe(0,7):find('UNKNOWN不是0',1,true))
        assert(receive(1,sampleRows()))
        local x=f.Read(0,7);local y=f.Read(0,8);local z=f.Read(0,9)
        assert(x.count==3 and x.eraCount==2 and x.eras.ERA_CLASSICAL==2 and x.eras.ERA_RENAISSANCE==1)
        assert(#x.excluded==3 and x.excluded[1].reason=='UNSUPPORTED_TYPE')
        assert(y.count==1 and y.eras.ERA_INDUSTRIAL==1 and b.kind=='INDUSTRY')
        assert(z.count==0 and z.eraCount==0 and z.availability=='KNOWN' and f.state=='VERIFIED')
        local report='';for page=1,5 do report=report..f.Describe(0,7,true,page)end
        assert(report:find('ERA_INDUSTRIAL 国内来源：B 1件',1,true))
        assert(report:find('排除 3 件',1,true))
        assert(f.Describe(0,9):find('合格 0 件',1,true))
        assert(propertyWrites==0 and carrierWrites==0)
        """)

    def test_read_is_copy_same_input_is_not_new_publication(self):
        Fixture().check(r"""
        local f=shared.GreatWorkFacts;assert(receive(1,sampleRows()))
        local first=f.revision;local snapshot=encode(f.Read(0,7))
        local exposed=f.Read(0,7);exposed.eras.ERA_CLASSICAL=100;exposed.works[1].era='ERA_FUTURE'
        assert(encode(f.Read(0,7))==snapshot)
        for seq=2,21 do assert(receive(seq,sampleRows()))end
        assert(f.revision==first and f.ack==21 and encode(f.Read(0,7))==snapshot)
        local scansBefore=encode(scans)
        for _=1,25 do f.Describe(0,7,true,1);f.Read(0,8)end
        assert(encode(scans)==scansBefore and propertyWrites==0 and carrierWrites==0)
        """)

    def test_unknown_keeps_confirmed_value_but_is_not_empty(self):
        Fixture().check(r"""
        local f=shared.GreatWorkFacts;assert(receive(1,sampleRows()))
        assert(receive(2,{{8,20,0,103,'GREATWORK_BACH_1'}},{[7]=false}))
        local x=f.Read(0,7)
        assert(x.availability=='UNKNOWN' and x.count==3 and x.eraCount==2 and f.state=='UNKNOWN')
        assert(f.Describe(0,7):find('待复核（保留最近确认值）',1,true))
        assert(f.Describe(0,9,true):find('国内来源尚未完全确认',1,true))
        assert(receive(3,{}))
        assert(f.Read(0,7).count==0 and f.Read(0,7).availability=='KNOWN' and f.state=='VERIFIED')
        """)

    def test_duplicate_instances_and_slots_rejected(self):
        for rows, why in [
            ("{{7,10,0,100,'GREATWORK_BHASA_1'},{8,20,0,100,'GREATWORK_BHASA_1'}}", "GW_DUPLICATE_INSTANCE"),
            ("{{7,10,0,100,'GREATWORK_BHASA_1'},{7,10,0,101,'GREATWORK_BHASA_1'}}", "GW_DUPLICATE_SLOT"),
        ]:
            with self.subTest(reason=why):
                Fixture().check("assert(receive(1,sampleRows())); reject(packet(2," + rows + "),'" + why + "'); "
                                "assert(shared.GreatWorkFacts.Read(0,7).count==3 and shared.GreatWorkFacts.state=='UNKNOWN')")

    def test_wrong_epoch_and_duplicate_sequence_cannot_poison(self):
        Fixture().check(r"""
        local f=shared.GreatWorkFacts;assert(receive(1,sampleRows()))
        local p=packet(2,{});p.FactsEpoch=p.FactsEpoch-1;reject(p,'GW_STALE_EPOCH')
        assert(f.ack==1 and f.state=='VERIFIED')
        p=packet(1,{});p.FactsCount=999
        assert(f.Receive(0,p)==false and f.ack==1 and f.Read(0,7).count==3 and f.state=='VERIFIED')
        local ok,why=f.Receive(9,p);assert(ok==false and why=='GW_UNSUPPORTED_OWNER')
        assert(f.Read(9,7)==nil)
        """)

    def test_format_count_scope_turn_and_status_rejections(self):
        cases = [
            ("p.Seq=0", "GW_SEQUENCE"),
            ("p.Turn=turn-1", "GW_STALE_TURN"),
            ("p.FactsInput=p.FactsInput-1", "GW_STALE_INPUT"),
            ("p.FactsCount=p.FactsCount+1", "GW_WORK_FORMAT"),
            ("p.FactsCities=p.FactsCities+1", "GW_CITY_COUNT"),
            ("p.FactsData=p.FactsData..'garbage'", "GW_WORK_FORMAT"),
            ("p.FactsRefs=p.FactsRefs..'garbage'", "GW_REFERENCE_FORMAT"),
            ("p.FactsRefs=p.FactsRefs:gsub('^([^;]+);','%1;%1;')", "GW_DUPLICATE_CITY"),
            ("p.FactsRefs=p.FactsRefs:gsub('9,[^;]+;','');p.FactsCities=p.FactsCities-1", "GW_INCOMPLETE_SCOPE"),
            ("p.FactsRefs=p.FactsRefs:gsub('^(7,[^,]+),1;','%1,0;')", "GW_UNKNOWN_WITH_WORKS"),
            ("p.FactsData=p.FactsData:gsub('7,10,0','7,99,0',1)", "GW_LOCATION_METADATA"),
        ]
        for mutation, why in cases:
            with self.subTest(reason=why):
                Fixture().check("assert(receive(1,sampleRows()));local p=packet(2,sampleRows());" + mutation + ";reject(p,'" + why + "')")

    def test_binding_change_rejects_old_reference_and_removes_current_fact(self):
        Fixture().check(r"""
        local f=shared.GreatWorkFacts;assert(receive(1,sampleRows()))
        local old=packet(2,sampleRows());a.properties.SPC_DEV_BINDING_B013_TOKEN='new binding'
        reject(old,'GW_STALE_REFERENCE')
        assert(f.Read(0,7)==nil and f.Read(0,8).count==1)
        assert(receive(3,sampleRows()) and f.Read(0,7).count==3)
        local saved=f.Read(0,8).count;b.failOwner=true
        assert(f.Read(0,8).availability=='UNKNOWN' and f.Read(0,8).count==saved)
        b.failOwner=false;b.nilOwner=true
        assert(f.Read(0,8).availability=='UNKNOWN' and f.Read(0,8).count==saved)
        b.nilOwner=false;b.owner=62
        assert(f.Read(0,8)==nil)
        """)

    def test_same_turn_move_then_return_updates_both_city_counts(self):
        Fixture().check(r"""
        local f=shared.GreatWorkFacts;local original=sampleRows();assert(receive(1,original))
        local moved=sampleRows();moved[3]={8,20,1,102,'GREATWORK_YING_1'}
        assert(receive(2,moved))
        assert(f.Read(0,7).count==2 and f.Read(0,7).eraCount==1)
        assert(f.Read(0,8).count==2 and f.Read(0,8).eraCount==2)
        assert(receive(3,original) and f.Read(0,7).eraCount==2 and f.Read(0,8).count==1)
        assert(turn==10 and f.revision==3)
        """)

    def test_exit_return_and_cold_load_are_session_only(self):
        Fixture().check(r"""
        local f=shared.GreatWorkFacts;assert(receive(1,sampleRows()))
        local permanent=encode(permanentStore);local cityPermanent=encode(a.properties)
        local pending=packet(2,sampleRows());local epoch=f.epoch
        assert(exits.GreatWorkFacts and returns.GreatWorkFacts)
        assert(not pcall(exits.GreatWorkFacts,a,{origin={owner=0,cityID=7},targetID=7,confirmed=false}))
        assert(f.Read(0,7).count==3)
        exits.GreatWorkFacts(a,{origin={owner=0,cityID=7},targetID=7,confirmed=true})
        assert(f.Read(0,7)==nil and f.epoch>epoch and f.ack==0 and f.state=='UNKNOWN')
        reject(pending,'GW_STALE_EPOCH')
        epoch=f.epoch;returns.GreatWorkFacts(0,a)
        assert(f.epoch>epoch and f.ack==0)
        assert(receive(1,sampleRows()) and f.Read(0,7).availability=='KNOWN')
        epoch=f.epoch
        -- New Gameplay module instance has no saved facts and shares only the monotonic epoch namespace.
        exits={};returns={};SPCGreatWorkFacts.Start(P,shared);local cold=shared.GreatWorkFacts
        assert(cold.epoch~=epoch and cold.Read(0,7)==nil and cold.state=='UNKNOWN')
        assert(receive(1,{}) and cold.Read(0,7).count==0)
        assert(encode(permanentStore)==permanent and encode(a.properties)==cityPermanent)
        assert(propertyWrites==0 and carrierWrites==0 and a.present.KEEP_LIBRARY)
        """)

    def test_reset_then_cold_start_cannot_reuse_old_epoch(self):
        Fixture().check(r"""
        local f=shared.GreatWorkFacts;f.Reset();local stale=packet(1,sampleRows());local epoch=f.epoch
        exits={};returns={};SPCGreatWorkFacts.Start(P,shared)
        assert(shared.GreatWorkFacts.epoch>epoch)
        reject(stale,'GW_STALE_EPOCH')
        assert(shared.GreatWorkFacts.Read(0,7)==nil)
        """)

    def test_restart_and_shutdown_keep_gameplay_subscriptions_bounded(self):
        Fixture().check(r"""
        for _=1,8 do
         exits={};returns={};SPCGreatWorkFacts.Start(P,shared)
         assert(#Events.GreatWorkCreated.list==1 and #Events.GreatWorkMoved.list==1)
        end
        local f=shared.GreatWorkFacts;f.Shutdown()
        assert(shared.GreatWorkFacts==nil)
        for _,e in pairs(Events)do assert(#e.list==0)end
        assert(propertyWrites==0 and carrierWrites==0)
        """)


    def test_domestic_copy_and_city_scope_change_do_not_claim_absence(self):
        Fixture().check(r"""
        assert(receive(1,sampleRows()));local f=shared.GreatWorkFacts
        local domestic=f.Domestic(0,'ERA_INDUSTRIAL')
        assert(domestic.availability=='VERIFIED' and domestic.eras.ERA_INDUSTRIAL[8].count==1)
        domestic.eras.ERA_INDUSTRIAL[8].count=99
        assert(f.Domestic(0,'ERA_INDUSTRIAL').eras.ERA_INDUSTRIAL[8].count==1)
        local new=city(10,'new','NONE');citylist[#citylist+1]=new
        fire('CityAddedToMap',0,10,new.x,new.y)
        assert(f.Domestic(0).availability=='UNKNOWN' and f.Read(0,10)==nil)
        assert(receive(2,sampleRows()))
        assert(f.Read(0,10).count==0 and f.Domestic(0).availability=='VERIFIED')
        """)

    def test_second_loss_uses_current_cached_location_not_original_city_id(self):
        Fixture().check(r"""
        a.id=17;local rows=sampleRows();for _,w in ipairs(rows)do if w[1]==7 then w[1]=17 end end
        assert(receive(1,rows));local f=shared.GreatWorkFacts
        assert(f.Read(0,17).count==3)
        local loss={origin={owner=0,cityID=7},targetID=17,confirmed=true}
        exits.GreatWorkFacts(a,loss)
        assert(f.Read(0,17)==nil and f.Read(0,8).count==1)
        local epoch=f.epoch;exits.GreatWorkFacts(a,loss)
        assert(f.epoch==epoch and propertyWrites==0 and carrierWrites==0)
        """)


class ProducerTests(unittest.TestCase):
    def test_single_slot_read_exact_legacy_projection_and_idle(self):
        fx = Fixture()
        fx.check("a.slots[10]={102,100,-1};b.slots[20]={103};")
        fx.check(PRODUCER)
        fx.lua.execute((m / "UI/DialogueRefresh.lua").read_text())
        fx.check(r"""
        init();local p=lastPacket;local ui=ExposedMembers.SPC_DialogueBackground
        assert(p.Valid==1 and p.Count==6 and p.FactsCount==3 and p.FactsCities==3)
        assert(p.Data=='7,-1,EMPTY;7,100,GREATWORK_BHASA_1;7,102,GREATWORK_YING_1;8,-1,EMPTY;8,103,GREATWORK_BACH_1;9,-1,EMPTY')
        assert(p.FactsData=='7,10,1,100,GREATWORK_BHASA_1;7,10,0,102,GREATWORK_YING_1;8,20,0,103,GREATWORK_BACH_1;')
        assert(a.slotCalls==3 and b.slotCalls==1 and c.slotCalls==0 and ui.slotReads==3)
        local scanned,sent,reads=ui.scans,ui.sends,ui.slotReads;local counters=encode(scans)
        for _=1,500 do fire('SystemUpdateUI');fire('GameCoreEventPublishComplete');fire('GameCoreEventPlaybackComplete')end
        assert(ui.scans==scanned and ui.sends==sent and ui.slotReads==reads and encode(scans)==counters)
        assert(a.slotCalls==3 and b.slotCalls==1 and propertyWrites==0)
        shutdown();assert(ExposedMembers.SPC_DialogueBackground==nil)
        for name,e in pairs(Events)do assert(#e.list==(factsHookCounts[name]or 0))end
        shared.GreatWorkFacts.Shutdown();for _,e in pairs(Events)do assert(#e.list==0)end
        """)

    def test_native_create_move_same_turn_scope_and_redundant_input(self):
        fx = Fixture(producer=True)
        fx.check(r"""
        local ui=ExposedMembers.SPC_DialogueBackground;local reads=ui.slotReads
        a.slots[10]={100};fire('GreatWorkCreated',0,999,a.x,a.y,10,100)
        fire('SystemUpdateUI')
        assert(ui.slotReads==reads+1 and a.slotCalls==1 and b.slotCalls==0 and c.slotCalls==0)
        assert(shared.GreatWorkFacts.Read(0,7).count==1 and turn==10)
        reads=ui.slotReads;a.slots[10]={};b.slots[10]={100}
        fire('GreatWorkMoved',0,7,0,8,10,10,100);fire('GameCoreEventPublishComplete')
        assert(ui.slotReads==reads+2 and c.slotCalls==0)
        assert(shared.GreatWorkFacts.Read(0,7).count==0 and shared.GreatWorkFacts.Read(0,8).count==1)
        reads=ui.slotReads;b.slots[10]={};a.slots[10]={100}
        fire('GreatWorkMoved',0,8,0,7,10,10,100);fire('SystemUpdateUI')
        assert(ui.slotReads==reads+2 and shared.GreatWorkFacts.Read(0,7).count==1)
        local revision=shared.GreatWorkFacts.revision
        fire('GreatWorkMoved',0,8,0,7,10,10,100);fire('SystemUpdateUI')
        assert(shared.GreatWorkFacts.revision==revision and shared.GreatWorkFacts.state=='VERIFIED')
        -- Unknown creator cannot be mistaken for a CityID; plot resolution scoped creation to A.
        assert(c.slotCalls==0 and turn==10 and propertyWrites==0)
        """)

    def test_trade_updates_owned_endpoint_and_unknown_signature_is_bounded(self):
        fx = Fixture(producer=True)
        fx.check(r"""
        local ui=ExposedMembers.SPC_DialogueBackground
        a.slots[10]={100};fire('GreatWorkCreated',0,999,a.x,a.y);fire('SystemUpdateUI')
        local reads=ui.slotReads;a.slots[10]={}
        fire('GreatWorkMoved',0,7,2,80,10,10,100);fire('SystemUpdateUI')
        assert(ui.slotReads==reads+1 and shared.GreatWorkFacts.Read(0,7).count==0 and c.slotCalls==0)
        reads=ui.slotReads;b.slots[20]={104}
        fire('GreatWorkMoved',2,80,0,8,10,20,104);fire('SystemUpdateUI')
        assert(ui.slotReads==reads+1 and shared.GreatWorkFacts.Read(0,8).eras.ERA_ANCIENT==1)
        reads=ui.slotReads;local scanned=ui.scans
        fire('GreatWorkMoved');fire('SystemUpdateUI')
        assert(ui.scans==scanned+1 and ui.slotReads==reads+3)
        reads=ui.slotReads;scanned=ui.scans;local sends=ui.sends
        for _=1,100 do fire('SystemUpdateUI')end
        assert(ui.scans==scanned and ui.slotReads==reads and ui.sends==sends)
        """)

    def test_native_district_and_governor_parameter_scope(self):
        Fixture(producer=True).check(r"""
        local ui=ExposedMembers.SPC_DialogueBackground;local reads=ui.slotReads
        a.slots[10]={100}
        -- Native district event: owner, districtID, cityID, x, y, districtType...
        fire('DistrictAddedToMap',0,777,7,a.x,a.y,'DISTRICT_THEATER',100);fire('SystemUpdateUI')
        assert(ui.slotReads==reads+1 and a.slotCalls==1 and b.slotCalls==0 and c.slotCalls==0)
        local sends=ui.sends;reads=ui.slotReads;a.active=3
        -- Assignment/establishment: cityOwner, cityID, governorOwner, governorID.
        fire('GovernorAssigned',0,7,0,555);fire('SystemUpdateUI')
        assert(ui.sends==sends+1 and ui.slotReads==reads and lastPacket.Valid==1)
        sends=ui.sends;a.active=4
        fire('GovernorEstablished',0,7,0,555);fire('SystemUpdateUI')
        assert(ui.sends==sends+1 and ui.slotReads==reads)
        """)

    def test_bounded_ack_retry_and_shutdown(self):
        fx = Fixture()
        fx.check(PRODUCER + "ackMode='none'")
        fx.lua.execute((m / "UI/DialogueRefresh.lua").read_text())
        fx.check(r"""
        init();local ui=ExposedMembers.SPC_DialogueBackground
        assert(#requestLog==1 and ui.scans==1 and ui.state=='WAIT_ACK')
        for _=1,30 do fire('SystemUpdateUI')end
        assert(#requestLog==3 and ui.retries==2 and ui.scans==1 and ui.state=='ACK_TIMEOUT')
        assert(requestLog[1].Seq==requestLog[2].Seq and requestLog[2].Seq==requestLog[3].Seq)
        local seq=lastPacket.Seq
        ackMode='both';a.slots[10]={100};fire('GreatWorkCreated',0,999,a.x,a.y);fire('SystemUpdateUI')
        assert(ui.sends==4 and lastPacket.Seq>seq and shared.GreatWorkFacts.Read(0,7).count==1)
        shutdown();assert(ExposedMembers.SPC_DialogueBackground==nil)
        for name,e in pairs(Events)do assert(#e.list==(factsHookCounts[name]or 0))end
        shared.GreatWorkFacts.Shutdown();for _,e in pairs(Events)do assert(#e.list==0)end
        """)

    def test_move_invalidates_inflight_packet_and_replaces_it_in_same_turn(self):
        Fixture(producer=True).check(r"""
        local f=shared.GreatWorkFacts;local ui=ExposedMembers.SPC_DialogueBackground
        ackMode='none';a.slots[10]={100};fire('GreatWorkCreated',0,999,a.x,a.y);fire('SystemUpdateUI')
        local stale=lastPacket;local reads=ui.slotReads;local sends=ui.sends
        assert(ui.state=='WAIT_ACK')
        a.slots[10]={};b.slots[10]={100};fire('GreatWorkMoved',0,7,0,8,10,10,100)
        assert(f.state=='UNKNOWN' and f.Read(0,7).availability=='UNKNOWN' and f.Read(0,8).availability=='UNKNOWN')
        fire('SystemUpdateUI');local replacement=lastPacket
        assert(ui.sends==sends+1 and ui.slotReads==reads+2 and replacement.FactsInput>stale.FactsInput)
        assert(replacement.Seq>stale.Seq and c.slotCalls==0 and turn==10)
        reject(stale,'GW_STALE_INPUT')
        assert(f.Read(0,7).availability=='UNKNOWN')
        assert(f.Receive(0,replacement))
        shared.Dialogue.seq[0]=replacement.Seq;fire('SystemUpdateUI')
        assert(f.Read(0,7).count==0 and f.Read(0,8).count==1 and f.state=='VERIFIED')
        local revision=f.revision;assert(f.Receive(0,stale)==false and f.revision==revision and f.state=='VERIFIED')
        """)

    def test_generation_and_epoch_changes_recollect_same_turn(self):
        Fixture(producer=True).check(r"""
        local ui=ExposedMembers.SPC_DialogueBackground;local sends=ui.sends;local reads=ui.slotReads
        local oldSeq=lastPacket.Seq
        shared.Dialogue.generation=shared.Dialogue.generation+1;shared.Dialogue.seq={}
        a.slots[10]={100};fire('SystemUpdateUI')
        assert(ui.sends==sends+1 and ui.slotReads==reads+3 and lastPacket.Generation==2 and lastPacket.Seq>oldSeq)
        assert(shared.GreatWorkFacts.Read(0,7).count==1 and turn==10)
        sends=ui.sends;reads=ui.slotReads;local epoch=lastPacket.FactsEpoch
        shared.GreatWorkFacts.Reset();fire('SystemUpdateUI')
        assert(ui.sends==sends+1 and ui.slotReads==reads+3 and lastPacket.FactsEpoch>epoch)
        assert(shared.GreatWorkFacts.Read(0,7).availability=='KNOWN')
        """)

    def test_read_failure_is_unknown_legacy_invalid_and_recovers(self):
        fx = Fixture(producer=True)
        fx.check(r"""
        a.slots[10]={100};fire('GreatWorkCreated',0,999,a.x,a.y);fire('SystemUpdateUI')
        a.failSlots=true;fire('GreatWorkCreated',0,999,a.x,a.y);fire('SystemUpdateUI')
        assert(lastPacket.Valid==0 and lastPacket.Data=='')
        local x=shared.GreatWorkFacts.Read(0,7)
        assert(x.count==1 and x.availability=='UNKNOWN')
        a.failSlots=false;fire('GreatWorkCreated',0,999,a.x,a.y);fire('SystemUpdateUI')
        assert(lastPacket.Valid==1 and shared.GreatWorkFacts.Read(0,7).availability=='KNOWN')
        """)


class LegacyIsolationTests(unittest.TestCase):
    def test_real_legacy_carriers_equal_with_facts_success_or_failure(self):
        snapshots = []
        for branch in ("absent", "accepted", "rejected"):
            with self.subTest(branch=branch):
                fx = Fixture()
                fx.include("Dialogue")
                fx.include("GreatWorkAdjacency")
                fx.check(r"""
                -- The real old writers own their effects; Facts owns no effect callback.
                shared.CityProgressionStore=nil
                local district={GetID=function()return 21 end,GetCity=function()return a end,
                 GetType=function()return 'DISTRICT_THEATER'end,IsComplete=function()return true end,
                 GetX=function()return a.x end,GetY=function()return a.y end}
                districtlist[1]=district
                local base={0,0,-2,3,2,0}
                Map={GetPlot=function()return {GetAdjacencyYield=function(_,pid,cid,kind,yield)
                 assert(pid==0 and cid==7 and kind=='DISTRICT_THEATER');return base[yield]end}end}
                SPCGWAdjacency.Start(P,shared);SPCDialogue.Start(P,shared)
                local adj,n=SPCGWAdjacencyModel.Collect(P,0)
                assert(adj=='7,21,DISTRICT_THEATER,0,0,-2,3,2,0'and n==1)
                local legacy='7,-1,EMPTY;7,100,GREATWORK_BHASA_1;7,102,GREATWORK_YING_1;7,105,UNKNOWN_WRITING;7,106,RELIC;7,107,PRODUCT;8,-1,EMPTY;9,-1,EMPTY'
                wire={Generation=1,Seq=1,Turn=turn,Valid=1,Data=legacy,Count=8,AdjData=adj,AdjCount=n}
                factsRows={{7,10,0,100,'GREATWORK_BHASA_1'},{7,10,1,102,'GREATWORK_YING_1'},
                 {7,10,2,105,'UNKNOWN_WRITING'},{7,20,0,106,'RELIC'},{7,20,1,107,'PRODUCT'}}
                """)
                if branch == "accepted":
                    fx.check("assert(receive(1,factsRows));local p=shared.GreatWorkFacts.Read(0,7);"
                             "assert(p.count==2 and p.eras.ERA_RENAISSANCE==1 and not p.eras.ERA_INDUSTRIAL)")
                elif branch == "rejected":
                    fx.check("local p=packet(1,factsRows);p.FactsCount=999;reject(p,'GW_WORK_FORMAT')")
                fx.check(r"""
                shared.Dialogue.Receive(0,wire)
                local plan=shared.Dialogue.last[0][7];local adj=shared.GreatWorkAdjacency.last[0][7]
                assert(not plan.error and not adj.error)
                -- Historical legacy rule remains creator-based, including unknown supported-category types.
                assert(plan.count==3 and plan.excluded==2 and plan.d==2 and plan.percent==25 and plan.applied==25)
                assert(plan.eras.ERA_INDUSTRIAL and not plan.eras.ERA_RENAISSANCE)
                assert(adj.count==3 and adj.base.SCIENCE==3 and adj.base.CULTURE==2 and adj.base.GOLD==-2)
                assert(a.present.BUILDING_SPC_B059_D2 and a.present.BUILDING_SPC_B060_SCIENCE_P0
                 and a.present.BUILDING_SPC_B060_SCIENCE_P1 and a.present.BUILDING_SPC_B060_GOLD_N1
                 and a.present.BUILDING_SPC_B060_CULTURE_P1 and a.present.KEEP_LIBRARY)
                local before=carrierWrites;wire.Seq=2;shared.Dialogue.Receive(0,wire)
                assert(carrierWrites==before and propertyWrites==0)
                parity=encode({a=a.present,b=b.present,c=c.present,dialogue=plan,gwa=adj,writes=carrierWrites})
                """)
                snapshots.append(fx.lua.globals().parity)
        self.assertEqual(snapshots[0], snapshots[1])
        self.assertEqual(snapshots[0], snapshots[2])


class WiringTests(unittest.TestCase):
    def test_actual_gameplay_branch_isolates_unexpected_facts_exception(self):
        fx=Fixture()
        source=(m/'Gameplay.lua').read_text()
        start=source.index("  if params.Action=='DIALOGUE_SAMPLE' then\n")
        end=source.index("  if params.Action=='SHADOW_SELECT'",start)
        fx.lua.execute('function sampleRoute(playerID,params)\n'+source[start:end]+'\nend')
        fx.check(r"""
        local calls=0
        shared.GreatWorkFacts.Receive=function()error('injected unexpected facts error')end
        shared.Dialogue={Receive=function(pid,p)calls=calls+1;assert(pid==0 and p.Seq==1)end}
        sampleRoute(0,{Action='DIALOGUE_SAMPLE',Seq=1})
        assert(calls==1 and shared.GreatWorkFacts.lastError=='GW_RECEIVE_EXCEPTION')
        assert(propertyWrites==0 and carrierWrites==0)
        """)


if __name__ == "__main__":
    unittest.main(verbosity=2)
