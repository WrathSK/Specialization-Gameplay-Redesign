-- B018 composed diagnostic. No production authorization, property writes or yields.
SPCQualificationProbe={}
local Carrier=(function()
-- Read-only native-API candidate, NOT registered in modinfo. No engine writes/events.
-- env is injected for tests; actual Gameplay context/return behavior still needs user proof.
local M={}
function M.New(env,trait)
 assert(type(trait)=="string" and #trait>0,"EXPLICIT_CARRIER_REQUIRED")
 local C={}
 function C.Read(player)
  local out={contextSource="GAMEPLAY_CANDIDATE",player=player,status="UNKNOWN",carrier=trait}
  local ok,reason=pcall(function()
   assert(type(player)=="number" and player>=0 and player<math.huge and player%1==0,"INVALID_PLAYER")
   assert(env.Players and env.Players[player],"PLAYER_NOT_READY")
   local config=env.PlayerConfigurations and env.PlayerConfigurations[player]
   assert(config,"CONFIG_NOT_READY")
   local civ=config:GetCivilizationTypeName()
   assert(type(civ)=="string" and #civ>0,"CIV_NOT_READY")
   assert(env.GameInfo and env.GameInfo.Traits and env.GameInfo.Traits[trait],"CARRIER_NOT_DEFINED")
   local found=false
   -- No early success: an interrupted database iteration must not appear complete.
   for row in env.GameInfo.CivilizationTraits() do
    assert(type(row.CivilizationType)=="string" and type(row.TraitType)=="string","BAD_TRAIT_ROW")
    if row.CivilizationType==civ and row.TraitType==trait then found=true end
   end
   out.status=found and "ENABLED" or "DISABLED"
   out.civilization=civ
  end)
  if not ok then out.status="UNKNOWN";out.reason=tostring(reason) end
  return out
 end
 return C
end
return M

end)()
local Roster=(function()
-- Native API candidate; not registered with the running Mod. No persisted state.
-- Membership, qualification and historical participation are different facts.
local M={}
local function integer(n) return type(n)=="number" and n>=0 and n<math.huge and n%1==0 end
function M.Collect(env,readEligibility)
 local ok,result=pcall(function()
  assert(type(readEligibility)=="function","QUALIFICATION_READER_REQUIRED")
  local ids=env.PlayerManager.GetAliveIDs()
  assert(type(ids)=="table","ROSTER_NOT_A_TABLE")
  local length=0
  for k in pairs(ids) do assert(integer(k) and k>=1,"ROSTER_NOT_AN_ARRAY");length=length+1 end
  assert(length<=128,"ROSTER_TOO_LARGE") -- bounded candidate, not an engine slot definition
  local ordered,seen={},{}
  for i=1,length do
   local pid=ids[i];assert(integer(pid),"INVALID_OR_SPARSE_ROSTER")
   if not seen[pid] then seen[pid]=true;ordered[#ordered+1]=pid end
  end
  table.sort(ordered)
  local out={contextSource="GAMEPLAY_CANDIDATE",status="COMPLETE_ROSTER",current=seen,
   ordered=ordered,enabled={},disabled={},unknown={}}
  for _,pid in ipairs(ordered) do
   local success,e=pcall(readEligibility,pid)
   if not success or type(e)~="table" or e.player~=pid or e.contextSource~="GAMEPLAY_CANDIDATE" then
    out.unknown[pid]="QUALIFICATION_READER_FAILED_OR_MISMATCH"
   elseif e.status=="ENABLED" then out.enabled[#out.enabled+1]=pid
   elseif e.status=="DISABLED" then out.disabled[pid]=true
   else out.unknown[pid]=e.reason or "QUALIFICATION_UNKNOWN" end
  end
  return out
 end)
 if ok then return result end
 -- Never return a partially authorized list or retain earlier results on roster failure.
 return {contextSource="GAMEPLAY_CANDIDATE",status="UNKNOWN",reason=tostring(result),enabled={}}
end
function M.Classify(snapshot,pid)
 if not integer(pid) or type(snapshot)~="table" or snapshot.contextSource~="GAMEPLAY_CANDIDATE"
  or snapshot.status~="COMPLETE_ROSTER" then return "UNKNOWN" end
 if not snapshot.current[pid] then return "NOT_CURRENT" end
 if snapshot.disabled[pid] then return "DISABLED" end
 if snapshot.unknown[pid] then return "UNKNOWN" end
 for _,p in ipairs(snapshot.enabled) do if p==pid then return "ENABLED" end end
 return "UNKNOWN"
end
return M

end)()
local Life=(function()
-- Offline authorization lifecycle only. No engine events, writes, or effect removal.
local M={}
function M.New(collect,context)
 assert(context=="DEV_DIAGNOSTIC_ONLY" and type(collect)=="function","DIAGNOSTIC_ONLY")
 local epoch,ready,allowed,tickets=0,false,{},{}
 local S={}
 function S.Invalidate()
  epoch=epoch+1;ready=false;allowed={};tickets={}
  return epoch
 end
 function S.Refresh(phase)
  local attempt=S.Invalidate() -- old authorizations die BEFORE any external reads
  if phase~="AFTER_LOAD_CLOSE" then return {status="UNKNOWN",reason="NOT_READY_PHASE"} end
  local ok,s=pcall(collect)
  if attempt~=epoch then return {status="UNKNOWN",reason="SUPERSEDED_REFRESH"} end
  local valid,nextAllowed=pcall(function()
   assert(ok and type(s)=="table" and s.contextSource=="GAMEPLAY_CANDIDATE"
    and s.status=="COMPLETE_ROSTER","ROSTER_UNAVAILABLE")
   assert(type(s.enabled)=="table" and type(s.current)=="table"
    and type(s.disabled)=="table" and type(s.unknown)=="table","BAD_ROSTER")
   local out={};local n=0
   for k in pairs(s.enabled) do
    assert(type(k)=="number" and k>=1 and k%1==0,"BAD_ENABLED_ARRAY");n=n+1
   end
   for i=1,n do
    local p=s.enabled[i]
    assert(type(p)=="number" and p>=0 and p<math.huge and p%1==0 and s.current[p]==true
     and not s.disabled[p] and not s.unknown[p] and not out[p],"CONFLICTING_ELIGIBILITY")
    out[p]=true
   end
   return out
  end)
  if not valid then return {status="UNKNOWN",reason=tostring(nextAllowed)} end
  if attempt~=epoch then return {status="UNKNOWN",reason="SUPERSEDED_REFRESH"} end
  allowed=nextAllowed;ready=true
  return {status="READY_DIAGNOSTIC",epoch=epoch}
 end
 function S.Acquire(player)
  if not ready or not allowed[player] then return nil end
  local token={} -- private issuance registry, not mutable public epoch fields
  tickets[token]={player=player,epoch=epoch}
  return token
 end
 function S.Check(token,player)
  local receipt=tickets[token]
  return ready and receipt~=nil and receipt.player==player and receipt.epoch==epoch and allowed[player]==true
 end
 return S
end
return M

end)()
function SPCQualificationProbe.Start(P,shared)
 local env={Players=Players,PlayerConfigurations=PlayerConfigurations,GameInfo=GameInfo,PlayerManager=PlayerManager}
 local c=Carrier.New(env,"TRAIT_CIVILIZATION_SPC_TEST")
 local latest
 local function collect()
  env.Players=Players;env.PlayerConfigurations=PlayerConfigurations;env.GameInfo=GameInfo;env.PlayerManager=PlayerManager
  return Roster.Collect(env,c.Read)
 end
 local gate=Life.New(function() latest=collect();return latest end,"DEV_DIAGNOSTIC_ONLY")
 local data={version=P.VERSION,phase="INITIALIZE",hook="ABSENT"}
 shared.QualificationProbe=data
 local function ranges(ids)
  local out={};local first,last
  local function flush() if first~=nil then out[#out+1]=first==last and tostring(first) or (first.."-"..last) end end
  for _,v in ipairs(ids) do
   if last and v==last+1 then last=v else flush();first=v;last=v end
  end
  flush();return #out>0 and table.concat(out,",") or "(none)"
 end
 local function publish(phase,check)
  data.phase=phase;data.status=latest and latest.status or "UNKNOWN";data.permissions={}
  local ids=latest and latest.ordered or {}
  local permitted={};local unknown={}
  for _,pid in ipairs(ids) do
   local token=gate.Acquire(pid)
   data.permissions[pid]=token~=nil and gate.Check(token,pid) or false
   if data.permissions[pid] then permitted[#permitted+1]=pid end
   if latest.unknown[pid] then unknown[#unknown+1]=pid end
  end
  local absent,present={},{}
  if data.status=="COMPLETE_ROSTER" then
   for pid=54,61 do
    local target=latest.current[pid] and present or absent;target[#target+1]=pid
   end
  end
  data.text="phase="..phase.." hook="..data.hook.." roster="..data.status
   .."\n当前名单="..ranges(ids).." (count="..#ids..")"
   .."\n诊断获准="..ranges(permitted).." 未知="..ranges(unknown)
   .."\n54-61在名单内="..ranges(present).." 名单外="..ranges(absent)
   .."\n内部撤销/重取检查="..(check or "NOT_RUN")
   .."\n仅诊断许可；未接正式门控或游戏收益。"
  if data.status~="COMPLETE_ROSTER" then data.text=data.text.."\n"..tostring(latest and latest.reason) end
  print("[SPC]["..P.VERSION.."][QUALIFICATION] "..data.text)
 end
 latest=collect()
 local function onLoad()
  local ok,err=pcall(function()
   local first=gate.Refresh("AFTER_LOAD_CLOSE")
   local previous={};for _,pid in ipairs(latest and latest.enabled or {}) do previous[pid]=gate.Acquire(pid) end
   gate.Invalidate()
   local passed=true;local tested=0
   for pid,token in pairs(previous) do tested=tested+1;if gate.Check(token,pid) then passed=false end end
   local second=gate.Refresh("AFTER_LOAD_CLOSE")
   for pid,token in pairs(previous) do
    local fresh=gate.Acquire(pid)
    if gate.Check(token,pid) or not fresh or not gate.Check(fresh,pid) then passed=false end
   end
   local ready=first.status=="READY_DIAGNOSTIC" and second.status=="READY_DIAGNOSTIC"
   publish("LOAD_CLOSE",ready and tested>0 and (passed and "PASS" or "FAIL") or "NOT_PROVEN")
  end)
  if not ok then gate.Invalidate();latest={status="UNKNOWN",reason=tostring(err)};publish("LOAD_ERROR","NOT_PROVEN") end
 end
 local e=Events and Events.LoadScreenClose
 if e and type(e.Add)=="function" then
  local ok=pcall(e.Add,onLoad);data.hook=ok and "REGISTERED" or "ERROR"
 end
 publish("INITIALIZE")
 -- Only scalar diagnostics cross contexts. The private gate and tokens are not exported.
end
