-- Normal training name confirmation is independent of opening P0 or the sidebar.
include('Probe')
include('ExpeditionSpyRead')
local P=SPCP0;local job;local finished;local seq=0
local function stop(reason)
 local j=job;job=nil;ContextPtr:ClearUpdate()
 ExposedMembers.SPC_ExpeditionTrainingNameError=reason
 if j then finished=j.key end
end
local function tick(dt)
 local j=job;if not j then return end
 local v=ExposedMembers.SPC_ExpeditionActivity
 if not v or v.phase~='NAMING' or v.teamKey~=j.key or v.unitID~=j.id then stop();return end
 j.elapsed=j.elapsed+(dt or 0);j.poll=j.poll+(dt or 0)
 if j.elapsed>=10 then stop('TRAINING_NAME_CONFIRMATION_TIMEOUT');return end
 if j.poll<0.25 then return end;j.poll=0
 if j.sent then
  local r=ExposedMembers.SPC_ExpeditionGateReply
  if r and r.token==j.token then stop(r.error)end
  return
 end
 local r=SPCExpeditionSpyRead.NativeName(j.owner,j.id)
 if r.status=='PENDING' then return end
 if r.status~='READY' then stop(r.reason);return end
 seq=seq+1;j.token='TRAIN_NAME:'..j.key..':'..seq;j.sent=true
 local ok,err=pcall(UI.RequestPlayerOperation,j.owner,PlayerOperations.EXECUTE_SCRIPT,
  {OnStart='SPC_ExpeditionGateRequest',Action='NAME',Token=j.token,UnitID=j.id,Name=r.name,
   NameOffmapChecked=true,NameSampleTurn=Game.GetCurrentGameTurn()})
 if not ok then stop(tostring(err))end
end
local function pulse()
 local v=ExposedMembers.SPC_ExpeditionActivity
 if not v or v.phase~='NAMING' or not v.trainingToken or not v.teamKey or
  v.owner~=Game.GetLocalPlayer() or not P.IsTestPlayer(v.owner)then return end
 if job or finished==v.teamKey then return end
 job={owner=v.owner,id=v.unitID,key=v.teamKey,elapsed=0,poll=0}
 ContextPtr:SetUpdate(tick)
end
Events.GameCoreEventPublishComplete.Add(pulse)
Events.LoadScreenClose.Add(pulse)
ContextPtr:SetShutdown(function()stop();Events.GameCoreEventPublishComplete.Remove(pulse);Events.LoadScreenClose.Remove(pulse)end)
