include('Probe')
local P=SPCP0
local selected,target,pending,token;local consumed=false;local reads=0;local initialized=false
local function L(k,...)return Locale.Lookup('LOC_SPC_MOVE_PROBE_'..k,...)end
local function show(s)Controls.Report:SetText(s)end
local function scalar(u,k)
 local ok,v=pcall(function()return u[k](u)end)
 return ok and (type(v)=='number' or type(v)=='boolean') and tostring(v) or 'UNKNOWN'
end
local function close()Controls.Window:SetHide(true)end
local function nativeSample()
 if not selected or not consumed or reads>=4 then return end
 reads=reads+1
 local player=Players[selected.owner];local u=player and player:GetUnits():FindID(selected.id)
 print('[SPC][B191][N1_TASK] movementProbe=UI_READ owner='..selected.owner..' unit='..selected.id
  ..' actual='..scalar(u,'GetX')..','..scalar(u,'GetY')..' operation='..scalar(u,'GetSpyOperation')..' activity='..scalar(u,'GetActivityType'))
end
local function reply()
 local r=ExposedMembers.SPC_ExpeditionMovementReply
 if not token or type(r)~='table' or r.token~=token or r.owner~=Game.GetLocalPlayer() or r.version~=P.VERSION then return end
 pending=false;consumed=consumed or r.reload==true
 local text=L('RESULT',L('STATUS_'..r.status),r.reason or '-',tostring(r.x or '?'),tostring(r.y or '?'))
 show(text..'[NEWLINE]'..L(consumed and 'RELOAD' or 'RETRY'))
 Controls.Place:SetDisabled(consumed);Controls.Move:SetDisabled(consumed)
end
local function published()reply();nativeSample()end
local function open()
 if not P.IsTestPlayer(Game.GetLocalPlayer())then return end
 Controls.Window:SetHide(false);ExposedMembers.SPC_ExpeditionMovementOpen=P.VERSION
 if consumed or pending then reply();return end
 local u=UI.GetHeadSelectedUnit();selected=nil;target=nil
 if u and u:GetOwner()==Game.GetLocalPlayer()then
  local r=P.Info('Units',u:GetType())
  if r and (r.UnitType=='UNIT_SPY' or r.UnitType=='UNIT_SPC_EXPEDITION_SPY')then
   selected={owner=u:GetOwner(),id=u:GetID(),kind=u:GetType(),name=u:GetName()}
  end
 end
 Controls.Place:SetDisabled(not selected);Controls.Move:SetDisabled(not selected)
 Controls.Target:SetText(L('MARK_HINT'))
 show(selected and L('SELECTED',Locale.Lookup(P.Info('Units',selected.kind).Name),selected.id) or L('SELECT_FIRST'))
end
local function mark()
 if consumed or pending then return end
 local ok,plot=pcall(function()return Map.GetPlotByIndex(UI.GetCursorPlotID())end)
 if not ok or not plot then show(L('NO_PLOT'));return end
 target={x=plot:GetX(),y=plot:GetY()};Controls.Target:SetText(L('TARGET',target.x,target.y))
end
local function run(method)
 if consumed or pending then return end
 if not selected or not target then show(L('SELECT_FIRST'));return end
 local player=Players[selected.owner];local u=player and player:GetUnits():FindID(selected.id)
 if not u or u:GetOwner()~=selected.owner or u:GetType()~=selected.kind or u:GetName()~=selected.name then show(L('CHANGED'));return end
 local ok,op=pcall(function()return u:GetSpyOperation()end)
 if not ok or op~=-1 then show(L('NOT_IDLE'));return end
 ExposedMembers.SPC_MovementSequence=(ExposedMembers.SPC_MovementSequence or 0)+1
 token='MOVE:'..P.VERSION..':'..ExposedMembers.SPC_MovementSequence;pending=true
 local p={OnStart='SPC_ExpeditionMovementRequest',Token=token,Method=method,UnitID=selected.id,Kind=selected.kind,Name=selected.name,
  FromX=u:GetX(),FromY=u:GetY(),X=target.x,Y=target.y,SampleTurn=Game.GetCurrentGameTurn(),NativeOperation=op}
 -- An uncertain dispatch is never resent. The explicit read button only reads
 -- the reply/native unit; there is no frame callback, timeout or polling.
 Controls.Place:SetDisabled(true);Controls.Move:SetDisabled(true);show(L('WAIT'))
 local sent=pcall(UI.RequestPlayerOperation,selected.owner,PlayerOperations.EXECUTE_SCRIPT,p)
 if not sent then consumed=true;pending=false;show(L('SEND_UNKNOWN')..'[NEWLINE]'..L('RELOAD'));return end
 reply()
end
local function initialize()
 if initialized then return end;initialized=true
 Controls.Close:RegisterCallback(Mouse.eLClick,close)
 Controls.Place:RegisterCallback(Mouse.eLClick,function()run('PlaceUnit')end)
 Controls.Move:RegisterCallback(Mouse.eLClick,function()run('MoveUnit')end)
 Controls.Read:RegisterCallback(Mouse.eLClick,function()reply();nativeSample()end)
 LuaEvents.SPC_ExpeditionMovementOpen.Add(open);Events.GameCoreEventPublishComplete.Add(published)
 ContextPtr:SetInputHandler(function(message,key)
  if type(message)=='table' or type(message)=='userdata'then key=message:GetKey();message=message:GetMessageType()end
  if Controls.Window:IsHidden()then return false end
  if key==Keys.VK_M then if message==KeyEvents.KeyUp then mark()end;return true end
  if key==Keys.VK_ESCAPE then if message==KeyEvents.KeyUp then close()end;return true end
  return false
 end,true)
 close();ExposedMembers.SPC_ExpeditionMovementUIVersion=P.VERSION
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 if initialized then
  LuaEvents.SPC_ExpeditionMovementOpen.Remove(open);Events.GameCoreEventPublishComplete.Remove(published)
  ExposedMembers.SPC_ExpeditionMovementUIVersion=nil;ExposedMembers.SPC_ExpeditionMovementOpen=nil
 end
end)
