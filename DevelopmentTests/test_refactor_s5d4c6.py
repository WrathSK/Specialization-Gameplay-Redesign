"""Historical native surfaces, actual current Insights projection/kernel; history remains read-only."""
import ast
import unittest
from refactor_harness import Context,ROOT,legacy_source_observation,measure


def fixture(boot=True):
    # Only the historical native/metadata surface literal. No frozen assertions changed.
    path=ROOT/'DevelopmentTests/test_culture_insights_tourism.py';tree=ast.parse(path.read_text())
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='fixture')
    text=ast.literal_eval(next(n.value.args[0]for n in fn.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='execute'))
    c=Context()
    with legacy_source_observation():c.execute(text)
    c.globals().include=c.load
    # city is a factory; native methods belong to each instance.
    c.execute("""
    GameEvents=eventSource();Events.GameCoreEventPublishComplete=event();Events.BuildingRemovedFromMap=event();Game={GetCurrentGameTurn=function()return 1 end}
    P.Count=function(k)counts[k]=(counts[k]or 0)+1 end
    for _,v in ipairs({a,b,foreign})do v.GetBuildingLocation=function()return v.id end end
    Map={GetPlotIndex=function(x,y)return x end};CityManager={GetCityAt=function(x,y)for _,v in ipairs({a,b,foreign})do if v.id==x then return v end end end}
    P.RemoveBuilding=function(city,id)if failRemove then error('NATIVE_REMOVE_FAILED')end;city.present[id]=nil;removes=removes+1;Events.BuildingRemovedFromMap(city.id,8,id,city.owner)end
    P.CreateBuilding=function(city,id)creates=creates+1;if not failCreate then city.present[id]=true;city.pillaged[id]=nil end;GameEvents.BuildingPillageStateChanged.Fire(city.owner,city.id,id,false)end
    function pp()Events.GameCoreEventPublishComplete()end
    function loss(city,id)P.RemoveBuilding(city,id)end
    function encode(t)local out={};for k,v in pairs(t)do out[#out+1]=tostring(k)..'='..(type(v)=='table'and encode(v)or tostring(v))end;table.sort(out);return table.concat(out,';')end
    function history()return encode({a.records,b.records,foreign.records})end
    """)
    for module in ('NetworkInput','CurrentSpecializationFacts','CultureInsightsTourism'):c.load(module)
    c.execute("d=SPCCultureInsightsTourism.Start(P,shared);insight(a,'CIVILIZATION_A','PEOPLE');insight(b,'CIVILIZATION_B','WORKS')")
    if boot:c.execute('d.Audit();assert(a.present[1] and b.present[1])')
    return c


class InsightsHealth(unittest.TestCase):
    def test_exact_external_loss_only_target_city_history_identical(self):
        c=fixture();c.execute("local before=history();facts=0;loss(a,1);pp();assert(a.present[1] and b.present[1] and facts==1 and history()==before);local r,w=reads,creates+removes;for i=1,1000 do pp()end;assert(reads==r and creates+removes==w)")
        measure('S5d4c6_exact_history_projection',{'city_fact_reads':1,'permanent_history_writes':0,'thousand_idle_extra_reads':0})
    def test_live_pillage_repairs_existing_value_and_history_unchanged(self):
        c=fixture();c.execute("local before=history();a.pillaged[1]=true;GameEvents.BuildingPillageStateChanged.Fire(0,1,1,true);pp();assert(a.present[1] and not a.pillaged[1] and history()==before)")
    def test_other_city_loss_during_write_kept_next_snapshot(self):
        c=fixture();c.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(city,id)create(city,id);if once and city==a then once=false;loss(b,1)end end;loss(a,1);pp();assert(a.present[1] and not b.present[1]);pp();assert(b.present[1])")
    def test_damage_during_creation_not_hidden(self):
        c=fixture();c.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(city,id)create(city,id);if once and city==a then once=false;a.pillaged[id]=true;GameEvents.BuildingPillageStateChanged.Fire(0,1,id,true)end end;loss(a,1);pp();assert(a.pillaged[1]);pp();assert(a.present[1] and not a.pillaged[1])")
    def test_unknown_history_holds_current_then_new_health_recovers(self):
        c=fixture();c.execute("local before=history();historyError=true;GameEvents.BuildingPillageStateChanged.Fire(0,1,1,false);pp();assert(a.present[1] and d.errors['0:1']);historyError=false;local r,w=reads,creates+removes;for i=1,1000 do pp()end;assert(reads==r and creates+removes==w);loss(a,1);pp();assert(a.present[1] and not d.errors['0:1'] and history()==before)")
    def test_failed_native_create_requires_new_evidence(self):
        c=fixture();c.execute("local before=history();failCreate=true;loss(a,1);pp();assert(not a.present[1] and d.errors['0:1']);failCreate=false;local r,w=reads,creates+removes;for i=1,1000 do pp()end;assert(reads==r and creates+removes==w);GameEvents.BuildingPillageStateChanged.Fire(0,1,1,false);pp();assert(a.present[1] and history()==before and not d.errors['0:1'])")
    def test_foreign_and_unowned_health_zero_reads(self):
        c=fixture();c.execute("local r=reads;GameEvents.BuildingPillageStateChanged.Fire(3,3,1,true);GameEvents.BuildingPillageStateChanged.Fire(0,1,9999,true);pp();assert(reads==r)")
    def test_cold_cleanup_removes_foreign_saved_effect_without_history_changes(self):
        c=fixture(boot=False);c.execute("a.present[88]=true;foreign.present[12]=true;local before=history();Events.LoadScreenClose();assert(a.present[1] and not a.present[88] and not foreign.present[12] and history()==before);local r,w=reads,creates+removes;for i=1,1000 do pp()end;assert(reads==r and creates+removes==w)")
    def test_initialization_reentry_queues_without_repeat(self):
        c=fixture(boot=False);c.execute("a.present[88]=true;local remove=P.RemoveBuilding;local count=0;P.RemoveBuilding=function(city,id)if city==a and id==88 then count=count+1;assert(d.initializing and not d.Audit({player=0,city=2}))end;return remove(city,id)end;d.Audit();assert(d.ready and not d.initializing and count==1);pp();assert(a.present[1] and b.present[1] and count==1)")
    def test_new_reference_unknown_never_replays_old_effect(self):
        c=fixture();c.execute("local before=history();a.token='REPLACED';a.unknown=true;d.Audit({player=0,city=1});assert(not a.present[1] and d.errors['0:1'] and history()==before and b.present[1])")
    def test_confirmed_exit_return_preserves_history(self):
        c=fixture();c.execute("local before=history();a.owner=3;exits.CultureInsightsTourism(a,{confirmed=true,origin={owner=0}});assert(not a.present[1] and history()==before and not d.records['0:1']);a.owner=0;returns.CultureInsightsTourism(0,a);assert(a.present[1] and history()==before)")
    def test_max_exact192_and_unreadable_signature_do_not_guess_zero(self):
        c=fixture();c.execute("a.records={};for i=1,64 do for _,category in ipairs({'PEOPLE','WORKS','PLACES'})do insight(a,'CIVILIZATION_'..i,category)end end;d.Audit({player=0,city=1});assert(a.present[192] and not a.present[1]);a.unknown=true;GameEvents.BuildingPillageStateChanged.Fire(0,1,192,false);pp();assert(a.present[192] and d.errors['0:1'])")

if __name__=='__main__':unittest.main()
