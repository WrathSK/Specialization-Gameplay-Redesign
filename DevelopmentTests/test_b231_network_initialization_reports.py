"""B231 actual Lua counterexamples and observation isolation. Local evidence only."""
from pathlib import Path
import unittest
from test_culture_network import fixture
from test_expedition_trace_reader import reader
R=Path(__file__).resolve().parents[1]
ROUTES="send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3)"

class Initialization(unittest.TestCase):
 def fresh(self):
  l=fixture(False);l.execute('print=function()end');return l
 def test_cityless_player_does_not_abort_real_initialization(self):
  l=self.fresh();l.execute("Players[63]={GetCities=function()return nil end};complete(4,1);"+ROUTES+";assert(cn.ready and not cn.error and amount(cities[1])==1 and propertyWrites==0)")
 def test_empty_collection_also_allowed(self):
  l=self.fresh();l.execute("Players[63]={GetCities=function()return {Members=function()return pairs({})end}end};"+ROUTES+";assert(cn.ready)")
 def test_foreign_saved_owned_carrier_still_cleared(self):
  l=self.fresh();l.execute("local c=equip({id=9,owner=9,GetID=function()return 9 end,GetOwner=function()return 9 end});c.present.BUILDING_SPC_CULTURE_NETWORK_CULTURE_0=true;c.GetBuildings=function()return {city=c,HasBuilding=function(_,id)return c.present[id]==true end}end;Players[9]={GetCities=function()return {Members=function()return pairs({c})end}end};Players[63]={GetCities=function()return nil end};"+ROUTES+";assert(cn.ready and not c.present.BUILDING_SPC_CULTURE_NETWORK_CULTURE_0)")
 def test_getter_exception_keeps_not_ready_with_phase_and_safe_location(self):
  l=self.fresh();l.execute("Players[63]={GetCities=function()error('private/path/CultureNetwork.lua:237: attempt to index a nil value secret-contents',0)end};"+ROUTES+";assert(not cn.ready and cn.failure.phase=='INITIAL_CITY_COLLECTION' and cn.failure.errorClass=='LUA_NIL' and cn.failure.errorFile=='CultureNetwork.lua' and cn.failure.errorLine==237 and cn.failure.owner==63);local text=cn.Describe(0,cities[1]);assert(text:find('LUA_NIL') and text:find('INITIAL_CITY_COLLECTION') and not text:find('CN_NOT_READY') and not text:find('private') and not text:find('secret'));for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do assert(not e.line:find('private') and not e.line:find('secret'))end")
 def test_cleanup_failure_not_mistaken_for_missing_collection(self):
  l=self.fresh();l.execute("failHas='BUILDING_SPC_CULTURE_NETWORK_CULTURE_0';"+ROUTES+";assert(not cn.ready and cn.failure.phase=='INITIAL_CARRIER_CLEANUP' and cn.failure.errorCode=='CN_PRESENCE_UNKNOWN');failHas=nil;fire('PlayerTurnActivated',0);fire('GameCoreEventPublishComplete');assert(cn.ready and not cn.failure)")
 def test_definition_failure_is_not_generic_not_ready(self):
  l=self.fresh();l.execute("yieldRows={};"+ROUTES+";local text=cn.Describe(0,cities[1]);assert(not cn.ready and cn.failure.phase=='DEFINITION_VALIDATION' and text:find('CN_YIELD_INVALID') and not text:find('CN_NOT_READY'))")
 def test_nil_player_recovery_remains_idempotent(self):
  l=self.fresh();l.execute("Players[63]={GetCities=function()return nil end};complete(4,1);"+ROUTES+";local a,b=created,removed;for i=1,5 do fire('LoadScreenClose');fire('PlayerTurnActivated',0);fire('GameCoreEventPublishComplete')end;assert(created==a and removed==b and propertyWrites==0)")

