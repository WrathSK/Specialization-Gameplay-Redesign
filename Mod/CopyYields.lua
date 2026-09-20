include('RuntimeWork')
include('SampleLifecycle')
-- B051: absolute city-layer copy yields. No permanent design facts or history-derived routes.
SPCCopyYields={}
function SPCCopyYields.Plan(amount,pop)
 assert(type(amount)=='number' and amount==amount and amount>=0 and amount<=65535.5 and amount*2%1==0,'COPY_PRECISION_UNSUPPORTED')
 local integer=math.floor(amount);local half=amount~=integer;local coefficient,bit=0,nil
 if half then
  assert(type(pop)=='number' and pop%1==0 and pop>=1 and pop<=255,'COPY_POPULATION_UNSUPPORTED')
  local odd=pop;bit=0;while odd%2==0 do odd=odd/2;bit=bit+1 end
  coefficient=1/2^(bit+1);integer=integer-(odd-1)/2
 end
 return {integer=integer,bit=bit,coefficient=coefficient,amount=amount}
end
function SPCCopyYields.Start(P,shared)
 local batch
 local function readFacts(pid,c) return batch and batch.Facts(pid,c) or shared.EffectiveFacts.Read(pid,c) end
 local data={ready=false,busy=false,generation=0,samples={},seq={},receiveErrors={},errors={},last={},changes=0};shared.CopyYields=data
 SPCSampleLifecycle.Reset(data,'copy')
 local function currentDistricts(pid) return batch and batch.Live(pid,false) or SPCSampleLifecycle.Live(P,pid,false) end
 local function sample(pid)
  if batch and batch.copyRows and batch.copyRows[pid] then return batch.copyRows[pid] end
  local s=data.samples[pid];assert(s,'COPY_BACKGROUND_PENDING')
  local live=currentDistricts(pid);local rows={}
  local retired=false
  for key,r in pairs(s.rows) do if not live[key] or live[key].reference~=r.reference then retired=true end end
  for key,d in pairs(live) do
   local r=s.rows[key];assert(r or retired,'COPY_BACKGROUND_PENDING')
   -- Changed reference is confirmed loss of that old observation, not a reusable value.
   if r and r.reference==d.reference then rows[key]=r end
  end
  if batch then batch.copyRows=batch.copyRows or {};batch.copyRows[pid]=rows end
  return rows
 end
 local function target(pid,c,y)
  if not P.IsTestPlayer(pid) or c:GetOwner()~=pid then return 0 end
  local f=readFacts(pid,c)
  assert(type(f.specialization)=='string' and type(f.active)=='number','COPY_FACTS_UNAVAILABLE')
  local ok,ids=pcall(shared.NetworkBridge.CurrentRecipientSources or shared.NetworkBridge.RecipientSources,pid,c,'INDUSTRY')
  if not ok then
   local b=shared.NetworkBridge.players and shared.NetworkBridge.players[pid]
   if b and b.validity=='CONFIRMED_INVALID' then return 0 end
   error(ids)
  end
  if #ids==0 then return 0 end
  local best=0;local rows
  for _,id in ipairs(ids) do
   local source=Players[pid]:GetCities():FindID(id)
   if source and source:GetOwner()==pid then
   local sf=readFacts(pid,source)
   assert(type(sf.specialization)=='string' and type(sf.active)=='number','COPY_FACTS_UNAVAILABLE')
   if sf.specialization=='INDUSTRY' and sf.active==4 then
    rows=rows or sample(pid);local d=rows[id..':'..sf.first.districtID]
    if d and d.type=='DISTRICT_INDUSTRIAL_ZONE' and sf.first.type==d.type then best=math.max(best,d.production*0.5) end
   end
   end
  end
  return best
 end
 local function row(y,mode,bit) return assert(P.Info('Buildings','BUILDING_SPC_B051_'..y..'_'..mode..'_'..bit),'B051_DATABASE_MISSING') end
 local function reconcile(c,y,plan,confirmed)
  local b=c:GetBuildings();local removed=false
  for _,add in ipairs({false,true}) do for _,mode in ipairs({'POS','NEG','POP'}) do
   for bit=0,(mode=='POP' and 7 or 15) do
    local n=plan.integer;local want=mode=='POP' and plan.bit==bit or
     (mode=='POS' and n>0 and math.floor(n/2^bit)%2==1) or
     (mode=='NEG' and n<0 and math.floor(-n/2^bit)%2==1)
    want=want==true
    if want==add then
     local id=row(y,mode,bit).Index;local has=P.HasBuilding(b,id);assert(type(has)=='boolean','COPY_CARRIER_UNKNOWN')
     if has~=want then
      if want then P.CreateBuilding(c:GetBuildQueue(),id) else P.RemoveBuilding(b,id);removed=true end
      assert(P.HasBuilding(b,id)==want,'COPY_WRITE_UNCONFIRMED');data.changes=data.changes+1
     end
    end
   end
  end end
  if removed and plan.amount==0 and confirmed then P.Count('copy_withdraw') end
 end
 function data.Audit(scope) P.Count('audit_copy');
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true;batch=SPCRuntimeWork.New(P,shared)
  for pid,p in pairs(Players) do if P.IsTestPlayer(pid) and SPCRuntimeWork.Player(scope,pid) then
   local ok,why=pcall(function()
    for _,c in p:GetCities():Members() do P.Count('city_scan'); for _,y in ipairs({'PRODUCTION'}) do
     local key=pid..':'..c:GetID()..':'..y
     local good,plan=pcall(function() return SPCCopyYields.Plan(target(pid,c,y),c:GetPopulation()) end)
     local reason=not good and tostring(plan) or nil
     local precision=reason and (reason:find('COPY_PRECISION_UNSUPPORTED',1,true) or reason:find('COPY_POPULATION_UNSUPPORTED',1,true))
     if not good and precision then plan=SPCCopyYields.Plan(0,1) end
     local wrote,err=false,nil
     if good or precision then wrote,err=pcall(reconcile,c,y,plan,good) end
     data.errors[key]=reason or (not wrote and tostring(err) or nil)
     if wrote then data.last[key]=plan end
    end end
   end)
   if not ok then print('[SPC][B051][AUDIT_ERROR] '..tostring(why)) end
  end end
  data.busy=false;batch=nil
 end
 function data.Receive(pid,p)
  if SPCSampleLifecycle.Receive(P,data,'copy',pid,p,false) then data.Audit({player=pid}) end
 end
 function data.Describe(pid,c)
  local lines={'B051.67自动复制 | city='..c:GetID()..' | 人口='..c:GetPopulation()}
  local function code(err) return tostring(err):match('COPY_[A-Z_]+') or tostring(err):match('SAMPLE_[A-Z_]+') or tostring(err):match('B051_[A-Z_]+') or tostring(err):match('NETWORK_[A-Z_]+') or 'COPY_GAMEPLAY_EXCEPTION' end
  local bg=ExposedMembers.SPC_CopyBackground
  local s=data.samples[pid]
  lines[#lines+1]='后台='..(bg and tostring(bg.state) or '未启动')..' | 请求='..(bg and tostring(bg.requests) or '0')..' | 接收序号='..tostring(data.seq[pid] or '无')..' | 有效批次='..(s and tostring(s.turn) or '无')
  if bg and bg.error then lines[#lines+1]='后台原因：'..bg.error end
  if data.receiveErrors[pid] then lines[#lines+1]='接收原因：'..code(data.receiveErrors[pid]) end
  for _,y in ipairs({'PRODUCTION'}) do
   local key=pid..':'..c:GetID()..':'..y;local plan=data.last[key];local err=data.errors[key]
   local good,n=pcall(target,pid,c,y)
   lines[#lines+1]=y..' 本项预期='..(good and tostring(n) or '暂不可判断')..' | 已配置='..(plan and tostring(plan.amount) or '未知')
   if err then
    print('[SPC][B051][DETAIL] '..err)
    lines[#lines+1]='本项原因：'..code(err)
    local message=err:find('PRECISION_UNSUPPORTED',1,true) and '数值不是支持的半点倍数/超出范围，未取整。' or
     (err:find('SCOPE_UNRESOLVED',1,true) and '存在范围未确认区域，未发放部分结果。' or '当前数据暂不可用时保留已验证收益；确认失效才撤销，详情见日志。')
    lines[#lines+1]=message
   end
  end
  lines[#lines+1]='原生总量 Science='..c:GetYield(P.Info('Yields','YIELD_SCIENCE').Index)..' / Production='..c:GetYield(P.Info('Yields','YIELD_PRODUCTION').Index)
  if c:GetProperty('SPC_B050_HALF_ENABLED') then lines[#lines+1]='注意：B050半点实验仍开启，请先Half OFF。' end
  lines[#lines+1]='读取不触发刷新；已配置不是实测增量。'
  return table.concat(lines,'\n')
 end
 local function hook(source,n,f) local e=P.Field(source,n);if e and e.Add then e.Add(f) end end
 -- Only lifecycle cleanup visits ineligible owners; no periodic specialization work for them.
 local function cleanupDormant()
  for pid,p in pairs(Players) do if not P.IsTestPlayer(pid) then
   local ok,err=pcall(function() for _,c in p:GetCities():Members() do P.Count('city_scan');
    for _,y in ipairs({'PRODUCTION'}) do reconcile(c,y,SPCCopyYields.Plan(0,1),true) end
   end end)
   if not ok then print('[SPC][B051][CLEANUP_ERROR] '..tostring(err)) end
  end end
 end
 hook(Events,'LoadScreenClose',function() data.ready=true;SPCSampleLifecycle.Reset(data,'copy');data.receiveErrors={};cleanupDormant();data.Audit() end)
 hook(Events,'CityTransfered',cleanupDormant)
 for _,n in ipairs({'PlayerTurnActivated','CityPopulationChanged','GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','CityTransfered','DistrictRemovedFromMap'}) do SPCRuntimeWork.Hook(P,Events,n,data.Audit) end
end
