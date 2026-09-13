-- Background startup retry: no dependency on opening P0 or the native trade screen.
include('Probe')
local P=SPCP0;local busy=false;local hooks={}
local function refresh()
 local s=ExposedMembers.SPC_P0;local pid=Game.GetLocalPlayer()
 if busy or not s or s.Version~=P.VERSION or not s.NetworkBoost or not P.IsTestPlayer(pid) then return end
 if s.NetworkBoost.ready and s.GreatWorkProbe and s.GreatWorkProbe.ready then return end
 busy=true
 local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='BOOST_INIT',Token=P.VERSION..':boost:init'})
 busy=false;if not ok then print('[SPC][B055][INIT] '..tostring(err)) end
end
ContextPtr:SetInitHandler(function()
 for _,name in ipairs({'SystemUpdateUI','LoadScreenClose','GameCoreEventPlaybackComplete'}) do
  local e=P.Field(Events,name);if e and e.Add then e.Add(refresh);hooks[#hooks+1]=e end
 end
 refresh()
end)
ContextPtr:SetShutdown(function() for _,e in ipairs(hooks) do if e.Remove then e.Remove(refresh) end end end)
