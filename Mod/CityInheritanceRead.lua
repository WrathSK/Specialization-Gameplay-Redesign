-- B063 read-only observer. Coordinates locate a watched plot, NOT an adopted permanent UID.
SPCCityInheritanceRead={}
function SPCCityInheritanceRead.Start(P,shared)
 local d={watch={}};shared.CityInheritanceRead=d
 local keys={TOKEN='SPC_DEV_BINDING_B013_TOKEN',FLOW='SPC_DEV_CITY_FLOW_B020',JOURNAL='SPC_DEV_CITY_JOURNAL_B015',INVEST='SPC_DEV_INVESTMENT_LEDGER_V1',TEMPLATES='SPC_STANDARDIZATION_LEDGER_V1'}
 local order={'TOKEN','FLOW','JOURNAL','INVEST','TEMPLATES'}
 local function copy(v,n) n=n or 0;assert(n<=16,'PROPERTY_DEPTH');if type(v)~='table' then return v end;local r={};for k,x in pairs(v) do r[k]=copy(x,n+1) end;return r end
 local function same(a,b,n) n=n or 0;if n>16 or type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end;for k,v in pairs(a) do if not same(v,b[k],n+1) then return false end end;for k in pairs(b) do if a[k]==nil then return false end end;return true end
 local function count(v) local n=0;if type(v)=='table' then for _ in pairs(v) do n=n+1 end end;return n end
 local function sample(c)
  local s={owner=c:GetOwner(),id=c:GetID(),x=c:GetX(),y=c:GetY(),values={},districts={}}
  for k,key in pairs(keys) do s.values[k]=copy(c:GetProperty(key)) end
  for _,d in Players[s.owner]:GetDistricts():Members() do local city=d:GetCity()
   if city and city:GetID()==s.id and city:GetOwner()==s.owner then local def=P.Info('Districts',d:GetType());s.districts[#s.districts+1]=tostring(def and def.DistrictType or d:GetType())..':'..tostring(d:IsComplete()) end
  end
  table.sort(s.districts);return s
 end
 function d.Record(pid,c)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'SELECT_OWN_CITY')
  d.watch[pid]=sample(c)
  return d.Read(pid)
 end
 function d.Read(pid)
  assert(P.IsTestPlayer(pid),'TEST_PLAYER_REQUIRED');local old=assert(d.watch[pid],'先选择己方测试城市并记录；记录仅本次加载有效')
  local c=CityManager.GetCityAt(old.x,old.y)
  if not c then return '原城市位置当前无城市；不认定新城是同一城市，不写入任何记录。' end
  local s=sample(c);local v=s.values;local j=v.JOURNAL or {};local inv=v.INVEST or {};local std=v.TEMPLATES or {}
  local rows={'B063 城市继承只读观察（未执行继承/迁移）',
   '原Owner/CityID='..old.owner..'/'..old.id..' → 当前='..s.owner..'/'..s.id,
   '当前玩家启用='..tostring(P.IsTestPlayer(s.owner))..' | 位置='..s.x..','..s.y,
   '原TOKEN='..tostring(old.values.TOKEN)..' | 当前TOKEN='..tostring(v.TOKEN)}
  for _,k in ipairs(order) do
   local before,after=old.values[k],v[k]
   rows[#rows+1]=k..'：'..(before==nil and '原无' or '原有')..' → '..(after==nil and '现无' or '现有')..' | '..(same(before,after) and '内容一致' or '内容不同')
  end
  rows[#rows+1]='原始账本：专业='..tostring(j.specialization)..' | 投资笔数='..count(inv.investments)..' | 模板数='..count(std.learned)
  rows[#rows+1]='账本旧Owner/CityID='..tostring(j.owner)..'/'..tostring(j.cityID)..'（保留旧值不等于已适配新Owner）'
  rows[#rows+1]='区域：'..table.concat(s.districts,', ')
  rows[#rows+1]='本按钮不改Property/身份/Potential/收益；换Owner后现有机制未必可用。'
  return table.concat(rows,'\n')
 end
end
