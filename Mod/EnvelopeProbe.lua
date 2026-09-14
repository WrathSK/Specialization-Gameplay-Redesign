-- B019 finite synthetic fixture ONLY. No city APIs, production permits or yields.
-- Uses the same before/target/PENDING/DONE envelope contract as the offline model.
SPCEnvelopeProbe={}
local M=SPCEnvelopeProbe
local function equal(a,b,depth)
 depth=depth or 0
 if depth>12 or type(a)~=type(b) then return false end
 if type(a)~="table" then return a==b end
 for k,v in pairs(a) do if not equal(v,b[k],depth+1) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end;return true
end
function M.Expected(pid,step)
 if step==0 then return nil end
 local function facts(rev)
  return {schemaVersion=1,owner=pid,cityUID="DEV_B019",revision=rev,
   specialization=rev==0 and "NONE" or "RESEARCH",potential=rev==0 and 0 or 1,investments={}}
 end
 local op=step<=3 and 1 or 2
 local phase=(step-1)%3+1
 local before=op==2 and facts(0) or nil
 local target=facts(op-1)
 local actual=target;if phase==1 then actual=before end
 return {schema=1,kind="MOCK_CITY_ENVELOPE",owner=pid,cityUID="DEV_B019",storageRevision=step,
  facts=actual,
  record={schema=1,kind="MOCK_CITY_PENDING",state=phase==3 and "DONE" or "PENDING",
   operationID="B019-"..op,cityUID="DEV_B019",owner=pid,beforePresent=op==2,before=before,target=target}}
end
local names={ [0]="EMPTY", "BEFORE_PENDING", "TARGET_PENDING", "DONE", "BEFORE_PENDING", "TARGET_PENDING", "DONE" }
local chinese={ [0]="空白测试记录", "计划已记；成果未写", "成果已写；待对账", "对账完成", "第二笔计划已记", "第二笔成果已写；待对账", "两笔均已完成" }
function M.Start(P,shared)
 local data={version=P.VERSION,players={},ready=false,hook="ABSENT"};shared.EnvelopeProbe=data
 local function read(pid)
  local ok,v=pcall(function() return Game:GetProperty("SPC_DEV_ENVELOPE_B019_P"..pid) end)
  if not ok then return nil,"READ_ERROR" end
  for step=0,6 do if equal(v,M.Expected(pid,step)) then return step,v end end
  return nil,"INVALID_NO_OVERWRITE"
 end
 function data.Run(pid,action,expectedStep)
  if not P.IsTestPlayer(pid) then return "OUTSIDE_TEST_CIV" end
  local b=data.players[pid] or {attempts=0};data.players[pid]=b
  local step,old=read(pid);local outcome="READ_ONLY"
  if action=="ENVELOPE_NEXT" then
   if not data.ready then outcome="WAIT_LOAD_CLOSE"
   elseif b.busy or b.halted then outcome="SESSION_HELD"
   elseif step==nil then outcome="INVALID_NO_OVERWRITE"
   elseif type(expectedStep)~="number" or expectedStep~=step then outcome="STALE_NO_WRITE"
   elseif step==6 then outcome="COMPLETE_NO_WRITE"
   else
    b.busy=true
    local again,value=read(pid)
    if again~=step or not equal(value,old) then outcome="CHANGED_NO_WRITE";b.halted=true
    else
     b.attempts=b.attempts+1
     local ok=pcall(function() P.SetProperty(Game,"SPC_DEV_ENVELOPE_B019_P"..pid,M.Expected(pid,step+1)) end)
     local after=read(pid)
     if after==step+1 then outcome=ok and "SAVED_READBACK_MATCH" or "SAVED_AFTER_THROW"
     else outcome="WRITE_UNCONFIRMED_HELD";b.halted=true end
    end
    b.busy=false;step,old=read(pid)
   end
  end
  b.step=step;b.state=step and names[step] or old;b.outcome=outcome
  local phase=step and chinese[step] or "记录异常，禁止覆盖"
  b.text=table.concat({"B019 单表阶段="..tostring(step or "?").."/6 | "..tostring(b.state),
   phase.." | "..outcome,
   "本次加载写入="..b.attempts.." | 自动读档阶段="..tostring(b.autoStep or "NONE"),
   "load="..tostring(data.ready).." hook="..data.hook.." | 合成编号DEV_B019",
   "仅测试表；Next明确推进一阶段；读档不自动写入。"},"\n")
  print("[SPC][B019][ENVELOPE] "..b.text);return b.text
 end
 local function onLoad()
  data.ready=true
  local ok,ids=pcall(function() return PlayerManager.GetAliveIDs() end)
  if not ok or type(ids)~="table" then data.loadError="ROSTER_UNAVAILABLE";print("[SPC][B019] ROSTER_UNAVAILABLE");return end
  for _,pid in ipairs(ids) do
   if P.IsTestPlayer(pid) then
    data.Run(pid,"ENVELOPE_READ")
    data.players[pid].autoStep=data.players[pid].step
    data.Run(pid,"ENVELOPE_READ")
   end
  end
 end
 if Events and Events.LoadScreenClose and Events.LoadScreenClose.Add then
  local ok=pcall(function() Events.LoadScreenClose.Add(onLoad) end)
  data.hook=ok and "REGISTERED" or "REGISTER_FAILED"
 end
end
