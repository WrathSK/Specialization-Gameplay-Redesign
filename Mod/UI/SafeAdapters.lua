-- ProductionPanel-local containment; native data and selection remain the base panel's.
SPCSafeAdapters={}
function SPCSafeAdapters.New()
 local d={entries={},hooks={},closed=false}
 local function clone(v,seen)
  if type(v)~='table'then return v end
  seen=seen or {};if seen[v]then return seen[v]end
  local o={};seen[v]=o;for k,x in pairs(v)do o[k]=clone(x,seen)end;return o
 end
 function d.Add(name,owns,keys,construct)
  local e={name=name,owns=owns,errors={},exports={}};d.entries[#d.entries+1]=e
  local before={};for _,key in ipairs(keys or {})do before[key]={value=ExposedMembers[key]}end
  local ok,api=pcall(construct)
  e.api=ok and type(api)=='table' and api or nil
  if not e.api then e.errors.New=ok and 'ADAPTER_API_INVALID' or tostring(api)end
  for _,key in ipairs(keys or {})do
   local current=ExposedMembers[key]
   if ok then e.exports[key]=current
   elseif current~=before[key].value then ExposedMembers[key]=before[key].value end
  end
  return e
 end
 function d.Call(e,method,...)
  if d.closed or not e or not e.api or e.unavailable then return false end
  local fn=e.api[method];if type(fn)~='function'then return true end
  local ok,value=pcall(fn,...);e.errors[method]=not ok and tostring(value) or nil
  return ok,value
 end
 function d.Items(e,data)
  if not e then return end
  if not e.api or e.unavailable or type(e.api.Items)~='function'then
   for _,key in ipairs({'ProjectItems','UnitItems'})do for _,item in ipairs(data[key] or {})do
    if (not e.api or e.unavailable) and e.owns(item)then item.Disabled=true;item.ToolTip='专业化界面暂不可用，请保留日志。'end
   end end
   return
  end
  -- Current adapters mutate list membership and row fields only. Copies are local
  -- to this UI render and never clone City/native handles or persist between calls.
  local projects,units=clone(data.ProjectItems),clone(data.UnitItems)
  local ok=d.Call(e,'Items',data)
  if not ok then
   data.ProjectItems=projects;data.UnitItems=units
   for _,key in ipairs({'ProjectItems','UnitItems'})do for _,item in ipairs(data[key] or {})do
    if e.owns(item)then item.Disabled=true;item.ToolTip='专业化界面暂不可用，请保留日志。'end
   end end
  end
 end
 function d.Before(e,c,item,queued)
  if not e or not e.api or e.unavailable or type(e.api.Before)~='function'then return not (e and e.owns(item))end
  local ok,result=d.Call(e,'Before',c,item,queued)
  if not ok then return not e.owns(item)end
  return not not result
 end
 function d.Hook(source,name,e,method,fn)
  local event=source and source[name];if not event or type(event.Add)~='function'then return end
  local active=true
  local callback=function(...)if active and not d.closed then
   if fn then pcall(fn,...)else d.Call(e,method,...)end
  end end
  d.hooks[#d.hooks+1]={event,callback}
  local ok,err=pcall(event.Add,callback)
  if not ok then
   active=false
   if e then e.unavailable=true;e.errors['Hook:'..name]=tostring(err)end
  end
 end
 function d.Close()
  if d.closed then return end;d.closed=true
  for _,h in ipairs(d.hooks)do if h[1].Remove then pcall(h[1].Remove,h[2])end end;d.hooks={}
  for _,e in ipairs(d.entries)do
   if e.api and type(e.api.Close)=='function'then pcall(e.api.Close)end
   for key,value in pairs(e.exports)do
   if ExposedMembers[key]==value then ExposedMembers[key]=nil end
  end end
 end
 return d
end
