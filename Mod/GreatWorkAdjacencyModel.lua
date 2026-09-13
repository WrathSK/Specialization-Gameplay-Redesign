-- D0023: pure BASE vector; never uses actual or city-total yields.
SPCGWAdjacencyModel={Yields={'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'}}
local M=SPCGWAdjacencyModel
function M.Parts(base)
 assert(type(base)=='number' and base==base and base%1==0 and math.abs(base)<=8191,'GWA_BASE_PRECISION_OR_DIRECTORY')
 local n=math.abs(base);local parts={};local sign=base<0 and 'N' or 'P'
 for bit=0,12 do if n%2==1 then parts[#parts+1]=sign..bit end;n=math.floor(n/2) end
 return parts
end
function M.Collect(P,pid)
 local rows={}
 for _,d in Players[pid]:GetDistricts():Members() do
  local c=d:GetCity();local def=P.Info('Districts',d:GetType())
  if c and c:GetOwner()==pid and def and def.RequiresPopulation and def.RequiresPopulation~=0 and d:IsComplete() then
   local r={c:GetID(),d:GetID(),def.DistrictType};local plot=assert(Map.GetPlot(d:GetX(),d:GetY()),'GWA_PLOT')
   for _,y in ipairs(M.Yields) do
    local n=plot:GetAdjacencyYield(pid,c:GetID(),d:GetType(),P.Info('Yields','YIELD_'..y).Index)
    M.Parts(n);r[#r+1]=n
   end
   rows[#rows+1]=table.concat(r,',')
  end
 end
 table.sort(rows);return table.concat(rows,';'),#rows
end
