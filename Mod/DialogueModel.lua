-- D0022 pure current-collection plan, shared by UI diagnostics and Gameplay.
SPCDialogueModel={}
local allowed={WRITING=true,MUSIC=true,SCULPTURE=true,PORTRAIT=true,LANDSCAPE=true,RELIGIOUS=true,ARTIFACT=true}
function SPCDialogueModel.Plan(P,works)
 local eras,seen={},{};local out={count=0,excluded=0,d=0,rows={}}
 for _,entry in ipairs(works) do
  assert(type(entry.id)=='number' and entry.id>=0 and entry.id%1==0 and not seen[entry.id],'DIALOGUE_WORK_ID');seen[entry.id]=true
  local w=assert(P.Info('GreatWorks',entry.type),'DIALOGUE_WORK_TYPE')
  local kind=(w.GreatWorkObjectType or ''):gsub('GREATWORKOBJECT_','')
  if allowed[kind] then
   local era
   if kind=='ARTIFACT' then era=w.EraType else
    local gp=assert(P.Info('GreatPersonIndividuals',w.GreatPersonIndividualType),'DIALOGUE_CREATOR_MISSING');era=gp.EraType
   end
   assert(era and P.Info('Eras',era),'DIALOGUE_ERA_MISSING')
   if not eras[era] then eras[era]=true;out.d=out.d+1 end
   out.count=out.count+1;out.rows[#out.rows+1]={name=w.Name,era=era,id=entry.id,artifact=kind=='ARTIFACT'}
  else out.excluded=out.excluded+1 end
 end
 out.percent=15*math.max(0,out.d-1);out.factor=100+out.percent;out.eras=eras
 return out
end
function SPCDialogueModel.Collect(P,c)
 local b=c:GetBuildings();local works={}
 for r in GameInfo.Buildings() do if b:HasBuilding(r.Index) then
  local n=b:GetNumGreatWorkSlots(r.Index);assert(type(n)=='number' and n>=0 and n%1==0,'DIALOGUE_SLOTS')
  for slot=0,n-1 do local id=b:GetGreatWorkInSlot(r.Index,slot)
   if id and id~=-1 then
    local row=assert(P.Info('GreatWorks',b:GetGreatWorkTypeFromIndex(id)),'DIALOGUE_WORK_TYPE')
    works[#works+1]={id=id,type=row.GreatWorkType}
   end
  end
 end end
 table.sort(works,function(a,b) return a.id<b.id end);return works
end
