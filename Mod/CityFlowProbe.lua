-- B021 DEV normal-save recovery; existing matched records only, no missing-history adoption.
SPCCityFlowProbe={}
function SPCCityFlowProbe.Start(P,shared)
 local KEY="SPC_DEV_CITY_FLOW_B020"
 local data={ready=false,players={},active={},owners={},hooks={}};shared.CityFlowProbe=data
 local function clone(v) if type(v)~="table" then return v end;local c={};for k,x in pairs(v) do c[k]=clone(x) end;return c end
 local function same(a,b,n)
  n=n or 0;if n>12 or type(a)~=type(b) then return false end
  if type(a)~="table" then return a==b end
  for k,v in pairs(a) do if not same(v,b[k],n+1) then return false end end
  for k in pairs(b) do if a[k]==nil then return false end end;return true
 end
 local function bucket(pid)
  if not data.players[pid] then data.players[pid]={writes=0,last="NONE"} end;return data.players[pid]
 end
 local function identity(pid,city)
  assert(city and city:GetOwner()==pid,"OWNER_CHANGED")
  local token,state=shared.BindingProbe.Resolve(pid,city);assert(token and state=="BOUND_MATCH","BINDING_CHANGED")
  return token
 end
 local function read(pid,city)
  local v=city:GetProperty(KEY);if v==nil then return nil end
  local token=identity(pid,city)
  assert(type(v)=="table" and v.schema==1 and v.owner==pid and v.cityID==city:GetID() and v.token==token
   and v.x==city:GetX() and v.y==city:GetY() and type(v.revision)=="number" and v.revision>=1 and v.revision%1==0
   and type(v.target)=="table" and (v.stage=="BEFORE_PENDING" or v.stage=="TARGET_PENDING" or v.stage=="DONE"),"BAD_FLOW_RECORD")
  local expected=v.target;if v.stage=="BEFORE_PENDING" then expected=v.before end
  assert(same(v.facts,expected),"FACT_STAGE_MISMATCH")
  local f=v.target
  assert(f.owner==pid and f.cityID==v.cityID and f.token==token and f.health=="TRACKING" and f.kind=="DEV_FOUNDATION_JOURNAL","TARGET_IDENTITY")
  assert((f.specialization=="NONE" and f.potential==0 and f.first==nil) or (f.potential==1 and type(f.first)=="table"),"TARGET_FACTS")
  return clone(v)
 end
 local function write(pid,city,b,old,nextValue)
  assert(not (shared.CityProgressionStore and shared.CityProgressionStore.Owns(city)),"GAME_STORE_OWNS_CITY")
  assert(not b.halted and P.IsTestPlayer(pid) and data.ready,"WRITE_NOT_AUTHORIZED")
  assert(same(read(pid,city),old),"STALE_FLOW")
  assert(identity(pid,city)==nextValue.token,"WRITE_IDENTITY_CHANGED")
  b.writes=b.writes+1;pcall(function() P.SetProperty(city,KEY,clone(nextValue)) end)
  assert(same(read(pid,city),nextValue),"FLOW_WRITE_UNCONFIRMED")
  if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(city,'CityFlowProbe.lua') end
 end
 local function commit(pid,city,target)
  local b=bucket(pid);local old=read(pid,city)
  assert(not old or old.stage=="DONE","PENDING_HELD")
  local v={schema=1,owner=pid,cityID=city:GetID(),token=identity(pid,city),x=city:GetX(),y=city:GetY(),
   revision=old and old.revision+1 or 1,stage="BEFORE_PENDING",before=old and clone(old.facts) or nil,target=clone(target),facts=old and clone(old.facts) or nil}
  write(pid,city,b,old,v);old=clone(v)
  v.facts=clone(target);v.stage="TARGET_PENDING";v.revision=v.revision+1;write(pid,city,b,old,v);old=clone(v)
  v.stage="DONE";v.revision=v.revision+1;write(pid,city,b,old,v)
 end
 local function guarded(pid,fn)
  local b=bucket(pid)
  if b.busy then b.halted=true;b.last="REENTRANT_HELD";return false end
  if b.halted then return false end
  b.busy=true;local ok,err=pcall(fn);b.busy=false
  if not ok then b.halted=true;b.last=tostring(err) end
  print("[SPC][B021][FLOW] "..pid.." "..b.last);return ok and not b.halted
 end
 local hook=SPCFreshBindingHook.Install(shared,P,function(e)
  assert(guarded(e.owner,function()
   assert(data.ready and data.hooks.complete=="REGISTERED","FLOW_LISTENER_NOT_READY")
   local city=CityManager.GetCity(e.owner,e.cityID);assert(identity(e.owner,city)==e.token,"FRESH_CHANGED")
   assert(read(e.owner,city)==nil,"NO_EXISTING_ADOPTION")
   local target=city:GetProperty("SPC_DEV_CITY_JOURNAL_B015")
   assert(target and target.specialization=="NONE" and target.health=="TRACKING","FRESH_TARGET_CHANGED")
   commit(e.owner,city,target);data.active[e.token]=true;data.owners[e.token]=e.owner;bucket(e.owner).last="FOUNDATION_DONE"
  end),"FLOW_FRESH_HELD")
 end,"DEV_ONLY")
 local function family(name)
  local seen={};local rows=P.Rows("DistrictReplaces");assert(rows,"REPLACEMENTS_UNAVAILABLE")
  for step=1,32 do
   assert(P.Info("Districts",name) and not seen[name],"DISTRICT_MAPPING_INVALID");seen[name]=true
   if P.Families[name] then return P.Families[name] end
   local parent
   for _,row in ipairs(rows) do if row.CivUniqueDistrictType==name then
    assert(not parent or parent==row.ReplacesDistrictType,"REPLACEMENT_CONFLICT");parent=row.ReplacesDistrictType
   end end
   if not parent then return "NON_V01" end;name=parent
  end
  error("MAPPING_LIMIT")
 end
 local function complete(pid,index,x,y)
  if not data.ready or not P.IsTestPlayer(pid) then return end
  guarded(pid,function()
   local info=P.Info("Districts",index);assert(info,"TYPE_UNAVAILABLE")
   local f=family(info.DistrictType);if f=="NON_V01" then return end
   local d=CityManager.GetDistrictAt(x,y);assert(d,"DISTRICT_UNAVAILABLE")
   local city=d:GetCity();assert(city and city:GetOwner()==pid and d:GetOwner()==pid and d:GetType()==index,"EVENT_IDENTITY")
   if shared.CityProgressionStore and shared.CityProgressionStore.Owns(city) then return end
   local raw=city:GetProperty(KEY)
   if raw==nil then bucket(pid).last="UNTRACKED_NO_WRITE";return end
   local token=identity(pid,city)
   if not data.active[token] then bucket(pid).last="LOAD_READ_ONLY_NO_WRITE";return end
   local old=read(pid,city);assert(old.stage=="DONE" and d:IsComplete()==true,"COMPLETION_NOT_READY")
   if old.facts.specialization~="NONE" then bucket(pid).last="LOCK_PRESERVED_NO_WRITE";return end
   local j=shared.CityJournalProbe.players[pid];assert(j and not j.halted,"LEGACY_COMPLETION_HELD")
   local target=city:GetProperty("SPC_DEV_CITY_JOURNAL_B015")
   assert(target and target.health=="TRACKING" and target.token==token,"LEGACY_RECORD_INVALID")
   assert(target.specialization==f,"LEGACY_COMPLETION_ORDER_OR_FAMILY")
   assert(target.first and target.first.districtID==d:GetID() and target.first.type==info.DistrictType
    and target.first.turn==Game.GetCurrentGameTurn() and target.revision==old.facts.revision+1,"LEGACY_EVENT_ORDER_MISMATCH")
   commit(pid,city,target);bucket(pid).last="COMPLETION_DONE"
  end)
 end
 function data.Read(pid,city)
  if shared.CityProgressionStore and shared.CityProgressionStore.Owns(city) then return "Game进度记录；旧Flow冻结" end
  if not P.IsTestPlayer(pid) then return "OUTSIDE_TEST_CIV" end
  local b=bucket(pid)
  local ok,line=pcall(function()
   local v=read(pid,city);if not v then return "UNTRACKED_NO_WRITE（旧城不补写）" end
   return "city="..v.cityID.." | "..v.stage.." rev="..v.revision
    .."\nDEV="..tostring(v.facts and v.facts.specialization).." / "..tostring(v.facts and v.facts.potential)
    .."\n模式="..(data.active[v.token] and (data.active[v.token]=="RESUMED_NORMAL" and "RESUMED_NORMAL" or "LIVE_THIS_LOAD") or "LOAD_HELD")
  end)
  local out="B021 新城流程 | "..(ok and line or ("READ_ERROR "..tostring(line)))
   .."\n本次加载写入="..b.writes.." stopped="..tostring(b.halted or false).." 最近="..b.last
   .."\nload="..tostring(data.ready).." complete="..tostring(data.hooks.complete)
   .."\n仅DEV记录；正常匹配存档恢复，缺失/冲突不补写。"
  print("[SPC][B021][READ] "..out);return out
 end
 -- Read-only permission for the bounded B022 carrier experiment; no DEV adoption.
 function data.SupportFacts(pid,city)
  if shared.CityProgressionStore and shared.CityProgressionStore.Owns(city) then return shared.CityProgressionStore.Base(pid,city) end
  assert(P.IsTestPlayer(pid) and data.ready and not bucket(pid).halted,"SUPPORT_FLOW_HELD")
  local v=read(pid,city)
  assert(v and v.stage=="DONE" and data.active[v.token],"SUPPORT_RECORD_NOT_ACTIVE")
  assert(same(v.facts,city:GetProperty("SPC_DEV_CITY_JOURNAL_B015")),"SUPPORT_JOURNAL_MISMATCH")
  return clone(v.facts)
 end
 local function resume(pid,city)
  if shared.CityProgressionStore and shared.CityProgressionStore.Owns(city) then return end
  local v=read(pid,city)
  if not v then return end -- old/untracked cities are never adopted
  assert(v.stage=="DONE","LOAD_PENDING_HELD")
  local j=shared.CityJournalProbe
  assert(j.phase=="AFTER_LOAD_CLOSE" and j.hooks.OnDistrictConstructed=="REGISTERED"
   and data.hooks.complete=="REGISTERED","LOAD_LISTENERS_NOT_READY")
  local b=j.players[pid];assert(b and not b.halted,"LOAD_LEGACY_HELD")
  local source=city:GetProperty("SPC_DEV_CITY_JOURNAL_B015")
  assert(same(v.facts,source),"LOAD_SOURCE_MISMATCH")
  if source.specialization=="NONE" then
   -- Reject an observable gap; this scan does not prove all past history.
   local center=false;local scanned=0
   for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
    scanned=scanned+1;assert(scanned<=512,"LOAD_SCAN_LIMIT")
    local c=d:GetCity();assert(c,"LOAD_DISTRICT_CITY")
    if c:GetOwner()==pid and c:GetID()==city:GetID() then
     local info=P.Info("Districts",d:GetType());assert(info,"LOAD_DISTRICT_TYPE")
     local complete=d:IsComplete();assert(type(complete)=="boolean","LOAD_COMPLETENESS")
     if info.DistrictType=="DISTRICT_CITY_CENTER" and complete then center=true end
     assert(not complete or family(info.DistrictType)=="NON_V01","LOAD_COMPLETED_SPECIALTY_WITHOUT_FACT")
    end
   end
   assert(center,"LOAD_CENTER_MISSING")
  else
   assert(source.first and family(source.first.type)==source.specialization,"LOAD_SPECIALTY_FACT_MISMATCH")
  end
  data.active[v.token]="RESUMED_NORMAL";data.owners[v.token]=pid
 end
 function data.ResumeInherited(pid,city)
  shared.CityJournalProbe.EnsureInherited(pid)
  assert(data.ready and not bucket(pid).halted,"INHERIT_FLOW_HELD")
  resume(pid,city)
 end
 local event=P.Field(GameEvents,"OnDistrictConstructed")
 if event and event.Add then local ok=pcall(event.Add,complete);data.hooks.complete=ok and "REGISTERED" or "ERROR" end
 local load=P.Field(Events,"LoadScreenClose")
 if load and load.Add then load.Add(function()
  data.ready=true
  for pid,player in pairs(Players) do if P.IsTestPlayer(pid) then
   local b=bucket(pid)
   if not b.halted then
    local ok,err=pcall(function() for _,city in player:GetCities():Members() do P.Count('city_scan'); resume(pid,city) end end)
    if not ok then
     b.halted=true;b.last=tostring(err)
     -- Player-wide failure must not leave previously scanned cities displayed active.
     for token in pairs(data.active) do
      if data.owners[token]==pid then data.active[token]=nil end
     end
    else b.last="LOAD_CHECK_COMPLETE" end
   end
   for _,city in player:GetCities():Members() do P.Count('city_scan'); data.Read(pid,city) end
  end end
 end) end
end
