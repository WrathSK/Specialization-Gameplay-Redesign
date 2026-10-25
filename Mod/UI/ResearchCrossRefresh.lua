include('Probe')
include('SampleLifecycle')
include('ResearchCrossSample')
local P=SPCP0;local busy=false;local hooks={};local seenData,seenGeneration,seenTurn,seenSample
local public={state='LOADED',attempts=0,requests=0};ExposedMembers.SPC_ResearchCrossBackground=public
local client=SPCSampleLifecycle.Client(P,'cross','RESEARCH_CROSS_SAMPLE',public,{recoveryProof=true})
local replacements
local sampler=SPCSampleLifecycle.Sampler(P,false,function(pid,r)
 local d=r.district;local pillaged=d:IsPillaged();assert(type(pillaged)=='boolean','CROSS_PILLAGE_UNKNOWN')
 local fields={r.cityID,r.id,r.reference,pillaged and '1'or '0'}
 replacements=replacements or SPCResearchCrossSample.Replacements(P)
 local domain=SPCResearchCrossModel.Domain(r.type,replacements)
 for _,y in ipairs(SPCResearchCrossModel.Yields)do
  local value=0
  if domain and not pillaged then value=Map.GetPlot(r.x,r.y):GetAdjacencyYield(pid,r.cityID,d:GetType(),P.Info('Yields','YIELD_'..y).Index)end
  assert(type(value)=='number'and value==value and math.abs(value)<1e8,'CROSS_BASE_UNAVAILABLE')
  fields[#fields+1]=string.format('%.17g',value)
 end
 return table.concat(fields,',')
end,160000)
local function refresh()
 local shared=ExposedMembers.SPC_P0;local data=shared and shared.ResearchCross
 if busy or not shared or shared.Version~=P.VERSION or not data or not data.ready then return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid)then return end
 local turn=Game.GetCurrentGameTurn()
 if data~=seenData or data.generation~=seenGeneration then sampler.Reset()
 elseif turn~=seenTurn or data.sampleRevision~=seenSample then sampler.All()end
 seenData=data;seenGeneration=data.generation;seenTurn=turn;seenSample=data.sampleRevision
 if not sampler.Pending()and public.pending==0 and not client.NeedsSample()then return end
 public.attempts=public.attempts+1
 if not client.Before(data)then return end
 if not sampler.Pending()and not client.NeedsSample()then return end
 busy=true
 replacements=nil
 local valid,rows,n,err=sampler.Read(pid)
 if valid==nil then busy=false;return end -- superseded by a real cause retained for the next boundary
 local current=ExposedMembers.SPC_P0
 if current~=shared or current.ResearchCross~=data or current.Version~=P.VERSION
  or data.generation~=seenGeneration or data.sampleRevision~=seenSample or Game.GetLocalPlayer()~=pid then
  sampler.All();busy=false;return -- changed source/reference cause remains pending,never sends old context data
 end
 public.error=not valid and tostring(err)or nil;public.count=n
 client.Send(pid,data,valid,rows,n);busy=false
end
local function safe()local ok,err=pcall(refresh);if not ok then busy=false;public.state='ERROR';public.error=tostring(err)end end
local function bind(name,fn)local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn}end end
ContextPtr:SetInitHandler(function()
 for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','SystemUpdateUI'})do bind(name,safe)end
 SPCSampleLifecycle.BindSampler(P,sampler,bind,false)
 bind('PlayerTurnActivated',safe) -- existing turn safety census; no new periodic fallback
 bind('LoadScreenClose',function()client.Reset();sampler.Reset();safe()end)
 ContextPtr:SetUpdate(function(dt)client.Tick(dt)end) -- existing scalar timeout only
 safe()
end)
ContextPtr:SetShutdown(function()
 client.Close();sampler.Reset();ContextPtr:ClearUpdate()
 for _,h in ipairs(hooks)do if h[1].Remove then h[1].Remove(h[2])end end
 if ExposedMembers.SPC_ResearchCrossBackground==public then ExposedMembers.SPC_ResearchCrossBackground=nil end
end)
