"""B248 delta: actual investment notification/access and read-only UI evidence.
No native training, rendering or restructuring acceptance is inferred.
"""
from pathlib import Path
import sqlite3
import subprocess
import unittest
import xml.etree.ElementTree as ET
from test_b247_restructuring import runtime, R
from test_b247_ui_package import ui
M=R/'Mod'


def investment(l):
    text=(M/'Gameplay.lua').read_text()
    a=text.index('local function refreshInvestmentSupport');b=text.index('\nlocal function request',a)
    l.execute(text[a:b].replace('local function refreshInvestmentSupport','function refreshInvestmentSupport',1))


class Access(unittest.TestCase):
    def test_actual_committed_investment_unlocks_without_turn_or_load(self):
        l=runtime(True);investment(l)
        l.execute("""
        late=Z.city(4,'DISTRICT_COMMERCIAL_HUB',3);Events.PlayerTurnActivated.Fire(0)
        assert(not late.markers.BUILDING_SPC_RESTRUCTURING_ACCESS)
        T.invest(late,88448);assert(T.control(late).active==4)
        assert(not late.markers.BUILDING_SPC_RESTRUCTURING_ACCESS)
        local reads=0;local read=shared.EffectiveFacts.Read
        shared.EffectiveFacts.Read=function(pid,c)assert(c==late);reads=reads+1;return read(pid,c)end
        refreshInvestmentSupport(0,{status='COMMITTED',city=late:GetID()})
        assert(late.markers.BUILDING_SPC_RESTRUCTURING_ACCESS and reads==1)
        """)
    def test_noncommitted_request_does_not_grant_access(self):
        l=runtime(True);investment(l)
        l.execute("""
        late=Z.city(4,'DISTRICT_COMMERCIAL_HUB',3);Events.PlayerTurnActivated.Fire(0)
        local reads=0;local read=shared.EffectiveFacts.Read
        shared.EffectiveFacts.Read=function(...)reads=reads+1;return read(...)end
        for _,s in ipairs({'PREPARED','FAILED','HELD'})do refreshInvestmentSupport(0,{status=s,city=late:GetID()})end
        assert(reads==0 and not late.markers.BUILDING_SPC_RESTRUCTURING_ACCESS)
        """)
    def test_duplicate_notification_has_no_marker_or_store_write(self):
        l=runtime(True);investment(l)
        l.execute("""
        local writes=T.writes();local create,remove=P.CreateBuilding,P.RemoveBuilding;local calls=0
        P.CreateBuilding=function(...)calls=calls+1;return create(...)end
        P.RemoveBuilding=function(...)calls=calls+1;return remove(...)end
        for i=1,3 do refreshInvestmentSupport(0,{status='COMMITTED',city=source:GetID()})end
        assert(calls==0 and T.writes()==writes)
        """)
    def test_governor_event_withdraws_and_restores_only_qualified_access(self):
        l=runtime(True)
        l.execute("T.governor(3);Events.GovernorChanged.Fire(0);assert(not source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS);T.governor(4);Events.GovernorChanged.Fire(0);assert(source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS and not c.markers.BUILDING_SPC_RESTRUCTURING_ACCESS)")
    def test_existing_four_load_rebuilds_missing_marker_without_turn(self):
        l=runtime(True)
        l.execute("source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS=nil;local w=T.writes();Events.LoadScreenClose.Fire();assert(source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS and T.writes()==w)")
    def test_failed_marker_readback_reports_without_false_success(self):
        l=runtime()
        l.execute("""
        traces={};SPCExpeditionTrainingDiagnostics={New=function()return {Record=function(stage,v)traces[#traces+1]={stage=stage,v=v}end}end}
        markerFail=true;Z.service();assert(svc.errors['0:'..source:GetID()]=='REST_MARKER_WRITE_UNCONFIRMED')
        for _,x in ipairs(traces)do assert(not(x.stage=='REST_ACCESS' and x.v.city==source:GetID() and x.v.markerPresent))end
        markerFail=false;svc.Refresh(0,source:GetID());assert(source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS)
        """)
    def test_does_not_read_wrong_player_or_before_load(self):
        l=runtime()
        l.execute("SPCRestructuring.Start(P,shared);svc=shared.Restructuring;local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function()error('UNEXPECTED_READ')end;svc.Refresh(3,source:GetID());svc.Refresh(0,source:GetID());assert(not source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS);shared.EffectiveFacts.Read=read;Events.LoadScreenClose.Fire();assert(source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS)")


