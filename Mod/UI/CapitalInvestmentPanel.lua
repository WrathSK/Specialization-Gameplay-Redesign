include('Probe')
include('CapitalInvestmentUI')
include('InstanceManager')
local P=SPCP0;local U=SPCCapitalInvestmentUI
local current,pending,requestError,requestFailure,lastRevision
local domainRows=InstanceManager:new('CapitalDomain','Root',Controls.Domains)
local modeRows=InstanceManager:new('CapitalMode','Root',Controls.Modes)
local domains={{id='DISTRICT_CAMPUS',name='RESEARCH'},{id='DISTRICT_THEATER',name='CULTURE'},{id='DISTRICT_INDUSTRIAL_ZONE',name='INDUSTRY'}}
local function L(k,...)return Locale.Lookup('LOC_SPC_CAPITAL_'..k,...)end
local function number(n)
 if type(n)~='number'then return '—'end
 return string.format('%.6f',n):gsub('0+$',''):gsub('%.$','')
end
local function reason(k,detail)
 local phases={DEBIT_INTENT_WRITE='PAUSE_INTENT',DEBIT_CALLING_WRITE='PAUSE_CALLING',NATIVE_DEBIT='PAUSE_DEBIT',
  CONTRACT_ACTIVATE='PAUSE_RECEIPT',ACTIVE_RECEIPT_WRITE='PAUSE_RECEIPT',CREDIT_INTENT_WRITE='PAUSE_CREDIT',
  CREDIT_CALLING_WRITE='PAUSE_CREDIT',NATIVE_CREDIT='PAUSE_CREDIT',SETTLED_RECEIPT_WRITE='PAUSE_CREDIT'}
 if detail and phases[detail.phase]then return L(phases[detail.phase])end
 if k and (k:match('^STORE_') or k:match('^PROGRESSION_') or k:match('^EVIDENCE_') or k=='CAPITAL_STATE_UNKNOWN')then return L('PAUSE_STATE')end
 local names={CAPITAL_DOMAIN_OCCUPIED='该领域已有未结算合同',CAPITAL_ACTIVE_III_REQUIRED='签约需要商业 ACTIVE III',
  CAPITAL_NETWORK_PENDING='等待商路网络核验',CAPITAL_ATTAINMENT_HISTORY_UNKNOWN='同级来源缺少可靠机构建立时间',
  CAPITAL_COMMERCE_PENDING='等待商业状态更新',CAPITAL_QUOTE_STALE='报价已变化，请核对新报价后再次确认',
  CAPITAL_MONEY_UNCONFIRMED='金币实际变化与请求不符，已停止重复操作；请交回日志',
  CAPITAL_NATIVE_OUTCOME_UNKNOWN='金币回执尚未确认；合同已暂停',CAPITAL_TREASURY_EMPTY='当前没有可投入金币',
  CAPITAL_SOURCE_UNKNOWN='专业来源暂不可确认',CAPITAL_REFERENCE_UNAVAILABLE='城市归属暂不可确认',
  CAPITAL_TREASURY_UNAVAILABLE='国库暂不可读取',CAPITAL_STANDARD_SPEED_ONLY='本版资本投资仅支持标准速度'}
 return names[k] or (k and L('ERROR',k) or L('WAITING'))
end
local function backend()
 local b=U.Backend();return b,b and current and b.views[current.owner..':'..current.city]
end
local function city()
 if not current or current.owner~=Game.GetLocalPlayer()then return end
 local c=Players[current.owner] and Players[current.owner]:GetCities():FindID(current.city)
 if c and c:GetOwner()==current.owner and U.Reference(current.owner,c)==current.reference then return c end
end
local function close()
 current=nil;pending=nil;requestError=nil;requestFailure=nil;lastRevision=nil
 Controls.Window:SetHide(true);ContextPtr:SetHide(true)
