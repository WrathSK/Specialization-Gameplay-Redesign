"""B187 actual-module arrival collection and controlled-name readback regressions.
No mocks establish native controlled-name survival or Spy engine implementation details.
"""
import unittest
from test_expedition_spy_task import gate

REPLACE = """
 local old=units[40];units[41]=unit(41,100,2,15,8)
 units[41].name=old.name;units[40]=nil;currentTurn=83
"""
class Binding(unittest.TestCase):
    def ready(self, window=False):
        l=gate(window=window)
        l.execute("req('CREATE','a');nativeDispatch('b');"+REPLACE)
        return l
    def test_collection_name_arrives_without_plot_membership(self):
        l=self.ready();l.execute("Units.GetUnitsInPlot=function()return {}end;ownTurn(2);local r=req('READ','r');assert(r.phase=='ARRIVED' and r.bound and r.unitID==41 and r.sourceCity==1 and r.identity.plotStatus=='ABSENT' and r.identity.lookupName=='MATCH' and properties==0 and destroys==0)")
    def test_plot_missing_or_throwing_is_diagnostic_only(self):
        for change in ['Units.GetUnitsInPlot=nil',"Units.GetUnitsInPlot=function()error('unreadable plot')end"]:
            with self.subTest(change=change):
                l=self.ready();l.execute(change+";ownTurn(2);local r=req('READ','r');assert(r.bound and r.phase=='ARRIVED' and r.identity.plotStatus=='UNREADABLE' and r.occupancyUnknown)")
    def test_name_failures_are_distinct_and_never_adopted(self):
        for change,status in [('units[41].name=nil','ABSENT'),('units[41].name="wrong"','MISMATCH'),('units[41].GetName=nil','UNREADABLE'),("units[41].GetName=function()error('unreadable name')end",'UNREADABLE')]:
            with self.subTest(status=status,change=change):
                l=self.ready();l.execute(change+f";local r=req('READ','r');assert(not r.bound and r.phase=='TRAVELLING' and r.identity.candidateName=='{status}' and r.identity.lookupName=='{status}' and r.sourceCity==1 and r.reservedCapacity);currentTurn=85;ownTurn(2);r=req('READ','s');assert(r.phase=='HELD' and not r.bound and properties==0 and destroys==0);req('CREATE','again');assert(initCalls==1);req('END','e',41);assert(destroys==1)")
    def test_exact_lookup_missing_wrong_id_owner_type_name_or_endpoint_holds(self):
        for change in ['return nil',"local u=unit(42,100,2,15,8);u.name=units[41].name;return u",'return unit(41,100,3,15,8)','return unit(41,103,2,15,8)','return unit(41,100,2,15,8)',"local u=unit(41,100,2,16,8);u.name=units[41].name;return u"]:
            with self.subTest(change=change):
                l=self.ready();l.execute("Players[2]:GetUnits().FindID=function(self,id)if id==41 then "+change+" end end;ownTurn(2);local r=req('READ','r');assert(r.phase=='HELD' and not r.bound and r.sourceCity==1 and r.identity and r.reservedCapacity and properties==0 and destroys==0)")
    def test_old_lookup_alias_does_not_override_exact_new_lookup(self):
        l=self.ready();l.execute("Players[2]:GetUnits().FindID=function(self,id)if id==40 or id==41 then return units[41]end end;Units.GetUnitsInPlot=function()return {}end;ownTurn(2);local r=req('READ','r');assert(r.bound and r.createdID==40 and r.trackedID==41 and r.identity.createdLookupID==41 and r.identity.createdName=='MATCH')")
    def test_throwing_old_lookup_keeps_candidate_and_source_diagnostics(self):
        l=self.ready();l.execute("units[41].name=nil;Players[2]:GetUnits().FindID=function(self,id)if id==40 then error('old ID unreadable')end;return units[id]end;local r=req('READ','r');assert(not r.snapshotUnknown and r.identity.createdName=='UNREADABLE' and r.identity.trackedName=='UNREADABLE' and r.identity.candidateName=='ABSENT' and r.identity.candidateID==41 and r.sourceCity==1 and not r.bound and r.reservedCapacity)")
    def test_old_lookup_getid_failure_is_reported_without_losing_source(self):
        l=self.ready();l.execute("units[41].name=nil;Players[2]:GetUnits().FindID=function(self,id)if id==40 then return {GetID=function()error('bad ID')end}end;return units[id]end;local r=req('READ','r');assert(not r.snapshotUnknown and r.identity.createdName=='UNREADABLE' and r.sourceCity==1 and r.reservedCapacity)")
    def test_new_lookup_failure_holds_but_report_survives(self):
        l=self.ready();l.execute("Players[2]:GetUnits().FindID=function(self,id)if id==41 then error('new ID unreadable')end end;ownTurn(2);local r=req('READ','r');assert(r.phase=='HELD' and not r.snapshotUnknown and not r.bound and r.identity.lookupName=='UNREADABLE' and r.identity.candidateName=='MATCH' and r.sourceCity==1)")
    def test_duplicate_name_or_old_prototype_reserves_capacity(self):
        for kind in ['UNIT_SPC_EXPEDITION_SPY','UNIT_SPC_EXPEDITION_GATE','UNIT_SPC_EXPEDITION_ZERO']:
            with self.subTest(kind=kind):
                l=self.ready();l.execute("info[102].UnitType='"+kind+"';units[42]=unit(42,102,2,15,8);units[42].name=units[41].name;ownTurn(2);local r=req('READ','r');assert(r.phase=='HELD' and r.stop=='TEAM_NAME_AMBIGUOUS' and r.identity.candidateName=='AMBIGUOUS' and r.count==2 and r.reservedCapacity and properties==0 and destroys==0)")
    def test_source_and_target_invalidity_never_adopts(self):
        for change in ['city.token=nil','city.token="replacement"','city.owner=3','targetCity.id=10','targetCity.owner=4','visible=false','met=false']:
            with self.subTest(change=change):
                l=self.ready();l.execute(change+";ownTurn(2);local r=req('READ','r');assert(r.phase=='HELD' and not r.bound and r.trackedID==40 and r.sourceCity==1 and properties==0 and destroys==0)")
    def test_read_scans_collection_once_and_pending_turn_once(self):
        l=gate();l.execute("req('CREATE','a');nativeDispatch('b');scans=0;local us=Players[2]:GetUnits();local old=us.Members;us.Members=function(self)scans=scans+1;return old(self)end;req('READ','r');assert(scans==1);scans=0;ownTurn(2);assert(scans==1);"+REPLACE+";scans=0;ownTurn(2);assert(scans==1);scans=0;ownTurn(2);assert(scans==0);req('READ','s');assert(scans==1)")
    def test_repeat_arrival_does_not_rewrite_name_or_complete_task(self):
        l=self.ready();l.execute("ownTurn(2);ownTurn(2);for i=1,5 do req('READ','r'..i)end;local r=req('READ','last');assert(r.bound and r.phase=='ARRIVED' and not r.taskCompletions and properties==0 and destroys==0 and placeCalls==0 and finishCalls==0 and nativeCalls==0)")
    def test_unbound_window_keeps_source_and_precise_name_states(self):
        l=gate(window=True);l.execute("gateOpen();Controls.CreateButton.click();Controls.ArmButton.click();"+REPLACE+";units[41].name=nil;Units.GetUnitsInPlot=function()return {}end;Controls.RefreshButton.click();local s=Controls.Report.text;assert(s:find('RETAINED_SOURCE') and s:find('IDENTITY_ABSENT') and s:find('IDENTITY_IDS:40,40,41,1',1,true) and s:find('IDENTITY_TURN:83,85',1,true));local n=sent;Controls.TaskButton.click();assert(sent==n and properties==0)")
    def test_cold_session_cannot_adopt_name_or_claim_source(self):
        l=self.ready();l.execute("SPCExpeditionSpyGate.Start(P,shared);local r=req('READ','r');assert(r.unbound and not r.bound and not r.sourceCity and not r.identity and r.count==1);req('CREATE','again');assert(initCalls==1 and properties==0)")

if __name__=='__main__':unittest.main()
