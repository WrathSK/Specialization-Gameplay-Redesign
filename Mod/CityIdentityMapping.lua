-- E1 explicit one-city experiment. Never consumed as gameplay identity or migrated progress.
SPCCityIdentityMapping={KEY='SPC_E1_IDENTITY_MAPPING_EXPERIMENT_V2'}
function SPCCityIdentityMapping.Start(P,shared)
 local M=SPCCityIdentityMapping;local cp=SPCCityIdentityRead.Copy
 local d={error=nil};shared.CityIdentityExperiment=d
 local record,ready,restored=nil,false,false
 local events,overflow={},false
 local function same(a,b)
  if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
  for k,v in pairs(a)do if not same(v,b[k])then return false end end
  for k in pairs(b)do if a[k]==nil then return false end end;return true
 end
 local function int(v)return type(v)=='number' and v>=0 and v<1000000000 and v%1==0 end
 local function validRef(v)return type(v)=='table' and int(v.owner) and int(v.cityID) and int(v.x) and int(v.y)end
 local function ref(c)return c and {owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()}end
 local function validate(raw)
  local v=cp(raw);if v==nil then return nil end
  assert(type(v)=='table' and v.schema==2 and v.experiment=='ONE_CITY_MAPPING_ONLY','实验格式不兼容')
  assert(int(v.revision) and v.revision>0 and int(v.requester) and validRef(v.originRef) and validRef(v.currentRef),'实验引用损坏')
  assert(type(v.originToken)=='string' and v.candidateKey=='E1V2:'..v.originToken and v.requester==v.originRef.owner,'实验编号冲突')
  assert(({ORIGIN_VERIFIED=true,TRANSFER_PENDING=true,MAPPED_EXPERIMENT=true,HELD=true})[v.mappingState],'实验状态损坏')
  assert(type(v.reason)=='string','实验原因缺失')
  if v.mappingState=='ORIGIN_VERIFIED'then assert(same(v.currentRef,v.originRef) and v.transition==nil,'起点冲突')end
  if v.transition~=nil then
   local t=v.transition;assert(type(t)=='table' and same(t.fromRef,v.originRef) and int(t.turn),'转移记录损坏')
   assert(t.toRef==nil or validRef(t.toRef),'目标引用损坏')
   assert(type(t.evidence)=='table' and #t.evidence<=16,'证据超限')
   for _,e in ipairs(t.evidence)do assert(type(e)=='table' and type(e.name)=='string' and int(e.turn) and type(e.args)=='table' and #e.args<=8,'证据格式损坏')end
  end
  if v.mappingState=='MAPPED_EXPERIMENT'then
   assert(v.transition and same(v.transition.toRef,v.currentRef),'保存映射不一致')
   local state=SPCCityIdentityExperiment.Shadow(v.originRef,v.currentRef,v.transition.evidence,false,v.transition.turn)
   assert(state=='SHADOW_CANDIDATE','保存证据不完整')
  end
  return v
 end
 local function read()return validate(Game:GetProperty(M.KEY))end
 local function save(v)
  assert(not d.error,'写入已暂停');assert(same(read(),record),'实验记录已被改变')
  v=cp(v);v.revision=(record and record.revision or 0)+1;validate(v)
  Game:SetProperty(M.KEY,v);assert(same(read(),v),'写入未确认，停止重试');record=cp(v)
 end
 local function held(reason)
  if not record or record.mappingState=='HELD'then return end
  local v=cp(record);v.mappingState='HELD';v.reason=reason;save(v)
 end
 local function initialize()
  if ready then return true end
  local ok,raw=pcall(function()return Game:GetProperty(M.KEY)end)
  if not ok then return false end
  record=validate(raw);ready=true;restored=record~=nil
  if record then
   local now=ref(CityManager.GetCityAt(record.originRef.x,record.originRef.y))
   if record.mappingState=='TRANSFER_PENDING'then held('读档时转移尚未确认，不重放旧事件')
   elseif record.mappingState~='HELD' and now and not same(now,record.currentRef)then held('读档对象与保存引用不一致')end
  end
  return true
 end
 local function guard(phase,fn,...)
  if d.error then return '身份映射实验暂停：'..d.error end
  local ok,result=pcall(fn,...)
  if not ok then d.error=phase..'：'..(tostring(result):match('^[^\r\n]*') or '读取失败'):gsub('^.-:%d+: ',''):sub(1,120);return '身份映射实验暂停：'..d.error end
  return result
 end
 local function evaluate()
  if not record or record.mappingState~='TRANSFER_PENDING'then return end
  if overflow then held('事件缓冲不完整');return end
  local t=record.transition
  if Game.GetCurrentGameTurn()~=t.turn then held('转移未在观察回合内完成');return end
  local now=ref(CityManager.GetCityAt(record.originRef.x,record.originRef.y))
  local state,why=SPCCityIdentityExperiment.Shadow(record.originRef,now,events,overflow,t.turn)
  if state=='SHADOW_CANDIDATE'then
   local v=cp(record);v.currentRef=now;v.mappingState='MAPPED_EXPERIMENT';v.reason='单次转移证据已自动保存'
   v.transition.toRef=now;v.transition.evidence=cp(events);save(v)
  elseif now then
   -- Missing/temporarily unavailable evidence can wait; contradictory evidence cannot.
   if why~='缺少原引用移除证据' and why~='缺少新引用加入证据' and why~='缺少含旧Owner的Gameplay转移事件' and why~='原引用未变；不证明永久身份'then held(why)end
  end
 end
 function d.Begin(pid,c)
  return guard('登记',function()
   if not P.IsTestPlayer(pid)then return '当前玩家不在测试范围。'end
   if not c or c:GetOwner()~=pid then return '请选择己方分城。'end
   if not initialize()then return 'Game记录暂不可读，请稍后手动重试。'end
   if record then return '已有单城映射实验，不覆盖。请左键“实验对照”。'end
   local values={};for k,key in pairs(SPCCityIdentityRead.Keys)do values[k]=c:GetProperty(key)end
   local token=values.TOKEN
   if type(token)~='string' or tonumber(token:match('^DEV%-B013%-P(%d+)%-'))~=pid then return '原绑定凭据不完整，未写入。'end
   local snap={ref=ref(c),values=values,ledger=Game:GetProperty('SPC_DEV_BINDING_B013_P'..pid)}
   if SPCCityIdentityRead.Preview(snap).state~='LOCAL_CANDIDATE'then return '原账本未通过核对，未写入。'end
   save({schema=2,experiment='ONE_CITY_MAPPING_ONLY',requester=pid,candidateKey='E1V2:'..token,originToken=token,
    originRef=ref(c),currentRef=ref(c),mappingState='ORIGIN_VERIFIED',reason='原范围已登记',revision=1})
   return '单城映射实验已建立。转自由城后不点诊断，直接另存读档，再左键“实验对照”。'
  end)
 end
 function d.Describe(pid)
  return guard('核对',function()
   if not P.IsTestPlayer(pid)then return '当前玩家不在测试范围。'end
   if not initialize()then return 'Game记录暂不可读，请稍后手动重试。'end
   if not record then return '未启用新映射实验；选择己方分城，右键“记录城市身份”。旧实验记录保持不变。'end
   if record.requester~=pid then return '这是另一玩家的实验。'end
   evaluate()
   local now=ref(CityManager.GetCityAt(record.originRef.x,record.originRef.y))
   if record.mappingState=='MAPPED_EXPERIMENT' and now and not same(now,record.currentRef)then held('当前对象与保存引用不一致')end
   local label=({ORIGIN_VERIFIED='原范围已登记',TRANSFER_PENDING='等待转移证据',MAPPED_EXPERIMENT=restored and '已保存映射恢复' or '单次映射已保存',HELD='暂停认领'})[record.mappingState]
   if not now then label='当前对象暂不可读，尚未核对恢复'end
   return table.concat({P.VERSION..' | 单城持久映射',label..'：'..record.reason,
    '编号：'..record.candidateKey,'原Owner '..record.originRef.owner..' → 保存Owner '..record.currentRef.owner,
    '保存修订 '..record.revision..'；当前对象'..(same(now,record.currentRef) and '一致' or '不同/不可读'),
    '仅单次自由城实验；未迁移专业记录或收益。'},'\n')
  end)
 end
 local function observe(name,...)
  if not ready or not record or record.mappingState=='HELD'then return end
  local a={...};local o=record.originRef;local n=record.currentRef
  local endpoint=(a[1]==o.owner and a[2]==o.cityID) or (a[1]==n.owner and a[2]==n.cityID)
  for _,e in ipairs(events)do if e.name=='CityBuilt' or e.name=='CityAddedToMap' or e.name=='CityInitialized'then endpoint=endpoint or (a[1]==e.args[1] and a[2]==e.args[2])end end
  local coords=(name=='CityBuilt' or name=='CityAddedToMap' or name=='CityInitialized') and a[3]==o.x and a[4]==o.y
  if name=='CityConquered'then coords=a[4]==o.x and a[5]==o.y end
  if name=='CityTransfered' or name=='CulturalIdentityCityConverted' or name=='CityLiberated'then
   local c=CityManager.GetCityAt(o.x,o.y);endpoint=endpoint or (c and a[1]==c:GetOwner() and a[2]==c:GetID())
  end
  if not endpoint and not coords then return end
  local args={};for i=1,math.min(select('#',...),8)do local v=select(i,...);args[i]=(type(v)=='number' or type(v)=='boolean') and v or (type(v)=='string' and v:sub(1,64) or 'UNKNOWN')end
  local e={name=name,args=args,turn=Game.GetCurrentGameTurn()}
  if name=='CityConquered' or name=='CityLiberated'then held('该易主路径不在单次自由城实验范围');return end
  if record.mappingState=='MAPPED_EXPERIMENT'then
   for _,old in ipairs(record.transition.evidence)do if same(e,old)then return end end
   if e.turn==record.transition.turn then
    local newRef=args[1]==n.owner and args[2]==n.cityID
    if name=='CityTransfered' and newRef then return end
    if name=='CulturalIdentityCityConverted' and newRef and args[3]==o.owner then return end
    if (name=='CityBuilt' or name=='CityAddedToMap' or name=='CityInitialized') and newRef and args[3]==n.x and args[4]==n.y then return end
    if name=='CityRemovedFromMap' and args[1]==o.owner and args[2]==o.cityID then return end
   end
   held('映射后出现额外变化，不接续第二次转移');return
  end
  for _,old in ipairs(events)do if same(e,old)then return end end
  if #events>=16 then overflow=true;held('事件缓冲不完整');return end
  events[#events+1]=e
  if record.mappingState=='ORIGIN_VERIFIED'then
   local v=cp(record);v.mappingState='TRANSFER_PENDING';v.reason='等待同次转移证据';v.transition={fromRef=cp(o),turn=e.turn,evidence={}};save(v)
  end
  evaluate()
 end
 local function hook(ns,name,fn)local e=P.Field(ns,name);if e and type(e.Add)=='function'then e.Add(fn)end end
 for _,name in ipairs({'CityTransfered','CityRemovedFromMap','CityAddedToMap','CityInitialized','CulturalIdentityCityConverted','CityLiberated'})do local n=name;hook(Events,n,function(...)if not ready or not record or d.error or record.mappingState=='HELD'then return end;guard('事件/'..n,observe,n,...)end)end
 for _,name in ipairs({'CityBuilt','CityConquered'})do local n=name;hook(GameEvents,n,function(...)if not ready or not record or d.error or record.mappingState=='HELD'then return end;guard('事件/'..n,observe,n,...)end)end
 hook(Events,'LoadScreenClose',function()guard('加载',initialize)end)
 guard('加载',initialize) -- cold load watch does not depend on opening diagnostics
end
