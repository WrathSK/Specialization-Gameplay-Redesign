-- B044: native project crews, explicit legacy DEV spawn, single-use capped injection.
SPCUnitActions={}
function SPCUnitActions.Start(P,shared)
 local data={};shared.UnitActions=data
 local plans,busy={},{}
 local KEY='SPC_CREW_ACTION_RECEIPTS_V1'
 local function unit(pid,id)
  assert(P.IsTestPlayer(pid),'TEST_PLAYER_REQUIRED')
  local u=Players[pid]:GetUnits():FindID(id);assert(u and u:GetOwner()==pid,'OWN_UNIT_REQUIRED')
  return u,P.Info('Units',u:GetType()).UnitType
 end
 local function target(pid,u)
  shared.UnitTargets.Refresh(pid,{UnitID=u:GetID(),Token='ACTION_SITE',BuilderPreview=false})
  local s=shared.UnitTargetSnapshot;assert(not s.error,s.error)
  local plot=Map.GetPlot(u:GetX(),u:GetY()):GetIndex()
  for _,v in ipairs(s.plots) do
   if v.plot==plot then return Players[pid]:GetCities():FindID(v.cityID) end
  end
  error('MOVE_TO_LEGAL_TARGET: select unit to see map markers')
 end
 local function fresh(pid,u)
  assert(u:GetBuildCharges()==1,'CREW_REQUIRES_EXACTLY_ONE_CHARGE')
  assert(u:GetProperty('SPC_CREW_RESERVED')==nil,'CREW_RESERVED')
  local c=target(pid,u);local s=shared.ConstructionProbe.ReadSnapshot(pid,c)
  assert((s.kind=='Buildings' or s.kind=='Districts') and s.progress<s.cost,'LEGAL_CONSTRUCTION_REQUIRED')
  return c,s
 end
 -- B045 presentation-only refresh. Reuse exact existing eligibility/queue checks.
 -- Invalidating an ephemeral preview never consumes, grants or changes city facts.
 function data.ReadView(pid,id,token)
  local view={owner=pid,unitID=id,token=token,legal=false,prepared=false,turn=Game.GetCurrentGameTurn()}
  local previousTargets=shared.UnitTargetSnapshot
  local ok,err=pcall(function()
   local u,kind=unit(pid,id)
   view.x=u:GetX();view.y=u:GetY()
   if kind=='UNIT_SETTLER' then
    -- Locate the district before checking the cap, to give a specific cap tooltip.
    local city
    for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
     local c=d:GetCity()
     if c and c:GetOwner()==pid and d:GetX()==u:GetX() and d:GetY()==u:GetY() then city=c;break end
    end
    assert(city,'MOVE_TO_LEGAL_TARGET')
    local v=shared.InvestmentAction.ReadView(pid,city,id)
    for k,value in pairs(v) do view[k]=value end
    local p=plans[pid]
    view.prepared=view.prepared and p~=nil and p.unitID==id and p.cityID==city:GetID() and p.token==view.planToken
    return
   end
   assert(P.CrewBase(kind),'CREW_REQUIRED')
   local c,s=fresh(pid,u);local amount=P.CrewAmount(kind)
   view.legal=true;view.amount=amount;view.progress=s.progress;view.cost=s.cost
   view.after=math.min(s.cost,s.progress+amount);view.waste=math.max(0,amount-(s.cost-s.progress))
   local row=P.Info(s.kind,s.target);view.targetName=row and row.Name or s.target
   local plan=plans[pid]
   view.prepared=plan~=nil and plan.unitID==id and plan.kind==kind and plan.cityID==c:GetID()
    and plan.turn==view.turn and plan.target==s.target and plan.cost==s.cost
    and plan.progress==s.progress and plan.amount==amount
   if view.prepared then view.planToken=plan.token end
  end)
  shared.UnitTargetSnapshot=previousTargets -- Do not overwrite the marker reader's reply.
  if not ok then view.legal=false;view.prepared=false;view.reason=tostring(err) end
  local plan=plans[pid]
  if plan and plan.unitID==id and not view.prepared then
   plans[pid]=nil
   if shared.InvestmentAction and shared.InvestmentAction.CancelPreview then shared.InvestmentAction.CancelPreview(pid,id) end
   if shared.UnitActionPreview and shared.UnitActionPreview.unitID==id then shared.UnitActionPreview=nil end
  end
  shared.UnitActionView=view
  return view
 end
 function data.Run(pid,p)
  if busy[pid] then return 'BUSY: no second action' end
  busy[pid]=true
  local destructive=false
  local ok,result,investment=pcall(function()
   assert(P.IsTestPlayer(pid),'TEST_PLAYER_REQUIRED')
   if p.Action=='UNIT_ACTION_SPAWN' then
    local c=Players[pid]:GetCities():FindID(p.CityID);assert(c and c:GetOwner()==pid,'SELECT_OWN_CITY')
    local row=P.Info('Units','UNIT_SPC_CREW_250');assert(row,'CREW_DEFINITION_MISSING_RELOAD_OR_NEW_GAME')
    for _,v in Players[pid]:GetUnits():Members() do
     local vr=P.Info('Units',v:GetType())
     assert(v:GetX()~=c:GetX() or v:GetY()~=c:GetY() or vr.FormationClass~='FORMATION_CLASS_CIVILIAN','MOVE_CIVILIAN_OFF_CITY_CENTER')
    end
    local seen=Players[pid]:GetProperty('SPC_CREW_DEV_SPAWN') or {}
    assert(not seen[p.Token],'SPAWN_REQUEST_ALREADY_USED');seen[p.Token]=true
    P.SetProperty(Players[pid],'SPC_CREW_DEV_SPAWN',seen)
    destructive=true;UnitManager.InitUnit(pid,'UNIT_SPC_CREW_250',c:GetX(),c:GetY())
    return 'DEV spawn requested: Crew 250. Select unit; verify appearance and 1 charge. No project paid.'
   end
   local u,kind=unit(pid,p.UnitID)
   assert(kind=='UNIT_SETTLER' or P.CrewBase(kind)~=nil,'SETTLER_OR_CREW_REQUIRED')
   if p.Action=='UNIT_ACTION_PREPARE' then
    plans[pid]=nil
    if kind=='UNIT_SETTLER' then
     local c=target(pid,u)
     local text=shared.InvestmentAction.Prepare(pid,c,u:GetID(),p.Token,true)
     local preview=shared.InvestmentPreview
     if preview and preview.owner==pid and preview.unitID==u:GetID() then plans[pid]={kind=kind,cityID=c:GetID(),unitID=u:GetID(),token=preview.token} end
     return text
    end
    local c,s=fresh(pid,u);local amount=P.CrewAmount(kind)
    plans[pid]={kind=kind,cityID=c:GetID(),unitID=u:GetID(),token=p.Token,turn=Game.GetCurrentGameTurn(),target=s.target,cost=s.cost,progress=s.progress,amount=amount}
    return 'CREW PREPARED | consume this Crew ('..amount..')\nProgress='..s.progress..' / '..s.cost..' | apply='..math.min(amount,s.cost-s.progress)..' | waste='..math.max(0,amount-(s.cost-s.progress))..'\nConfirm unit action once. No production added yet.'
   end
   assert(p.Action=='UNIT_ACTION_CONFIRM','UNKNOWN_ACTION')
   local plan=plans[pid];plans[pid]=nil
   assert(plan and plan.unitID==u:GetID() and plan.kind==kind,'PREPARE_THIS_UNIT_FIRST')
   assert(p.PlanToken==nil or p.PlanToken==plan.token,'PREVIEW_TOKEN_CHANGED')
   local c=Players[pid]:GetCities():FindID(plan.cityID);assert(c and c:GetOwner()==pid,'OWNER_CHANGED')
   if kind=='UNIT_SETTLER' then
    return shared.InvestmentAction.Confirm(pid,c,plan.token)
   end
   local amount=P.CrewAmount(kind);assert(amount==plan.amount,'TARGET_CHANGED_PREPARE_AGAIN')
   local now,s=fresh(pid,u)
   assert(now:GetID()==c:GetID() and plan.turn==Game.GetCurrentGameTurn() and s.target==plan.target and s.cost==plan.cost and s.progress==plan.progress,'TARGET_CHANGED_PREPARE_AGAIN')
   local receipts=Players[pid]:GetProperty(KEY) or {};assert(not receipts[plan.token],'RECEIPT_EXISTS')
   local function record(state)
    receipts[plan.token]={state=state,unitID=plan.unitID,cityID=c:GetID(),target=s.target,amount=math.min(amount,s.cost-s.progress)}
    P.SetProperty(Players[pid],KEY,receipts)
   end
   destructive=true;record('INTENT');P.SetProperty(u,'SPC_CREW_RESERVED',plan.token)
   assert(u:GetProperty('SPC_CREW_RESERVED')==plan.token,'RESERVATION_UNCONFIRMED')
   Players[pid]:GetUnits():Destroy(u)
   assert(not Players[pid]:GetUnits():FindID(plan.unitID),'UNIT_DEBIT_UNCONFIRMED')
   local after=shared.ConstructionProbe.ReadSnapshot(pid,c)
   assert(after.target==s.target and after.progress==s.progress and after.cost==s.cost,'TARGET_CHANGED_AFTER_DEBIT')
   record('GRANT_ATTEMPTED') -- Never automatically replay an uncertain engine grant.
   c:GetBuildQueue():AddProgress(math.min(amount,s.cost-s.progress))
   record('COMPLETED')
   return 'CREW CONSUMED | added='..math.min(amount,s.cost-s.progress)..' | wasted='..math.max(0,amount-(s.cost-s.progress))..'\nVerify native target progress. Repeated confirm cannot grant again.'
  end)
  busy[pid]=nil
  if not ok then plans[pid]=nil end
  local plan=plans[pid];shared.UnitActionPreview=nil
  if plan then
   local u=Players[pid]:GetUnits():FindID(plan.unitID)
   if u then shared.UnitActionPreview={owner=pid,unitID=plan.unitID,token=plan.token,turn=Game.GetCurrentGameTurn(),x=u:GetX(),y=u:GetY()} end
  end
  local output=ok and result or ((destructive and 'HELD / RESULT UNCERTAIN (do not retry): ' or 'REJECTED: ')..tostring(result):match('[^\r\n]+'))
  if not ok or output:find('REJECTED',1,true) or output:find('HELD',1,true) then
   print('[SPC][B043][UNIT_ACTION_DETAIL] '..output)
   local hints={
    MOVE_TO_LEGAL_TARGET='请先移动到高亮的目标地块。施工队前往当前施工目标；移民前往本城专业区域。',
    MOVE_SETTLER_TO_IDENTITY_DISTRICT='请将移民移动到本城已确定专业的区域。',
    POTENTIAL_CAP_4='专业潜力已达到4级，不需要继续投资。',
    PREPARE_THIS_UNIT_FIRST='请先准备当前单位的操作。',
    PREVIEW_TOKEN_CHANGED='准备内容已变化，请重新准备。',
    TARGET_CHANGED_PREPARE_AGAIN='建设目标或进度已变化，请重新准备。',
    CREW_REQUIRES_EXACTLY_ONE_CHARGE='施工队劳动力不是1，已停止操作，请回传诊断。',
    MOVE_CIVILIAN_OFF_CITY_CENTER='请先将平民单位移出市中心。',
   }
   for code,hint in pairs(hints) do
    if output:find(code,1,true) and not destructive then return 'REJECTED: '..hint..' ['..code..']',investment end
   end
   if destructive or output:find('HELD',1,true) then return 'HELD: 操作结果尚未确认，请停止重试并回传日志。',investment end
   -- Preserve stable uppercase reason identifiers, not Lua paths/line numbers.
   local reason=output:match(':%d+:%s*([A-Z][A-Z0-9_]+)') or 'ACTION_REJECTED'
   return 'REJECTED: 当前操作不可执行。['..reason..'] 详细信息已写入日志。',investment
  end
  return output,investment
 end
 local removed=Events and Events.UnitRemovedFromMap
 if removed and removed.Add then removed.Add(function(pid,id)
  if plans[pid] and plans[pid].unitID==id then plans[pid]=nil end
 end) end
end
