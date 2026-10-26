"""Bounded derived network framing only; no actual persistence or consumer wiring."""
import json,unittest
from refactor_harness import Context,ROOT,measure
from test_refactor_s9f1 import plain

SETUP="""
M=SPCNetworkRecoveryModel
function commerce()
 return {version=1,family='COMMERCE',sequence=1,receiver={reference='receiver-reference',stamp='receiver-lifecycle'},shape={gold=15,access=true},sources={
 [1]={reference='self-reference',stamp='self-lifecycle',status='CONFIRMED',domains={DISTRICT_CAMPUS={eligible=true,X=30.125},DISTRICT_HOLY_SITE={eligible=false}}},
 [2]={reference='source-reference',stamp='source-lifecycle',status='RETAINED',domains={DISTRICT_CAMPUS={eligible=true,X=11.25}}},
 [3]={status='UNKNOWN',reference='unknown-reference'}}}
end
function culture()
 return {version=1,family='CULTURE',sequence=2,receiver={reference='receiver-reference',stamp='receiver-lifecycle'},shape={kind='RESEARCH',plot=123,count=2},sources={
 [1]={reference='source1',stamp='lifecycle1',status='CONFIRMED',eligible=true,civilizations={CIVILIZATION_ROME=true,CIVILIZATION_GREECE=true}},
 [2]={reference='source2',stamp='lifecycle2',status='RETAINED',eligible=true,civilizations={CIVILIZATION_ROME=true}},
 [3]={status='CONFIRMED',reference='source3',stamp='lifecycle3',eligible=false,civilizations={}},
 [4]={status='UNKNOWN'}}}
end
function roundtrip(v)local encoded=M.Encode(v);local out=M.Decode(encoded);assert(M.Encode(out)==encoded);return out,encoded end
function frame(value)return #value..':'..value end
"""
def context():
 v=Context();v.load('NetworkRecoveryModel');v.execute(SETUP);return v

