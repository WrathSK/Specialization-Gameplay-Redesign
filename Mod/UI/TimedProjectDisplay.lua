include("ClaimProjectUI")
include("DialogueProjectUI")
include("EngineeringStudyUI")
-- Shared cached timing text for independent UI contexts; never changes actual production.
SPCTimedProjectDisplay={}
-- Translate known player-facing notes here. Controllers and stored reasons keep their original values.
local noteKeys={
 ["当前生产不可读"]="CURRENT_PRODUCTION_UNKNOWN",
 ["1回合；保存读档继续计时"]="CLAIM_ACTIVE",
 ["已改选目标；重新选择须完整占用一回合"]="CLAIM_SWITCHED",
 ["当前队列未确认；不完成项目"]="CLAIM_QUEUE_UNKNOWN",
 ["错过完整回合窗口；请重新选择"]="CLAIM_WINDOW_MISSED",
 ["当前队列未确认；等待相关事件，不完成项目"]="CLAIM_QUEUE_FACT_REQUIRED",
 ["当前项目没有计时；请先改选普通目标，再重选认领项目，重新占用完整一回合"]="CLAIM_NO_TIMER",
 ["改选另一认领项目"]="CLAIM_DIFFERENT_CLAIM",
 ["当前目标已改变"]="CLAIM_TARGET_CHANGED",
 ["未确认完整生产回合；请重新选择"]="FULL_TURN_UNCONFIRMED",
 ["等待原生完成事件；结果未知时不重复调用"]="CLAIM_COMPLETION_PENDING",
 ["已改选目标；需重新占用完整回合"]="CLAIM_RESTART",
 ["找不到对应已完成区域；暂停认领"]="CLAIM_DISTRICT_UNAVAILABLE",
 ["认领项目不能排在队列后面；请选为唯一当前目标"]="CLAIM_SOLE_QUEUE",
 ["等待原生选择确认"]="CLAIM_TARGET_PENDING",
 ["读档同步等待确认；不会自动重发"]="CLAIM_RELOAD_PENDING",
 ["启动确认超时；请重新选择项目"]="CLAIM_START_TIMEOUT",
 ["完整一回合计时中"]="DIALOGUE_ACTIVE",
 ["时代对话必须为唯一当前生产目标"]="DIALOGUE_SOLE_QUEUE",
 ["当前资格尚不可确认；未清除历史，也不完成项目"]="DIALOGUE_ELIGIBILITY_UNKNOWN",
 ["当前资格或生产未确认；等待相关事件，不完成项目"]="DIALOGUE_FACT_REQUIRED",
 ["原生完成已请求；结果不明时不重复调用"]="DIALOGUE_COMPLETION_PENDING",
 ["完成来源已不确定；不重放或补取之后的馆藏"]="DIALOGUE_COMPLETION_SOURCE_UNKNOWN",
 ["完成时事实未确认；不以之后的馆藏补算"]="DIALOGUE_COLLECTION_UNKNOWN",
}
local countNotes={
 {pattern="^认领必须为唯一当前目标；队列数量=(%d+)$",key="CLAIM_SOLE_QUEUE_COUNT"},
 {pattern="^等待队列确认；数量=(%d+)$",key="CLAIM_QUEUE_COUNT_PENDING"},
}
local function localizedNote(note)
 if type(note)~="string" then return note end
 local key=noteKeys[note]
 if key then return Locale.Lookup("LOC_SPC_TIMED_PROJECT_REASON_"..key) end
 for _,entry in ipairs(countNotes) do
  local count=note:match(entry.pattern)
  if count then return Locale.Lookup("LOC_SPC_TIMED_PROJECT_REASON_"..entry.key,count) end
 end
 return note
end
local function localizedStatus(turns,note)
 return turns,localizedNote(note)
end
function SPCTimedProjectDisplay.IsCurrent(c)
 if SPCEngineeringStudyUI.Current(c) or SPCDialogueProjectUI.Current(c) or SPCClaimProjectUI.Current(c) then return true end
 local row=GameInfo.Projects.PROJECT_SPC_OVERFLOW_SINK_TEST
 return c and c:GetOwner()==Game.GetLocalPlayer() and row and c:GetBuildQueue():GetCurrentProductionTypeHash()==row.Hash
