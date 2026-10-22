-- B259: one existing quotation snapshot, three UI-only selection columns.
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
-- Display only: transaction values and native receipts remain untouched.
local function num(v)return type(v)=='number' and string.format('%.0f',v) or '—'end
local function treasury(v)return type(v)=='number' and string.format('%.0f',math.floor(v)) or '—'end
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
  if contract.stage=='ACTIVE' then g.investing=true end
 end
 table.sort(groups,function(a,b)if not not a.investing~=not not b.investing then return a.investing==true end;if a.id==b.id then return a.key<b.key end;return a.id<b.id end)
 for _,g in ipairs(groups)do table.sort(g.rows,function(a,b)return a.domain<b.domain end)end
 for key in pairs(current.iconPages)do if not groupByKey[key]then current.iconPages[key]=nil end end
 -- Keep identity, never list position, across reordered/new/removed quote rows.
 local g=groupByKey[current.target]
 if not g then current.target=nil;current.domain=nil
 elseif not g.byDomain[current.domain]then current.domain=nil end
end
local function layout()
 local width,height=UIManager:GetScreenSizeVal()
 local available=math.max(220,width-16)
 local narrow=available<800
 local column=narrow and math.min(360,available) or math.min(295,math.floor((available-2)/3))
 -- Native ChooserAnim top inset; all column bottoms reach the viewport.
 local h=math.max(240,height-27)
 Controls.Window:SetSizeVal(narrow and column or column*3+2,h)
 local contentHeight=h-(narrow and 40 or 0)
 Controls.CityColumn:SetSizeVal(column,contentHeight)
 local top=narrow and 0 or 148
 local sideHeight=contentHeight-top
 for _,name in ipairs({'DistrictColumn','DetailColumn'})do Controls[name]:SetSizeVal(column,sideHeight);Controls[name]:SetOffsetY(top)end
 Controls.CompactBar:SetHide(not narrow)
 Controls.DistrictColumn:SetOffsetX(narrow and 0 or column+1);Controls.DetailColumn:SetOffsetX(narrow and 0 or column*2+2)
 local g,row=selection()
 Controls.CityColumn:SetHide(narrow and g~=nil)
 Controls.DistrictColumn:SetHide(narrow and (not g or row~=nil))
 Controls.DetailColumn:SetHide(narrow and row==nil)
 Controls.DistrictBack:SetHide(not narrow);Controls.DetailBack:SetHide(not narrow or row==nil)
 Controls.CompactRefresh:SetHide(narrow and row~=nil)
 Controls.DistrictScroll:SetSizeY(sideHeight-(narrow and 102 or 58))
 Controls.CityName:SetTruncateWidth(column-86)
 Controls.Balance:SetTruncateWidth(column-44);Controls.Capacity:SetTruncateWidth(column-44)
 Controls.EmptyCities:SetWrapWidth(column-38);Controls.EmptyDistricts:SetWrapWidth(column-38)
 for _,name in ipairs({'QuoteTitle','TermsTitle','HelpTitle','CurrentTitle'})do Controls[name]:SetTruncateWidth(column-42)end
 for _,name in ipairs({'Quote','Contract','Terms','Help','ContractTitle'})do Controls[name]:SetWrapWidth(column-42)end
 Controls.QuoteBuilding:SetTruncateWidth(column-78)
 Controls.Error:SetWrapWidth(column-44)
 local footer=90
 Controls.Footer:SetSizeY(footer)
 Controls.Confirm:SetSizeVal(math.min(285,column-10),41)
 Controls.Refresh:SetSizeVal(math.min(285,column-10),24)
 -- Measure wrapped text before assigning content heights. Only the overall column scrolls.
 local y=0
 for _,name in ipairs({'Quote','Terms','Help','Current'})do
  local body=name=='Current' and 0 or Controls[name]:GetSizeY()
  if name=='Quote' and not Controls.QuoteBuildingRow:IsHidden() then body=body+46 end
  if name=='Current' then
   body=Controls.ContractTitle:IsHidden() and 0 or Controls.ContractTitle:GetSizeY()
   if not Controls.ContractCard:IsHidden() then body=body+5+Controls.Contract:GetSizeY() else body=0 end
   if not Controls.Error:IsHidden() then body=body+(body>0 and 8 or 0)+Controls.Error:GetSizeY() end
   body=math.max(18,body)
  end
  local cardHeight=body+62
  Controls[name..'Body']:SetSizeY(body)
  Controls[name..'Card']:SetOffsetY(y);Controls[name..'Card']:SetSizeY(cardHeight)
  y=y+cardHeight+12
 end
 Controls.Details:SetSizeY(y-12)
 Controls.DetailScroll:SetSizeY(math.max(40,sideHeight-54-footer-8))
 return column,column
