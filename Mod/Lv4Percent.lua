-- P0-L1: exact old Culture IV worker-percent retirement owner.
-- Types/Buildings remain inert cleanup IDs. No old benefit is generated.
SPCLv4Percent={}
function SPCLv4Percent.Start(P,shared)
 local d={ready=false,busy=false,errors={},changes=0};shared.Lv4Percent=d
 local names={};for bit=0,7 do names[#names+1]='BUILDING_SPC_LV4_PERCENT_CULTURE_'..bit end
 function d.WithdrawCulture(c)
  local rows={};local b=c:GetBuildings()
  for _,name in ipairs(names)do
   local r=assert(P.Info('Buildings',name),'LV4_DATABASE_MISSING')
   local present=P.HasBuilding(b,r.Index);assert(type(present)=='boolean','LV4_CARRIER_UNKNOWN');rows[#rows+1]={id=r.Index,present=present}
  end
  for _,r in ipairs(rows)do if r.present then
   P.RemoveBuilding(b,r.id);assert(P.HasBuilding(b,r.id)==false,'LV4_REMOVE_UNCONFIRMED');d.changes=d.changes+1
  end end
  return true
 end
 function d.Audit()end -- compatibility only; L1 invokes the precise withdrawal once per relevant city
 function d.Describe(pid,c)
  return shared.CultureAesthetic and shared.CultureAesthetic.Describe(pid,c) or '旧文化专家百分比已退休；新能力等待确认。'
 end
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('Lv4Percent',function(c,loss)
  shared.CityProgressionStore.RemoveOwned(c,loss,names)
 end)end
end
