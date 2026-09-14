-- B027 bounded single-player diagnostic bridge. No Property, Modifier or yields.
SPCNetworkBridge={}
function SPCNetworkBridge.Start(P,shared)
 local d={ready=false,players={}};shared.NetworkBridge=d
 ExposedMembers.SPCNetworkEpoch=(ExposedMembers.SPCNetworkEpoch or 0)+1
 d.epoch=ExposedMembers.SPCNetworkEpoch
 local function integer(n) return type(n)=="number" and n>=0 and n%1==0 and n<2147483648 end
 local function city(pid,id)
  local p=Players[pid];local c=p and p:GetCities():FindID(id)
  assert(c and c:GetOwner()==pid,"ENDPOINT_MISSING_OR_CHANGED");return c
 end
 local function short(err)
  local first=tostring(err):match("[^\r\n]+") or "UNKNOWN"
  return (first:match(":%d+: (.+)$") or first):sub(1,180)
 end
 local derive
 local function notify()
  if shared.Lv3Effects then shared.Lv3Effects.Audit() end
  if shared.StandardizationDiscount then shared.StandardizationDiscount.Audit() end
  if shared.NetworkBoost then shared.NetworkBoost.Audit() end
  if shared.CommerceConvergence then shared.CommerceConvergence.Audit() end
 end
 -- Concrete native evidence only; a dirty signal or changed turn is not evidence.
 function d.Verified(pid,failedFullRead)
  local b=d.players[pid];if not b or not b.routes then return false end
  local ok,invalid=pcall(function()
   if failedFullRead and Players[pid]:GetTrade():CountOutgoingRoutes()<#b.routes then return true end
   for _,r in ipairs(b.routes) do
    local op,dp=Players[r.op],Players[r.dp]
    if not op or not dp then return true end
    local o,z=op:GetCities():FindID(r.oc),dp:GetCities():FindID(r.dc)
    if not o or not z or o:GetOwner()~=r.op or z:GetOwner()~=r.dp then return true end
    local known,u=pcall(function() return op:GetUnits():FindID(r.trader) end)
    if known and not u then return true end
    if r.op~=r.dp then
     local readable,war=pcall(function() return op:GetDiplomacy():IsAtWarWith(r.dp) end)
     if readable and war==true then return true end
    end
   end
   return false
  end)
  if ok and invalid then
   b.routes=nil;b.sources=nil;b.centers=nil;b.recipients=nil;b.fingerprint=nil;b.reason='CONFIRMED_INVALID'
   P.Count('confirmed_invalid') -- topology revision advances only on a complete replacement
   local perf=ExposedMembers.SPC_Performance;if perf then perf.revision=b.revision;perf.routes=0 end
   return false
  end
  return true -- transient unreadability is not confirmed removal
 end
 function d.Receive(pid,p)
  P.Count('net_receive')
  if not P.IsTestPlayer(pid) or p.Epoch~=d.epoch or not integer(p.Seq) then return end
  local b=d.players[pid] or {seq=-1,revision=0};d.players[pid]=b
  if p.Seq<=b.seq then P.Count('send_duplicate');return end
  b.seq=p.Seq
  local changed=false
  local ok,err=pcall(function()
   assert(d.ready,'LOAD_NOT_READY')
   assert(p.Turn==Game.GetCurrentGameTurn() and p.Signal==(shared.RouteSignalRevision or 0),'STALE_SIGNAL_OR_TURN')
   if p.Valid~=1 then b.revalidation='NEEDS_REVALIDATION';return end
   local count=p.Count
   if p.WireCount~=nil then
    assert(integer(p.WireCount) and p.WireCount>=1 and p.WireCount<=129,'WIRE_COUNT_INVALID')
    count=p.WireCount-1;assert(p.Count==nil or p.Count==count,'WIRE_COUNT_CONFLICT')
   end
   assert(integer(count) and count<=128,'ROUTE_COUNT_INVALID')
   local data=p.Data;if count==0 and data=='EMPTY' then data='' end
   assert(type(data)=='string' and #data<=16384,'ROUTE_DATA_INVALID')
   local rows,seen,keys={},{},{}
   for line in data:gmatch('[^;]+') do
    local a,o,c,z,u=line:match('^(%d+),(%d+),(%d+),(%d+),(%d+)$')
    assert(a,'ROW_FORMAT');a,o,c,z,u=tonumber(a),tonumber(o),tonumber(c),tonumber(z),tonumber(u)
    for _,v in ipairs({a,o,c,z,u}) do assert(integer(v),'ROW_RANGE') end
    assert(a==pid and not seen[u],'ORIGIN_OR_DUPLICATE_TRADER');seen[u]=true
    city(a,o);city(c,z)
    rows[#rows+1]={op=a,oc=o,dp=c,dc=z,trader=u}
    keys[#keys+1]=a..':'..u..'|'..a..':'..o..'>'..c..':'..z
   end
   assert(#rows==count,'PARTIAL_BATCH')
   assert(Players[pid]:GetTrade():CountOutgoingRoutes()==count,'CURRENT_COUNT_CHANGED')
   table.sort(keys);local fingerprint=table.concat(keys,'\n')
   if b.routes and b.fingerprint==fingerprint then
    b.turn=p.Turn;b.signal=p.Signal;b.revalidation='VERIFIED';P.Count('same_snapshot');return
   end
   local sources,centers,recipients=derive(pid,rows)
   b.routes=rows;b.sources=sources;b.centers=centers;b.recipients=recipients;b.fingerprint=fingerprint
   b.turn=p.Turn;b.signal=p.Signal;b.reason='READY_BACKGROUND_UI';b.revalidation='VERIFIED'
   b.revision=b.revision+1;b.error=nil;changed=true;P.Count('publication')
   local perf=ExposedMembers.SPC_Performance;if perf then perf.revision=b.revision;perf.routes=#rows end
  end)
  if not ok then b.revalidation='NEEDS_REVALIDATION';b.error=short(err);P.Count('route_failure') end
  local previously=b.routes~=nil
  d.Verified(pid)
  if changed or (previously and not b.routes) then notify() end
 end
 derive=function(pid,rows)
  P.Count("derive")
  local sources,centers,recipients={},{},{}
  local player=Players[pid];local capital=player:GetCities():GetCapitalCity()
  local scanned=0
  for _,c in player:GetCities():Members() do P.Count('city_scan');
   scanned=scanned+1;assert(scanned<=512,"CITY_LIMIT")
   local id=c:GetID();local ok,f=pcall(shared.EffectiveFacts.Read,pid,c)
   if ok and f.potential>=1 then
    if f.specialization=="RESEARCH" or f.specialization=="CULTURE" or f.specialization=="INDUSTRY" then sources[id]=f.specialization end
    if f.specialization=="COMMERCE" then centers[id]={} end
   end
  end
  if capital then centers[capital:GetID()]=centers[capital:GetID()] or {} end
  for _,r in ipairs(rows) do
   city(r.op,r.oc);city(r.dp,r.dc)
   if r.dp==pid and centers[r.dc] and sources[r.oc] then centers[r.dc][r.oc]=true end
  end
  if capital and sources[capital:GetID()] then centers[capital:GetID()][capital:GetID()]=true end
  -- D0009: direct connection grants reception, independently of distribution.
  -- Recipient keys merge direct, capital-self and outgoing-route qualifications.
  for centerID,sourceSet in pairs(centers) do
   for src in pairs(sourceSet) do
    local kind=sources[src];recipients[kind]=recipients[kind] or {}
    local set=recipients[kind];set[centerID]=set[centerID] or {};set[centerID][src]=true
   end
  end
  for _,r in ipairs(rows) do
   if r.dp==pid and centers[r.oc] then
    for src in pairs(centers[r.oc]) do
     local kind=sources[src];recipients[kind]=recipients[kind] or {}
     local set=recipients[kind];set[r.dc]=set[r.dc] or {};set[r.dc][src]=true
    end
   end
  end
  return sources,centers,recipients
 end
 -- Fresh direct connection types for Commerce III; never use display text or source count as yield.
 function d.ConnectedKinds(pid,selected)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  local b=d.players[pid]
  assert(d.Verified(pid),'NETWORK_REFRESH_PENDING')
  -- Current route additions are reconciled by the next complete snapshot.
  local sources,centers=derive(pid,b.routes);local result={}
  for src in pairs(centers[selected:GetID()] or {}) do result[sources[src]]=true end
  return result
 end
 -- B055 national union: a recipient counts once if at least one current ACTIVE source reaches it.
 function d.National(pid)
  assert(P.IsTestPlayer(pid) and d.ready,'NETWORK_NOT_READY_OR_OWNER')
  local b=d.players[pid]
  assert(d.Verified(pid),'NETWORK_REFRESH_PENDING')
  -- Current route additions are reconciled by the next complete snapshot.
  local _,_,recipients=derive(pid,b.routes);local result={}
  for _,kind in ipairs({'RESEARCH','CULTURE'}) do
   local r={n=0,level=0,sources={},recipients={}};result[kind]=r
   for cid,set in pairs(recipients[kind] or {}) do
    for src in pairs(set) do
     local ok,f=pcall(shared.EffectiveFacts.Read,pid,city(pid,src))
     if ok and f.specialization==kind and type(f.active)=='number' and f.active>=1 and f.active<=4 and f.active%1==0 then
      r.sources[src]=f.active;r.recipients[cid]=true;r.level=math.max(r.level,f.active)
     end
    end
   end
   for _ in pairs(r.recipients) do r.n=r.n+1 end
  end
  return result
 end
 -- B049 readonly current source identities, never a history/event-derived list.
 function d.RecipientSources(pid,selected,kind)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  local b=d.players[pid]
  assert(d.Verified(pid),'NETWORK_REFRESH_PENDING')
  -- Current route additions are reconciled by the next complete snapshot.
  local _,_,recipients=derive(pid,b.routes);local result={}
  for src in pairs((recipients[kind] or {})[selected:GetID()] or {}) do result[#result+1]=src end
  table.sort(result);return result
 end
 local kinds={"RESEARCH","CULTURE","INDUSTRY"}
 local labels={RESEARCH="科研",CULTURE="文化",INDUSTRY="工业"}
 local function size(set) local n=0;for _ in pairs(set or {}) do n=n+1 end;return n end
 local function name(pid,id)
  local c=city(pid,id);local ok,n=pcall(function() return c:GetName() end)
  if not ok or type(n)~="string" then return "城市#"..id end
  if Locale and Locale.Lookup then local yes,v=pcall(Locale.Lookup,n);if yes then n=v end end
  return n:gsub("[\r\n]"," ").." (#"..id..")"
 end
 local detailPage={}
 function d.Read(pid,selected,details)
  local b=d.players[pid]
  if not b or not b.routes then return "B031 网络待刷新: "..(b and b.reason or "NO_BACKGROUND_BATCH") end
  if not d.Verified(pid) then return "B031 网络待刷新: REFRESH_PENDING" end
  local ok,out=pcall(function()
   assert(selected:GetOwner()==pid,"SELECTED_OWNER_CHANGED")
   assert(d.Verified(pid),"CURRENT_ROUTE_INVALID")
   local sources,centers,recipients=derive(pid,b.routes)
   local id=selected:GetID();local title="B031 "..name(pid,id)
   if details then
    local entries={}
    for src in pairs(centers[id] or {}) do
     entries[#entries+1]="接入 "..labels[sources[src]]..": "..name(pid,src)..(src==id and " [首都自身]" or " [直连]")
    end
    for _,k in ipairs(kinds) do
     for src in pairs((recipients[k] or {})[id] or {}) do
      entries[#entries+1]="接收 "..labels[k]..": 来源 "..name(pid,src)
     end
    end
    for _,route in ipairs(b.routes) do
     if route.oc==id or (route.dp==pid and route.dc==id) then
      entries[#entries+1]="商路 "..name(route.op,route.oc).." → "..name(route.dp,route.dc)
     end
    end
    table.sort(entries)
    if #entries==0 then entries[1]="无接入来源、接收来源或相关商路" end
    local signature=table.concat(entries,"\n");local key=pid..":"..id;local cursor=detailPage[key]
    local pages=math.ceil(#entries/3)
    local page=(cursor and cursor.signature==signature) and (cursor.page%pages+1) or 1
    detailPage[key]={signature=signature,page=page}
    local lines={title.." | 明细 "..page.."/"..pages}
    for i=(page-1)*3+1,math.min(page*3,#entries) do lines[#lines+1]=entries[i] end
    lines[#lines+1]="再次点网络明细翻页；接收来源不等于可转发来源。"
    lines[#lines+1]="DEV网络状态；商业III专家奖励另按ACTIVE门控。"
    return table.concat(lines,"\n")
   end
   detailPage[pid..":"..id]=nil
   local dist=0
   for _,route in ipairs(b.routes) do if route.oc==id and route.dp==pid and centers[id] and next(centers[id]) then dist=dist+1 end end
   local lines={title.." | 当前商路总数="..#b.routes,
    "本城来源类型="..(labels[sources[id]] or (centers[id] and "贸易中心/非来源" or "非网络来源")).." | 贸易中心="..(centers[id] and "是" or "否").." | 分发路线="..dist}
   for _,k in ipairs(kinds) do
    local connected=0;for src in pairs(centers[id] or {}) do if sources[src]==k then connected=connected+1 end end
    local set=recipients[k] or {}
    lines[#lines+1]=labels[k]..": 本中心接入来源="..connected.." | 全国接收城市="..size(set).." | 本城接收="..(set[id] and "是" or "否")
   end
   lines[#lines+1]="来源数≠接收城市数；网络明细可看城市/方向。DEV网络；商业III专家奖励另按ACTIVE门控。"
   return table.concat(lines,"\n")
  end)
  return ok and out or ("B031 网络待刷新: "..short(out))
 end
 function d.Rebuild()
  for pid,b in pairs(d.players) do
   if d.Verified(pid) then
    local ok,s,c,r=pcall(derive,pid,b.routes)
    if ok then b.sources=s;b.centers=c;b.recipients=r else b.error=short(s);b.revalidation='NEEDS_REVALIDATION' end
   else b.sources=nil;b.centers=nil;b.recipients=nil end
  end
  if shared.Lv3Effects then shared.Lv3Effects.Audit() end
  if shared.StandardizationDiscount then shared.StandardizationDiscount.Audit() end
  if shared.NetworkBoost then shared.NetworkBoost.Audit() end
  if shared.CommerceConvergence then shared.CommerceConvergence.Audit() end
 end
 for _,name in ipairs({"OnDistrictConstructed","CityBuilt"}) do
  local ev=P.Field(GameEvents,name);if ev and ev.Add then ev.Add(d.Rebuild) end
 end
 function d.CheckEvidence(failedFullRead)
  local changed=false
  for pid,b in pairs(d.players) do local had=b.routes~=nil;d.Verified(pid,failedFullRead);if had and not b.routes then changed=true end end
  if changed then notify() end
 end
 for _,name in ipairs({'TradeRouteActivityChanged','TradeRouteRemovedFromMap','UnitRemovedFromMap','CityRemovedFromMap','CityTransfered','DiplomacyDeclareWar'}) do
  local ev=P.Field(Events,name);if ev and ev.Add then ev.Add(function() d.CheckEvidence(false) end) end
 end
 local turn=P.Field(Events,"PlayerTurnActivated");if turn and turn.Add then turn.Add(d.Rebuild) end
 local e=P.Field(Events,"LoadScreenClose");if e and e.Add then e.Add(function() d.ready=true end) end
end
