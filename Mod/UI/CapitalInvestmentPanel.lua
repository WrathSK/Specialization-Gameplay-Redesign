include('Probe')
include('CapitalInvestmentUI')
local P=SPCP0;local U=SPCCapitalInvestmentUI
local current,pending,requestError,requestFailure,lastRevision
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
 ExposedMembers.SPC_CapitalUISequence=(ExposedMembers.SPC_CapitalUISequence or 0)+1
 local token='CAPITAL:'..P.VERSION..':'..ExposedMembers.SPC_CapitalUISequence
 local packet={OnStart='SPC_P0_Request',Action=action,CityID=current.city,Domain=current.domain,Mode=mode,
  Revision=v and v.revision or -1,CityToken=v and v.token or '',Token=token}
 pending=token;requestError=nil;requestFailure=nil
 local ok,result=pcall(UI.RequestPlayerOperation,current.owner,PlayerOperations.EXECUTE_SCRIPT,packet)
 if not ok or result==false then pending=nil;requestError='CAPITAL_REQUEST_UNCONFIRMED'end
 render()
end
render=function()
 local c=city();if not c then close();return end
 local b,v=backend();local row
 for _,r in ipairs(v and v.domains or {})do if r.id==current.domain then row=r;break end end
 local contract=v and v.contracts and v.contracts[current.domain]
 Controls.CityName:SetText(Locale.Lookup(c:GetName()))
 Controls.Balance:SetText(L('BALANCE',number(v and v.balance)))
 local domainName=''
 for i,d in ipairs(domains)do
  Controls['Domain'..i..'Caption']:SetText(L(d.name));Controls['Domain'..i]:SetAlpha(current.domain==d.id and 1 or .7)
  if current.domain==d.id then domainName=L(d.name)end
 end
 local q=row and row.quote
 Controls.Subject:SetText(L('SUBJECT',domainName))
 Controls.Source:SetText(q and (q.sSource and L('SOURCE',q.sSourceName,number(q.S)) or L('NO_SOURCE')) or L('WAITING'))
 Controls.Fundamentals:SetText(q and L('FUNDAMENTALS',q.D,q.S,number(q.C),number(q.r*100)) or '')
 Controls.Principal:SetText(q and L('PRINCIPAL',number(q.principal),q.due) or '')
 Controls.Stable:SetText(q and L('STABLE_DETAIL',number(q.safe),number(q.safe-q.principal)) or '')
 Controls.Venture:SetText(q and L('VENTURE_DETAIL',number(q.probability*100),number(q.success),number(q.failure),number(q.expected),number(q.net)) or '')
 Controls.Warning:SetText(q and q.net<0 and L('NEGATIVE_EV') or q and q.net<q.safe-q.principal and L('BELOW_SAFE') or '')
 local text=L('NO_CONTRACT')
 if contract then
  local state={ACTIVE='执行中',SETTLED='已结算',TERMINATED='已终止',HELD='需核对回执',DEBIT_INTENT='确认中',DEBIT_CALLING='需核对扣款',CREDIT_INTENT='到期待结算',CREDIT_CALLING='需核对返还'}
  text=L('CONTRACT',state[contract.stage] or contract.stage,number(contract.principal),contract.due)
  text=text..'[NEWLINE]'..L('LOCKED_TERMS',contract.D,contract.S,number(contract.C),contract.sSourceName or L('SOURCE_NONE'))
  if contract.stage=='SETTLED'then
   if contract.mode=='VENTURE'then text=text..'[NEWLINE]'..L(contract.won and 'RESULT_SUCCESS' or 'RESULT_FAILURE')end
   text=text..'[NEWLINE]'..L('SETTLED',number(contract.paid),number(contract.paid-(contract.debited or contract.principal)))
  elseif contract.stage=='TERMINATED'then text=text..'[NEWLINE]'..L('TERMINATED')end
 end
 Controls.Contract:SetText(text);Controls.Contract:SetToolTipString(text)
 local can=v and v.stage=='READY' and v.canSign and row and row.canSign and pending==nil
 Controls.StableConfirm:SetDisabled(not can);Controls.VentureConfirm:SetDisabled(not can)
 Controls.Refresh:SetDisabled(pending~=nil)
 local errorText=pending and L('REQUEST_WAIT') or v and v.stage=='HELD' and reason(v.reason,v.failure) or requestError and reason(requestError,requestFailure)
  or row and not row.canSign and reason(row.reason) or v and not v.canSign and reason(v.reason) or ''
 Controls.Error:SetText(errorText);Controls.Error:SetToolTipString(errorText)
 lastRevision=v and v.revision
end
local function open(pid,id)
 if pid~=Game.GetLocalPlayer() or not P.IsTestPlayer(pid)then return end
 local c=Players[pid] and Players[pid]:GetCities():FindID(id);if not c or c:GetOwner()~=pid then return end
 current={owner=pid,city=id,reference=U.Reference(pid,c),domain=domains[1].id}
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
local function initialize()
 Controls.Title:SetText(L('TITLE'));Controls.CloseCaption:SetText(L('CLOSE'))
 Controls.StableCaption:SetText(L('CONFIRM_STABLE'));Controls.VentureCaption:SetText(L('CONFIRM_VENTURE'));Controls.RefreshCaption:SetText(L('REFRESH'))
 Controls.Help:SetText(L('HELP'))
 Controls.Close:RegisterCallback(Mouse.eLClick,close)
 Controls.Refresh:RegisterCallback(Mouse.eLClick,function()send('CAPITAL_REFRESH')end)
 Controls.StableConfirm:RegisterCallback(Mouse.eLClick,function()send('CAPITAL_CONFIRM','STABLE')end)
 Controls.VentureConfirm:RegisterCallback(Mouse.eLClick,function()send('CAPITAL_CONFIRM','VENTURE')end)
 for i,d in ipairs(domains)do local id=d.id
  Controls['Domain'..i]:RegisterCallback(Mouse.eLClick,function()if current and not pending then current.domain=id;send('CAPITAL_REFRESH')end end)
 end
 LuaEvents.SPC_CapitalOpen.Add(open);Events.GameCoreEventPublishComplete.Add(publish)
 Events.LoadScreenClose.Add(close);Events.LocalPlayerChanged.Add(close)
 ContextPtr:SetInputHandler(function(message,key)if current and message==KeyEvents.KeyUp and key==Keys.VK_ESCAPE then close();return true end;return false end,true)
 close()
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 close();LuaEvents.SPC_CapitalOpen.Remove(open);Events.GameCoreEventPublishComplete.Remove(publish)
 Events.LoadScreenClose.Remove(close);Events.LocalPlayerChanged.Remove(close)
end)
