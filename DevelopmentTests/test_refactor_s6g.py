"""S6g actual Bridge/CN scalar discovery, independent of native effect policies."""
import unittest
from refactor_harness import measure
from test_refactor_s4b import culture
from test_refactor_s6d import get_index


def fixture(large=False):
    l=culture()
    if large:
        l.execute("""
        function addCity(id,kind)
         local c={id=id,owner=0,token='CITY'..id,kind=kind,active=4,potential=4}
         function c:GetID()return self.id end;function c:GetOwner()return self.owner end
         function c:GetX()return self.id end;function c:GetY()return 10 end
         function c:GetProperty(k)if k=='SPC_DEV_BINDING_B013_TOKEN'then return self.token end end
         function c:GetName()return 'C'..self.id end
         equip(c);local buildings=c.GetBuildings
         function c:GetBuildings()local b=buildings(self);b.city=self;return b end
         cities[id]=c
        end
        addCity(6,'COMMERCE');addCity(7,'CULTURE')
        for id=8,37 do addCity(id,'RESEARCH')end
        local routes={'0,4,0,2,10','0,2,0,1,11','0,2,0,5,12','0,7,0,6,13'}
        for id=8,37 do local unit=id+20;units[unit]={};routes[#routes+1]='0,6,0,'..id..','..unit end
        complete(7,1);send(table.concat(routes,';'),#routes);complete(4,1);cn.SourceChanged(0,4)
        assert(amount(cities[1])==1 and amount(cities[8])==1 and amount(cities[37])==1)
        """)
    l.execute("""
      function up(fn,name)for i=1,100 do local k,v=debug.getupvalue(fn,i);if not k then return end;if k==name then return v end end end
      local currentCulture=net.CurrentCultureBatch
      function privateView()return assert(up(up(currentCulture,'currentView'),'views'))[0]end
      function watch()
       local v=privateView();local graph=v.recipients.CULTURE or {};local tables={[cn.records]='records',[graph]='graph'}
       for _,row in pairs(graph)do tables[row]='edges'end
       work={records=0,graph=0,edges=0};local original=pairs
       pairs=function(t)local iter,state,key=original(t);local kind=tables[t]
        return function(st,k)local a,b=iter(st,k);if a~=nil and kind then work[kind]=work[kind]+1 end;return a,b end,state,key
       end
       unwatch=function()pairs=original end
      end
      function state()local out={};for id=1,37 do if cities[id]then out[#out+1]=id..':'..amount(cities[id])end end;return table.concat(out,';')end
    """)
    return l


