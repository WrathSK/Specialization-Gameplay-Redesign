-- Offline candidate: keep B015/B020 foundation records unchanged; store only investments.
local M={}
local families={RESEARCH='CAMPUS',CULTURE='THEATER_SQUARE',INDUSTRY='INDUSTRIAL_ZONE',COMMERCE='COMMERCIAL_HUB'}
local function cp(v) if type(v)~='table' then return v end;local c={};for k,x in pairs(v) do c[k]=cp(x) end;return c end
local function same(a,b)
 if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
 for k,v in pairs(a) do if not same(v,b[k]) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end;return true
end
function M.New(rules,id,storage)
 assert(id.contextSource=='MOCK_ONLY','OFFLINE_ONLY')
 local function foundation()
  -- Future adapter delegates to actual CityFlowProbe.SupportFacts, not raw district inference.
  local f=storage.foundation()
  assert(type(f)=='table' and f.owner==id.owner and f.token==id.cityUID
   and type(f.cityID)=='number' and f.potential==1 and families[f.specialization]
   and f.health=='TRACKING' and f.kind=='DEV_FOUNDATION_JOURNAL'
   and type(f.first)=='table' and type(f.first.districtID)=='number' and type(f.first.type)=='string',
   'VERIFIED_SPECIALIZED_FOUNDATION_REQUIRED')
  return f
 end
 local function anchor(f) return {owner=f.owner,cityID=f.cityID,token=f.token,first=cp(f.first),specialization=f.specialization} end
 local function read()
  local f=foundation();local saved=storage.read()
  if saved then
   assert(saved.schema==1 and same(saved.anchor,anchor(f)),'INVESTMENT_ANCHOR_CHANGED')
   assert(type(saved.investments)=='table','INVESTMENT_LEDGER_REQUIRED')
  else saved={investments={},revision=1} end
  local n=0;for _ in pairs(saved.investments) do n=n+1 end
  local facts={schemaVersion=1,owner=id.owner,cityUID=id.cityUID,revision=saved.revision,
   specialization=f.specialization,potential=1+n,investments=cp(saved.investments),
   firstCompletion={family=families[f.specialization],eventID='FOUNDATION:'..id.cityUID,
    districtUID=id.cityUID..':DISTRICT:'..f.first.districtID}}
  local valid=rules.Restore(facts,id);assert(valid.status=='READY',valid.reason)
  return {schema=1,facts=valid.facts,pending=cp(saved.pending)}
 end
 local function write(nextState)
  local f=foundation();local old=read()
  assert(nextState.schema==1,'STATE_SCHEMA')
  local valid=rules.Restore(nextState.facts,id);assert(valid.status=='READY',valid.reason)
  assert(same(nextState.facts.firstCompletion,old.facts.firstCompletion)
   and nextState.facts.specialization==old.facts.specialization,'FOUNDATION_MUST_NOT_CHANGE')
  -- Restore only copies recognized permanent fields; no saved ACTIVE or received networks.
  storage.write({schema=1,anchor=anchor(f),revision=valid.facts.revision,
   investments=cp(valid.facts.investments),pending=cp(nextState.pending)})
 end
 local function effective(governor)
  local state=read();assert(not state.pending,'INVESTMENT_PENDING')
  return rules.Derive(state.facts,id,governor)
 end
 return {read=read,write=write,effective=effective}
end
return M
