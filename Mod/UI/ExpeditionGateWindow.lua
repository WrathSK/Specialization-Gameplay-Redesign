include('Probe')
include('ExpeditionGateRead')
local P=SPCP0;local R=SPCExpeditionGateRead
local pending;local pendingAction;local current;local travel;local targets={};local selected=1;local initialCapacity
local errorKeys={OWN_CITY_REQUIRED='OWN_CITY',CULTURE_ACTIVE_IV_REQUIRED='CULTURE_IV',CITY_CENTER_OCCUPIED='OCCUPIED',
 EXISTING_TEST_TEAM_COUNTS='CAP',SPAWN_UNCERTAIN_NO_RETRY='HELD',SPAWN_UNCONFIRMED='HELD',
 SPAWN_COUNT_UNCONFIRMED='HELD',TEST_TEAM_CHANGED='TEAM_CHANGED',END_UNCONFIRMED='END_FAILED',TEST_DATABASE_NOT_READY='DB'}
local function L(key,...)return Locale.Lookup('LOC_SPC_EXPEDITION_GATE_'..key,...)end
local function setReport(s)
 Controls.Report:SetText(s);Controls.ReportScroll:CalculateSize();Controls.ReportScroll:ReprocessAnchoring()
end
local function render()
 local out={};local v=current;local pid=Game.GetLocalPlayer()
 if not v then setReport(L('INITIAL'));return end
 if v.error then
  out[#out+1]=L(errorKeys[v.error] or 'ERROR',v.error)
 else
  out[#out+1]=L('COUNT',v.count or 0)
  if v.unitID then out[#out+1]=L('UNIT',v.unitID,v.x,v.y)end
  if v.phase=='ENDED' then out[#out+1]=L('ENDED')end
  if v.phase=='HELD' then out[#out+1]=L('HELD')end
  if v.createdID and not v.sameUnit and v.phase~='ENDED' then out[#out+1]=L('MISSING')end
  if v.watchID then
   if v.watchedAlive then
    out[#out+1]=L('WATCH',v.watchID,v.watchX,v.watchY,v.watchedX,v.watchedY)
    out[#out+1]=L('WATCH_NOTE')
   else out[#out+1]=L('MISSING')end
  end
 end
 local now=R.Capacity(pid)
 out[#out+1]=L('CAPACITY',initialCapacity or '?',now or '?')
 if travel then
  if travel.status=='READ_OK' then
   out[#out+1]=L('TIMING',Locale.Lookup(travel.targetName),travel.travel,travel.establish,travel.total)
   out[#out+1]=L('TIMING_SCOPE',travel.turn)
  else out[#out+1]=L('TIMING_UNKNOWN',travel.error or 'UNKNOWN')end
 end
 out[#out+1]=L('STOP_HINT');setReport(table.concat(out,'[NEWLINE][NEWLINE]'))
end
local function reply()
 if not pending then return end
 local v=ExposedMembers.SPC_ExpeditionGateReply
 if v and v.owner==Game.GetLocalPlayer() and v.token==pending then
  current=v;if pendingAction=='END' and not v.error then travel=nil end;pending=nil;pendingAction=nil;ContextPtr:ClearUpdate();render();return true
 end
end
local function request(action)
 if pending then setReport(L('WAIT'));return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid)then return end
 local c=UI.GetHeadSelectedCity()
 local id=current and current.unitID
 if (action=='ARM' or action=='END') and not id then setReport(L('TEAM_CHANGED'));return end
 if action=='CREATE' and (not c or c:GetOwner()~=pid)then setReport(L('OWN_CITY'));return end
 if action=='CREATE' then initialCapacity=R.Capacity(pid);travel=nil end
 ExposedMembers.SPC_ExpeditionGateSequence=(ExposedMembers.SPC_ExpeditionGateSequence or 0)+1
 pending='N1:'..P.VERSION..':'..ExposedMembers.SPC_ExpeditionGateSequence
 pendingAction=action
 local packet={OnStart='SPC_ExpeditionGateRequest',Token=pending,Action=action,CityID=c and c:GetID(),UnitID=id}
 local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,packet)
 if not ok then pending=nil;setReport(L('SEND_ERROR',tostring(err)));return end
 setReport(L('WAIT'));if reply()then return end
 local elapsed=0
 ContextPtr:SetUpdate(function(dt)
  elapsed=elapsed+dt;if reply()then return end
  if elapsed>=10 then pending=nil;ContextPtr:ClearUpdate();setReport(L('TIMEOUT'))end
 end)
end
local function updateTarget()
 local t=targets[selected]
 Controls.TargetLabel:SetText(t and Locale.Lookup(t.name) or L('NO_TARGET'))
end
local function refreshTargets()
 local old=targets[selected];targets=R.Targets(Game.GetLocalPlayer());selected=1
 if old then for i,t in ipairs(targets)do if t.owner==old.owner and t.id==old.id then selected=i;break end end end
 updateTarget()
end
local function close()
 Controls.Window:SetHide(true);ContextPtr:SetHide(true)
 ExposedMembers.SPC_ExpeditionGateUIOpenVersion=nil
 ContextPtr:ClearUpdate();pending=nil;targets={};travel=nil
end
local function open()
 if not P.IsTestPlayer(Game.GetLocalPlayer())then return end
 -- InGame.LoadNewContext starts every add-in root hidden; a visible child
 -- cannot override that parent. Confirm both before acknowledging the handoff.
 ContextPtr:SetHide(false);Controls.Window:SetHide(false)
 if ContextPtr:IsHidden() or Controls.Window:IsHidden()then return end
 refreshTargets();request('READ')
 ExposedMembers.SPC_ExpeditionGateUIOpenVersion=P.VERSION
end
local function visibility()
 if not P.IsTestPlayer(Game.GetLocalPlayer())then close()end
end
local initialized=false
local function initialize()
 if initialized then return end
 Controls.CloseButton:RegisterCallback(Mouse.eLClick,close)
 Controls.CreateButton:RegisterCallback(Mouse.eLClick,function()request('CREATE')end)
 Controls.RefreshButton:RegisterCallback(Mouse.eLClick,function()refreshTargets();request('READ')end)
 Controls.ArmButton:RegisterCallback(Mouse.eLClick,function()request('ARM')end)
 Controls.EndButton:RegisterCallback(Mouse.eLClick,function()request('END')end)
 local function move(delta)
  if #targets>0 then selected=((selected-1+delta)%#targets)+1;travel=nil;updateTarget();render()end
 end
 Controls.PreviousButton:RegisterCallback(Mouse.eLClick,function()move(-1)end)
 Controls.NextButton:RegisterCallback(Mouse.eLClick,function()move(1)end)
 Controls.TravelButton:RegisterCallback(Mouse.eLClick,function()
  if pending then setReport(L('WAIT'));return end
  if not current or not current.unitID then setReport(L('TEAM_CHANGED'));return end
  if not targets[selected]then setReport(L('NO_TARGET'));return end
  travel=R.Read(Game.GetLocalPlayer(),current.unitID,targets[selected]);render()
  print('[SPC][B180][N1_TRAVEL] status='..travel.status..' unit='..tostring(travel.unitID)..' target='..tostring(travel.targetOwner)..':'..tostring(travel.targetID)..' travel='..tostring(travel.travel)..' establish='..tostring(travel.establish)..' spyBefore='..tostring(travel.spyBefore)..' spyAfter='..tostring(travel.spyAfter)..' error='..tostring(travel.error))
 end)
 for control,key in pairs({CloseButtonCaption='CLOSE',CreateButtonCaption='CREATE',RefreshButtonCaption='REFRESH',TravelButtonCaption='TRAVEL',ArmButtonCaption='ARM',EndButtonCaption='END'})do
  Controls[control]:SetText(L(key))
 end
 LuaEvents.SPC_ExpeditionGateOpen.Add(open)
 Events.LoadScreenClose.Add(visibility)
 Events.LocalPlayerTurnBegin.Add(visibility)
 Events.GameCoreEventPublishComplete.Add(reply) -- O(1), only while waiting on an explicit request.
 ContextPtr:SetInputHandler(function(message,key)
  if message==KeyEvents.KeyUp and key==Keys.VK_ESCAPE and not Controls.Window:IsHidden()then close();return true end
  return false
 end,true)
 close();visibility();initialized=true
 ExposedMembers.SPC_ExpeditionGateUIVersion=P.VERSION -- UI readiness only; no saved gameplay state.
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 close()
 if initialized then
  LuaEvents.SPC_ExpeditionGateOpen.Remove(open)
  Events.LoadScreenClose.Remove(visibility);Events.LocalPlayerTurnBegin.Remove(visibility)
  Events.GameCoreEventPublishComplete.Remove(reply)
  ExposedMembers.SPC_ExpeditionGateUIVersion=nil;initialized=false
 end
end)