def training_ui():
    l=ui()
    l.execute("""
    reads=0;writes=0;traces={};present=false;visible=false;allowed=false
    local row={UnitType='UNIT_SPC_RESTRUCTURING_TEAM',Index=5,Hash=155}
    GameInfo.Units.UNIT_SPC_RESTRUCTURING_TEAM=row
    GameInfo.Buildings={BUILDING_SPC_RESTRUCTURING_ACCESS={Index=6}}
    P={IsTestPlayer=function(pid)return pid==0 end}
    MilitaryFormationTypes={STANDARD_MILITARY_FORMATION=0};CityCommandResults={FAILURE_REASONS=22}
    ExposedMembers.SPC_P0={Restructuring={ready=true}}
    SPCExpeditionTrainingDiagnostics={New=function()return {Record=function(stage,v)traces[#traces+1]={stage=stage,v=v}end}end}
    local q={CanProduce=function(_,p,exclude,results)
      reads=reads+1;assert(p.UnitType==155 and p.MilitaryFormationType==0)
      if failRead then error('private path must not escape')end
      if exclude then return visible end
      return allowed,{[22]={'LOC_CANNOT_TRAIN_UNIT','private/path/forbidden'}}
    end,GetUnitCost=function()return 500 end}
    tc={GetOwner=function()return 0 end,GetID=function()return 77 end,
      GetBuildings=function()return {HasBuilding=function()return present end}end,GetBuildQueue=function()return q end}
    data={City=tc,UnitItems={}}
    """)
    return l


class TrainingEvidence(unittest.TestCase):
    def test_native_hidden_marker_and_reasons_are_observed_without_mutation(self):
        l=training_ui();l.execute("""
        SPCRestructuringUI.ObserveTraining(P,data);assert(#data.UnitItems==0 and #sent==0)
        local v=traces[1].v;assert(v.markerPresent==false and v.count==0 and v.readyToSelect==false and v.eligibility==false)
        assert(v.nativeCost==500 and v.nativeReason1=='LOC_CANNOT_TRAIN_UNIT' and v.nativeReason2=='REDACTED')
        SPCRestructuringUI.ObserveTraining(P,data);assert(reads==2 and #traces==1)
        """)
    def test_visible_and_disabled_are_distinct(self):
        l=training_ui();l.execute("""
        present=true;visible=true;data.UnitItems={{Type='UNIT_SPC_RESTRUCTURING_TEAM',Disabled=true}}
        SPCRestructuringUI.ObserveTraining(P,data);local v=traces[1].v
        assert(v.count==1 and v.paused and v.readyToSelect and not v.eligibility and v.markerPresent)
        allowed=true;data.UnitItems[1].Disabled=false;SPCRestructuringUI.ObserveTraining(P,data)
        assert(#traces==2 and traces[2].v.eligibility and not traces[2].v.paused and #sent==0)
        """)
    def test_missing_service_or_failed_reader_not_inferred_ready(self):
        l=training_ui();l.execute("ExposedMembers.SPC_P0.Restructuring=nil;failRead=true;SPCRestructuringUI.ObserveTraining(P,data);local v=traces[1].v;assert(not v.ready and v.guardStatus=='ABSENT' and v.readStatus=='FAILED' and v.reason=='REST_TRAINING_READ_FAILED' and #sent==0)")
    def test_other_owner_and_no_city_are_not_sampled(self):
        l=training_ui();l.execute("SPCRestructuringUI.ObserveTraining(P,{});tc.GetOwner=function()return 3 end;SPCRestructuringUI.ObserveTraining(P,data);assert(reads==0 and #traces==0 and #sent==0)")


