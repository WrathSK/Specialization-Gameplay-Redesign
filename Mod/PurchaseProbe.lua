-- B053 manual currency-isolation fixture, never a network effect.
SPCPurchaseProbe={}
function SPCPurchaseProbe.Start(P,shared)
 local d={};shared.PurchaseProbe=d
 local function row(kind) local r=P.Info('Buildings','BUILDING_SPC_B053_'..kind);assert(r,'B053_DATABASE_MISSING');return r end
 local function set(c,kind,want)
  local r=row(kind);local b=c:GetBuildings()
  if b:HasBuilding(r.Index)~=want then
   if want then c:GetBuildQueue():CreateBuilding(r.Index) else b:RemoveBuilding(r.Index) end
  end
  assert(b:HasBuilding(r.Index)==want,'B053_CARRIER_UNCONFIRMED')
 end
 function d.Describe(c)
  local b=c:GetBuildings();local fixture=b:HasBuilding(row('FIXTURE').Index);local discount=b:HasBuilding(row('DISCOUNT').Index)
  return 'B053货币隔离实验 | city='..c:GetID()..'\n双币测试条件='..tostring(fixture)..' | 20%测试折扣='..tostring(discount)
   ..'\n对象：纪念碑、粮仓。只在此城测试，不接网络。'
   ..'\nBASE临时开放本城市中心建筑信仰购买；OFF完全撤销实验。'
 end
 function d.Run(pid,c,action)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'B053_TEST_CITY_REQUIRED')
  if action=='PURCHASE_BASE' then set(c,'DISCOUNT',false);set(c,'FIXTURE',true)
  elseif action=='PURCHASE_ON' then
   assert(c:GetBuildings():HasBuilding(row('FIXTURE').Index),'B053_BASE_REQUIRED');set(c,'DISCOUNT',true)
  elseif action=='PURCHASE_OFF' then set(c,'DISCOUNT',false);set(c,'FIXTURE',false) end
  return d.Describe(c)
 end
 local e=P.Field(Events,'LoadScreenClose')
 if e and e.Add then e.Add(function()
  -- Reload always leaves the experiment OFF, including a captured former test city.
  for _,p in pairs(Players) do for _,c in p:GetCities():Members() do
   local ok,err=pcall(function() set(c,'DISCOUNT',false);set(c,'FIXTURE',false) end)
   if not ok then print('[SPC][B053][CLEANUP] '..tostring(err)) end
  end end
 end) end
end
