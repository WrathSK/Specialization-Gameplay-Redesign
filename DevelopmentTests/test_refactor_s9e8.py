"""R13 actual Capital/Store plus UI: delayed Treasury delivery is not a new balance."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import subprocess,unittest
from lupa.lua51 import lua_type
from refactor_harness import ROOT,TrackedLua51,SOURCES,measure
from test_refactor_s6e import Profile,observed
from test_b262_capital_sidebar import ui


@contextmanager
def baseline():
 p=ROOT/'Mod/CapitalInvestment.lua';s=subprocess.check_output(['git','show','db42d26:Mod/CapitalInvestment.lua'],cwd=ROOT,text=True)
 read,execute=Path.read_text,TrackedLua51.execute;digest=sha256(s.encode()).hexdigest()
 def run(vm,text,*args,**kw):
  if sha256(text.encode()if isinstance(text,str)else text).hexdigest()==digest:SOURCES[digest]='historical/db42d26/Mod/CapitalInvestment.lua'
  return execute(vm,text,*args,**kw)
 with patch.object(Path,'read_text',lambda x,*a,**kw:s if x==p else read(x,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield


def detach(x):
 return {detach(k):detach(v)for k,v in x.items()}if lua_type(x)=='table'else x


def connected():
 g=observed();u=ui();u.execute('ContextPtr.input(inputEvent(2,27))')
 city_id,x,y=[g.eval('source:'+s+'()')for s in ('GetID','GetX','GetY')]
 u.execute("local id,x,y=...;c.GetID=function()return id end;c.GetX=function()return x end;c.GetY=function()return y end;Players[0].GetCities=function()return {FindID=function(_,n)if n==id then return c end end}end",city_id,x,y)
 def sync():
  b={name:detach(g.eval('cap.'+name))for name in ('views','revision','lastRequest')}
  u.globals().capBackend=u.table_from(b,recursive=True);u.execute('ExposedMembers.SPC_P0.CapitalInvestment=capBackend')
 def request(packet):
  g.globals().cap.Request(0,g.table_from(detach(packet)));sync()
 u.globals()._request=request;u.execute('onSend=function(p)_request(p)end');sync()
 u.execute('LuaEvents.SPC_CapitalOpen(0,...);Events.GameCoreEventPublishComplete.Fire();managers.CapitalDomain.items[1].Root.click();Events.GameCoreEventPublishComplete.Fire();managers.CapitalMode.items[1].Root.click()',city_id)
 return g,u,sync


class TreasuryOrdering(Profile,unittest.TestCase):
 def test_actual_late_event_counterexample_and_no_extra_quote_sources(self):
  rows=[]
  for old in (True,False):
   with baseline()if old else nullcontext():
    v=observed();v.execute("assert(C.confirm());local revision=C.view().revision;resetWork();Events.TreasuryChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire();sample={stale=C.view().quoteStale==true,balance=C.view().balance,revisionChanged=C.view().revision~=revision,nativeBalanceReads=work.balance,sourceReads=sourceWork(),depthReads=work.depth,money=moneyCalls}")
    rows.append(detach(v.globals().sample))
  self.assertTrue(rows[0]['stale']);self.assertFalse(rows[1]['stale']);self.assertEqual(rows[1]['balance'],1000.125*.75)
  self.assertEqual(rows[1]['nativeBalanceReads'],1);self.assertEqual(rows[1]['sourceReads'],0);self.assertEqual(rows[1]['depthReads'],0);self.assertEqual(rows[1]['money'],1)
  measure('S9e8_Capital_delayed_Treasury',{'baseline':'B380','before':rows[0],'after':rows[1],'native_order':'simulated independent delivery','native_CPU_or_heap_claim':False})
 def test_real_Capital_Store_and_separate_UI_remain_current_after_confirm(self):
  g,u,sync=connected();u.execute('assert(not Controls.Confirm.disabled);Controls.Confirm.click()');g.execute("Events.TreasuryChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(C.contract().stage=='ACTIVE'and moneyCalls==1 and not C.view().quoteStale)");sync()
  u.execute("Events.GameCoreEventPublishComplete.Fire();assert(not Controls.Balance.text:find('—')and not Controls.Current.text:find('报价已变化')and Controls.Current.text:find('执行中')and managers.CapitalDomain.items[1].Marker.text:find('INVESTING'));local n=#sent;Controls.Confirm.click();assert(#sent==n);managers.CapitalDomain.items[2].Root.click();Events.GameCoreEventPublishComplete.Fire();managers.CapitalMode.items[1].Root.click();assert(not Controls.Confirm.disabled)")
  g.execute('local n=T.writes();resetWork();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(T.writes()==n and work.balance==0 and sourceWork()==0 and moneyCalls==1)')
 def test_all_three_events_only_invalidate_views_with_a_different_balance(self):
  for event in ('TreasuryChanged','PlayerTreasuryChanged','PlayerGoldChanged'):
   v=observed();v.execute("event=...;assert(C.confirm());local revision=C.view().revision;Events[event].Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(not C.view().quoteStale and C.view().revision==revision and cap.views['0:'..other:GetID()].quoteStale and moneyCalls==1)",event)
 def test_real_balance_change_remains_stale_and_no_old_confirmation_debits(self):
  v=observed();v.execute("assert(C.confirm());balance=balance+10;Events.TreasuryChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(C.view().quoteStale);local p={Action='CAPITAL_CONFIRM',CityID=source:GetID(),Domain='DISTRICT_THEATER',Mode='VENTURE',Revision=C.view().revision,CityToken=C.view().token,Token='stale'};assert(not cap.Request(0,p)and moneyCalls==1 and rolls==0);assert(not C.view().quoteStale);assert(C.confirm('DISTRICT_THEATER','STABLE','fresh')and moneyCalls==2)")
 def test_matching_balance_does_not_clear_independent_or_reentrant_causes(self):
  v=observed();v.execute("cap.Mark(0,source:GetID());Events.TreasuryChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(C.view().quoteStale);assert(explicit());local read=shared.NetworkBridge.CurrentCapitalSources;local once=true;shared.NetworkBridge.CurrentCapitalSources=function(...)if once then once=false;cap.Mark(0,source:GetID());Events.TreasuryChanged.Fire(0)end;return read(...)end;assert(explicit());Events.GameCoreEventPublishComplete.Fire();assert(C.view().quoteStale and moneyCalls==0)")
 def test_unknown_Treasury_is_conservative_and_never_retries_on_idle(self):
  v=observed();v.execute("assert(C.confirm());local saved=T.encode(C.state());balanceReadFail=true;Events.TreasuryChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(C.view().quoteStale and T.encode(C.state())==saved);resetWork();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(work.balance==0 and sourceWork()==0 and moneyCalls==1);balanceReadFail=false;assert(explicit())")
 def test_reentrant_native_delivery_keeps_owner_fallback(self):
  v=observed();v.execute("local t=Players[0].GetTreasury;local once=true;Players[0].GetTreasury=function(...)if once then once=false;Events.TreasuryChanged.Fire(0)end;return t(...)end;Events.TreasuryChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(C.view().quoteStale and moneyCalls==0);Players[0].GetTreasury=t;assert(explicit())")
 def test_no_initial_view_keeps_existing_owner_discovery(self):
  import test_b241_capital as capital
  text=capital.SETUP;old='cap.Refresh(0,source:GetID());cap.Refresh(0,other:GetID())';self.assertEqual(text.count(old),1)
  with patch.object(capital,'SETUP',text.replace(old,'')):v=observed()
  v.execute("assert(next(cap.views)==nil);Events.TreasuryChanged.Fire(0);assert(work.balance==1);Events.GameCoreEventPublishComplete.Fire();assert(C.view().available and C.view().quoteStale and sourceWork()==0 and moneyCalls==0)")
 def test_foreign_and_idle_events_do_not_sample_local_treasury(self):
  v=observed();v.execute("resetWork();local revision=cap.revision;Events.TreasuryChanged.Fire(9);for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(work.balance==0 and sourceWork()==0 and cap.revision==revision and moneyCalls==0)")
 def test_event_during_native_debit_does_not_replay_and_final_fresh_read_wins(self):
  v=observed();v.execute("onMoney=function()Events.TreasuryChanged.Fire(0)end;assert(C.confirm());Events.PlayerTreasuryChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(not C.view().quoteStale and C.contract().stage=='ACTIVE'and moneyCalls==1);local n=T.writes();Events.PlayerGoldChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(T.writes()==n and moneyCalls==1)")

if __name__=='__main__':unittest.main()
