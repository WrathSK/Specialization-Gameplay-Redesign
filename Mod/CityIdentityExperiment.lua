-- Explicit one-city experiment. Only this Game property is writable; never a gameplay authority.
SPCCityIdentityExperiment={KEY='SPC_E1_IDENTITY_EXPERIMENT_V1'}
function SPCCityIdentityExperiment.Start(P,shared)
 local M=SPCCityIdentityExperiment;local cp=SPCCityIdentityRead.Copy
 local d={error=nil};shared.CityIdentityExperiment=d
 local record,events,ready=nil,{},false
 local overflow=false
 local function same(a,b)
  if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
  for k,v in pairs(a)do if not same(v,b[k])then return false end end
  for k in pairs(b)do if a[k]==nil then return false end end;return true
 end
 local function ref(c)return {owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()}end
 local function integer(v)return type(v)=='number' and v>=0 and v%1==0 end
 local function validRef(v)return type(v)=='table' and integer(v.owner) and integer(v.cityID) and integer(v.x) and integer(v.y)end
 local function read()
  local v=cp(Game:GetProperty(M.KEY));if v==nil then return nil end
  assert(type(v)=='table' and v.schema==1 and v.experiment=='ONE_CITY_ONLY' and integer(v.requester) and validRef(v.origin) and type(v.token)=='string' and type(v.events)=='table' and #v.events<=16 and integer(v.revision),'实验记录格式冲突，未覆盖')
  assert(v.current==nil or validRef(v.current),'实验当前引用损坏')
  assert(type(v.state)=='string' and type(v.native)=='table','实验状态损坏')
  return v
 end
 local function save(v)
  assert(not d.error,'实验已暂停，保留现有记录')
  assert(same(read(),record),'实验记录已变化，停止写入')
  v=cp(v);v.revision=(record and record.revision or 0)+1
  Game:SetProperty(M.KEY,v)
  assert(same(read(),v),'实验写入未确认；停止重试')
  record=cp(v)
 end
 local function guarded(fn)
  if d.error then return "城市身份实验暂停："..d.error end
  local ok,value=pcall(fn)
  if not ok then d.error=tostring(value):sub(1,160);return '城市身份实验暂停：'..d.error end
  return value
 end
 local function getters(c)
  local out={}
  for _,name in ipairs({'GetOriginalOwner','GetOwnerBeforeOccupation','GetJustConqueredFrom','GetLastTransferType'})do
   local ok,v=pcall(function()return c[name](c)end)
   out[name]=ok and type(v)=='number' and v or 'UNKNOWN'
  end
  return out
 end
 function d.Begin(pid,c)
  return guarded(function()
   assert(ready and P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'请在加载完成后选择己方分城')
   if record then return '本存档已有单城实验，不覆盖。请点“实验对照”；新实验请使用实验前存档。' end
   local values={};for k,key in pairs(SPCCityIdentityRead.Keys)do values[k]=c:GetProperty(key)end
   local token=values.TOKEN;assert(type(token)=='string','缺少原绑定凭据')
   local owner=tonumber(token:match('^DEV%-B013%-P(%d+)%-[1-9]%d*$'));assert(owner==pid,'原Owner凭据不符')
   local s={ref=ref(c),values=values,ledger=Game:GetProperty('SPC_DEV_BINDING_B013_P'..pid)}
   assert(SPCCityIdentityRead.Preview(s).state=='LOCAL_CANDIDATE','原账本尚未通过结构核对')
   events={};overflow=false;save({schema=1,experiment='ONE_CITY_ONLY',requester=pid,origin=ref(c),token=token,revision=0,startedTurn=Game.GetCurrentGameTurn(),state='ORIGIN_RECORDED',events={},native=getters(c)})
   return '单城实验已建立并保存到Game记录。转自由城后点“实验对照”，再另存/读档。未修改专业记录或收益。'
  end)
 end
 function d.Describe(pid)
  return guarded(function()
   assert(ready and P.IsTestPlayer(pid),'加载未完成')
   if not record then return '尚未建立实验；请选择己方分城，右键“记录城市身份”。' end
   assert(record.requester==pid,'实验属于另一玩家，未写入')
   local c=CityManager.GetCityAt(record.origin.x,record.origin.y)
   local now=c and ref(c);local native=c and getters(c) or {}
   local state='HELD';local reason='当前对象缺失或证据不足'
   if now and same(now,record.origin) then state='ORIGIN_REFERENCE';reason='原引用一致；不据此证明永久generation'
   elseif now then
    local removed,transferred=false,false
    -- Only events from this load, same observed turn. Persisted old events cannot authorize a new mapping.
    local turn=Game.GetCurrentGameTurn()
    for _,e in ipairs(events)do if e.turn==turn then
     if e.name=='CityRemovedFromMap' and e.args[1]==record.origin.owner and e.args[2]==record.origin.cityID then removed=true end
     if e.name=='CityTransfered' and e.args[1]==now.owner and e.args[2]==now.cityID then transferred=true end
     if e.name=='CityConquered' and e.args[1]==now.owner and e.args[2]==record.origin.owner and e.args[3]==now.cityID and e.args[4]==now.x and e.args[5]==now.y then transferred=true end
    end end
    if not overflow and removed and transferred and (native.GetOwnerBeforeOccupation==record.origin.owner or native.GetJustConqueredFrom==record.origin.owner) then
     state='MAPPING_CANDIDATE';reason='移除/转移事件与原生旧Owner相符；仍仅实验候选'
    else reason='新引用已观察；尚缺可靠旧Owner或同次转移证据' end
   end
   -- Explicit read/checkpoint only; event callbacks never write. On cold load retain saved evidence separately.
   if #events>0 then
    local v=cp(record);v.current=now;v.native=native;v.state=state;v.events=cp(events);v.overflow=overflow
    if not same(v,record) then save(v) end
   end
   local lines={P.VERSION..' | 单城保存实验','Game记录已读取；编号：'..record.token,'本次核对：'..reason,
    '已保存状态：'..record.state..'；修订 '..record.revision,
    '原引用：'..record.origin.owner..'/'..record.origin.cityID,
    '当前引用：'..(now and now.owner..'/'..now.cityID or '无城市'),
    '本次加载事件 '..#events..'；存档保留事件 '..#record.events,
    '只保存实验；未认领身份、迁移账本或发放收益。',
    overflow and '事件缓冲已满：证据不完整，保持待确认。' or '事件缓冲：正常'}
   if #events==0 and record.current then lines[#lines+1]='保存时引用与当前：'..(same(now,record.current) and '一致（非永久身份认证）' or '不同/不可读；不自动重配')end
   for _,name in ipairs({'GetOriginalOwner','GetOwnerBeforeOccupation','GetJustConqueredFrom','GetLastTransferType'})do lines[#lines+1]=name..'='..tostring(native[name] or 'UNKNOWN')end
   return table.concat(lines,'\n')
  end)
 end
 local function hook(ns,name,fn)local e=P.Field(ns,name);if e and type(e.Add)=='function'then e.Add(fn)end end
 local function observe(name,...)
  if not ready or not record or d.error then return end
  local a={...};local o=record.origin
  local endpoint=a[1]==o.owner and a[2]==o.cityID
  local coords=(a[3]==o.x and a[4]==o.y) or (a[4]==o.x and a[5]==o.y)
  -- Transfer lacks coordinates: at most one watched-plot lookup, only on a transfer callback.
  if name=='CityTransfered' then local c=CityManager.GetCityAt(o.x,o.y);endpoint=endpoint or (c and a[1]==c:GetOwner() and a[2]==c:GetID())end
  if not endpoint and not coords then return end
  local args={};for i=1,math.min(select('#',...),8)do local v=select(i,...);args[i]=(type(v)=='number' or type(v)=='boolean') and v or (type(v)=='string' and v:sub(1,64) or 'UNKNOWN')end
  local e={name=name,args=args,turn=Game.GetCurrentGameTurn()}
  for _,old in ipairs(events)do if same(e,old)then return end end
  if #events>=16 then overflow=true;return end
  events[#events+1]=e
 end
 for _,name in ipairs({'CityTransfered','CityRemovedFromMap','CityAddedToMap','CityInitialized'})do local n=name;hook(Events,n,function(...)local ok=pcall(observe,n,...);if not ok then d.error='事件观察失败，未写入'end end)end
 for _,name in ipairs({'CityBuilt','CityConquered'})do local n=name;hook(GameEvents,n,function(...)local ok=pcall(observe,n,...);if not ok then d.error='事件观察失败，未写入'end end)end
 hook(Events,'LoadScreenClose',function()events={};overflow=false;d.error=nil;ready=false;local ok,v=pcall(read);if ok then record=v;ready=true else d.error=tostring(v)end end)
end
