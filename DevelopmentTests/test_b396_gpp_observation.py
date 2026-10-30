"""B396 actual cold P0 include closure/transport and business-path differential.
Native API values are doubles. No user-game count semantics or gameplay fix claim.
"""
from pathlib import Path
import json,subprocess,unittest
from unittest.mock import patch
from lupa.lua51 import LuaRuntime
from refactor_harness import ROOT,TrackedLua51,SOURCES
from hashlib import sha256

PANEL=ROOT/'Mod/UI/P0Panel.lua'
KINDS=('RESEARCH','CULTURE','INDUSTRY','COMMERCE')
DISTRICTS=('DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE','DISTRICT_COMMERCIAL_HUB')

def cold(kind='CULTURE',mode='on'):
 l=LuaRuntime(unpack_returned_tuples=True)
 l.execute("""
  ExposedMembers={};printed={};loads=0;reads=0;workerReads=0;commands=0;notifies=0
  print=function(s)printed[#printed+1]=s end
  Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return 12 end}
  GameConfiguration={IsAnyMultiplayer=function()return false end}
  PlayerConfigurations={[0]={GetCivilizationTypeName=function()return 'CIVILIZATION_SPC_AMERICA'end,GetLeaderTypeName=function()return 'LEADER_SPC_T_ROOSEVELT'end}}
  Players={[0]={IsHuman=function()return true end,GetGreatPeoplePoints=function()return {GetPointsPerTurn=function(_,i)return 20+i end}end}}
  city={GetOwner=function()return 0 end,GetID=function()return 1 end,GetX=function()return 2 end,GetY=function()return 3 end}
  district={GetType=function()return 7 end,GetCity=function()return city end,GetX=function()return 4 end,GetY=function()return 5 end}
  city.GetDistricts=function()return {Members=function()local done;return function()if not done then done=true;return 0,district end end end}end
  Map={GetPlot=function()return {GetIndex=function()return 33 end}end,GetPlotByIndex=function()return {GetWorkerCount=function()workerReads=workerReads+1;return 1 end}end}
  UI={GetHeadSelectedCity=function()return city end,GetInterfaceModeParameter=function(k)return 99 end}
  CityCommandTypes={MANAGE=3,PARAM_MANAGE_CITIZEN=4};CityCommandResults={PLOTS=1,CITIZENS=2,MAX_CITIZENS=3,LOCKED_CITIZENS=4}
  rows={{[8]=33},{[8]=2},{[8]=3},{[8]=1}}
  CityManager={GetCommandTargets=function(c,cmd,p)assert(cmd==3 and p[4]==99);reads=reads+1;return rows end,RequestCommand=function()commands=commands+1;error('FORBIDDEN_WRITE')end}
  LuaEvents={SPC_B205TrainingTrace=function()notifies=notifies+1 end}
  GameInfo={Districts={},GreatPersonClasses={}}
  for i,k in ipairs({'SCIENTIST','WRITER','ARTIST','MUSICIAN','ENGINEER','MERCHANT'})do GameInfo.GreatPersonClasses['GREAT_PERSON_CLASS_'..k]={Index=i}end
 """)
 l.globals().fixtureKind=kind
 district=DISTRICTS[KINDS.index(kind)]if kind in KINDS else 'DISTRICT_HARBOR'
 l.globals().fixtureDistrict=district;l.execute('GameInfo.Districts[7]={DistrictType=fixtureDistrict}')
 def include(name):
  if name=='ExpeditionTrainingDiagnostics':
   l.execute('loads=loads+1')
   if mode in ('include','missing'):raise FileNotFoundError('OPTIONAL_TRANSPORT_MISSING')
   if mode=='construct':
    l.execute("SPCExpeditionTrainingDiagnostics={ENABLED=true,New=function()error('NEW_FAILED')end}");return
   if mode=='noop':
    l.execute("SPCExpeditionTrainingDiagnostics={ENABLED=true,New=function()return {id='DISABLED',Record=function()end}end}");return
   if mode=='sink':
    l.execute("SPCExpeditionTrainingDiagnostics={ENABLED=true,New=function()return {Record=function()error('SINK_FAILED')end}end}");return
  if name=='CultureDiagnostics' and mode=='deleted':raise FileNotFoundError('OPTIONAL_OBSERVER_REMOVED')
  candidates=(ROOT/'Mod/UI'/(name+'.lua'),ROOT/'Mod'/(name+'.lua'))
  p=next((p for p in candidates if p.is_file()),None)
  if p is None:raise FileNotFoundError(name)
  l.execute(p.read_text())
 l.globals().include=include
 # Execute the original include closure,not a pre-injected logger/Render mock.
 source=PANEL.read_text();l.execute(source[:source.index('local P=SPCP0')])
 l.execute("assert(SPCExpeditionTrainingDiagnostics==nil and ExposedMembers.SPC_B205TrainingTrace==nil)")
 if mode=='off':l.execute('SPCCultureDiagnostics.ENABLED=false')
 if mode=='disabled':l.execute("SPCExpeditionTrainingDiagnostics={ENABLED=false,New=function()error('DISABLED_REPLACED')end};priorLogger=SPCExpeditionTrainingDiagnostics")
 if mode=='disabled-thin':l.execute('SPCExpeditionTrainingDiagnostics={ENABLED=false};priorLogger=SPCExpeditionTrainingDiagnostics')
 if mode=='present':
  l.execute((ROOT/'Mod/ExpeditionTrainingDiagnostics.lua').read_text());l.execute('priorLogger=SPCExpeditionTrainingDiagnostics')
 if mode=='internal-noop':l.execute("setmetatable(ExposedMembers,{__newindex=function(t,k,v)if k=='SPC_B205TrainingTrace'then error('ROOT_UNAVAILABLE')end;rawset(t,k,v)end})")
 body=source[source.index('local function displayResponse()'):source.index('-- B060 read/control')]
 l.execute(r"""
  local P=SPCP0;local pendingToken,pendingAction,pageCity,page,readings='click1','LV2_GPP_READ',1,1,{};local localReport
  local function status(s)displayed=s end
  ExposedMembers.SPC_P0={Version=P.VERSION,LastToken='click1',Snapshot='city=1 '..fixtureKind..' ACTIVE=4 workers=1\nNative EMPIRE GPP/turn: old'}
 """+body+"""
  function reply(token)
   pendingToken=token or 'click1';ExposedMembers.SPC_P0.LastToken=pendingToken
   return displayResponse()
  end
 """)
 return l

