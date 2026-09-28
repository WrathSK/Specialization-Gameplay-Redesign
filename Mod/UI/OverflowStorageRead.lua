-- B119: explicit clicks only; one-city progress inventory is read on prepare/ack/report.
SPCOverflowStorageRead={}
function SPCOverflowStorageRead.New(P,show,send)
 local api={};local prepared=nil;local active=nil;local requestPending=false;local report="尚未开启完成承接试验。先从生产列表选择“溢出承接实验（无收益）”。"
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
 ExposedMembers.SPC_OverflowExactRead=function(pid,id)
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
   output("完成承接：尚未执行｜项目进度="..active.value.."[NEWLINE]再次左键原生完成此无收益项目；不是扣生产力。[NEWLINE]右键只读。仅实验前存档可恢复。")
  else
   prepared=nil
   output("调用记录｜"..g.status.."[NEWLINE]"..g.reason.."[NEWLINE]这是接口回复，不是最新生产读数；右键刷新。未发奖、未自动过回合。")
  end
 end
 function api.Click()
  if requestPending then output("清除请求等待回复；不自动重发。右键可读迟到结果。");return end
  local ok,err=pcall(function()
   local c,pid=selected();local before,n,total=snapshot(c)
   local row=GameInfo.Projects[project];assert(row,"专用项目未加载；勿继续旧实验")
   assert(n==1 and c:GetBuildQueue():GetCurrentProductionTypeHash()==row.Hash,"请在城市生产列表选择唯一目标：溢出承接实验（无收益）")
   local projectKey="Projects:"..row.Index;local value=before[projectKey].value
   assert(value>=0 and value<=10000,"项目进度需在0至10000之间；负值请回测试前档")
   local turn=Game.GetCurrentGameTurn();local action="OVERFLOW_PREPARE"
   if prepared then
    assert(prepared.owner==pid and prepared.id==c:GetID() and prepared.x==c:GetX() and prepared.y==c:GetY() and prepared.turn==turn,"选城/回合已变化；重新准备")
    assert(same(prepared.before,before),"准备后目标进度已变化；重新准备")
    active=prepared;action="OVERFLOW_APPLY"
   else
    ExposedMembers.SPC_OverflowSerial=(ExposedMembers.SPC_OverflowSerial or 0)+1
    active={owner=pid,id=c:GetID(),x=c:GetX(),y=c:GetY(),turn=turn,before=before,total=total,value=value,projectKey=projectKey,token="B119O:"..turn..":"..ExposedMembers.SPC_OverflowSerial}
   end
   active.sent=action;requestPending=true
   output(action=="OVERFLOW_PREPARE" and "正在准备；尚未写入。" or "已发完成承接请求；请勿重复点击。")
   send(pid,PlayerOperations.EXECUTE_SCRIPT,packet(action,active))
   api.Pulse()
  end)
  if not ok then
   prepared=nil
   output("完成承接暂停："..shortError(err).."[NEWLINE]已发请求如结果不明不得重试；仅测试前存档可恢复。")
  end
 end
 function api.Read()
  api.Pulse()
  local ok,detail=pcall(function()
   local c,pid=selected();local values,n=snapshot(c);local q=c:GetBuildQueue()
   if active then assert(active.owner==pid and active.id==c:GetID() and active.x==c:GetX() and active.y==c:GetY(),"所选城不是本次实验城") end
   local row=GameInfo.Projects[project];assert(row,"专用项目未加载")
   local pv=values["Projects:"..row.Index];assert(pv,"项目读数缺失")
   local hash=q:GetCurrentProductionTypeHash();local current=n==0 and "无生产目标" or nil
   if n>0 then
    for _,kind in ipairs({"Buildings","Districts","Units","Projects"}) do
     for item in GameInfo[kind]() do
      if item.Hash==hash then
       local v=values[kind..":"..item.Index];assert(v,"当前目标进度缺失")
       current=v.name.."｜进度="..v.value
      end
     end
    end
    assert(current,"当前目标未知，不能判零")
   end
   local changed=0;local examples={}
   if active then
    for k,v in pairs(values) do
     if k~=active.projectKey and (not active.before[k] or active.before[k].value~=v.value) then
      changed=changed+1
      if #examples<4 then examples[#examples+1]=v.name..":"..tostring(active.before[k] and active.before[k].value).."→"..v.value end
     end
    end
   end
   return "当前读数｜回合"..Game.GetCurrentGameTurn().."｜城"..c:GetID().."｜队列"..n..
    "[NEWLINE]当前目标："..current.."[NEWLINE]实验项目保留进度="..pv.value..
    (active and ("[NEWLINE]其它目标相对准备时变化"..changed.."项"..(#examples>0 and ("："..table.concat(examples,"；")) or "")) or "")..
    "[NEWLINE]最新读数不代表完整PASS；后续目标选中时及正常一回合后分别截图。"
  end)
  show((ok and detail or ("当前读数不可确认："..shortError(detail))).."[NEWLINE]——[NEWLINE]"..report)
 end
 return api
end
