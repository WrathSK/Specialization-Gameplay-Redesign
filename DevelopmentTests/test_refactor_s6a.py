"""S6a D working-set/report separation; current Lua5.1 native doubles, no engine PASS."""
import unittest
from unittest.mock import patch
from refactor_harness import Context,measure
from refactor_fixtures import depth_context


class Cache(unittest.TestCase):
    def test_business_boundary_2047_2048_2049_preserves_warm_set(self):
        rows=[]
        for n in (2047,2048,2049):
            c=depth_context(n);c.execute('for i=1,... do sample(i)end;resetCounts();for i=1,... do sample(i)end',n,n)
            rows.append({'cities':n,'warm_captures':c.eval('counts.dc_capture or 0'),'business':c.eval('shared.DistrictCompleteness.BusinessCacheSize()'),'reports':c.eval('shared.DistrictCompleteness.CacheSize()')})
        self.assertEqual([r['warm_captures']for r in rows],[0,0,1])
        self.assertEqual([r['business']for r in rows],[2047,2048,2048])
        self.assertTrue(all(r['reports']==8 for r in rows))
        measure('S6a_business_capacity',rows)

    def test_detail_rotation_does_not_evict_compact_and_only_miss_recaptures(self):
        c=depth_context(32);c.execute('''
        for i=1,32 do sample(i)end;resetCounts()
        for i=1,32 do assert(sample(i,true).value.excluded)end
        assert(counts.dc_capture==32 and shared.DistrictCompleteness.CacheSize()==8)
        resetCounts();for i=1,32 do assert(sample(i).availability=='READY')end
        assert(not counts.dc_capture and shared.DistrictCompleteness.BusinessCacheSize()==32)
        local revision=sample(1).revision;resetCounts();local d=sample(1,true)
        assert(counts.dc_capture==1 and d.revision==revision);sample(2);assert(counts.dc_capture==1)
        d.value.districts[1].buildings[1].tier=99;assert(sample(1).value.districts[1].buildings[1].tier==1)
        ''')
        measure('S6a_32_report_rotation',{'report_recaptures':32,'later_business_recaptures':0,'detail_capacity':8})

    def test_raw_still_present_compact_to_detail_keeps_existing_zero_recapture_contract(self):
        c=depth_context(8);c.execute('for i=1,8 do sample(i)end;resetCounts();for i=1,8 do local d=sample(i,true);assert(d.value.excluded)end;assert(not counts.dc_capture and not counts.building_check)')

    def test_report_miss_failure_holds_business_without_fabricating_detail_or_idle_retry(self):
        c=depth_context(9);c.execute('''
        for i=1,9 do sample(i)end
        local get=cities[1].GetBuildings;cities[1].GetBuildings=function()error('RAW_UNAVAILABLE')end
        local d=sample(1,true);assert(d.availability=='TEMPORARILY_UNAVAILABLE'and d.value==nil)
        local b=sample(1);assert(b.value.domains.DISTRICT_CAMPUS.value==1 and b.availability=='TEMPORARILY_UNAVAILABLE')
        local n=counts.dc_capture;for i=1,1000 do sample(1,true);sample(1)end;assert(counts.dc_capture==n)
        cities[1].GetBuildings=get;shared.DistrictCompleteness.MarkDirty(0,1)
        assert(sample(1,true).availability=='READY'and sample(1).value.domains.DISTRICT_CAMPUS.value==1)
        ''')

    def test_same_D_revision_new_sample_refreshes_queued_report_observation(self):
        c=depth_context();c.execute('''
        local first=sample(1,true);assert(#first.value.excluded==0)
        local info=P.Info;P.Info=function(tab,index)if tab=='Buildings'and index==2 then return {Index=2,BuildingType='BUILDING_TEST_2'}end;return info(tab,index)end
        cities[1].GetBuildQueue=function()return {CurrentlyBuilding=function()return 2 end}end
        shared.DistrictCompleteness.MarkDirty(0,1);local second=sample(1,true)
        assert(second.revision==first.revision and #second.value.excluded==1 and second.value.excluded[1].reason=='UNDER_CONSTRUCTION')
        ''')

    def test_dirty_scopes_reach_business_entries_whose_raw_has_been_evicted(self):
        c=depth_context(32);c.execute('''
        for i=1,32 do sample(i)end;resetCounts();local d=shared.DistrictCompleteness
        d.MarkDirty(1,1);for i=1,32 do sample(i)end;assert(not counts.dc_capture)
        d.MarkDirty(0,1);sample(2);assert(not counts.dc_capture);sample(1);assert(counts.dc_capture==1)
        d.MarkDirty(0);for i=1,32 do sample(i)end;assert(counts.dc_capture==33)
        d.MarkDirty();for i=1,32 do sample(i)end;assert(counts.dc_capture==65)
        ''')

    def test_overflow_dirty_during_capture_cannot_certify_old_sample(self):
        c=depth_context(2049);c.execute('''
        for i=1,2048 do sample(i)end
        local get=cities[2049].GetBuildings;local once=true
        cities[2049].GetBuildings=function()if once then once=false;shared.DistrictCompleteness.MarkDirty(0,2049)end;return get()end
        local d=sample(2049);assert(d.validity=='UNKNOWN'and d.error=='DC_CHANGED_DURING_CAPTURE')
        assert(sample(2049).availability=='READY'and shared.DistrictCompleteness.BusinessCacheSize()==2048)
        resetCounts();for i=1,2048 do sample(i)end;assert(not counts.dc_capture)
        ''')

    def test_load_during_capture_rejects_detached_entry_and_resets_both_layers(self):
        c=depth_context();c.execute('''
        sample(2);local get=cities[1].GetBuildings;local once=true
        cities[1].GetBuildings=function()if once then once=false;Events.LoadScreenClose.Fire()end;return get()end
        local a=sample(1);assert(a.availability=='TEMPORARILY_UNAVAILABLE'and a.validity=='UNKNOWN')
        assert(shared.DistrictCompleteness.BusinessCacheSize()==0 and shared.DistrictCompleteness.CacheSize()==0)
        local b=sample(1);assert(b.availability=='READY'and b.epoch>a.epoch-1)
        assert(shared.DistrictCompleteness.BusinessCacheSize()==1)
        ''')

    def test_reference_replacement_during_capture_does_not_publish_detached_entry(self):
        c=depth_context();c.execute('''
        local get=cities[1].GetBuildings;local once=true
        cities[1].GetBuildings=function()
         if once then once=false;cities[1].token='NEW_REFERENCE';assert(sample(1).availability=='READY')end
         return get()
        end
        local old=sample(1);assert(old.validity=='UNKNOWN'and old.error=='DC_CHANGED_DURING_CAPTURE')
        local current=sample(1);assert(current.availability=='READY'and current.reference.token=='NEW_REFERENCE')
        ''')

    def test_same_city_reentrant_reader_never_certifies_last_sample_as_current(self):
        c=depth_context();c.execute('''sample(1);sample(2);local get=cities[1].GetBuildings;local once=true
        cities[1].GetBuildings=function()if once then
         once=false;local nested=sample(1);assert(nested.error=='DC_CAPTURE_IN_PROGRESS'and nested.availability=='TEMPORARILY_UNAVAILABLE'and nested.value.domains.DISTRICT_CAMPUS.value==1)
         assert(sample(2).availability=='READY')
        end;return get()end
        shared.DistrictCompleteness.MarkDirty(0,1);assert(sample(1).availability=='READY')''')

    def test_native_write_generation_during_capture_requires_new_related_cause(self):
        c=depth_context();c.execute('''
        local version=0;shared.EffectiveFacts={Version=function()return version end}
        sample(1);local get=cities[1].GetBuildings;local once=true
        cities[1].GetBuildings=function()if once then once=false;version=version+1 end;return get()end
        shared.DistrictCompleteness.MarkDirty(0,1);local d=sample(1)
        assert(d.error=='DC_WRITE_DURING_CAPTURE'and d.value.domains.DISTRICT_CAMPUS.value==1)
        local n=counts.dc_capture;sample(1);assert(counts.dc_capture==n)
        shared.DistrictCompleteness.MarkDirty(0,1);assert(sample(1).availability=='READY')
        ''')

    def test_confirmed_removal_releases_capacity_and_no_raw_resurrection_on_new_reference(self):
        c=depth_context(2049);c.execute('''
        for i=1,2048 do sample(i)end
        Events.CityRemovedFromMap.Fire(0,1);assert(shared.DistrictCompleteness.BusinessCacheSize()==2047)
        assert(sample(2049).availability=='READY'and shared.DistrictCompleteness.BusinessCacheSize()==2048)
        resetCounts();sample(2049);assert(not counts.dc_capture)
        Events.LoadScreenClose.Fire();assert(shared.DistrictCompleteness.BusinessCacheSize()==0 and shared.DistrictCompleteness.CacheSize()==0)
        cities[1].token='REUSED';cities[1].present={};local d=sample(1,true)
        assert(d.availability=='READY'and d.value.domains.DISTRICT_CAMPUS.value==0)
        ''')

    def test_confirmed_store_return_matches_old_location_not_new_city_id(self):
        context=Context();context.execute("shared.CityProgressionStore={RegisterReturn=function(name,fn)onReturn=fn end}")
        with patch('refactor_fixtures.Context',return_value=context):c=depth_context()
        c.execute('''
        cities[1].GetX=function()return 1 end;sample(1);sample(2)
        cities[1].id=900;onReturn(0,cities[1])
        assert(shared.DistrictCompleteness.BusinessCacheSize()==1)
        resetCounts();sample(2);assert(not counts.dc_capture)
        ''')

    def test_unprintable_capture_error_cannot_leave_a_false_ready_hit(self):
        c=depth_context();c.execute('''sample(1);local get=cities[1].GetBuildings
        cities[1].GetBuildings=function()error(setmetatable({},{__tostring=function()error('BROKEN_STRING')end}))end
        shared.DistrictCompleteness.MarkDirty(0,1);local d=sample(1)
        assert(d.error=='DC_CAPTURE_FAILED'and d.availability=='TEMPORARILY_UNAVAILABLE')
        local n=counts.dc_capture;assert(sample(1).availability=='TEMPORARILY_UNAVAILABLE'and counts.dc_capture==n)
        cities[1].GetBuildings=get;shared.DistrictCompleteness.MarkDirty(0,1);assert(sample(1).availability=='READY')''')

    def test_many_idle_boundaries_do_not_capture_or_write(self):
        c=depth_context(32);c.execute('for i=1,32 do sample(i)end;resetCounts();for i=1,1000 do publish()end;assert(not counts.dc_capture and not counts.building_check and not counts.property_write and not counts.carrier_write)')


if __name__=='__main__':unittest.main()