end
local render
local function send(action,mode)
 if not current or pending then return end
 local b,v=backend();if not city()then close();return end
 if action=='CAPITAL_CONFIRM' then
  local row;for _,r in ipairs(v and v.domains or {})do if r.id==current.domain then row=r;break end end
  if not (v and v.stage=='READY' and v.canSign and row and row.canSign and row.quote and (mode=='STABLE' or mode=='VENTURE'))then render();return end
 end
 ExposedMembers.SPC_CapitalUISequence=(ExposedMembers.SPC_CapitalUISequence or 0)+1
 local token='CAPITAL:'..P.VERSION..':'..ExposedMembers.SPC_CapitalUISequence
 local packet={OnStart='SPC_P0_Request',Action=action,CityID=current.city,Domain=current.domain,Mode=mode,
  Revision=v and v.revision or -1,CityToken=v and v.token or '',Token=token}
 pending=token;requestError=nil;requestFailure=nil
 local ok,result=pcall(UI.RequestPlayerOperation,current.owner,PlayerOperations.EXECUTE_SCRIPT,packet)
 if not ok or result==false then pending=nil;requestError='CAPITAL_REQUEST_UNCONFIRMED'end
 render()
end
local function layout()
 local width,height=UIManager:GetScreenSizeVal();local narrow=width-16<800
 local column=narrow and math.min(360,math.max(220,width-16)) or 295
 local h=math.max(240,height-27);local body=h-(narrow and 40 or 0);local top=narrow and 0 or 148
 Controls.Window:SetSizeVal(narrow and column or column*3+2,h)
 Controls.DomainColumn:SetSizeVal(column,body)
 for _,name in ipairs({'ModeColumn','DetailColumn'})do Controls[name]:SetSizeVal(column,body-top);Controls[name]:SetOffsetY(top)end
 Controls.ModeColumn:SetOffsetX(narrow and 0 or column+1);Controls.DetailColumn:SetOffsetX(narrow and 0 or column*2+2)
 Controls.DomainColumn:SetHide(narrow and current.domain~=nil)
 Controls.ModeColumn:SetHide(not current.domain or (narrow and current.mode~=nil))
 Controls.DetailColumn:SetHide(not current.mode)
 Controls.CompactBar:SetHide(not narrow);Controls.Back:SetHide(not current.domain)
 Controls.CityName:SetTruncateWidth(column-68);Controls.Balance:SetTruncateWidth(column-44)
 Controls.Confirm:SetSizeVal(math.min(285,column-10),41);Controls.Refresh:SetSizeVal(math.min(285,column-10),24)
 local y=0
 for _,name in ipairs({'Quote','Returns','Basis','Current'})do
  Controls[name..'Title']:SetTruncateWidth(column-42);Controls[name]:SetWrapWidth(column-44)
  local height=Controls[name]:GetSizeY();Controls[name..'Body']:SetSizeY(height);Controls[name..'Card']:SetOffsetY(y);Controls[name..'Card']:SetSizeY(height+62);y=y+height+74
 end
 Controls.Details:SetSizeY(y-12);Controls.DetailScroll:SetSizeY(math.max(40,body-top-54-90-8))
 return column
