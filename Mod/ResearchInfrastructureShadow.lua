-- D0031 RES_L4_INFRA only: pure desired plan, never applies a yield/carrier.
SPCResearchInfrastructureShadow={}
local M=SPCResearchInfrastructureShadow
-- Only the shadow reader needs workers. Use the already indexed city districts;
-- D is highest single Campus, while working Campus specialists are counted once each.
function M.WithWorkers(f,d)
 local input=SPCDistrictCompleteness.Clone(f)
 if f.validity~='VERIFIED' or f.identity~='RESEARCH' or f.active~=4
  or d.validity~='VERIFIED' or d.availability~='READY' then return input end
 local ok,n=pcall(function()
  local total=0
  for _,r in ipairs(d.value.districts) do
   if r.domain=='DISTRICT_CAMPUS' and r.complete and not r.pillaged then
    local plot=assert(Map.GetPlotByIndex(r.plot),'RI_CAMPUS_PLOT_UNAVAILABLE')
    local count=plot:GetWorkerCount()
    assert(type(count)=='number' and count>=0 and count<math.huge and count%1==0,'RI_WORKERS_UNKNOWN')
    total=total+count
   end
  end
  return total
 end)
 if ok then input.workers=n else input.workerError=tostring(n) end
 return input
end
function M.Plan(f,d)
 local p={ability='RES_L4_INFRA',mode='SHADOW_ONLY',appliedScience=0}
 if f.validity~='VERIFIED' or f.active==nil then p.status='UNKNOWN';return p end
 if f.identity~='RESEARCH' or f.active<4 then p.status='INACTIVE';p.science=0;return p end
 if d.validity~='VERIFIED' or d.availability~='READY' or not d.value then p.status='HELD_COMPLETENESS';return p end
 if f.workers==nil then p.status='UNKNOWN_WORKERS';p.reason=f.workerError;return p end
 local campus=d.value.domains.DISTRICT_CAMPUS
 if not campus then p.status='NO_ELIGIBLE_CAMPUS';p.science=0;return p end
 p.status='READY';p.workers=f.workers;p.d=campus.value;p.selectedDistrict=campus.districtID;p.science=p.d*p.workers
 return p
end
function M.Describe(P,shared,pid,city)
 local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,city)
 local d=shared.DistrictCompleteness.Read(pid,city,f.token)
 local p=M.Plan(M.WithWorkers(f,d),d)
 local lines={P.VERSION..' | P0-A 区域完善度 / Research Infrastructure SHADOW_ONLY',
  '只读影子计算；实际新增收益=0；旧writer保持运行。',
  '专业='..tostring(f.identity)..' Potential='..tostring(f.potential)..' ACTIVE='..tostring(f.active)..' facts='..f.validity..' ACTIVE status='..tostring(f.activeStatus),
  'D validity='..d.validity..' availability='..d.availability..' revision='..tostring(d.revision)}
 if f.reason then lines[#lines+1]=f.reason end;if d.error then lines[#lines+1]='保留上次完整事实，不当作0：'..d.error end
 if d.value then
  for _,r in ipairs(d.value.districts) do
   local selected=r.domain and d.value.domains[r.domain]
   lines[#lines+1]=r.type..' #'..r.id..' domain='..tostring(r.domain)..' complete='..tostring(r.complete)..' pillaged='..tostring(r.pillaged)
   for _,b in ipairs(r.buildings) do
    local label=b.name and Locale and Locale.Lookup and Locale.Lookup(b.name) or b.type
    lines[#lines+1]='  '..label..' ['..b.type..'] Tier='..tostring(b.tier)..' contribution='..b.contribution
     ..' pillaged='..tostring(b.pillaged)..' reason='..tostring(b.reason)..' tierSource='..tostring(b.tierSource)
   end
   lines[#lines+1]='  cap前='..r.uncapped..' cap后='..r.value..' /10；最高单区域='..tostring(selected and selected.districtID==r.id or false)
  end
  for _,b in ipairs(d.value.excluded) do lines[#lines+1]=b.type..' contribution=0 pillaged='..tostring(b.pillaged)..' reason='..b.reason end
 end
 lines[#lines+1]='科研基础设施影子：'..p.status..' | D='..tostring(p.d)..' × working specialists='..tostring(p.workers)..' → Science='..tostring(p.science)
 lines[#lines+1]='这是D0031预期值，不是当前城市已获得的收益；旧Copy/百分比与新规则不同，不做数值相等断言。'
 return table.concat(lines,'\n')
end
