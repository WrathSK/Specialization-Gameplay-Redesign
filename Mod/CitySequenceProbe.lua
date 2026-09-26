-- B106: opt-in, one-location, bounded Gameplay event evidence. No state authority.
SPCCitySequenceProbe={}
function SPCCitySequenceProbe.Start(P,shared)
 local d={};shared.CitySequenceProbe=d
 local ready=false
 local capture
 local hooks={}
 local LIMIT=48
 local function number(v)return type(v)=='number' and v==v and v>-math.huge and v<math.huge end
 local foundReason=P.Field(EventSubTypes,'FOUND_CITY')
 if not number(foundReason)then foundReason=nil end
 local function integer(v)return type(v)=='number' and v>=0 and v<math.huge and v%1==0 end
 local function reference(c)
  return {owner=c:GetOwner(),id=c:GetID(),x=c:GetX(),y=c:GetY()}
 end
 local function remember(r)
  if not capture or not integer(r.owner) or not integer(r.id) then return end
  for _,v in ipairs(capture.refs)do if v.owner==r.owner and v.id==r.id then return end end
  if #capture.refs>=12 then capture.error='REFERENCE_LIMIT';capture.stopped=true;return end
  capture.refs[#capture.refs+1]={owner=r.owner,id=r.id}
 end
 local function known(owner,id)
  for _,v in ipairs(capture.refs)do if v.owner==owner and v.id==id then return true end end
  return false
 end
 local function occupant()
  local ok,c=pcall(CityManager.GetCityAt,capture.x,capture.y)
  if not ok then return 'UNKNOWN' end
  if not c then return 'EMPTY' end
  local good,r=pcall(reference,c)
  if not good or not integer(r.owner) or not integer(r.id) or r.x~=capture.x or r.y~=capture.y then return 'UNKNOWN' end
  remember(r);return 'CITY',r.owner,r.id
 end
 local function append(name,a,b,c,e)
  if #capture.rows>=LIMIT then capture.error='TRACE_LIMIT';capture.stopped=true;return end
  local t=Game.GetCurrentGameTurn()
  assert(integer(t),'TURN_UNAVAILABLE')
  -- Primitive tuple only; never retain event payloads, engine objects or full city data.
  capture.rows[#capture.rows+1]={name=name,turn=t,a=a,b=b,c=c,e=e}
 end
 local function snapshot(name)
  local state,owner,id=occupant();append(name,state,owner,id)
 end
 local function guarded(fn,...)
  if not capture or capture.stopped then return end
  local ok=pcall(fn,...)
  if not ok then capture.error='OBSERVER_READ_ERROR';capture.stopped=true end
 end
 local function spatial(name,owner,id,x,y,oldOwner)
  if x~=capture.x or y~=capture.y then return end
  assert(integer(owner) and integer(id),'BAD_EVENT_REFERENCE')
  if oldOwner~=nil then assert(integer(oldOwner),'BAD_OLD_OWNER')end
  remember({owner=owner,id=id});append(name,owner,id,oldOwner)
  capture.publish=true;capture.playback=true
 end
 local function removed(owner,id)
  if not known(owner,id)then return end
  append('Removed',owner,id);capture.publish=true;capture.playback=true
 end
 local function transferred(owner,id,oldOwner,transferType)
  if not known(owner,id)then
   local city=CityManager.GetCity(owner,id)
   if not city then return end
   local r=reference(city);if r.x~=capture.x or r.y~=capture.y then return end
   remember(r)
  end
  assert(integer(owner) and integer(id) and integer(oldOwner),'BAD_TRANSFER')
  -- Native transfer enum may be a signed hash.
  local reason=type(transferType)=='number' and transferType or nil
  append('Transfer',owner,id,oldOwner,reason);capture.publish=true;capture.playback=true
 end
 local function activated(owner,unitID,x,y,reason,visible)
  if x~=capture.x or y~=capture.y then return end
  assert(integer(owner) and integer(unitID),'BAD_UNIT_REFERENCE')
  -- The settler may already be gone. Record scalars only; never look it up or
  -- treat a unit ID as a city ID. Visibility does not gate diagnostic capture.
  local raw=number(reason) and reason or 'UNAVAILABLE'
  local name=foundReason~=nil and raw==foundReason and 'FoundCity' or 'UnitActivate'
  append(name,owner,unitID,raw,type(visible)=='boolean' and tostring(visible) or 'UNKNOWN')
  capture.publish=true;capture.playback=true
 end
 local function boundary(name,flag)
  if not capture[flag]then return end
  capture[flag]=false;snapshot(name)
 end
 local function hook(ns,name,fn)
  local ev=P.Field(ns,name)
  if not ev or type(ev.Add)~='function' then hooks[name]=false;return end
  local ok=pcall(ev.Add,function(...)guarded(fn,...)end);hooks[name]=ok
 end
 local load=P.Field(Events,'LoadScreenClose')
 hooks.LoadScreenClose=load and type(load.Add)=='function' and pcall(load.Add,function()ready=true end) or false
 hook(GameEvents,'CityBuilt',function(o,id,x,y)spatial('Built',o,id,x,y)end)
 hook(GameEvents,'CityConquered',function(o,old,id,x,y)spatial('Conquered',o,id,x,y,old)end)
 hook(Events,'CityAddedToMap',function(o,id,x,y)spatial('Added',o,id,x,y)end)
 hook(Events,'CityInitialized',function(o,id,x,y)spatial('Initialized',o,id,x,y)end)
 hook(Events,'CityRemovedFromMap',removed)
 hook(Events,'CityTransfered',transferred)
 hook(Events,'UnitActivate',activated)
 hook(Events,'GameCoreEventPublishComplete',function()boundary('Publish','publish')end)
 hook(Events,'GameCoreEventPlaybackComplete',function()boundary('Playback','playback')end)
 function d.Begin(pid,c,u,token)
  local ok,out=pcall(function()
   assert(ready and P.IsTestPlayer(pid),'LOCAL_PLAYER_OR_LOAD_NOT_READY')
   assert(type(token)=='string' and #token<=100,'REQUEST_TOKEN')
   if capture and capture.token==token then return d.Describe(pid,1)end
   local x,y,settlerID
   if u then
    local row=P.Info('Units',u:GetType())
    assert(u:GetOwner()==pid and row and row.UnitType=='UNIT_SETTLER','SELECT_OWN_SETTLER')
    x,y=u:GetX(),u:GetY();settlerID=u:GetID()
    assert(integer(settlerID),'SETTLER_REFERENCE_UNAVAILABLE')
   else
    assert(c and c:GetOwner()==pid,'SELECT_OWN_CITY_OR_SETTLER');x,y=c:GetX(),c:GetY()
   end
   assert(integer(x) and integer(y),'LOCATION_UNAVAILABLE')
   local prior=capture
   capture={owner=pid,x=x,y=y,token=token,settlerID=settlerID,rows={},refs={}}
   local valid=pcall(function()snapshot('Start')end)
   if not valid or capture.error then capture=prior;error('START_READ_FAILED')end
   return d.Describe(pid,1)
  end)
  return ok and out or '事件观察未开始：'..tostring(out)..'\n原有记录未改。'
 end
 function d.Read(pid,page)
  -- A manual operation may itself provoke a native publish. Mark it so the
  -- later boundary cannot be mistaken for an operation-only completion.
  if capture and capture.owner==pid and (capture.publish or capture.playback) then
   guarded(function()append('ReadRequest')end)
  end
  return d.Describe(pid,page)
 end
 function d.Describe(pid,page)
  if not capture then return '尚未开始事件观察。选中己方移民或城市，右键“移民 / 施工队”。'end
  if capture.owner~=pid then return '事件观察不属于当前玩家。'end
  local pages=math.max(1,math.ceil(#capture.rows/10));page=tonumber(page)or 1
  if page~=page or page==math.huge or page==-math.huge then page=1 end
  page=(math.max(1,math.floor(page))-1)%pages+1
  local lines={'事件顺序（Gameplay，只读） | 位置 '..capture.x..','..capture.y..' | 页 '..page..'/'..pages,
   '以下仅为手动事件观察，不参与新城登记判定。'..(capture.error and (' 暂停：'..capture.error)or ''),
   '监听 Publish='..tostring(hooks.GameCoreEventPublishComplete)..' / Playback='..tostring(hooks.GameCoreEventPlaybackComplete)..' / Transfer='..tostring(hooks.CityTransfered),
   '建城观察：UnitActivate='..tostring(hooks.UnitActivate)..' / FOUND_CITY='..(foundReason~=nil and tostring(foundReason) or '不可用')..' / 起始移民='..(capture.settlerID and tostring(capture.settlerID) or '未选')}
  local missing={};for name,ok in pairs(hooks)do if not ok then missing[#missing+1]=name end end
  if #missing>0 then table.sort(missing);lines[#lines+1]='缺少监听：'..table.concat(missing,',')end
  for i=(page-1)*10+1,math.min(page*10,#capture.rows)do
   local r=capture.rows[i];local args={}
   for _,k in ipairs({'a','b','c','e'})do if r[k]~=nil then args[#args+1]=tostring(r[k])end end
   lines[#lines+1]=i..'. T'..r.turn..' '..r.name..' '..table.concat(args,' / ')
  end
  lines[#lines+1]='Publish/Playback=后续首个批次通知；CITY后为Owner/ID，EMPTY=查询无城（非销毁定论）。'
  lines[#lines+1]='FoundCity/UnitActivate：Owner/单位ID/原因/可见性；仅FoundCity表示原因匹配，不是新城登记。'
  lines[#lines+1]='事件参数：Owner/ID；Conquered/Transfer另含旧Owner。ReadRequest=手动读取，后随批次不能单独作证。右键翻页；读档重置。'
  return table.concat(lines,'\n')
 end
end
