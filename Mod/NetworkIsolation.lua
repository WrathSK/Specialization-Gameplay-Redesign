-- B137: explicit one-way session diagnostic. No Property/save writes or GC.
SPCNetworkIsolation={}
function SPCNetworkIsolation.Start(P,shared)
 local d={active=false,phase='NORMAL',modules={},epoch=shared.NetworkBridge.epoch};shared.NetworkIsolation=d
 local names={'Lv3Effects','NetworkBoost','CopyYields','CommerceConvergence','StandardizationDiscount'}
 local labels={'商业三级连接','网络鼓舞/尤里卡','工业复制','商业汇聚','工业折扣'}
 local uiNames={'SPC_P0_BackgroundRoutes','SPC_CopyBackground','SPC_DiscountEligibility'}
 local counters={'route_scan','net_send','derive_executed','input_publication','copy_send','discount_send'}
 local function short(e) return tostring(e):gsub('^.-:%d+: ',''):match('[^\r\n]+'):sub(1,150) end
 local function counter(k)
  local p=ExposedMembers.SPC_Performance;local e=p and p.entries and p.entries[k]
  return e and type(e.total)=='number' and e.total or nil
 end
 function d.Active(pid) return d.active and (pid==nil or pid==d.player) end
 local function uiStopped(epoch)
  for _,key in ipairs(uiNames) do
   local u=ExposedMembers[key]
   if not u or u.version~=P.VERSION or u.networkStopped~=true or u.networkStopEpoch~=epoch then return false,key end
  end
  return true
 end
 function d.Read(pid)
  assert(P.IsTestPlayer(pid),'ISOLATION_OWNER')
  local lines={'Network 同档隔离对照｜'..d.phase..'｜T'..Game.GetCurrentGameTurn()}
  if not d.active then
   for _,key in ipairs(uiNames) do
    local u=ExposedMembers[key]
    if u and u.networkStopped then return 'Network隔离未完成：UI已停止，但Gameplay尚未确认。停止对照，冷启动原存档。' end
   end
   lines[#lines+1]='当前为正常模式。左键只读；右键单向停用本次会话的 Network 分支。'
   lines[#lines+1]='仅用原存档副本；不要保存实验结果。退出游戏、重载原存档恢复。'
  else
   local uiOK,uiError=uiStopped(d.epoch)
   local perf=ExposedMembers.SPC_Performance
   local safe=uiOK and d.phase=='READY' and perf and perf.enabled==true and perf.inflight==0
   lines[#lines+1]='UI发送退出='..(uiOK and '3/3' or ('未确认 '..tostring(uiError)))..'｜收益撤销='..tostring(d.completed or 0)..'/5'
   local changed={}
   for _,k in ipairs(counters) do
    local now=counter(k);local before=d.baseline and d.baseline[k]
    if now==nil or before==nil then safe=false;changed[#changed+1]=k..'=不可读'
    elseif now~=before then safe=false;changed[#changed+1]=k..' +'..tostring(now-before) end
   end
   lines[#lines+1]=safe and '可观察：退出后网络采集/发送/派生/发布无新增。' or '停止对照：退出或静默条件未满足。'
   if #changed>0 then lines[#lines+1]=table.concat(changed,' / ') end
   for i,name in ipairs(names) do if d.modules[name] and d.modules[name]~='CLEARED' then lines[#lines+1]=labels[i]..'：'..d.modules[name] end end
   if d.error then lines[#lines+1]=d.error end
   lines[#lines+1]='保留本地能力、身份/投资、模板及其它后台；不是关闭整个 Mod。'
   lines[#lines+1]='不要保存/继续正式游玩；冷启动重载原存档恢复，不在本会话重开。'
  end
  local heap=SPCPerformance and SPCPerformance.Heap and SPCPerformance.Heap()
  lines[#lines+1]='Lua调用处用量='..(heap and string.format('%.2f MiB',heap) or '不可读')..'（非本Mod独占；未执行GC）'
  return table.concat(lines,'\n')
 end
 function d.Begin(pid,epoch)
  assert(P.IsTestPlayer(pid),'ISOLATION_OWNER')
  if d.active then return d.Read(pid) end -- no cleanup retry after partial failure
  assert(epoch==d.epoch and shared.NetworkBridge.ready,'ISOLATION_EPOCH_OR_LOAD')
  local uiOK,why=uiStopped(epoch);assert(uiOK,'ISOLATION_UI_NOT_STOPPED:'..tostring(why))
  assert(not shared.NetworkBridge.players[pid] or not shared.NetworkBridge.players[pid].refreshing,'ISOLATION_BRIDGE_BUSY')
  for _,name in ipairs(names) do
   local m=shared[name];assert(m and type(m.ExperimentalNetworkWithdraw)=='function' and not m.busy,'ISOLATION_MODULE_NOT_READY:'..name)
  end
  d.player=pid;d.active=true;d.phase='WITHDRAWING';d.completed=0;d.startTurn=Game.GetCurrentGameTurn()
  local bridgeOK,bridgeError=pcall(shared.NetworkBridge.ExperimentalStop,pid)
  if not bridgeOK then d.error=short(bridgeError) end
  for _,name in ipairs(names) do
   local ok,result=pcall(shared[name].ExperimentalNetworkWithdraw,pid)
   if ok and result==true then d.modules[name]='CLEARED';d.completed=d.completed+1
   else d.modules[name]=short(result) end
  end
  d.phase=bridgeOK and d.completed==#names and 'READY' or 'FAILED'
  d.baseline={};for _,k in ipairs(counters) do d.baseline[k]=counter(k) end
  return d.Read(pid)
 end
end