class Codec(unittest.TestCase):
 def test_exact_commerce_facts_shape_and_three_provenance_states_roundtrip(self):
  v=context();v.execute("local out=roundtrip(commerce());assert(out.shape.gold==15 and out.shape.access and out.sources[1].domains.DISTRICT_CAMPUS.X==30.125 and out.sources[2].status=='RETAINED'and out.sources[3].status=='UNKNOWN'and not out.sources[3].domains)")
 def test_complete_civilization_sets_overlap_and_ineligible_empty_source_roundtrip(self):
  v=context();v.execute("local out,wire=roundtrip(culture());assert(out.sources[1].civilizations.CIVILIZATION_ROME and out.sources[2].civilizations.CIVILIZATION_ROME and out.sources[1].civilizations.CIVILIZATION_GREECE and not out.sources[3].eligible and out.shape.count==2);local _,n=wire:gsub('CIVILIZATION_ROME','');assert(n==1)")
 def test_canonical_order_ignores_table_insertion_order(self):
  v=context();v.execute("local a,b=culture(),culture();b.sources={};for i=4,1,-1 do b.sources[i]=a.sources[i]end;b.sources[1].civilizations={CIVILIZATION_GREECE=true,CIVILIZATION_ROME=true};assert(M.Encode(a)==M.Encode(b));a=commerce();b=commerce();b.sources[1].domains={DISTRICT_HOLY_SITE={eligible=false},DISTRICT_CAMPUS={eligible=true,X=30.125}};assert(M.Encode(a)==M.Encode(b))")
 def test_exact_decimal17_survives_binary32_native_number_counterexample(self):
  v=context();v.execute("for _,n in ipairs({0,1/3,.1,123456.123456789,1e-250,1e200,9007199254740990})do local a=commerce();a.sources[1].domains.DISTRICT_CAMPUS.X=n;local out=roundtrip(a);assert(out.sources[1].domains.DISTRICT_CAMPUS.X==n)end")
  import struct
  self.assertNotEqual(struct.unpack('f',struct.pack('f',1/3))[0],1/3)
  measure('S9g1_decimal17_network_values',{'wire':'canonical string framing','double_roundtrip':True,'binary32_fraction_counterexample':True,'native_Property_writes':0})
 def test_source_and_sequence_integers_keep_exact_near_maximum_supported_values(self):
  v=context();v.execute("local a=commerce();a.sequence=9007199254740990;a.sources[999999999]=a.sources[1];a.sources[1]=nil;local out=roundtrip(a);assert(out.sequence==a.sequence and out.sources[999999999])")
 def test_empty_bundle_zero_shapes_and_absent_unknown_reference_are_not_invented_facts(self):
  v=context();v.execute("local a=commerce();a.sources={};a.shape={gold=0,access=false};local out=roundtrip(a);assert(next(out.sources)==nil and out.shape.gold==0 and not out.shape.access);a=culture();a.sources={[1]={status='UNKNOWN'}};a.shape={kind='NONE',count=0};out=roundtrip(a);assert(out.sources[1].reference==nil and out.shape.plot==nil)")
 def test_no_native_cache_or_permanent_Copy_surface_is_accessed(self):
  v=context();v.execute("local bad=setmetatable({},{__index=function()error('NATIVE_OR_COPY_FORBIDDEN')end});Game=bad;Players=bad;GameInfo=bad;Events=bad;GameEvents=bad;SPCCityIdentityRead=bad;local a=roundtrip(commerce());local b=roundtrip(culture());assert(a and b)")
 def test_detached_codec_does_not_mutate_input_or_share_nested_tables(self):
  v=context();v.execute("local a=commerce();local before=M.Encode(a);local out=M.Decode(before);out.sources[1].domains.DISTRICT_CAMPUS.X=99;out.receiver.stamp='CHANGED';assert(M.Encode(a)==before and a.sources[1].domains.DISTRICT_CAMPUS.X==30.125)")
 def test_new_lua_context_decodes_exact_blob_without_old_objects(self):
  a=context();wire=a.eval('M.Encode(culture())');b=context();b.execute("local out=M.Decode(...);assert(out.sources[2].status=='RETAINED'and out.sources[2].civilizations.CIVILIZATION_ROME)",wire)
 def test_source_limit_512_and_no_513_silently_dropped(self):
  v=context();v.execute("local a=commerce();a.sources={};for i=1,512 do a.sources[i]={status='UNKNOWN'}end;assert(roundtrip(a));a.sources[513]={status='UNKNOWN'};assert(not pcall(M.Encode,a))")
 def test_culture_dictionary_255_and_per_source_64_are_hard_limits(self):
  v=context();v.execute("local a=culture();a.sources={};for i=1,4 do local set={};for j=1,(i==4 and 63 or 64)do set['CIVILIZATION_TEST_'..((i-1)*64+j)]=true end;a.sources[i]={status='CONFIRMED',reference='r'..i,stamp='s'..i,eligible=true,civilizations=set}end;assert(roundtrip(a));a.sources[4].civilizations.CIVILIZATION_TEST_256=true;assert(not pcall(M.Encode,a));a=culture();for i=1,65 do a.sources[1].civilizations['CIVILIZATION_TEST_'..i]=true end;assert(not pcall(M.Encode,a))")
 def test_worst_supported_reference_lengths_and_512_five_domain_sources_fit_hard_wire_cap(self):
  v=context();v.execute("local a=commerce();a.sources={};local names={'DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE','DISTRICT_HOLY_SITE','DISTRICT_HARBOR'};for i=1,512 do local domains={};for _,name in ipairs(names)do domains[name]={eligible=true,X=1.234567891234567e100}end;a.sources[i]={status='CONFIRMED',reference=string.rep('r',512),stamp=string.rep('s',512),domains=domains}end;local out,wire=roundtrip(a);commerceBytes=#wire;assert(commerceBytes<M.MaxBytes and out.sources[512])")
  measure('S9g1_maximum_commerce_bundle',{'sources':512,'domains_each':5,'reference_and_stamp_bytes_each':512,'wire_bytes':v.eval('commerceBytes'),'wire_cap_bytes':1048576,'base_Copy_budget_changed':False,'automatic_calls':0})
 def test_worst_culture_reference_dictionary_and_set_sizes_fit_wire_cap_without_duplicate_strings(self):
  v=context();v.execute("local a=culture();a.sources={};for i=1,512 do local set={};for j=1,64 do local id=((i+j-2)%255)+1;local name='CIVILIZATION_'..string.rep('X',109)..string.format('%06d',id);set[name]=true end;a.sources[i]={status='CONFIRMED',reference=string.rep('r',512),stamp=string.rep('s',512),eligible=true,civilizations=set}end;local out,wire=roundtrip(a);cultureBytes=#wire;assert(cultureBytes<M.MaxBytes and out.sources[512])")
  measure('S9g1_maximum_culture_bundle',{'sources':512,'civilizations_each':64,'dictionary':255,'wire_bytes':v.eval('cultureBytes'),'wire_cap_bytes':1048576,'native_storage_or_CPU_claim':False})
 def test_unknown_source_cannot_contain_any_raw_fact_or_set(self):
  for change in ("a.sources[3].domains={}","a.sources[3].eligible=false","a.sources[3].civilizations={}"):
   v=context();v.execute('local a=commerce();'+change+';assert(not pcall(M.Encode,a))')
 def test_nonfinite_negative_and_fractional_ids_or_sequences_reject(self):
  for change in ('a.sequence=0','a.sequence=.5','a.sequence=math.huge','a.sources[-1]=a.sources[1]','a.sources[.5]=a.sources[1]',"a.sources['1']=a.sources[1]",'a.sources[1].domains.DISTRICT_CAMPUS.X=-1','a.sources[1].domains.DISTRICT_CAMPUS.X=0/0','a.sources[1].domains.DISTRICT_CAMPUS.X=math.huge'):
   v=context();v.execute('local a=commerce();'+change+';assert(not pcall(M.Encode,a))')
 def test_version_unknown_fields_cross_family_and_malformed_shape_reject(self):
  for change in ('a.version=2','a.extra=true','a.receiver.extra=true','a.sources[1].extra=true','a.sources[1].domains.DISTRICT_CAMPUS.extra=true',"a.family='OTHER'","a.sources[1].status='READY'",'a.shape.gold=2147483648','a.shape.access=1',"a.sources[1].civilizations={}","a.sources[1].domains.UNKNOWN={eligible=false}"):
   v=context();v.execute('local a=commerce();'+change+';assert(not pcall(M.Encode,a))')
  for change in ("a.shape.kind='UNKNOWN'",'a.shape.count=256',"a.shape={kind='NONE',plot=4,count=0}",'a.sources[3].civilizations.CIVILIZATION_ROME=true',"a.sources[1].civilizations={WRONG=true}"):
   v=context();v.execute('local a=culture();'+change+';assert(not pcall(M.Encode,a))')
 def test_overlong_references_identifiers_and_metatables_reject_without_native_access(self):
  for change in ("a.receiver.reference=string.rep('r',513)","a.sources[1].stamp=string.rep('s',513)",'a.sources=setmetatable(a.sources,{})','a.sources[1].domains=setmetatable(a.sources[1].domains,{})','a.sources[1].domains.DISTRICT_CAMPUS=a.sources','a.sources[1].domains.DISTRICT_CAMPUS.X=function()end'):
   v=context();v.execute('local a=commerce();'+change+';assert(not pcall(M.Encode,a))')
 def test_every_single_byte_prefix_truncation_and_extra_suffix_reject(self):
  v=context();v.execute("local wire=M.Encode(commerce());for i=0,#wire-1 do assert(not pcall(M.Decode,wire:sub(1,i)))end;assert(not pcall(M.Decode,wire..'0:'));assert(not pcall(M.Decode,wire..'X'));assert(not pcall(M.Decode,string.rep('x',M.MaxBytes+1)))")
 def test_noncanonical_integer_boolean_version_and_frame_lengths_reject(self):
  v=context();v.execute("local w=M.Encode(commerce());for _,b in ipairs({'01:x','-1:x','1.0:x','10000000:x','9999999:'})do assert(not pcall(M.Decode,b))end;local v=w:gsub(frame('SPC_NETWORK_RECOVERY')..frame('1'),frame('SPC_NETWORK_RECOVERY')..frame('2'),1);assert(not pcall(M.Decode,v));v=w:gsub(frame('COMMERCE')..frame('1'),frame('COMMERCE')..frame('01'),1);assert(not pcall(M.Decode,v))")
 def test_only_library_is_packaged_no_production_reader_or_writer_includes_it(self):
  import xml.etree.ElementTree as ET
  name='NetworkRecoveryModel.lua';tree=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual([n.text for n in tree.findall('./Files/File')].count(name),1);self.assertIn(name,[n.text for n in tree.findall('./InGameActions/ImportFiles/File')])
  for p in ('CityProgressionStore.lua','Commerce.lua','CultureNetwork.lua','Gameplay.lua'):
   self.assertNotIn("include('NetworkRecoveryModel')",(ROOT/'Mod'/p).read_text())

if __name__=='__main__':unittest.main()
