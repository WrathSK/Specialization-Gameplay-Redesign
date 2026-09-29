include("ClaimProjectUI")
-- Shared cached timing text for independent UI contexts; never changes actual production.
SPCTimedProjectDisplay={}
function SPCTimedProjectDisplay.IsCurrent(c)
 if SPCClaimProjectUI.Current(c) then return true end
 local row=GameInfo.Projects.PROJECT_SPC_OVERFLOW_SINK_TEST
 return c and c:GetOwner()==Game.GetLocalPlayer() and row and c:GetBuildQueue():GetCurrentProductionTypeHash()==row.Hash
end
function SPCTimedProjectDisplay.Text(pid,id)
 local c=Players[pid] and Players[pid]:GetCities():FindID(id)
 local claim=SPCClaimProjectUI.Current(c)
 if claim then return SPCClaimProjectUI.Text(pid,id,claim)end
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
  if SPCClaimProjectUI.IsProject(item.Type)then
   local turns,note=SPCClaimProjectUI.Text(data.Owner,data.City:GetID(),item.Type)
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
 parent.CurrentProductionProgressString:SetText(turns=="1" and "计时已开启：1回合" or ("计时："..turns))
 parent.CurrentProductionProgress:SetPercent(0)
 parent.CurrentProductionProgress:SetShadowPercent(0)
 parent.ProductionIcon:SetToolTipString(note)
end
