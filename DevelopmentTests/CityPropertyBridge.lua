-- Local integration candidate ONLY. Injected API-shaped city mocks; never in modinfo.
-- The caller supplies validated fresh-history evidence or uses read-only load reconciliation.
local M={}
function M.New(deps,pid,cid,token,fresh,context)
 assert(context=="MOCK_ONLY" and deps.contextSource=="MOCK_ONLY","OFFLINE_ONLY")
 assert(type(token)=="string" and #token>0,"BOUND_TOKEN_REQUIRED")
 local permit=deps.life.Acquire(pid);assert(permit,"NO_ENTRY_PERMISSION")
 local function permitted() assert(deps.life.Check(permit,pid),"ENTRY_PERMISSION_EXPIRED") end
 permitted() -- No city access for disabled/unknown/noncurrent owners.
 local proof=false
 if fresh~=nil then
  assert(fresh.contextSource==context and fresh.status=="FRESH_BOUND_HISTORY_COMPLETE"
   and fresh.owner==pid and fresh.cityID==cid and fresh.token==token,"FRESH_HISTORY_REQUIRED")
  proof=true
 end
 local x,y
 local function city()
  local c=deps.CityManager.GetCity(pid,cid)
  assert(c and c:GetOwner()==pid and c:GetID()==cid,"CITY_REFERENCE_CHANGED")
  local bound,state=deps.binding.Resolve(pid,c)
  assert(bound==token and state=="BOUND_MATCH","CITY_BINDING_CHANGED")
  assert(c:GetOwner()==pid and c:GetID()==cid,"CITY_CHANGED_DURING_BINDING_READ")
  local cx,cy=c:GetX(),c:GetY()
  if x==nil then
   assert(type(cx)=="number" and type(cy)=="number","CITY_POSITION_REQUIRED")
   x,y=cx,cy
  end
  assert(cx==x and cy==y,"CITY_POSITION_CHANGED")
  return c
 end
 city();permitted()
 local function identity()
  city()
  return {contextSource=context,present=true,owner=pid,cityUID=token,freshFoundationObserved=proof}
 end
 local key="SPC_MOCK_CITY_ENVELOPE_CANDIDATE"
 local store={}
 function store.read()
  local c=city();local value=c:GetProperty(key)
  city() -- getter callbacks must not silently change owner/binding/position.
  return {status="READ_OK",value=value}
 end
 function store.write(value)
  permitted();local c=city();permitted()
  -- Authorization remains the entry epoch; re-enabling requires a new channel.
  c:SetProperty(key,value)
 end
 local adapter=deps.Envelope.New(store,deps.Recovery,identity,context)
 local gate=deps.Gate.New(deps.life,deps.Planner.New(deps.State),adapter.Resolve,context,
  {model=deps.Recovery,read=adapter.ReadRecord,write=adapter.WriteRecord})
 return {gate=gate,writeFacts=adapter.WriteFacts,readRecord=adapter.ReadRecord,reference=token}
end
return M