end
function SPCTimedProjectDisplay.Text(pid,id)
 local c=Players[pid] and Players[pid]:GetCities():FindID(id)
 if SPCEngineeringStudyUI.Current(c)then return SPCEngineeringStudyUI.Text(pid,id)end
 if SPCDialogueProjectUI.Current(c)then return localizedStatus(SPCDialogueProjectUI.Text(pid,id))end
 local claim=SPCClaimProjectUI.Current(c)
 if claim then return localizedStatus(SPCClaimProjectUI.Text(pid,id,claim))end
 local selection=ExposedMembers.SPC_TimedProjectSelection
 local s=(ExposedMembers.SPC_P0 or {}).TimedProjectState
 if selection and selection.owner==pid and selection.id==id and selection.status~="ACK" and (not s or s.token~=selection.token) then
  return selection.status=="ERROR" and "未启动" or "确认中",selection.reason
 end
 if not s or s.owner~=pid or s.id~=id then
  local c=Players[pid] and Players[pid]:GetCities():FindID(id)
  if SPCTimedProjectDisplay.IsCurrent(c) then return "未启动","当前项目尚无计时；读档不续算，请在生产列表重新选择" end
  return "1*","选为唯一当前目标后自动计时1回合；本批只支持单城，不跨读档续算"
 end
 if s.status=="ACTIVE" then return "1","下一次正常生产结算后自动完成" end
 if s.status=="CONFIRMING" then return "待确认","正在确认完成；不会重复调用" end
 if s.status=="STOPPED" then return "已暂停",s.reason end
 return "需重开","本次计时已结束；重新选择项目才会请求新的计时" end
function SPCTimedProjectDisplay.Items(data)
 for _,item in ipairs(data.ProjectItems or {})do
  if item.Type==SPCEngineeringStudyUI.PROJECT then
   local turns,note=SPCEngineeringStudyUI.Text(data.Owner,data.City:GetID())
   item.TurnsLeft=turns;item.Progress=0;item.ToolTip=note.."[NEWLINE]"..(item.ToolTip or "")
  elseif item.Type==SPCDialogueProjectUI.PROJECT then
   local read=item.IsCurrentProduction==false and SPCDialogueProjectUI.Preview or SPCDialogueProjectUI.Text
   local turns,note=localizedStatus(read(data.Owner,data.City:GetID()))
   item.TurnsLeft=turns;item.Progress=0;item.ToolTip=note.."[NEWLINE]"..(item.ToolTip or "")
  elseif SPCClaimProjectUI.IsProject(item.Type)then
   local turns,note=localizedStatus(SPCClaimProjectUI.Text(data.Owner,data.City:GetID(),item.Type))
   item.TurnsLeft=turns;item.Progress=0;item.ToolTip=note.."[NEWLINE]"..(item.ToolTip or "")
  elseif item.Type=="PROJECT_SPC_OVERFLOW_SINK_TEST" then
   local turns,note=SPCTimedProjectDisplay.Text(data.Owner,data.City:GetID())
   item.TurnsLeft=turns;item.Progress=0 -- hide cost-ratio bar in this disposable list model
   item.ToolTip=note.."[NEWLINE]"..(item.ToolTip or "")
  end
 end
end
function SPCTimedProjectDisplay.Current(parent,pid,id)
 local c=Players[pid] and Players[pid]:GetCities():FindID(id)
 local row=GameInfo.Projects.PROJECT_SPC_OVERFLOW_SINK_TEST
 if not SPCTimedProjectDisplay.IsCurrent(c) then return end
 local turns,note=SPCTimedProjectDisplay.Text(pid,id)
 parent.CurrentProductionCost:SetText("[ICON_Turn]"..turns)
 local progressText=turns=="1" and Locale.Lookup("LOC_SPC_TIMED_PROJECT_TIMER_ACTIVE")
  or Locale.Lookup("LOC_SPC_TIMED_PROJECT_TIMER_STATUS",turns)
 parent.CurrentProductionProgressString:SetText(progressText)
 parent.CurrentProductionProgress:SetPercent(0)
 parent.CurrentProductionProgress:SetShadowPercent(0)
 parent.ProductionIcon:SetToolTipString(note)
end
