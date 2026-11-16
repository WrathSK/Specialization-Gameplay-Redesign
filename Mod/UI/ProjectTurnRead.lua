-- Read the current queue for the overflow test timer.
SPCProjectTurnRead={}
function SPCProjectTurnRead.New()
 ExposedMembers.SPC_ProjectTurnRead=function(pid,id)
  local c=Players[pid] and Players[pid]:GetCities():FindID(id)
  assert(c and c:GetOwner()==pid,"城市不可读")
  local row=assert(GameInfo.Projects.PROJECT_SPC_OVERFLOW_SINK_TEST,"实验项目缺失")
  local q=c:GetBuildQueue();local v=q:GetProjectProgress(row.Index)
  assert(type(v)=="number" and v==v and math.abs(v)<math.huge,"进度未知")
  return {owner=pid,id=id,turn=Game.GetCurrentGameTurn(),value=v,size=q:GetSize(),isProject=q:GetCurrentProductionTypeHash()==row.Hash}
 end
 return {}
end
