-- B068: UI-only mirror. The validated Gameplay read is the only state source.
include('Probe')
local P=SPCP0
local parent,parentWidth,key,token,age,lastError
local timer=0;local observedTurn,observedWrites;local dirty=true;local shown
local names={RESEARCH='科研',CULTURE='文化',INDUSTRY='工业',COMMERCE='商业'}
local hidden
local function hide(v) if hidden~=v then hidden=v;Controls.Badge:SetHide(v) end end
local titles={'专业城市','专业名城','专业都会','专业中心'}
local function reportError(err)
 if err~=lastError then
  if err then print('[SPC][POTENTIAL_UI] '..tostring(err)) end
  lastError=err
 end
end
local function update(dt)
 timer=timer+dt;if timer<0.5 then return end
 local step=timer;timer=0
 local pid=Game.GetLocalPlayer();local c=UI.GetHeadSelectedCity()
 if not P.IsTestPlayer(pid) or not c or c:GetOwner()~=pid then
  hide(true);key=nil;token=nil;return
 end
 if not parent then
  parent=ContextPtr:LookUpControl('/InGame/WorldTracker/WorldTrackerHeader')
  if not parent then reportError('POTENTIAL_HEADER_UNAVAILABLE');return end
  Controls.Badge:ChangeParent(parent)
 end
 local width=parent:GetSizeX()
 if width~=parentWidth then parentWidth=width;Controls.Badge:SetOffsetVal(width+8,36) end
 local k=pid..':'..c:GetID()
 local turn=Game.GetCurrentGameTurn();local writes=ExposedMembers.SPC_RuntimeUIRevision or 0
 if k~=key or turn~=observedTurn or writes~=observedWrites then dirty=true end
 observedTurn=turn;observedWrites=writes
 if k~=key then key=k;token=nil;age=10;shown=nil;hide(true) end
 age=(age or 0)+step
 if token then
  local v=(ExposedMembers.SPC_P0 or {}).CityPresentationView
  if v and v.token==token and v.owner==pid and v.cityID==c:GetID() then
   token=nil;reportError(v.error)
   local name=names[v.specialization];local title=titles[v.potential]
   hide(not (name and title))
   if name and title and shown~=name..v.potential..tostring(v.investments) then
    shown=name..v.potential..tostring(v.investments)
    Controls.BadgeCaption:SetText(name..v.potential..'级')
    Controls.Badge:SetToolTipString(title..'[NEWLINE]当前专业：'..name..'[NEWLINE]专业潜力：'..v.potential..'级'
     ..'[NEWLINE]已完成专业投资：'..tostring(v.investments)..'次[NEWLINE][NEWLINE]专业潜力代表这座城市永久完成的专业化投资。实际启用的专业等级仍取决于已建立总督的晋升条件。')
   end
  elseif age>5 then token=nil;hide(true);reportError('PRESENTATION_TIMEOUT') end
 end
 -- Only the selected city; no city enumeration or state mutation.
 if not token and dirty and not UI.IsGameCoreBusy() then
  dirty=false
  ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
  token=P.VERSION..':POTENTIAL:'..ExposedMembers.SPC_P0_UISequence;age=0
  local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
   {OnStart='SPC_P0_Request',Action='CITY_PRESENTATION_READ',CityID=c:GetID(),Token=token})
  if not ok then token=nil;reportError(err) end
 end
end
ContextPtr:SetInitHandler(function() ContextPtr:SetHide(false);ContextPtr:SetUpdate(update) end)
ContextPtr:SetShutdown(function() ContextPtr:ClearUpdate();hide(true) end)
