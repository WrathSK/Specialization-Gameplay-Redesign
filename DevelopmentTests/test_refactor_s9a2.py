"""Production observers use current selected owner view; idle native reads stay zero."""
from pathlib import Path
from unittest.mock import patch
import json,unittest
from refactor_harness import ROOT,Context,TrackedLua51,legacy_source_observation,measure
import test_b246_development as development
import test_store_write_boundaries as store_fixture

KINDS=('CapitalInvestment','DevelopmentInvestment','Commerce')


def ui(kind,observer=True):
 c=Context('UI');c.load('UI/SafeAdapters');c.execute("""
 print=function()end;P={VERSION='S9a2',IsTestPlayer=function(pid)return pid==0 end};SPCP0=P
 Game.GetLocalPlayer=function()return 0 end
 owner=0;selected=1;headReads=0;notifications=0;rowReads=0
 function city(id)return {GetOwner=function()return owner end,GetID=function()return id end}end
 cities={[1]=city(1),[2]=city(2)}
 UI={GetHeadSelectedCity=function()headReads=headReads+1;return cities[selected]end}
 Locale={Lookup=function(k)if localeError then error('TEMPORARY_LOCALIZATION')end;return k end}
 views={['0:1']={revision=1,available=true,identity='COMMERCE',potential=3,token='TOKEN1',reference={owner=0,cityID=1,x=10,y=11,token='TOKEN1',changes=0}},
 ['0:2']={revision=2,available=true,identity='COMMERCE',potential=3,token='TOKEN2',reference={owner=0,cityID=2,x=20,y=21,token='TOKEN2',changes=0}}}
 backend={views=views,revision=2};ExposedMembers.SPC_P0={}
 SPCDevelopmentInvestmentRead={New=function()end};include=function()end
 """);c.execute('ExposedMembers.SPC_P0[...]=backend',kind);c.load('UI/'+kind+'UI')
 c.execute('factory=_G[...];api=factory.New(P,function(pid,id)notifications=notifications+1;lastNotice=pid..\':\'..id;if onNotify then onNotify()end end,'+('SPCSafeAdapters.NewViewObserver()'if observer else'nil')+');project=factory.PROJECT', 'SPC'+kind+'UI')
 return c


class ActualUI(unittest.TestCase):
 def test_three_production_adapters_skip_unrelated_city_refresh_without_new_idle_head_reads(self):
  for kind in KINDS:
   c=ui(kind);c.execute("api.Items({City=cities[1],ProjectItems={{Type=project}}});api.Publish();assert(notifications==0);headReads=0;for i=1,1000 do api.Publish()end;assert(headReads==0);views['0:2'].revision=3;backend.revision=3;api.Publish();assert(headReads==1 and notifications==0);views['0:1'].revision=4;backend.revision=4;api.Publish();assert(headReads==2 and notifications==1 and lastNotice=='0:1')")
  measure('S9a2_selected_owner_view',{'production_adapters':3,'unrelated_city_refresh_notifications':0,'same_city_change_notifications':1,'thousand_idle_extra_head_reads':0,'request_or_native_queue_change':False})
 def test_same_turn_second_change_and_selected_view_deletion_recovery_are_not_deduplicated(self):
  for kind in KINDS:
   c=ui(kind);c.execute("api.Publish();notifications=0;for rev=3,4 do backend.revision=rev;views['0:1'].revision=rev;api.Publish()end;assert(notifications==2);local row=views['0:1'];views['0:1']=nil;backend.revision=5;api.Publish();assert(notifications==3);views['0:1']=row;row.revision=6;backend.revision=6;api.Publish();assert(notifications==4)")
 def test_selection_native_render_updates_single_slot_without_new_selection_listener(self):
  for kind in KINDS:
   c=ui(kind);c.execute("api.Items({City=cities[1],ProjectItems={}});api.Publish();selected=2;api.Items({City=cities[2],ProjectItems={}});notifications=0;headReads=0;api.Publish();assert(headReads==0 and notifications==0);views['0:1'].revision=3;backend.revision=3;api.Publish();assert(notifications==0);views['0:2'].revision=4;backend.revision=4;api.Publish();assert(notifications==1 and lastNotice=='0:2')")
 def test_backend_restart_same_revision_and_reused_city_reference_are_not_old_success(self):
  for kind in KINDS:
   c=ui(kind);c.execute("api.Publish();notifications=0;backend={views=views,revision=2};ExposedMembers.SPC_P0[...]=backend;api.Publish();assert(notifications==1);views['0:1'].reference.x=99;backend.revision=3;api.Publish();assert(notifications==2);views['0:1'].token='NEW_TOKEN';backend.revision=4;api.Publish();assert(notifications==3)",kind)
 def test_failed_render_does_not_suppress_later_same_version_publication_recovery(self):
  for kind in KINDS:
   c=ui(kind);c.execute("ad=SPCSafeAdapters.New();e=ad.Add('UI',function(item)return item.Type==project end,{},function()return api end);ad.Items(e,{City=cities[1],ProjectItems={{Type=project}}});api.Publish();notifications=0;backend.revision=3;views['0:1'].revision=3;localeError=true;local data={City=cities[1],ProjectItems={{Type=project,Name='original'}}};ad.Items(e,data);assert(data.ProjectItems[1].Name=='original'and data.ProjectItems[1].Disabled);localeError=false;api.Publish();assert(notifications==1)")
 def test_publication_latches_before_synchronous_notify_reentry(self):
  for kind in KINDS:
   c=ui(kind);c.execute("onNotify=function()api.Publish();api.Items({City=cities[1],ProjectItems={}})end;api.Publish();assert(notifications==1);views['0:1'].revision=3;backend.revision=3;api.Publish();assert(notifications==2)")
 def test_actual_production_registry_injects_three_distinct_observers(self):
  from refactor_defect_fixtures import panel
  c=panel("received={};for _,name in ipairs({'CapitalInvestmentUI','DevelopmentInvestmentUI','CommerceUI'})do local n=name;local ctor=_G['SPC'..n].New;_G['SPC'..n].New=function(p,notify,observer)received[n]=observer;return ctor(p,notify)end end")
  c.execute("local a,b,c=received.CapitalInvestmentUI,received.DevelopmentInvestmentUI,received.CommerceUI;assert(type(a.SourceChanged)=='function'and type(b.Observe)=='function'and type(c.Close)=='function'and not rawequal(a,b)and not rawequal(b,c)and not rawequal(a,c))")
 def test_close_releases_observer_and_blocks_late_publish_native_reads(self):
  for kind in KINDS:
   c=ui(kind);c.execute("api.Publish();headReads=0;api.Close();backend.revision=3;api.Publish();assert(headReads==0)")
 def test_legacy_constructor_without_observer_keeps_previous_module_refresh_contract(self):
  for kind in KINDS:
   c=ui(kind,False);c.execute("api.Publish();assert(notifications==1);views['0:2'].revision=3;backend.revision=3;api.Publish();assert(notifications==2)")


