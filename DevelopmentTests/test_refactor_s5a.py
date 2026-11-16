"""S5a primitive gates. Explicit pure scopes; production wiring follows S5a2."""
import unittest
import xml.etree.ElementTree as E
from refactor_harness import Context,ROOT


def registry():
    c=Context();c.load('FactChanges');c.execute("d=SPCFactChanges.New(shared);calls={};function emit(id,kind,topic,revision)d.Emit({owner=0,cityID=id,reference='REF'..id,kinds={kind or 'ACTIVE'},cause='FIXTURE_FACT',topic=topic,revision=revision})end")
    return c


class Registry(unittest.TestCase):
    def test_explicit_scope_kinds_topics_and_mark_only_until_flush(self):
        c=registry();c.execute("d.RegisterConsumer('identity',function(r)calls[#calls+1]='I'..r.city end,{kinds={'IDENTITY'}});d.RegisterConsumer('templates',function(r)calls[#calls+1]='T'..r.city end,{kinds={'HISTORY'},topics={'TEMPLATES'}});emit(1,'ACTIVE');emit(2,'IDENTITY');emit(3,'HISTORY','INSIGHTS');emit(4,'HISTORY','TEMPLATES');assert(#calls==0 and d.pending==4);d.Flush();assert(table.concat(calls,',')=='I2,T4');assert(d.pending==0)")
    def test_phase_order_and_consumer_failure_isolation_no_idle_retry(self):
        c=registry();c.execute("d.RegisterConsumer('effects',function(r)calls[#calls+1]='E'..r.city end,{kinds={'ACTIVE'},phase=1});d.RegisterConsumer('broken',function()error('BROKEN')end,{kinds={'ACTIVE'},phase=0});d.RegisterConsumer('invalidate',function(r)calls[#calls+1]='D'..r.city end,{kinds={'ACTIVE'},phase=0});emit(1);emit(2);d.Flush();assert(table.concat(calls,',')=='D1,D2,E1,E2' and d.errors.broken);local n=d.delivered;for i=1,1000 do d.Flush()end;assert(d.delivered==n)")
    def test_detached_investment_evidence_and_consumer_copy_isolation(self):
        c=registry();c.execute("local proof={status='COMMITTED',cause='INVESTMENT_COMMITTED',player=0,city=1,receipt='R',unitUID='U',revision=2,reference={owner=0,cityID=1,x=1,y=1},anchor={owner=0,cityID=1,token='T',first={districtID=1,type='DISTRICT_CAMPUS'},specialization='RESEARCH'}};d.RegisterConsumer('mutator',function(r)r.investment.anchor.first.type='MUTATED';r.kinds.ACTIVE=nil end,{kinds={'POTENTIAL'}});d.RegisterConsumer('reader',function(r)assert(r.investment.anchor.first.type=='DISTRICT_CAMPUS' and r.kinds.ACTIVE and r.investment.receipt=='R');calls[#calls+1]=r end,{kinds={'POTENTIAL'}});d.Emit({owner=0,cityID=1,reference='REF1',kinds={'POTENTIAL','ACTIVE'},cause='INVESTMENT_COMMITTED',revision=2,investment=proof});proof.anchor.token='CHANGED';emit(1,'HISTORY','TEMPLATES',3);d.Flush();assert(#calls==1 and calls[1].investment.anchor.token=='T' and calls[1].revisions.POTENTIAL==2 and calls[1].revisions.HISTORY==3)")
    def test_coalesces_before_publish_but_second_true_change_runs_again(self):
        c=registry();c.execute("d.RegisterConsumer('consumer',function(r)calls[#calls+1]=r.revision end,{kinds={'ACTIVE'}});for i=1,10 do emit(1,'ACTIVE',nil,i)end;assert(d.pending==1 and #calls==0);d.Flush();assert(#calls==1 and calls[1]==10);emit(1,'ACTIVE',nil,11);d.Flush();assert(#calls==2 and calls[2]==11)")
    def test_reentry_keeps_new_snapshot_and_never_recurses(self):
        c=registry();c.execute("d.RegisterConsumer('consumer',function(r)calls[#calls+1]=r.city;if #calls==1 then emit(2);assert(not d.Flush())end end,{kinds={'ACTIVE'}});emit(1);d.Flush();assert(#calls==1 and d.pending==1);d.Flush();assert(#calls==2 and calls[2]==2 and d.pending==0)")
    def test_capacity_invalid_payload_and_topic_overflow_are_atomic(self):
        c=registry();c.execute("for i=1,2048 do emit(i)end;assert(not pcall(emit,2049) and d.pending==2048 and d.sequence==2048);local cyclic={};cyclic.self=cyclic;assert(not pcall(d.Emit,{owner=0,cityID=1,kinds={'ACTIVE'},cause='INVALID',evidence=cyclic}));assert(d.sequence==2048);d.Close();d=SPCFactChanges.New(shared);for i=1,32 do d.Emit({owner=0,cityID=1,kinds={'HISTORY'},cause='CAUSE'..i,topic='TOPIC'..i})end;assert(not pcall(d.Emit,{owner=0,cityID=1,kinds={'HISTORY'},cause='OVERFLOW',topic='OVERFLOW'}));assert(d.sequence==32 and d.pending==1);d.RegisterConsumer('verify',function(r)assert(not r.causes.OVERFLOW and not r.topics.OVERFLOW)end,{kinds={'HISTORY'}});d.Flush()")
    def test_rejects_native_metatables_functions_and_unbounded_declarations(self):
        c=registry();c.execute("for _,e in ipairs({setmetatable({},{__index=function()error('NATIVE_READ')end}),{callback=function()end}})do assert(not pcall(d.Emit,{owner=0,cityID=1,kinds={'ACTIVE'},cause='BAD',evidence=e}))end;assert(d.sequence==0);for i=1,128 do d.RegisterConsumer('C'..i,function()end,{kinds={'D'}})end;assert(not pcall(d.RegisterConsumer,'EXTRA',function()end,{kinds={'D'}}));assert(not pcall(d.Emit,{owner=0,cityID=1,kinds={'UNDECLARED'},cause='BAD'}))")
    def test_close_clears_context_without_removing_newer_instance(self):
        c=registry();c.execute("emit(1);local old=d;d=SPCFactChanges.New(shared);old.Close();assert(shared.FactChanges==d and old.pending==0 and not old.Flush());emit(2);d.Close();assert(shared.FactChanges==nil and not d.Flush() and not pcall(emit,3))")
    def test_actual_composition_quarantines_failed_registered_consumer(self):
        c=registry();c.load('RuntimeComposition');c.execute("local startup=SPCRuntimeComposition.New(shared);local writes=0;startup.Run('bad',{}, {},function()d.RegisterConsumer('bad',function()writes=writes+1 end,{kinds={'ACTIVE'}});error('LATE_FAILURE')end);startup.Run('good',{}, {},function()d.RegisterConsumer('good',function()calls[#calls+1]='GOOD'end,{kinds={'ACTIVE'}})end);emit(1);d.Flush();assert(writes==0 and #calls==1 and d.errors.bad and shared.StartStatus.bad.state=='FAILED')")
    def test_nested_payload_validation_matches_final_envelope_and_no_stuck_busy(self):
        c=registry();c.execute("local deep={};for i=1,7 do deep={next=deep}end;assert(not pcall(d.Emit,{owner=0,cityID=1,kinds={'ACTIVE'},cause='DEEP',evidence=deep}) and d.sequence==0);deep={};for i=1,6 do deep={next=deep}end;d.RegisterConsumer('good',function(r)calls[#calls+1]=r.city end,{kinds={'ACTIVE'}});d.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='DEEP',evidence=deep});d.Flush();assert(#calls==1);emit(2);d.Flush();assert(#calls==2)")
    def test_close_during_callback_stops_old_snapshot_and_new_context_works(self):
        c=registry();c.execute("local old=d;d.RegisterConsumer('close',function(r)calls[#calls+1]=r.city;d=SPCFactChanges.New(shared)end,{kinds={'ACTIVE'}});emit(1);emit(2);old.Flush();assert(#calls==1 and old.closed and not old.Flush());d.RegisterConsumer('new',function(r)calls[#calls+1]=r.city end,{kinds={'ACTIVE'}});emit(3);d.Flush();assert(#calls==2 and calls[2]==3 and shared.FactChanges==d)")
    def test_throwing_error_formatter_does_not_latch_dispatch(self):
        c=registry();c.execute("d.RegisterConsumer('bad',function()error(setmetatable({},{__tostring=function()error('FORMAT_FAILED')end}))end,{kinds={'ACTIVE'}});d.RegisterConsumer('good',function(r)calls[#calls+1]=r.city end,{kinds={'ACTIVE'}});emit(1);d.Flush();emit(2);d.Flush();assert(#calls==2 and d.errors.bad=='FACT_CALLBACK_FAILED')")
    def test_envelope_and_declarations_reject_metatables_before_access(self):
        c=registry();c.execute("local reads=0;local native=setmetatable({},{__index=function()reads=reads+1;error('NATIVE_READ')end});assert(not pcall(d.Emit,native));assert(not pcall(d.RegisterConsumer,'options',function()end,native));assert(not pcall(d.RegisterConsumer,'list',function()end,{kinds=native}));assert(not pcall(d.Emit,{owner=0,kinds=native,cause='BAD'}));assert(reads==0 and d.sequence==0)")
    def test_declared_topic_capacity_is_bounded_and_registration_atomic(self):
        c=registry();c.execute("local topics={};for i=1,33 do topics[i]='T'..i end;assert(not pcall(d.RegisterConsumer,'topic',function()end,{kinds={'HISTORY'},topics=topics}));topics[33]=nil;d.RegisterConsumer('topic',function()calls[#calls+1]='OK'end,{kinds={'HISTORY'},topics=topics});emit(1,'HISTORY','T32');d.Flush();assert(#calls==1)")
    def test_runtime_helpers_are_in_vfs_and_package_inventory(self):
        root=E.parse(ROOT/'Mod/SpecializationP0.modinfo');package=[v.text for v in root.findall('./Files/File')];imports=[v.text for v in root.findall("./InGameActions/ImportFiles[@id='SPCP0_Common']/File")]
        for name in ['FactChanges.lua','SafeCallbacks.lua','RuntimeComposition.lua','UI/SafeAdapters.lua']:
            self.assertEqual(package.count(name),1);self.assertEqual(imports.count(name),1)

if __name__=='__main__':unittest.main()
