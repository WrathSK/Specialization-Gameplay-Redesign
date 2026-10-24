"""S6d detached reverse edges; actual CN/Std commit and fallback contracts."""
import unittest
from refactor_harness import Context, measure
from test_refactor_s4b import culture, standard


def index():
    c=Context();c.load('ReverseDependencies');c.execute('d=SPCReverseDependencies.New()');return c


def get_index(l,name):
    l.execute("""
    function up(fn,name)for i=1,100 do local k,v=debug.getupvalue(fn,i);if not k then return end;if k==name then return v end end end
    """)
    l.execute('idx=assert(up('+name+".Audit,'dependents'))")


class Relations(unittest.TestCase):
    def test_false_values_membership_replacement_and_detached_returns(self):
        c=index();c.execute("local v={[1]=false,[2]={status='UNKNOWN'}};assert(d.Replace(0,10,v));v[1]=nil;local out=d.Dependents(0,1);assert(out[10]);out[10]=nil;assert(d.Dependents(0,1)[10]);d.Replace(0,10,{[2]=false,[3]=true});assert(not next(d.Dependents(0,1))and d.Dependents(0,2)[10]and d.Dependents(0,3)[10]);assert(d.Stats().targets==1 and d.Stats().edges==2)")
    def test_owner_isolation_remove_and_empty_sources(self):
        c=index();c.execute("d.Replace(0,10,{[1]=true});d.Replace(1,10,{[2]=true});d.Remove(0,10);d.Remove(0,10);assert(not next(d.Dependents(0,1))and d.Dependents(1,2)[10]);d.Replace(1,10,{});assert(d.Stats().targets==0 and d.Stats().edges==0)")
    def test_target_capacity_preserves_old_graph_and_latches_explicit_unavailable(self):
        c=index();c.execute("d=SPCReverseDependencies.New(1,4);assert(d.Replace(0,10,{[1]=false}));local ok,why=d.Replace(0,11,{[2]=true});assert(not ok and why=='DEPENDENCY_INDEX_CAPACITY');assert(d.Stats().targets==1 and d.Stats().edges==1);local v,e=d.Dependents(0,1);assert(v==nil and e==why);d.Remove(0,10);assert(d.Stats().targets==0 and d.Dependents(0,1)==nil)")
    def test_edge_capacity_or_invalid_input_never_partially_replace(self):
        for sources in ('{[2]=true,[3]=true,[4]=true}','{bad=true}','setmetatable({[1]=true},{})'):
            c=index();c.execute("d=SPCReverseDependencies.New(3,2);d.Replace(0,10,{[1]=true});assert(not d.Replace(0,10,"+sources+"));assert(d.Stats().targets==1 and d.Stats().edges==1 and d.Dependents(0,1)==nil)")
    def test_large_warm_lookup_visits_only_detached_dependency_set(self):
        c=index();c.execute("for i=1,2048 do assert(d.Replace(0,i,{[i]=true}))end;local v=d.Dependents(0,100);assert(v[100]);local n=0;for _ in pairs(v)do n=n+1 end;assert(n==1 and d.Stats().targets==2048 and d.Stats().edges==2048)")
        measure('S6d_reverse_index_bound',{'targets':2048,'edges':2048,'single_source_returned_targets':1,'native_reads':0,'timers':0,'capacity_failure':'UNAVAILABLE; original consumer scan fallback until new context'})


