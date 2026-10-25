include('UnitSiteFacts')
-- Shared unit preview/dispatch; action owners return explicit transaction outcomes.
SPCUnitActions={}
function SPCUnitActions.Start(P,shared)
 local data={};shared.UnitActions=data
 local plans,busy={},{}
 local function unit(pid,id)
  assert(P.IsTestPlayer(pid),'TEST_PLAYER_REQUIRED')
  local u=Players[pid]:GetUnits():FindID(id);assert(u and u:GetOwner()==pid,'OWN_UNIT_REQUIRED')
  return u,P.Info('Units',u:GetType()).UnitType
 end
 local function target(pid,u)return SPCUnitSiteFacts.TargetCity(shared,pid,u)end
 local function fresh(pid,u)return shared.CrewProjects.UseTarget(pid,u)end
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
    local city,known
    if SPCUnitSiteFacts then
     local ok;ok,city,known=pcall(SPCUnitSiteFacts.DistrictCity,P,pid,u)
     if not ok then city=nil;known=false end
    end
    if not known then for _,d in Players[pid]:GetDistricts():Members()do P.Count('district_scan')
     local c=d:GetCity()
     if c and c:GetOwner()==pid and d:GetX()==u:GetX() and d:GetY()==u:GetY() then city=c;break end
    end
    end
    assert(city,'MOVE_TO_LEGAL_TARGET')
    local v=shared.InvestmentAction.ReadView(pid,city,id)
    for k,value in pairs(v) do view[k]=value end
    local p=plans[pid]
    view.prepared=view.prepared and p~=nil and p.unitID==id and p.cityID==city:GetID() and p.token==view.planToken
    return
   end
   assert(P.CrewBase(kind),'CREW_REQUIRED')
   local c,s=fresh(pid,u);local amount=shared.CrewProjects.Unit(pid,u).capacity
   view.legal=true;view.amount=amount;view.progress=s.progress;view.cost=s.cost
   view.baseInput=math.min(amount,s.cost-s.progress);view.baseUnused=amount-view.baseInput
   local row=P.Info(s.kind,s.target);view.targetName=row and row.Name or s.target
   local plan=plans[pid]
   view.prepared=plan~=nil and plan.unitID==id and plan.kind==kind and plan.cityID==c:GetID()
    and plan.turn==view.turn and plan.target==s.target and plan.cost==s.cost
    and plan.progress==s.progress and plan.amount==amount and plan.grant==shared.CrewProjects.Unit(pid,u).grant
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
  if busy[pid]then return 'BUSY: no second action',nil,{status='BUSY',kind='UNIT_ACTION'}end
  busy[pid]=true
  local outcome={status='REJECTED',kind='UNIT_ACTION',phase='PRECHECK'}
  local ok,result,investment=pcall(function()
   assert(P.IsTestPlayer(pid),'TEST_PLAYER_REQUIRED')
   if p.Action=='UNIT_ACTION_SPAWN' then
    error('CREW_PAID_FORMATION_REQUIRED')
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
     outcome={status=plans[pid]and 'PREPARED'or 'REJECTED',kind='INVESTMENT',phase='PREPARE'}
     return text
    end
    local c,s=fresh(pid,u);local amount=shared.CrewProjects.Unit(pid,u).capacity
    plans[pid]={kind=kind,cityID=c:GetID(),unitID=u:GetID(),token=p.Token,turn=Game.GetCurrentGameTurn(),target=s.target,cost=s.cost,progress=s.progress,amount=amount,grant=shared.CrewProjects.Unit(pid,u).grant}
    outcome={status='PREPARED',kind='CREW_USE',phase='PREPARE'}
    return 'CREW PREPARED | consume this Crew ('..amount..')\nProgress='..s.progress..' / '..s.cost..' | baseInput='..math.min(amount,s.cost-s.progress)..' | unusedBase='..math.max(0,amount-(s.cost-s.progress))..'\nConfirm unit action once. No production added yet.'
   end
   assert(p.Action=='UNIT_ACTION_CONFIRM','UNKNOWN_ACTION')
   local plan=plans[pid];plans[pid]=nil
   assert(plan and plan.unitID==u:GetID() and plan.kind==kind,'PREPARE_THIS_UNIT_FIRST')
   assert(p.PlanToken==nil or p.PlanToken==plan.token,'PREVIEW_TOKEN_CHANGED')
   local c=Players[pid]:GetCities():FindID(plan.cityID);assert(c and c:GetOwner()==pid,'OWNER_CHANGED')
   if kind=='UNIT_SETTLER' then
    local text,receipt=shared.InvestmentAction.Confirm(pid,c,plan.token)
    local status=receipt and receipt.status
    outcome={status=(status=='COMMITTED'or status=='ALREADY_COMMITTED')and 'COMMITTED'or status=='UNKNOWN'and 'HELD'or 'REJECTED',kind='INVESTMENT',phase='CONFIRM'}
    return text,receipt
   end
   outcome=shared.CrewProjects.Consume(pid,u,c,plan)
   if outcome.status=='COMMITTED'then
    return 'CREW CONSUMED | baseInput='..outcome.baseInput..' | unusedBase='..outcome.unusedBase..'\nVerify native target progress. Repeated confirm cannot grant again.'
   end
   return outcome.error or outcome.status

  end)
  busy[pid]=nil
  if not ok then plans[pid]=nil end
  local plan=plans[pid];shared.UnitActionPreview=nil
  if plan then
   local u=Players[pid]:GetUnits():FindID(plan.unitID)
   if u then shared.UnitActionPreview={owner=pid,unitID=plan.unitID,token=plan.token,turn=Game.GetCurrentGameTurn(),x=u:GetX(),y=u:GetY()} end
  end
  if not ok then outcome={status='REJECTED',kind=outcome.kind,phase='PRECHECK',error=tostring(result)}end
  local output=ok and result or ('REJECTED: '..tostring(result):match('[^\r\n]+'))
  if outcome.status=='REJECTED'or outcome.status=='HELD'then
   print('[SPC][B043][UNIT_ACTION_DETAIL] '..output)
   local hints={
    MOVE_TO_LEGAL_TARGET='请先移动到高亮的目标地块。施工队前往当前施工目标；移民前往本城专业区域。',
    MOVE_SETTLER_TO_IDENTITY_DISTRICT='请将移民移动到本城已确定专业的区域。',
    POTENTIAL_CAP_4='专业潜力已达到4级，不需要继续投资。',
    PREPARE_THIS_UNIT_FIRST='请先准备当前单位的操作。',
    PREVIEW_TOKEN_CHANGED='准备内容已变化，请重新准备。',
    TARGET_CHANGED_PREPARE_AGAIN='建设目标或进度已变化，请重新准备。',
    CREW_SOURCE_UNAVAILABLE='施工队缺少可靠来源绑定，请停止操作并回传日志。',
    CREW_WONDER_REQUIRED='施工队只能用于当前正在建造的奇观。',
    CREW_PAID_FORMATION_REQUIRED='请从工业城市生产列表付费组建施工队。',
    CREW_REQUIRES_EXACTLY_ONE_CHARGE='施工队劳动力不是1，已停止操作，请回传诊断。',
    MOVE_CIVILIAN_OFF_CITY_CENTER='请先将平民单位移出市中心。',
   }
   for code,hint in pairs(hints) do
    if output:find(code,1,true) and outcome.status=='REJECTED'then return 'REJECTED: '..hint..' ['..code..']',investment,outcome end
   end
   if outcome.status=='HELD'then return 'HELD: 操作结果尚未确认，请停止重试并回传日志。',investment,outcome end
   -- Preserve stable uppercase reason identifiers, not Lua paths/line numbers.
   local reason=output:match(':%d+:%s*([A-Z][A-Z0-9_]+)') or 'ACTION_REJECTED'
   return 'REJECTED: 当前操作不可执行。['..reason..'] 详细信息已写入日志。',investment,outcome
  end
  return output,investment,outcome
 end
 local removed=Events and Events.UnitRemovedFromMap
 if removed and removed.Add then removed.Add(function(pid,id)
  if plans[pid] and plans[pid].unitID==id then plans[pid]=nil end
 end) end
end
