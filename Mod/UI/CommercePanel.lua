include('Probe')
include('CommerceUI')
local P=SPCP0;local U=SPCCommerceUI
local current,pending,lastRevision,lastToken,requestError
local initialized=false
local function L(k,...)return Locale.Lookup('LOC_SPC_COMMERCE_'..k,...)end
local function number(v)
 if type(v)~='number' or v~=v or v==math.huge or v==-math.huge then return L('WAITING')end
 local out=string.format('%.6f',v):gsub('0+$',''):gsub('%.$','');return out
end
local function reason(k)
 local keys={COMMERCE_EFFECTIVE='EFFECTIVE',COMMERCE_NOT_SELECTED='NOT_SELECTED',COMMERCE_LOCAL_DISTRICT_REQUIRED='LOCAL_DISTRICT_REQUIRED',
  COMMERCE_CAPACITY='NO_WORKERS',COMMERCE_ACTIVE_III_REQUIRED='INACTIVE',COMMERCE_NETWORK_UNKNOWN='NETWORK_WAIT',
  COMMERCE_REPUTATION_UNKNOWN='REPUTATION_UNKNOWN',COMMERCE_SOURCE_IDENTITY_UNKNOWN='SOURCE_IDENTITY_UNKNOWN'}
 return keys[k] and L(keys[k]) or L('ERROR',k or L('WAITING'))
end
local function backendView()
 local b=U.Backend();if not b or not current then return b end
 return b,b.views[current.owner..':'..current.city]
end
local function city()
 if not current or current.owner~=Game.GetLocalPlayer() or not P.IsTestPlayer(current.owner)then return end
 local c=Players[current.owner] and Players[current.owner]:GetCities():FindID(current.city)
 if c and c:GetOwner()==current.owner and U.Reference(current.owner,c)==current.reference then return c end
end
local function close()
 current=nil;pending=nil;requestError=nil;lastRevision=nil;lastToken=nil
 Controls.Window:SetHide(true);ContextPtr:SetHide(true)
