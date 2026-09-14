-- D0020 read-only per-work basis and difference plan. No modifiers or city-total feedback.
SPCGreatWorkBasis={}
local cultural={WRITING=true,MUSIC=true,SCULPTURE=true,PORTRAIT=true,LANDSCAPE=true,RELIGIOUS=true,ARTIFACT=true}
local function number(n)
 assert(type(n)=='number' and n==n and n>=0 and n<math.huge,'GW_BASIS_INVALID');return n
end
function SPCGreatWorkBasis.Plan(works)
 local groups={CULTURE={count=0,first=0,tourism=0,totalFirst=0,totalTourism=0},RELIC={count=0,first=0,tourism=0,totalFirst=0,totalTourism=0}}
 local seen,rows={},{}
 for _,w in ipairs(works) do
  assert(w.id~=nil,'GW_ID_MISSING')
  assert(not seen[w.id],'GW_DUPLICATE_WORK');seen[w.id]=true
  local t=(w.object or ''):gsub('GREATWORKOBJECT_','')
  local group=cultural[t] and 'CULTURE' or nil
  if group then
   local first=number(group=='CULTURE' and w.culture or w.faith);local tour=number(w.tourism)
   local g=groups[group];g.count=g.count+1;g.first=math.max(g.first,first);g.tourism=math.max(g.tourism,tour)
   rows[#rows+1]={id=w.id,name=w.name,group=group,baseFirst=first,baseTourism=tour}
  end
 end
 for _,w in ipairs(rows) do local g=groups[w.group]
  w.addFirst=g.first-w.baseFirst;w.addTourism=g.tourism-w.baseTourism
  g.totalFirst=g.totalFirst+w.addFirst;g.totalTourism=g.totalTourism+w.addTourism
 end
 return {groups=groups,rows=rows,excluded=#works-#rows}
end
function SPCGreatWorkBasis.Collect(P,c)
 local yields={}
 for r in GameInfo.GreatWork_YieldChanges() do
  local y=yields[r.GreatWorkType] or {};yields[r.GreatWorkType]=y
  y[r.YieldType]=(y[r.YieldType] or 0)+number(r.YieldChange)
 end
 local b=c:GetBuildings();local seen,works={},{}
 for r in GameInfo.Buildings() do if P.HasBuilding(b,r.Index) then
  local n=b:GetNumGreatWorkSlots(r.Index)
  assert(type(n)=='number' and n>=0 and n%1==0,'GW_SLOT_COUNT_UNKNOWN')
  for slot=0,n-1 do
   local id=b:GetGreatWorkInSlot(r.Index,slot)
   if id and id~=-1 then
    assert(not seen[id],'GW_DUPLICATE_SLOT');seen[id]=true
    local w=assert(P.Info('GreatWorks',b:GetGreatWorkTypeFromIndex(id)),'GW_TYPE_UNKNOWN')
    local y=yields[w.GreatWorkType] or {}
    works[#works+1]={id=id,name=Locale.Lookup(w.Name),object=w.GreatWorkObjectType,culture=y.YIELD_CULTURE or 0,faith=y.YIELD_FAITH or 0,tourism=number(w.Tourism),building=r.Index,slot=slot}
   end
  end
 end end
 table.sort(works,function(a,b) return a.id<b.id end)
 return works
end
function SPCGreatWorkBasis.Describe(P,c)
 local ok,out=pcall(function()
  local p=SPCGreatWorkBasis.Plan(SPCGreatWorkBasis.Collect(P,c))
  local rows={'D0020基础补齐计划（未发放；倍率/主题化尚未接入）'}
  for _,kind in ipairs({'CULTURE'}) do local g=p.groups[kind]
   rows[#rows+1]=string.format('%s组%d件 | 最高基础 %g / %g旅游 | 应补总量 %g / %g旅游',kind=='CULTURE' and '文化' or '遗物信仰',g.count,g.first,g.tourism,g.totalFirst,g.totalTourism)
  end
  for i=1,math.min(4,#p.rows) do local w=p.rows[i]
   rows[#rows+1]=string.format('%s | 基础%g/%g旅游 → 补%g/%g旅游',w.name,w.baseFirst,w.baseTourism,w.addFirst,w.addTourism)
  end
  if #p.rows>4 then rows[#rows+1]='另有'..(#p.rows-4)..'件已计入；显示前4件。' end
  rows[#rows+1]='排除遗物/产品/未知类型='..p.excluded..'；按当前作品重算，不保存最高值。'
  return table.concat(rows,'\n')
 end)
 return ok and out or ('巨作基础读取未完成：'..tostring(out))
end
