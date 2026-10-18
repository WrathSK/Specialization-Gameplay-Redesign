"""Fixture-only native RequestRefresh frames; never a runtime scheduler."""
SOURCE=r"""
if not refreshContexts then
 refreshContexts={};refreshEventDepth=0;refreshDraining=false;refreshAuto=true;refreshFrames=0
 function drainRefreshFrames(limit)
  if refreshDraining or refreshEventDepth>0 then return end
  refreshDraining=true
  local rounds=0
  while rounds<(limit or 64)do
   local batch={};for c in pairs(refreshContexts)do if c.refreshPending then batch[#batch+1]=c end end
   if #batch==0 then break end
   rounds=rounds+1;refreshFrames=refreshFrames+1
   for _,c in ipairs(batch)do
    if c.refreshPending and c.refreshHandler then
     c.refreshPending=false;c.refreshHandler()
    end
   end
  end
  refreshDraining=false
 end
 function refreshEvent(fn,...)
  refreshEventDepth=refreshEventDepth+1
  local r=table.pack(pcall(fn,...))
  refreshEventDepth=refreshEventDepth-1
  if refreshEventDepth==0 and refreshAuto and not refreshDraining then drainRefreshFrames()end
  if not r[1]then error(r[2],0)end
  return table.unpack(r,2,r.n)
 end
 function wrapRefreshEvent(e)
  local mt=getmetatable(e)
  if mt and mt.__call and not mt.refreshWrapped then
   local call=mt.__call;mt.__call=function(...)return refreshEvent(call,...)end;mt.refreshWrapped=true
  end
  return e
 end
 function refreshContext(c,handler)
  refreshContexts[c]=true
  function c:SetRefreshHandler(fn)self.refreshHandler=fn end
  function c:RequestRefresh()self.refreshPending=true;self.refreshRequests=(self.refreshRequests or 0)+1 end
  function c:ClearRequestRefresh()self.refreshPending=false end
  if handler then c:SetRefreshHandler(handler)end
 end
end
for _,ns in ipairs({Events or {},LuaEvents or {}})do for _,e in pairs(ns)do if type(e)=='table'then wrapRefreshEvent(e)end end end
if event then local original=event;event=function(...)return wrapRefreshEvent(original(...))end end
"""
def install(lua,context='ContextPtr',handler=None):
 lua.execute(SOURCE)
 lua.execute('refreshContext('+context+(','+handler if handler else '')+')')


def install_native_events(lua):
 """Legacy lifecycle fixtures supply subsequent engine publications explicitly.

 No frame delivers these. B227's ordering/starvation suite sets nativeAuto=false
 and supplies each event itself; these convenience events are not native evidence.
 """
 lua.execute(r"""
 nativeAuto=true;nativeEventDepth=0;nativeSettling=false
 for _,e in pairs(Events)do
  local mt=type(e)=='table' and getmetatable(e)
  if mt and mt.__call and not mt.nativeWrapped then
   local call=mt.__call
   mt.__call=function(...)
    nativeEventDepth=nativeEventDepth+1
    local result=table.pack(pcall(call,...))
    nativeEventDepth=nativeEventDepth-1
    if nativeEventDepth==0 and nativeAuto and not nativeSettling then
     nativeSettling=true
     for i=1,6 do Events.GameCoreEventPublishComplete()end
     nativeSettling=false
    end
    if not result[1]then error(result[2],0)end
    return table.unpack(result,2,result.n)
   end
   mt.nativeWrapped=true
  end
 end
 """)
