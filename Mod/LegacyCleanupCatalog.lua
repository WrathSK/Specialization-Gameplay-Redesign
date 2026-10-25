-- Pure exact legacy ownership only. Explicit metadata, no native access or hooks.
if not SPCTombstones then include('Tombstones')end
SPCLegacyCleanupCatalog={}
function SPCLegacyCleanupCatalog.Build(eraCount,boostRows,integerRows)
 assert(type(eraCount)=='number'and eraCount>=1 and eraCount<2147483648 and eraCount%1==0,'LEGACY_ERA_DIRECTORY_UNKNOWN')
 local out,seen={},{}
 local function add(key,names,kind)
  local row={key=key,kind=kind or 'buildings',names={}};local own={}
  for _,name in ipairs(names)do
   assert(type(name)=='string'and not own[name]and not seen[name],'LEGACY_DUPLICATE_OR_INVALID_NAME')
   assert(kind=='plot_flags'or name:match('^BUILDING_SPC_[A-Z0-9_]+$'),'LEGACY_NON_INTERNAL_NAME')
   own[name]=true;seen[name]=true;row.names[#row.names+1]=name
  end
  assert(#row.names>0,'LEGACY_DIRECTORY_EMPTY');table.sort(row.names);out[#out+1]=row
 end
 add('YieldCarrierProbe',{'SPC_B029_ONE','SPC_B029_HALF'},'plot_flags')
 local half={};for _,y in ipairs({'SCIENCE','PRODUCTION'})do for _,mode in ipairs({'POP','SUB'})do for bit=0,7 do
  half[#half+1]='BUILDING_SPC_B050_'..y..'_'..mode..'_'..bit
 end end end;add('HalfYieldProbe',half)
 add('GreatWorkProbe',{'BUILDING_SPC_B055_GW_CITY','BUILDING_SPC_B055_GW_OBJECT'})
 add('PurchaseProbe',{'BUILDING_SPC_B053_FIXTURE','BUILDING_SPC_B053_DISCOUNT'})
 add('Lv3Support',SPCTombstones.Names('SpecialistSupport'))
 local lv3=SPCTombstones.Names('Lv3Culture')
 for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY'})do lv3[#lv3+1]='BUILDING_SPC_DEV_LV3_COM_'..kind end
 add('Lv3Effects',lv3);add('Lv4Percent',SPCTombstones.Names('Lv4Culture'))
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
 add('NetworkBoost',boost)
 local adjacency={}
 for _,y in ipairs({'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'})do for _,sign in ipairs({'P','N'})do for bit=0,12 do
  adjacency[#adjacency+1]='BUILDING_SPC_B060_'..y..'_'..sign..bit
 end end end;add('GreatWorkAdjacency',adjacency)
 local dialogue={};for n=2,eraCount do dialogue[#dialogue+1]='BUILDING_SPC_B059_D'..n end
 for _,n in ipairs({25,50,100,200})do dialogue[#dialogue+1]='BUILDING_SPC_B059_TEST'..n end
 add('Dialogue',dialogue);add('CommerceConvergence',SPCTombstones.Names('CommerceConvergence'))
 return out -- caller-owned lists; no retained per-city or historical cache
end
