include("Probe")
include("SourceYieldProbe")
include("Lv4CopyRead")
include("YieldCarrierProbe")
local P=SPCP0
-- Legacy requests remain isolated: no broad snapshot, district history, or engine-object encoding.
-- B004 adds bounded automatic trader-operation diagnostics at the bottom.
ExposedMembers.SPC_P0={Version=P.VERSION,Stage="INITIALIZED",Events={}}
local shared=ExposedMembers.SPC_P0
local function stage(value)
  shared.Stage=value
  local line="[SPC]["..P.VERSION.."][GAMEPLAY] "..value
  print(line)
  shared.Events[#shared.Events+1]=line
  if #shared.Events>32 then table.remove(shared.Events,1) end
end
local function request(playerID,params)
  if type(params)~="table" or type(params.Token)~="string" or #params.Token>100 then return end
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
    if shared.Lv2Housing then shared.Lv2Housing.Audit() end
    if shared.Lv2GPP then shared.Lv2GPP.Audit() end
    if shared.Lv3Support then shared.Lv3Support.Audit() end
    if shared.Lv3Effects then shared.Lv3Effects.Audit() end
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
    if P.IsTestPlayer(playerID) and shared.Lv2GPP then shared.Lv2GPP.Audit() end
    if P.IsTestPlayer(playerID) and shared.Lv3Support then shared.Lv3Support.Audit() end
    if P.IsTestPlayer(playerID) and shared.Lv3Effects then shared.Lv3Effects.Audit() end
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
    city:SetProperty("SPC_P0_MARKER",params.Token)
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
