include('Probe')
include('DevelopmentInvestmentUI')
include('InstanceManager')
local P=SPCP0;local U=SPCDevelopmentInvestmentUI
local list=InstanceManager:new('DevelopmentChoice','Root',Controls.Choices)
local current,pending,requestError,lastRevision
local rows={};local render
local function L(k,...)return Locale.Lookup('LOC_SPC_DEVELOPMENT_'..k,...)end
local function num(v)return type(v)=='number' and string.format('%.6f',v):gsub('0+$',''):gsub('%.$','') or '—'end
local function label(tab,id)local r=id and GameInfo[tab][id];return r and Locale.Lookup(r.Name) or '—'end
local function reason(k)
 local keys={DEVELOPMENT_ACTIVE_IV_REQUIRED='ACTIVE_REQUIRED',DEVELOPMENT_CAPACITY_FULL='CAPACITY_FULL',DEVELOPMENT_TARGET_OCCUPIED='OCCUPIED',
 DEVELOPMENT_NO_BUILDING='NO_BUILDING',DEVELOPMENT_NO_OUTGOING='NO_OUTGOING',DEVELOPMENT_OUTGOING_PENDING='NETWORK_PENDING',
 DEVELOPMENT_PRICE_UNAVAILABLE='PRICE_UNKNOWN',DEVELOPMENT_PRICE_READER_UNAVAILABLE='PRICE_UNKNOWN',DEVELOPMENT_QUOTE_STALE='STALE',
 DEVELOPMENT_GOLD_INSUFFICIENT='NO_GOLD',DEVELOPMENT_WORKERS_UNKNOWN='WORKERS_UNKNOWN',DEVELOPMENT_STANDARD_SPEED_ONLY='SPEED',
 DEVELOPMENT_MONEY_UNCONFIRMED='MONEY_HELD',DEVELOPMENT_NATIVE_OUTCOME_UNKNOWN='MONEY_HELD'}
 return k and L(keys[k] or 'STATE_UNKNOWN',k) or ''
end
local function backend()local b=U.Backend();return b,b and current and b.views[current.owner..':'..current.city]end
local function city()
 if not current or current.owner~=Game.GetLocalPlayer()then return end
 local c=Players[current.owner] and Players[current.owner]:GetCities():FindID(current.city)
 if c and c:GetOwner()==current.owner and U.Reference(current.owner,c)==current.reference then return c end
end
local function close()
 current=nil;pending=nil;requestError=nil;lastRevision=nil;rows={};list:ResetInstances()
 Controls.Window:SetHide(true);ContextPtr:SetHide(true)
end
local function send(action)
 if not current or pending then return end
 local c=city();if not c then close();return end
 local b,v=backend();local row=rows[current.selected]
 ExposedMembers.SPC_DevelopmentUISequence=(ExposedMembers.SPC_DevelopmentUISequence or 0)+1
 local token='DEVELOPMENT:'..P.VERSION..':'..ExposedMembers.SPC_DevelopmentUISequence
 local p={OnStart='SPC_P0_Request',Action=action,CityID=current.city,Token=token,CityToken=v and v.token or '',Revision=v and v.revision or -1}
 if row then p.TargetCity=row.targetCity;p.Domain=row.domain end
 pending=token;requestError=nil
 local ok,result=pcall(UI.RequestPlayerOperation,current.owner,PlayerOperations.EXECUTE_SCRIPT,p)
 if not ok or result==false then pending=nil;requestError='DEVELOPMENT_REQUEST_UNCONFIRMED'end
 render()
