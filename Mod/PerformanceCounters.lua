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

-- Opt-in, six-turn observation. Fixed six-row ring; no saves, GC control or effects.
 function M.Heap()
  if type(collectgarbage)~='function' then return nil end
  local ok,n=pcall(collectgarbage,'count')
  if ok and type(n)=='number' then return n/1024 end -- MiB, only this Lua state
 end
function M.StartMemory(P,shared)
 local d={};shared.MemoryObservation=d
 local armed=false;local player;local startTurn;local baseline;local rows={};local pending;local seen={}
 local keys={'city_scan','district_scan','facts','building_check','building_create','building_remove','property_write','derive_executed'}
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
  if begin then armed=true;player=pid;startTurn=Game.GetCurrentGameTurn();baseline=nil;rows={};seen={};pending=nil;snapshot('开始')
  elseif not baseline then return '左键开始一次观测；右键读取。不修改游戏状态。'
  else snapshot('手动读取')end
  local lines={'内存观测 | '..(armed and '运行中（最多6回合）' or '已停止')..' | 仅本次加载',
   'Gameplay Lua MiB；不是文明6进程总内存。不可用表示接口不开放。'}
  for _,v in ipairs(rows)do lines[#lines+1]='T'..v.turn..' '..v.label..'：'..(v.heap and string.format('%.2f MiB',v.heap) or '不可用')end
  local last=rows[#rows];local values={}
  for _,k in ipairs(keys)do values[#values+1]=labels[k]..' '..(last.totals[k]-baseline[k])end
  lines[#lines+1]='开始以来：'..table.concat(values,' / ')
  local dc=shared.DistrictCompleteness;local net=shared.NetworkBridge;local claim=shared.ClaimProjects;local store=shared.CityProgressionStore
  lines[#lines+1]='当前缓存条目：D '..(dc and dc.CacheSize() or 0)..' / 网络玩家 '..size(net and net.players)..' / 认领视图 '..size(claim and claim.views)..' / 确认 '..size(claim and claim.syncAck)..' / 城市记录 '..(store and store.RecordCount() or 0)
  lines[#lines+1]='没有强制GC或清理；回合进入采样不代表引擎已完成回收。'
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
