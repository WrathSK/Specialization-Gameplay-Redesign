-- Ordered startup containment only; not an event bus, fact cache or restart manager.
SPCRuntimeComposition={}
local M=SPCRuntimeComposition
local natives=setmetatable({},{__mode='k'})
function M.Native(source)return natives[source] or source end
local function failed(entry)return entry.state=='FAILED' or entry.state=='SKIPPED_DEPENDENCY'end
function M.New(shared)
 local d={entries={},order={}};shared.StartStatus=d.entries
 -- Explicit production duties are reserved before their owners start. No
 -- discovery, restart or replacement cleanup: each owner supplies its old body.
 local cleanup={RegisterExit={},RegisterReturn={}};local cleanupStore
 function d.RequireCleanup(name,exit,returned)
  assert(not d.sealed and not d.entries[name],'CLEANUP_REQUIREMENT_LATE')
  local store=assert(shared.CityProgressionStore,'CLEANUP_STORE_UNAVAILABLE')
  assert(not cleanupStore or cleanupStore==store,'CLEANUP_STORE_CHANGED');cleanupStore=store
  local function reserve(key,label)
   if label==nil then return end
   assert(type(label)=='string'and #label>0 and not cleanup[key][label],'CLEANUP_REQUIREMENT_CONFLICT')
   local slot={owner=name};cleanup[key][label]=slot
   assert(type(store[key])=='function','CLEANUP_REGISTRY_UNAVAILABLE')
   store[key](label,function(...)
    local entry=d.entries[name]
    assert(shared.CityProgressionStore==store and entry and entry.state=='OK'and type(slot.fn)=='function',
     'CLEANUP_OWNER_UNAVAILABLE '..name)
    return slot.fn(...)
   end)
  end
  reserve('RegisterExit',exit);reserve('RegisterReturn',returned)
 end
 function d.Run(name,deps,exports,fn,fields)
  assert(not d.entries[name],'START_DUPLICATE_ENTRY')
  local entry={state='STARTING'};d.entries[name]=entry;d.order[#d.order+1]=name
  for _,dep in ipairs(deps or {})do
   if not d.entries[dep] or d.entries[dep].state~='OK'then
    entry.state='SKIPPED_DEPENDENCY';entry.code=dep;return false
   end
  end
  local prior={};for _,key in ipairs(exports or {})do prior[key]={value=shared[key]}end
  local slots={{shared,'OnPermanentCityWrite',shared.OnPermanentCityWrite},{shared,'OnFreshCityBinding',shared.OnFreshCityBinding}}
  for _,slot in ipairs(fields or {})do slots[#slots+1]={slot[1],slot[2],slot[1][slot[2]]}end
  local hooks={};local original={Events=Events,GameEvents=GameEvents,LuaEvents=LuaEvents}
  local handles={} -- native event identity → original callback → guard, within this entry
  local function facade(source)
   if source==nil then return nil end
   local cache={};local namespace=setmetatable({}, {__index=function(_,key)
    local event=source[key];if not event or type(event.Add)~='function'then return event end
    if cache[key]then return cache[key]end
    local byfn=handles[event];if not byfn then byfn={};handles[event]=byfn end
    local proxy=setmetatable({}, {__index=function(_,method)
     if method=='Add'then return function(fn)
      assert(type(fn)=='function','START_CALLBACK_TYPE')
      local guard=byfn[fn]
      if not guard then guard=function(...)if not failed(entry)then return fn(...)end end;byfn[fn]=guard end
      hooks[#hooks+1]={event=event,fn=guard};return event.Add(guard)
     end end
     if method=='Remove'then
      if type(event.Remove)~='function'then return nil end
      return function(fn)return event.Remove(byfn[fn] or fn)end
     end
     return event[method]
    end,__call=function(_,...)return event(...)end})
    cache[key]=proxy;return proxy
   end,__newindex=function()error('START_EVENT_NAMESPACE_WRITE',0)end})
   natives[namespace]=source;return namespace
  end
  local methods={}
  local function registration(owner,key)
   if not owner or type(owner[key])~='function'then return end
   local native=owner[key];local wrapped=function(label,fn,...)
    assert(type(fn)=='function','START_REGISTRATION_TYPE')
    local guarded=function(...)
     assert(not failed(entry),'STARTUP_FAILED_'..name)
     return fn(...)
    end
    local slots=owner==cleanupStore and cleanup[key]
    local slot=slots and slots[label]
    if slot then
     assert(not d.sealed and slot.owner==name and not slot.fn,'CLEANUP_REGISTRATION_CONFLICT')
     slot.fn=guarded;return
    end
    return native(label,guarded,...)
   end
   methods[#methods+1]={owner,key,native,wrapped};owner[key]=wrapped
  end
  registration(shared.CityProgressionStore,'RegisterExit')
  registration(shared.CityProgressionStore,'RegisterReturn')
  registration(shared.LegacyCleanup,'RegisterRunner')
  registration(shared.LegacyCleanup,'RegisterPostCleanup')
  registration(shared.GreatWorkFacts,'RegisterConsumer')
  registration(shared.FactChanges,'RegisterConsumer')
  registration(shared.DistrictCompleteness,'RegisterConsumer')
  registration(shared.NetworkBridge,'RegisterConsumer')
  Events=facade(original.Events);GameEvents=facade(original.GameEvents);LuaEvents=facade(original.LuaEvents)
  local ok,err=pcall(fn)
  Events=original.Events;GameEvents=original.GameEvents;LuaEvents=original.LuaEvents
  for _,slot in ipairs(methods)do if slot[1][slot[2]]==slot[4]then slot[1][slot[2]]=slot[3]end end
  entry.state=ok and 'OK' or 'FAILED'
  if not ok then
   entry.code=tostring(err):match('([A-Z][A-Z0-9_]+)') or 'START_ERROR'
   pcall(print,'[SPC][START_FAILED] '..name..':'..entry.code)
   for _,h in ipairs(hooks)do if type(h.event.Remove)=='function'then pcall(h.event.Remove,h.fn)end end
   for key,v in pairs(prior)do shared[key]=v.value end
   for _,slot in ipairs(slots)do slot[1][slot[2]]=slot[3]end
  end
  return ok
 end
 function d.Complete()
  local failures=0;for _,e in pairs(d.entries)do if e.state~='OK'then failures=failures+1 end end
  d.sealed=true;d.failures=failures;return failures
 end
 return d
end
