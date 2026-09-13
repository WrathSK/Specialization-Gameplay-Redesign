"""Local simulations only; never label these as in-game verification.
Run: PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/test_specialization_p0.py
"""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from lupa import LuaRuntime

root = Path(__file__).resolve().parents[1] / "Sid Meier's Civilization VI/Mods/SpecializationP0"
lua = LuaRuntime(unpack_returned_tuples=True)
for path in root.rglob("*.lua"):
    lua.execute("assert(load(...))", path.read_text())
manifest = ET.parse(root / "SpecializationP0.modinfo")
files = [n.text for n in manifest.findall("./Files/File")]
assert len(files) == len(set(files))
for file in files:
    assert (root / file).is_file(), file
ids = {e.attrib["ID"] for e in ET.parse(root / "UI/P0Panel.xml").iter() if "ID" in e.attrib}
assert set(re.findall(r"Controls\.(\w+)", (root / "UI/P0Panel.lua").read_text())) <= ids
lua.execute((root / "Probe.lua").read_text())
lua.execute(r'''
logs={}; print=function(s) logs[#logs+1]=s end
function gi(rows, typeKey)
  local t={}
  for i,r in ipairs(rows) do
    r.Index=r.Index or i-1; r.Hash=r.Hash or r.Index+100
    t[r.Index]=r; t[r.Hash]=r
    if typeKey then t[r[typeKey]]=r end
  end
  return setmetatable(t,{__call=function()
    local i=0; return function() i=i+1; return rows[i] end
  end})
end
GameInfo={
  Yields=gi({{YieldType="YIELD_SCIENCE",Index=0},{YieldType="YIELD_PRODUCTION",Index=1}},"YieldType"),
  Districts=gi({{DistrictType="DISTRICT_CAMPUS",Index=0,RequiresPopulation=1},
    {DistrictType="DISTRICT_THEATER",Index=1,RequiresPopulation=1},
    {DistrictType="DISTRICT_TEST_REPLACEMENT",Index=2}},"DistrictType"),
  DistrictReplaces=gi({{CivUniqueDistrictType="DISTRICT_TEST_REPLACEMENT",ReplacesDistrictType="DISTRICT_CAMPUS"}}),
  Buildings=gi({{BuildingType="BUILDING_TEST",PrereqDistrict="DISTRICT_THEATER",IsWonder=false,Index=0}},"BuildingType"),
  Governors=gi({{GovernorType="GOV_TEST",Index=0}},"GovernorType"),
  GovernorPromotionSets=gi({{GovernorType="GOV_TEST",GovernorPromotion="PROMO_TEST"}}),
  GovernorPromotions=gi({{GovernorPromotionType="PROMO_TEST",BaseAbility=true,Level=0}},"GovernorPromotionType"),
  GreatWorks=gi({{GreatWorkType="WORK_TEST",GreatWorkObjectType="GREATWORKOBJECT_WRITING",EraType="ERA_CLASSICAL",Index=0}},"GreatWorkType"),
  GreatWork_YieldChanges=gi({{GreatWorkType="WORK_TEST",YieldType="YIELD_CULTURE",YieldChange=2}}),
  Building_YieldDistrictCopies=gi({}), District_CitizenGreatPersonPoints=gi({}),
  Building_CitizenYieldChanges=gi({}), Boosts=gi({})
}
PlayerConfigurations={[0]={GetCivilizationTypeName=function() return "CIVILIZATION_SPC_TEST" end,
  GetLeaderTypeName=function() return "LEADER_SPC_TEST" end}}
Game={GetCurrentGameTurn=function() return 10 end,GetLocalPlayer=function() return 0 end}
properties={}; writes=0; complete=false; districtType=0
plot={GetIndex=function() return 50 end,GetWorkerCount=function() return 2 end,
  GetAdjacencyYield=function(self,owner,city,d,y) assert(owner==0 and city==1); return 8 end}
buildings={HasBuilding=function(self,id) return id==0 end,
  GetBuildingsAtLocation=function(self,p) assert(p==50); return {0} end,
  GetNumGreatWorkSlots=function() return 1 end,GetGreatWorkInSlot=function() return 301 end,
  GetGreatWorkTypeFromIndex=function(self,id) assert(id==301); return 0 end}
district={GetType=function() return districtType end,GetID=function() return 7 end,
  GetX=function() return 1 end,GetY=function() return 2 end,
  IsComplete=function() return complete end,GetAdjacencyYield=function() return 100 end}
function collection(object)
  return {Members=function() return ipairs({object}) end,FindID=function(self,id)
    if object:GetID()==id then return object end end}
end
districts=collection(district); districts.IsPillaged=function() return false end
governor={GetType=function() return 0 end,IsEstablished=function() return false end,
  HasPromotion=function(self,hash) assert(hash==100); return true end}
city={GetID=function() return 1 end,GetOwner=function() return 0 end,GetName=function() return "Fixture" end,
  GetX=function() return 1 end,GetY=function() return 2 end,GetPopulation=function() return 12 end,
  GetProperty=function(self,k) return properties[k] end,
  SetProperty=function(self,k,v) properties[k]=v; writes=writes+1 end,
  GetAssignedGovernor=function() return governor end,GetDistricts=function() return districts end,
  GetTrade=function() return {GetOutgoingRoutes=function() return {{TraderUnitID=10,OriginCityPlayer=0,
    OriginCityID=1,DestinationCityPlayer=0,DestinationCityID=2}} end,GetIncomingRoutes=function() return {} end} end,
  GetBuildings=function() return buildings end,
  GetBuildQueue=function() return {CurrentlyBuilding=function() return "BUILDING_TEST" end,
    GetBuildingCost=function() return 1000 end,GetBuildingProgress=function() return 700 end} end}
cities=collection(city);cities.GetCapitalCity=function() return city end
player={GetCities=function() return cities end,GetDistricts=function() return districts end,
  GetGovernors=function() return {GetGovernorPointsSpent=function() return 9 end} end,
  GetEra=function() return 2 end}
Players={[0]=player}
Map={GetPlot=function() return plot end,GetCityPlots=function()
  return {GetPurchasedPlots=function() return {50} end} end}
function event()
  local callbacks={}
  return {Add=function(f) callbacks[#callbacks+1]=f end,Remove=function(f)
    for i,v in ipairs(callbacks) do if v==f then table.remove(callbacks,i); return end end end,
    Fire=function(...) for _,f in ipairs(callbacks) do f(...) end end}
end
Events=setmetatable({},{__index=function(t,k) local e=event();rawset(t,k,e);return e end})
GameEvents={SPC_P0_Request=event()};ExposedMembers={}
include=function() end

assert(SPCP0.Family("DISTRICT_TEST_REPLACEMENT")=="RESEARCH")
assert(SPCP0.WorkTypes.GREATWORKOBJECT_PRODUCT==nil)
assert(SPCP0.WorkTypes.GREATWORKOBJECT_RELIC==nil)
assert(SPCP0.WorkTypes.GREATWORKOBJECT_RELIGIOUS==true)
assert(SPCP0.Discounts[1]==10 and SPCP0.Discounts[4]==40)
assert(#SPCP0.Specs==5 and SPCP0.Specs[5].cost==1500 and SPCP0.Specs[5].charge==1360)
for _,kind in ipairs({"DISTRICT","BUILDING","WONDER"}) do
  local preview=SPCP0.CrewPreview(750,1000,700,kind)
  assert(preview.applied==300 and preview.wasted==450 and preview.nextTarget==0)
end
assert(SPCP0.CrewPreview(750,1000,1000,"BUILDING")==nil)
assert(SPCP0.CrewPreview(750,1000,700,"PROJECT")==nil)
assert(SPCP0.CrewPreview(750,nil,700,"BUILDING")==nil)
assert(SPCP0.CrewPreview(750,0/0,700,"BUILDING")==nil)
local text,ok=SPCP0.Snapshot("UI",0,"FIXTURE")
assert(ok and not text:find("SNAPSHOT_ERROR"),text)
assert(text:find("BASE_CANDIDATE") and text:find("ACTUAL_CANDIDATE"))
assert(text:find("instance=301") and text:find("typeID=0") and text:find("plot=50"))
assert(writes==0) -- observation must not write state
local old=plot.GetAdjacencyYield;plot.GetAdjacencyYield=nil
text,ok=SPCP0.Snapshot("GAMEPLAY",0,"MISSING_BASE")
assert(not ok and text:find("ABSENT") and text:find("USER_GAME_TEST_REQUIRED"))
plot.GetAdjacencyYield=old
local oldM=districts.Members;districts.Members=function() error("fixture enumeration failure") end
text,ok=SPCP0.Snapshot("GAMEPLAY",0,"ENUM_FAILURE")
assert(not ok and text:find("traversalErrors=1"))
districts.Members=oldM
''')
# Poison broad probes and city subsystems: property-only handlers must never call them.
lua.execute(r''' 
SPCP0.Snapshot=function() error("FULL_SNAPSHOT_FORBIDDEN") end
SPCP0.Summary=function() error("SUMMARY_FORBIDDEN") end
SPCP0.Rows=function() error("DATABASE_SCAN_FORBIDDEN") end
city.GetDistricts=function() error("DISTRICT_SCAN_FORBIDDEN") end
city.GetTrade=function() error("TRADE_SCAN_FORBIDDEN") end
city.GetBuildQueue=function() error("QUEUE_SCAN_FORBIDDEN") end
city.GetAssignedGovernor=function() error("GOVERNOR_SCAN_FORBIDDEN") end
local hostile=setmetatable({},{__pairs=function() error("NO_PAIRS") end,
 __tostring=function() error("NO_TOSTRING") end})
assert(SPCP0.Scalar(hostile)=="<table:not-inspected>")
assert(SPCP0.Scalar(false)=="false" and #SPCP0.Scalar(string.rep("x",2000))==512)
''')
lua.execute((root / "TradeRouteProbe.lua").read_text())
lua.execute((root / "CompletionProbe.lua").read_text())
lua.execute((root / "StorageProbe.lua").read_text())
lua.execute((root / "BindingProbe.lua").read_text())
lua.execute((root / "CompletionRecordProbe.lua").read_text())
lua.execute((root / "CityJournalProbe.lua").read_text())
lua.execute((root / "EligibilityProbe.lua").read_text())
lua.execute((root / "QualificationProbe.lua").read_text())
lua.execute((root / "Gameplay.lua").read_text())
lua.execute(r'''
GameEvents.SPC_P0_Request.Fire(0,{Action="CAPTURE",CityID=1,Token="a"})
assert(writes==0 and ExposedMembers.SPC_P0.LastToken=="a")
GameEvents.SPC_P0_Request.Fire(0,{Action="MARK_CITY",CityID=999,Token="invalid"})
assert(writes==0 and ExposedMembers.SPC_P0.LastToken==nil)
GameEvents.SPC_P0_Request.Fire(0,{Action="MARK_CITY",CityID=1,Token="marker-before-save"})
assert(writes==1 and properties.SPC_P0_FIRST_ELIGIBLE==nil)
assert(ExposedMembers.SPC_P0.LastToken=="marker-before-save")
GameEvents.SPC_P0_Request.Fire(0,{Action="MARK_CITY",CityID=1,Token="duplicate"})
assert(writes==1 and properties.SPC_P0_MARKER=="marker-before-save")
Events.PlayerTurnActivated.Fire(0)
Events.DistrictBuildProgressChanged.Fire(0,7,1)
assert(writes==1 and properties.SPC_P0_FIRST_SPEC==nil)
''')
# Reinitialize scripts retaining mock properties, NOT a real save/load.
lua.execute('GameEvents.SPC_P0_Request=event(); ExposedMembers={}')
lua.execute((root / "TradeRouteProbe.lua").read_text())
lua.execute((root / "CompletionProbe.lua").read_text())
lua.execute((root / "StorageProbe.lua").read_text())
lua.execute((root / "BindingProbe.lua").read_text())
lua.execute((root / "CompletionRecordProbe.lua").read_text())
lua.execute((root / "CityJournalProbe.lua").read_text())
lua.execute((root / "EligibilityProbe.lua").read_text())
lua.execute((root / "QualificationProbe.lua").read_text())
lua.execute((root / "Gameplay.lua").read_text())
lua.execute(r'''
GameEvents.SPC_P0_Request.Fire(0,{Action="CAPTURE",CityID=1,Token="after-mock-reload"})
assert(writes==1 and ExposedMembers.SPC_P0.Snapshot:find("marker%-before%-save"))
local setter=city.SetProperty
properties={};city.SetProperty=function() error("MOCK_SET_FAILURE") end
GameEvents.SPC_P0_Request.Fire(0,{Action="MARK_CITY",CityID=1,Token="error"})
assert(ExposedMembers.SPC_P0.LastToken==nil and ExposedMembers.SPC_P0.Stage:find("ERROR"))
city.SetProperty=setter

Controls=setmetatable({},{__index=function(t,k)
  local c={SetHide=function() end,SetText=function(self,s) self.text=s end,
    RegisterCallback=function(self,button,f) self.callback=f end};rawset(t,k,c);return c end})
ContextPtr={SetHide=function() end,SetInitHandler=function(self,f) self.init=f end,
  SetShutdown=function() end,SetUpdate=function(self,f) self.update=f end,ClearUpdate=function(self) self.update=nil end}
Mouse={eLClick=1};PlayerOperations={EXECUTE_SCRIPT=1}
UI={GetHeadSelectedCity=function() return city end,
  RequestPlayerOperation=function(playerID,operation,params) queuedRequest=params end}
UIManager={SetClipboardString=function(self,text) clipboard=text end}
''')
lua.execute((root / "UI/P0Panel.lua").read_text())
lua.execute(r'''
ContextPtr:init()
Controls.CopyButton.callback()
assert(Controls.Status.text:find("No reading requested"))
local priorRequest=queuedRequest
local qualification=ExposedMembers.SPC_P0.QualificationProbe
Controls.QualificationButton.callback()
assert(queuedRequest==priorRequest and qualification==ExposedMembers.SPC_P0.QualificationProbe)
local eligibilityData=ExposedMembers.SPC_P0.EligibilityProbe
local initialSample=eligibilityData.samples.INITIALIZE
-- B017 reads cached unknowns only, never dispatches or modifies evidence.
local rows={};for i=0,8 do rows[i]={status="UNKNOWN",reason="EligibilityProbe:12: CIV_NOT_READY"} end
rows[99]={status="DISABLED"}
eligibilityData.samples.LOAD_CLOSE={status="COMPLETE",unknown=9,rows=rows}
Controls.EligibilityUnknownButton.callback()
assert(Controls.Status.text:find("player=0") and Controls.Status.text:find("player=7"))
assert(not Controls.Status.text:find("player=8") and not Controls.Status.text:find("player=99"))
assert(Controls.Status.text:find("CIV_NOT_READY") and queuedRequest==priorRequest)
Controls.EligibilityUnknownButton.callback()
assert(Controls.Status.text:find("player=8") and not Controls.Status.text:find("player=0"))
assert(rows[0].reason=="EligibilityProbe:12: CIV_NOT_READY")
eligibilityData.samples.LOAD_CLOSE=nil
Controls.EligibilityUnknownButton.callback()
assert(queuedRequest==priorRequest)
Controls.EligibilityButton.callback()
assert(Controls.Status.text:find("INITIALIZE") and queuedRequest==priorRequest)
assert(eligibilityData.samples.INITIALIZE==initialSample and not eligibilityData.samples.LOAD_CLOSE)
ExposedMembers.SPC_P0.AutoRouteProbe={[0]={text="AUTO_CACHE_ONLY",sequence=17}}
local oldSnapshot=SPCP0.NetworkProbe
SPCP0.NetworkProbe=function() error("UI_MUST_NOT_SAMPLE") end
Controls.RouteStateButton.callback()
assert(Controls.Status.text:find("AUTO_CACHE_ONLY") and queuedRequest==priorRequest)
assert(ExposedMembers.SPC_P0.AutoRouteProbe[0].sequence==17)
ExposedMembers.SPC_P0_BackgroundRoutes={version=SPCP0.VERSION,text="SHADOW_CACHE_ONLY",generation=23}
Controls.BackgroundRoutesButton.callback()
assert(Controls.Status.text:find("SHADOW_CACHE_ONLY") and queuedRequest==priorRequest)
assert(ExposedMembers.SPC_P0_BackgroundRoutes.generation==23)

SPCP0.NetworkProbe=oldSnapshot
Controls.CaptureButton.callback()
Controls.CopyButton.callback()
assert(clipboard:find("matched=false") and Controls.Status.text:find("PENDING_OR_ERROR"))
GameEvents.SPC_P0_Request.Fire(0,queuedRequest)
Controls.CopyButton.callback()
assert(clipboard:find("SPC_P0_EXPORT_BEGIN") and clipboard:find("SPC_P0_EXPORT_END"))
assert(clipboard:find("matched=true") and clipboard:find("marker="))
assert(clipboard:find("%[UI%]") and clipboard:find("%[GAMEPLAY%]"))
assert(not clipboard:find("SNAPSHOT_ERROR"),clipboard)
''')
lua.execute(r'''
Controls.BaselineButton.callback()
Controls.CaptureButton.callback()
GameEvents.SPC_P0_Request.Fire(0,queuedRequest)
Controls.CopyButton.callback()
assert(clipboard:find("BASELINE") and clipboard:find("AFTER"))
-- Independent gameplay probes: keep all broad scans poisoned.
local oldGov=city.GetAssignedGovernor
local oldDistricts=city.GetDistricts
local beforeFocus=writes
city.GetAssignedGovernor=nil
player.GetGovernors=function() error("GOVERNOR_OBJECT_LOOKUP_FORBIDDEN") end
GameInfo.GovernorPromotionSets=nil -- no promotion DB scan either
local function focused(button)
 button.callback();GameEvents.SPC_P0_Request.Fire(0,queuedRequest)
 if ContextPtr.update then ContextPtr.update(0.1) end
 assert(Controls.Status.text:find("ACK") or Controls.Status.text:find("READ FAILED"))
 Controls.CopyButton.callback()
 return ExposedMembers.SPC_P0.Snapshot
end
local result=focused(Controls.GovernorButton)
assert(result:find("NOT_READY"))
properties.SPC_P0_GOV_CONTROL_A007=1
result=focused(Controls.GovernorButton)
assert(result:find("CONTROL_OK") and result:find("present=nil established=nil"))
properties.SPC_P0_GOV_PRESENT=1
result=focused(Controls.GovernorButton)
assert(result:find("present=1 established=nil"))
properties.SPC_P0_GOV_ESTABLISHED=1;properties.SPC_P0_GOV_REQ_2=1
result=focused(Controls.GovernorButton)
assert(result:find("present=1 established=1") and result:find("2/3/4=1/nil/nil"))
properties.SPC_P0_GOV_PRESENT=0;properties.SPC_P0_GOV_ESTABLISHED=0;properties.SPC_P0_GOV_REQ_2=0
result=focused(Controls.GovernorButton)
assert(result:find("present=0 established=0") and result:find("2/3/4=0/nil/nil"))
-- Only raw property fixtures; engine evaluation and revocation are NOT simulated.
city.GetDistricts=function() error("CITY_DISTRICT_MEMBERS_MUST_NOT_BE_USED") end
district.GetCity=function() return city end
districtType=0;complete=true
local worker=0
plot.GetWorkerCount=function() return worker end
result=focused(Controls.SpecialistsButton)
assert(result:find("workers=0 complete=true"))
worker=1;result=focused(Controls.SpecialistsButton);assert(result:find("workers=1"))
worker=0;result=focused(Controls.SpecialistsButton);assert(result:find("workers=0"))
plot.GetWorkerCount=nil
focused(Controls.SpecialistsButton)
assert(ExposedMembers.SPC_P0.LastToken==nil and Controls.Status.text:find("GetWorkerCount"))
plot.GetWorkerCount=function() return 0 end
local members=districts.Members
districts.Members=function() local n=0;return function() n=n+1;return n,district end end
focused(Controls.SpecialistsButton)
assert(ExposedMembers.SPC_P0.LastToken==nil and Controls.Status.text:find("DISPLAY_LIMIT"))
districts.Members=function() return nil end
focused(Controls.SpecialistsButton)
assert(ExposedMembers.SPC_P0.LastToken==nil and Controls.Status.text:find("ITERATOR_INVALID"))
districts.Members=members
focused(Controls.SpecialistsButton)
local savedCityGetter=district.GetCity
district.GetCity=function() return {GetID=function() return 999 end,GetOwner=function() return 0 end} end
local filtered=focused(Controls.SpecialistsButton)
assert(filtered:find("NO_SPECIALTY_DISTRICT"))
district.GetCity=savedCityGetter
Controls.SpecialistsButton.callback()
ContextPtr.update(11)
assert(ContextPtr.update==nil and Controls.Status.text:find("NO RESPONSE"))
GameEvents.SPC_P0_Request.Fire(0,queuedRequest)
Controls.CopyButton.callback()
assert(Controls.Status.text:find("ACK"))
assert(writes==beforeFocus)
-- B001: adjacency is UI-only and must not dispatch or consult poisoned wide probes.
local requestBefore=queuedRequest
local actual=8
plot.GetAdjacencyYield=function(self,p,c,d,y) assert(p==0 and c==1 and d==0);return 8 end
district.GetAdjacencyYield=function(self,y) return actual end
Controls.AdjacencyButton.callback()
assert(queuedRequest==requestBefore and Controls.Status.text:find("UI OBSERVATION"))
assert(Controls.Status.text:find("8 / 8"))
actual=16;Controls.AdjacencyButton.callback()
assert(Controls.Status.text:find("8 / 16"))
Controls.NextButton.callback();assert(Controls.Status.text:find("district 1/1"))
plot.GetAdjacencyYield=nil;Controls.AdjacencyButton.callback()
assert(Controls.Status.text:find("UNKNOWN / 16"))
Controls.CopyButton.callback();assert(clipboard:find("UI OBSERVATION"))
-- Cross-yield channels are independently read, not summed or copied from city totals.
GameInfo.Yields=gi({{YieldType="YIELD_SCIENCE",Index=0},{YieldType="YIELD_GOLD",Index=1}},"YieldType")
plot.GetAdjacencyYield=function(self,p,c,d,y) return y==0 and 8 or 0 end
district.GetAdjacencyYield=function(self,y) return y==0 and 16 or 5 end
Controls.AdjacencyButton.callback()
assert(Controls.Status.text:find("YIELD_GOLD: 0 / 5"))
local oldMembers=districts.Members
districts.Members=function() return ipairs({}) end
Controls.AdjacencyButton.callback();assert(Controls.Status.text:find("NO_SPECIALTY_DISTRICT"))
districts.Members=oldMembers
local routes={}
city.GetTrade=function() return {GetOutgoingRoutes=function() return routes end} end
local function readUIRoute()
 local prior=queuedRequest
 Controls.TradeButton.callback()
 assert(queuedRequest==prior) -- no UI route snapshot is used as Gameplay authority
 Controls.CopyButton.callback()
 return clipboard
end
local result=readUIRoute()
assert(result:find("NO_OUTGOING_ROUTES"))
local hostile=setmetatable({TraderUnitID=21,OriginCityPlayer=0,OriginCityID=1,DestinationCityPlayer=0,DestinationCityID=2},
 {__pairs=function() error("NO_ROUTE_RECURSION") end,__tostring=function() error("NO_ROUTE_STRINGIFY") end})
routes={hostile,{TraderUnitID=22,OriginCityPlayer=0,OriginCityID=1,DestinationCityPlayer=3,DestinationCityID=8}}
result=readUIRoute()
assert(result:find("rawCount=2") and result:find("FROM 0:1 Fixture") and result:find("TO   0:2 UNRESOLVED"))
assert(result:find("sameOwnerRaw=true") and result:find("originMatchesSelection=true"))
Controls.NextButton.callback()
assert(Controls.Status.text:find("trader=22") and Controls.Status.text:find("sameOwnerRaw=false"))
Controls.NextButton.callback()
assert(Controls.Status.text:find("trader=21"))
routes={};result=readUIRoute();assert(result:find("rawCount=0"))
city.GetTrade=function() return {} end
readUIRoute();assert(Controls.Status.text:find("GetOutgoingRoutes:ABSENT"))
city.GetTrade=function() return {GetOutgoingRoutes=function() return {} end} end
readUIRoute()

city.GetTrade=nil -- Gameplay event read must work despite the observed missing getter
local eventResult=focused(Controls.RouteEventsButton)
assert(eventResult:find("NO_MATCHING_EVENT_OBSERVED"))
Events.TradeRouteActivityChanged.Fire(0,0,1,0,2,99)
eventResult=focused(Controls.RouteEventsButton)
assert(eventResult:find("FROM 0:1 TO 0:2") and eventResult:find("extra=99"))
assert(eventResult:find("NOT an active%-route list"))
Events.TradeRouteActivityChanged.Fire(3,3,9,3,8)
assert(#ExposedMembers.SPC_P0.TradeEvents==1)
assert(writes==beforeFocus)
local journalResult=focused(Controls.CityJournalButton)
assert(journalResult:find("UNTRACKED_NO_WRITE") and writes==beforeFocus)
city.GetAssignedGovernor=oldGov;city.GetDistricts=oldDistricts
UIManager.SetClipboardString=function() return false end
Controls.CopyButton.callback()
assert(Controls.Status.text:find("Clipboard unavailable/rejected"))
assert(Controls.Status.text:find("ACK |"))
UIManager.SetClipboardString=function() end
Controls.CopyButton.callback()
assert(Controls.Status.text:find("delivery UNVERIFIED"))
assert(not Controls.Status.text:find("Diagnostics copied"))
local before=writes
PlayerConfigurations[0].GetCivilizationTypeName=function() return "CIVILIZATION_SCOTLAND" end

GameEvents.SPC_P0_Request.Fire(0,{Action="MARK_CITY",CityID=1,Token="forbidden"})
assert(writes==before)
Controls.MarkButton.callback()
assert(Controls.Status.text:find("OUTSIDE_TEST_CIV"))
''')
print("LOCAL_SIMULATION_PASS: Lua/XML, dormant pure fixtures, property-only UI/gameplay with forbidden broad probes, native governor property/control/present/established/threshold/revocation fixtures with governor getters forbidden, and specialist 0-1-0/limit fixtures, UI adjacency/policy-candidate/cross-yield/UNKNOWN and UI route direction/paging/removal and Gameplay scoped raw-event fixtures, scalar safety, one write, idempotency, mock reload, failure stages, pending export, matching ACK, civ rejection. IN_GAME=USER_GAME_TEST_REQUIRED")
