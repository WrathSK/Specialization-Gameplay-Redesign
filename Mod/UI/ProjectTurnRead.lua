-- B120: no per-frame/hover requests; one project's cached UI value only.
SPCProjectTurnRead={}
function SPCProjectTurnRead.New(P,show,send)
 local api={};local active=nil;local pending=false
 ExposedMembers.SPC_ProjectTurnRead=function(pid,id)
  local c=Players[pid] and Players[pid]:GetCities():FindID(id)
  assert(c and c:GetOwner()==pid,"城市不可读")
  local row=assert(GameInfo.Projects.PROJECT_SPC_OVERFLOW_SINK_TEST,"实验项目缺失")
  local q=c:GetBuildQueue();local v=q:GetProjectProgress(row.Index)
  assert(type(v)=="number" and v==v and math.abs(v)<math.huge,"进度未知")
  return {owner=pid,id=id,turn=Game.GetCurrentGameTurn(),value=v,size=q:GetSize(),isProject=q:GetCurrentProductionTypeHash()==row.Hash}
 end
 function api.Read()
  local g=(ExposedMembers.SPC_P0 or {}).ProjectTurnEvidence
  if not g or (active and g.token~=active.token) then show("尚无本次项目观察回复；不自动重发。重载后需重新开启。");return end
  local labels={ACTIVE="观察中",ENDED="观察结束",STOPPED="观察暂停"}
  local lines={"项目结算观察｜"..(labels[g.status] or g.status).."｜城"..g.id,"起始T"..g.start.."｜"..g.reason,
   "按发生顺序；UI是当时缓存，不保证与GP同步。"}
  for _,v in ipairs(g.rows) do lines[#lines+1]=v end
  if g.missing~="" then lines[#lines+1]="缺接口："..g.missing end
  show(table.concat(lines,"[NEWLINE]"))
 end
 function api.Pulse()
  if not pending or not active then return end
  local g=(ExposedMembers.SPC_P0 or {}).ProjectTurnEvidence
  if not g or g.token~=active.token or (active.ending and g.status=="ACTIVE") then return end
  pending=false;api.Read()
 end
 function api.Begin()
  if pending then show("请求仍待回复；右键报告可读取。不会重发。");return end
  local old=(ExposedMembers.SPC_P0 or {}).ProjectTurnEvidence
  if old and old.status=="ACTIVE" then active={token=old.token,id=old.id,owner=old.owner};api.Read();return end
  local ok,err=pcall(function()
   local pid=Game.GetLocalPlayer();local c=UI.GetHeadSelectedCity()
   assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,"请选择己方测试城")
   local v=ExposedMembers.SPC_ProjectTurnRead(pid,c:GetID())
   assert(v.size==1 and v.isProject,"请先把溢出承接实验选为唯一生产目标")
   ExposedMembers.SPC_ProjectTurnSerial=(ExposedMembers.SPC_ProjectTurnSerial or 0)+1
   active={owner=pid,id=c:GetID(),token="B120:"..v.turn..":"..ExposedMembers.SPC_ProjectTurnSerial}
   pending=true;show("正在开启项目观察；不改生产。")
   send(pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart="SPC_P0_Request",Action="PROJECT_TURN_BEGIN",Token=active.token,CityID=active.id,StartTurn=v.turn})
   api.Pulse()
  end)
  if not ok then pending=false;show("项目观察未开启："..tostring(err)) end
 end
 function api.End()
  local g=(ExposedMembers.SPC_P0 or {}).ProjectTurnEvidence
  if not g or g.status~="ACTIVE" then api.Read();return end
  if pending then api.Pulse();return end
  active={owner=g.owner,id=g.id,token=g.token,ending=true};pending=true
  send(g.owner,PlayerOperations.EXECUTE_SCRIPT,{OnStart="SPC_P0_Request",Action="PROJECT_TURN_END",Token=g.token,CityID=g.id})
  api.Pulse()
 end
 return api
end
