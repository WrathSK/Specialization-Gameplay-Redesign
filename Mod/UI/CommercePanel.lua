include('Probe')
include('CommerceUI')
include('InstanceManager')
local P=SPCP0;local U=SPCCommerceUI
local current,pending,lastRevision,lastToken,requestError
local initialized=false
local domains=InstanceManager:new('CommerceDomain','Root',Controls.Domains)
local render,toggle
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
local function layout()
 local width,height=UIManager:GetScreenSizeVal()
 local narrow=width-16<590;local column=narrow and math.min(360,math.max(220,width-16)) or 295
 local h=math.max(240,height-27);local top=narrow and 0 or 148
 Controls.Window:SetSizeVal(narrow and column or column*2+1,h)
 Controls.DomainColumn:SetSizeVal(column,h)
 Controls.DetailColumn:SetSizeVal(column,h-top);Controls.DetailColumn:SetOffsetX(narrow and 0 or column+1);Controls.DetailColumn:SetOffsetY(top)
 Controls.DomainColumn:SetHide(narrow and current.domain~=nil);Controls.DetailColumn:SetHide(current.domain==nil)
 Controls.Back:SetHide(not narrow)
 Controls.CityName:SetTruncateWidth(column-68)
 Controls.Summary:SetTruncateWidth(column-44);Controls.Reputation:SetTruncateWidth(column-44)
 Controls.Confirm:SetSizeVal(math.min(285,column-10),41)
 local y=0
 for _,name in ipairs({'Value','Source','Rules','Status'})do
  Controls[name..'Title']:SetTruncateWidth(column-42);Controls[name]:SetWrapWidth(column-44)
  local body=Controls[name]:GetSizeY();Controls[name..'Card']:SetOffsetY(y);Controls[name..'Card']:SetSizeY(body+62);y=y+body+74
 end
 local footer=narrow and 90 or 66
 Controls.Footer:SetSizeY(footer)
 Controls.Details:SetSizeY(y-12);Controls.DetailScroll:SetSizeY(math.max(40,h-top-54-footer-8))
 return column
