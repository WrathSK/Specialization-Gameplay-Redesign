-- B049: calculation preparation only. No property/carrier/yield writes.
SPCLv4CopyRead={}
-- Keep engine details in Lua.log, never in the player-facing report.
local function notice(raw)
 local text=tostring(raw)
 if text:find('NETWORK_REFRESH_PENDING',1,true) or text:find('CURRENT_COUNT_CHANGED',1,true) then
  return '工业网络数据正在刷新，暂不能判断接收状态；稍后重新读取。'
 end
 if text:find('NETWORK_NOT_READY_OR_OWNER',1,true) then return '工业网络尚未就绪，暂不能判断接收状态。' end
 return '工业网络读取未完成，详情已记录到日志。'
end
function SPCLv4CopyRead.Metadata(P,shared,pid,c,token)
 local out={owner=pid,cityID=c:GetID(),token=token,turn=Game.GetCurrentGameTurn(),sources={}}
 local ok,err=pcall(function()
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'OWNER_CHANGED')
  local f=shared.EffectiveFacts.Read(pid,c);out.kind=f.specialization;out.active=f.active
  local good,ids=pcall(shared.NetworkBridge.RecipientSources,pid,c,'INDUSTRY')
  if not good then out.networkError=tostring(ids);print('[SPC][B049][COPY_NETWORK_DETAIL] '..out.networkError);return end
  out.industryRecipient=#ids>0
  for _,id in ipairs(ids) do
   local source=Players[pid]:GetCities():FindID(id);assert(source and source:GetOwner()==pid,'SOURCE_OWNER_CHANGED')
   local sf=shared.EffectiveFacts.Read(pid,source)
   if sf.specialization=='INDUSTRY' and sf.active==4 then
    out.sources[#out.sources+1]={cityID=id,districtID=sf.first.districtID,active=sf.active}
   end
  end
 end)
 if not ok then out.error=tostring(err) end
 return out
end
function SPCLv4CopyRead.Half(n)
 assert(type(n)=='number' and n==n and math.abs(n)<math.huge,'YIELD_UNKNOWN')
 return n*0.5
end
function SPCLv4CopyRead.Maximum(sources)
 local best,id=0,nil
 for _,s in ipairs(sources) do
  local v=SPCLv4CopyRead.Half(s.production)
  if v>best then best=v;id=s.cityID end
 end
 return best,id
end
-- UI-only reader matches HD's district:GetYield use, not its adjacency-only getter.
function SPCLv4CopyRead.Render(P,m)
 local ok,text=pcall(function()
  assert(m and not m.error,m and m.error or 'NO_METADATA')
  assert(m.owner==Game.GetLocalPlayer() and m.turn==Game.GetCurrentGameTurn(),'STALE_METADATA')
  local cities=Players[m.owner]:GetCities();local c=cities:FindID(m.cityID)
  assert(c and c:GetOwner()==m.owner,'OWNER_CHANGED')
  local function label(city) return Locale.Lookup(city:GetName())..' (#'..city:GetID()..')' end
  local lines={'区域与来源复核（读取不修改收益）',label(c)..' | '..m.kind..' ACTIVE='..m.active}
  local raw={};local wanted={}
  for _,v in ipairs(m.sources) do wanted[v.cityID..':'..v.districtID]=true end
  for _,d in Players[m.owner]:GetDistricts():Members() do P.Count('district_scan');
   local dc=d:GetCity()
   if dc and dc:GetOwner()==m.owner and d:IsComplete() and
    wanted[dc:GetID()..':'..d:GetID()] then
    local yields={};local total=0
    for _,key in ipairs({'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'}) do
     local n=d:GetYield(P.Info('Yields','YIELD_'..key).Index)
     SPCLv4CopyRead.Half(n);yields[key]=n;total=total+n
    end
    raw[dc:GetID()]=raw[dc:GetID()] or {};raw[dc:GetID()][d:GetID()]={production=yields.PRODUCTION,total=total}
   end
  end
  if m.networkError then lines[#lines+1]=notice(m.networkError)
  elseif #m.sources==0 then
   if m.industryRecipient==true then lines[#lines+1]='本城已接收工业网络，但当前没有有效的工业四级来源；本项生产力预期为0。'
   elseif m.industryRecipient==false then lines[#lines+1]='本城尚未接收工业网络；本项生产力预期为0。'
   else lines[#lines+1]='工业网络接收状态尚未读取，请重新读取。' end
  else
   local sources={}
   for _,s in ipairs(m.sources) do
    local value=raw[s.cityID] and raw[s.cityID][s.districtID];assert(value,'SOURCE_DISTRICT_UNAVAILABLE')
    sources[#sources+1]={cityID=s.cityID,production=value.production}
    lines[#lines+1]='工业来源 '..label(cities:FindID(s.cityID))..'：区域Production='..value.production..'；50%='..SPCLv4CopyRead.Half(value.production)
   end
   local amount,id=SPCLv4CopyRead.Maximum(sources)
   lines[#lines+1]='本城工业接收预期：max='..amount..'；来源='..tostring(id or '无')..'（不求和）'
  end
  lines[#lines+1]='上方自动复制配置与原生总量用于验收；下方来源计算不代表实测增量。'
  return table.concat(lines,'\n')
 end)
 if not ok then
  print('[SPC][B049][COPY_READ_DETAIL] '..tostring(text))
  return 'Lv4复制读取未完成，请重新读取；详情已记录到日志。'
 end
 return text
end
