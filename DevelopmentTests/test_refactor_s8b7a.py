"""Behavior-neutral split of existing Commerce config/reputation validation."""
import json,subprocess,unittest
from refactor_harness import ROOT,Context,measure

BASE='1bffe3b'
SETUP="""
function setup()
 local v=SPCCommerceModel.New(0);v.selected={'DISTRICT_CAMPUS','DISTRICT_THEATER'}
 v=SPCCommerceModel.BeginReputation(v,0,'THREE')
 local r={origin={owner=0},base={specialization='COMMERCE',first={turn=0}},investment={investments={ONE='U1',TWO='U2',THREE='U3'}}}
 return v,r
end
function encode(t)
 if type(t)~='table'then return type(t)..':'..tostring(t)end
 local keys={};for k in pairs(t)do keys[#keys+1]=k end;table.sort(keys,function(a,b)return tostring(a)<tostring(b)end)
 local out={};for _,k in ipairs(keys)do out[#out+1]=encode(k)..'='..encode(t[k])end;return '{'..table.concat(out,',')..'}'
end
function result(fn)
 local ok,value=pcall(fn)
 if not ok then return 'ERROR:'..(type(value)=='string'and value:match('([A-Z][A-Z_]+)$')or'UNKNOWN')end
 return encode(value)
end
"""


def context(old=False):
 c=Context();c.load('RestructuringModel');c.load('TurnLedger')
 if old:
  source=subprocess.check_output(['git','show',BASE+':Mod/CommerceModel.lua'],cwd=ROOT,text=True)
  from hashlib import sha256
  from refactor_harness import SOURCES,executed,completion
  digest=sha256(source.encode()).hexdigest();key='historical/'+BASE+'/Mod/CommerceModel.lua';SOURCES[digest]=key;executed(key,digest)
  try:c.execute(source)
  except Exception:completion(key,False);raise
  completion(key,True)
 else:c.load('CommerceModel')
 c.execute(SETUP);return c


class Differential(unittest.TestCase):
 def test_full_validator_accepts_rejects_in_identical_order_without_mutation(self):
  mutations=['',"v=nil","v=false","v='BROKEN'","v.version=99","v.owner=-1","v.selected='BROKEN'","v.selected[2]='DISTRICT_CAMPUS'","v.selected[1]=nil","v.selected[0]='DISTRICT_HARBOR'","v.selected[6]='DISTRICT_HARBOR'","v.selected[1]='DISTRICT_UNKNOWN'","v.reputation='BROKEN'","v.reputation.version=99","v.reputation.age=99","v.reputation.cursor=-1","v.reputation.age=1","v.reputation.state='UNKNOWN'","v.reputation.receipt=''","r.origin.owner=9","r.investment.investments.THREE=nil","v.reputation.qualification={}","v.selected[2]='DISTRICT_CAMPUS';v.reputation='BROKEN'","v.extra={keep=true};v.reputation.extra='keep'"]
  for mutation in mutations:
   values=[]
   for old in (True,False):
    c=context(old);c.execute('v,r=setup();'+(mutation+';'if mutation else '')+'before=encode(v);out=result(function()return SPCCommerceModel.Validate(v,r)end);assert(encode(v)==before)')
    values.append(c.eval('out'))
   self.assertEqual(values[0],values[1],mutation)
  measure('S8b7a_Commerce_validation_differential',{'cases':len(mutations),'same_result_error_order_bytes':True,'production_partial_consumer':'NOT_YET_WIRED'})
 def test_original_business_operations_have_exact_same_outputs(self):
  calls=["return SPCCommerceModel.Select(v,'DISTRICT_HARBOR',true)","return SPCCommerceModel.EffectiveSelections(v,1)","return SPCCommerceModel.Advance(v,10,'COMMERCE')","local n=SPCCommerceModel.Advance(v,10,'COMMERCE');return SPCCommerceModel.Advance(n,20,'COMMERCE')","return SPCCommerceModel.Exit(v)","return SPCCommerceModel.OwnerChanged(v,1,10)","local n=SPCCommerceModel.OwnerChanged(v,1,10);return SPCCommerceModel.Resume(n,0,20)","v.reputation='BROKEN';return SPCCommerceModel.Select(v,'DISTRICT_HARBOR',true)","v.reputation='BROKEN';return SPCCommerceModel.EffectiveSelections(v,1)"]
  for operation in calls:
   values=[]
   for old in (True,False):
    c=context(old);c.execute('v,r=setup();out=result(function()'+operation+'end)');values.append(c.eval('out'))
   self.assertEqual(values[0],values[1],operation)
 def test_full_validator_returns_same_object_and_pure_subchecks_do_not_read_natives(self):
  c=context();c.execute("v,r=setup();local before=encode(v);assert(rawequal(SPCCommerceModel.Validate(v,r),v)and rawequal(SPCCommerceModel.ValidateConfiguration(v,r),v)and rawequal(SPCCommerceModel.ValidateReputation(v.reputation,r),v.reputation));local bad=setmetatable({},{__index=function()error('NATIVE_FORBIDDEN')end});Players=bad;Game=bad;GameInfo=bad;GameConfiguration=bad;Events=bad;GameEvents=bad;SPCCommerceModel.Validate(v,r);assert(encode(v)==before)")
 def test_subchecks_separate_observations_without_changing_full_failure_behavior(self):
  c=context();c.execute("v,r=setup();v.reputation='BROKEN';assert(pcall(SPCCommerceModel.ValidateConfiguration,v,r)and not pcall(SPCCommerceModel.ValidateReputation,v.reputation,r)and not pcall(SPCCommerceModel.Validate,v,r));v,r=setup();v.selected='BROKEN';assert(not pcall(SPCCommerceModel.ValidateConfiguration,v,r)and pcall(SPCCommerceModel.ValidateReputation,v.reputation,r)and not pcall(SPCCommerceModel.Validate,v,r))")


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 inherited=unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S8b6'])
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