class ColdP0(unittest.TestCase):
 def test_actual_include_reply_render_transport_and_collector_four_professions(self):
  from collect_expedition_trace import fields,train_line
  for kind in KINDS:
   l=cold(kind);l.execute("assert(reply());assert(reads==1 and workerReads==1 and commands==0 and loads==1);assert(displayed:find('UI EMPIRE GPP/turn:',1,true));assert(not displayed:find('Native EMPIRE GPP/turn:',1,true));for i=1,100 do reply()end;assert(reads==1 and loads==1)")
   line=next(str(v)for v in l.globals().printed.values()if 'point=GPP_EXPLICIT_UI'in str(v));f=fields(line)
   self.assertEqual((f['specialization'],f['requestKey'],f['eventIndex'],f['workers'],f['count'],f['expectedNumber'],f['actualNumber']),(kind,'click1','33','2','1','3','1'))
   self.assertEqual(train_line(line),line)
 def test_off_deleted_missing_constructor_noop_and_sink_preserve_report(self):
  reports=[]
  for mode in ('on','off','deleted','missing','include','construct','noop','internal-noop','sink','disabled','disabled-thin'):
   l=cold(mode=mode);l.execute("assert(reply());assert(reply());assert(commands==0)");reports.append(l.globals().displayed)
   self.assertEqual(l.globals().reads,1 if mode in ('on','sink')else 0,mode)
   self.assertLessEqual(l.globals().loads,1,mode)
   if mode in ('off','deleted','disabled','disabled-thin'):self.assertEqual(l.globals().loads,0)
   if mode in ('disabled','disabled-thin'):l.execute('assert(SPCExpeditionTrainingDiagnostics==priorLogger)')
  self.assertTrue(all(x==reports[0]for x in reports))
 def test_preserve_existing_logger_and_attempt_missing_transport_only_once(self):
  l=cold(mode='present');l.execute('reply();assert(loads==0 and reads==1 and priorLogger==SPCExpeditionTrainingDiagnostics)')
  l=cold(mode='missing');l.execute("for i=1,30 do reply('t'..i)end;SPCCultureDiagnostics.Emit('CULTURE_GP','TEST',function()error('NO_BUILDER')end);assert(loads==1 and reads==0)")
 def test_four_profession_anchor_fences_unknown_and_future_excluded(self):
  for change in ("GameInfo.Districts[7].DistrictType='DISTRICT_THEATER'", "rows[4][8]=nil", "rows[1][9]=33", "local f=CityManager.GetCommandTargets;CityManager.GetCommandTargets=function(...)local v=f(...);UI.GetHeadSelectedCity=function()return nil end;return v end"):
   l=cold('INDUSTRY');l.execute(change+";reply();local rows=ExposedMembers.SPC_B205TrainingTrace.entries;local text=rows[#rows].line;assert(text:find('readStatus=UNKNOWN',1,true)and not text:find('workers=',1,true));assert(commands==0)")
  l=cold('HARBOR');l.execute('reply();assert(reads==0 and loads==0 and commands==0)')
 def test_explicit_GP_survives_automatic_budget_and_UI_cap_precedes_sampling(self):
  l=cold();l.execute("reply();for i=1,400 do SPCCultureDiagnostics.Emit('CULTURE_GP','NOISE',function()return {owner=0,city=i}end)end;SPCCultureDiagnostics.Emit('CULTURE_GP','GPP_EXPLICIT_GP',function()return {owner=0,city=1,requestKey='pair',workers=1}end);local root=ExposedMembers.SPC_B205TrainingTrace;local text=root.entries[#root.entries].line;assert(text:find('point=GPP_EXPLICIT_GP',1,true)and text:find('traceRole=CULTURE_GPP_READ_GP',1,true));for i=2,400 do reply('t'..i)end;assert(reads==192 and workerReads==192);assert(root.entries[#root.entries].line:find('point=LIMIT_REACHED',1,true))")

