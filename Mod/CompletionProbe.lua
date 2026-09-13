-- B011: bounded read-only Gameplay observations; no specialization or Property writes.
SPCCompletionProbe={}
function SPCCompletionProbe.Start(P,shared)
 if shared.CompletionProbe then return end
 local data={version=P.VERSION,phase="BEFORE_LOAD_CLOSE",players={},hooks={},sequence=0}
 shared.CompletionProbe=data
 local function scalar(v) return P.Scalar(v):sub(1,100) end
 local function call(object,method,...)
  local ok,value=P.Call(object,method,...)
  if not ok then return "UNAVAILABLE" end
  if value==nil then return "nil" end
  return value
 end
 local function bucket(pid)
  local b=data.players[pid]
  if not b then b={rows={},built=0,constructed=0,added=0,dropped=0,errors=0};data.players[pid]=b end
  return b
 end
 local function family(info)
  if not info then return "UNKNOWN_TYPE" end
  local current=info.DistrictType;local seen={}
  local roots={DISTRICT_CAMPUS="RESEARCH",DISTRICT_THEATER="CULTURE",DISTRICT_INDUSTRIAL_ZONE="INDUSTRY",DISTRICT_COMMERCIAL_HUB="COMMERCE"}
  local replacements=P.Rows("DistrictReplaces")
  if not replacements then return "UNKNOWN_MAPPING" end
  for step=1,32 do
   if seen[current] then return "UNKNOWN_CYCLE" end;seen[current]=true
   if roots[current] then return roots[current] end
   local parent
   for _,row in ipairs(replacements) do
    if row.CivUniqueDistrictType==current then
     if parent and parent~=row.ReplacesDistrictType then return "UNKNOWN_CONFLICT" end
     parent=row.ReplacesDistrictType
    end
   end
   if not parent then return "NON_V01" end
   if not P.Info("Districts",parent) then return "UNKNOWN_PARENT" end
   current=parent
  end
  return "UNKNOWN_DEPTH"
 end
 local function observe(kind,pid,cityID,x,y,typeID,instanceID)
  if not P.IsTestPlayer(pid) then return end
  local b=bucket(pid);b[kind]=b[kind]+1;data.sequence=data.sequence+1
  local row={seq=data.sequence,kind=kind,phase=data.phase,turn=Game.GetCurrentGameTurn(),player=pid,
   cityID=cityID,districtID=instanceID,x=x,y=y,rawType=typeID}
  local ok,err=pcall(function()
   if kind=="built" then
    local city=CityManager.GetCity(pid,cityID)
    row.cityName=call(city,"GetName");row.owner=call(city,"GetOwner")
    row.observation=city and row.owner==pid and "CITY_OBSERVED" or "CITY_UNAVAILABLE"
    return
   end
   local eventInfo=P.Info("Districts",typeID)
   row.districtType=eventInfo and eventInfo.DistrictType or "UNKNOWN_TYPE"
   row.family=family(eventInfo)
   -- Static manager API, not a colon method. Errors remain explicit observations.
   local district=CityManager.GetDistrictAt(x,y)
   if not district then row.observation="DISTRICT_UNAVAILABLE";return end
   row.districtID=call(district,"GetID")
   row.owner=call(district,"GetOwner")
   row.objectType=call(district,"GetType")
   local objectInfo=P.Info("Districts",row.objectType)
   row.complete=call(district,"IsComplete");row.pillaged=call(district,"IsPillaged")
   local city=call(district,"GetCity")
   row.cityID=call(city,"GetID");row.cityOwner=call(city,"GetOwner");row.cityName=call(city,"GetName")
   if row.owner~=pid or row.cityOwner~=pid or not objectInfo or objectInfo.DistrictType~=row.districtType
    or (cityID~=nil and row.cityID~=cityID) or (instanceID~=nil and row.districtID~=instanceID) then
    row.observation="OBJECT_MISMATCH"
   elseif type(row.complete)~="boolean" then row.observation="COMPLETENESS_UNAVAILABLE"
   elseif row.complete then row.observation="COMPLETE_OBSERVED"
   else row.observation="NOT_COMPLETE" end
  end)
  if not ok then row.observation="READ_ERROR";row.error=scalar(err);b.errors=b.errors+1 end
  local labels={built="建城",constructed="完成通知",added="区域加入地图"}
  row.text="#"..row.seq.." "..labels[kind].." T"..scalar(row.turn).." "..row.phase
   .."\n城市="..scalar(row.cityID).." 区域实例="..scalar(row.districtID).." owner="..scalar(row.owner)
   .."\n"..scalar(row.districtType or row.cityName).." / "..scalar(row.family).." complete="..scalar(row.complete)
   .."\n"..scalar(row.observation)..(row.error and (" "..row.error) or "")
  b.rows[#b.rows+1]=row
  if #b.rows>64 then table.remove(b.rows,1);b.dropped=b.dropped+1 end
  print("[SPC]["..P.VERSION.."][COMPLETION] "..row.text:gsub("\n"," | "))
 end
 local function listen(namespace,name,fn)
  local e=P.Field(namespace,name)
  if e and type(P.Field(e,"Add"))=="function" then
   local ok=pcall(e.Add,fn);data.hooks[name]=ok and "REGISTERED" or "REGISTER_ERROR"
  else data.hooks[name]="ABSENT" end
 end
 listen(GameEvents,"CityBuilt",function(pid,cid,x,y) observe("built",pid,cid,x,y) end)
 listen(GameEvents,"OnDistrictConstructed",function(pid,typeID,x,y) observe("constructed",pid,nil,x,y,typeID) end)
 -- Only the first six documented fields are used; do not guess progress payload positions.
 listen(Events,"DistrictAddedToMap",function(pid,did,cid,x,y,typeID) observe("added",pid,cid,x,y,typeID,did) end)
 listen(Events,"LoadScreenClose",function() data.phase="AFTER_LOAD_CLOSE" end)
 print("[SPC]["..P.VERSION.."][COMPLETION] INITIALIZED; memory-only observations, counters reset per load")
end
