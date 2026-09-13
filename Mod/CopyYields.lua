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
 local data={ready=false,busy=false,generation=0,samples={},seq={},receiveErrors={},errors={},last={},changes=0};shared.CopyYields=data
 local function integer(n) return type(n)=='number' and n>=0 and n%1==0 end
 local function city(pid,id) local c=Players[pid]:GetCities():FindID(id);assert(c and c:GetOwner()==pid,'COPY_CITY_OWNER');return c end
 local function currentDistricts(pid)
  local out={}
  for _,d in Players[pid]:GetDistricts():Members() do
   local c=d:GetCity();local row=P.Info('Districts',d:GetType())
   if c and c:GetOwner()==pid and d:IsComplete() and row then
    out[c:GetID()..':'..d:GetID()]={cityID=c:GetID(),id=d:GetID(),type=row.DistrictType}
   end
  end
  return out
 end
 local function sample(pid)
  local s=data.samples[pid];assert(s and s.turn==Game.GetCurrentGameTurn(),'COPY_BACKGROUND_PENDING')
  local live=currentDistricts(pid)
  for key,d in pairs(live) do assert(s.rows[key] and s.rows[key].type==d.type,'COPY_DISTRICT_SET_CHANGED') end
  for key in pairs(s.rows) do assert(live[key],'COPY_DISTRICT_SET_CHANGED') end
  return s.rows
 end
 local function target(pid,c,y)
  if not P.IsTestPlayer(pid) or c:GetOwner()~=pid then return 0 end
  local f=shared.EffectiveFacts.Read(pid,c)
  if y=='SCIENCE' then
   if f.specialization~='RESEARCH' or f.active~=4 then return 0 end
   local rows=sample(pid);local sum=0;local anchor=false
   for _,d in pairs(rows) do if d.cityID==c:GetID() then
    if d.id==f.first.districtID and d.type==f.first.type and d.type=='DISTRICT_CAMPUS' then anchor=true end
    if d.type~='DISTRICT_CAMPUS' then
     sum=sum+d.total
    end
   end end
   assert(anchor,'COPY_RESEARCH_ANCHOR');return sum*0.5
  end
  local ids=shared.NetworkBridge.RecipientSources(pid,c,'INDUSTRY')
  if #ids==0 then return 0 end
  local best=0;local rows
  for _,id in ipairs(ids) do
   local source=city(pid,id);local sf=shared.EffectiveFacts.Read(pid,source)
   if sf.specialization=='INDUSTRY' and sf.active==4 then
    rows=rows or sample(pid);local d=rows[id..':'..sf.first.districtID]
    assert(d and d.type=='DISTRICT_INDUSTRIAL_ZONE' and sf.first.type==d.type,'COPY_INDUSTRY_ANCHOR')
    best=math.max(best,d.production*0.5)
   end
  end
  return best
 end
 local function row(y,mode,bit) return assert(P.Info('Buildings','BUILDING_SPC_B051_'..y..'_'..mode..'_'..bit),'B051_DATABASE_MISSING') end
 local function reconcile(c,y,plan)
  local b=c:GetBuildings()
  for _,add in ipairs({false,true}) do for _,mode in ipairs({'POS','NEG','POP'}) do
   for bit=0,(mode=='POP' and 7 or 15) do
    local n=plan.integer;local want=mode=='POP' and plan.bit==bit or
     (mode=='POS' and n>0 and math.floor(n/2^bit)%2==1) or
     (mode=='NEG' and n<0 and math.floor(-n/2^bit)%2==1)
    want=want==true
    if want==add then
     local id=row(y,mode,bit).Index;local has=b:HasBuilding(id);assert(type(has)=='boolean','COPY_CARRIER_UNKNOWN')
     if has~=want then
      if want then c:GetBuildQueue():CreateBuilding(id) else b:RemoveBuilding(id) end
      assert(b:HasBuilding(id)==want,'COPY_WRITE_UNCONFIRMED');data.changes=data.changes+1
     end
    end
   end
  end end
 end
 function data.Audit()
  if not data.ready or data.busy then return end;data.busy=true
  for pid,p in pairs(Players) do if P.IsTestPlayer(pid) then
   local ok,why=pcall(function()
    for _,c in p:GetCities():Members() do for _,y in ipairs({'SCIENCE','PRODUCTION'}) do
     local key=pid..':'..c:GetID()..':'..y
     local good,plan=pcall(function() return SPCCopyYields.Plan(target(pid,c,y),c:GetPopulation()) end)
     local reason=not good and tostring(plan) or nil
     if not good then plan=SPCCopyYields.Plan(0,1) end
     local wrote,err=pcall(reconcile,c,y,plan)
     data.errors[key]=reason or (not wrote and tostring(err) or nil)
     data.last[key]=wrote and plan or nil
    end end
   end)
   if not ok then print('[SPC][B051][AUDIT_ERROR] '..tostring(why)) end
  end end
  data.busy=false
 end
 function data.Receive(pid,p)
  if not data.ready or p.Generation~=data.generation or not P.IsTestPlayer(pid) or not integer(p.Seq) or p.Seq<=(data.seq[pid] or -1) then return end
  data.seq[pid]=p.Seq;data.samples[pid]=nil
  local ok,err=pcall(function()
   assert(p.Turn==Game.GetCurrentGameTurn() and p.Valid==1,'COPY_SAMPLE_INVALID')
   assert(type(p.Data)=='string' and #p.Data<=60000,'COPY_SAMPLE_SIZE')
   local live=currentDistricts(pid);local rows={};local count=0
   for line in p.Data:gmatch('[^;]+') do
    local a,b,total,prod=line:match('^(%d+),(%d+),([^,]+),([^,]+)$');a=tonumber(a);b=tonumber(b);total=tonumber(total);prod=tonumber(prod)
    assert(a and b and type(total)=='number' and type(prod)=='number' and total==total and prod==prod and math.abs(total)<1e8 and math.abs(prod)<1e8,'COPY_ROW_INVALID')
    local key=a..':'..b;local d=assert(live[key],'COPY_STALE_DISTRICT');assert(not rows[key],'COPY_DUPLICATE')
    rows[key]={cityID=a,id=b,type=d.type,total=total,production=prod};count=count+1;assert(count<=512,'COPY_ROW_LIMIT')
   end
   assert(count==p.Count,'COPY_PARTIAL_BATCH')
   for key in pairs(live) do assert(rows[key],'COPY_PARTIAL_BATCH') end
   data.samples[pid]={turn=p.Turn,rows=rows}
  end)
  data.receiveErrors[pid]=not ok and tostring(err) or nil
  if not ok then print('[SPC][B051][SAMPLE_ERROR] '..tostring(err)) end
  data.Audit()
 end
 function data.Describe(pid,c)
  local lines={'B051.67自动复制 | city='..c:GetID()..' | 人口='..c:GetPopulation()}
  local function code(err) return tostring(err):match('COPY_[A-Z_]+') or tostring(err):match('B051_[A-Z_]+') or tostring(err):match('NETWORK_[A-Z_]+') or 'COPY_GAMEPLAY_EXCEPTION' end
  local bg=ExposedMembers.SPC_CopyBackground
  local s=data.samples[pid]
  lines[#lines+1]='后台='..(bg and tostring(bg.state) or '未启动')..' | 请求='..(bg and tostring(bg.requests) or '0')..' | 接收序号='..tostring(data.seq[pid] or '无')..' | 有效批次='..(s and tostring(s.turn) or '无')
  if bg and bg.error then lines[#lines+1]='后台原因：'..bg.error end
  if data.receiveErrors[pid] then lines[#lines+1]='接收原因：'..code(data.receiveErrors[pid]) end
  for _,y in ipairs({'SCIENCE','PRODUCTION'}) do
   local key=pid..':'..c:GetID()..':'..y;local plan=data.last[key];local err=data.errors[key]
   local good,n=pcall(target,pid,c,y)
   lines[#lines+1]=y..' 本项预期='..(good and tostring(n) or '暂不可判断')..' | 已配置='..(plan and tostring(plan.amount) or '未知')
   if err then
    print('[SPC][B051][DETAIL] '..err)
    lines[#lines+1]='本项原因：'..code(err)
    local message=err:find('PRECISION_UNSUPPORTED',1,true) and '数值不是支持的半点倍数/超出范围，未取整。' or
     (err:find('SCOPE_UNRESOLVED',1,true) and '存在范围未确认区域，未发放部分结果。' or '当前数据/资格未就绪，本项已尝试撤销；详情见日志。')
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
   local ok,err=pcall(function() for _,c in p:GetCities():Members() do
    for _,y in ipairs({'SCIENCE','PRODUCTION'}) do reconcile(c,y,SPCCopyYields.Plan(0,1)) end
   end end)
   if not ok then print('[SPC][B051][CLEANUP_ERROR] '..tostring(err)) end
  end end
 end
 hook(Events,'LoadScreenClose',function() data.ready=true;data.generation=data.generation+1;data.samples={};data.seq={};data.receiveErrors={};cleanupDormant();data.Audit() end)
 hook(Events,'CityTransfered',cleanupDormant)
 for _,n in ipairs({'PlayerTurnActivated','CityPopulationChanged','GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','CityTransfered','DistrictRemovedFromMap'}) do hook(Events,n,data.Audit) end
end
