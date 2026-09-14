-- B050 explicitly enabled precision experiment. No network/effect automation.
SPCHalfYieldProbe={}
function SPCHalfYieldProbe.Plan(pop)
 assert(type(pop)=='number' and pop%1==0 and pop>=1 and pop<=255,'POPULATION_OUT_OF_PROBE_RANGE')
 local odd,bit=pop,0
 while odd%2==0 do odd=odd/2;bit=bit+1 end
 return {bit=bit,coefficient=1/2^(bit+1),subtract=(odd-1)/2}
end
function SPCHalfYieldProbe.Start(P,shared)
 local data={ready=false,busy=false,errors={},baseline={}};shared.HalfYieldProbe=data
 local key='SPC_B050_HALF_ENABLED'
 local function name(y,mode,bit) return 'BUILDING_SPC_B050_'..y..'_'..mode..'_'..bit end
 local function totals(c)
  return {science=c:GetYield(P.Info('Yields','YIELD_SCIENCE').Index),production=c:GetYield(P.Info('Yields','YIELD_PRODUCTION').Index),population=c:GetPopulation()}
 end
 local function reconcile(pid,c,plan)
  for _,adding in ipairs({false,true}) do
   for _,y in ipairs({'SCIENCE','PRODUCTION'}) do for _,mode in ipairs({'POP','SUB'}) do for bit=0,7 do
    local row=P.Info('Buildings',name(y,mode,bit));assert(row,'B050_DATABASE_MISSING')
    local want=plan~=nil and ((mode=='POP' and plan.bit==bit) or (mode=='SUB' and math.floor(plan.subtract/2^bit)%2==1))
    if want==adding then
     local b=c:GetBuildings();local has=P.HasBuilding(b,row.Index)
     if has~=want then
      if want then P.CreateBuilding(c:GetBuildQueue(),row.Index) else P.RemoveBuilding(b,row.Index) end
      assert(P.HasBuilding(b,row.Index)==want,'B050_WRITE_UNCONFIRMED')
     end
    end
   end end end
  end
 end
 function data.Audit()
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true
  for pid,p in pairs(Players) do
   local ok,err=pcall(function()
    for _,c in p:GetCities():Members() do P.Count('city_scan');
     local enabled=c:GetProperty(key)==true
     if enabled then
      local good,plan=pcall(function() assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'OWNER_CHANGED');return SPCHalfYieldProbe.Plan(c:GetPopulation()) end)
      local applied,why=pcall(reconcile,pid,c,good and plan or nil)
      data.errors[pid..':'..c:GetID()]=not good and tostring(plan) or (not applied and tostring(why) or nil)
     end
    end
   end)
   if not ok then print('[SPC][B050][AUDIT] '..tostring(err)) end
  end
  data.busy=false
 end
 function data.Describe(pid,c)
  local enabled=c:GetProperty(key)==true;local t=totals(c);local base=data.baseline[pid..':'..c:GetID()]
  local text='B050固定半点实验 | city='..c:GetID()..' | '..(enabled and 'ON' or 'OFF')..' | 人口='..t.population
  if enabled then
   local ok,p=pcall(SPCHalfYieldProbe.Plan,t.population)
   if ok then text=text..'\n配置：人口×'..p.coefficient..' - '..p.subtract..' = 0.5（科技、生产力各一份；非实测）' end
  end
  text=text..'\n原生总量：Science='..t.science..' / Production='..t.production
  if base and base.population==t.population then text=text..'\n相对本次ON前：Science='..(t.science-base.science)..' / Production='..(t.production-base.production)..'（含原生倍率/其它变化）' end
  local err=data.errors[pid..':'..c:GetID()]
  if err then print('[SPC][B050][DETAIL] '..err);text=text..'\n应用未完成，详情已写日志，请关闭实验。' end
  return text
 end
 function data.Run(pid,c,action)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'OWN_TEST_CITY_REQUIRED')
  if action=='HALF_ON' then
   SPCHalfYieldProbe.Plan(c:GetPopulation())
   if c:GetProperty(key)~=true then data.baseline[pid..':'..c:GetID()]=totals(c) end
   P.SetProperty(c,key,true);data.ready=true;data.Audit()
  elseif action=='HALF_OFF' then
   -- Revoke carriers before clearing flag, so an uncertain removal can be retried.
   reconcile(pid,c,nil);P.SetProperty(c,key,false);data.errors[pid..':'..c:GetID()]=nil
  end
  return data.Describe(pid,c)
 end
 local function hook(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f) end end
 hook('LoadScreenClose',function() data.ready=true;data.Audit() end)
 for _,n in ipairs({'CityPopulationChanged','PlayerTurnActivated','CityTransfered'}) do hook(n,data.Audit) end
end
