-- B055 isolated backend comparison. Not automatic era preservation or GW-002 gameplay.
SPCGreatWorkProbe={}
function SPCGreatWorkProbe.Start(P,shared)
 local d={ready=false};shared.GreatWorkProbe=d
 local function set(c,mode,want)
  local r=assert(P.Info('Buildings','BUILDING_SPC_B055_GW_'..mode),'B055_GW_DATABASE_MISSING')
  local b=c:GetBuildings()
  if b:HasBuilding(r.Index)~=want then
   if want then c:GetBuildQueue():CreateBuilding(r.Index) else b:RemoveBuilding(r.Index) end
  end
  assert(b:HasBuilding(r.Index)==want,'B055_GW_WRITE_UNCONFIRMED')
 end
 function d.Clean()
  for _,p in pairs(Players) do local cities=p:GetCities();if cities then for _,c in cities:Members() do
   set(c,'CITY',false);set(c,'OBJECT',false)
  end end end;d.ready=true
 end
 function d.Run(pid,c,action)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'B055_GW_TEST_CITY_REQUIRED')
  if not d.ready then d.Clean() end
  if action~='GW_READ' then
   assert(action=='GW_CITY' or action=='GW_OBJECT' or action=='GW_OFF','B055_GW_ACTION')
   -- Mutually exclusive modes, remove before add; repeated clicks cannot stack.
   for _,m in ipairs({'CITY','OBJECT'}) do if action~='GW_'..m then set(c,m,false) end end
   if action=='GW_CITY' then set(c,'CITY',true) elseif action=='GW_OBJECT' then set(c,'OBJECT',true) end
  end
  local mode='OFF'
  for _,m in ipairs({'CITY','OBJECT'}) do
   local r=P.Info('Buildings','BUILDING_SPC_B055_GW_'..m)
   if c:GetBuildings():HasBuilding(r.Index) then mode=m end
  end
  return 'B055 巨作接口对照 | city='..c:GetID()..' | '..mode
   ..'\nCITY：整城固定+2基础文化；OBJECT：每件标准文化巨作+2文化。'
   ..'\n二者互斥；未配置旅游业加成；排除遗物、产品、未知类型。'
   ..'\n这是手动实验，不是已完成的时代补贴/50%基础相邻能力。'
 end
 local e=P.Field(Events,'CityTransfered');if e and e.Add then e.Add(function() if d.ready then d.Clean() end end) end
end
