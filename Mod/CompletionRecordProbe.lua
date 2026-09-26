-- DEV first OBSERVED completion, not a proven historical first specialization.
SPCCompletionRecordProbe={}
function SPCCompletionRecordProbe.Start(P,shared)
 if shared.CompletionRecordProbe then return end
 local KEY="SPC_DEV_COMPLETION_B014"
 local d={version=P.VERSION,phase="BEFORE_LOAD_CLOSE",players={},hooks={}}
 shared.CompletionRecordProbe=d
 local roots=P.Families
 local function bucket(pid)
  if not d.players[pid] then d.players[pid]={writes=0,last="NONE",busy=false} end
  return d.players[pid]
 end
 local function integer(v) return type(v)=="number" and v>=0 and v%1==0 and v<math.huge end
 local function family(typeName)
  local seen={};local current=typeName
  local rows=P.Rows("DistrictReplaces");assert(rows,"MAPPING_UNAVAILABLE")
  for step=1,32 do
   assert(not seen[current],"REPLACEMENT_CYCLE");seen[current]=true
   assert(P.Info("Districts",current),"UNKNOWN_DISTRICT")
   if roots[current] then return roots[current] end
   local parent
   for _,r in ipairs(rows) do if r.CivUniqueDistrictType==current then
    assert(not parent or parent==r.ReplacesDistrictType,"REPLACEMENT_CONFLICT");parent=r.ReplacesDistrictType
   end end
   if not parent then return "NON_V01" end
   current=parent
  end
  error("REPLACEMENT_LIMIT")
 end
 local function read(pid,city,token)
  local v=city:GetProperty(KEY)
  if v==nil then return nil end
  assert(type(v)=="table" and v.schema==1 and v.bindingToken==token and v.owner==pid
   and v.cityID==city:GetID() and v.kind=="FIRST_OBSERVED_COMPLETION"
   and integer(v.districtID) and integer(v.turn) and type(v.districtType)=="string"
   and v.observedFamily==family(v.districtType) and v.observedFamily~="NON_V01","RECORD_CONFLICT")
  return v
 end
 function d.Read(pid,city)
  if not P.IsTestPlayer(pid) then return "OUTSIDE_TEST_CIV" end
  local b=bucket(pid)
  local ok,text=pcall(function()
   local token,state=shared.BindingProbe.Resolve(pid,city)
   if not token then return "BINDING_NOT_READY "..tostring(state) end
   local v=read(pid,city,token)
   return "city="..city:GetID().." token="..token.."\n"..(v and ("OBSERVED_RECORD_MATCH\nfamily="..v.observedFamily
    .." type="..v.districtType.."\ndistrict="..v.districtID.." turn="..v.turn) or "NO_OBSERVED_RECORD")
  end)
  local result=P.VERSION.." | DEV完成记录\n"..(ok and text or ("READ_ERROR "..tostring(text)))
   .."\n本次加载记录写入="..b.writes.." 阶段="..d.phase
   .."\nConstructed="..tostring(d.hooks.OnDistrictConstructed).." Load="..tostring(d.hooks.LoadScreenClose)
   .."\n最近事件="..b.last.."\n仅首次观察记录；未锁定专业/授予Potential或收益。"
  print("[SPC][B014][RECORD] "..result);return result
 end
 local function onComplete(pid,index,x,y)
  if not P.IsTestPlayer(pid) then return end
  local b=bucket(pid)
  if d.phase~="AFTER_LOAD_CLOSE" then b.last="LOAD_IGNORED";return end
  if b.busy then b.last="REENTRANT_IGNORED";return end
  b.busy=true
  local ok,err=pcall(function()
   local info=P.Info("Districts",index);assert(info,"TYPE_UNAVAILABLE")
   local f=family(info.DistrictType)
   if f=="NON_V01" then b.last="NON_V01_IGNORED";return end
   local district=CityManager.GetDistrictAt(x,y);assert(district,"DISTRICT_UNAVAILABLE")
   local city=district:GetCity()
   assert(city and city:GetOwner()==pid and district:GetOwner()==pid and district:GetType()==index,"OBJECT_MISMATCH")
   if shared.CityProgressionStore and shared.CityProgressionStore.BlocksLegacy(city) then b.last="GAME_STORE_OR_PENDING";return end
   assert(district:IsComplete()==true,"NOT_COMPLETE")
   local token,state=shared.BindingProbe.Resolve(pid,city)
   if not token then b.last="BINDING_NOT_READY "..tostring(state);return end
   local old=read(pid,city,token)
   if old then b.last="EXISTING_OBSERVATION_NO_WRITE";return end
   local v={schema=1,kind="FIRST_OBSERVED_COMPLETION",bindingToken=token,owner=pid,cityID=city:GetID(),
    districtID=district:GetID(),districtType=info.DistrictType,observedFamily=f,turn=Game.GetCurrentGameTurn()}
   assert(integer(v.districtID) and integer(v.turn),"INVALID_EVENT_FIELDS")
   assert(shared.BindingProbe.Resolve(pid,city)==token and city:GetProperty(KEY)==nil,"STALE_BINDING_OR_RECORD")
   b.writes=b.writes+1;pcall(function() P.SetProperty(city,KEY,v) end)
   local after=read(pid,city,token);assert(after,"WRITE_UNCONFIRMED")
   for k,value in pairs(v) do assert(after[k]==value,"READBACK_MISMATCH") end
   for k in pairs(after) do assert(v[k]~=nil,"EXTRA_READBACK_FIELD") end
   b.last="OBSERVATION_SAVED"
  end)
  b.busy=false;if not ok then b.last="ERROR "..tostring(err) end
  print("[SPC][B014][RECORD] "..b.last)
 end
 local function listen(ns,name,fn)
  local e=P.Field(ns,name)
  if e and type(e.Add)=="function" then local ok=pcall(e.Add,fn);d.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
  else d.hooks[name]="ABSENT" end
 end
 listen(GameEvents,"OnDistrictConstructed",onComplete)
 listen(Events,"LoadScreenClose",function() d.phase="AFTER_LOAD_CLOSE" end)
end
