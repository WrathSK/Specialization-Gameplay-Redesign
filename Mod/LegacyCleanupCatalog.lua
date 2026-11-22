-- Pure fixed ownership; each group can be resolved without unrelated metadata.
if not SPCTombstones then include('Tombstones')end
SPCLegacyCleanupCatalog={}
local C=SPCLegacyCleanupCatalog
local keys={'YieldCarrierProbe','HalfYieldProbe','GreatWorkProbe','PurchaseProbe','Lv3Support','Lv3Effects','Lv4Percent','GreatWorkAdjacency','Dialogue','CommerceConvergence'}
function C.Keys()local out={};for i,key in ipairs(keys)do out[i]=key end;return out end
function C.Group(key,eraCount)
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
function C.Build(eraCount)
 local out,seen={},{}
 for _,key in ipairs(keys)do
  local row=C.Group(key,eraCount)
  for _,name in ipairs(row.names)do assert(not seen[name],'LEGACY_DUPLICATE_OR_INVALID_NAME');seen[name]=true end
  out[#out+1]=row
 end
 return out
end