end
render=function()
 local c=city();if not c then close();return end
 local b,v=backend();rows={};list:ResetInstances()
 for _,row in ipairs(v and v.options or {})do rows[#rows+1]=row end
 -- Signed contracts remain inspectable after route/qualification loss.
 for _,contract in pairs(v and v.contracts or {})do
  local target=Players[current.owner]:GetCities():FindID(contract.target.cityID)
  local name=target and target:GetX()==contract.target.x and target:GetY()==contract.target.y and Locale.Lookup(target:GetName()) or L('CITY_ID',contract.target.cityID)
  rows[#rows+1]={targetCity=contract.target.cityID,targetName=name,domain=contract.domain,contract=contract}
 end
 Controls.CityName:SetText(Locale.Lookup(c:GetName()))
 Controls.Balance:SetText(L('BALANCE',num(v and v.balance),v and v.used or 0,v and v.workers or 0))
 for index,row in ipairs(rows)do
  local i=index;local instance=list:GetInstance()
  instance.Caption:SetText(row.targetName..' · '..label('Districts',row.domain))
  local text=row.contract and L('STATE_'..row.contract.stage) or reason(row.reason)
  instance.State:SetText(text);instance.Root:SetToolTipString(row.targetName..' · '..label('Districts',row.domain)..'[NEWLINE]'..text)
  instance.Root:SetAlpha(current.selected==i and 1 or .75)
  instance.Root:RegisterCallback(Mouse.eLClick,function()if current and not pending then current.selected=i;render()end end)
 end
 Controls.Choices:CalculateSize();Controls.Choices:ReprocessAnchoring();Controls.Scroll:CalculateInternalSize()
 local row=rows[current.selected];local contract=row and row.contract
 Controls.Subject:SetText(row and row.targetName..' · '..label('Districts',row.domain) or L('SELECT'))
 Controls.Quote:SetText(row and row.price and L('QUOTE',label('Buildings',row.building),num(row.price),num(row.cost),row.candidates) or '')
 Controls.Terms:SetText(row and L('TERMS') or '')
 Controls.Contract:SetText(contract and L('CONTRACT',L('STATE_'..contract.stage),num(contract.cost),num(contract.debited)) or '')
 local can=v and v.stage=='READY' and v.canSign and not v.quoteStale and row and row.canSign and not pending
 Controls.Confirm:SetDisabled(not can);Controls.Refresh:SetDisabled(pending~=nil)
 local message=pending and L('WAITING') or requestError and reason(requestError) or v and v.stage=='HELD' and reason(v.reason)
  or v and v.quoteStale and L('STALE') or row and not row.canSign and not contract and reason(row.reason)
  or v and not v.canSign and reason(v.reason) or #rows==0 and reason(v and v.reason) or ''
 Controls.Error:SetText(message);Controls.Error:SetToolTipString(message)
 lastRevision=v and v.revision
end
local function open(pid,id)
 if pid~=Game.GetLocalPlayer() or not P.IsTestPlayer(pid)then return end
 local c=Players[pid] and Players[pid]:GetCities():FindID(id);if not c then return end
 current={owner=pid,city=id,reference=U.Reference(pid,c)};pending=nil;requestError=nil;lastRevision=nil
 ContextPtr:SetHide(false);Controls.Window:SetHide(false);send('DEVELOPMENT_OPEN')
end
local function publish()
 if not current then return end
 if not city()then close();return end
 local b,v=backend();local ack=b and b.lastRequest
 local answered=pending and ack and ack.token==pending and ack.owner==current.owner and ack.city==current.city
 if answered then pending=nil;requestError=not ack.accepted and ack.reason or nil end
 if answered or not v or v.revision~=lastRevision then render()end
end
local function initialize()
 for _,pair in ipairs({{'Title','TITLE'},{'CloseCaption','CLOSE'},{'ConfirmCaption','CONFIRM'},{'RefreshCaption','REFRESH'},{'Help','HELP'}})do Controls[pair[1]]:SetText(L(pair[2]))end
 Controls.Close:RegisterCallback(Mouse.eLClick,close)
 Controls.Confirm:RegisterCallback(Mouse.eLClick,function()send('DEVELOPMENT_CONFIRM')end)
 Controls.Refresh:RegisterCallback(Mouse.eLClick,function()send('DEVELOPMENT_REFRESH')end)
 LuaEvents.SPC_DevelopmentOpen.Add(open);Events.GameCoreEventPublishComplete.Add(publish)
 Events.LoadScreenClose.Add(close);Events.LocalPlayerChanged.Add(close)
 ContextPtr:SetInputHandler(function(message,key)if current and message==KeyEvents.KeyUp and key==Keys.VK_ESCAPE then close();return true end;return false end,true)
 close()
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 close();LuaEvents.SPC_DevelopmentOpen.Remove(open);Events.GameCoreEventPublishComplete.Remove(publish)
 Events.LoadScreenClose.Remove(close);Events.LocalPlayerChanged.Remove(close)
end)