end
render=function()
 local c=city();if not c then close();return end
 local b,v=backend();collect(v)
 local g,row=selection();local contract=row and row.contract
 Controls.CityName:SetText(Locale.Lookup(c:GetName()))
 Controls.Balance:SetText(L('TREASURY',treasury(v and v.balance)))
 Controls.Capacity:SetText(L('CAPACITY',v and v.used or 0,v and v.workers or 0))
 Controls.EmptyCities:SetText(#groups==0 and (reason(v and v.reason)~='' and reason(v.reason) or L('NO_OPTIONS')) or '')
 Controls.EmptyCities:SetHide(#groups>0)
 Controls.EmptyDistricts:SetText(not g and L('SELECT_CITY') or reason(g.reason)~='' and reason(g.reason) or L('NO_DISTRICTS'))
 Controls.EmptyDistricts:SetHide(g and #g.rows>0 or false)
 Controls.Quote:SetText(row and row.price and L('QUOTE_VALUES',num(row.price),num(row.cost),row.candidates) or L(row and 'NO_QUOTE' or g and 'SELECT_DISTRICT' or 'SELECT_CITY'))
 Controls.QuoteBuildingRow:SetHide(not (row and row.price and row.building))
 Controls.QuoteIcon:SetHide(not (row and row.price and row.building))
 Controls.QuoteBuilding:SetText(row and row.building and label('Buildings',row.building) or '')
 if row and row.building then Controls.QuoteIcon:SetIcon('ICON_'..row.building,32);Controls.QuoteIcon:SetSizeVal(32,32)end
 Controls.Terms:SetText(L('TERMS'))
 Controls.Contract:SetText(contract and L('CONTRACT',L('STATE_'..contract.stage),num(contract.cost),num(contract.debited)) or L('NO_CONTRACT'))
 Controls.ContractCard:SetHide(false)
 Controls.ContractTitle:SetHide(not contract)
 Controls.Confirm:SetDisabled(not canConfirm(v,row));Controls.Refresh:SetDisabled(pending~=nil);Controls.CompactRefresh:SetDisabled(pending~=nil)
 local message=pending and L('WAITING') or requestError and reason(requestError) or v and v.stage=='HELD' and reason(v.reason)
  or v and v.quoteStale and L('STALE') or row and not row.canSign and not contract and reason(row.reason)
  or v and not v.canSign and reason(v.reason) or #groups==0 and reason(v and v.reason) or ''
 Controls.Error:SetText(message);Controls.Error:SetToolTipString(message);Controls.Error:SetHide(message=='')
 local cityWidth,districtWidth=layout()
 cities:ResetInstances();districts:ResetInstances()
 for _,target in ipairs(groups)do
  local key=target.key;local instance=cities:GetInstance();local count=0
  for _,option in ipairs(target.rows)do if option.canSign then count=count+1 end end
  instance.Caption:SetText(target.name);instance.Caption:SetTruncateWidth(cityWidth-(target.investing and 160 or 90))
  instance.Investing:SetText(L('INVESTING'));instance.Investing:SetHide(not target.investing)
  local text=target.reason and reason(target.reason) or L('CITY_OPTIONS',count)
  instance.State:SetText(text);instance.State:SetTruncateWidth(cityWidth-78);instance.State:SetHide(#target.rows>0)
  instance.Root:SetSizeY(72);instance.DistrictInfo:SetSizeVal(cityWidth-70,30)
  local slots=math.max(1,math.min(7,math.floor((cityWidth-70)/32)))
  local pages=math.max(1,math.ceil(#target.rows/slots))
  local page=math.min(current.iconPages[key] or 1,pages);current.iconPages[key]=page
  for i=1,7 do
   local icon=instance['DistrictIcon'..i];local option=i<=slots and target.rows[(page-1)*slots+i]
   icon:SetHide(not option)
   if option then
    icon:SetIcon('ICON_'..option.domain)
    icon:SetToolTipString(label('Districts',option.domain)..'[NEWLINE]'..(option.canSign and L('DISTRICT_READY',num(option.cost)) or option.contract and L('STATE_'..option.contract.stage) or reason(option.reason)))
   end
  end
  instance.PreviousIcons:SetHide(pages==1);instance.NextIcons:SetHide(pages==1)
  instance.PreviousIcons:SetDisabled(page==1);instance.NextIcons:SetDisabled(page==pages)
  instance.PreviousIcons:RegisterCallback(Mouse.eLClick,function()if current and not pending and page>1 then current.iconPages[key]=page-1;render()end end)
  instance.NextIcons:RegisterCallback(Mouse.eLClick,function()if current and not pending and page<pages then current.iconPages[key]=page+1;render()end end)
  instance.Root:SetToolTipString(target.name..'[NEWLINE]'..text)
  instance.Root:RegisterCallback(Mouse.eLClick,function()
   if current and not pending then current.target=key;current.domain=nil;requestError=nil;render()end
  end)
 end
 for _,option in ipairs(g and g.rows or {})do
  local domain=option.domain;local instance=districts:GetInstance()
  instance.Icon:SetIcon('ICON_'..domain);instance.Caption:SetText(label('Districts',domain))
  instance.Caption:SetTruncateWidth(districtWidth-112)
  local text=option.canSign and L('DISTRICT_READY',num(option.cost)) or option.contract and L('STATE_'..option.contract.stage) or reason(option.reason)
  instance.State:SetText(text);instance.State:SetWrapWidth(districtWidth-112)
  instance.Root:SetSizeY(math.max(76,instance.State:GetSizeY()+45))
  instance.Caption:SetColorByName(current.domain==domain and 'Gold' or 'White')
  instance.Root:SetToolTipString(label('Districts',domain)..'[NEWLINE]'..text)
  instance.Root:RegisterCallback(Mouse.eLClick,function()
   if current and not pending then current.domain=domain;requestError=nil;render()end
  end)
 end
 for _,name in ipairs({'Cities','CityStack','Districts','DistrictStack','ContractCard','QuoteContent','TermsContent','HelpContent','CurrentContent'})do Controls[name]:CalculateSize();Controls[name]:ReprocessAnchoring()end
 for _,name in ipairs({'CityScroll','DistrictScroll','DetailScroll'})do Controls[name]:CalculateInternalSize()end
 Controls.Window:ReprocessAnchoring();lastRevision=v and v.revision
end
local function open(pid,id)
 if pid~=Game.GetLocalPlayer() or not P.IsTestPlayer(pid)then return end
 local c=Players[pid] and Players[pid]:GetCities():FindID(id);if not c then return end
 current={owner=pid,city=id,reference=U.Reference(pid,c),iconPages={}};pending=nil;requestError=nil;lastRevision=nil
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
 {'CurrentTitle','CURRENT_TITLE'},{'ContractTitle','CONTRACT_TITLE'},{'HelpTitle','RULES_TITLE'},{'ConfirmCaption','CONFIRM'},{'RefreshCaption','REFRESH'},{'Help','HELP'},
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
 ContextPtr:SetInputHandler(function(message,key)
  if type(message)=='table' or type(message)=='userdata'then key=message:GetKey();message=message:GetMessageType()end
  if current and key==Keys.VK_ESCAPE then
   if message==KeyEvents.KeyUp then close()end
   return true
  end
  return false
 end,true)
 close()
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 close();LuaEvents.SPC_DevelopmentOpen.Remove(open);Events.GameCoreEventPublishComplete.Remove(publish)
 Events.LoadScreenClose.Remove(close);Events.LocalPlayerChanged.Remove(close);Events.SystemUpdateUI.Remove(resizeEvent)
end)
