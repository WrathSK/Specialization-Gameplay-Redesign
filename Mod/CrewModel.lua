-- B237 pure Crew definitions. No native calls or mutable runtime ownership.
SPCCrewModel={
 -- Stable native IDs are not capacity values; preserve existing unit provenance.
 IDS={250,420,750,1000,1360},
 CAPACITY={260,420,750,1000,1360},
 RATIOS={150,140,130,120},
 UNIT_PROPERTY='SPC_CREW_SOURCE_V1',
 ORDER_PROPERTY='SPC_CREW_ORDERS_V1',
 RECEIPT_PROPERTY='SPC_CREW_GRANTS_V1'
}
local M=SPCCrewModel
function M.Copy(v)if type(v)~='table'then return v end;local o={};for k,x in pairs(v)do o[k]=M.Copy(x)end;return o end
function M.Same(a,b)
 if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
 for k,v in pairs(a)do if not M.Same(v,b[k])then return false end end
 for k in pairs(b)do if a[k]==nil then return false end end;return true
end
function M.Int(v)return type(v)=='number' and v>=0 and v<1000000000 and v%1==0 end
function M.Project(tier,ratio,speed)
 local base=assert(M.CAPACITY[tier]);local id='PROJECT_SPC_CREW_'..M.IDS[tier]..(ratio==150 and '' or '_P'..ratio)
 if speed and math.floor(math.floor(base*ratio/100)*speed/100)~=M.Cost(tier,ratio,speed)then id=id..'_S'..speed end
 return id
end
function M.Marker(tier,ratio)return 'BUILDING_SPC_CREW_ACCESS_'..M.IDS[tier]..'_'..ratio end
function M.Parse(id)
 if type(id)~='string'then return end
 local base,speed=id:match('^(PROJECT_SPC_CREW_[%d_P]+)_S(%d+)$');speed=tonumber(speed)
 for tier in ipairs(M.CAPACITY)do for _,ratio in ipairs(M.RATIOS)do
  if M.Project(tier,ratio)==id or base==M.Project(tier,ratio) and speed and speed>0 and speed<10000 and M.Project(tier,ratio,speed)==id then return tier,ratio end
 end end
end
function M.Multiplier(active,N)
 assert(M.Int(active) and active<=4,'CREW_ACTIVE_UNKNOWN')
 if active<3 then return nil end;if active==3 then return 150 end
 assert(M.Int(N),'CREW_N_UNKNOWN');return N>=6 and 120 or N>=3 and 130 or N>=1 and 140 or 150
end
function M.Amount(tier,speed)
 assert(type(speed)=='number' and speed>0 and speed<10000,'CREW_SPEED_UNKNOWN')
 return math.floor(assert(M.CAPACITY[tier],'CREW_TIER_UNKNOWN')*speed/100)
end
function M.Cost(tier,ratio,speed)
 assert(ratio==150 or ratio==140 or ratio==130 or ratio==120,'CREW_RATIO_UNKNOWN')
 return math.floor(M.Amount(tier,speed)*ratio/100)
end
function M.ValidateUnit(v,pid,kind)
 assert(type(v)=='table' and v.version==1 and v.owner==pid and M.Int(v.tier)
  and kind=='UNIT_SPC_CREW_'..tostring(M.IDS[v.tier]) and M.Int(v.capacity) and v.capacity>0
  and type(v.source)=='string' and #v.source>0 and M.Int(v.x) and M.Int(v.y)
  and type(v.grant)=='string' and #v.grant>0,'CREW_SOURCE_UNAVAILABLE')
 return v
end
return M
