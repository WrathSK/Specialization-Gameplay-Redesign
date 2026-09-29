-- ProductionPanel-context-only view; real queue/cost/progress remain untouched.
SPCTimedProjectDisplay={}
function SPCTimedProjectDisplay.Text(pid,id)
 local s=(ExposedMembers.SPC_P0 or {}).TimedProjectState
 if not s or s.owner~=pid or s.id~=id then return "开启后1","需在诊断面板点击“开启1回合”；尚未开启计时" end
 if s.status=="ACTIVE" then return "1","下一次正常生产结算后完成（原型待实测）" end
 if s.status=="CONFIRMING" then return "待确认","正在确认完成；不会重复调用" end
 if s.status=="STOPPED" then return "已暂停",s.reason end
 return "需重开","本次计时已结束；不会自动续算" end
function SPCTimedProjectDisplay.Items(data)
 for _,item in ipairs(data.ProjectItems or {})do
  if item.Type=="PROJECT_SPC_OVERFLOW_SINK_TEST" then
   local turns,note=SPCTimedProjectDisplay.Text(data.Owner,data.City:GetID())
   item.TurnsLeft=turns;item.Progress=0 -- hide cost-ratio bar in this disposable list model
   item.ToolTip=note.."[NEWLINE]"..(item.ToolTip or "")
  end
 end
end
function SPCTimedProjectDisplay.Current(parent,pid,id)
 local c=Players[pid] and Players[pid]:GetCities():FindID(id)
 local row=GameInfo.Projects.PROJECT_SPC_OVERFLOW_SINK_TEST
 if not c or not row or c:GetBuildQueue():GetCurrentProductionTypeHash()~=row.Hash then return end
 local turns,note=SPCTimedProjectDisplay.Text(pid,id)
 parent.CurrentProductionCost:SetText("[ICON_Turn]"..turns)
 parent.CurrentProductionProgressString:SetText(turns=="1" and "计时已开启：1回合" or ("计时："..turns))
 parent.CurrentProductionProgress:SetPercent(0)
 parent.CurrentProductionProgress:SetShadowPercent(0)
 parent.ProductionIcon:SetToolTipString(note)
end
