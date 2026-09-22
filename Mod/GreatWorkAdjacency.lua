include('GreatWorkAdjacencyModel')
SPCGWAdjacency={}
function SPCGWAdjacency.Start(P,shared)
 local M=SPCGWAdjacencyModel
 local d={ready=false,busy=false,samples={},last={},off={},errors={}};shared.GreatWorkAdjacency=d
 local allowed={WRITING=true,MUSIC=true,SCULPTURE=true,PORTRAIT=true,LANDSCAPE=true,RELIGIOUS=true,ARTIFACT=true}
 local function key(y,part) return 'BUILDING_SPC_B060_'..y..'_'..part end
 local function carriers(c,want)
  local b=c:GetBuildings()
  -- Clear obsolete pieces before adding new pieces; each piece is a per-work amount.
  for _,y in ipairs(M.Yields) do for _,sign in ipairs({'P','N'}) do for bit=0,12 do
   local id=key(y,sign..bit);local r=P.Info('Buildings',id)
   assert(r,'GWA_DATABASE_MISSING')
   if P.HasBuilding(b,r.Index) and not want[id] then P.RemoveBuilding(b,r.Index);assert(not P.HasBuilding(b,r.Index),'GWA_REMOVE_FAILED') end
  end end end
  for id in pairs(want) do local r=P.Info('Buildings',id)
   if not P.HasBuilding(b,r.Index) then P.CreateBuilding(c:GetBuildQueue(),r.Index) end
   assert(P.HasBuilding(b,r.Index),'GWA_WRITE_FAILED')
  end
 end
 function d.Init()
  if d.ready then return end
  for _,p in pairs(Players) do local cities=p:GetCities();if cities then for _,c in cities:Members() do P.Count('city_scan'); carriers(c,{}) end end end
  d.ready=true
 end
 function d.Audit(pid)
  if not d.ready or d.busy or not P.IsTestPlayer(pid) then return end;d.busy=true
  d.last[pid]={}
  local rowsByCity={}
  for _,r in pairs(d.samples[pid] and d.samples[pid].rows or {}) do
   rowsByCity[r.city]=rowsByCity[r.city] or {};table.insert(rowsByCity[r.city],r)
  end
  for _,c in Players[pid]:GetCities():Members() do P.Count('city_scan');
   local ok,plan=pcall(function()
    local sample=d.samples[pid];local collection=shared.Dialogue.samples[pid]
    assert(sample and collection and sample.turn==Game.GetCurrentGameTurn() and collection.turn==sample.turn,'GWA_SAMPLE_PENDING')
    local f=shared.EffectiveFacts.Read(pid,c);local base={};for _,y in ipairs(M.Yields) do base[y]=0 end
    for _,r in pairs(rowsByCity[c:GetID()] or {}) do if r.city==c:GetID() then for i,y in ipairs(M.Yields) do base[y]=base[y]+r.values[i] end end end
    local count=0;for _,w in ipairs(collection.cities[c:GetID()] or {}) do
     local def=assert(P.Info('GreatWorks',w.type),'GWA_WORK_TYPE');local kind=def.GreatWorkObjectType:gsub('GREATWORKOBJECT_','')
     if allowed[kind] then count=count+1 end
    end
    local active=f.specialization=='CULTURE' and f.active==4 and not d.off[pid]
    local want={};for _,y in ipairs(M.Yields) do local parts=M.Parts(base[y]);if active and count>0 then for _,part in ipairs(parts) do want[key(y,part)]=true end end end
    return {base=base,count=count,active=active,want=want}
   end)
   if not ok then plan={error=tostring(plan),want={}} end
   local applied,why=pcall(carriers,c,plan.want);if not applied then plan.error=tostring(why) end
   d.last[pid][c:GetID()]=plan
  end
  d.busy=false
 end
 function d.Receive(pid,a)
  if not P.IsTestPlayer(pid) then return end
  local ok,result=pcall(function()
   d.Init()
   assert(type(a.AdjCount)=='number' and a.AdjCount>=0,'GWA_UI_BASE_READ_FAILED')
   assert(a.Valid==1 and a.Turn==Game.GetCurrentGameTurn() and type(a.AdjData)=='string' and #a.AdjData<=100000,'GWA_SAMPLE_INVALID')
   local expected={};for _,district in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
    local c=district:GetCity();local def=P.Info('Districts',district:GetType())
    if c and c:GetOwner()==pid and def and def.RequiresPopulation and def.RequiresPopulation~=0 and district:IsComplete() then expected[district:GetID()]={city=c:GetID(),kind=def.DistrictType} end
   end
   local rows={};local count=0
   for line in a.AdjData:gmatch('[^;]+') do
    local fields={};for field in line:gmatch('[^,]+') do fields[#fields+1]=field end
    assert(#fields==9,'GWA_ROW');local city,id=tonumber(fields[1]),tonumber(fields[2]);local e=expected[id]
    assert(e and e.city==city and e.kind==fields[3] and not rows[id],'GWA_DISTRICT_CHANGED')
    local values={};for i=4,9 do local n=tonumber(fields[i]);M.Parts(n);values[#values+1]=n end
    rows[id]={city=city,values=values};count=count+1
   end
   assert(count==a.AdjCount,'GWA_COUNT');for id in pairs(expected) do assert(rows[id],'GWA_INCOMPLETE') end
   return {turn=a.Turn,rows=rows}
  end)
  d.samples[pid]=ok and result or nil;d.errors[pid]=not ok and tostring(result) or nil;d.Audit(pid)
 end
 function d.Describe(pid,c)
  local p=d.last[pid] and d.last[pid][c:GetID()]
  if not p or p.error then return '巨作基础相邻未就绪：'..tostring(d.errors[pid] or (p and p.error) or '等待后台样本') end
  local rows={'B060 巨作BASE相邻 | '..(d.off[pid] and 'TEST OFF' or 'AUTO')..' | 合格作品='..p.count..' | 生效资格='..tostring(p.active)}
  for _,y in ipairs(M.Yields) do rows[#rows+1]=string.format('%s BASE=%g | 每件=%g | 配置合计(倍率前)=%g',y,p.base[y],p.base[y]/2,p.active and p.base[y]/2*p.count or 0) end
  rows[#rows+1]='配置不是实测；半点/作品倍率按下方原生读数验证。'
  return table.concat(rows,'\n')
 end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('GreatWorkAdjacency',function(c,loss)
   local ids={};for _,y in ipairs(M.Yields)do for _,sign in ipairs({'P','N'})do for bit=0,12 do ids[#ids+1]=key(y,sign..bit)end end end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end)end

 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterReturn('GreatWorkAdjacency',function(pid)d.samples={};d.last={} end)end

end