end
render=function()
 local c=city();if not c then close();return end
 local b,v=backendView();local good=U.Available(v) and v.reference==current.reference
 Controls.CityName:SetText(Locale.Lookup(c:GetName()))
 Controls.Summary:SetText(good and L('SIDEBAR_CAPACITY',#(v.effective or {}),number(v.workers)) or L('WAITING'))
 local reputation=good and v.reputation or {}
 local reputationText
 if not good then reputationText=L('WAITING')
 elseif v.reputationKnown==false or v.reason=='COMMERCE_REPUTATION_UNKNOWN' or reputation.state=='UNKNOWN_INTERVAL' then reputationText=L('REPUTATION_UNKNOWN')
 elseif reputation.state=='NOT_ESTABLISHED' then reputationText=L('REPUTATION_NOT_STARTED')
 elseif type(reputation.age)~='number' or type(reputation.effective)~='number' then reputationText=L('REPUTATION_UNKNOWN')
 else reputationText=L('REPUTATION',number(reputation.age),number(reputation.effective))end
 Controls.Reputation:SetText(reputationText);Controls.Reputation:SetToolTipString(reputationText)
 local rows,defs,order,seen={},{},{},{}
 for _,row in ipairs(good and v.domains or {})do rows[row.id]=row end
 for _,def in ipairs(U.DOMAINS)do defs[def.id]=def end
 -- Selected order is backend-owned. Never reorder configuration to match the UI.
 for _,id in ipairs(good and v.selected or {})do if defs[id] and not seen[id]then order[#order+1]=id;seen[id]=true end end
 for _,def in ipairs(U.DOMAINS)do if not seen[def.id]then order[#order+1]=def.id end end
 if current.domain and not rows[current.domain]then current.domain=nil end
 local row=rows[current.domain]
 local state=row and reason(row.reason or (row.effective and 'COMMERCE_EFFECTIVE' or row.selected and 'COMMERCE_CAPACITY' or 'COMMERCE_NOT_SELECTED')) or L('PICK_DOMAIN')
 local detail=row and row.effective and L('VALUE_DETAIL',number(row.gold),number(row.raw),number(v.totalGold)) or row and (row.selected and L('VALUE_PAUSED') or L('VALUE_AFTER_ENABLE')) or L('PICK_DOMAIN')
 Controls.Value:SetText(detail)
 Controls.Source:SetText(row and row.effective and L('SOURCE_DETAIL',row.sourceName and Locale.Lookup(row.sourceName) or L('NO_SOURCE'),number(row.X),number(row.localD),number(reputation.effective)) or L('SOURCE_AFTER_ENABLE'))
 Controls.Rules:SetText(L('FORMULA')..'[NEWLINE][NEWLINE]'..L('LIFO_HELP'))
 local message=requestError and reason(requestError) or pending and L('REQUEST_WAIT') or good and v.stage~='READY' and reason(v.reason) or ''
 if good and v.cleanupConfirmed==false then message=message..'[NEWLINE]'..L('CLEANUP_ERROR',number(v.remainingCarrierGold))end
 Controls.Status:SetText(state..(message~='' and '[NEWLINE][NEWLINE]'..message or ''))
 Controls.ConfirmCaption:SetText(L(row and row.selected and 'STOP' or 'START'))
 Controls.Confirm:SetDisabled(not(good and v.canConfigure and row and (row.selected or row.eligible)) or pending~=nil)
 local column=layout();domains:ResetInstances()
 for _,id in ipairs(order)do
  local def=defs[id];local item=rows[id];local instance=domains:GetInstance()
  instance.Icon:SetIcon('ICON_'..id);instance.Caption:SetText(L('DOMAIN_'..def.key))
  instance.Caption:SetTruncateWidth(column-96)
  instance.Marker:SetText(item and item.effective and L('RUNNING') or item and item.selected and L('SELECTED_PAUSED') or '')
  instance.Marker:SetHide(not(item and item.selected))
  local text=item and reason(item.reason or (item.effective and 'COMMERCE_EFFECTIVE' or item.selected and 'COMMERCE_CAPACITY' or 'COMMERCE_NOT_SELECTED')) or L('WAITING')
  instance.State:SetText(text);instance.State:SetWrapWidth(column-96)
  instance.Root:SetSizeY(math.max(100,instance.State:GetSizeY()+76))
  instance.Caption:SetColorByName(current.domain==id and 'Gold' or 'White')
  instance.Root:RegisterCallback(Mouse.eLClick,function()if current and not pending then current.domain=id;render()end end)
 end
 Controls.Domains:CalculateSize();Controls.Domains:ReprocessAnchoring();Controls.DomainScroll:CalculateInternalSize();Controls.DetailScroll:CalculateInternalSize();Controls.Window:ReprocessAnchoring()
 if good then lastRevision=v.revision;lastToken=v.token end
end
toggle=function(domain)
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
local function resizeEvent(kind)if current and kind==SystemUpdateUI.ScreenResize then render()end end
local function initialize()
 if initialized then return end
 Controls.CloseButton:RegisterCallback(Mouse.eLClick,close)
 Controls.Confirm:RegisterCallback(Mouse.eLClick,function()if current and current.domain then toggle(current.domain)end end)
 Controls.Back:RegisterCallback(Mouse.eLClick,function()if current then current.domain=nil;render()end end)
 for _,pair in ipairs({{'Title','TITLE'},{'DetailTitle','DETAIL_TITLE'},{'ValueTitle','VALUE_TITLE'},{'SourceTitle','SOURCE_TITLE'},{'RulesTitle','RULES_TITLE'},{'StatusTitle','STATUS_TITLE'},{'BackCaption','BACK'}})do Controls[pair[1]]:SetText(L(pair[2]))end
 LuaEvents.SPC_CommerceOpen.Add(open);Events.GameCoreEventPublishComplete.Add(publish)
 Events.LoadScreenClose.Add(close);Events.LocalPlayerChanged.Add(close)
 ContextPtr:SetInputHandler(function(message,key)
  if type(message)=='table' or type(message)=='userdata'then key=message:GetKey();message=message:GetMessageType()end
  if current and key==Keys.VK_ESCAPE then
   if message==KeyEvents.KeyUp then close()end
   return true
  end
  return false
 end,true)
 Events.SystemUpdateUI.Add(resizeEvent)
 initialized=true;close()
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 close()
 if initialized then
  LuaEvents.SPC_CommerceOpen.Remove(open);Events.GameCoreEventPublishComplete.Remove(publish)
  Events.LoadScreenClose.Remove(close);Events.LocalPlayerChanged.Remove(close);Events.SystemUpdateUI.Remove(resizeEvent);initialized=false
 end
end)
