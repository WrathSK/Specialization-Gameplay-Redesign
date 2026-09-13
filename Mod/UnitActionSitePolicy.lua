-- Offline candidate only: not imported by modinfo or used by live actions.
-- Adapters must resolve and freshly validate target ownership/location in Gameplay.
SPCUnitActionSitePolicy={}
function SPCUnitActionSitePolicy.Check(action,unit,target)
 if type(unit)~='table' or type(target)~='table' then return false,'STATE_UNKNOWN' end
 if target.verified~=true then return false,'TARGET_UNVERIFIED' end
 if type(unit.owner)~='number' or unit.owner~=target.owner then return false,'OWN_TARGET_REQUIRED' end
 local function integer(v) return type(v)=='number' and v>=0 and v<math.huge and v%1==0 end
 if not integer(unit.plot) or not integer(target.plot) or not integer(target.cityID) then return false,'LOCATION_UNKNOWN' end
 if unit.plot~=target.plot then return false,'MOVE_TO_TARGET_PLOT' end
 if action=='CREW' then
  if unit.isCrew~=true or unit.charges~=1 then return false,'ONE_CHARGE_CREW_REQUIRED' end
  if target.kind~='BUILDING' and target.kind~='DISTRICT' and target.kind~='WONDER' then return false,'ILLEGAL_CONSTRUCTION' end
  if target.current~=true or target.complete~=false then return false,'CURRENT_INCOMPLETE_TARGET_REQUIRED' end
 elseif action=='INVESTMENT' then
  if unit.isSettler~=true then return false,'SETTLER_REQUIRED' end
  if target.kind~='DISTRICT' or target.complete~=true or target.identityAnchor~=true then return false,'COMPLETED_IDENTITY_DISTRICT_REQUIRED' end
  if not integer(target.potential) or target.potential<1 or target.potential>=4 then return false,'POTENTIAL_NOT_INVESTABLE' end
 else return false,'UNKNOWN_ACTION' end
 return true,'LEGAL_SITE'
end
