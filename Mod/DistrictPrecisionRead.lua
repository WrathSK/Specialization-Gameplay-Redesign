-- Read native UI getters only on an explicit DP_READ response, never on a timer.
SPCDistrictPrecisionRead={}
local baseline -- one selected-city sample, no history
local results={} -- at most four explicit-stage summaries for that city
local function number(n) assert(type(n)=='number' and n==n and math.abs(n)<math.huge,'DP_NATIVE_UNKNOWN');return n end
function SPCDistrictPrecisionRead.Render(P,v,token)
 local ok,text=pcall(function()
  assert(v and v.token==token and v.owner==Game.GetLocalPlayer(),'DP_VIEW_UNAVAILABLE')
  local c=assert(Players[v.owner]:GetCities():FindID(v.city),'DP_CITY_UNAVAILABLE')
  local y=P.Info('Yields','YIELD_SCIENCE').Index
  local d,found=nil,0
  for _,r in c:GetDistricts():Members() do
   local typ=P.Info('Districts',r:GetType()).DistrictType;local match=typ=='DISTRICT_CAMPUS'
   for _,x in ipairs(P.Rows('DistrictReplaces') or {}) do if x.CivUniqueDistrictType==typ and x.ReplacesDistrictType=='DISTRICT_CAMPUS' then match=true end end
   if match then found=found+1;d=r end
  end
  assert(found==1 and d:IsComplete() and not d:IsPillaged(),'DP_ONE_READY_CAMPUS_REQUIRED')
  local key=table.concat({v.owner,v.city,c:GetX(),c:GetY(),d:GetID(),d:GetX(),d:GetY()},':')
  local n={key=key,district=number(d:GetYield(y)),adjacency=number(d:GetAdjacencyYield(y)),
   base=number(Map.GetPlot(d:GetX(),d:GetY()):GetAdjacencyYield(v.owner,v.city,d:GetType(),y)),
   city=number(c:GetYield(y)),pop=c:GetPopulation(),turn=Game.GetCurrentGameTurn()}
  if baseline and baseline.key~=key then baseline=nil;results={} end
  local restarted=baseline and v.amount==0 and (baseline.pop~=n.pop or baseline.turn~=n.turn)
  if restarted then baseline=nil;results={} end
  if not baseline and v.amount==0 then baseline=n end
  local out={'原生读数：学院科技 '..string.format('%.6f',n.district)..'；学院相邻 '..string.format('%.6f',n.adjacency),
   'Plot BASE '..string.format('%.6f',n.base)..'；城市科技 '..string.format('%.6f',n.city)}
  if restarted then out[#out+1]='回合/人口已变化：已用当前OFF读数重新建立基线。' end
  if baseline then
   assert(v.amount==0 or v.amount==0.3 or v.amount==0.5 or v.amount==1,'DP_STAGE_UNKNOWN')
   results[v.amount]=string.format('配置 %s → 区域 Δ%+.6f / 城市 Δ%+.6f',tostring(v.amount),n.district-baseline.district,n.city-baseline.city)
   out[#out+1]=string.format('相邻 Δ%+.6f / Plot BASE Δ%+.6f',n.adjacency-baseline.adjacency,n.base-baseline.base)
   for _,a in ipairs({0.3,0.5,1,0}) do if results[a] then out[#out+1]=results[a] end end
   if baseline.pop~=n.pop or baseline.turn~=n.turn then out[#out+1]='注意：回合/人口已变化，对照可能混入其它收益。' end
  else out[#out+1]='缺少OFF基线：先右键关闭，再读数；不要据城市总量单独判PASS。' end
  return table.concat(out,'\n')
 end)
 return ok and text or ('原生读数 UNKNOWN：'..(tostring(text):match('DP_[A-Z_]+') or '接口暂不可用')..'；不作精度结论。')
end