end
local function render()
 local c=city();if not c then close();return end
 local b,v=backendView();local good=U.Available(v) and v.reference==current.reference
 Controls.CityName:SetText(Locale.Lookup(c:GetName()))
 Controls.Summary:SetText(good and L('SUMMARY',#(v.effective or {}),number(v.workers),#(v.selected or {}),number(v.totalGold)) or L('WAITING'))
 local reputation=good and v.reputation or {}
 local reputationText
 if not good then reputationText=L('WAITING')
 elseif v.reason=='COMMERCE_REPUTATION_UNKNOWN' or reputation.state=='UNKNOWN_INTERVAL' then reputationText=L('REPUTATION_UNKNOWN')
 elseif reputation.state=='NOT_ESTABLISHED' then reputationText=L('REPUTATION_NOT_STARTED')
 elseif type(reputation.age)~='number' or type(reputation.effective)~='number' then reputationText=L('REPUTATION_UNKNOWN')
 else reputationText=L('REPUTATION',number(reputation.age),number(reputation.effective))end
 Controls.Reputation:SetText(reputationText);Controls.Reputation:SetToolTipString(reputationText)
 local rows={};for _,r in ipairs(good and v.domains or {})do rows[r.id]=r end
 for i,domain in ipairs(U.DOMAINS)do
  local r=rows[domain.id];local prefix='Domain'..i
  Controls[prefix..'Name']:SetText(L('DOMAIN_'..domain.key))
  Controls[prefix..'Icon']:SetIcon(domain.icon)
  local state=r and reason(r.reason or (r.effective and 'COMMERCE_EFFECTIVE' or r.selected and 'COMMERCE_CAPACITY' or 'COMMERCE_NOT_SELECTED')) or L('WAITING')
  Controls[prefix..'State']:SetText(state);Controls[prefix..'State']:SetToolTipString(state)
  Controls[prefix..'Toggle']:SetToolTipString(state)
  local detail=r and L('DOMAIN_DETAIL',number(r.localD),number(r.X),number(r.raw),number(r.gold or r.floor)) or L('WAITING')
  local source=L('SOURCE',r and r.sourceName and Locale.Lookup(r.sourceName) or L('NO_SOURCE'))
  Controls[prefix..'Details']:SetText(detail);Controls[prefix..'Details']:SetToolTipString(detail)
  Controls[prefix..'Source']:SetText(source);Controls[prefix..'Source']:SetToolTipString(source)
  Controls[prefix..'ToggleCaption']:SetText(L(r and r.selected and 'DISABLE' or 'ENABLE'))
  Controls[prefix..'Toggle']:SetDisabled(not(good and v.canConfigure and r and (r.selected or r.eligible)) or pending~=nil)
  Controls[prefix..'State']:SetAlpha(r and r.effective and 1 or .7)
 end
 local message=requestError and reason(requestError) or pending and L('REQUEST_WAIT') or good and v.stage~='READY' and reason(v.reason) or ''
 if good and v.cleanupConfirmed==false then
  local warning=L('CLEANUP_ERROR',number(v.remainingCarrierGold))
  message=message~='' and message..'[NEWLINE]'..warning or warning
 end
 Controls.Error:SetText(message);Controls.Error:SetToolTipString(message)
 if good then lastRevision=v.revision;lastToken=v.token end
end
local function toggle(domain)
 if pending then return end
 local c=city();local b,v=backendView()
 if not c or not U.Available(v) or not v.canConfigure or v.reference~=current.reference then render();return end
 local row;for _,r in ipairs(v.domains or {})do if r.id==domain then row=r;break end end
 if not row or (not row.selected and not row.eligible)then return end
 ExposedMembers.SPC_CommerceUISequence=(ExposedMembers.SPC_CommerceUISequence or 0)+1
 local token='COMMERCE:'..P.VERSION..':'..ExposedMembers.SPC_CommerceUISequence
 local packet={OnStart='SPC_P0_Request',Action='COMMERCE_SELECT',CityID=current.city,Domain=domain,Enabled=not row.selected,
  Reference=current.reference,CityToken=v.token,Revision=v.revision,Token=token}
 pending=token;requestError=nil -- latch before native re-entry; never send on render/hover.
 local ok,result=pcall(UI.RequestPlayerOperation,current.owner,PlayerOperations.EXECUTE_SCRIPT,packet)
 if not ok or result==false then pending=nil;requestError='COMMERCE_REQUEST_UNCONFIRMED'end
 render()
end
local function open(pid,id)
 if pid~=Game.GetLocalPlayer() or not P.IsTestPlayer(pid)then return end
 local c=Players[pid] and Players[pid]:GetCities():FindID(id);local b=U.Backend();local v=b and b.views[pid..':'..id]
 if not c or c:GetOwner()~=pid or not U.Available(v) or v.reference~=U.Reference(pid,c)then return end
 current={owner=pid,city=id,reference=v.reference};pending=nil;requestError=nil;lastRevision=nil;lastToken=nil
 ContextPtr:SetHide(false);Controls.Window:SetHide(false);render()
end
local function publish()
 if not current then return end
 if not city()then close();return end
 local b,v=backendView();local ack=b and b.lastRequest
 local answered=pending and ack and ack.token==pending and ack.owner==current.owner and ack.city==current.city
 if answered then pending=nil;requestError=not ack.accepted and ack.reason or nil end
 if answered or not v or v.revision~=lastRevision or v.token~=lastToken then render()end
end
local function initialize()
 if initialized then return end
 Controls.CloseButton:RegisterCallback(Mouse.eLClick,close)
 for i,domain in ipairs(U.DOMAINS)do
  local id=domain.id;Controls['Domain'..i..'Toggle']:RegisterCallback(Mouse.eLClick,function()toggle(id)end)
 end
 Controls.Title:SetText(L('TITLE'));Controls.CloseButtonCaption:SetText(L('CLOSE'))
 local formula=L('FORMULA');Controls.Formula:SetText(formula);Controls.Formula:SetToolTipString(formula)
 Controls.Help:SetText(L('LIFO_HELP'))
 LuaEvents.SPC_CommerceOpen.Add(open);Events.GameCoreEventPublishComplete.Add(publish)
 Events.LoadScreenClose.Add(close);Events.LocalPlayerChanged.Add(close)
 ContextPtr:SetInputHandler(function(message,key)
  if message==KeyEvents.KeyUp and key==Keys.VK_ESCAPE and current then close();return true end
  return false
 end,true)
 initialized=true;close()
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 close()
 if initialized then
  LuaEvents.SPC_CommerceOpen.Remove(open);Events.GameCoreEventPublishComplete.Remove(publish)
  Events.LoadScreenClose.Remove(close);Events.LocalPlayerChanged.Remove(close);initialized=false
 end
end)
