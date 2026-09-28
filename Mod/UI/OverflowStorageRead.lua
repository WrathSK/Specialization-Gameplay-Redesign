-- B118: explicit clicks only; one-city progress inventory is read on prepare/ack/report.
SPCOverflowStorageRead={}
function SPCOverflowStorageRead.New(P,show,send)
 local api={};local prepared=nil;local active=nil;local requestPending=false;local report="尚未开启精确扣除试验。先从生产列表选择“溢出承接实验（无收益）”。"
 local project="PROJECT_SPC_OVERFLOW_SINK_TEST"
 local function shortError(err)
  local raw=tostring(err);print("[SPC][OverflowStorageUI] "..raw)
  return (raw:match("^[^\r\n]+") or "接口错误"):gsub("^.-:%d+: ?","")
 end
 local function output(s) report=s;show(s) end
 local function snapshot(c)
  local q=c:GetBuildQueue();local n=q:GetSize()
  assert(type(n)=="number" and n>=0 and n==math.floor(n),"UI队列不可确认")
  local out={};local total=0
  for _,pair in ipairs({{"Buildings","GetBuildingProgress"},{"Districts","GetDistrictProgress"},{"Units","GetUnitProgress"},{"Projects","GetProjectProgress"}}) do
   assert(type(q[pair[2]])=="function","进度接口缺失："..pair[2])
   for row in GameInfo[pair[1]]() do
    total=total+1;assert(total<=4096,"进度目录超过原型上限")
    local v=q[pair[2]](q,row.Index)
    assert(type(v)=="number" and v==v and math.abs(v)<math.huge,"目标进度未知："..tostring(row.Index))
    out[pair[1]..":"..row.Index]={value=v,name=Locale.Lookup(row.Name)}
   end
  end
  return out,n,total
 end
 local function selected()
  local pid=Game.GetLocalPlayer();local c=UI.GetHeadSelectedCity()
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,"请选择己方测试城市")
  return c,pid
 end
 local function packet(action,f)
  return {OnStart="SPC_P0_Request",Action=action,Token=f.token,CityID=f.id,StartTurn=f.turn,Progress=f.value}
 end
 local function same(a,b)
  for k,v in pairs(a) do if not b[k] or b[k].value~=v.value then return false end end
  for k in pairs(b) do if not a[k] then return false end end
  return true
 end
 -- Called synchronously by Gameplay only on explicit prepare/apply; no hover/poll scan.
 ExposedMembers.SPC_P0=ExposedMembers.SPC_P0 or {}
 ExposedMembers.SPC_P0.OverflowExactRead=function(pid,id)
  local c=Players[pid] and Players[pid]:GetCities():FindID(id)
  assert(c and c:GetOwner()==pid,"即时读数城市不可确认")
  local row=GameInfo.Projects[project];assert(row,"专用实验项目未加载；需要正确数据库")
  local q=c:GetBuildQueue();assert(q:GetCurrentProductionTypeHash()==row.Hash,"即时目标不是实验项目")
  return {owner=pid,id=id,turn=Game.GetCurrentGameTurn(),project=project,size=q:GetSize(),value=q:GetProjectProgress(row.Index)}
 end
 function api.Pulse()
  if not active or not requestPending then return end
  local g=(ExposedMembers.SPC_P0 or {}).OverflowStorage
  if not g or g.token~=active.token then return end
  if active.sent=="OVERFLOW_APPLY" and g.status=="PREPARED" then return end
  requestPending=false
  if g.status=="PREPARED" then prepared=active
   output("精确扣除：尚未执行｜项目进度="..active.value.."[NEWLINE]再次左键只扣"..active.value.."；不会改队列或自动完成。[NEWLINE]右键只读。仅实验前存档可恢复。")
  else
   prepared=nil
   local ok,detail=pcall(function()
    local c=Players[active.owner]:GetCities():FindID(active.id)
    assert(c and c:GetOwner()==active.owner and c:GetX()==active.x and c:GetY()==active.y,"城市已变化，无法核对")
    local after=snapshot(c);local changed={};local count=0
    for k,v in pairs(after) do
     if k~=active.projectKey and (not active.before[k] or active.before[k].value~=v.value) then
      count=count+1;if #changed<5 then changed[#changed+1]=v.name..":"..tostring(active.before[k] and active.before[k].value).."→"..v.value end
     end
    end
    local p=after[active.projectKey];assert(p,"专用项目读数缺失")
    return "项目："..active.value.."→"..p.value.."；其它目标变化"..count.."项。"..
     ((p.value~=0 or count~=0) and ("未达归零判据，停止！"..table.concat(changed,"；")) or "即时归零仅是读数，后续残留仍待检验。")
   end)
   output("精确扣除｜"..g.status.."[NEWLINE]"..g.reason.."[NEWLINE]"..(ok and detail or ("即时核对未完成："..shortError(detail))).."[NEWLINE]未自动过回合、未改队列；用下一目标与下一正常生产回合判断残留/负债。")
  end
 end
 function api.Click()
  if requestPending then output("清除请求等待回复；不自动重发。右键可读迟到结果。");return end
  local ok,err=pcall(function()
   local c,pid=selected();local before,n,total=snapshot(c)
   local row=GameInfo.Projects[project];assert(row,"专用项目未加载；勿继续旧实验")
   assert(n==1 and c:GetBuildQueue():GetCurrentProductionTypeHash()==row.Hash,"请在城市生产列表选择唯一目标：溢出承接实验（无收益）")
   local projectKey="Projects:"..row.Index;local value=before[projectKey].value
   assert(value>0 and value<=10000,"项目进度需为正且不超过10000；为0时可正常生产一回合后再试，负值请回测试前档")
   local turn=Game.GetCurrentGameTurn();local action="OVERFLOW_PREPARE"
   if prepared then
    assert(prepared.owner==pid and prepared.id==c:GetID() and prepared.x==c:GetX() and prepared.y==c:GetY() and prepared.turn==turn,"选城/回合已变化；重新准备")
    assert(same(prepared.before,before),"准备后目标进度已变化；重新准备")
    active=prepared;action="OVERFLOW_APPLY"
   else
    ExposedMembers.SPC_OverflowSerial=(ExposedMembers.SPC_OverflowSerial or 0)+1
    active={owner=pid,id=c:GetID(),x=c:GetX(),y=c:GetY(),turn=turn,before=before,total=total,value=value,projectKey=projectKey,token="B118O:"..turn..":"..ExposedMembers.SPC_OverflowSerial}
   end
   active.sent=action;requestPending=true
   output(action=="OVERFLOW_PREPARE" and "正在准备；尚未写入。" or "已发精确扣除请求；请勿重复点击。")
   send(pid,PlayerOperations.EXECUTE_SCRIPT,packet(action,active))
   api.Pulse()
  end)
  if not ok then
   prepared=nil
   output("精确扣除暂停："..shortError(err).."[NEWLINE]已发请求如结果不明不得重试；仅测试前存档可恢复。")
  end
 end
 function api.Read()
  api.Pulse()
  local ok,detail=pcall(function()
   local c,pid=selected();local values,n,total=snapshot(c);local rows={}
   if active then assert(active.owner==pid and active.id==c:GetID(),"所选城不是本次实验城") end
   local changes=0
   for k,v in pairs(values) do
    if v.value~=0 and (not active or not active.before[k] or v.value~=active.before[k].value) then
     changes=changes+1;if #rows<6 then rows[#rows+1]=v.name.."="..v.value end
    end
   end
   table.sort(rows)
   return "按需读数：队列"..n.."；"..(#rows>0 and table.concat(rows,"；") or "未读到新增非零目标进度")..(changes>6 and "（更多见生产面板）" or "")
  end)
  show(report.."[NEWLINE]"..(ok and detail or shortError(detail)))
 end
 return api
end
