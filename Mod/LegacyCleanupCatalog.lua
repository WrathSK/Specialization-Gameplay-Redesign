-- Pure fixed ownership; each group can be resolved without unrelated metadata.
if not SPCTombstones then include('Tombstones')end
SPCLegacyCleanupCatalog={}
local C=SPCLegacyCleanupCatalog
local keys={'YieldCarrierProbe','HalfYieldProbe','GreatWorkProbe','PurchaseProbe','Lv3Support','Lv3Effects','Lv4Percent','NetworkBoost','GreatWorkAdjacency','Dialogue','CommerceConvergence'}
function C.Keys()local out={};for i,key in ipairs(keys)do out[i]=key end;return out end
function C.Group(key,eraCount,boostRows,integerRows)
 local names,kind={},'buildings'
 if key=='YieldCarrierProbe'then names={'SPC_B029_ONE','SPC_B029_HALF'};kind='plot_flags'
 elseif key=='HalfYieldProbe'then
  for _,y in ipairs({'SCIENCE','PRODUCTION'})do for _,mode in ipairs({'POP','SUB'})do for bit=0,7 do names[#names+1]='BUILDING_SPC_B050_'..y..'_'..mode..'_'..bit end end end
 elseif key=='GreatWorkProbe'then names={'BUILDING_SPC_B055_GW_CITY','BUILDING_SPC_B055_GW_OBJECT'}
 elseif key=='PurchaseProbe'then names={'BUILDING_SPC_B053_FIXTURE','BUILDING_SPC_B053_DISCOUNT'}
 elseif key=='Lv3Support'then names=SPCTombstones.Names('SpecialistSupport')
 elseif key=='Lv3Effects'then
  names=SPCTombstones.Names('Lv3Culture');for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY'})do names[#names+1]='BUILDING_SPC_DEV_LV3_COM_'..k end
 elseif key=='Lv4Percent'then names=SPCTombstones.Names('Lv4Culture')
 elseif key=='NetworkBoost'then
 assert(type(boostRows)=='table'and getmetatable(boostRows)==nil and next(boostRows),'LEGACY_BOOST_DIRECTORY_UNKNOWN')
 assert(type(integerRows)=='table'and getmetatable(integerRows)==nil and next(integerRows),'LEGACY_INTEGER_DIRECTORY_UNKNOWN')
 local boost={}
 local count=0
 for key,row in pairs(boostRows)do
  assert(type(key)=='string'and type(row)=='table'and getmetatable(row)==nil,'LEGACY_BOOST_ROW_UNKNOWN')
  local kind,weight,n=key:match('^(%u+):(%d+):(%d+)$');weight=tonumber(weight);n=tonumber(n)
  assert((kind=='RESEARCH'or kind=='CULTURE')and weight and weight>=1 and weight<=4 and n and n>=1 and n<=129
   and key==kind..':'..weight..':'..n and row.building=='BUILDING_SPC_B055_'..kind..'_'..weight..'_'..n,'LEGACY_BOOST_ROW_UNKNOWN')
  count=count+1;boost[#boost+1]=row.building
 end
 assert(count==1032,'LEGACY_BOOST_DIRECTORY_INCOMPLETE');count=0
 for key,name in pairs(integerRows)do
  assert(type(key)=='string','LEGACY_INTEGER_ROW_UNKNOWN')
  local kind,n=key:match('^(%u+):(%d+)$');n=tonumber(n)
  assert((kind=='RESEARCH'or kind=='CULTURE')and n and n>=1 and n<=45 and key==kind..':'..n
   and name=='BUILDING_SPC_B058_'..kind..'_'..n,'LEGACY_INTEGER_ROW_UNKNOWN')
  count=count+1;boost[#boost+1]=name
 end
 assert(count==90,'LEGACY_INTEGER_DIRECTORY_INCOMPLETE')
 for _,kind in ipairs({'RESEARCH','CULTURE'})do for _,n in ipairs({2,4})do boost[#boost+1]='BUILDING_SPC_B057_'..kind..'_'..n end end
 names=boost
 elseif key=='GreatWorkAdjacency'then
  for _,y in ipairs({'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'})do for _,sign in ipairs({'P','N'})do for bit=0,12 do names[#names+1]='BUILDING_SPC_B060_'..y..'_'..sign..bit end end end
 elseif key=='Dialogue'then
  assert(type(eraCount)=='number'and eraCount>=1 and eraCount<2147483648 and eraCount%1==0,'LEGACY_ERA_DIRECTORY_UNKNOWN')
  for n=2,eraCount do names[#names+1]='BUILDING_SPC_B059_D'..n end
  for _,n in ipairs({25,50,100,200})do names[#names+1]='BUILDING_SPC_B059_TEST'..n end
 elseif key=='CommerceConvergence'then names=SPCTombstones.Names('CommerceConvergence')
 else error('LEGACY_GROUP_UNKNOWN')end
 local seen={};for _,name in ipairs(names)do
  assert(type(name)=='string'and not seen[name],'LEGACY_DUPLICATE_OR_INVALID_NAME')
  assert(kind=='plot_flags'or name:match('^BUILDING_SPC_[A-Z0-9_]+$'),'LEGACY_NON_INTERNAL_NAME');seen[name]=true
 end
 assert(#names>0,'LEGACY_DIRECTORY_EMPTY');table.sort(names);return {key=key,kind=kind,names=names}
end
function C.Build(eraCount,boostRows,integerRows)
 local out,seen={},{}
 for _,key in ipairs(keys)do
  local row=C.Group(key,eraCount,boostRows,integerRows)
  for _,name in ipairs(row.names)do assert(not seen[name],'LEGACY_DUPLICATE_OR_INVALID_NAME');seen[name]=true end
  out[#out+1]=row
 end
 return out
end
