-- Research-only pure planner. No native reader, Property, Modifier, or yield application.
-- TOTAL is a user-authorized conditional alternative; not an accepted-spec replacement.
local M={}
local yields={RESEARCH='SCIENCE',CULTURE='CULTURE',INDUSTRY='PRODUCTION'}
local function finite(n) return type(n)=='number' and n==n and math.abs(n)<math.huge end
function M.Plan(s,mode)
 local ok,result=pcall(function()
  assert(s.context=='MOCK_ONLY' and s.complete==true,'SNAPSHOT_NOT_COMPLETE_MOCK')
  assert(mode=='LOCAL' or mode=='TOTAL','BASIS_MODE')
  local out={status='OFFLINE_PROPOSAL',mode=mode,revision=s.revision,cities={},edges={}}
  for id,c in pairs(s.cities) do
   if c.owner==s.player and c.specialization=='COMMERCE' and c.active==4 then
    local row={SCIENCE={amount=0,sources={}},CULTURE={amount=0,sources={}},PRODUCTION={amount=0,sources={}}}
    out.cities[id]=row
    for src,connected in pairs((s.directSources or {})[id] or {}) do
     local f=s.cities[src]
     assert(f,'SOURCE_MISSING')
     if connected and f.owner==s.player and yields[f.specialization] and f.active>=1 and f.active<=4 then
      local y=yields[f.specialization]
      -- Input provenance is a research fixture, not something the native API supplies.
      if mode=='LOCAL' then assert(f.localBasisVerified,'LOCAL_BASIS_UNVERIFIED') end
      local amount=(mode=='LOCAL' and f.localYields or f.totalYields)[y]
      assert(finite(amount) and amount>=0,'BASIS_INVALID_OR_NEGATIVE')
      out.edges[#out.edges+1]={from=src,to=id,yield=y}
      local target=row[y]
      if target.basis==nil or amount>target.basis then
       target.basis=amount;target.amount=0.2*amount;target.sources={[src]=true}
      elseif amount==target.basis then target.sources[src]=true end
     end
    end
   end
  end
  -- Diagnose possible additional same-output dependencies supplied by research fixtures.
  -- Native completeness of this graph is NOT asserted by this offline planner.
  local graph={}
  for _,edge in ipairs(out.edges) do graph[edge.from]=graph[edge.from] or {};graph[edge.from][edge.to]=true end
  for _,edge in ipairs(s.extraDependencies or {}) do graph[edge.from]=graph[edge.from] or {};graph[edge.from][edge.to]=true end
  local visiting,done={},{}
  local function visit(id)
   assert(not visiting[id],'YIELD_DEPENDENCY_CYCLE_REVIEW_REQUIRED')
   if done[id] then return end
   visiting[id]=true
   for nextID in pairs(graph[id] or {}) do visit(nextID) end
   visiting[id]=nil;done[id]=true
  end
  for id in pairs(graph) do visit(id) end
  return out
 end)
 if not ok then return {status='UNKNOWN',reason=tostring(result)} end
 return result
end
return M
