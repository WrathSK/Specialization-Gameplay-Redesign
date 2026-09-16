include('RuntimeWork')
-- One current native player boost per kind, carried by the capital. Never grants progress.
include('BoostConfig')
include('BoostIntegerConfig')
SPCNetworkBoost={}
-- The boundary accepts FinalRawBoost AFTER all future float modifiers. No default round.
function SPCNetworkBoost.Quantize(finalRaw)
 assert(type(finalRaw)=='number' and finalRaw==finalRaw and finalRaw>=0 and finalRaw<math.huge,'B057_RAW_INVALID')
 return math.floor(finalRaw+0.5)
end
local testRows={}
for _,kind in ipairs({'RESEARCH','CULTURE'}) do for _,amount in ipairs({2,4}) do
 testRows[#testRows+1]='BUILDING_SPC_B057_'..kind..'_'..amount
end end
function SPCNetworkBoost.Start(P,shared)
 local d={ready=false,busy=false,applied={},plans={},errors={},changes=0,testRaw={}};shared.NetworkBoost=d
 local kinds={'RESEARCH','CULTURE'}
 local function row(id) return assert(P.Info('Buildings',id),'B055_DATABASE_MISSING') end
 local function set(c,id,want)
  local r=row(id);local b=c:GetBuildings();local present=P.HasBuilding(b,r.Index)
  assert(type(present)=='boolean','B055_CARRIER_UNKNOWN')
  if present~=want then
   if want then P.CreateBuilding(c:GetBuildQueue(),r.Index) else P.RemoveBuilding(b,r.Index) end
   assert(P.HasBuilding(b,r.Index)==want,'B055_WRITE_UNCONFIRMED');d.changes=d.changes+1
  end
 end
 function d.Clean()
  -- Only initialization/ownership transitions scan for saved derived carriers.
  for _,player in pairs(Players) do local cities=player:GetCities();if cities then for _,c in cities:Members() do P.Count('city_scan');
   for _,r in pairs(SPCBoostConfig.rows) do set(c,r.building,false) end
   for _,id in pairs(SPCBoostIntegerConfig.rows) do if P.Info('Buildings',id) then set(c,id,false) end end
   for _,id in ipairs(testRows) do if P.Info('Buildings',id) then set(c,id,false) end end
  end end end
  d.applied={}
 end
 function d.Plan(pid)
  local result={}
  if d.testRaw[pid]~=nil then
   local raw=d.testRaw[pid];local applied=SPCNetworkBoost.Quantize(raw)
   for _,kind in ipairs(kinds) do
    local id=applied>0 and ('BUILDING_SPC_B057_'..kind..'_'..applied) or nil
    if id then row(id) end
    result[kind]={n=0,level=0,sources={},building=id,amount=applied,finalRaw=raw,test=true}
   end
   return result
  end
  local network=(shared.NetworkBridge.CurrentNational or shared.NetworkBridge.National)(pid)
  for _,kind in ipairs(kinds) do
   local source=network[kind];local n=source.n;local level=source.level
   assert(n<=SPCBoostConfig.maxRecipients,'B055_RECIPIENT_LIMIT')
   local raw=SPCBoostConfig.k[kind]*level*math.sqrt(n)
   -- All future efficiency modifiers must be applied HERE in floating point, before Quantize.
   local finalRaw=raw
   local applied=SPCNetworkBoost.Quantize(finalRaw)
   assert(applied<=SPCBoostIntegerConfig.maxApplied,'B058_INTEGER_CATALOG_LIMIT')
   local id=applied>0 and assert(SPCBoostIntegerConfig.rows[kind..':'..applied],'B058_INTEGER_MISSING') or nil
   if id then row(id) end
   result[kind]={n=n,level=level,sources=source.sources,building=id,amount=applied,raw=raw,finalRaw=finalRaw}
  end
  return result
 end
 function d.Audit(scope) P.Count('audit_boost');
  if not d.ready or d.busy then P.Count('busy_skip');return end;d.busy=true
  for pid,player in pairs(Players) do
   if SPCRuntimeWork.Player(scope,pid) and (P.IsTestPlayer(pid) or d.applied[pid]) then
    local ok,plan=pcall(function() if P.IsTestPlayer(pid) then return d.Plan(pid) end return {} end)
    d.errors[pid]=not ok and tostring(plan) or nil
    if not ok then plan={} end
    local capital=P.IsTestPlayer(pid) and player:GetCities():GetCapitalCity() or nil
    local old=d.applied[pid] or {};d.applied[pid]=old
    local written,why=pcall(function()
     -- Remove stale effects first; never combine sources/centers/modifier fragments.
     for _,kind in ipairs(kinds) do
      local want=capital and plan[kind] and plan[kind].building
      local entry=old[kind]
      if entry and (entry.building~=want or (entry.city:GetID()~=capital:GetID() or entry.city:GetOwner()~=pid)) then
       set(entry.city,entry.building,false);old[kind]=nil
      end
     end
     for _,kind in ipairs(kinds) do
      local want=capital and plan[kind] and plan[kind].building
      if want then set(capital,want,true);old[kind]={city=capital,building=want,amount=plan[kind].amount} end
     end
    end)
    if not written then d.errors[pid]=tostring(why);print('[SPC][B055][WRITE] '..tostring(why)) end
    d.plans[pid]=plan
   end
  end
  d.busy=false
 end
 function d.EnsureReady(pid)
  if not P.IsTestPlayer(pid) or d.busy then P.Count('busy_skip');return end
  if not d.ready then
   d.busy=true;local ok,err=pcall(d.Clean);d.busy=false
   if not ok then d.errors[pid]=tostring(err);return end
   d.ready=true
  end
  d.Audit()
 end
 function d.Test(pid,raw)
  assert(P.IsTestPlayer(pid),'B057_TEST_PLAYER_REQUIRED')
  if raw~=nil then
   local applied=SPCNetworkBoost.Quantize(raw)
   assert(applied==0 or applied==2 or applied==4,'B057_TEST_INPUT_UNSUPPORTED')
   if applied>0 then for _,kind in ipairs(kinds) do row('BUILDING_SPC_B057_'..kind..'_'..applied) end end
  end
  d.EnsureReady(pid);assert(d.ready,'B057_INIT_PENDING')
  d.testRaw[pid]=raw;d.Audit()
  return d.Describe(pid)
 end
 function d.Describe(pid)
  local out={d.testRaw[pid]~=nil and 'B057 整数接口实验：替换本Mod网络Boost（两种类型）' or 'B058 自动网络：全部浮点计算后一次四舍五入'}
  for _,kind in ipairs(kinds) do
   local p=d.plans[pid] and d.plans[pid][kind];local a=d.applied[pid] and d.applied[pid][kind]
   out[#out+1]=(kind=='RESEARCH' and '科研→鼓舞' or '文化→尤里卡')..(p and string.format(' | ACTIVE=%d N=%d | 预期+%.6f百分点',p.level,p.n,p.amount) or ' | 待后台刷新')
   if p and not p.test then out[#out+1]=string.format('Raw=%.6f FinalRaw=%.6f → Applied=%d',p.raw,p.finalRaw,p.amount) end
   out[#out+1]='配置='..tostring(a and a.amount or 0)..' | k='..SPCBoostConfig.k[kind]
  end
  if d.testRaw[pid]~=nil then out[#out+1]=string.format('FinalRaw=%.6f → floor(raw+0.5)=%d；重载退出实验',d.testRaw[pid],SPCNetworkBoost.Quantize(d.testRaw[pid])) end
  out[#out+1]='状态='..tostring(d.errors[pid] or (d.ready and 'READY' or 'PENDING'))
  out[#out+1]='配置≠实测；读取基线后同回合触发一次未触发的尤里卡/鼓舞，再读取。'
  return table.concat(out,'\n')
 end
 local function hook(src,n,fn) local e=P.Field(src,n);if e and e.Add then e.Add(fn) end end
 for _,n in ipairs({'PlayerTurnActivated'}) do SPCRuntimeWork.Hook(P,Events,n,d.Audit) end
 hook(Events,'CityTransfered',function() if d.ready and not d.busy then
  d.busy=true;local ok,err=pcall(d.Clean);d.busy=false
  if not ok then print('[SPC][B055][CLEAN] '..tostring(err));d.ready=false;return end;d.Audit()
 end end)
end
