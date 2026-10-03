include('CultureMeaningModel')
include('CurrentSpecializationFacts')
include('NetworkInput')
-- One explicitly chosen session fixture, no saved authority or benefit replay.
SPCCultureMeaningProbe={}
function SPCCultureMeaningProbe.Start(P,shared)
 local M=SPCCultureMeaningModel
 local d={ready=false,busy=false,mode='OFF',variant='SPLIT',changes=0};shared.CultureMeaningProbe=d
 local target,indices
 local owned={};for _,name in ipairs(M.Owned)do owned[name]=true end
 function d.IsOwnedCarrier(name)return owned[name]==true end
 local function validate()
  if indices then return end
  local nextIDs={}
  for _,name in ipairs(M.Owned)do
   local r=assert(P.Info('Buildings',name),'ME_DEFINITIONS_MISSING')
   assert((r.InternalOnly==1 or r.InternalOnly==true) and r.PrereqDistrict=='DISTRICT_CITY_CENTER' and r.CitizenSlots==0 and r.Housing==0,'ME_CARRIER_INVALID')
   nextIDs[name]=r.Index
  end
  indices=nextIDs
 end
 local function installed(c,name)
  local yes=P.HasBuilding(c:GetBuildings(),indices[name]);assert(type(yes)=='boolean','ME_CARRIER_UNKNOWN');return yes
 end
 local function project(c,want)
  validate()
  local failure
  for _,name in ipairs(M.Owned)do
   local ok,why=pcall(function()
    local present=installed(c,name);local damaged=false
    if present and want[name] then
     local value=c:GetBuildings():IsPillaged(indices[name]);assert(type(value)=='boolean','ME_CARRIER_HEALTH_UNKNOWN');damaged=value
    end
    if present and (not want[name] or damaged) then
     P.RemoveBuilding(c:GetBuildings(),indices[name]);assert(not installed(c,name),'ME_REMOVE_UNCONFIRMED');d.changes=d.changes+1
    end
   end)
   if not ok then failure=failure or why end
  end
  assert(not failure,failure) -- Attempt all exact withdrawals, never add after any failure.
  for _,name in ipairs(M.Owned)do if want[name] and not installed(c,name) then
   P.CreateBuilding(c:GetBuildQueue(),indices[name]);assert(installed(c,name),'ME_CREATE_UNCONFIRMED');d.changes=d.changes+1
  end end
 end
 local function current()
  assert(target,'ME_NO_FIXTURE')
  local c=assert(Players[target.owner]:GetCities():FindID(target.city),'ME_CITY_UNKNOWN')
  assert(c:GetOwner()==target.owner and P.IsTestPlayer(target.owner),'ME_OWNER_UNKNOWN')
  assert(SPCNetworkInput.Reference(c)==target.reference,'ME_REFERENCE_CHANGED');return c
 end
 local function plan(c)
  local f=SPCCurrentSpecializationFacts.Read(P,shared,target.owner,c)
  local w=shared.GreatWorkFacts.Summary(target.owner,target.city)
  if w then assert(w.reference==target.reference,'ME_WORK_REFERENCE_CHANGED')end
  local p=M.Plan(f,w,nil)
  if p.status=='NEEDS_DEPTH' then p=M.Plan(f,w,shared.DistrictCompleteness.Read(target.owner,c,f.token))end
  assert(SPCNetworkInput.Reference(c)==target.reference,'ME_REFERENCE_CHANGED');return p
 end
 local function dialogueHold(pid,c,percent)
  local ok,why=pcall(shared.Dialogue.HoldMeaningProbe,pid,c,percent)
  if not ok then d.error=tostring(why):sub(1,240);error(why)end
 end
 local function forget()
  if target then
   shared.Dialogue.ForgetMeaningProbe(target.owner,target.city,target.reference)
   shared.GreatWorkAdjacency.ForgetMeaningProbe(target.owner,target.city,target.reference)
  end
  target=nil;d.mode='OFF';d.lastPlan=nil;d.error=nil;d.stopping=nil
 end
 local function finish()
  d.stopping=true
  local ok,why=pcall(function()
   local c=current();project(c,{}) -- Old writer cannot resume until this confirms.
   if shared.Dialogue.meaningOverride then shared.Dialogue.ReleaseMeaningProbe(target.owner,c)end
   shared.GreatWorkAdjacency.ReleaseMeaningProbe(target.owner,c);forget()
  end)
  if not ok then d.error=tostring(why);error(why)end
 end
 local function reset(isLoad)
  -- One load-only pass over sixteen exact owned definitions. Not an AI ability audit.
  -- Saved transient test carriers must be removed even on a foreign held city.
  d.busy=true
  local ok,why=pcall(function()
   validate();local count=0
   for _,player in pairs(Players)do local collection=player:GetCities();if collection then
    for _,c in collection:Members()do P.Count('city_scan');count=count+1;assert(count<=2048,'ME_CLEANUP_SCOPE_LIMIT');project(c,{})end
   end end
   if isLoad then shared.Dialogue.ready=false;shared.Dialogue.Init() -- Cold-load cleanup of saved foreign test pieces.
   elseif target then shared.Dialogue.WithdrawMeaningProbe(target.owner,current())
   else shared.Dialogue.Init()end -- Never clear already-ready other cities on first probe fallback.
   forget();if isLoad then d.variant='SPLIT';d.lastAction=nil end;d.ready=true
  end)
  d.busy=false;d.error=not ok and tostring(why) or nil
  if not ok then d.ready=false;d.resetFailed=true else d.resetFailed=nil end
  return ok
 end
 local function audit(scope)
  if not d.ready or d.busy or not target then return end
  if scope and ((scope.player~=nil and scope.player~=target.owner) or (scope.city~=nil and scope.city~=target.city))then return end
  d.busy=true;local c
  local ok,why=pcall(function()
   local candidate=Players[target.owner]:GetCities():FindID(target.city)
   if candidate and candidate:GetOwner()==target.owner and SPCNetworkInput.Reference(candidate)~=target.reference then
    project(candidate,{});forget();error('ME_REFERENCE_CHANGED')
   end
   c=current();P.Count('city_scan');local p=plan(c);local want={}
   assert(shared.GreatWorkAdjacency.IsMeaningHeld(target.owner,c),'ME_OLD_WRITER_NOT_HELD')
   if not d.stopping and p.status=='READY' and p.count>0 then
    dialogueHold(target.owner,c,(d.mode=='SCALED' or d.mode=='SCALED_BASELINE') and 100 or 0)
   end
   if not d.stopping and (d.mode=='ACTIVE' or d.mode=='SCALED') and p.status=='READY' and p.count>0 then
    for _,y in ipairs({'SCIENCE','GOLD','CULTURE'})do for _,name in ipairs(M.Parts(y,p.each[y],y=='CULTURE' and d.variant or nil))do want[name]=true end end
   end
   project(c,want);d.lastPlan=p
  end)
  if not ok then
   local code=tostring(why)
   -- Unknown same-reference inputs retain the last confirmed projection. A
   -- known unsafe collection/configuration removes only these fourteen test IDs.
   if c and (code:find('ME_FIXTURE_UNSUPPORTED_WORK') or code:find('ME_CREATE_') or code:find('ME_ENCODING_') or code:find('ME_OLD_WRITER_'))then
    local cleared,err=pcall(project,c,{});if not cleared then why=err end
   end
  end
  d.error=not ok and tostring(why) or nil;d.busy=false
  return ok
 end
 function d.Audit(scope)
  if d.advancing then
   -- Coalesce only reentrant recalculation of this fixture. No event history.
   if target and (not scope or (scope.player==nil or scope.player==target.owner) and (scope.city==nil or scope.city==target.city))then d.deferred=true end
   return false,'TRANSITION_BUSY'
  end
  return audit(scope)
 end
 local function transition(mode,c)
  local previous=d.mode;d.mode=mode
  if not audit({player=c:GetOwner(),city=c:GetID()})then
   local why=d.error or 'ME_UPDATE_PENDING'
   if target then
    local percent=(previous=='SCALED' or previous=='SCALED_BASELINE') and 100 or 0
    local restored,err=pcall(shared.Dialogue.RestoreMeaningProbeIntent,c:GetOwner(),c,percent)
    if restored then d.mode=previous else why=why..'; '..tostring(err)end
   end -- An exact reference exit may already have forgotten this fixture.
   error(why)
  end
 end
 local function action(fn,...)
  assert(not d.advancing and not d.busy,'ME_TRANSITION_BUSY')
  d.advancing=true;local ok,why=pcall(fn,...);d.advancing=false
  local deferred=d.deferred;d.deferred=nil
  if not ok then d.error=tostring(why):sub(1,240);error(why)end
  -- Re-read current inputs after a successful transition. This is one bounded
  -- reconciliation, not a retry loop or a once-per-turn suppression.
  if deferred and target and not d.stopping then audit({player=target.owner,city=target.city})end
 end
 local function advance(pid,c)
  if not d.ready then assert(reset(),'ME_LOAD_CLEANUP_FAILED')end
  if target and (target.owner~=pid or target.city~=c:GetID() or target.reference~=SPCNetworkInput.Reference(c))then finish()end
  if not target then
   target={owner=pid,city=c:GetID(),reference=SPCNetworkInput.Reference(c),x=c:GetX(),y=c:GetY()}
   local ok,p=pcall(function()
    local value=plan(c)
    if value.status=='READY' and value.count>0 then M.Parts('CULTURE',value.each.CULTURE,d.variant)end
    return value
   end) -- Reject non-3 candidates before holding any old effect.
   if not ok or p.status~='READY' or p.count==0 then forget();error(not ok and p or 'ME_NEEDS_CULTURE_IV_AND_WORK')end
   -- Hold first, clear by old writer's exact owned path, never use off[player].
   d.mode='BASELINE'
   local held,why=pcall(shared.GreatWorkAdjacency.HoldMeaningProbe,pid,c)
   if not held then d.error=tostring(why);error(why)end
   project(c,{});dialogueHold(pid,c,0);d.lastPlan=p;d.error=nil
  elseif d.stopping or d.error then finish()
  elseif d.mode=='BASELINE' then
   -- Repeat the old module's confirmation before any new native write.
   shared.GreatWorkAdjacency.HoldMeaningProbe(pid,c)
   local p=plan(c);assert(p.status=='READY' and p.count>0,'ME_NEEDS_CULTURE_IV_AND_WORK')
   transition('ACTIVE',c)
  elseif d.mode=='ACTIVE' then
   local p=plan(c)
   if not (p.status=='READY' and p.count>0 and p.each.CULTURE>0)then d.error='ME_NEEDS_POSITIVE_CULTURE';return end
   transition('SCALED',c)
  elseif d.mode=='SCALED' then
   transition('SCALED_BASELINE',c)
  else finish()end
 end
 function d.Advance(pid,c,token)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'ME_OWNER_UNKNOWN')
  if token then
   assert(type(token)=='string' and #token>0 and #token<=100,'ME_ACTION_TOKEN')
   local old=d.lastAction
   if old and old.token==token then
    assert(old.owner==pid and old.city==c:GetID() and old.kind=='ADVANCE','ME_ACTION_TOKEN_CONFLICT');return
   end
  end
  return action(function()
   if token then d.lastAction={token=token,owner=pid,city=c:GetID(),kind='ADVANCE'}end -- One bounded receipt.
   advance(pid,c)
  end)
 end
 function d.CycleVariant(pid,c,token)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'ME_OWNER_UNKNOWN')
  if token then
   assert(type(token)=='string' and #token>0 and #token<=100,'ME_ACTION_TOKEN')
   local old=d.lastAction
   if old and old.token==token then
    assert(old.owner==pid and old.city==c:GetID() and old.kind=='CONFIG','ME_ACTION_TOKEN_CONFLICT');return
   end
  end
  return action(function()
   assert(not target and d.mode=='OFF','ME_VARIANT_REQUIRES_OFF')
   local found
   for i,name in ipairs(M.Variants)do if name==d.variant then found=i;break end end
   assert(found,'ME_ENCODING_VARIANT_UNKNOWN')
   d.variant=M.Variants[found%#M.Variants+1]
   if token then d.lastAction={token=token,owner=pid,city=c:GetID(),kind='CONFIG'}end
   d.error=nil
  end)
 end
 function d.View(pid,c)
  local ref=SPCNetworkInput.Reference(c)
  local match=target and target.owner==pid and target.city==c:GetID() and target.reference==ref
  local p=match and d.lastPlan or nil
  local configured={SCIENCE=0,GOLD=0,CULTURE=0}
  local stamp={};if p then for _,entry in ipairs(M.Domains)do local v=p.domains[entry[1]];stamp[#stamp+1]=entry[1]..':'..tostring(v and v.value)end end
  local dialoguePercent,dialogueError
  if match then dialoguePercent,dialogueError=shared.Dialogue.ReadMeaningProbe(pid,c)end
  local q=match and shared.Dialogue.meaningQualification
  if q and (q.owner~=pid or q.city~=c:GetID() or q.reference~=ref)then q=nil end
  local read,why=pcall(function()
   validate();for _,y in ipairs({'SCIENCE','GOLD','CULTURE'})do for bit=0,M.ProbeBits[y]-1 do
    local name='BUILDING_SPC_MEANING_PROBE_'..y..'_'..bit
    if installed(c,name) then
     assert(y~='CULTURE' or d.variant=='SPLIT','ME_CONFIG_VARIANT_MISMATCH')
     local damaged=c:GetBuildings():IsPillaged(indices[name]);assert(type(damaged)=='boolean','ME_CARRIER_HEALTH_UNKNOWN')
     if not damaged then configured[y]=configured[y]+2^bit/M.ProbeScale[y] end
    end
   end end
   local pieces=0
   for _,part in pairs(M.VariantParts)do if installed(c,part.name)then
    pieces=pieces+1
    assert(configured.CULTURE==0 and pieces==1,'ME_CONFIG_VARIANT_OVERLAP')
    assert(M.VariantParts[d.variant] and M.VariantParts[d.variant].name==part.name,'ME_CONFIG_VARIANT_MISMATCH')
    local damaged=c:GetBuildings():IsPillaged(indices[part.name]);assert(type(damaged)=='boolean','ME_CARRIER_HEALTH_UNKNOWN')
    if not damaged then configured.CULTURE=part.amount end
   end end
  end)
  return {variant=d.variant,configuredScience=read and configured.SCIENCE or nil,configuredGold=read and configured.GOLD or nil,configuredCulture=read and configured.CULTURE or nil,configurationError=not read and tostring(why) or nil,
   owner=pid,cityID=c:GetID(),reference=ref,mode=match and d.mode or 'OFF',error=d.error,
   currentIdentity=q and q.specialization,currentPotential=q and q.potential,currentActive=q and q.active,currentActiveStatus=q and q.activeStatus,
   active=p and p.active,count=p and p.count,science=p and p.each.SCIENCE,gold=p and p.each.GOLD,culture=p and p.each.CULTURE,
   totalScience=p and p.total.SCIENCE,totalGold=p and p.total.GOLD,totalCulture=p and p.total.CULTURE,planStatus=p and p.status,
   campus=p and p.domains.DISTRICT_CAMPUS and p.domains.DISTRICT_CAMPUS.value,
   commerce=p and p.domains.DISTRICT_COMMERCIAL_HUB and p.domains.DISTRICT_COMMERCIAL_HUB.value,
   harbor=p and p.domains.DISTRICT_HARBOR and p.domains.DISTRICT_HARBOR.value,
   oldHeld=match and shared.GreatWorkAdjacency.IsMeaningHeld(pid,c) or false,
   dialoguePercent=dialoguePercent,dialogueError=dialogueError,stamp=table.concat(stamp,';')}
 end
 function d.End(pid,c,token)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'ME_OWNER_UNKNOWN')
  if token then
   assert(type(token)=='string' and #token>0 and #token<=100,'ME_ACTION_TOKEN')
   local old=d.lastAction
   if old and old.token==token then
    assert(old.owner==pid and old.city==c:GetID() and old.kind=='END','ME_ACTION_TOKEN_CONFLICT');return
   end
  end
  return action(function()
   if not target and d.mode=='OFF' and token then
    d.lastAction={token=token,owner=pid,city=c:GetID(),kind='END'};return
   end
   assert(target and target.owner==pid and target.city==c:GetID(),'ME_NO_FIXTURE')
   if token then d.lastAction={token=token,owner=pid,city=c:GetID(),kind='END'}end
   finish()
  end)
 end
 function d.Describe(pid,c,view)
  local v=view or d.View(pid,c)
  local names={OFF='未开启',BASELINE='①基线：追加0／旧对话0%',ACTIVE='②追加：整数收益／旧对话0%',SCALED='③组合：整数收益／旧对话100%',SCALED_BASELINE='④倍率基线：追加0／旧对话100%'}
  local variants={SPLIT='拆分片段',SINGLE3='单一+3',SINGLE3_SCALE100='单一+3／倍率100%候选'}
  local lines={'意义延展验证｜'..names[v.mode], '当前配置：'..(variants[v.variant] or '未确认')..'（候选≠修复）'}
  if v.count then
   lines[#lines+1]=string.format('合格%d件｜每件理论 +%g科研 / +%g金币 / +%g文化',v.count,v.science,v.gold,v.culture)
   lines[#lines+1]=string.format('逐领域Floor后相加；理论文化合计 +%g。',v.totalCulture)
  end
  if v.mode~='OFF' then
   lines[#lines+1]=v.configuredScience and string.format('每件配置 +%g科研 / +%g金币 / +%g文化｜旧对话 %s%%（配置≠实测）',v.configuredScience,v.configuredGold,v.configuredCulture,tostring(v.dialoguePercent or '未确认')) or '载体配置未确认。'
  end
  local nexts={OFF='左键准备基线；需要Culture ACTIVE4和确认馆藏。',BASELINE='左键启用追加；右键只读。',ACTIVE='左键加入本城100%旧对话；需文化追加>0。',SCALED='左键撤回追加，保留本城100%旧对话。',SCALED_BASELINE='左键结束，按当前事实恢复旧系统。'}
  lines[#lines+1]=nexts[v.mode]
  if v.currentActiveStatus then lines[#lines+1]=v.currentActiveStatus=='KNOWN' and ('当前资格：'..tostring(v.currentIdentity)..' ACTIVE '..tostring(v.currentActive)..'（需要文化4级）') or '当前资格：未确认，不将未知记为0。'end
  if v.dialogueError then
   local code=tostring(v.dialogueError):match('ME_[A-Z_]+') or '接口未确认'
   lines[#lines+1]='对话配置未确认：'..code
  end
  if v.error then lines[#lines+1]='异常：'..(v.error:match('ME_[A-Z_]+') or '接口未确认')..'；左键先结束。'end
  if v.mode~='OFF' then lines[#lines+1]='仅本城可逆原型；配置按钮右键可直接结束。追加预期不受对话／主题化放大，原生门禁未通过。'end
  return table.concat(lines,'\n')
 end
 local store=shared.CityProgressionStore
 if store then store.RegisterExit('CultureMeaningProbe',function(c,loss)
  assert(store.IsExitTarget(c,loss),'ME_EXIT_UNCONFIRMED')
  store.RemoveOwned(c,loss,M.Owned)
  if target and target.owner==loss.origin.owner and target.x==c:GetX() and target.y==c:GetY() then forget()end
 end)end
 local function bind(source,name,fn)local e=P.Field(source,name);if e and e.Add then e.Add(fn)end end
 bind(Events,'LoadScreenClose',function()reset(true)end)
 local lastTurn
 bind(Events,'PlayerTurnActivated',function(pid)
  if not P.IsTestPlayer(pid)then return end
  if not d.ready and not d.resetFailed then reset()end
  local turn=Game.GetCurrentGameTurn();if lastTurn~=turn then lastTurn=turn;d.Audit({player=pid})end
 end)
 bind(Events,'CityBuildingsChanged',function(pid,cid)d.Audit({player=pid,city=cid})end)
 for _,name in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap'})do bind(Events,name,function(x,y,id,owner)
  if not target or d.busy then return end
  local row=P.Info('Buildings',id);local typ=row and row.BuildingType
  if typ and (indices and indices[typ] or shared.GreatWorkAdjacency.IsOwnedCarrier(typ) or shared.Dialogue.IsOwnedCarrier(typ))then return end
  if type(owner)=='number' and owner>=0 and owner%1==0 and owner~=target.owner then return end
  local ok,c=pcall(function()local district=CityManager.GetDistrictAt and CityManager.GetDistrictAt(x,y);return district and district:GetCity() or CityManager.GetCityAt(x,y)end)
  d.Audit({player=owner,city=ok and c and c:GetID() or nil})
 end)end
 -- Native signatures vary; fallback is still only the current one-city fixture.
 for _,name in ipairs({'BuildingPillaged','BuildingRepaired','DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted'})do
  bind(Events,name,function()d.Audit()end)
 end
 for _,name in ipairs({'BuildingConstructed','OnDistrictConstructed','OnPillage'})do bind(GameEvents,name,function()d.Audit()end)end
 -- Called only after both Receive functions accepted this exact request.
 -- The Facts callback remains owned by the existing independent consumers.
 function d.CollectionConfirmed(pid,packet)
  if not target or pid~=target.owner then return false end
  local c=current();local paired,why=shared.Dialogue.IsMeaningSampleCurrent(pid,c,packet)
  if not paired then return false,why end
  d.Audit({player=pid,city=target.city}) -- Also refresh unchanged collections on a new turn.
  return not d.busy and not d.error
 end
end
