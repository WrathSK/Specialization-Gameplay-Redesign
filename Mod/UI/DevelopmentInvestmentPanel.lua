-- B252: one existing quotation snapshot, three UI-only selection columns.
include('Probe')
include('DevelopmentInvestmentUI')
include('InstanceManager')
local P=SPCP0;local U=SPCDevelopmentInvestmentUI
local cities=InstanceManager:new('DevelopmentCity','Root',Controls.Cities)
local districts=InstanceManager:new('DevelopmentDistrict','Root',Controls.Districts)
local current,pending,requestError,lastRevision
local groups,groupByKey={},{}
local render
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
local function selection()
 local g=current and groupByKey[current.target]
 return g,g and g.byDomain[current.domain]
end
local function close()
 current=nil;pending=nil;requestError=nil;lastRevision=nil;groups={};groupByKey={}
 cities:ResetInstances();districts:ResetInstances()
 Controls.Window:SetHide(true);ContextPtr:SetHide(true)
end
local function canConfirm(v,row)
 return v and v.stage=='READY' and v.canSign and not v.quoteStale and row and row.canSign and not pending
end
local function send(action)
 if not current or pending then return end
 if not city()then close();return end
 local b,v=backend();local g,row=selection()
 if action=='DEVELOPMENT_CONFIRM' and not canConfirm(v,row)then return end
 ExposedMembers.SPC_DevelopmentUISequence=(ExposedMembers.SPC_DevelopmentUISequence or 0)+1
 local token='DEVELOPMENT:'..P.VERSION..':'..ExposedMembers.SPC_DevelopmentUISequence
 local p={OnStart='SPC_P0_Request',Action=action,CityID=current.city,Token=token,CityToken=v and v.token or '',Revision=v and v.revision or -1}
 if row then p.TargetCity=row.targetCity;p.Domain=row.domain end
 pending=token;requestError=nil
 local ok,result=pcall(UI.RequestPlayerOperation,current.owner,PlayerOperations.EXECUTE_SCRIPT,p)
 if not ok or result==false then pending=nil;requestError='DEVELOPMENT_REQUEST_UNCONFIRMED'end
 render()
