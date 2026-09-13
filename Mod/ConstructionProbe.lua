-- B039 explicit DEV grant, not a Crew/project or unit-consumption implementation.
SPCConstructionProbe={}
function SPCConstructionProbe.Start(P,shared)
 local data={};shared.ConstructionProbe=data
 local plans={};local busy={}
 local function key(pid,c) return pid..':'..c:GetID() end
 local function snapshot(pid,c)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'OWN_TEST_CITY_REQUIRED')
  local q=c:GetBuildQueue();local current=q:CurrentlyBuilding()
  assert(current~=nil and current~='','EMPTY_QUEUE')
  local row,kind,code
  for i,t in ipairs({'Buildings','Districts','Units','Projects'}) do
   local r=P.Info(t,current)
   if r then assert(not row,'AMBIGUOUS_TARGET');row=r;kind=t;code=i-1 end
  end
  assert(row and type(row.Index)=='number','TARGET_UNKNOWN')
  local utils=ExposedMembers.DLHD and ExposedMembers.DLHD.Utils
  assert(utils and type(utils.GetCityCurrentBuildQueueCost)=='function' and type(utils.GetCityCurrentBuildQueueProgress)=='function','HD_QUEUE_READ_HELPERS_UNAVAILABLE')
  -- These HD helpers read UI-context queue data; validate ownership/type before and after.
  local cost=utils.GetCityCurrentBuildQueueCost(pid,c:GetID(),code,row.Index)
  local progress=utils.GetCityCurrentBuildQueueProgress(pid,c:GetID(),code,row.Index)
  assert(type(cost)=='number' and cost>0 and cost<math.huge and type(progress)=='number' and progress>=0 and progress<math.huge,'QUEUE_NUMBERS_INVALID')
  assert(c:GetOwner()==pid and q:CurrentlyBuilding()==current,'TARGET_CHANGED_DURING_READ')
  return {target=current,kind=kind,label=(kind=='Buildings' and row.IsWonder and 'Wonder' or kind),cost=cost,progress=progress}
 end
 data.ReadSnapshot=snapshot
 local function short(err) return tostring(err):match('[^\r\n]+') or 'UNKNOWN' end
 function data.Prepare(pid,c)
  local k=key(pid,c);plans[k]=nil
  if busy[k] then return 'B039 BUSY' end
  local ok,out=pcall(function()
   local s=snapshot(pid,c);assert(s.kind=='Buildings' or s.kind=='Districts','ONLY_BUILDING_DISTRICT_WONDER')
   assert(s.progress<s.cost,'TARGET_ALREADY_COMPLETE')
   s.turn=Game.GetCurrentGameTurn();s.amount=math.min(250,s.cost-s.progress);plans[k]=s
   return 'B039 DEV PREVIEW | city='..c:GetID()..' '..s.label..' '..tostring(s.target)
    ..'\nProgress '..s.progress..' / '..s.cost..' | remaining='..(s.cost-s.progress)
    ..'\nDEV grant=250 | apply='..s.amount..' | discard='..(250-s.amount)
    ..'\nNo production added yet. Inject 250 (DEV) confirms once.'
    ..'\nTEST ONLY: no Crew required/consumed; no project implemented.'
  end)
  return ok and out or ('B039 REJECTED: '..short(out))
 end
 function data.Apply(pid,c)
  local k=key(pid,c);if busy[k] then return 'B039 BUSY' end
  local plan=plans[k];plans[k]=nil
  if not plan then return 'B039 REJECTED: Preview construction first; no production added.' end
  busy[k]=true;local attempted=false
  local ok,out=pcall(function()
   local now=snapshot(pid,c)
   assert(plan.turn==Game.GetCurrentGameTurn() and now.target==plan.target and now.kind==plan.kind and now.cost==plan.cost and now.progress==plan.progress,'PREVIEW_CHANGED_PREVIEW_AGAIN')
   -- One invocation only. Do not pass surplus to the engine, recurse or retry on uncertainty.
   attempted=true;c:GetBuildQueue():AddProgress(plan.amount)
   local got,after=pcall(snapshot,pid,c)
   local observed=got and ('Now '..tostring(after.target)..' progress='..after.progress..' / '..after.cost) or ('After queue: '..short(after))
   return 'B039 DEV REQUEST SENT | city='..c:GetID()..' '..tostring(plan.target)
    ..'\nBefore='..plan.progress..' / '..plan.cost..' | requested='..plan.amount..' | discarded='..(250-plan.amount)
    ..'\n'..observed
    ..'\nVerify native completion/next queue. This message alone is not PASS.'
    ..'\nPreview consumed; repeated Inject will not add production.'
  end)
  busy[k]=false
  return ok and out or ('B039 '..(attempted and 'RESULT_UNCERTAIN (do not retry blindly): ' or 'REJECTED: ')..short(out))
 end
end
