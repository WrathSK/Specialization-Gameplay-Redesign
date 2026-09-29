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

-- Opt-in six-turn count-only observation. Manual full-GC below has no event hook or save state.
 function M.Heap()
  if type(collectgarbage)~='function' then return nil end
  local ok,n=pcall(collectgarbage,'count')
  if ok and type(n)=='number' and n==n and n>=0 and n<math.huge then return n/1024 end -- MiB reported at this call site; engine heap sharing is unproven
 end
function M.StartMemory(P,shared)
 local d={};shared.MemoryObservation=d
 ExposedMembers.SPC_MemoryAttribution=nil -- new observer/session; never restore old samples

 -- B134 diagnostic only: one explicit UI request, one protected full-cycle call.
 -- Do not stop/restart GC, tune its parameters, clear caches or write any Property.
 local gcRows={};local gcFailure;local lastGCToken;local lastGCReport;local gcBusy=false
 local function running()
  if type(collectgarbage)~='function' then return nil end
  local ok,v=pcall(collectgarbage,'isrunning');if ok and type(v)=='boolean' then return v end
 end
 local function cpuTime()
  if not os or type(os.clock)~='function' then return nil end
  local ok,v=pcall(os.clock);if ok and type(v)=='number' and v==v and v>=0 and v<math.huge then return v end
 end
 local function state(v)if v==nil then return '未知' end;return v and '运行' or '停止' end
 function d.ReadGC(pid)
  if not P.IsTestPlayer(pid)then return '仅本地人类玩家可诊断' end
  local lines={'手动GC诊断 | Lua环境 '..tostring(_VERSION)..' | 本次加载最近3次',
   'Gameplay调用处整个Lua堆；非本Mod独占，不等于进程内存。'}
  if #gcRows==0 then lines[#lines+1]='默认关闭。右键此按钮明确执行一次完整GC；左键仅看结果。' end
  for _,v in ipairs(gcRows)do
   lines[#lines+1]='T'..v.turn..' '..v.status..'：'..(v.before and string.format('%.2f',v.before) or '?')..' → '..(v.after and string.format('%.2f',v.after) or '?')..' MiB'
   lines[#lines+1]='GC状态 '..state(v.runningBefore)..' → '..state(v.runningAfter)..'；CPU耗时 '..(v.cpu and string.format('%.3f秒',v.cpu) or '不可用')
  end
  if gcFailure then lines[#lines+1]='本次加载停止再次尝试：'..gcFailure end
  lines[#lines+1]='无回合/每帧自动GC；不清属性/账本/缓存。可能短暂停顿。'
  lines[#lines+1]='比较初始稳定点及随后2回合的回收后基线；首次初始化/终结处理可能影响读数。'
  return table.concat(lines,'\n')
 end
 function d.CollectGC(pid,token)
  if not P.IsTestPlayer(pid)then return '仅本地人类玩家可诊断' end
  if type(token)~='string' or #token==0 or #token>100 then return 'GC请求标识无效；未执行' end
  if token==lastGCToken then return lastGCReport or 'GC请求处理中；不会重复执行' end
  if gcBusy then return 'GC请求处理中；不会重复执行' end
  if gcFailure then return d.ReadGC(pid) end
  local v={turn=Game.GetCurrentGameTurn(),status='未执行'} -- allocate report row before sample
  v.runningBefore=running();v.before=M.Heap()
  if v.before==nil then
   gcFailure='count接口不可用，无法建立前后比较；转入定域对照调查。'
  else
   gcBusy=true;lastGCToken=token
   local started=cpuTime()
   local ok,err=pcall(collectgarbage,'collect')
   local finished=cpuTime()
   v.after=M.Heap();v.runningAfter=running();gcBusy=false
   v.status=ok and '完整GC调用成功' or '完整GC调用失败'
   if started and finished and finished>=started then v.cpu=finished-started end
   if not ok then gcFailure='collect不可用/失败：'..(type(err)=='string' and err:sub(1,160) or type(err))
   elseif v.after==nil then gcFailure='回收后count不可用。'
   elseif v.runningBefore~=nil and v.runningAfter~=nil and v.runningBefore~=v.runningAfter then
    gcFailure='GC运行状态改变；停止诊断并调查，不自动恢复或调参。'
   end
  end
  gcRows[#gcRows+1]=v;if #gcRows>3 then table.remove(gcRows,1)end
  lastGCReport=d.ReadGC(pid);return lastGCReport
 end
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
  lines[#lines+1]='此观测不执行GC；手动GC另看专用报告。调用量不等于内存归因。'
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
  local label=v[2];local e=P.Field(Events,v[1]);if e and e.Add then e.Add(function(pid)event(label,pid)end)end
 end
 local transfer=P.Field(Events,'CityTransfered');if transfer and transfer.Add then transfer.Add(function(newOwner,id,oldOwner)
  if armed and (newOwner==player or oldOwner==player)then event('转移',player)end
 end)end
 local publish=P.Field(Events,'GameCoreEventPublishComplete');if publish and publish.Add then publish.Add(function()
  if armed and pending then local label=pending;pending=nil;snapshot(label)end
 end)end
end
