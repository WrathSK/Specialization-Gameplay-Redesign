include('Probe')
include('SampleLifecycle')
local P=SPCP0;local busy=false;local hooks={};local elapsed=0
local public={state='LOADED',attempts=0,requests=0};ExposedMembers.SPC_CopyBackground=public
local client=SPCSampleLifecycle.Client(P,'copy','COPY_YIELD_SAMPLE',public)
local function refresh()
 local shared=ExposedMembers.SPC_P0;local data=shared and shared.CopyYields
 if busy or not shared or shared.Version~=P.VERSION or not data or not data.ready then return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
 public.attempts=public.attempts+1
 if not client.Before(data) then return end
 busy=true;local rows={};local n=0
 local ok,err=pcall(function()
  for _,r in pairs(SPCSampleLifecycle.Live(P,pid,false)) do
    local sum,prod=0,0
    for _,y in ipairs({'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'}) do
     local v=r.district:GetYield(P.Info('Yields','YIELD_'..y).Index)
     assert(type(v)=='number' and v==v and math.abs(v)<1e8,'COPY_UI_YIELD_UNKNOWN')
     sum=sum+v;if y=='PRODUCTION' then prod=v end
    end
    n=n+1;rows[#rows+1]=r.cityID..','..r.id..','..r.reference..','..string.format('%.17g',sum)..','..string.format('%.17g',prod)
  end
  table.sort(rows)
 end)
 public.error=not ok and tostring(err) or nil;public.count=n
 client.Send(pid,data,ok,rows,n);busy=false
end
local function safe() local ok,err=pcall(refresh);if not ok then busy=false;public.state='ERROR';public.error=tostring(err) end end
local function bind(name,fn) local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn} end end
ContextPtr:SetInitHandler(function()
 for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','PlayerTurnActivated'}) do bind(name,safe) end
 bind('LoadScreenClose',function() client.Reset();safe() end)
 bind('SystemUpdateUI',function()
  local shared=ExposedMembers.SPC_P0;local d=shared and shared.CopyYields
  if public.pending==1 or not d or not d.samples[Game.GetLocalPlayer()] then safe() end
 end)
 ContextPtr:SetUpdate(function(dt)
  client.Tick(dt)
  if type(dt)=='number' and dt>=0 then elapsed=elapsed+dt;if elapsed>=1 then elapsed=0;safe() end end
 end)
 safe()
end)
ContextPtr:SetShutdown(function()
 client.Close();ContextPtr:ClearUpdate()
 for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end
 if ExposedMembers.SPC_CopyBackground==public then ExposedMembers.SPC_CopyBackground=nil end
end)