end
render=function()
 local c=city();if not c then close();return end
 local b,v=backend();local row;local byID={}
 for _,r in ipairs(v and v.domains or {})do byID[r.id]=r;if r.id==current.domain then row=r end end
 if current.domain and not row then current.domain=nil;current.mode=nil end
 local contract=v and v.contracts and v.contracts[current.domain]
 Controls.CityName:SetText(Locale.Lookup(c:GetName()))
 Controls.Balance:SetText(L('BALANCE',v and type(v.balance)=='number' and string.format('%.0f',math.floor(v.balance)) or '—'))
 local q=row and row.quote
 Controls.Quote:SetText(q and L('PRINCIPAL',number(q.principal),q.due) or L('WAITING'))
 local returns=q and (current.mode=='STABLE' and L('STABLE_DETAIL',number(q.safe),number(q.safe-q.principal)) or L('VENTURE_DETAIL',number(q.probability*100),number(q.success),number(q.failure),number(q.expected),number(q.net))) or L('WAITING')
 if q and current.mode=='VENTURE' then
  if q.net<0 then returns=returns..'[NEWLINE][NEWLINE]'..L('NEGATIVE_EV')
  elseif q.net<q.safe-q.principal then returns=returns..'[NEWLINE][NEWLINE]'..L('BELOW_SAFE')end
 end
 Controls.Returns:SetText(returns)
 Controls.Basis:SetText(q and (L('FUNDAMENTALS',q.D,q.S,number(q.C),number(q.r*100))..'[NEWLINE]'..(q.sSource and L('SOURCE',q.sSourceName,number(q.S)) or L('NO_SOURCE'))..'[NEWLINE][NEWLINE]'..L('HELP')) or L('WAITING'))
 local text=L('NO_CONTRACT')
 if contract then
  local states={ACTIVE='执行中',SETTLED='已结算',TERMINATED='已终止',HELD='需核对回执',DEBIT_INTENT='确认中',DEBIT_CALLING='需核对扣款',CREDIT_INTENT='到期待结算',CREDIT_CALLING='需核对返还'}
  text=L('CONTRACT_MODE',L(contract.mode=='STABLE' and 'MODE_STABLE' or 'MODE_VENTURE'))..'[NEWLINE]'..L('CONTRACT',states[contract.stage] or contract.stage,number(contract.principal),contract.due)
  text=text..'[NEWLINE]'..L('ACTUAL_DEBIT',number(contract.debited))..'[NEWLINE]'..L('LOCKED_TERMS',contract.D,contract.S,number(contract.C),contract.sSourceName or L('SOURCE_NONE'))
  if contract.stage=='SETTLED' then
   if contract.mode=='VENTURE' then text=text..'[NEWLINE]'..L(contract.won and 'RESULT_SUCCESS' or 'RESULT_FAILURE')end
   text=text..'[NEWLINE]'..L('SETTLED',number(contract.paid),number(contract.paid-(contract.debited or contract.principal)))
  elseif contract.stage=='TERMINATED' then text=text..'[NEWLINE]'..L('TERMINATED')end
 end
 local message=pending and L('REQUEST_WAIT') or v and v.stage=='HELD' and reason(v.reason,v.failure) or requestError and reason(requestError,requestFailure)
  or row and not row.canSign and reason(row.reason) or v and not v.canSign and reason(v.reason) or ''
 Controls.Current:SetText(text..(message~='' and '[NEWLINE][NEWLINE]'..message or ''))
 Controls.ConfirmCaption:SetText(L(current.mode=='VENTURE' and 'CONFIRM_VENTURE' or 'CONFIRM_STABLE'))
 Controls.Confirm:SetDisabled(not(v and v.stage=='READY' and v.canSign and row and row.canSign and q and current.mode and not pending))
 Controls.Refresh:SetDisabled(pending~=nil)
 local column=layout();domainRows:ResetInstances();modeRows:ResetInstances()
 for _,d in ipairs(domains)do
  local id=d.id;local item=domainRows:GetInstance();local dr=byID[id];local ct=v and v.contracts and v.contracts[id]
  local open=ct and ct.stage~='SETTLED' and ct.stage~='TERMINATED'
  item.Icon:SetIcon('ICON_'..id);item.Caption:SetText(L(d.name));item.Caption:SetTruncateWidth(column-96)
  item.Marker:SetText(open and L(ct.stage=='ACTIVE' and 'INVESTING' or 'CONTRACT_PENDING') or '');item.Marker:SetHide(not open)
  item.State:SetText(dr and (dr.canSign and L('AVAILABLE') or reason(dr.reason)) or L('WAITING'));item.State:SetWrapWidth(column-96)
  item.Root:SetSizeY(math.max(100,item.State:GetSizeY()+76));item.Caption:SetColorByName(current.domain==id and 'Gold' or 'White')
  item.Root:RegisterCallback(Mouse.eLClick,function()if current and not pending then current.domain=id;current.mode=nil;send('CAPITAL_REFRESH')end end)
 end
 if current.domain then for _,mode in ipairs({'STABLE','VENTURE'})do
  local chosen=mode;local item=modeRows:GetInstance();item.Caption:SetText(L('MODE_'..mode));item.Caption:SetTruncateWidth(column-40)
  item.State:SetText(q and (mode=='STABLE' and L('STABLE_BRIEF',number(q.safe)) or L('VENTURE_BRIEF',number(q.probability*100),number(q.success),number(q.failure))) or L(mode=='STABLE' and 'STABLE_SUMMARY' or 'VENTURE_SUMMARY'));item.State:SetWrapWidth(column-40)
  item.Root:SetSizeY(item.State:GetSizeY()+48);item.Caption:SetColorByName(current.mode==mode and 'Gold' or 'White')
  item.Root:RegisterCallback(Mouse.eLClick,function()if current and not pending then current.mode=chosen;render()end end)
 end end
 for _,name in ipairs({'Domains','Modes'})do Controls[name]:CalculateSize();Controls[name]:ReprocessAnchoring()end
 for _,name in ipairs({'DomainScroll','ModeScroll','DetailScroll'})do Controls[name]:CalculateInternalSize()end
 Controls.Window:ReprocessAnchoring();lastRevision=v and v.revision