class Package(unittest.TestCase):
    def test_art_dependency_and_investor_member_no_binaries(self):
        r=ET.parse(M/'Specialization.dep').getroot()
        self.assertIn('b248a322-3e2a-4a6a-830a-6b0d1f3435fc',[x.get('text')for x in r.findall('./RequiredGameArtIDs/Element/id')])
        r=ET.parse(M/'SpecializationP0.modinfo').getroot();self.assertEqual(r.get('version'),'275')
        self.assertIn('b248a322-3e2a-4a6a-830a-6b0d1f3435fc',[x.get('id')for x in r.findall('./Dependencies/Mod')])
        names=[x.text for x in r.findall('./Files/File')];self.assertEqual(len(names),len(set(names)))
        actual={str(p.relative_to(M))for p in M.rglob('*')if p.is_file() and p.name not in ('.DS_Store','SpecializationP0.modinfo')}
        self.assertEqual(set(names),actual)
        a=ET.parse(M/'ArtDefs/Units.artdef').getroot()
        team=next(e for c in a.findall('./m_RootCollections/Element')for e in c.findall('Element')if e.find('m_Name').get('text')=='UNIT_SPC_RESTRUCTURING_TEAM')
        refs=[x.get('text')for x in team.findall('.//m_ElementName')];self.assertIn('Leu_Investor',refs)
        self.assertFalse(any(x.startswith('Builder_') for x in refs))
    def test_other_unit_art_unchanged(self):
        before=ET.fromstring(subprocess.check_output(['git','show','834d4c2:Mod/ArtDefs/Units.artdef'],cwd=R))
        after=ET.parse(M/'ArtDefs/Units.artdef').getroot()
        def other(root):
            out={}
            for col in root.findall('m_RootCollections/Element'):
                for x in col.findall('Element'):
                    name=x.find('m_Name').get('text')
                    if name!='UNIT_SPC_RESTRUCTURING_TEAM':out[name]=ET.tostring(x)
            return out
        self.assertEqual(other(before),other(after))
    def test_icon_alias_preserves_all_investor_variants_not_gameplay(self):
        db=sqlite3.connect(':memory:')
        try:
            db.execute('CREATE TABLE IconDefinitions(Name TEXT PRIMARY KEY,Atlas TEXT,"Index" INTEGER)')
            expected={'':('FLAGS',0),'_WHITE':('FLAGS',0),'_PORTRAIT':('PORTRAITS',0),'_PORTRAIT_ASIAN':('PORTRAITS',4)}
            for suffix,(atlas,index)in expected.items():db.execute('INSERT INTO IconDefinitions VALUES(?,?,?)',('ICON_UNIT_LEU_INVESTOR'+suffix,atlas,index))
            sql=(M/'Data/Icons.sql').read_text();db.executescript(sql[sql.index('-- Reuse the installed Monopoly++'):])
            for suffix,val in expected.items():self.assertEqual(db.execute('SELECT Atlas,"Index" FROM IconDefinitions WHERE Name=?',('ICON_UNIT_SPC_RESTRUCTURING_TEAM'+suffix,)).fetchone(),val)
        finally:db.close()
        self.assertEqual((M/'Data/Restructuring.sql').read_bytes(),subprocess.check_output(['git','show','834d4c2:Mod/Data/Restructuring.sql'],cwd=R))
    def test_lua51_syntax_and_no_polling_or_probe_side_effect(self):
        from lupa.lua51 import LuaRuntime
        l=LuaRuntime(unpack_returned_tuples=True)
        for f in ['Gameplay.lua','Restructuring.lua','RestructuringUI.lua','UI/CrewProjectOrder.lua','Probe.lua']:
            s=(M/f).read_text();l.execute('assert(loadstring(...))',s)
        for f in ['Restructuring.lua','RestructuringUI.lua']:
            s=(M/f).read_text()
            for t in ['SetUpdate(',"'SystemUpdateUI'",'Automation.GetTime','os.clock','collectgarbage(']:self.assertNotIn(t,s)
        body=(M/'RestructuringUI.lua').read_text().split('function M.ObserveTraining',1)[1]
        for t in ['RequestPlayerOperation','SetProperty','CreateBuilding','ChangeYield','RequestCommand']:self.assertNotIn(t,body)

if __name__=='__main__':unittest.main()
