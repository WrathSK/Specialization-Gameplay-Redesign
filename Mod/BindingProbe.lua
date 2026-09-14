-- B013 DEV-only. Never produces a specialization or a production UID.
SPCBindingProbe={}
function SPCBindingProbe.Start(P,shared)
 if shared.BindingProbe then return end
 local TOKEN="SPC_DEV_BINDING_B013_TOKEN"
 local data={version=P.VERSION,phase="BEFORE_LOAD_CLOSE",players={},hooks={}}
 shared.BindingProbe=data
 local function key(pid) return "SPC_DEV_BINDING_B013_P"..pid end
 local function integer(n) return type(n)=="number" and n>=0 and n%1==0 and n<1000000000 end
 local function bucket(pid)
  if not data.players[pid] then data.players[pid]={gameWrites=0,cityWrites=0,last="NONE",busy=false} end
  return data.players[pid]
 end
 local function same(a,b,depth)
  if depth>8 or type(a)~=type(b) then return false end
  if type(a)~="table" then return a==b end
  for k,v in pairs(a) do if not same(v,b[k],depth+1) then return false end end
  for k in pairs(b) do if a[k]==nil then return false end end
  return true
 end
 local function clone(v)
  if type(v)~="table" then return v end
  local c={};for k,x in pairs(v) do c[k]=clone(x) end;return c
 end
 local function ledger(pid)
  local v=Game:GetProperty(key(pid))
  if v==nil then return nil end
  assert(type(v)=="table" and v.schema==1 and v.owner==pid and integer(v.counter)
   and v.counter<=32 and type(v.records)=="table","BAD_LEDGER")
  local n,seen=0,{}
  for k,r in pairs(v.records) do
   assert(type(r)=="table" and integer(r.cityID) and k==tostring(r.cityID) and r.owner==pid
    and integer(r.x) and integer(r.y) and integer(r.serial) and r.serial>0 and r.serial<=v.counter
    and not seen[r.serial] and r.uid=="DEV-B013-P"..pid.."-"..r.serial
    and (r.state=="RESERVED" or r.state=="CONFIRMED"),"BAD_RECORD")
   n=n+1;seen[r.serial]=true
  end
  assert(n==v.counter,"BAD_COUNTER")
  return clone(v)
 end
 local function inspect(pid,city)
  assert(city and city:GetOwner()==pid,"CITY_OWNER_MISMATCH")
  local v=ledger(pid);local token=city:GetProperty(TOKEN)
  local r=v and v.records[tostring(city:GetID())]
  local state
  if not r and token==nil then state="UNTRACKED_NO_WRITE"
  elseif not r or token==nil then state="PARTIAL_NO_REPAIR"
  elseif token~=r.uid or r.x~=city:GetX() or r.y~=city:GetY() then state="CONFLICT_NO_REPAIR"
  elseif r.state=="CONFIRMED" then state="BOUND_MATCH"
  else state="RESERVED_MATCH_NO_REPAIR" end
  return state,v,token,r
 end
 function data.Resolve(pid,city)
  if not P.IsTestPlayer(pid) then return nil,"OUTSIDE_TEST_CIV" end
  if shared.CityInheritance then local uid,status=shared.CityInheritance.Resolve(pid,city);if uid then return uid,status end end
  local state,_,token=inspect(pid,city)
  if state~="BOUND_MATCH" then return nil,state end
  return token,state
 end
 function data.Read(pid,city)
  if not P.IsTestPlayer(pid) then return "OUTSIDE_TEST_CIV" end
  local b=bucket(pid)
  local ok,state,v,token,r=pcall(inspect,pid,city)
  local line=ok and ("城市="..city:GetID().." | "..state.."\ncity token="..tostring(token)
   .."\nledger token="..tostring(r and r.uid).." state="..tostring(r and r.state)
   .."\n总账counter="..tostring(v and v.counter or 0)) or ("READ_ERROR "..tostring(state))
  local text=P.VERSION.." | DEV新城绑定\n"..line.."\n本次加载写入 Game="..b.gameWrites.." City="..b.cityWrites
   .."\n阶段="..data.phase.." CityBuilt="..tostring(data.hooks.CityBuilt).." Load="..tostring(data.hooks.LoadScreenClose)
   .."\n最近事件="..b.last.."\n仅DEV编号；不写专业/Potential。"
  print("[SPC][B013][BINDING] "..text);return text
 end
 local function gameWrite(pid,b,before,next)
  assert(same(ledger(pid),before,0),"STALE_LEDGER")
  b.gameWrites=b.gameWrites+1
  pcall(function() P.SetProperty(Game,key(pid),next) end)
  assert(same(ledger(pid),next,0),"GAME_WRITE_UNCONFIRMED")
 end
 local function foundation(pid,cid,x,y)
  if not P.IsTestPlayer(pid) then return end
  local b=bucket(pid)
  if data.phase~="AFTER_LOAD_CLOSE" then b.last="LOAD_EVENT_IGNORED";return end
  if b.busy then b.last="REENTRANT_IGNORED";return end
  b.busy=true
  local ok,err=pcall(function()
   assert(integer(cid) and integer(x) and integer(y),"BAD_EVENT")
   local city=CityManager.GetCity(pid,cid)
   assert(city and city:GetID()==cid and city:GetOwner()==pid and city:GetX()==x and city:GetY()==y,"EVENT_OBJECT_MISMATCH")
   local state,old=inspect(pid,city)
   if state=="BOUND_MATCH" then b.last="DUPLICATE_NO_WRITE";return end
   assert(state=="UNTRACKED_NO_WRITE","EXISTING_BINDING_NO_REPAIR")
   if old==nil then
    -- DEV bootstrap only: a missing ledger must not strand extant city tokens.
    for _,c in Players[pid]:GetCities():Members() do P.Count('city_scan'); assert(c:GetProperty(TOKEN)==nil,"TOKEN_WITHOUT_LEDGER") end
   end
   local next=clone(old or {schema=1,owner=pid,counter=0,records={}})
   assert(next.counter<32,"DEV_CITY_LIMIT_32")
   next.counter=next.counter+1
   local uid="DEV-B013-P"..pid.."-"..next.counter
   next.records[tostring(cid)]={cityID=cid,owner=pid,x=x,y=y,serial=next.counter,uid=uid,state="RESERVED"}
   gameWrite(pid,b,old,next)
   city=CityManager.GetCity(pid,cid)
   assert(city and city:GetID()==cid and city:GetOwner()==pid and city:GetX()==x and city:GetY()==y
    and city:GetProperty(TOKEN)==nil,"CITY_CHANGED_BEFORE_WRITE")
   b.cityWrites=b.cityWrites+1;pcall(function() P.SetProperty(city,TOKEN,uid) end)
   assert(city:GetProperty(TOKEN)==uid,"CITY_WRITE_UNCONFIRMED")
   local confirmed=clone(next);confirmed.records[tostring(cid)].state="CONFIRMED"
   gameWrite(pid,b,next,confirmed)
   assert(inspect(pid,city)=="BOUND_MATCH","FINAL_BINDING_MISMATCH")
  if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(city,'BindingProbe.lua') end
   b.last="NEW_CITY_BOUND"
   if shared.OnFreshCityBinding then shared.OnFreshCityBinding(pid,city) end
  end)
  b.busy=false
  if not ok then b.last="ERROR "..tostring(err) end
  print("[SPC][B013][BINDING] city="..tostring(cid).." "..b.last)
 end
 local function listen(ns,name,fn)
  local e=P.Field(ns,name)
  if e and type(e.Add)=="function" then
   local ok=pcall(e.Add,fn);data.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
  else data.hooks[name]="ABSENT" end
 end
 listen(GameEvents,"CityBuilt",foundation)
 listen(Events,"LoadScreenClose",function()
  data.phase="AFTER_LOAD_CLOSE"
  -- Automatic read-only audit; no repair, allocation or confirmation during load.
  for pid,player in pairs(Players) do
   if P.IsTestPlayer(pid) then
    local ok,err=pcall(function() for _,city in player:GetCities():Members() do P.Count('city_scan'); data.Read(pid,city) end end)
    if not ok then bucket(pid).last="LOAD_AUDIT_ERROR "..tostring(err) end
   end
  end
 end)
end