class Consumers(unittest.TestCase):
    def test_actual_CN_index_contains_all_sources_not_only_contributors(self):
        l=culture();get_index(l,'cn');l.execute("complete(4,1);cn.SourceChanged(0,4);for _,r in pairs(cn.records)do for sid in pairs(r.sources)do assert(idx.Dependents(r.owner,sid)[r.id])end end;net.CheckEvidence(false);cn.SourceChanged(0,4);assert(idx.Dependents(0,4)[1]and cn.records['0:1'].provenance[4].status=='RETAINED')")
    def test_actual_CN_old_dependency_disconnect_and_new_receiver(self):
        l=culture();get_index(l,'cn');l.execute("complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1);local view=net.CurrentCultureBatch(0);view.recipients[1]={};net.CurrentCultureBatch=function()return view end;cn.SourceChanged(0,4);assert(amount(cities[1])==0 and not idx.Dependents(0,4)[1]);view.recipients[1]={[4]=true};cn.SourceChanged(0,4);assert(amount(cities[1])==1 and idx.Dependents(0,4)[1])")
    def test_actual_CN_failure_and_reference_cleanup_keep_index_consistent(self):
        l=culture();get_index(l,'cn');l.execute("complete(4,1);cn.SourceChanged(0,4);assert(idx.Dependents(0,4)[1]);cities[4].historyUnknown=true;cn.SourceChanged(0,4);assert(idx.Dependents(0,4)[1]);cities[1].token='NEW';readFail=true;cn.Audit({player=0,city=1});assert(cn.records['0:1']==nil and not idx.Dependents(0,4)[1])")
    def test_actual_Std_empty_or_unknown_source_is_indexed_and_second_change_updates(self):
        l=standard();get_index(l,'std');l.execute("for _,r in pairs(std.records)do for sid in pairs(r.sources)do assert(idx.Dependents(r.owner,sid)[r.city])end end;knowledge[5]=false;std.SourceChanged(0,5);assert(idx.Dependents(0,5)[1]);knowledge[5]={learned={},districts={learned={}}};std.SourceChanged(0,5);assert(idx.Dependents(0,5)[1]);learn(5);studies[5]=2;std.SourceChanged(0,5);assert(stdValue(1)==14)")
    def test_actual_Std_old_edge_disconnect_and_new_topology_source(self):
        l=standard();get_index(l,'std');l.execute("local view=net.CurrentIndustryBatch(0);view.recipients[1]={[3]=true};net.CurrentIndustryBatch=function()return view end;std.SourceChanged(0,5);assert(stdValue(1)==12 and not idx.Dependents(0,5)[1]);view.recipients[1][5]=true;std.SourceChanged(0,5);assert(stdValue(1)==14 and idx.Dependents(0,5)[1])")
    def test_actual_Std_cold_exception_A_and_unrecorded_city_not_skipped(self):
        l=standard(False,True);get_index(l,'std');l.execute("cities[3].active=2;knowledge[5]=false;send('0,5,0,2,10;0,3,0,2,11;0,2,0,1,12',3);assert(stdValue(1)==14 and std.records['0:1'].loaded);assert(idx.Dependents(0,5)[1]);knowledge[5]={learned={},districts={learned={}}};std.SourceChanged(0,5);assert(stdValue(1)==0 and not std.records['0:1'].loaded);std.records['0:1']=nil;idx.Remove(0,1);std.SourceChanged(0,3);assert(std.records['0:1'])")
    def test_actual_index_failure_falls_back_without_business_failure(self):
        for make,name in ((culture,'cn'),(standard,'std')):
            l=make();get_index(l,name)
            if name=='cn':
                l.execute("complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1);assert(not idx.Replace(0,1,{bad=true}));cities[4].active=3;cn.SourceChanged(0,4);assert(amount(cities[1])==0 and not cn.error and cn.dependencyIndexError=='DEPENDENCY_INDEX_SOURCE')")
            else:
                l.execute("assert(not idx.Replace(0,1,{bad=true}));cities[5].active=2;std.SourceChanged(0,5);assert(stdValue(1)==12 and not std.error and std.dependencyIndexError=='DEPENDENCY_INDEX_SOURCE')")
    def test_failed_reference_clear_keeps_old_CN_edges_until_actual_clear(self):
        l=culture();get_index(l,'cn');l.execute("complete(4,1);cn.SourceChanged(0,4);cities[1].token='NEW';removeFail=true;cn.Audit({player=0,city=1});assert(cn.records['0:1']and idx.Dependents(0,4)[1]);removeFail=false;readFail=true;cn.Audit({player=0,city=1});assert(cn.records['0:1']==nil and not idx.Dependents(0,4)[1])")
    def test_Std_write_failure_preserves_old_edge_for_later_new_cause(self):
        l=standard();get_index(l,'std');l.execute("local view=net.CurrentIndustryBatch(0);view.recipients[1]={[3]=true};net.CurrentIndustryBatch=function()return view end;createFail=true;std.SourceChanged(0,5);assert(std.errors['0:1']and idx.Dependents(0,5)[1]);createFail=false;std.SourceChanged(0,5);assert(stdValue(1)==12 and not idx.Dependents(0,5)[1])")
    def test_false_changed_member_does_not_expand_existing_scope(self):
        l=culture();l.execute("factReads={};cn.Audit({player=0,changed={[1]=false}});assert(not factReads[1])")

if __name__=='__main__':unittest.main()
