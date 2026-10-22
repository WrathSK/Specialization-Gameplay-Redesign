-- B015 DEV submission experiment; not a permanent UID or production specialization.
SPCCityJournalProbe={}
function SPCCityJournalProbe.Start(P,shared)
 if shared.CityJournalProbe then return end
 local KEY="SPC_DEV_CITY_JOURNAL_B015"
 local j={phase="BEFORE_LOAD_CLOSE",players={},hooks={}};shared.CityJournalProbe=j
 local function bucket(pid)
  if not j.players[pid] then j.players[pid]={writes=0,busy=false,halted=false,last="NONE"} end
  return j.players[pid]
 end
 local function int(v) return type(v)=="number" and v>=0 and v%1==0 and v<math.huge end
 local function clone(v)
  if type(v)~="table" then return v end
  local r={};for k,x in pairs(v) do r[k]=clone(x) end;return r
 end
 local function equal(a,b,depth)
  if depth>8 or type(a)~=type(b) then return false end
  if type(a)~="table" then return a==b end
  for k,v in pairs(a) do if not equal(v,b[k],depth+1) then return false end end
  for k in pairs(b) do if a[k]==nil then return false end end;return true
 end
 local function family(name)
  local seen={};local rows=P.Rows("DistrictReplaces");assert(rows,"NO_REPLACEMENT_TABLE")
  for step=1,32 do
   assert(P.Info("Districts",name) and not seen[name],"INVALID_DISTRICT_MAPPING");seen[name]=true
   if P.Families[name] then return P.Families[name] end
   local parent
   for _,r in ipairs(rows) do if r.CivUniqueDistrictType==name then
    assert(not parent or parent==r.ReplacesDistrictType,"REPLACEMENT_CONFLICT");parent=r.ReplacesDistrictType
   end end
   if not parent then return "NON_V01" end;name=parent
  end
  error("REPLACEMENT_LIMIT")
 end
 local function read(pid,city)
  local token,state=shared.BindingProbe.Resolve(pid,city);assert(token,"BINDING_UNVERIFIED "..tostring(state))
  local v=city:GetProperty(KEY)
  if v~=nil then
   assert(type(v)=="table" and v.schema==1 and v.kind=="DEV_FOUNDATION_JOURNAL"
    and v.owner==pid and v.cityID==city:GetID() and v.token==token
    and v.x==city:GetX() and v.y==city:GetY() and int(v.revision) and int(v.foundationTurn)
    and (v.health=="TRACKING" or v.health=="GAP"),"JOURNAL_IDENTITY_OR_SCHEMA_CONFLICT")
   assert(v.health~="GAP" or type(v.gapReason)=="string","GAP_REASON_MISSING")
   if v.specialization=="NONE" then assert(v.potential==0 and v.first==nil,"EMPTY_FACT_CONFLICT")
   else
    assert(v.potential==1 and type(v.first)=="table" and int(v.first.districtID) and int(v.first.turn)
     and v.first.turn>=v.foundationTurn and v.specialization==family(v.first.type)
     and v.specialization~="NON_V01","FIRST_FACT_CONFLICT")
   end
  end
  return clone(v),token
 end
 local function write(pid,city,b,old,nextValue)
  assert(not (shared.CityProgressionStore and shared.CityProgressionStore.BlocksLegacy(city)),"GAME_STORE_OWNS_CITY")
  assert(equal(read(pid,city),old,0),"STALE_JOURNAL")
  b.writes=b.writes+1
  pcall(function() P.SetProperty(city,KEY,nextValue) end)
  assert(equal(read(pid,city),nextValue,0),"WRITE_UNCONFIRMED")
  if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(city,'CityJournalProbe.lua') end
 end
 -- A failure stops ALL further submissions for this player in this session.
 -- Preserve a GAP if storage remains usable. Never overwrite identity conflicts.
 local function run(pid,city,fn)
  if shared.CityProgressionStore and shared.CityProgressionStore.BlocksLegacy(city) then return end
  local b=bucket(pid)
  if b.halted then return end
  if b.busy then b.halted=true;b.last="REENTRANCY_STOP";return end
  b.busy=true
  local ok,err=pcall(fn,b)
  if not ok or b.halted then
   b.halted=true;b.last="STOP "..tostring(err or "REENTRANCY")
   if city then
    local marked=pcall(function()
     local old=read(pid,city)
     if old and old.health~="GAP" then
      local v=clone(old);v.health="GAP";v.gapReason=b.last;v.revision=v.revision+1;write(pid,city,b,old,v)
     end
    end)
    if not marked then b.last=b.last.." GAP_WRITE_UNCONFIRMED" end
   end
  end
  b.busy=false;print("[SPC][B015][JOURNAL] "..b.last)
 end
 -- Called only AFTER B013 creates a NEW confirmed binding, not on duplicate or load.
 shared.OnFreshCityBinding=function(pid,city)
  if not P.IsTestPlayer(pid) or j.phase~="AFTER_LOAD_CLOSE" then return end
  run(pid,city,function(b)
   assert(j.hooks.OnDistrictConstructed=="REGISTERED" and j.hooks.LoadScreenClose=="REGISTERED","LISTENER_NOT_READY")
   local old,token=read(pid,city);assert(old==nil,"EXISTING_JOURNAL_NO_RESET")
   local collection=Players[pid]:GetDistricts()
   local iterator,state,key=collection:Members();assert(type(iterator)=="function","DISTRICT_ITERATOR_INVALID")
   local scanned,center=0,false
   for _,district in iterator,state,key do
    scanned=scanned+1;assert(scanned<=512,"DISTRICT_SCAN_LIMIT")
    local c=district:GetCity();assert(c,"DISTRICT_CITY_UNAVAILABLE")
    if c:GetOwner()==pid and c:GetID()==city:GetID() then
     local info=P.Info("Districts",district:GetType());assert(info,"DISTRICT_TYPE_UNAVAILABLE")
     local complete=district:IsComplete();assert(type(complete)=="boolean","COMPLETENESS_UNAVAILABLE")
     if info.DistrictType=="DISTRICT_CITY_CENTER" and complete then center=true end
     assert(not complete or family(info.DistrictType)=="NON_V01","PREEXISTING_COMPLETED_SPECIALTY")
    end
   end
   assert(center,"CITY_CENTER_NOT_OBSERVED")
   local turn=Game.GetCurrentGameTurn();assert(int(turn),"TURN_UNAVAILABLE")
   write(pid,city,b,nil,{schema=1,kind="DEV_FOUNDATION_JOURNAL",owner=pid,cityID=city:GetID(),
    token=token,x=city:GetX(),y=city:GetY(),foundationTurn=turn,revision=0,health="TRACKING",specialization="NONE",potential=0})
   b.last="FOUNDATION_SAVED"
  end)
 end
 local function completed(pid,index,x,y)
  if not P.IsTestPlayer(pid) or j.phase~="AFTER_LOAD_CLOSE" then return end
  local city
  -- Unknown object/type failures cannot silently skip an earlier completion.
  local ok,err=pcall(function()
   local info=P.Info("Districts",index);assert(info,"EVENT_TYPE_UNAVAILABLE")
   local f=family(info.DistrictType);if f=="NON_V01" then return end
   local d=CityManager.GetDistrictAt(x,y);assert(d,"EVENT_DISTRICT_UNAVAILABLE")
   city=d:GetCity();assert(city and city:GetOwner()==pid and d:GetOwner()==pid and d:GetType()==index,"EVENT_OWNER_OR_TYPE_CONFLICT")
   run(pid,city,function(b)
    local raw=city:GetProperty(KEY)
    if raw==nil then b.last="UNTRACKED_NO_WRITE";return end -- no adoption of old cities
    local old=read(pid,city)
    assert(old.health=="TRACKING","PERSISTENT_HISTORY_GAP")
    assert(d:IsComplete()==true,"EVENT_NOT_COMPLETE")
    if old.specialization~="NONE" then b.last="LOCK_PRESERVED_NO_WRITE";return end
    local v=clone(old);v.specialization=f;v.potential=1;v.revision=v.revision+1
    v.first={districtID=d:GetID(),type=info.DistrictType,turn=Game.GetCurrentGameTurn()}
    assert(int(v.first.districtID) and int(v.first.turn),"INVALID_EVENT_FIELDS")
    write(pid,city,b,old,v);b.last="DEV_SPECIALIZATION_SAVED"
   end)
  end)
  if not ok then run(pid,city,function() error(err) end) end
 end
 function j.Read(pid,city)
  if not P.IsTestPlayer(pid) then return "OUTSIDE_TEST_CIV" end
  if shared.CityProgressionStore and shared.CityProgressionStore.BlocksLegacy(city) then return "Game进度记录；旧Journal冻结" end
  local b=bucket(pid)
  local ok,line=pcall(function()
   local raw=city:GetProperty(KEY)
   if raw==nil then return "city="..city:GetID().." | UNTRACKED_NO_WRITE" end
   local v=read(pid,city)
   return "city="..v.cityID.." token="..v.token.."\nhealth="..v.health.." revision="..v.revision
    .."\nDEV specialization="..v.specialization.." potential="..v.potential
    .."\nfirst="..(v.first and (v.first.type.." district="..v.first.districtID.." turn="..v.first.turn) or "NONE")
  end)
  local result=P.VERSION.." | 新城提交实验\n"..(ok and line or ("READ_ERROR "..tostring(line)))
   .."\n本次加载写入="..b.writes.." stopped="..tostring(b.halted).."\n最近动作="..b.last
   .."\n"..j.phase.." Constructed="..tostring(j.hooks.OnDistrictConstructed)
   .."\n仅DEV候选事实；未启用专业收益或正式继承。"
  print("[SPC][B015][JOURNAL] "..result);return result
 end
 function j.EnsureInherited(pid)
  assert(j.phase=="AFTER_LOAD_CLOSE" and not bucket(pid).halted,"INHERIT_JOURNAL_HELD")
 end
 local function listen(ns,name,fn)
  local e=P.Field(ns,name)
  if e and type(e.Add)=="function" then local ok=pcall(e.Add,fn);j.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
  else j.hooks[name]="ABSENT" end
 end
 if not (shared.CityProgressionStore and shared.CityProgressionStore.UsesNewAuthority) then listen(GameEvents,"OnDistrictConstructed",completed) end
 listen(Events,"LoadScreenClose",function()
  j.phase="AFTER_LOAD_CLOSE"
  if shared.CityProgressionStore and shared.CityProgressionStore.UsesNewAuthority then return end
  for pid,player in pairs(Players) do if P.IsTestPlayer(pid) then
   local ok,err=pcall(function() for _,city in player:GetCities():Members() do P.Count('city_scan'); j.Read(pid,city) end end)
   if not ok then bucket(pid).halted=true;bucket(pid).last="LOAD_AUDIT_ERROR "..tostring(err) end
  end end
 end)
end