class SharedReports(unittest.TestCase):
 def ready(self):
  l=fixture();l.execute('print=function()end');return l
 def test_missing_consumer_keeps_public_routes_centers_and_sources(self):
  l=self.ready();l.execute("shared.CultureNetwork=nil;local s=net.Report(0,cities[1],false);assert(s:find('已发布商路 3') and s:find('来源城 3') and s:find('中心 2') and s:find('文化：本城接入 1') and s:find('未建立'))")
 def test_throwing_consumer_cannot_hide_shared_report(self):
  l=self.ready();l.execute("cn.Describe=function()error('private/path/CultureNetwork.lua:350: attempt to call a nil value secret')end;local s=net.Report(0,cities[1],false);assert(s:find('已发布商路 3') and s:find('文化收益报告失败') and s:find('CultureNetwork.lua:350') and not s:find('private') and not s:find('secret'))")
 def test_failed_initialization_keeps_shared_report(self):
  l=fixture(False);l.execute("print=function()end;yieldRows={};"+ROUTES+";local s=net.Report(0,cities[1],false);assert(s:find('已发布商路 3') and s:find('DEFINITION_VALIDATION') and s:find('CN_YIELD_INVALID'))")
 def test_no_refresh_verification_facts_or_business_writes(self):
  l=self.ready();l.execute("complete(4,1);cn.SourceChanged(0,4);local a,b=created,removed;local rev=net.players[0].inputRevision;local n=counts.derive;net.Refresh=function()error('REFRESH')end;net.Verified=function()error('VERIFY')end;net.Input=function()error('INPUT')end;shared.EffectiveFacts.Read=function()error('FACTS')end;for p=1,3 do assert(net.Report(0,cities[1],true,p):find('公共网络'))end;assert(created==a and removed==b and propertyWrites==0 and net.players[0].inputRevision==rev and counts.derive==n)")
 def test_missing_snapshot_not_reported_as_zero(self):
  l=fixture(False);l.execute("print=function()end;local s=net.Report(0,cities[1],false);assert(s:find('NETWORK_NO_INPUT') and s:find('已发布商路 未知') and s:find('角色尚未确认') and net.players[0]==nil and not cn.ready)")
 def test_known_empty_routes_distinct_from_missing(self):
  l=self.ready();l.execute("send('',0);local s=net.Report(0,cities[1],false);assert(s:find('已发布商路 0') and s:find('已就绪') and not s:find('NETWORK_NO_INPUT'))")
 def test_retained_view_marked_pending_without_triggering_revalidation(self):
  l=self.ready();l.execute("net.players[0].availability='NEEDS_REVALIDATION';local s=net.Report(0,cities[1],false);assert(s:find('上次已发布拓扑') and s:find('已发布商路 3') and s:find('NETWORK_REVALIDATION_PENDING'))")
 def test_mismatched_version_not_presented_as_current(self):
  l=self.ready();l.execute("net.players[0].derivedFor=999;local s=net.Report(0,cities[1],false);assert(s:find('NETWORK_VIEW_UNAVAILABLE') and s:find('来源城 未知'))")
 def test_details_pagination_and_safe_trace_relations(self):
  l=self.ready();l.execute("local s='';for page=1,3 do s=s..net.Report(0,cities[2],true,page)end;assert(s:find('来源 文化') and s:find('贸易中心') and s:find('本中心接入 文化') and s:find('商路 C4') and s:find('→ C2'));local found={};for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do if e.stage=='NETWORK_LINK'then found[e.relation]=true;assert(not e.line:find('C4'))end end;assert(found.SOURCE and found.CENTER and found.CENTER_INPUT and found.ROUTE)")
 def test_late_reader_preserves_phase_and_public_evidence(self):
  l=fixture(False);l.execute("print=function()end;yieldRows={};"+ROUTES+";net.Report(0,cities[1],false);lines={};print=function(s)lines[#lines+1]=s end")
  l.execute(reader.command('trace','MARK:','DONE'))
  rows=[reader.training_line(s) for s in l.globals().lines.values()]
  self.assertTrue(any(s and 'stage=NETWORK_PUBLIC' in s and 'routeCount=3' in s for s in rows))
  self.assertTrue(any(s and 'phase=DEFINITION_VALIDATION' in s and 'errorCode=CN_YIELD_INVALID' in s for s in rows))
 def test_trace_bounded_under_repeated_detail_reads(self):
  l=self.ready();l.execute("for i=1,200 do net.Report(0,cities[1],true,i)end;assert(#ExposedMembers.SPC_B205TrainingTrace.entries<=64)")
 def test_selected_owner_guard_and_no_business_writes(self):
  l=self.ready();l.execute("local a,b=created,removed;cities[1].owner=9;local s=net.Report(0,cities[1],true);assert(s:find('NETWORK_SELECTED_OWNER_CHANGED') and created==a and removed==b)")
 def test_real_gameplay_action_dispatch(self):
  text=(R/'Mod/Gameplay.lua').read_text()
  branch=text.split('if params.Action=="NETWORK_READ" or params.Action=="NETWORK_DETAIL" then',1)[1].split('\n  end',1)[0]
  l=self.ready();l.execute('stage=function()end;params={Action="NETWORK_READ",Token="test",Page=1};playerID=0;city=cities[1];shared.CultureNetwork=nil')
  l.execute('(function()'+branch+' end)()')
  self.assertIn('已发布商路 3',l.globals().shared.Snapshot)
  self.assertEqual(l.globals().shared.LastToken,'test')
 def test_unknown_filename_and_raw_message_redacted(self):
  l=self.ready();l.execute("local f=SPCExpeditionTrainingDiagnostics.Failure('private/path/username.lua:81: token-secret','PUBLIC_REPORT');assert(f.errorFile=='UNKNOWN' and f.errorLine==81 and f.errorCode=='READ_ERROR');assert(not net.Report(0,cities[1],false):find('token-secret'))")
 def test_no_timer_or_operation_in_new_network_paths(self):
  for path in ['Mod/CultureNetwork.lua','Mod/NetworkBridge.lua']:
   text=(R/path).read_text()
   for word in ['SetUpdate','SystemUpdateUI','RequestOperation','RequestCommand']:
    self.assertNotIn(word,text)
if __name__=='__main__':unittest.main()
