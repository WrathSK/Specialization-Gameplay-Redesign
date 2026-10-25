"""S7a3 D4-supported state vs frozen extra-tolerance tests; no native immunity claim."""
from contextlib import contextmanager
from pathlib import Path
import sqlite3
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import ROOT,legacy_source_observation,measure
from project_paths import external_database
from test_refactor_s5d4c1 import actual,actual_cross
import test_refactor_s5d4c1 as health_cases
import test_refactor_s5d4c2 as infrastructure_cases
from refactor_harness import TrackedLua51,SOURCES
from hashlib import sha256


FILES=('ResearchApply','ResearchInfrastructure','ResearchChair','ResearchCross')
@contextmanager
def historical_source():
    previous=Path.read_text
    originals={ROOT/'Mod'/(name+'.lua'):subprocess.check_output(['git','show','a4226d4:Mod/'+name+'.lua'],cwd=ROOT,text=True)for name in FILES}
    def read(path,*a,**kw):
        if path in originals:return originals[path]
        return previous(path,*a,**kw)
    execute=TrackedLua51.execute
    history={sha256(text.encode()).hexdigest():'historical/a4226d4/'+str(path.relative_to(ROOT))for path,text in originals.items()}
    def historical_execute(vm,source,*a,**kw):
        digest=sha256(source.encode()).hexdigest()if isinstance(source,str)else None
        if digest in history:SOURCES[digest]=history[digest]
        return execute(vm,source,*a,**kw)
    with patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',historical_execute):
        with legacy_source_observation():yield


class FrozenArtificialDamage(unittest.TestCase):
    def test_precleanup_artificial_carrier_damage_expectations_unchanged_at_B316(self):
        names=['test_live_pillage_repairs_without_dead_events_and_does_not_rearm_self','test_confirmed_damage_during_creation_is_not_suppressed','test_actual_cross_pillage_repairs_through_exact_health','test_actual_cross_UNKNOWN_holds_then_reliable_sample_recovers']
        with historical_source():
            case=health_cases.ResearchHealth()
            for name in names:getattr(case,name)()
            infrastructure_cases.InfrastructureHealth().test_exact_loss_and_pillage_keep_existing_repair_policy()
        measure('S7a3_frozen_artificial_damage',{'source':'a4226d4','unchanged_assertions':names+['test_refactor_s5d4c2.InfrastructureHealth.test_exact_loss_and_pillage_keep_existing_repair_policy'],'current_classification':'SUPERSEDED_FOR_UNSUPPORTED_CARRIER_DAMAGE','reason':'D4 no-pillage current-version new campaign; original frozen evidence remains'})


class CurrentD4(unittest.TestCase):
    def test_forced_unsupported_damage_is_not_rebuilt_or_presented_as_actual_yield(self):
        l=actual();l.execute("local id=chairID(0);cities[1].damage[id]=true;local w=writes;fire('GameEvents.BuildingPillageStateChanged',0,1,id,true);pp();assert(cities[1].damage[id] and writes==w);local text=chair.Describe(0,cities[1],true);assert(text:find('配置%+2'));for i=1,1000 do pp()end;assert(writes==w)")
        l=actual_cross();l.execute("local id=crossID(0);cities[1].damage[id]=true;local w=writes;fire('GameEvents.BuildingPillageStateChanged',0,1,id,true);fire('GameCoreEventPublishComplete');assert(cities[1].damage[id]and writes==w);for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(writes==w)")
    def test_infrastructure_external_loss_and_cross_UNKNOWN_missing_restore_still_work(self):
        l=actual();l.execute("infra=shared.ResearchInfrastructure;infra.Audit({player=0,city=1});local k=GameInfo.Buildings.BUILDING_SPC_RESEARCH_INFRA_0.Index;assert(cities[1].carriers[k]);local cap=counters.dc_capture;external(cities[1],k);pp();assert(cities[1].carriers[k]and counters.dc_capture==cap and not infra.errors[0][1])")
        l=actual_cross();l.execute("local id=crossID(0);d.samples[0]=nil;externalCross(0);local w=writes;fire('GameCoreEventPublishComplete');assert(writes==w and not cities[1].built[id]and d.errors[0][1]);for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(writes==w);districts[13].base=7;fire('FeatureAddedToMap');pulse();assert(cities[1].built[id]and not d.errors[0][1])")

    def test_each_diff_only_removes_own_carrier_rebuild_predicate(self):
        replacements={'ResearchApply':('not v.want or v.plot~=p.plot or v.pillaged','not v.want or v.plot~=p.plot'),'ResearchInfrastructure':('not wanted or r.plot~=p.plot or r.pillaged','not wanted or r.plot~=p.plot'),'ResearchChair':('not r.want or r.plot~=p.plot or r.pillaged','not r.want or r.plot~=p.plot'),'ResearchCross':('not r.want or r.pillaged','not r.want')}
        for name,(before,after)in replacements.items():
            original=subprocess.check_output(['git','show','a4226d4:Mod/'+name+'.lua'],cwd=ROOT,text=True)
            self.assertEqual(original.count(before),1)
            self.assertEqual(original.replace(before,after,1),(ROOT/'Mod'/(name+'.lua')).read_text())
    def test_real_anchor_and_ordinary_building_pillage_still_withdraws_then_recovers(self):
        l=actual();l.execute("local c=cities[1];local campus=c.ds[1];local was=campus.pillaged;campus.pillaged=true;shared.DistrictCompleteness.MarkDirty(0,1);shared.ResearchInfrastructure.Audit({player=0,city=1});shared.ResearchApply.Audit({player=0,city=1});shared.ResearchChair.Audit({player=0,city=1});assert(cc('BUILDING_LIBRARY')==0);campus.pillaged=was;shared.DistrictCompleteness.MarkDirty(0,1);shared.ResearchChair.Audit({player=0,city=1});assert(cc('BUILDING_LIBRARY')==3)")
    def test_actual_configuration_sql_preserves_non_spc_and_covers_four_families(self):
        source=sqlite3.connect(external_database(ROOT).as_uri()+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');source.backup(db);source.close()
        before=list(db.execute("SELECT * FROM Buildings_XP2 WHERE substr(BuildingType,1,13)<>'BUILDING_SPC_' ORDER BY BuildingType"))
        db.executescript((ROOT/'Mod/Data/InternalCarrierPillage.sql').read_text())
        measured={}
        for family in ('APPLY','INFRA','CHAIR','CROSS'):
            rows=list(db.execute("SELECT b.BuildingType,b.InternalOnly,x.Pillage FROM Buildings b LEFT JOIN Buildings_XP2 x ON x.BuildingType=b.BuildingType WHERE b.BuildingType LIKE ?",('BUILDING_SPC_RESEARCH_'+family+'_%',)))
            self.assertGreater(len(rows),0);self.assertTrue(all(internal==1 and pillage==0 for _,internal,pillage in rows));measured[family]=len(rows)
        self.assertEqual(before,list(db.execute("SELECT * FROM Buildings_XP2 WHERE substr(BuildingType,1,13)<>'BUILDING_SPC_' ORDER BY BuildingType")));db.close()
        measure('S7a3_D4_copied_engine_configuration',{'family_rows':measured,'all_InternalOnly_Pillage0':True,'non_SPC_unchanged':True,'native_immunity':'USER_GAME_TEST_REQUIRED'})


if __name__=='__main__':unittest.main()
