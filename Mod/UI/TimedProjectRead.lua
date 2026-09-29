-- Cached diagnostic; requests only on explicit start/cancel, never hover or polling.
SPCTimedProjectRead={}
function SPCTimedProjectRead.New(P,show,send)
 local api={};local pending=nil;local seen=nil
 local function state()return (ExposedMembers.SPC_P0 or {}).TimedProjectState end
 function api.Read()
  local s=state()
  if not s then show("项目计时未开启。请在生产列表选择溢出承接实验为唯一目标，自动开启。读档不续算。");return end
  local labels={ACTIVE="计时已开启",CONFIRMING="正在确认完成",COMPLETED="项目已退出",STOPPED="已暂停",EARLY_END="提前结束"}
  show("自动项目｜"..(labels[s.status] or s.status).."｜城"..tostring(s.id).."[NEWLINE]启动T"..tostring(s.start)..
   "｜结束回合确认："..(s.deactivated and "是" or "否").."｜调用"..s.attempts.."次[NEWLINE]"..s.reason..
   "[NEWLINE]无正式奖励；目标退出不等于无溢出验收。查看后续目标进度请右键“完成承接试验”。")
 end
 function api.Pulse()
  local s=state()
  if not s then return end
  local signature=s.token..":"..s.status..":"..tostring(s.deactivated)
  if signature==seen then return end
  seen=signature
  if pending and s.token==pending then pending=nil end
  api.Read()
 end
 function api.Begin()
  if pending then show("开启请求待回复，不重复发送。");return end
  local s=state();if s and (s.status=="ACTIVE" or s.status=="CONFIRMING")then api.Read();return end
  local ok,err=pcall(function()
   local pid=Game.GetLocalPlayer();local c=UI.GetHeadSelectedCity()
   assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,"请选择己方城")
   local v=ExposedMembers.SPC_ProjectTurnRead(pid,c:GetID())
   assert(v.isProject and v.size==1,"请先选择溢出承接实验为唯一目标")
   ExposedMembers.SPC_TimedProjectSerial=(ExposedMembers.SPC_TimedProjectSerial or 0)+1
   pending="B121:"..v.turn..":"..ExposedMembers.SPC_TimedProjectSerial
   show("正在开启1回合计时…")
   send(pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart="SPC_P0_Request",Action="TIMED_PROJECT_BEGIN",Token=pending,CityID=c:GetID(),StartTurn=v.turn})
   api.Pulse()
  end)
  if not ok then pending=nil;show("计时未开启："..tostring(err))end
 end
 function api.Cancel()
  local s=state();if not s or s.status~="ACTIVE" then api.Read();return end
  send(s.owner,PlayerOperations.EXECUTE_SCRIPT,{OnStart="SPC_P0_Request",Action="TIMED_PROJECT_CANCEL",Token=s.token,CityID=s.id})
  api.Pulse()
 end
 return api
end