class Observer(unittest.TestCase):
 def test_unknown_versions_or_references_never_cache_success_and_recovery_is_observed(self):
  c=Context('UI');c.load('UI/SafeAdapters');c.execute("b={revision=1};o=SPCSafeAdapters.NewViewObserver();v={revision=7,token='T',reference='0:1:2:3'};assert(o.SourceChanged(b)and o.Observe(b,'0:1',v));assert(not o.Observe(b,'0:1',v));for _,bad in ipairs({'VERSION','REFERENCE','TOKEN'})do local old=v[bad=='VERSION'and'revision'or bad=='TOKEN'and'token'or'reference'];local field=bad=='VERSION'and'revision'or bad=='TOKEN'and'token'or'reference';v[field]=nil;assert(o.Observe(b,'0:1',v));v[field]=old;assert(o.Observe(b,'0:1',v))end;v.reference={owner=0,cityID=1,x=2,y=3,token='T',changes=0};assert(o.Observe(b,'0:1',v));v.reference.x=0/0;assert(o.Observe(b,'0:1',v));v.reference.x=2;assert(o.Observe(b,'0:1',v))")
 def test_closed_observer_drops_old_backend_and_cannot_reacquire_it(self):
  c=Context('UI');c.load('UI/SafeAdapters');c.execute("o=SPCSafeAdapters.NewViewObserver();weak=setmetatable({},{__mode='v'});do local b={revision=1};weak[1]=b;assert(o.SourceChanged(b));o.Close();assert(not o.SourceChanged(b)and not o.Observe(b,'0:1',{revision=1,token='T',reference='R'}))end;collectgarbage('collect');assert(weak[1]==nil)")
 def test_observer_retains_only_single_scalar_header_and_does_not_keep_view_or_native_city(self):
  c=Context('UI');c.load('UI/SafeAdapters');c.execute("o=SPCSafeAdapters.NewViewObserver();b={revision=1};weak=setmetatable({},{__mode='v'});do local v={revision=1,token='T',reference={owner=0,cityID=1,x=2,y=3}};weak[1]=v;weak[2]=v.reference;o.Observe(b,'0:1',v)end;collectgarbage('collect');assert(weak[1]==nil and weak[2]==nil);for i=1,100 do assert(o.Observe(b,'0:'..i,{revision=i,token='T',reference='0:1:2:3'}))end;assert(not o.Observe(b,'0:100',{revision=100,token='T',reference='0:1:2:3'}))")


class RealProducer(unittest.TestCase):
 def test_actual_Development_deleted_view_publishes_once_without_money_or_history_write(self):
  with patch.object(store_fixture,'LuaRuntime',TrackedLua51),legacy_source_observation():v=development.runtime()
  v.execute("local id=source:GetID();assert(dev.views['0:'..id]);local r=dev.revision;local w=T.writes();local b=balance;local m=moneyCalls;local get=Players[0].GetCities;Players[0].GetCities=function(...)local cities=get(...);local find=cities.FindID;cities.FindID=function(o,n)if n==id then return nil end;return find(o,n)end;return cities end;dev.Refresh(0,id);assert(dev.views['0:'..id]==nil and dev.revision==r+1 and T.writes()==w and balance==b and moneyCalls==m);dev.Refresh(0,id);assert(dev.revision==r+1)")


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S8b10'])])

if __name__=='__main__':unittest.main()
