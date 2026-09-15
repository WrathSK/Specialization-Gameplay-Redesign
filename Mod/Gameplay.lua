include("Probe")
include("SourceYieldProbe")
include("Lv4CopyRead")
include("YieldCarrierProbe")
local P=SPCP0
-- Legacy requests remain isolated: no broad snapshot, district history, or engine-object encoding.
-- B004 adds bounded automatic trader-operation diagnostics at the bottom.
ExposedMembers.SPC_P0={Version=P.VERSION,Stage="INITIALIZED",Events={}}
local shared=ExposedMembers.SPC_P0
ExposedMembers.SPC_Performance=SPCPerformance.New()
local function stage(value)
  shared.Stage=value
  local line="[SPC]["..P.VERSION.."][GAMEPLAY] "..value
  print(line)
  shared.Events[#shared.Events+1]=line
  if #shared.Events>32 then table.remove(shared.Events,1) end
end
local function request(playerID,params)
  shared.RequestIngress=shared.RequestIngress or {count=0}
  local ingress=shared.RequestIngress;ingress.count=ingress.count+1
  ingress.player=playerID;ingress.shape=type(params)
  ingress.action=type(params)=='table' and P.Scalar(params.Action) or 'NO_TABLE'
  ingress.token=type(params)=='table' and P.Scalar(params.Token) or 'NO_TABLE'
  if type(params)=='table' and params.Action=='DIALOGUE_SAMPLE' then
    shared.DialogueIngress={player=playerID,token=P.Scalar(params.Token),seq=P.Scalar(params.Seq),dataBytes=type(params.Data)=='string' and #params.Data or -1}
  end
  if type(params)~="table" or type(params.Token)~="string" or #params.Token>100 then return end
  -- B068 presentation is a disposable mirror, never a source of city state.
  if params.Action=='NETWORK_REVALIDATE_FAILURE' then
    if P.IsTestPlayer(playerID) and shared.NetworkBridge and params.Epoch==shared.NetworkBridge.epoch then shared.NetworkBridge.CheckEvidence(true) end
    return
  end
  if params.Action=='CITY_PRESENTATION_READ' then
    if not P.IsTestPlayer(playerID) then return end
    local ok,f=pcall(function()
      local c=Players[playerID]:GetCities():FindID(params.CityID)
      assert(c and c:GetOwner()==playerID,'PRESENTATION_CITY_UNAVAILABLE')
      return shared.EffectiveFacts.Read(playerID,c)
    end)
    shared.CityPresentationView={token=params.Token,owner=playerID,cityID=params.CityID,
      specialization=ok and f.specialization or nil,potential=ok and f.potential or nil,
      investments=ok and f.investmentCount or nil,error=not ok and tostring(f) or nil}
    return
  end
  if params.Action=='DIALOGUE_SAMPLE' then
    local ok,err=pcall(shared.Dialogue.Receive,playerID,params)
    if not ok then
      if shared.Dialogue and P.IsTestPlayer(playerID) then shared.Dialogue.errors[playerID]='DIALOGUE_RECEIVE_EXCEPTION: '..tostring(err) end
      print('[SPC][B059][SAMPLE] '..tostring(err))
    end
    return
  end
  if params.Action=='SHADOW_SELECT' or params.Action=='SHADOW_READ' then
    shared.RequestToken=params.Token
    if shared.InheritanceIsolation then
      shared.Snapshot='城市所有权/继承模块已暂停。已有备份保留；不再记录转移或执行恢复。其它专业诊断入口仍可使用。'
      shared.LastToken=params.Token;return
    end
    local ok,out=pcall(function()
      local d=assert(shared.InheritanceShadow,'SHADOW_MODULE_NOT_LOADED')
      if params.Action=='SHADOW_SELECT' then return d.Select(playerID,Players[playerID]:GetCities():FindID(params.CityID)) end
      return shared.CityInheritance and shared.CityInheritance.Describe(playerID) or d.Describe(playerID)
    end)
    shared.Snapshot=ok and out or ('继承备份读取失败：'..tostring(out));shared.LastToken=params.Token;return
  end
  if params.Action=='INHERIT_RECORD' or params.Action=='INHERIT_READ' then
    local ok,out=pcall(function()
      local d=assert(shared.CityInheritanceRead,'INHERIT_MODULE_NOT_LOADED')
      if params.Action=='INHERIT_RECORD' then return d.Record(playerID,Players[playerID]:GetCities():FindID(params.CityID)) end
      return d.Read(playerID)
    end)
    shared.Snapshot=ok and out or ('继承观察未完成：'..tostring(out));shared.LastToken=params.Token;return
  end
  if type(params.Action)=='string' and params.Action:find('^COMMERCE_') then
    shared.RequestToken=params.Token
    local ok,out=pcall(function()
      assert(P.IsTestPlayer(playerID),'CONTROL_OWNER')
      local c=Players[playerID]:GetCities():FindID(params.CityID);assert(c and c:GetOwner()==playerID,'CONTROL_CITY')
      local d=assert(shared.CommerceConvergence,'COMMERCE_MODULE_NOT_LOADED')
      d.Control(playerID,c,params.Action:sub(10));return d.Describe(playerID,c)
    end)
    shared.Snapshot=ok and out or ('商业四读取失败：'..tostring(out));shared.LastToken=params.Token;return
  end
  if params.Action=='GWA_READ' or params.Action=='GWA_OFF' or params.Action=='GWA_AUTO' then
    shared.RequestToken=params.Token
    local ok,out=pcall(function()
      assert(P.IsTestPlayer(playerID),'GWA_NOT_TEST_PLAYER')
      local c=Players[playerID]:GetCities():FindID(params.CityID)
      assert(c and c:GetOwner()==playerID,'GWA_CITY_UNAVAILABLE')
      local d=assert(shared.GreatWorkAdjacency,'GWA_MODULE_NOT_LOADED')
      assert(type(d.Describe)=='function','GWA_MODULE_INCOMPLETE')
      if params.Action~='GWA_READ' then d.off[playerID]=params.Action=='GWA_OFF';d.Audit(playerID) end
      return d.Describe(playerID,c)
    end)
    shared.Snapshot=ok and out or ('巨作相邻请求失败：'..tostring(out))
    shared.LastToken=params.Token
    return
  end
  if params.Action=='GW_READ' or params.Action=='GW_BASELINE' or params.Action=='DIALOGUE_OFF' or params.Action=='DIALOGUE_AUTO' or params.Action=='DIALOGUE_TEST25' or params.Action=='DIALOGUE_TEST50' or params.Action=='DIALOGUE_TEST100' then
    if not P.IsTestPlayer(playerID) then return end
    local c=Players[playerID]:GetCities():FindID(params.CityID);if not c then return end
    if params.Action~='GW_READ' and params.Action~='GW_BASELINE' then
      local percent=({DIALOGUE_TEST25=25,DIALOGUE_TEST50=50,DIALOGUE_TEST100=100})[params.Action]
      shared.Dialogue.test[playerID]=percent and {city=c:GetID(),percent=percent} or nil
      shared.Dialogue.off[playerID]=params.Action=='DIALOGUE_OFF';shared.Dialogue.Audit(playerID) end
    shared.Snapshot=shared.Dialogue.Describe(playerID,c);shared.LastToken=params.Token;return
  end
  if params.Action=='BOOST_INIT' then
    if not P.IsTestPlayer(playerID) then return end
    local ok,err=pcall(function()
      shared.NetworkBoost.EnsureReady(playerID)
      if not shared.GreatWorkProbe.ready then shared.GreatWorkProbe.Clean() end
    end)
    if not ok then print('[SPC][B055][INIT] '..tostring(err)) end
    return
  end
  if params.Action=='BOOST_TEST_ZERO' or params.Action=='BOOST_TEST_HALF' or params.Action=='BOOST_TEST_HIGH' or params.Action=='BOOST_TEST_AUTO' then
    if not P.IsTestPlayer(playerID) then return end
    local raw=({BOOST_TEST_ZERO=0,BOOST_TEST_HALF=1.5,BOOST_TEST_HIGH=3.8})[params.Action]
    local ok,out=pcall(shared.NetworkBoost.Test,playerID,raw)
    shared.Snapshot=ok and out or ('整数实验未启用：'..tostring(out));shared.LastToken=params.Token;return
  end
  if params.Action=='BOOST_READ' or params.Action=='BOOST_BASELINE' then
    if not P.IsTestPlayer(playerID) then return end
    shared.Snapshot=shared.NetworkBoost.Describe(playerID);shared.LastToken=params.Token;return
  end
  if params.Action=='GW_READ' or params.Action=='GW_CITY' or params.Action=='GW_OBJECT' or params.Action=='GW_OFF' then
    if not P.IsTestPlayer(playerID) then return end
    local c=Players[playerID]:GetCities():FindID(params.CityID)
    if not c or c:GetOwner()~=playerID then return end
    local ok,out=pcall(shared.GreatWorkProbe.Run,playerID,c,params.Action)
    if not ok then print('[SPC][B055][GW] '..tostring(out)) end
    shared.Snapshot=ok and out or '巨作实验未完成，请回传报告/日志。';shared.LastToken=params.Token;return
  end
  if params.Action=='DISCOUNT_INIT' then
    if shared.StandardizationDiscount then shared.StandardizationDiscount.Initialize(playerID,params) end
    return
  end
  if params.Action=='DISCOUNT_ELIGIBILITY' then
    if shared.StandardizationDiscount then shared.StandardizationDiscount.Receive(playerID,params) end
    return
  end
  if params.Action=='DISCOUNT_READ' then
    if not P.IsTestPlayer(playerID) then return end
    local c=Players[playerID]:GetCities():FindID(params.CityID)
    if not c or c:GetOwner()~=playerID then return end
    shared.Snapshot=shared.StandardizationDiscount.Describe(playerID,c,params.Page);shared.LastToken=params.Token;return
  end
  if params.Action=='COPY_YIELD_SAMPLE' then
    if shared.CopyYields then shared.CopyYields.Receive(playerID,params) end
    return
  end
  if params.Action=='HALF_ON' or params.Action=='HALF_OFF' or params.Action=='HALF_READ' then
    if not P.IsTestPlayer(playerID) then return end
    local c=Players[playerID]:GetCities():FindID(params.CityID)
    if not c or c:GetOwner()~=playerID then return end
    local ok,result=pcall(shared.HalfYieldProbe.Run,playerID,c,params.Action)
    if not ok then print('[SPC][B050][REQUEST] '..tostring(result)) end
    shared.Snapshot=ok and result or '半点实验未完成，请回传日志。';shared.LastToken=params.Token;return
  end
  if params.Action=='PURCHASE_BASE' or params.Action=='PURCHASE_ON' or params.Action=='PURCHASE_OFF' or params.Action=='PURCHASE_READ' then
    if not P.IsTestPlayer(playerID) then return end
    local c=Players[playerID]:GetCities():FindID(params.CityID)
    if not c or c:GetOwner()~=playerID then return end
    local ok,v=pcall(shared.PurchaseProbe.Run,playerID,c,params.Action)
    shared.Snapshot=ok and v or ('B053实验未完成：'..(tostring(v):match('B053_[A-Z_]+') or 'UNKNOWN'))
    if not ok then print('[SPC][B053] '..tostring(v)) end
    shared.LastToken=params.Token;return
  end
  if params.Action=="STANDARDIZATION_READ" then
    if not P.IsTestPlayer(playerID) then return end
    local c=Players[playerID]:GetCities():FindID(params.CityID)
    if not c or c:GetOwner()~=playerID then return end
    shared.Snapshot=shared.Standardization.Describe(playerID,c,params.Page)
    shared.LastToken=params.Token;return
  end
  if params.Action=="LV4_COPY_READ" then
    if not P.IsTestPlayer(playerID) then return end
    local c=Players[playerID]:GetCities():FindID(params.CityID)
    if not c or c:GetOwner()~=playerID then return end
    shared.Lv4CopyRead=SPCLv4CopyRead.Metadata(P,shared,playerID,c,params.Token)
    shared.Snapshot=shared.CopyYields.Describe(playerID,c);shared.LastToken=params.Token;return
  end
  if params.Action=="LV4_PERCENT_READ" then
    if not P.IsTestPlayer(playerID) then return end
    local c=Players[playerID]:GetCities():FindID(params.CityID)
    if not c or c:GetOwner()~=playerID then return end
    shared.Snapshot=shared.Lv4Percent.Describe(playerID,c);shared.LastToken=params.Token;return
  end
  if params.Action=="UNIT_ACTION_VIEW" then
    if P.IsTestPlayer(playerID) and type(params.UnitID)=="number" and shared.UnitActions then
      shared.UnitActions.ReadView(playerID,params.UnitID,params.Token)
    end
    return
  end
  if params.Action=="UNIT_ACTION_SPAWN" or params.Action=="UNIT_ACTION_PREPARE" or params.Action=="UNIT_ACTION_CONFIRM" then
    if not P.IsTestPlayer(playerID) then return end
    shared.Snapshot=shared.UnitActions.Run(playerID,params);shared.LastToken=params.Token
    if shared.NetworkBridge then shared.NetworkBridge.Refresh(playerID) end
    if shared.Lv2Housing then shared.Lv2Housing.Audit() end
    if shared.Lv2GPP then shared.Lv2GPP.Audit() end
    if shared.Lv3Support then shared.Lv3Support.Audit() end
    if shared.Lv3Effects then shared.Lv3Effects.Audit() end
    if shared.NetworkBoost then shared.NetworkBoost.Audit() end
    if shared.Dialogue then shared.Dialogue.Audit(playerID) end
    return
  end
  if params.Action=="UNIT_TARGETS_READ" then
    if shared.UnitTargets then shared.UnitTargets.Refresh(playerID,params) end
    return
  end
  if params.Action=="INDUSTRY_BASE" then
    if shared.IndustrySupport then shared.IndustrySupport.Receive(playerID,params) end
    return
  end
  if params.Action=="LV2_GPP_DIRTY" then
    if shared.NetworkBridge then shared.NetworkBridge.Refresh(playerID) end
    if P.IsTestPlayer(playerID) and shared.Lv2GPP then shared.Lv2GPP.Audit() end
    if P.IsTestPlayer(playerID) and shared.Lv3Support then shared.Lv3Support.Audit() end
    if P.IsTestPlayer(playerID) and shared.Lv3Effects then shared.Lv3Effects.Audit() end
    if P.IsTestPlayer(playerID) and shared.NetworkBoost then shared.NetworkBoost.Audit() end
    if shared.Dialogue then shared.Dialogue.Audit(playerID) end
    return
  end
  if params.Action=="NETWORK_PUSH" then
    if shared.NetworkBridge then shared.NetworkBridge.Receive(playerID,params) end
    return
  end
  if params.Action~="UNIT_SITE_READ" and params.Action~="CONSTRUCTION_PREVIEW" and params.Action~="CONSTRUCTION_APPLY" and params.Action~="LV2_GPP_READ" and params.Action~="LV2_HOUSING_READ" and params.Action~="INVEST_PREPARE" and params.Action~="INVEST_CONFIRM" and params.Action~="PROGRESSION_READ" and params.Action~="CARRIER_STEP" and params.Action~="CARRIER_OFF" and params.Action~="SOURCE_YIELDS" and params.Action~="NETWORK_DETAIL" and params.Action~="NETWORK_READ" and params.Action~="RESEARCH_ON" and params.Action~="RESEARCH_OFF" and params.Action~="RESEARCH_READ" and params.Action~="CITY_FLOW_READ" and params.Action~="ENVELOPE_READ" and params.Action~="ENVELOPE_NEXT" and params.Action~="CAPTURE" and params.Action~="MARK_CITY" and params.Action~="GOVERNOR" and params.Action~="SPECIALISTS" and params.Action~="TRADE_EVENTS" and params.Action~="STORAGE_READ" and params.Action~="STORAGE_WRITE" and params.Action~="BINDING_READ" and params.Action~="COMPLETION_RECORD_READ" and params.Action~="CITY_JOURNAL_READ" then return end
  if not P.IsTestPlayer(playerID) then return end
  shared.LastToken=nil
  shared.RequestToken=params.Token
  shared.Action=params.Action
  shared.FailureAt=nil
  stage("RECEIVED "..params.Action)
  if params.Action=="STORAGE_READ" or params.Action=="STORAGE_WRITE" then
    shared.Snapshot=shared.StorageProbe.Run(playerID,params.Action=="STORAGE_WRITE")
    shared.LastToken=params.Token;stage("ACK STORAGE");return
  end
  if params.Action=="ENVELOPE_READ" or params.Action=="ENVELOPE_NEXT" then
    shared.Snapshot=shared.EnvelopeProbe.Run(playerID,params.Action,params.ExpectedStage)
    shared.LastToken=params.Token;stage("ACK ENVELOPE");return
  end
  if params.Action=="UNIT_SITE_READ" then
    shared.Snapshot=shared.UnitSiteProbe.Read(playerID,params.UnitID)
    shared.LastToken=params.Token;stage("ACK UNIT_SITE_READ");return
  end
  local player=Players[playerID]
  local city=type(params.CityID)=="number" and player:GetCities():FindID(params.CityID)
  if not city or city:GetOwner()~=playerID then stage("REJECT_CITY");return end
  if params.Action=="CONSTRUCTION_PREVIEW" or params.Action=="CONSTRUCTION_APPLY" then
    shared.Snapshot=params.Action=="CONSTRUCTION_PREVIEW" and shared.ConstructionProbe.Prepare(playerID,city) or shared.ConstructionProbe.Apply(playerID,city)
    shared.LastToken=params.Token;stage("ACK CONSTRUCTION_PROBE");return
  end
  if params.Action=="INVEST_PREPARE" or params.Action=="INVEST_CONFIRM" then
    if params.Action=="INVEST_PREPARE" then
      shared.Snapshot=shared.InvestmentAction.Prepare(playerID,city,params.UnitID,params.Token)
    elseif type(params.PlanToken)=="string" and #params.PlanToken<=400 then
      shared.Snapshot=shared.InvestmentAction.Confirm(playerID,city,params.PlanToken)
    else shared.Snapshot="B033 REJECTED: PREPARE_FIRST" end
    if shared.NetworkBridge then shared.NetworkBridge.Refresh(playerID) end
    if shared.Lv2Housing then shared.Lv2Housing.Audit() end
    if shared.Lv2GPP then shared.Lv2GPP.Audit() end
    if shared.Lv3Support then shared.Lv3Support.Audit() end
    if shared.Lv3Effects then shared.Lv3Effects.Audit() end
    shared.LastToken=params.Token;stage("ACK INVESTMENT");return
  end
  if params.Action=="LV2_GPP_READ" then
    shared.Snapshot=shared.Lv2GPP.Describe(playerID,city)
    shared.LastToken=params.Token;stage("ACK LV2_GPP");return
  end
  if params.Action=="LV2_HOUSING_READ" then
    shared.Snapshot=shared.Lv2Housing.Describe(playerID,city)
    shared.LastToken=params.Token;stage("ACK LV2_HOUSING");return
  end
  if params.Action=="PROGRESSION_READ" then
    shared.Snapshot=shared.EffectiveFacts.Describe(playerID,city)
    shared.LastToken=params.Token;stage("ACK PROGRESSION");return
  end
  if params.Action=="CARRIER_STEP" or params.Action=="CARRIER_OFF" then
    shared.Snapshot=SPCYieldCarrierProbe.Run(playerID,city,params.Action=="CARRIER_STEP" and "STEP" or "OFF")
    shared.LastToken=params.Token;stage("ACK CARRIER");return
  end
  if params.Action=="SOURCE_YIELDS" then
    shared.Snapshot=SPCYieldCarrierProbe.Describe(playerID,city)
    shared.LastToken=params.Token;stage("ACK SOURCE_YIELDS");return
  end
  if params.Action=="NETWORK_READ" or params.Action=="NETWORK_DETAIL" then
    shared.Snapshot=shared.NetworkBridge.Read(playerID,city,params.Action=="NETWORK_DETAIL")
    shared.LastToken=params.Token;stage("ACK NETWORK");return
  end
  if params.Action=="RESEARCH_ON" or params.Action=="RESEARCH_OFF" or params.Action=="RESEARCH_READ" then
    local f=shared.EffectiveFacts.Read(playerID,city)
    if f.specialization=='INDUSTRY' then shared.Snapshot=shared.IndustrySupport.Describe(playerID,city)
    else shared.Snapshot=shared.ResearchSupport.Run(playerID,city,params.Action) end
    if shared.Lv3Support then shared.Snapshot=shared.Snapshot..shared.Lv3Support.Describe(playerID,city) end
    if shared.Lv3Effects then shared.Snapshot=shared.Snapshot..shared.Lv3Effects.Describe(playerID,city) end
    shared.LastToken=params.Token;stage("ACK RESEARCH_SUPPORT");return
  end
  if params.Action=="CITY_FLOW_READ" then
    shared.Snapshot=shared.CityFlowProbe.Read(playerID,city)
    shared.LastToken=params.Token;stage("ACK CITY_FLOW");return
  end
  if params.Action=="CITY_JOURNAL_READ" then
    shared.Snapshot=shared.CityJournalProbe.Read(playerID,city)
    shared.LastToken=params.Token;stage("ACK CITY_JOURNAL");return
  end
  if params.Action=="COMPLETION_RECORD_READ" then
    shared.Snapshot=shared.CompletionRecordProbe.Read(playerID,city)
    shared.LastToken=params.Token;stage("ACK COMPLETION_RECORD");return
  end
  if params.Action=="BINDING_READ" then
    shared.Snapshot=shared.BindingProbe.Read(playerID,city)
    shared.LastToken=params.Token;stage("ACK BINDING");return
  end
  if params.Action=="TRADE_EVENTS" then
    local lines={"GAMEPLAY EVENT OBSERVATION city="..params.CityID,"Events observed since this script loaded; NOT an active-route list"}
    local entries=shared.TradeEvents or {}
    local shown=0
    for i=#entries,1,-1 do
      local e=entries[i]
      if (e.op==playerID and e.oc==params.CityID) or (e.dp==playerID and e.dc==params.CityID) then
        lines[#lines+1]=e.text;shown=shown+1
        if shown>=3 then break end
      end
    end
    if shown==0 then lines[#lines+1]="NO_MATCHING_EVENT_OBSERVED (existing route may predate load)" end
    shared.Snapshot=table.concat(lines,"\n")
    shared.LastToken=params.Token;stage("ACK TRADE_EVENTS");return
  end
  if params.Action=="GOVERNOR" or params.Action=="SPECIALISTS" then
    shared.Snapshot=P.FocusProbe(city,params.Action,stage)
    shared.LastToken=params.Token
    stage("ACK "..params.Action)
    return
  end
  stage("BEFORE_GET city="..tostring(params.CityID))
  local marker=city:GetProperty("SPC_P0_MARKER")
  stage("AFTER_GET marker="..P.Scalar(marker))
  if params.Action=="MARK_CITY" and marker==nil then
    stage("BEFORE_SET")
    P.SetProperty(city,"SPC_P0_MARKER",params.Token)
    stage("AFTER_SET")
    marker=city:GetProperty("SPC_P0_MARKER")
    if marker~=params.Token then stage("ERROR_ROUNDTRIP");return end
  end
  shared.Snapshot="city="..tostring(params.CityID).." marker="..P.Scalar(marker)
  shared.LastToken=params.Token
  stage("ACK "..shared.Snapshot)
end
GameEvents.SPC_P0_Request.Add(function(...)
  local ok,err=pcall(request,...)
  if not ok then shared.FailureAt=shared.Stage;stage("ERROR "..P.Scalar(err)) end
end)
stage("INITIALIZED ISOLATED_PROBES USER_GAME_TEST_REQUIRED")

-- Installed HD Gameplay/Buildings.lua:147 uses these first five parameters.
-- Preserve evidence only; do not infer creation/destruction from activity callbacks.
shared.TradeEvents={}
local function onTradeActivity(actor,op,oc,dp,dc,...)
  if not P.IsTestPlayer(op) and not P.IsTestPlayer(dp) then return end
  local tail={...};local extra={}
  for i=1,math.min(select("#",...),6) do extra[#extra+1]=P.Scalar(tail[i]) end
  local line="turn="..Game.GetCurrentGameTurn().." actor="..P.Scalar(actor).." FROM "..P.Scalar(op)..":"..P.Scalar(oc)
    .." TO "..P.Scalar(dp)..":"..P.Scalar(dc).." extra="..table.concat(extra,",")
  shared.TradeEvents[#shared.TradeEvents+1]={op=op,oc=oc,dp=dp,dc=dc,text=line}
  if #shared.TradeEvents>32 then table.remove(shared.TradeEvents,1) end
  print("[SPC]["..P.VERSION.."][TRADE_EVENT_RAW] "..line)
end
local tradeEvent=P.Field(Events,"TradeRouteActivityChanged")
if tradeEvent and type(tradeEvent.Add)=="function" then
  tradeEvent.Add(function(...)
    local ok,err=pcall(onTradeActivity,...)
    if not ok then print("[SPC][TRADE_EVENT_ERROR] "..P.Scalar(err)) end
  end)
else stage("TRADE_ACTIVITY_EVENT_ABSENT") end

-- B004: automatic, read-only operation candidate diagnostics. No route authority.
include("TradeRouteProbe")
SPCTradeRouteProbe.Start(P,shared)

-- B011 read-only completion lifecycle evidence. No state transitions.
include("CompletionProbe")
SPCCompletionProbe.Start(P,shared)

include("StorageProbe")
SPCStorageProbe.Start(P,shared)

include("BindingProbe")
SPCBindingProbe.Start(P,shared)

include("CompletionRecordProbe")
SPCCompletionRecordProbe.Start(P,shared)

include("CityJournalProbe")
SPCCityJournalProbe.Start(P,shared)

-- B016: automatic read-only qualification evidence; does not replace legacy gates.
include("EligibilityProbe")
SPCEligibilityProbe.Start(P,shared)

include("QualificationProbe")
SPCQualificationProbe.Start(P,shared)

include("EnvelopeProbe")
SPCEnvelopeProbe.Start(P,shared)

include("FreshBindingHook")
include("CityFlowProbe")
SPCCityFlowProbe.Start(P,shared)

include("EffectiveFacts")
SPCEffectiveFacts.Start(P,shared)

include("InvestmentAction")
SPCInvestmentAction.Start(P,shared)

include("ResearchSupport")
SPCResearchSupport.Start(P,shared)
include("Lv2Housing")
SPCLv2Housing.Start(P,shared)
include("Lv2GPP")
SPCLv2GPP.Start(P,shared)

include("NetworkBridge")
SPCNetworkBridge.Start(P,shared)

include("IndustrySupport")
SPCIndustrySupport.Start(P,shared)

include("Lv3Support")
SPCLv3Support.Start(P,shared)

include("Lv3Effects")
SPCLv3Effects.Start(P,shared)

include("ConstructionProbe")
SPCConstructionProbe.Start(P,shared)

include("UnitActionSitePolicy")
include("UnitSiteProbe")
SPCUnitSiteProbe.Start(P,shared)

include("UnitTargets")
SPCUnitTargets.Start(P,shared)

include("UnitActions")
SPCUnitActions.Start(P,shared)

include("CrewProjects")
SPCCrewProjects.Start(P,shared)

include("CrewPrecision")
SPCCrewPrecision.Start(P,shared)

include("Lv4Percent")
SPCLv4Percent.Start(P,shared)

include("HalfYieldProbe")
SPCHalfYieldProbe.Start(P,shared)

include("CopyYields")
SPCCopyYields.Start(P,shared)

include("StandardizationCatalog")
include("Standardization")
SPCStandardization.Start(P,shared)

include("PurchaseProbe")
SPCPurchaseProbe.Start(P,shared)

include("StandardizationDiscount")
SPCStandardizationDiscount.Start(P,shared)

include("NetworkBoost")
SPCNetworkBoost.Start(P,shared)
include("GreatWorkProbe")
SPCGreatWorkProbe.Start(P,shared)

include("Dialogue")
SPCDialogue.Start(P,shared)

include("GreatWorkAdjacency")
SPCGWAdjacency.Start(P,shared)

include("CommerceConvergence")
SPCCommerceConvergence.Start(P,shared)

-- B067: ownership work is isolated for the self-founded-city playable scope.
-- Keep source and saved ledgers intact; no inheritance/backup listeners are installed.
shared.CityInheritanceRead=nil
shared.InheritanceShadow=nil
shared.CityInheritance=nil
shared.OnPermanentCityWrite=nil
shared.InheritanceIsolation=true
