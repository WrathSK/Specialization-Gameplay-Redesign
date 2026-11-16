if not SPCLegacyCleanupCatalog then include('LegacyCleanupCatalog')end
-- Explicit held cleanup only. No listeners, timers, scans or positive effects.
SPCLegacyCleanup={}
function SPCLegacyCleanup.Start(P,shared)
 local store=assert(shared.CityProgressionStore,'LEGACY_STORE_UNAVAILABLE')
 assert(type(store.IsExitCurrent)=='function'and type(store.ExitCompleted)=='function','LEGACY_EXIT_PROOF_UNAVAILABLE')
 local d={};shared.LegacyCleanup=d
 local keys=SPCLegacyCleanupCatalog.Keys();local runners,posts={},{}
 local ledger=setmetatable({},{__mode='k'}) -- values contain no ticket, function or native object
 local requiresRunner={Lv3Support=true,Lv3Effects=true}
 local function text(value)local ok,s=pcall(tostring,value);return ok and type(s)=='string'and s:sub(1,180)or'LEGACY_GROUP_FAILED'end
 local function current(c,loss,ticket,slot)
  assert(store.IsExitCurrent('LegacyCleanup',c,loss,ticket,slot)==true,'LEGACY_EXIT_CHANGED')
 end
 local function state(ticket)
  assert(type(ticket)=='table','LEGACY_TICKET_INVALID')
  local s=ledger[ticket];if not s then s={done={},errors={},running={},awaiting={}};ledger[ticket]=s end;return s
 end
 local function allDone(s,except)
  for _,key in ipairs(keys)do if key~=except and not s.done[key]then return false end end;return true
 end
 function d.RegisterRunner(key,fn)
  assert(requiresRunner[key]and type(fn)=='function'and not runners[key],'LEGACY_RUNNER_REGISTRATION_INVALID');runners[key]=fn
 end
 function d.RegisterPostCleanup(key,fn)
  assert(key=='Dialogue'and type(fn)=='function'and not posts[key],'LEGACY_POST_REGISTRATION_INVALID');posts[key]=fn
 end
 local function read(c,loss,ticket,slot,fn)
  local ok,value=pcall(fn);current(c,loss,ticket,slot)
  if not ok then error(value,0)end;return value
 end
 local function descriptor(key,c,loss,ticket,slot)
  if key=='NetworkBoost'then
   if not SPCBoostConfig then include('BoostConfig')end
   if not SPCBoostIntegerConfig then include('BoostIntegerConfig')end
   current(c,loss,ticket,slot)
   return SPCLegacyCleanupCatalog.Group(key,nil,SPCBoostConfig and SPCBoostConfig.rows,SPCBoostIntegerConfig and SPCBoostIntegerConfig.rows)
  elseif key=='Dialogue'then
   local n=read(c,loss,ticket,slot,function()local count=0;for _ in GameInfo.Eras()do count=count+1 end;return count end)
   return SPCLegacyCleanupCatalog.Group(key,n)
  end
  return SPCLegacyCleanupCatalog.Group(key)
 end
 local function physical(key,c,loss,ticket,slot)
  local s=state(ticket)
  assert(not s.running[key],'LEGACY_GROUP_BUSY');s.running[key]=true
  local ok,why=pcall(function()
   current(c,loss,ticket,slot);s.done[key]=nil;s.awaiting[key]=nil
   local row=descriptor(key,c,loss,ticket,slot)
   if row.kind=='plot_flags'then
    local plot=read(c,loss,ticket,slot,function()return Map.GetPlot(c:GetX(),c:GetY())end);assert(plot,'LEGACY_PLOT_UNKNOWN')
    for _,name in ipairs(row.names)do
     local value=read(c,loss,ticket,slot,function()return plot:GetProperty(name)end)
     if value~=nil and value~=0 then
      current(c,loss,ticket,slot);P.SetProperty(plot,name,0);current(c,loss,ticket,slot)
      assert(read(c,loss,ticket,slot,function()return plot:GetProperty(name)end)==0,'LEGACY_PLOT_WRITE_UNCONFIRMED')
     end
    end
   else
    local catalog=read(c,loss,ticket,slot,function()return GameInfo and GameInfo.Buildings end);assert(catalog~=nil,'LEGACY_BUILDINGS_UNAVAILABLE')
    local readable=read(c,loss,ticket,slot,function()
     local iterator,source,key=catalog();assert(type(iterator)=='function','LEGACY_BUILDINGS_UNAVAILABLE')
     local first=iterator(source,key);return first~=nil and type(first.BuildingType)=='string'and #first.BuildingType>0
    end)
    assert(readable,'LEGACY_BUILDINGS_UNAVAILABLE') -- one readiness row, never a full catalogue scan
    local buildings=read(c,loss,ticket,slot,function()return c:GetBuildings()end);assert(buildings,'LEGACY_BUILDINGS_UNAVAILABLE')
    local rows,seen={},{}
    for _,name in ipairs(row.names)do
     local definition=read(c,loss,ticket,slot,function()return catalog[name]end)
     if definition~=nil then
      local v=read(c,loss,ticket,slot,function()return {id=definition.Index,internal=definition.InternalOnly}end)
      assert((v.internal==true or v.internal==1)and type(v.id)=='number'and v.id>=0 and v.id%1==0 and not seen[v.id],'LEGACY_DEFINITION_INVALID');seen[v.id]=true
      local has=read(c,loss,ticket,slot,function()return P.HasBuilding(buildings,v.id)end);assert(type(has)=='boolean','LEGACY_PRESENCE_UNKNOWN')
      rows[#rows+1]={id=v.id,has=has}
     end -- only a successful exact native lookup returning nil proves absence
    end
    for _,v in ipairs(rows)do if v.has then
     current(c,loss,ticket,slot);P.RemoveBuilding(buildings,v.id);current(c,loss,ticket,slot)
     assert(read(c,loss,ticket,slot,function()return P.HasBuilding(buildings,v.id)end)==false,'LEGACY_REMOVE_UNCONFIRMED')
    end end
   end
   if key=='Dialogue'then
    local post=assert(posts[key],'LEGACY_POST_UNAVAILABLE');assert(post(c,loss)~=false,'LEGACY_POST_UNCONFIRMED');current(c,loss,ticket,slot)
   end
  end)
  s.running[key]=nil
  if not ok then error(why,0)end
  current(c,loss,ticket,slot);return true
 end
 local function complete(key,c,loss,ticket,slot,proved)
  if not proved then return false end
  local s=state(ticket);local attempt={};s.awaiting[key]=attempt
  local ok,value=pcall(function()
   current(c,loss,ticket,slot)
   if s.awaiting[key]~=attempt then return false end
   if not s.sweeping and allDone(s,key)then
    local function confirmed()
     return ledger[ticket]==s and s.awaiting[key]==attempt and allDone(s,key)and(not slot or slot())
    end
    if store.ExitCompleted('LegacyCleanup',c,loss,ticket,confirmed)~=true then return false end
   end
   if s.awaiting[key]~=attempt then return false end
   s.done[key]=attempt;s.errors[key]=nil;return true
  end)
  if s.awaiting[key]==attempt then s.awaiting[key]=nil end
  return ok and value==true
 end
 local function runGroup(key,c,loss,ticket)
  local proved=false
  local function clean(city,proof,cap,slot)proved=false;physical(key,city,proof,cap,slot);proved=true;return true end
  if requiresRunner[key]then
   local factory=assert(runners[key],'LEGACY_RUNNER_UNAVAILABLE')
   local fn=factory(clean,function(city,proof,cap,slot)return complete(key,city,proof,cap,slot,proved)end)
   assert(type(fn)=='function','LEGACY_RUNNER_INVALID');assert(fn(c,loss,ticket)~=false,'LEGACY_RUNNER_UNCONFIRMED')
  else
   clean(c,loss,ticket);assert(complete(key,c,loss,ticket,nil,proved),'LEGACY_GROUP_UNCONFIRMED')
  end
 end
 function d.Exit(c,loss,ticket)
  local s=state(ticket);assert(not s.sweeping,'LEGACY_SWEEP_BUSY');s.sweeping=true
  local ok,why=pcall(function()
   current(c,loss,ticket)
   for _,key in ipairs(keys)do if not s.done[key]then
    local good,value=pcall(function()assert(not s.awaiting[key],'LEGACY_GROUP_BUSY');runGroup(key,c,loss,ticket)end)
    if not good then s.errors[key]=text(value)end
    current(c,loss,ticket)
   end end
   local pending={};for _,key in ipairs(keys)do if not s.done[key]then pending[#pending+1]=key end end
   assert(#pending==0,'LEGACY_GROUP_PENDING '..table.concat(pending,','))
   assert(store.ExitCompleted('LegacyCleanup',c,loss,ticket,function()return ledger[ticket]==s and allDone(s)end)==true,'LEGACY_ACK_UNCONFIRMED')
  end)
  s.sweeping=false
  if not ok then error(why,0)end;return true
 end
 return d
end
