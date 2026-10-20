-- Event-driven display only. Instances are children of native city-banner containers.
include('LevelBannerModel')
local M=SPCLevelBannerModel
local entries={};local lastBackend,lastRevision
local bindings={}
local function destroy(k)
 local e=entries[k];if e then e.parent:DestroyChild(e.controls.Root);entries[k]=nil end
end
local function color(c,t)c:SetColor(UI.GetColorValue(t[1]/255,t[2]/255,t[3]/255,t[4]/255))end
local function render(e)
 local d=(ExposedMembers.SPC_P0 or {}).LevelBanners
 local v=d and d.views[e.pid..':'..e.id]
 local m=Game.GetLocalPlayer()==e.pid and M.View(v,e.pid,e.id,e.x,e.y) or nil
 local c=e.controls;c.Root:SetHide(not m);if not m then return end
 -- Exact cell and control size: use the proven Image icon path without stretching.
 c.Badge:SetIcon(m.icon,32);c.Badge:SetSizeVal(32,32)
 local bright=M.Colors[m.kind];local dark={19,35,55,255};local dim={70,83,103,255}
 for i,state in ipairs(m.segments)do
  color(c['Rim'..i],state=='DIM' and dim or bright)
  color(c['Fill'..i],state=='FILLED' and bright or dark)
 end
 c.Root:SetToolTipString(Locale.Lookup('LOC_SPC_LEVEL_BANNER_HELP',Locale.Lookup('LOC_SPC_LEVEL_'..m.kind),m.active,m.potential))
end
local function attach(pid,id,x,y,parent)
 local k=pid..':'..id
 if pid~=Game.GetLocalPlayer()then destroy(k);return end
 local e=entries[k]
 if e and (e.parent~=parent or e.x~=x or e.y~=y)then destroy(k);e=nil end
 if not e then
  local controls={};ContextPtr:BuildInstanceForControl('SPCLevelBannerInstance',controls,parent)
  e={pid=pid,id=id,x=x,y=y,parent=parent,controls=controls};entries[k]=e
 end
 render(e)
end
local function detach(parent)
 for k,e in pairs(entries)do if e.parent==parent then destroy(k)end end
end
local function published()
 local d=(ExposedMembers.SPC_P0 or {}).LevelBanners
 if d==lastBackend and (d and d.revision)==lastRevision then return end
 lastBackend=d;lastRevision=d and d.revision
 for _,e in pairs(entries)do render(e)end
end
local function ready()LuaEvents.SPC_LevelBannerReady();published()end
local function bind(source,name,fn)
 local e=source[name];if e then e.Add(fn);bindings[#bindings+1]={e,fn}end
end
ContextPtr:SetInitHandler(function()
 bind(LuaEvents,'SPC_LevelBannerAttach',attach);bind(LuaEvents,'SPC_LevelBannerDetach',detach)
 bind(Events,'GameCoreEventPublishComplete',published);bind(Events,'GameCoreEventPlaybackComplete',published)
 bind(Events,'LoadScreenClose',ready)
 bind(Events,'LocalPlayerChanged',function()for k in pairs(entries)do destroy(k)end;ready()end)
 ready()
end)
ContextPtr:SetShutdown(function()
 for _,b in ipairs(bindings)do b[1].Remove(b[2])end
 for k in pairs(entries)do destroy(k)end
 entries={};bindings={};lastBackend=nil;lastRevision=nil
end)
