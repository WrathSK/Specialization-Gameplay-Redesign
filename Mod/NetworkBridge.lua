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
 function d.Receive(pid,p)
  if not P.IsTestPlayer(pid) or p.Epoch~=d.epoch or not integer(p.Seq) then return end
  local b=d.players[pid] or {seq=-1};d.players[pid]=b
  if p.Seq<=b.seq then return end
  b.seq=p.Seq;b.routes=nil;b.sources=nil;b.centers=nil;b.recipients=nil;b.reason="INCOMPLETE"
  local ok,err=pcall(function()
   assert(d.ready,"LOAD_NOT_READY")
   assert(p.Turn==Game.GetCurrentGameTurn() and p.Signal==(shared.RouteSignalRevision or 0),"STALE_SIGNAL_OR_TURN")
   if p.Valid~=1 then b.reason="BACKGROUND_INVALIDATED";return end
   assert(integer(p.Count) and p.Count<=128 and type(p.Data)=="string" and #p.Data<=16384,"BATCH_LIMIT_OR_SHAPE")
   local rows,seen={},{}
   for line in p.Data:gmatch("[^;]+") do
    local a,o,c,z,u=line:match("^(%d+),(%d+),(%d+),(%d+),(%d+)$")
    assert(a,"ROW_FORMAT")
    a,o,c,z,u=tonumber(a),tonumber(o),tonumber(c),tonumber(z),tonumber(u)
    for _,v in ipairs({a,o,c,z,u}) do assert(integer(v),"ROW_RANGE") end
    assert(a==pid and not seen[u],"ORIGIN_OR_DUPLICATE_TRADER");seen[u]=true
    city(a,o);city(c,z)
    rows[#rows+1]={op=a,oc=o,dp=c,dc=z,trader=u}
   end
   assert(#rows==p.Count,"PARTIAL_BATCH")
   assert(Players[pid]:GetTrade():CountOutgoingRoutes()==p.Count,"CURRENT_COUNT_CHANGED")
   local sources,centers,recipients=derive(pid,rows)
   b.routes=rows;b.sources=sources;b.centers=centers;b.recipients=recipients
   b.turn=p.Turn;b.signal=p.Signal;b.reason="READY_BACKGROUND_UI"
  end)
  if not ok then b.reason=short(err);print("[SPC][B027][DETAIL] "..tostring(err)) end
  if shared.Lv3Effects then shared.Lv3Effects.Audit() end
  print("[SPC][B027][BRIDGE] player="..pid.." seq="..b.seq.." "..b.reason)
 end
 derive=function(pid,rows)
  local sources,centers,recipients={},{},{}
  local player=Players[pid];local capital=player:GetCities():GetCapitalCity()
  local scanned=0
  for _,c in player:GetCities():Members() do
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
  assert(b and b.routes and b.turn==Game.GetCurrentGameTurn() and b.signal==(shared.RouteSignalRevision or 0),'NETWORK_REFRESH_PENDING')
  assert(Players[pid]:GetTrade():CountOutgoingRoutes()==#b.routes,'CURRENT_COUNT_CHANGED')
  local sources,centers=derive(pid,b.routes);local result={}
  for src in pairs(centers[selected:GetID()] or {}) do result[sources[src]]=true end
  return result
 end
 -- B049 readonly current source identities, never a history/event-derived list.
 function d.RecipientSources(pid,selected,kind)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  local b=d.players[pid]
  assert(b and b.routes and b.turn==Game.GetCurrentGameTurn() and b.signal==(shared.RouteSignalRevision or 0),'NETWORK_REFRESH_PENDING')
  assert(Players[pid]:GetTrade():CountOutgoingRoutes()==#b.routes,'CURRENT_COUNT_CHANGED')
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
  if b.turn~=Game.GetCurrentGameTurn() or b.signal~=(shared.RouteSignalRevision or 0) then return "B031 网络待刷新: REFRESH_PENDING" end
  local ok,out=pcall(function()
   assert(selected:GetOwner()==pid,"SELECTED_OWNER_CHANGED")
   assert(Players[pid]:GetTrade():CountOutgoingRoutes()==#b.routes,"CURRENT_COUNT_CHANGED")
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
   if b.routes and b.turn==Game.GetCurrentGameTurn() and b.signal==(shared.RouteSignalRevision or 0) then
    local ok,s,c,r=pcall(derive,pid,b.routes)
    if ok then b.sources=s;b.centers=c;b.recipients=r else b.routes=nil;b.sources=nil;b.centers=nil;b.recipients=nil;b.reason=short(s) end
   else b.sources=nil;b.centers=nil;b.recipients=nil end
  end
  if shared.Lv3Effects then shared.Lv3Effects.Audit() end
 end
 for _,name in ipairs({"OnDistrictConstructed","CityBuilt"}) do
  local ev=P.Field(GameEvents,name);if ev and ev.Add then ev.Add(d.Rebuild) end
 end
 local turn=P.Field(Events,"PlayerTurnActivated");if turn and turn.Add then turn.Add(d.Rebuild) end
 local e=P.Field(Events,"LoadScreenClose");if e and e.Add then e.Add(function() d.ready=true end) end
end
