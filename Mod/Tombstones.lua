-- Exact retired IDs only. No native reads, writes, hooks or shared session state.
-- A retired writer does not imply inert SQL: Convergence's modifier rows remain
-- load-bearing cleanup targets until their separate retirement is approved.
SPCTombstones={}
local groups={ResearchCross={},ResearchInfrastructure={},SpecialistSupport={},Lv3Culture={},Lv4Culture={},CommerceConvergence={}}
local function add(group,name)groups[group][#groups[group]+1]=name end
for bit=0,7 do
 add('ResearchCross','BUILDING_SPC_DEV_LV3_POP_RESEARCH_'..bit)
 add('ResearchInfrastructure','BUILDING_SPC_LV4_PERCENT_RESEARCH_'..bit)
 add('Lv3Culture','BUILDING_SPC_DEV_LV3_POP_CULTURE_'..bit)
 add('Lv4Culture','BUILDING_SPC_LV4_PERCENT_CULTURE_'..bit)
end
for _,suffix in ipairs({'03','05','1'})do add('ResearchCross','BUILDING_SPC_B082_DISTRICT_'..suffix)end
for _,mode in ipairs({'POS','NEG','POP'})do for bit=0,(mode=='POP'and 7 or 15)do
 add('ResearchInfrastructure','BUILDING_SPC_B051_SCIENCE_'..mode..'_'..bit)
end end
for _,kind in ipairs({'RESEARCH','CULTURE','COMMERCE','INDUSTRY'})do add('SpecialistSupport','BUILDING_SPC_DEV_LV3_'..kind)end
for bit=0,7 do add('SpecialistSupport','BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_'..bit)end
for _,yield in ipairs({'SCIENCE','CULTURE','PRODUCTION'})do for bit=0,15 do add('CommerceConvergence','BUILDING_SPC_B061_'..yield..'_'..bit)end end
function SPCTombstones.Names(group)
 local names=assert(groups[group],'TOMBSTONE_GROUP_UNKNOWN');local out={}
 for i,name in ipairs(names)do out[i]=name end
 return out -- callers cannot mutate another owner's list
end