class ScopedTopology(unittest.TestCase):
    def test_real_full_and_scoped_batch_equal_per_selected_receiver_and_detached(self):
        l=fixture();l.execute("local full=net.CurrentCultureBatch(0);local v=net.CurrentCultureBatch(0,{sources={[4]=true},targets={[4]=true}});assert(v.scoped and v.candidates[1]and v.candidates[2]and v.candidates[5]);for cid,row in pairs(v.recipients)do for sid in pairs(full.recipients[cid])do assert(row[sid])end end;v.recipients[1][4]=nil;v.candidates[1]=nil;v.input.validity='BAD';local next=net.CurrentCultureBatch(0,{sources={[4]=true},targets={}});assert(next.recipients[1][4]and next.candidates[1]and net.Input(0).validity=='VERIFIED')")

    def test_multiple_sources_mixed_history_retains_unchanged_source(self):
        l=fixture();l.execute("cities[3].kind='CULTURE';cities[3].potential=4;cities[3].active=4;complete(3,1);complete(4,2);send('0,4,0,2,10;0,3,0,2,11;0,2,0,1,12',3);cities[4].historyUnknown=true;complete(3,3);cn.SourceChanged(0,3);assert(amount(cities[1])==3 and cn.records['0:1'].sources[4]and cn.records['0:1'].provenance[4].status=='RETAINED')")

    def test_real_new_receiver_disconnect_reconnect_and_second_history_change(self):
        l=fixture();l.execute("complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[5])==1);send('0,4,0,2,10;0,2,0,3,11',2);cn.SourceChanged(0,4);assert(amount(cities[5])==0 and cn.records['0:3']);cities[3].kind='RESEARCH';cities[3].potential=1;cities[3].active=1;net.Refresh(0);cn.SourceChanged(0,4);assert(amount(cities[3])==1);complete(4,2);cn.SourceChanged(0,4);assert(amount(cities[3])==2);send('0,4,0,2,10;0,2,0,5,11',2);cn.SourceChanged(0,4);assert(amount(cities[3])==0 and amount(cities[5])==2)")

    def test_old_api_missing_scope_marker_uses_full_fallback(self):
        l=fixture();l.execute("local read=net.CurrentCultureBatch;net.CurrentCultureBatch=function(pid)return read(pid)end;complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1);watch();cn.SourceChanged(0,4);unwatch();assert(work.records>0 and work.graph>0)")

    def test_private_index_capacity_failure_keeps_valid_topology_and_falls_back(self):
        l=fixture();l.execute("local idx=privateView().cultureIndex;assert(not idx.Replace(0,1,{bad=true}));local v=net.CurrentCultureBatch(0,{sources={[4]=true},targets={}});assert(not v.scoped and v.recipients[1][4]and v.input.validity=='VERIFIED');complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1 and not cn.error)")

    def test_capacity_limited_new_view_does_not_poison_acceptance(self):
        l=fixture();l.execute("local factory=SPCReverseDependencies.New;SPCReverseDependencies.New=function()return factory(1,1)end;cities[4].active=3;net.Refresh(0);SPCReverseDependencies.New=factory;assert(net.Input(0).validity=='VERIFIED');local v=net.CurrentCultureBatch(0,{sources={[4]=true},targets={}});assert(not v.scoped and v.recipients[1][4]);complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==0 and not cn.error)")

    def test_consumer_index_unavailable_uses_original_fallback(self):
        l=fixture();get_index(l,'cn');l.execute("assert(not idx.Replace(0,1,{bad=true}));watch();complete(4,1);cn.SourceChanged(0,4);unwatch();assert(amount(cities[1])==1 and work.records>0 and work.graph>0 and not cn.error)")

    def test_empty_and_false_changed_have_no_discovery_or_fact_work(self):
        for changed in ('{}','{[4]=false}'):
            l=fixture();l.execute("watch();factReads={};cn.Audit({player=0,changed="+changed+"});unwatch();assert(not next(factReads)and work.records==0 and work.graph==0 and work.edges==0)")

    def test_view_replacement_isolation_and_recovery_never_reuse_old_edges(self):
        l=fixture();l.execute("complete(4,1);cn.SourceChanged(0,4);for i=1,12 do send('',0);assert(not net.CurrentCultureBatch(0,{sources={[4]=true},targets={}}).candidates[1]);send('0,4,0,2,10;0,2,0,1,11',2);assert(net.CurrentCultureBatch(0,{sources={[4]=true},targets={}}).candidates[1]);cn.SourceChanged(0,4);assert(amount(cities[1])==1)end;net.CheckEvidence(false);local n=created+removed;cn.SourceChanged(0,4);assert(amount(cities[1])==1 and created+removed==n);send('0,4,0,2,10;0,2,0,1,11',2);cn.SourceChanged(0,4);assert(amount(cities[1])==1)")

    def test_two_components_reduce_scalar_discovery_with_identical_effects(self):
        results={};states={}
        for mode in ('full','scoped'):
            l=fixture(True)
            if mode=='full':l.execute("local read=net.CurrentCultureBatch;net.CurrentCultureBatch=function(pid)return read(pid)end")
            l.execute("watch();complete(4,2);cn.SourceChanged(0,4);unwatch();assert(amount(cities[1])==2 and amount(cities[8])==1 and amount(cities[37])==1)")
            results[mode]={k:l.globals().work[k]for k in ('records','graph','edges')};states[mode]=l.globals().state()
        self.assertEqual(states['full'],states['scoped'])
        self.assertGreater(results['full']['records'],30);self.assertEqual(results['scoped']['records'],0)
        self.assertGreater(results['full']['graph'],30);self.assertEqual(results['scoped']['graph'],0)
        self.assertLess(results['scoped']['edges'],results['full']['edges'])
        measure('S6g_Culture_scalar_discovery',{'cities':37,'components':2,'before':results['full'],'after':results['scoped'],'same_effects':True,'remaining':'new topology O(E) index build; Input full provenance copy unchanged; no CPU/native heap claim'})


if __name__=='__main__':unittest.main()