class NativeScope(unittest.TestCase):
 def test_existing_identity_invalidations_and_business_notifications_are_equal(self):
  from test_refactor_s5d4b1 import native
  results=[]
  for mode in ('on','off','absent','throw','lookup','sink'):
   c=native();c.load('CultureDiagnostics')
   c.execute("identity=0;invalidations=0;notifications=0;observed={};local player=P.IsTestPlayer;P.IsTestPlayer=function(pid)identity=identity+1;return player(pid)end;local invalid=d.InvalidateCommitted;d.InvalidateCommitted=function(...)invalidations=invalidations+1;return invalid(...)end;local emit=d.Emit;d.Emit=function(...)notifications=notifications+1;return emit(...)end;SPCExpeditionTrainingDiagnostics={New=function()return {Record=function(_,r)observed[#observed+1]=r end}end}")
   if mode=='off':c.execute('SPCCultureDiagnostics.ENABLED=false')
   if mode=='absent':c.execute('SPCCultureDiagnostics=nil')
   if mode=='throw':c.execute("SPCCultureDiagnostics.Emit=function()error('OPTIONAL_FAILED')end")
   if mode=='lookup':c.execute("SPCCultureDiagnostics=setmetatable({},{__index=function()error('LOOKUP_FAILED')end})")
   if mode=='sink':c.execute("SPCExpeditionTrainingDiagnostics.New=function()return {Record=function()error('SINK_FAILED')end}end")
   c.execute("n.Workers({player=0,city=1},'NATIVE_WORKER_CHANGED');n.Workers({player=1,city=2},'NATIVE_WORKER_CHANGED');n.Workers({},'UI_WORKERS_DIRTY');result={identity,invalidations,notifications,d.Generation(0,'COMMERCE'),d.Generation(0,'COMMERCE',1),d.sequence}")
   results.append(tuple(c.eval('result').values()))
   if mode=='on':c.execute('assert(#observed==2 and observed[1].owner==0 and observed[2].owner==0)')
  self.assertTrue(all(v==results[0]for v in results),results)

