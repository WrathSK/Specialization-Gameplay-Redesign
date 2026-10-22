-- Pure presentation; never infer an ACTIVE value from Potential.
SPCLevelBannerModel={}
local M=SPCLevelBannerModel
M.Colors={RESEARCH={139,221,233,255},CULTURE={211,127,229,255},INDUSTRY={239,189,104,255},COMMERCE={228,216,120,255}}
function M.View(v,pid,id,x,y)
 if type(v)~='table' or v.owner~=pid or v.cityID~=id or v.x~=x or v.y~=y
  or not M.Colors[v.specialization] or v.activeStatus~='KNOWN' then return nil end
 local a,p=v.active,v.potential
 if type(a)~='number' or type(p)~='number' or a%1~=0 or p%1~=0 or a<1 or a>p or p>4 then return nil end
 local segments={};for i=1,4 do segments[i]=i<=a and 'FILLED' or i<=p and 'OUTLINED' or 'DIM'end
 return {icon='ICON_SPC_LEVEL_'..v.specialization..'_'..a,kind=v.specialization,active=a,potential=p,segments=segments}
end
