-- The existing GC control and its calling-context heap trust latch.
SPCRuntimeGC={}
local M=SPCRuntimeGC
-- B270: native count uses a signed low-32-bit byte counter on the observed Mac.
-- Preserve raw KB/status; a negative observation invalidates this context's later
-- low positive values. Never infer missing 4-GiB multiples or force a collection.
local heapRangeUnsafe=false
function M.ReadHeap()
 if type(collectgarbage)~='function' then return nil,'UNAVAILABLE' end
 local ok,n=pcall(collectgarbage,'count')
 if not ok then return nil,'CALL_FAILED' end
 if type(n)~='number' then return nil,'NON_NUMERIC' end
 if n~=n or n==math.huge or n==-math.huge then return nil,'NONFINITE' end
 if n<0 then heapRangeUnsafe=true;return nil,'NATIVE_NEGATIVE',n end
 if heapRangeUnsafe then return nil,'RANGE_UNTRUSTED',n end
 return n/1024,'OK',n -- calling Gameplay heap, not Mod-exclusive/all Lua
end
function M.Heap() local n=M.ReadHeap();return n end
function M.Start(P,shared,prepareObserver)
 heapRangeUnsafe=false -- a fresh Gameplay observer; no saved/readback value restores trust
 local d={};shared.MemoryObservation=d
 shared.MemoryEvidence=nil
 ExposedMembers.SPC_MemoryAttribution=nil -- new observer/session; never restore old samples

 -- B138 reversible trial: one session-owned coordinator, never a save authority.
 local policy={growthMiB=128,minTurns=2,maxSeconds=2,rows=8,logRows=24}
 local a={enabled=true,collections=0,reason='WAIT_LOAD',rows={}}
 d.AutoGC=a -- scalar/read-only UI status plus a bounded result ring
 local publishEvidence,attachObserver
 if type(prepareObserver)=='function'then
  local ok,publish,attach=pcall(prepareObserver,P,shared,d,M.Heap)
  if ok then publishEvidence,attachObserver=publish,attach end
 end
 local function record(kind,reason,extra)
  if shared.MemoryObservation~=d then return end
  -- These existing heap reads can invalidate trust even without a log sink.
  pcall(function()
   local heap,status,raw=M.ReadHeap()
   if publishEvidence then publishEvidence(kind,reason,heap,status,raw,extra)end
  end)
 end
 local boundaries={}
 local function boundary(kind,pid)
  local ok,id=pcall(Game.GetLocalPlayer)
  if not ok or (pid~=nil and pid~=id) or not P.IsTestPlayer(id) then return end
  local t=Game.GetCurrentGameTurn()
  if boundaries[kind]==t then return end
  boundaries[kind]=t
  record(kind,'BOUNDARY')
 end
 for _,item in ipairs({{'LoadScreenClose','LOAD'},{'PlayerTurnActivated','TURN_BEGIN'},{'PlayerTurnDeactivated','TURN_END'}})do
  local event=P.Field(Events,item[1]);local kind=item[2]
  if event and type(event.Add)=='function' then
   pcall(event.Add,function(pid) if shared.MemoryObservation==d then pcall(boundary,kind,kind=='LOAD' and nil or pid) end end)
  end
 end
 local loaded=false;local anchor;local lastTurn;local pendingTurn;local assessedTurn
 local gcBusy=false;local lastToken;local switchToken;local logRows=0
 local waitingNetwork=false;local retryUsed=false
 local function current()return shared.MemoryObservation==d end
 local function localHuman(pid)
  local ok,id=pcall(Game.GetLocalPlayer)
  return current() and ok and id==pid and P.IsTestPlayer(pid)
 end
 local function finite(v)return type(v)=='number' and v==v and v>=0 and v<math.huge end
 local function clock(key)
  if not os or type(os[key])~='function' then return nil end
  local ok,v=pcall(os[key]);if ok and finite(v)then return v end
 end
 local function running()
  if type(collectgarbage)~='function' then return nil end
  local ok,v=pcall(collectgarbage,'isrunning');if ok and type(v)=='boolean' then return v end
 end
 local function number(v)return v and string.format('%.2f',v) or '?' end
 local function log(reason,row)
  a.reason=reason
  record('GC',reason,row) -- retained even after the human-readable print budget
  if logRows>=policy.logRows then return end
  logRows=logRows+1
  local line='[SPC][GC_TRIAL] T'..Game.GetCurrentGameTurn()..' '..reason
  if row then line=line..' beforeMiB='..number(row.before)..' afterMiB='..number(row.after)..' cpuSec='..number(row.cpu)..' wallSec='..number(row.wall) end
  if logRows==policy.logRows then line=line..' LOG_LIMIT; panel retains last8; no more session log rows' end
  print(line)
 end
 local function fail(reason)
  a.failure=reason;a.enabled=false;pendingTurn=nil;log('STOP:'..reason)
 end
 local function idle(pid)
  if (shared.RequestDepth or 0)>0 then return false,'REQUEST_INFLIGHT' end
  if shared.NetworkIsolation and shared.NetworkIsolation.active then return false,'NETWORK_ISOLATED' end
  local claim=shared.ClaimProjects
  if claim and claim.IsBusy and claim.IsBusy()then return false,'CLAIM_BUSY' end
  local net=shared.NetworkBridge
  if not net or not net.ready then return false,'NETWORK_NOT_READY' end
  local b=net.players and net.players[pid]
  if b and b.refreshing then return false,'NETWORK_REFRESHING' end
  if ExposedMembers.SPC_NetworkRequestInFlight==true then return false,'NETWORK_INFLIGHT' end
  -- Module public busy flags only; this is not proof that every native transaction ended.
  for key,m in pairs(shared)do if type(m)=='table' and m.busy then return false,'MODULE_BUSY:'..key end end
  local routes=ExposedMembers.SPC_P0_BackgroundRoutes
  if routes and routes.awaitingNetwork then return false,'ROUTES_PENDING' end
  for _,key in ipairs({'SPC_CopyBackground','SPC_IndustryBackground','SPC_ResearchCrossBackground','SPC_DiscountEligibility'})do
   local u=ExposedMembers[key]
   if u and u.pending and u.pending~=0 then return false,'UI_PENDING:'..key end
  end
  return true
 end
 local function collect(reason)
  if gcBusy or a.failure then return end
  gcBusy=true;pendingTurn=nil
  local v={turn=Game.GetCurrentGameTurn(),reason=reason}
  v.before=M.Heap();v.runningBefore=running()
  local started=clock('clock');local wallStarted=clock('time')
  if v.before==nil then fail('COUNT_UNAVAILABLE')
  elseif v.runningBefore==false then fail('ENGINE_GC_STOPPED')
  elseif not started then fail('CPU_CLOCK_UNAVAILABLE')
  else
   lastTurn=v.turn -- consume attempt before a potentially reentrant native call
   local ok,err=pcall(collectgarbage,'collect') -- the only full-collection primitive
   local finished=clock('clock');local wallFinished=clock('time')
   v.after=M.Heap();v.runningAfter=running()
   if finished and finished>=started then v.cpu=finished-started end
   if wallStarted and wallFinished and wallFinished>=wallStarted then v.wall=wallFinished-wallStarted end
   v.status=ok and 'COLLECTED' or 'FAILED'
   a.collections=a.collections+1
   a.rows[#a.rows+1]=v;if #a.rows>policy.rows then table.remove(a.rows,1)end
   anchor=v.after
   log(reason,v)
   if not ok then fail('COLLECT_FAILED:'..tostring(err):sub(1,120):gsub('[\r\n]',' '))
   elseif not v.after then fail('POST_COUNT_UNAVAILABLE')
   elseif v.runningAfter==false or (v.runningBefore~=nil and v.runningAfter~=nil and v.runningBefore~=v.runningAfter)then fail('ENGINE_GC_STATE_CHANGED')
   elseif not v.cpu or (wallStarted and not v.wall)then fail('CLOCK_INVALID')
   elseif v.cpu>policy.maxSeconds or (v.wall and v.wall>policy.maxSeconds)then fail('OVER_2_SECONDS') end
  end
  gcBusy=false
 end
 function d.ReadGC(pid)
  if not localHuman(pid)then return '仅本地人类玩家可诊断' end
  local lines={'GC试运行｜'..(a.failure and '已停用：'..a.failure or a.enabled and '自动开启' or '手动关闭'),
   '增长128 MiB + 间隔2回合；发布边界评估，网络及界面请求结束后最多补评估一次。',
   '最近状态 '..a.reason..'｜本次加载调用 '..a.collections..' 次｜Lua '..tostring(_VERSION)}
  lines[#lines+1]='起点 '..tostring(a.baselineSource or '尚未取得')..' / T'..tostring(a.baselineTurn or '?')
  for _,v in ipairs(a.rows)do
   lines[#lines+1]='T'..v.turn..' '..v.reason..' '..v.status..'：'..number(v.before)..' → '..number(v.after)..' MiB；CPU '..number(v.cpu)..'s / 时钟 '..number(v.wall)..'s'
  end
  lines[#lines+1]='左键只读；右键开关（仅本次加载）。失败/耗时>2秒锁定停用；不能中断已开始的调用。'
  lines[#lines+1]='Gameplay调用处整个Lua堆，非本Mod独占/进程内存；时钟可能粗粒度。无属性/账本清理或GC调参。'
  return table.concat(lines,'\n')
 end
 function d.SetAutoGC(pid,enabled,token)
  if not localHuman(pid)then return '仅本地人类玩家可诊断' end
  if type(enabled)~='boolean' or type(token)~='string' or #token==0 or #token>100 then return 'GC开关请求无效' end
  if switchToken==token then return d.ReadGC(pid) end
  switchToken=token;pendingTurn=nil
  if not a.failure then a.enabled=enabled;log(enabled and 'ENABLED_WAIT_NEXT_TURN' or 'DISABLED_BY_USER') end
  return d.ReadGC(pid)
 end
 function d.CollectGC(pid,token)
  if not localHuman(pid)then return '仅本地人类玩家可诊断' end
  if type(token)~='string' or #token==0 or #token>100 then return 'GC请求标识无效；未执行' end
  if token==lastToken or gcBusy or a.failure then return d.ReadGC(pid) end
  lastToken=token
  -- Retained explicit diagnostic API shares the coordinator/cooldown; not the trial UI button.
  if loaded and Game.GetCurrentGameTurn()-lastTurn>=policy.minTurns then collect('MANUAL') end
  return d.ReadGC(pid)
 end
 -- B139: LoadScreenClose may not reach this late-installed Gameplay observer.
 -- First eligible local activation is a count-only fallback, never a collection.
 -- A delayed/repeated load notification cannot reset the baseline or cooldown.
 local function baseline(source)
  if not current() or loaded or a.failure then return end
  loaded=true;lastTurn=Game.GetCurrentGameTurn();anchor=M.Heap()
  a.baselineSource=source;a.baselineTurn=lastTurn
  if not anchor then fail('LOAD_COUNT_UNAVAILABLE')
  else log(source..'_BASELINE_128MiB_2T_2s',{before=anchor}) end
 end
 local hooks={'LoadScreenClose','PlayerTurnActivated','PlayerTurnDeactivated','GameCoreEventPublishComplete'}
 local callbacks={
  function()
   baseline('LOAD')
  end,
  function(pid)
   if not current()then return end
   if not localHuman(pid)then pendingTurn=nil;waitingNetwork=false;return end
   -- Repeated local activation must not create another attempt in this same turn.
   if assessedTurn==Game.GetCurrentGameTurn() then return end
   pendingTurn=nil;waitingNetwork=false;retryUsed=false
   if a.enabled and not a.failure and localHuman(pid)then
    if not loaded then baseline('LOCAL_TURN');return end
    pendingTurn=Game.GetCurrentGameTurn()
   end
  end,
  function()if current()then pendingTurn=nil;waitingNetwork=false end end,
  function()
   if not current() or not pendingTurn or gcBusy then return end
   local t=pendingTurn
   if t~=Game.GetCurrentGameTurn() or not a.enabled or a.failure then pendingTurn=nil;return end
   if waitingNetwork then
    if ExposedMembers.SPC_NetworkRequestInFlight==true then return end -- scalar-only wait, no heap/log spam
    -- The same deferred safety window may include several concurrent UI requests.
    for _,key in ipairs({'SPC_CopyBackground','SPC_IndustryBackground','SPC_ResearchCrossBackground','SPC_DiscountEligibility'})do
     local ui=ExposedMembers[key];if ui and ui.pending and ui.pending~=0 then return end
    end
    waitingNetwork=false;retryUsed=true
   elseif assessedTurn==t then pendingTurn=nil;return end
   assessedTurn=t;pendingTurn=nil -- consume this attempt before idle/native reentry
   local ok,pid=pcall(Game.GetLocalPlayer)
   if not ok or not localHuman(pid)then return end
   local safe,why=idle(pid)
   if not safe then
    if (why=='NETWORK_INFLIGHT' or why:match('^UI_PENDING:')) and not retryUsed then waitingNetwork=true;pendingTurn=t end
    log('SKIP:'..why);return
   end
   if t-lastTurn<policy.minTurns then log('INTERVAL');return end
   local now=M.Heap()
   if not now then fail('COUNT_UNAVAILABLE');return end
   if now-anchor<policy.growthMiB then log('BELOW_THRESHOLD',{before=now});return end
   collect('AUTO_GROWTH')
  end}
 local function installGC()
 for _,name in ipairs(hooks)do local e=P.Field(Events,name)
  if not e or type(e.Add)~='function' then fail('HOOK_UNAVAILABLE:'..name);return end
 end
 for i,name in ipairs(hooks)do
  local ok=pcall(Events[name].Add,function(...)
   if not current() or a.failure then return end
   local success,err=pcall(callbacks[i],...)
   if not success then gcBusy=false;fail('CALLBACK_FAILED:'..tostring(err):sub(1,120):gsub('[\r\n]',' ')) end
  end)
  if not ok then fail('HOOK_REGISTRATION_FAILED:'..name);return end
 end
 end
 installGC() -- missing GC capability must not remove the existing count-only observer
 if type(attachObserver)=='function'then pcall(attachObserver)end
end
