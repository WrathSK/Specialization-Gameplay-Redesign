include('DiagnosticLog')
local print=SPCDiagnosticLog and SPCDiagnosticLog.For('CopyYieldRefresh') or print
-- B051 bounded background UI sampling; no panel dependency and no city-total feedback.
include('Probe')
local P=SPCP0
local elapsed=0;local sent;local seq=0;local busy=false;local initialized=false;local hooks={}
local public={state='LOADED',attempts=0,requests=0}
ExposedMembers.SPC_CopyBackground=public
local function code(err) return tostring(err):match('COPY_[A-Z_]+') or 'COPY_UI_EXCEPTION' end
local function refresh()
 local shared=ExposedMembers.SPC_P0
 if busy then return end
 if not shared or shared.Version~=P.VERSION or not shared.CopyYields or not shared.CopyYields.ready then public.state='WAIT_GAMEPLAY';return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
 busy=true;public.generation=shared.CopyYields.generation;public.attempts=public.attempts+1;public.state='SAMPLING'
 local count=0;local rows={}
 local ok,err=pcall(function()
  for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
   local c=d:GetCity();local row=P.Info('Districts',d:GetType())
   if c and c:GetOwner()==pid and d:IsComplete() and row then
    local sum,prod=0,0
    for _,y in ipairs({'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'}) do
     local n=d:GetYield(P.Info('Yields','YIELD_'..y).Index)
     assert(type(n)=='number' and n==n and math.abs(n)<1e8,'COPY_UI_YIELD_UNKNOWN')
     sum=sum+n;if y=='PRODUCTION' then prod=n end
    end
    count=count+1;assert(count<=512,'COPY_UI_ROW_LIMIT')
    rows[#rows+1]=c:GetID()..','..d:GetID()..','..string.format('%.17g',sum)..','..string.format('%.17g',prod)
   end
  end
  table.sort(rows)
 end)
 public.error=not ok and code(err) or nil
 local turn=Game.GetCurrentGameTurn();local payload=ok and table.concat(rows,';') or ''
 local signature=shared.CopyYields.generation..':'..turn..':'..tostring(ok)..':'..payload
 if signature~=sent or (shared.CopyYields.seq[pid] or -1)~=seq then
  seq=math.max(seq,shared.CopyYields.seq[pid] or 0)+1;local old=sent;sent=signature
  public.requests=public.requests+1;public.seq=seq;public.count=count
  local delivered,why=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
   {OnStart='SPC_P0_Request',Action='COPY_YIELD_SAMPLE',Token=P.VERSION..':copy:'..seq,Seq=seq,Generation=shared.CopyYields.generation,Turn=turn,Valid=ok and 1 or 0,Count=ok and count or 0,Data=payload})
  if not delivered then sent=old;public.error='COPY_SEND_ERROR';print('[SPC][B051][SEND_ERROR] '..tostring(why)) end
 end
 if not ok then print('[SPC][B051][UI_ERROR] '..tostring(err)) end
 public.state=public.error and 'ERROR' or 'SAMPLED'
 initialized=ok and shared.CopyYields.samples[pid]~=nil
 busy=false
end
local function safelyRefresh()
 local ok,err=pcall(refresh)
 if not ok then busy=false;public.state='ERROR';public.error=code(err);print('[SPC][B051][BACKGROUND_ERROR] '..tostring(err)) end
end
local function bind(name,fn)
 local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn} end
end
ContextPtr:SetInitHandler(function()
 -- Established event-driven path: runs even when this empty context receives no frame updates.
 for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','PlayerTurnActivated'}) do bind(name,safelyRefresh) end
 bind('LoadScreenClose',function() initialized=false;sent=nil;safelyRefresh() end)
 bind('SystemUpdateUI',function()
  local shared=ExposedMembers.SPC_P0;local d=shared and shared.CopyYields
  if not initialized or (d and d.ready and d.generation~=public.generation) then safelyRefresh() end
 end)
 safelyRefresh()
 ContextPtr:SetUpdate(function(dt)
  if type(dt)~='number' or dt<0 then return end
  elapsed=elapsed+dt;if elapsed>=1 then elapsed=0;safelyRefresh() end
 end)
end)
ContextPtr:SetShutdown(function()
 ContextPtr:ClearUpdate()
 for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end
 if ExposedMembers.SPC_CopyBackground==public then ExposedMembers.SPC_CopyBackground=nil end
end)