class DirtyTransport(unittest.TestCase):
 def test_observations_do_not_change_packets_retries_foreign_or_reentry(self):
  from test_refactor_s5d4b2 import ui
  results=[]
  for mode in ('on','off','absent','throw','lookup','sink'):
   for behavior in ('nil','true','false','throw','reentry'):
    c=ui();c.load('CultureDiagnostics');c.execute("diag={};SPCExpeditionTrainingDiagnostics={New=function()return {Record=function(_,r)diag[#diag+1]=r end}end};local player=P.IsTestPlayer;identity=0;P.IsTestPlayer=function(...)identity=identity+1;return player(...)end")
    if mode=='off':c.execute('SPCCultureDiagnostics.ENABLED=false')
    if mode=='absent':c.execute('SPCCultureDiagnostics=nil')
    if mode=='throw':c.execute("SPCCultureDiagnostics.Emit=function()error('OPTIONAL_FAILED')end")
    if mode=='lookup':c.execute("SPCCultureDiagnostics=setmetatable({},{__index=function()error('LOOKUP_FAILED')end})")
    if mode=='sink':c.execute("SPCExpeditionTrainingDiagnostics.New=function()return {Record=function()error('SINK_FAILED')end}end")
    script="if not injected then injected=true;Events.CityWorkerChanged.Fire(0,1)end"if behavior=='reentry'else "error('UNKNOWN_SEND')"if behavior=='throw'else 'return '+behavior
    c.execute("UI.RequestPlayerOperation=function(pid,op,p)sends=sends+1;packets[sends]=p;"+script+" end;Events.CityWorkerChanged.Fire(0,1);publish();publish();for i=1,1000 do publish()end;Events.CityWorkerChanged.Fire(1,2);publish();result={identity,sends};encoded={};for _,p in ipairs(packets)do encoded[#encoded+1]=table.concat({p.Action,p.Token,tostring(p.CityID),tostring(p.WorkerOnly),tostring(p.FactsChanged)},'|')end;shutdown()")
    vector=(behavior,tuple(c.eval('result').values()),tuple(c.eval('encoded').values()))
    if mode=='on':c.execute("assert(#diag>0);local ret=false;for _,r in ipairs(diag)do if r.point=='GPP_DIRTY_RETURN'then ret=true end end;assert(ret)")
    results.append((mode,vector))
  baseline=[v for mode,v in results if mode=='on']
  for mode in ('off','absent','throw','lookup','sink'):self.assertEqual([v for m,v in results if m==mode],baseline)
 def test_actual_Gameplay_ingress_survives_missing_or_throwing_observer(self):
  from test_refactor_s5d4b2 import active_investment,load_request
  vectors=[]
  for mode in ('on','off','absent','throw','lookup','sink'):
   l=active_investment();load_request(l);l.globals().include('CultureDiagnostics')
   l.execute("ingress={};SPCExpeditionTrainingDiagnostics={New=function()return {Record=function(_,r)ingress[#ingress+1]=r end}end}")
   if mode=='off':l.execute('SPCCultureDiagnostics.ENABLED=false')
   if mode=='absent':l.execute('SPCCultureDiagnostics=nil')
   if mode=='throw':l.execute("SPCCultureDiagnostics.Emit=function()error('OPTIONAL_FAILED')end")
   if mode=='lookup':l.execute("SPCCultureDiagnostics=setmetatable({},{__index=function()error('LOOKUP_FAILED')end})")
   if mode=='sink':l.execute("SPCExpeditionTrainingDiagnostics.New=function()return {Record=function()error('SINK_FAILED')end}end")
   l.execute("d.workers=1;rawRequest(0,{Action='LV2_GPP_DIRTY',Token='read1',CityID=1,WorkerOnly=true,FactsChanged=false});drainworker();assert(gpp(c,'RESEARCH')==2);result={reads,writes,shared.FactChanges.Generation(0,'COMMERCE'),shared.FactChanges.Generation(0,'COMMERCE',1)}")
   vectors.append(tuple(l.eval('result').values()))
   if mode=='on':l.execute("local found=false;for _,r in ipairs(ingress)do if r.point=='GPP_DIRTY_INGRESS'then found=true;assert(r.requestKey=='read1'and r.observerSide=='GAMEPLAY')end end;assert(found)")
  self.assertTrue(all(v==vectors[0]for v in vectors),vectors)

 def test_ingress_label_matches_conservative_nil_fact_flag(self):
  from test_refactor_s5d4b2 import active_investment,load_request
  l=active_investment();load_request(l);l.globals().include('CultureDiagnostics')
  l.execute("rows={};SPCExpeditionTrainingDiagnostics={New=function()return {Record=function(_,r)rows[#rows+1]=r end}end};rawRequest(0,{Action='LV2_GPP_DIRTY',Token='nil-facts',CityID=1,WorkerOnly=true});local found=false;for _,r in ipairs(rows)do if r.point=='GPP_DIRTY_INGRESS'then found=true;assert(r.recordType=='CONSERVATIVE')end end;assert(found)")

if __name__=='__main__':unittest.main()