end
-- Build a detached view; never annotate or mutate Gameplay's shared snapshot.
local function collect(v)
 groups={};groupByKey={}
 local targetCache={}
 local function group(id,name,saved)
  local target=targetCache[id]
  if target==nil then target=Players[current.owner]:GetCities():FindID(id) or false;targetCache[id]=target end
  local matches=target and (not saved or (target:GetX()==saved.x and target:GetY()==saved.y))
  local key=matches and U.Reference(current.owner,target) or 'HISTORY:'..tostring(saved and saved.token or id)
  local g=groupByKey[key]
  if not g then
   g={key=key,id=id,name=name or (matches and Locale.Lookup(target:GetName()) or L('CITY_ID',id)),rows={},byDomain={}}
   groups[#groups+1]=g;groupByKey[key]=g
  end
  return g
 end
 for _,item in ipairs(v and v.options or {})do
  local g=group(item.targetCity,item.targetName)
  if item.domain then
   local row={};for k,x in pairs(item)do row[k]=x end
   g.rows[#g.rows+1]=row;g.byDomain[row.domain]=row
  else g.reason=item.reason end
 end
 -- Contracts stay inspectable even after the route, current eligibility or city is lost.
 for _,contract in pairs(v and v.contracts or {})do
  local g=group(contract.target.cityID,nil,contract.target)
  local row=g.byDomain[contract.domain]
  if not row then row={targetCity=g.id,targetName=g.name,domain=contract.domain};g.rows[#g.rows+1]=row;g.byDomain[row.domain]=row end
  row.contract=contract
 end
 table.sort(groups,function(a,b)if a.id==b.id then return a.key<b.key end;return a.id<b.id end)
 for _,g in ipairs(groups)do table.sort(g.rows,function(a,b)return a.domain<b.domain end)end
 -- Keep identity, never list position, across reordered/new/removed quote rows.
 local g=groupByKey[current.target]
 if not g then current.target=nil;current.domain=nil
 elseif not g.byDomain[current.domain]then current.domain=nil end
end
local function layout()
 local width,height=UIManager:GetScreenSizeVal()
 local available=math.max(220,width-16)
 local narrow=available<800
 local a=narrow and math.min(360,available) or math.min(295,math.floor(available*.30))
 local b=narrow and a or math.min(280,math.floor(available*.29))
 local d=narrow and a or math.min(360,available-a-b-2)
 local h=math.max(240,height-114)
 Controls.Window:SetSizeVal(narrow and a or a+b+d+2,h)
 local contentHeight=h-(narrow and 40 or 0)
 Controls.CityColumn:SetSizeVal(a,contentHeight);Controls.DistrictColumn:SetSizeVal(b,contentHeight);Controls.DetailColumn:SetSizeVal(d,contentHeight)
 Controls.CompactBar:SetHide(not narrow)
 Controls.DistrictColumn:SetOffsetX(narrow and 0 or a+1);Controls.DetailColumn:SetOffsetX(narrow and 0 or a+b+2)
 local g,row=selection()
 Controls.CityColumn:SetHide(narrow and g~=nil)
 Controls.DistrictColumn:SetHide(narrow and (not g or row~=nil))
 Controls.DetailColumn:SetHide(narrow and row==nil)
 Controls.DistrictBack:SetHide(not narrow);Controls.DetailBack:SetHide(not narrow)
 Controls.CityName:SetTruncateWidth(a-36);Controls.Balance:SetWrapWidth(a-36)
 Controls.EmptyCities:SetWrapWidth(a-38);Controls.EmptyDistricts:SetWrapWidth(b-38)
 Controls.DistrictCity:SetTruncateWidth(b-36);Controls.Subject:SetWrapWidth(d-38)
 Controls.QuoteTitle:SetTruncateWidth(d-90)
 for _,name in ipairs({'Quote','Contract','Terms','Help'})do Controls[name]:SetWrapWidth(d-62)end
 Controls.Error:SetWrapWidth(d-24)
 for _,part in ipairs({{'Quote',52},{'Contract',40},{'Terms',40},{'Help',40}})do
  Controls[part[1]..'Card']:SetSizeY(Controls[part[1]]:GetSizeY()+part[2]+14)
 end
 local statusHeight=Controls.Error:GetSizeY()
 local footer=math.max(98,statusHeight+86)+(narrow and 28 or 0)
 Controls.Footer:SetSizeY(footer);Controls.Confirm:SetOffsetY(footer-(narrow and 28 or 0)-72)
 Controls.Refresh:SetOffsetY(footer-(narrow and 28 or 0)-29);Controls.DetailBack:SetOffsetY(footer-29)
 Controls.DetailScroll:SetSizeY(math.max(50,contentHeight-58-footer-8))
 return a,b
end
render=function()
 local c=city();if not c then close();return end
 local b,v=backend();collect(v)
 local g,row=selection();local contract=row and row.contract
 Controls.CityName:SetText(L('SOURCE',Locale.Lookup(c:GetName())))
 Controls.Balance:SetText(L('BALANCE',num(v and v.balance),v and v.used or 0,v and v.workers or 0))
 Controls.EmptyCities:SetText(#groups==0 and (reason(v and v.reason)~='' and reason(v.reason) or L('NO_OPTIONS')) or '')
 Controls.EmptyCities:SetHide(#groups>0)
 Controls.DistrictCity:SetText(g and g.name or L('SELECT_CITY'))
 Controls.EmptyDistricts:SetText(not g and L('SELECT_CITY') or reason(g.reason)~='' and reason(g.reason) or L('NO_DISTRICTS'))
 Controls.EmptyDistricts:SetHide(g and #g.rows>0 or false)
 Controls.Subject:SetText(row and g.name..'[NEWLINE]'..label('Districts',row.domain) or L(g and 'SELECT_DISTRICT' or 'SELECT_CITY'))
 Controls.Quote:SetText(row and row.price and L('QUOTE',label('Buildings',row.building),num(row.price),num(row.cost),row.candidates) or '')
 Controls.QuoteCard:SetHide(not (row and row.price))
 if row and row.building then Controls.QuoteIcon:SetIcon('ICON_'..row.building)end
 Controls.Terms:SetText(row and L('TERMS') or '');Controls.TermsCard:SetHide(not row)
 Controls.Contract:SetText(contract and L('CONTRACT',L('STATE_'..contract.stage),num(contract.cost),num(contract.debited)) or '')
 Controls.ContractCard:SetHide(not contract)
 Controls.Confirm:SetDisabled(not canConfirm(v,row));Controls.Refresh:SetDisabled(pending~=nil);Controls.CompactRefresh:SetDisabled(pending~=nil)
 local message=pending and L('WAITING') or requestError and reason(requestError) or v and v.stage=='HELD' and reason(v.reason)
  or v and v.quoteStale and L('STALE') or row and not row.canSign and not contract and reason(row.reason)
  or v and not v.canSign and reason(v.reason) or #groups==0 and reason(v and v.reason) or ''
 Controls.Error:SetText(message);Controls.Error:SetToolTipString(message)
 local cityWidth,districtWidth=layout()
 cities:ResetInstances();districts:ResetInstances()
 for _,target in ipairs(groups)do
  local key=target.key;local instance=cities:GetInstance();local count=0
  for _,option in ipairs(target.rows)do if option.canSign then count=count+1 end end
  instance.Caption:SetText(target.name);instance.Caption:SetTruncateWidth(cityWidth-90)
  local text=target.reason and reason(target.reason) or L('CITY_OPTIONS',count)
  instance.State:SetText(text);instance.State:SetWrapWidth(cityWidth-64)
  instance.Root:SetSizeY(math.max(74,instance.State:GetSizeY()+54))
  instance.State:SetColorByName(current.target==key and 'Gold' or 'White')
  instance.Root:SetToolTipString(target.name..'[NEWLINE]'..text)
  instance.Root:RegisterCallback(Mouse.eLClick,function()
   if current and not pending then current.target=key;current.domain=nil;requestError=nil;render()end
  end)
 end
 for _,option in ipairs(g and g.rows or {})do
  local domain=option.domain;local instance=districts:GetInstance()
  instance.Icon:SetIcon('ICON_'..domain);instance.Caption:SetText(label('Districts',domain))
  instance.Caption:SetTruncateWidth(districtWidth-105)
  local text=option.canSign and L('DISTRICT_READY',num(option.cost)) or option.contract and L('STATE_'..option.contract.stage) or reason(option.reason)
  instance.State:SetText(text);instance.State:SetWrapWidth(districtWidth-105)
  instance.Root:SetSizeY(math.max(78,instance.State:GetSizeY()+46))
  instance.Caption:SetColorByName(current.domain==domain and 'Gold' or 'White')
  instance.Root:SetToolTipString(label('Districts',domain)..'[NEWLINE]'..text)
  instance.Root:RegisterCallback(Mouse.eLClick,function()
   if current and not pending then current.domain=domain;requestError=nil;render()end
  end)
 end
 for _,name in ipairs({'Cities','CityStack','Districts','DistrictStack','Details'})do Controls[name]:CalculateSize();Controls[name]:ReprocessAnchoring()end
 for _,name in ipairs({'CityScroll','DistrictScroll','DetailScroll'})do Controls[name]:CalculateInternalSize()end
 Controls.Window:ReprocessAnchoring();lastRevision=v and v.revision
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
local function resizeEvent(kind)
 if kind==SystemUpdateUI.ScreenResize and current then render()end
end
local function initialize()
 for _,pair in ipairs({{'Title','TITLE'},{'DistrictTitle','DISTRICTS'},{'DetailTitle','DETAILS'},{'QuoteTitle','QUOTE_TITLE'},{'TermsTitle','EFFECT_TITLE'},
 {'ContractTitle','CONTRACT_TITLE'},{'HelpTitle','RULES_TITLE'},{'ConfirmCaption','CONFIRM'},{'RefreshCaption','REFRESH'},{'Help','HELP'},
 {'DistrictBackCaption','BACK'},{'DetailBackCaption','BACK'},{'CompactCloseCaption','CLOSE'},{'CompactRefreshCaption','REFRESH'}})do Controls[pair[1]]:SetText(L(pair[2]))end
 Controls.Close:SetToolTipString(L('CLOSE'));Controls.Close:RegisterCallback(Mouse.eLClick,close)
 Controls.Confirm:RegisterCallback(Mouse.eLClick,function()send('DEVELOPMENT_CONFIRM')end)
 Controls.Refresh:RegisterCallback(Mouse.eLClick,function()send('DEVELOPMENT_REFRESH')end)
 Controls.CompactRefresh:RegisterCallback(Mouse.eLClick,function()send('DEVELOPMENT_REFRESH')end)
 Controls.CompactClose:RegisterCallback(Mouse.eLClick,close)
 Controls.DistrictBack:RegisterCallback(Mouse.eLClick,function()if current and not pending then current.target=nil;current.domain=nil;render()end end)
 Controls.DetailBack:RegisterCallback(Mouse.eLClick,function()if current and not pending then current.domain=nil;render()end end)
 LuaEvents.SPC_DevelopmentOpen.Add(open);Events.GameCoreEventPublishComplete.Add(publish)
 Events.LoadScreenClose.Add(close);Events.LocalPlayerChanged.Add(close);Events.SystemUpdateUI.Add(resizeEvent)
 ContextPtr:SetInputHandler(function(message,key)if current and message==KeyEvents.KeyUp and key==Keys.VK_ESCAPE then close();return true end;return false end,true)
 close()
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 close();LuaEvents.SPC_DevelopmentOpen.Remove(open);Events.GameCoreEventPublishComplete.Remove(publish)
 Events.LoadScreenClose.Remove(close);Events.LocalPlayerChanged.Remove(close);Events.SystemUpdateUI.Remove(resizeEvent)
end)
