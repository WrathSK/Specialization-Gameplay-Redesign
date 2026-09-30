-- B069: fixed schema, scalar counters only. No automatic disk/print sink.
SPCPerformance={}
local M=SPCPerformance
local names={'unit_cb','unit_ignored','revalidate','route_scan','publication','same_snapshot','derive','facts','city_scan','district_scan','building_check','building_create','building_remove','property_write','net_send','net_receive','audit_lv3','audit_boost','audit_standard','audit_commerce','audit_copy','busy_skip','send_duplicate','send_inflight','send_timeout','route_failure','confirmed_invalid','manual_snapshot','fact_change','input_duplicate','input_publication','withdrawal','revalidate_same','stale_input','derive_requested','derive_executed','derived_cache_hit','derived_cache_miss','input_version_change','derived_invalidation','discount_attempt','discount_send','discount_pending','discount_ack','discount_retry','discount_timeout','discount_receive','discount_duplicate','discount_stale','discount_apply','discount_withdraw','discount_dirty_mark','discount_direct_refresh','discount_reconcile','discount_skipped_clean','discount_fact_capture','discount_city_processed','discount_ui_scan'}
for _,k in ipairs({'copy','industry','cross'}) do
 for _,n in ipairs({'attempt','send','receive','pending','retry','stale','apply','withdraw','duplicate','timeout'}) do names[#names+1]=k..'_'..n end
end
for _,n in ipairs({'read','capture','hit','dirty','publish','failure'}) do names[#names+1]='dc_'..n end
function M.New()
 local s={schema=1,turn=Game.GetCurrentGameTurn(),startTurn=Game.GetCurrentGameTurn(),entries={},inflight=0,peakInflight=0,revision=0,routes=0,enabled=true}
 for _,n in ipairs(names) do s.entries[n]={current=0,total=0,previous=0,peak=0} end
 return s
end
function M.Count(n,amount)
 local s=ExposedMembers and ExposedMembers.SPC_Performance
 if not s or not s.enabled then return end
 local e=s.entries[n];if not e then return end
 local t=Game.GetCurrentGameTurn()
 if t~=s.turn then
  for _,v in pairs(s.entries) do v.previous=v.current;v.peak=math.max(v.peak,v.current);v.current=0 end
  s.turn=t
 end
 amount=amount or 1;e.current=e.current+amount;e.total=e.total+amount
end
function M.Flight(n)
 local s=ExposedMembers and ExposedMembers.SPC_Performance
 if s then s.inflight=n;s.peakInflight=math.max(s.peakInflight,n) end
end
function M.Describe(detailed)
 M.Count('manual_snapshot',0)
 local s=ExposedMembers and ExposedMembers.SPC_Performance
 if not s then return 'Performance counters not initialized' end
 local lines={'B069 performance | turn='..s.turn..' | start='..s.startTurn,
  'Current / Total (direct Lua engine calls; native Modifier Property writes not observable)',
  'revision='..s.revision..' routes='..s.routes..' inflight='..s.inflight..' peak='..s.peakInflight}
 local groups={{'unit_cb','unit_ignored'},{'revalidate','route_scan'},{'publication','same_snapshot'},
 {'derive','facts'},{'city_scan','district_scan'},{'building_check','building_create','building_remove'},
 {'property_write','net_send','net_receive'},{'audit_lv3','audit_boost','audit_standard'},
 {'audit_commerce','audit_copy'},{'busy_skip','send_duplicate','send_inflight','send_timeout'},
 {'route_failure','confirmed_invalid'},{'fact_change','input_duplicate','input_publication'},{'withdrawal','revalidate_same','stale_input'},{'derive_requested','derive_executed'},{'derived_cache_hit','derived_cache_miss'},{'input_version_change','derived_invalidation'},{'discount_attempt','discount_send','discount_pending'},{'discount_ack','discount_retry','discount_timeout'},{'discount_receive','discount_duplicate','discount_stale'},{'discount_apply','discount_withdraw'},{'discount_dirty_mark','discount_direct_refresh','discount_reconcile'},{'discount_skipped_clean','discount_fact_capture','discount_city_processed','discount_ui_scan'}}
 for _,k in ipairs({'copy','industry','cross'}) do
  groups[#groups+1]={k..'_attempt',k..'_send',k..'_receive',k..'_pending'}
  groups[#groups+1]={k..'_retry',k..'_stale',k..'_apply',k..'_withdraw',k..'_duplicate',k..'_timeout'}
 end
 for _,g in ipairs(groups) do local a={};for _,n in ipairs(g) do local e=s.entries[n];a[#a+1]=n..'='..e.current..'/'..e.total end;lines[#lines+1]=table.concat(a,'  ') end
 local dc={};for _,n in ipairs({'read','capture','hit','dirty','publish','failure'}) do local e=s.entries['dc_'..n];dc[#dc+1]='dc_'..n..'='..e.current..'/'..e.total end;lines[#lines+1]=table.concat(dc,'  ')
 local audit=ExposedMembers.SPC_RuntimeAudit
 lines[#lines+1]='Runtime audit='..(audit and audit.state or 'NOT_INITIALIZED')..' | '..(audit and audit.reason or '')
 if audit and audit.sink then lines[#lines+1]='Audit file='..audit.sink.path..' | rows='..tostring(audit.rows) end
 if detailed then
  lines[#lines+1]='schema=1; auto_log='..(audit and audit.state=='ACTIVE' and 'ACTIVE' or 'DISABLED')..'; format=TSV; retention=8 x 4MiB'
  for _,n in ipairs(names) do local e=s.entries[n];lines[#lines+1]=n..' previous='..e.previous..' peak='..math.max(e.peak,e.current) end
 end
 return table.concat(lines,'\n')
end

-- Fixed-schema attribution, shared across invocation sites; only armed by the reader.
local auditLabels={
 Lv2Housing='住房',Lv2GPP='GPP',ResearchInfrastructure='科研基建',ResearchCross='跨学科',
 ResearchApply='学以致用',ResearchChair='学术主持',ResearchSupport='专家支持',
 IndustrySupport='工业支持',Lv3Effects='旧三级',Lv4Percent='旧四级',
 CommerceConvergence='旧商业汇聚',CopyYields='复制收益',StandardizationDiscount='工业折扣',
 NetworkBoost='旧网络',Dialogue='对话'}
local dispatchLabels={
 PlayerTurnActivated='回合',CityWorkerChanged='工人',CityFocusChanged='焦点',
 GovernorAssigned='总督指派',GovernorEstablished='总督就位',GovernorChanged='总督变化',GovernorPromoted='总督晋升',
 BuildingAddedToMap='建筑加入',BuildingRemovedFromMap='建筑移除',BuildingPillaged='建筑掠夺',BuildingRepaired='建筑修复',
 DistrictRemovedFromMap='区域移除',DistrictBuildProgressChanged='区域进度',DistrictPillaged='区域掠夺',DistrictRepaired='区域修复',
 CityTransfered='易主',CityRemovedFromMap='城市移除',CityPopulationChanged='人口',
 CityProductionCompleted='生产完成',CityTileOwnershipChanged='地块归属',GovernmentPolicyChanged='政策',
 GovernmentChanged='政体',ResearchCompleted='科技',CivicCompleted='市政',LoadScreenClose='加载',
 CityBuilt='建城',OnBuildingConstructed='建筑建成',OnDistrictConstructed='区域建成'}
local uiLabels={}
for _,name in ipairs({'worker','focus','governor','turn','load'}) do
 for _,owner in ipairs({'local','foreign','unknown'}) do uiLabels[name..'_'..owner]=true end
end
for _,k in ipairs({'send','sent','failed','received'}) do uiLabels[k]=true end
local schemas={audit=auditLabels,dispatch=dispatchLabels,ui=uiLabels}
local function attribution()
 local a=ExposedMembers and ExposedMembers.SPC_MemoryAttribution
 if not a or not a.active then return nil end
 if Game.GetCurrentGameTurn()>=a.startTurn+6 then a.active=false;return nil end
 return a
end
function M.Observe(group,key)
 local a=attribution()
 if not a or not schemas[group] or not schemas[group][key] then return end
 local counts=a[group];counts[key]=counts[key]+1
end
local function armAttribution()
 local a={active=true,startTurn=Game.GetCurrentGameTurn()}
 for group,keys in pairs(schemas) do a[group]={};for key in pairs(keys) do a[group][key]=0 end end
 ExposedMembers.SPC_MemoryAttribution=a
end
local function top(counts,labels,limit)
 local rows={}
 for k,n in pairs(counts) do if n>0 then rows[#rows+1]={key=k,n=n} end end
 table.sort(rows,function(a,b)return a.n>b.n or a.n==b.n and a.key<b.key end)
 local out={}
 for i=1,math.min(limit,#rows) do local row=rows[i];out[#out+1]=labels[row.key]..' '..row.n end
 return #out>0 and table.concat(out,' / ') or '无'
end

-- Opt-in count observation and B138 session-only controlled GC trial; no save state.
 function M.Heap()
  if type(collectgarbage)~='function' then return nil end
  local ok,n=pcall(collectgarbage,'count')
  if ok and type(n)=='number' and n==n and n>=0 and n<math.huge then return n/1024 end -- MiB reported at this call site; engine heap sharing is unproven
 end
function M.StartMemory(P,shared)
 local d={};shared.MemoryObservation=d
 ExposedMembers.SPC_MemoryAttribution=nil -- new observer/session; never restore old samples

 -- B138 reversible trial: one session-owned coordinator, never a save authority.
 local policy={growthMiB=128,minTurns=2,maxSeconds=2,rows=8,logRows=24}
 local a={enabled=true,collections=0,reason='WAIT_LOAD',rows={}}
 d.AutoGC=a -- scalar/read-only UI status plus a bounded result ring
 local loaded=false;local anchor;local lastTurn;local pendingTurn;local assessedTurn
 local gcBusy=false;local lastToken;local switchToken;local logRows=0
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
  local p=ExposedMembers.SPC_Performance
  if p and (p.inflight or 0)>0 then return false,'NETWORK_INFLIGHT' end
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
   '增长128 MiB + 间隔2回合；本地回合进入后发布边界评估。',
   '最近状态 '..a.reason..'｜本次加载调用 '..a.collections..' 次｜Lua '..tostring(_VERSION)}
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
 local hooks={'LoadScreenClose','PlayerTurnActivated','PlayerTurnDeactivated','GameCoreEventPublishComplete'}
 local callbacks={
  function()
   if not current() or loaded then return end
   loaded=true;lastTurn=Game.GetCurrentGameTurn();anchor=M.Heap()
   if not anchor then fail('LOAD_COUNT_UNAVAILABLE')
   elseif not a.failure then log('LOAD_BASELINE_128MiB_2T_2s',{before=anchor}) end
  end,
  function(pid)
   if not current()then return end
   pendingTurn=nil
   if loaded and a.enabled and not a.failure and localHuman(pid)then pendingTurn=Game.GetCurrentGameTurn() end
  end,
  function()if current()then pendingTurn=nil end end,
  function()
   if not current() or not pendingTurn or gcBusy then return end
   local t=pendingTurn;pendingTurn=nil -- no retry loop / reentrant publish / repeated sampling
   if t~=Game.GetCurrentGameTurn() or assessedTurn==t or not a.enabled or a.failure then return end
   assessedTurn=t
   local ok,pid=pcall(Game.GetLocalPlayer)
   if not ok or not localHuman(pid)then return end
   local safe,why=idle(pid)
   if not safe then log('SKIP:'..why);return end
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
 local armed=false;local player;local startTurn;local baseline;local rows={};local pending;local seen={}
 local keys={'city_scan','district_scan','facts','building_check','building_create','building_remove','property_write','derive_executed','dc_read','dc_capture','dc_hit','dc_dirty'}
 local function size(t)local n=0;for _ in pairs(t or {})do n=n+1 end;return n end
 local function snapshot(label)
  local heap=M.Heap();local c=ExposedMembers.SPC_Performance;local totals={}
  for _,k in ipairs(keys)do totals[k]=c and c.entries[k] and c.entries[k].total or 0 end
  baseline=baseline or totals
  local row={label=label,turn=Game.GetCurrentGameTurn(),heap=heap,totals=totals}
  rows[#rows+1]=row;if #rows>6 then table.remove(rows,1)end
 end
 local labels={city_scan='城市扫描',district_scan='区域扫描',facts='事实读取',building_check='建筑检查',building_create='建载体',building_remove='拆载体',property_write='属性写入',derive_executed='网络派生'}
 function d.Read(pid,begin)
  if not P.IsTestPlayer(pid)then return '仅本地人类玩家可观测' end
  if begin then armAttribution();armed=true;player=pid;startTurn=Game.GetCurrentGameTurn();baseline=nil;rows={};seen={};pending=nil;snapshot('开始')
  elseif not baseline then return '左键开始一次观测；右键读取。不修改游戏状态。'
  else snapshot('手动读取')end
  attribution();local attr=ExposedMembers.SPC_MemoryAttribution
  if attr and not attr.active then armed=false;pending=nil end
  local lines={'内存观测 | '..(armed and '运行中（最多6回合）' or '已停止')..' | 仅本次加载',
   'Gameplay调用处 Lua MiB；非本Mod独占，不等于进程内存。'}
  for _,v in ipairs(rows)do lines[#lines+1]='T'..v.turn..' '..v.label..'：'..(v.heap and string.format('%.2f MiB',v.heap) or '不可用')end
  local last=rows[#rows];local values={}
  for _,k in ipairs(keys)do if labels[k] then values[#values+1]=labels[k]..' '..(last.totals[k]-baseline[k]) end end
  lines[#lines+1]='开始以来：'..table.concat(values,' / ')
  local dc=shared.DistrictCompleteness;local net=shared.NetworkBridge;local claim=shared.ClaimProjects;local store=shared.CityProgressionStore
  lines[#lines+1]='当前缓存条目：D '..(dc and dc.CacheSize() or 0)..' / 网络玩家 '..size(net and net.players)..' / 认领视图 '..size(claim and claim.views)..' / 确认 '..size(claim and claim.syncAck)..' / 城市记录 '..(store and store.RecordCount() or 0)
  local function delta(k)return last.totals[k]-baseline[k]end
  lines[#lines+1]='D缓存：读取 '..delta('dc_read')..' / 重建 '..delta('dc_capture')..' / 命中 '..delta('dc_hit')..' / 标脏 '..delta('dc_dirty')
  if attr then
   lines[#lines+1]='核对调用最多6项（含早退；非耗时/字节）：'
   lines[#lines+1]=top(attr.audit,auditLabels,6)
   lines[#lines+1]='事件派发最多3项（逐回调计数）：'..top(attr.dispatch,dispatchLabels,3)
   local u=attr.ui
   lines[#lines+1]='UI事件 本人/其它/未知：工人 '..u.worker_local..'/'..u.worker_foreign..'/'..u.worker_unknown..'；焦点 '..u.focus_local..'/'..u.focus_foreign..'/'..u.focus_unknown
   lines[#lines+1]='UI总督 '..u.governor_local..'/'..u.governor_foreign..'/'..u.governor_unknown..'；回合 '..u.turn_local..'/'..u.turn_foreign..'/'..u.turn_unknown..'；加载 '..u.load_unknown
   lines[#lines+1]='GPP刷新：请求 '..u.send..' / 已提交 '..u.sent..' / 异常 '..u.failed..' / 已接收 '..u.received
  end
  lines[#lines+1]='此计数观测不触发GC；自动试运行另看GC报告。调用量不等于内存归因。'
  return table.concat(lines,'\n')
 end
 local function event(label,pid)
  if not armed or pid~=player then return end
  local t=Game.GetCurrentGameTurn()
  if t>=startTurn+6 then armed=false;pending=nil;return end
  if label~='转移' and seen[label]==t then return end
  seen[label]=t;snapshot(label);pending='发布后'
 end
 for _,v in ipairs({{'PlayerTurnDeactivated','回合离开'},{'PlayerTurnActivated','回合进入'}})do
  local label=v[2];local e=P.Field(Events,v[1]);if e and type(e.Add)=='function' then pcall(e.Add,function(pid)event(label,pid)end)end
 end
 local transfer=P.Field(Events,'CityTransfered');if transfer and type(transfer.Add)=='function' then pcall(transfer.Add,function(newOwner,id,oldOwner)
  if armed and (newOwner==player or oldOwner==player)then event('转移',player)end
 end)end
 local publish=P.Field(Events,'GameCoreEventPublishComplete');if publish and type(publish.Add)=='function' then pcall(publish.Add,function()
  if armed and pending then local label=pending;pending=nil;snapshot(label)end
 end)end
end