end
local function open(pid,id)
 if pid~=Game.GetLocalPlayer() or not P.IsTestPlayer(pid)then return end
 local c=Players[pid] and Players[pid]:GetCities():FindID(id);if not c or c:GetOwner()~=pid then return end
 current={owner=pid,city=id,reference=U.Reference(pid,c)}
 pending=nil;requestError=nil;requestFailure=nil;lastRevision=nil
 ContextPtr:SetHide(false);Controls.Window:SetHide(false);send('CAPITAL_OPEN')
end
local function publish()
 if not current then return end
 if not city()then close();return end
 local b,v=backend();local ack=b and b.lastRequest
 local answered=pending and ack and ack.token==pending and ack.owner==current.owner and ack.city==current.city
 if answered then pending=nil;requestError=not ack.accepted and ack.reason or nil;requestFailure=ack.failure end
 if answered or not v or v.revision~=lastRevision then render()end
end
local function resizeEvent(kind)if current and kind==SystemUpdateUI.ScreenResize then render()end end
local function initialize()
 for _,pair in ipairs({{'Title','TITLE'},{'ModeTitle','MODE_TITLE'},{'DetailTitle','DETAIL_TITLE'},{'QuoteTitle','QUOTE_TITLE'},{'ReturnsTitle','RETURNS_TITLE'},{'BasisTitle','BASIS_TITLE'},{'CurrentTitle','CURRENT_TITLE'},{'RefreshCaption','REFRESH'},{'BackCaption','BACK'},{'CompactCloseCaption','CLOSE'}})do Controls[pair[1]]:SetText(L(pair[2]))end
 Controls.Close:RegisterCallback(Mouse.eLClick,close);Controls.CompactClose:RegisterCallback(Mouse.eLClick,close)
 Controls.Refresh:RegisterCallback(Mouse.eLClick,function()send('CAPITAL_REFRESH')end)
 Controls.Confirm:RegisterCallback(Mouse.eLClick,function()if current then send('CAPITAL_CONFIRM',current.mode)end end)
 Controls.Back:RegisterCallback(Mouse.eLClick,function()if current and not pending then if current.mode then current.mode=nil else current.domain=nil end;render()end end)
 LuaEvents.SPC_CapitalOpen.Add(open);Events.GameCoreEventPublishComplete.Add(publish)
 Events.LoadScreenClose.Add(close);Events.LocalPlayerChanged.Add(close)
 Events.SystemUpdateUI.Add(resizeEvent)
 ContextPtr:SetInputHandler(function(message,key)
  if type(message)=='table' or type(message)=='userdata'then key=message:GetKey();message=message:GetMessageType()end
  if current and key==Keys.VK_ESCAPE then if message==KeyEvents.KeyUp then close()end;return true end
  return false
 end,true)
 close()
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 close();LuaEvents.SPC_CapitalOpen.Remove(open);Events.GameCoreEventPublishComplete.Remove(publish)
 Events.LoadScreenClose.Remove(close);Events.LocalPlayerChanged.Remove(close);Events.SystemUpdateUI.Remove(resizeEvent)
end)
