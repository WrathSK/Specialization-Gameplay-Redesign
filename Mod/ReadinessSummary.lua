-- B267 read-only initialization observations. A ready flag is not effect PASS.
SPCReadinessSummary={}
function SPCReadinessSummary.Start(P,shared)
 if not SPCExpeditionTrainingDiagnostics.ENABLED then return {Seal=function()end}end
 local trace=SPCExpeditionTrainingDiagnostics.New(P,'READINESS')
 local d={sealed=false,loadSeen=false,loadBeforeSeal=false};shared.ReadinessSummary=d
 local first=false;local afterLoad=false;local localPending=false;local localSeen=false
 local live={{'FR','CityProgressionStore'},{'NB','NetworkBridge'},{'RS','ResearchSupport'},
  {'H2','Lv2Housing'},{'G2','Lv2GPP'},{'RI','ResearchInfrastructure'},{'RX','ResearchCross'},
  {'RA','ResearchApply'},{'RC','ResearchChair'},{'RT','ResearchTraditionEffects'}}
 local controls={{'REST','Restructuring'},{'CN','CultureNetwork'},{'CA','CultureAesthetic'},
  {'S3_CLEANUP','Lv3Support'},{'E3_CLEANUP','Lv3Effects'}}
 local function value(pair)
  local ok,v=pcall(function()
   local module=shared[pair[2]];if not module then return 'MISSING'end
   if pair[1]=='FR'then return module.FreshReady()end
   return module.ready
  end)
  if not ok then return 'READ_ERROR'end
  return v==true and 'READY' or v==false and 'PENDING' or type(v)=='string' and v or 'UNKNOWN'
 end
 local function sample(reason)
  local states,missing,control={},{},{}
  for _,pair in ipairs(live)do local v=value(pair);states[#states+1]=pair[1]..':'..v;if v~='READY'then missing[#missing+1]=pair[1]end end
  for _,pair in ipairs(controls)do control[#control+1]=pair[1]..':'..value(pair)end
  trace.Record('READINESS_SUMMARY',{reason=reason,sealed=d.sealed,loadSeen=d.loadSeen,
   loadBeforeSeal=d.loadBeforeSeal,notReady=#missing==0 and 'NONE' or table.concat(missing,'|'),
   writerState=table.concat(states,'|'),controlState=table.concat(control,'|')})
 end
 local function safe(fn)return function(...)local ok=pcall(fn,...);if not ok then pcall(trace.Record,'READINESS_OBSERVER_FAILURE',{reason='READINESS_READ_ERROR'})end end end
 local function hook(source,name,fn)local e=P.Field(source,name);if e and e.Add then e.Add(safe(fn))end end
 hook(Events,'LoadScreenClose',function()
  d.loadSeen=true;d.loadBeforeSeal=d.loadBeforeSeal or not d.sealed;afterLoad=true
  trace.Record('READINESS_LOAD_RECEIVED',{sealed=d.sealed,loadBeforeSeal=d.loadBeforeSeal})
 end)
 hook(Events,'PlayerTurnActivated',function(pid)
  if not localSeen and pid==Game.GetLocalPlayer() and P.IsTestPlayer(pid)then localSeen=true;localPending=true end
 end)
 hook(Events,'GameCoreEventPublishComplete',function()
  if not d.sealed then return end
  if not first then first=true;sample('FIRST_PUBLISH')end
  if afterLoad then afterLoad=false;sample('AFTER_LOAD')end
  if localPending then localPending=false;sample('FIRST_LOCAL_TURN')end
 end)
 function d.Seal()d.sealed=true;pcall(trace.Record,'READINESS_SEALED',{sealed=true,loadSeen=d.loadSeen,loadBeforeSeal=d.loadBeforeSeal})end
 return d
end
