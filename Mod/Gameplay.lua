include("Probe")
include("SafeCallbacks")
include("RuntimeComposition")
include("SourceYieldProbe")
include("Lv4CopyRead")
include("YieldCarrierProbe")
local P=SPCP0
-- Legacy requests remain isolated: no broad snapshot, district history, or engine-object encoding.
-- B004 adds bounded automatic trader-operation diagnostics at the bottom.
ExposedMembers.SPC_P0={Version=P.VERSION,Stage="STARTING",Events={}}
local shared=ExposedMembers.SPC_P0
local composition=SPCRuntimeComposition.New(shared)
-- Diagnostic observers are protected and never control startup or reconciliation.
local readiness
pcall(function()include('ExpeditionTrainingDiagnostics');include('ReadinessSummary');readiness=SPCReadinessSummary.Start(P,shared)end)
ExposedMembers.SPC_Performance=SPCPerformance.New()
local function stage(value)
  shared.Stage=value
  local line="[SPC]["..P.VERSION.."][GAMEPLAY] "..value
  print(line)
  shared.Events[#shared.Events+1]=line
  if #shared.Events>32 then table.remove(shared.Events,1) end
end
-- Request-caused dirty notification; committed receipts are revalidated by the real action.
local function refreshInvestmentSupport(playerID,result)
 if not shared.FactChanges then return end
 local committed=type(result)=='table' and result.cause=='INVESTMENT_COMMITTED' and (result.status=='COMMITTED' or result.status=='ALREADY_COMMITTED')
 local reference=committed and result.reference
 local event={owner=playerID,cityID=committed and result.city or nil,
  reference=reference and table.concat({reference.owner,reference.cityID,reference.x,reference.y,result.anchor.token},':') or nil,
  kinds=committed and {'POTENTIAL','ACTIVE'} or {'ACTIVE','D','WORKERS'},
  cause=committed and (result.status=='COMMITTED' and 'INVESTMENT_COMMITTED' or 'INVESTMENT_RECOVERY') or 'REQUEST_FACTS_DIRTY',
  revision=committed and result.revision or nil,investment=committed and result.status=='COMMITTED' and result or nil}
 shared.FactChanges.Emit(event)
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
  -- Return a bounded diagnostic failure instead of silently dropping an eligible UI's request.
  local eligible,eligibilityReason=P.IsTestPlayer(playerID)
  if not eligible then
    shared.RequestToken=params.Token
    shared.FailureAt="PLAYER_ELIGIBILITY"
    shared.Stage="ERROR 玩家资格检查未通过："..tostring(eligibilityReason)
    return
  end
  if type(params.Action)=='string' and params.Action:match('^REST_') then
    if shared.Restructuring then shared.Restructuring.Request(playerID,params)end;return
  end
  if params.Action=='NETWORK_ISOLATE' or params.Action=='NETWORK_ISOLATION_READ' then
    local ok,out=pcall(function()
      if params.Action=='NETWORK_ISOLATE' then return shared.NetworkIsolation.Begin(playerID,params.Epoch) end
      return shared.NetworkIsolation.Read(playerID)
    end)
    shared.Snapshot=ok and out or ('Network隔离未就绪；停止对照并冷启动原存档：'..P.Scalar(out));shared.LastToken=params.Token;return
  end
  if params.Action=='MEMORY_GC_READ' or params.Action=='MEMORY_GC_COLLECT' or params.Action=='MEMORY_GC_AUTO_ON' or params.Action=='MEMORY_GC_AUTO_OFF' then
    local ok,out=pcall(function()
      local d=shared.MemoryObservation;assert(d,'GC diagnostic not initialized')
      if params.Action=='MEMORY_GC_COLLECT' then return d.CollectGC(playerID,params.Token) end
      if params.Action=='MEMORY_GC_AUTO_ON' or params.Action=='MEMORY_GC_AUTO_OFF' then return d.SetAutoGC(playerID,params.Action=='MEMORY_GC_AUTO_ON',params.Token) end
      return d.ReadGC(playerID)
    end)
    shared.Snapshot=ok and out or ('GC诊断不可用；停止本次测试：'..P.Scalar(out));shared.LastToken=params.Token;return
  end
  if params.Action=='EVENT_ORDER_TOGGLE' then
    local ok,out=pcall(function()
      if not shared.EventTiming then return 'B271时序探针已停用。'end
      return shared.EventTiming.Toggle(playerID)
    end)
    shared.Snapshot=ok and out or '事件诊断不可用';shared.LastToken=params.Token;return
  end
  if params.Action=='MEMORY_BEGIN' or params.Action=='MEMORY_READ' then
    local ok,out=pcall(shared.MemoryObservation.Read,playerID,params.Action=='MEMORY_BEGIN')
    shared.Snapshot=ok and out or ('内存观测不可用：'..tostring(out));shared.LastToken=params.Token;return
  end
  if params.Action=='ENGINEERING_STUDY_BEGIN' or params.Action=='ENGINEERING_STUDY_SYNC' then
    local d=shared.EngineeringStudy
    if d and not d.startupError then
      if params.Action=='ENGINEERING_STUDY_SYNC'then d.Sync(playerID,params.CityID,params.Token)else d.Request(playerID,params)end
    end;return
  end
  if params.Action=='DIALOGUE_CARRIER_NEXT' and shared.DialogueEffects then
    params.Action='DIALOGUE_PROJECT_READ' -- stale UI cannot re-enable the retired test writer
  end
  if params.Action=='DIALOGUE_CARRIER_NEXT' then
    local ok,out=pcall(function()
      local c=assert(Players[playerID]:GetCities():FindID(params.CityID),'请选择己方城市')
      shared.Dialogue.CarrierTestNext(playerID,c,params.Token,params.Reference)
      return shared.Dialogue.DescribeCarrierTest(playerID,c)
    end)
    shared.Snapshot=ok and out or ('倍率对照暂停：'..tostring(out)..'；回到原测试城市右键结束。');shared.LastToken=params.Token;return
  end
  if params.Action=='DIALOGUE_PROJECT_BEGIN' or params.Action=='DIALOGUE_PROJECT_SYNC' or params.Action=='DIALOGUE_PROJECT_READ' then
    local ok,out=pcall(function()
      local d=assert(shared.DialogueProjects,'时代对话未初始化');assert(not d.startupError,d.startupError)
      if params.Action=='DIALOGUE_PROJECT_SYNC' then d.Sync(playerID,params.CityID,params.Token);return end
      if params.Action=='DIALOGUE_PROJECT_BEGIN' then d.Request(playerID,params);return end
      local c=assert(Players[playerID]:GetCities():FindID(params.CityID),'请选择己方城市')
      return d.Describe(playerID,c)..(shared.DialogueEffects and '' or '\n\n'..shared.Dialogue.DescribeCarrierTest(playerID,c))
    end)
    if params.Action=='DIALOGUE_PROJECT_READ' then shared.Snapshot=ok and out or ('时代对话暂停：'..tostring(out));shared.LastToken=params.Token end
    return
  end
  if params.Action=='CLAIM_BEGIN' or params.Action=='CLAIM_SYNC' then
    local claim=shared.ClaimProjects
    if claim and not claim.startupError then
      if params.Action=='CLAIM_SYNC' then claim.Sync(playerID,params.CityID,params.Token) else claim.Request(playerID,params) end
    end
    return
  end
  if params.Action=='TIMED_PROJECT_BEGIN' or params.Action=='TIMED_PROJECT_CANCEL' then
    shared.TimedProject.Request(playerID,params);return
  end
  if params.Action=='PROJECT_TURN_BEGIN' or params.Action=='PROJECT_TURN_END' then
    shared.ProjectTurnObservation.Request(playerID,params);return
  end
  if params.Action=='OVERFLOW_PREPARE' or params.Action=='OVERFLOW_APPLY' then
    shared.OverflowStorageProbe.Request(playerID,params);return
  end
  if params.Action=='TIMED_PRODUCTION_BEGIN' or params.Action=='TIMED_PRODUCTION_CANCEL' then
    shared.TimedProductionProbe.Request(playerID,params);return
  end
  if params.Action=='CITY_SEQUENCE_BEGIN' or params.Action=='CITY_SEQUENCE_READ' then
    local ok,out=pcall(function()
      if params.Action=='CITY_SEQUENCE_READ' then return shared.CitySequenceProbe.Read(playerID,params.Page)end
      local player=Players[playerID]
      local c=params.CityID and player:GetCities():FindID(params.CityID)
      local u=params.UnitID and player:GetUnits():FindID(params.UnitID)
      assert(not params.UnitID or u,'SELECTED_UNIT_UNAVAILABLE')
      return shared.CitySequenceProbe.Begin(playerID,c,u,params.Token)
    end)
    shared.Snapshot=ok and out or '事件观察读取失败；没有修改专业记录。'
    shared.LastToken=params.Token;return
  end
  -- B068 presentation is a disposable mirror, never a source of city state.
  if params.Action=='PROGRESSION_IMPORT' or params.Action=='PROGRESSION_STORE_READ' then
    if not P.IsTestPlayer(playerID) then return end
    local ok,out=pcall(function()
      local c=params.CityID and Players[playerID]:GetCities():FindID(params.CityID)
      if params.Action=='PROGRESSION_IMPORT' then return shared.CityProgressionStore.Import(playerID,c) end
      return (shared.CityProgressionStore.NativeDescribe or shared.CityProgressionStore.Describe)(playerID,c)
    end)
    shared.Snapshot=ok and out or ('进度保存暂停：'..tostring(out));shared.LastToken=params.Token;return
  end
  if params.Action=='IDENTITY_EXPERIMENT_BEGIN' or params.Action=='IDENTITY_EXPERIMENT_READ' then
    if not P.IsTestPlayer(playerID) then return end
    local ok,out=pcall(function()
      if params.Action=='IDENTITY_EXPERIMENT_BEGIN' then return shared.CityIdentityExperiment.Begin(playerID,Players[playerID]:GetCities():FindID(params.CityID)) end
      return shared.CityIdentityExperiment.Describe(playerID)
    end)
    shared.Snapshot=ok and out or '实验读取失败；未迁移任何专业记录。';shared.LastToken=params.Token;return
  end
  if params.Action=='IDENTITY_RECORD' or params.Action=='IDENTITY_COMPARE' or params.Action=='IDENTITY_DETAIL' then
    if not P.IsTestPlayer(playerID) then return end
    local ok,out=pcall(function()
      if params.Action=='IDENTITY_RECORD' then
        local c=Players[playerID]:GetCities():FindID(params.CityID)
        return shared.CityIdentityRead.Record(playerID,c)
      end
      return shared.CityIdentityRead.Describe(playerID,params.Action=='IDENTITY_DETAIL')
    end)
    shared.Snapshot=ok and out or '城市身份：读取未完成；请选择己方城市。未执行迁移。'
    shared.LastToken=params.Token;return
  end
  if params.Action=='NETWORK_REVALIDATE_FAILURE' then
    if P.IsTestPlayer(playerID) and shared.NetworkBridge and params.Epoch==shared.NetworkBridge.epoch then shared.NetworkBridge.CheckEvidence(true) end
    return
  end
  if params.Action=='CULTURE_INSIGHTS_READ' then
    local ok,text=pcall(function()
      local c=params.CityID and Players[playerID]:GetCities():FindID(params.CityID)
      local report=P.DescribeCultureInsights(playerID,c,shared.CityProgressionStore)
      if shared.CultureInsightsTourism and c then report=report..'\n'..shared.CultureInsightsTourism.Describe(playerID,c)end
      if shared.CultureNetwork and c then report=report..'\n'..shared.CultureNetwork.Describe(playerID,c)end
      return report
    end)
    if not ok then print('[SPC][B191][N1_INSIGHT] status=UNKNOWN') end
    shared.Snapshot=ok and text or '文化见闻暂不可读（UNKNOWN）；请重新选择己方城市。'
    shared.LastToken=params.Token;return
  end
  if params.Action=='RESEARCH_TRADITION_READ' then
    if not P.IsTestPlayer(playerID) then return end
    local ok,text=pcall(function()
      local c=assert(Players[playerID]:GetCities():FindID(params.CityID),'TRADITION_CITY_UNKNOWN')
      return shared.ResearchTradition.Describe(playerID,c)
    end)
    shared.Snapshot=ok and text or '学术传统：城市暂不可读';shared.LastToken=params.Token;return
  end
  if params.Action=='RESEARCH_CHAIR_READ' or params.Action=='RESEARCH_CHAIR_DETAIL' then
    if not P.IsTestPlayer(playerID) then return end
    local ok,text=pcall(function()
      local c=assert(Players[playerID]:GetCities():FindID(params.CityID),'CHAIR_CITY_UNKNOWN')
      return shared.ResearchChair.Describe(playerID,c,params.Action=='RESEARCH_CHAIR_DETAIL')
    end)
    shared.Snapshot=ok and text or '学术主持：城市暂不可读';shared.LastToken=params.Token;return
  end
  if params.Action=='RESEARCH_APPLY_READ' or params.Action=='RESEARCH_APPLY_DETAIL' then
    if not P.IsTestPlayer(playerID) then return end
    local ok,text=pcall(function()
      local c=assert(Players[playerID]:GetCities():FindID(params.CityID),'AP_CITY_UNKNOWN')
      return shared.ResearchApply.Describe(playerID,c,params.Action=='RESEARCH_APPLY_DETAIL')
    end)
    shared.Snapshot=ok and text or '学以致用：城市暂不可读';shared.LastToken=params.Token;return
  end
  if params.Action=='RESEARCH_CROSS_SAMPLE' then shared.ResearchCross.Receive(playerID,params);return end
  if params.Action=='RESEARCH_CROSS_READ' or params.Action=='RESEARCH_CROSS_DETAIL' then
    if not P.IsTestPlayer(playerID) then return end
    local ok,out=pcall(function()
      local c=assert(Players[playerID]:GetCities():FindID(params.CityID),'CROSS_CITY_UNAVAILABLE')
      return shared.ResearchCross.Describe(playerID,c,params.Action=='RESEARCH_CROSS_DETAIL')
    end)
    shared.Snapshot=ok and out or '跨学科研究：城市暂不可读';shared.LastToken=params.Token;return
  end
  if params.Action=='COMPLETENESS_READ' or params.Action=='RESEARCH_INFRA_DETAIL' then
    if not P.IsTestPlayer(playerID) then return end
    shared.RequestToken=params.Token
    local ok,report=pcall(function()
      local c=Players[playerID]:GetCities():FindID(params.CityID)
      assert(c and c:GetOwner()==playerID,'DC_SELECTED_CITY_UNAVAILABLE')
      return shared.ResearchInfrastructure.Describe(playerID,c,params.Action=='RESEARCH_INFRA_DETAIL')
    end)
    shared.Snapshot=ok and report or ('科研基础设施读取未完成：'..tostring(report))
    shared.LastToken=params.Token;return
  end
  if params.Action=='CITY_PRESENTATION_READ' then
    if not P.IsTestPlayer(playerID) then return end
    local ok,f=pcall(function()
      local c=Players[playerID]:GetCities():FindID(params.CityID)
      assert(c and c:GetOwner()==playerID,'PRESENTATION_CITY_UNAVAILABLE')
      local f=shared.EffectiveFacts.Read(playerID,c)
      f.institutionArchive=shared.CityProgressionStore.InstitutionArchive(playerID,c)
      local good,s=pcall(shared.CityProgressionStore.InstitutionSummary,playerID,c)
      if good and s.token==f.token and s.reference.owner==playerID and s.reference.cityID==c:GetID()
       and s.reference.x==c:GetX() and s.reference.y==c:GetY()then
       f.institutionSummary=s
       if s.tradition then
        local ready,percent,nextAge=pcall(function()
         local speed=GameInfo.GameSpeeds[GameConfiguration.GetGameSpeedType()]
         return SPCResearchTradition.Shadow(s.tradition.age,assert(speed and speed.CostMultiplier)/100)
        end)
        if ready then s.tradition.percent=percent;s.tradition.nextAge=nextAge end
       end
      else f.institutionSummary={known=false}end
      return f
    end)
    shared.CityPresentationView={token=params.Token,owner=playerID,cityID=params.CityID,
      specialization=ok and f.specialization or nil,potential=ok and f.potential or nil,
      progression=ok and f.progression or nil,institutionArchive=ok and f.institutionArchive or nil,
      institutionSummary=ok and f.institutionSummary or nil,
      investments=ok and f.investmentCount or nil,active=ok and f.active or nil,activeStatus=ok and f.activeStatus or nil,
      x=ok and Players[playerID]:GetCities():FindID(params.CityID):GetX() or nil,
      y=ok and Players[playerID]:GetCities():FindID(params.CityID):GetY() or nil,error=not ok and tostring(f) or nil}
    -- Existing bounded trace, scalar results only; no extra native reads.
    if SPCExpeditionTrainingDiagnostics then
      if not shared.PresentationDiagnostics then shared.PresentationDiagnostics=SPCExpeditionTrainingDiagnostics.New(P,'PRESENTATION_GAMEPLAY')end
      local d=shared.PresentationDiagnostics;local v=shared.CityPresentationView
      if d then pcall(d.Record,'INSTITUTION_FACTS',{owner=playerID,city=params.CityID,requestKey=params.Token,
        specialization=v.specialization,potential=v.potential,active=v.active,activeStatus=v.activeStatus,readStatus=ok and 'READY' or 'UNAVAILABLE'})end
    end
    return
  end
  if type(params.Action)=='string' and params.Action:find('^INSPIRE_') then
    if not P.IsTestPlayer(playerID) then return end
    local c=Players[playerID]:GetCities():FindID(params.CityID)
    shared.CultureInspirationView=nil
    local ok,out=pcall(function()
      assert(c and c:GetOwner()==playerID,'INSP_CITY_UNKNOWN')
      local report,view=shared.CultureInspiration.Describe(playerID,c)
      view.token=params.Token;shared.CultureInspirationView=view;return report
    end)
    shared.Snapshot=ok and out or Locale.Lookup('LOC_SPC_INSPIRATION_PENDING')
    shared.LastToken=params.Token;return
  end
  if shared.CultureMeaning and type(params.Action)=='string' and params.Action:find('^CULTURE_MEANING_') then
    shared.CultureMeaningView=nil -- No test baseline or stale native view in normal mode.
    local ok,out=pcall(function()
      local c=assert(Players[playerID]:GetCities():FindID(params.CityID),'ME_CITY_UNKNOWN')
      assert(c:GetOwner()==playerID,'ME_OWNER_UNKNOWN')
      local report=shared.CultureMeaning.Describe(playerID,c) -- Read-only; old controls cannot write.
      if params.Action~='CULTURE_MEANING_READ' and params.Action~='CULTURE_MEANING_STATUS' then
        report=report..'\n实验开关已停用；此请求不会启用、撤销或替换正常收益。'
      end
      return report
    end)
    shared.Snapshot=ok and out or '意义延展：当前城市暂不可读。';shared.LastToken=params.Token;return
  end
  if params.Action=='CULTURE_MEANING_GATE_ADVANCE' or params.Action=='CULTURE_MEANING_ADVANCE' or params.Action=='CULTURE_MEANING_READ' or params.Action=='CULTURE_MEANING_CONFIG' or params.Action=='CULTURE_MEANING_END' or params.Action=='CULTURE_MEANING_DIAGNOSTIC_ADVANCE' or params.Action=='CULTURE_MEANING_DIAGNOSTIC_READ' then
    -- One request-local read model; a failed request must not reuse a prior UI view.
    shared.CultureMeaningView=nil
    local at='CITY';local actionError;local actionStage
    local function detail(why)
      local text=tostring(why):gsub('[%c]',' ');local code=text:match('(ME_[A-Z_]+)')
      if not code then return text:sub(1,120)end
      local reason=text:match(code..': ([A-Z_]+)');return code..(reason and (' / '..reason) or '')
    end
    local ok,out=pcall(function()
      local c=assert(Players[playerID]:GetCities():FindID(params.CityID),'ME_CITY_UNKNOWN')
      assert(c:GetOwner()==playerID,'ME_OWNER_UNKNOWN')
      at='MODULE';local probe=assert(shared.CultureMeaningProbe,'ME_MODULE_NOT_READY')
      if params.Action=='CULTURE_MEANING_DIAGNOSTIC_ADVANCE' then
        at='DIAGNOSTIC_ADVANCE';assert(type(probe.DiagnosticAdvance)=='function','ME_ACTION_NOT_READY')
        local changed,why=pcall(probe.DiagnosticAdvance,playerID,c,params.Token)
        if not changed then actionError=detail(why)end
      elseif params.Action=='CULTURE_MEANING_GATE_ADVANCE' then
        at='GATE_ADVANCE';assert(type(probe.GateAdvance)=='function','ME_ACTION_NOT_READY')
        local changed,why=pcall(probe.GateAdvance,playerID,c,params.Token)
        if not changed then actionError=detail(why)end
      elseif params.Action=='CULTURE_MEANING_ADVANCE' then
        at='ADVANCE';assert(type(probe.Advance)=='function','ME_ACTION_NOT_READY')
        local changed,why=pcall(probe.Advance,playerID,c,params.Token)
        if not changed then actionError=detail(why)end
      elseif params.Action=='CULTURE_MEANING_END' then
        at='END';assert(type(probe.End)=='function','ME_ACTION_NOT_READY')
        local changed,why=pcall(probe.End,playerID,c,params.Token)
        if not changed then actionError=detail(why)end
      elseif params.Action=='CULTURE_MEANING_CONFIG' then
        at='CONFIG';assert(type(probe.CycleVariant)=='function','ME_ACTION_NOT_READY')
        local changed,why=pcall(probe.CycleVariant,playerID,c,params.Token)
        if not changed then actionError=detail(why)end
      end
      actionStage=at
      at='VIEW';assert(type(probe.View)=='function','ME_VIEW_NOT_READY')
      local diagnostic=params.Action=='CULTURE_MEANING_DIAGNOSTIC_ADVANCE' or params.Action=='CULTURE_MEANING_DIAGNOSTIC_READ'
      local view=probe.View(playerID,c,diagnostic)
      assert(type(view)=='table' and view.owner==playerID and view.cityID==params.CityID,'ME_VIEW_INVALID')
      -- These errors belong only to this disposable view, not the probe's state.
      view.error=view.error or actionError or view.configurationError
      at='DESCRIBE';assert(type(probe.Describe)=='function','ME_DESCRIBE_NOT_READY')
      local report=probe.Describe(playerID,c,view);assert(type(report)=='string','ME_REPORT_INVALID')
      if actionError then report=report..'\n操作未完成 ['..tostring(actionStage or at)..']：'..actionError end
      if view.configurationError then report=report..'\n配置读取未完成 [VIEW]：'..detail(view.configurationError)end
      view.token=params.Token;shared.CultureMeaningView=view
      return report
    end)
    shared.Snapshot=ok and out or ('意义延展验证未完成 ['..at..']：'..detail(out)..(actionError and ('\n操作未完成 ['..tostring(actionStage or at)..']：'..actionError) or ''))
    shared.LastToken=params.Token;return
  end
  if params.Action=='CULTURE_AESTHETIC_READ' or params.Action=='CULTURE_AESTHETIC_DETAIL' then
    local ok,out=pcall(function()
      local c=assert(Players[playerID]:GetCities():FindID(params.CityID),'AE_CITY_UNKNOWN')
      return shared.CultureAesthetic.Describe(playerID,c,params.Action=='CULTURE_AESTHETIC_DETAIL',params.Page)
    end)
    shared.Snapshot=ok and out or '风雅熏陶：城市暂不可读';shared.LastToken=params.Token;return
  end
  if params.Action=='GREAT_WORK_FACTS_READ' or params.Action=='GREAT_WORK_FACTS_DETAIL' then
    local ok,out=pcall(shared.GreatWorkFacts.Describe,playerID,params.CityID,params.Action=='GREAT_WORK_FACTS_DETAIL',params.Page)
    shared.Snapshot=ok and out or '巨作事实：暂不可读，未改变收益。';shared.LastToken=params.Token;return
  end
  if params.Action=='DIALOGUE_SAMPLE' then
    -- Independent facts validation cannot block or substitute for the legacy writer.
    local factsOK,factsAccepted=false,false
    if shared.GreatWorkFacts then
      factsOK,factsAccepted=pcall(shared.GreatWorkFacts.Receive,playerID,params)
      if not factsOK then shared.GreatWorkFacts.lastError='GW_RECEIVE_EXCEPTION' end
    end
    local ok,accepted=pcall(shared.Dialogue.Receive,playerID,params)
    if not ok then
      if shared.Dialogue and P.IsTestPlayer(playerID) then shared.Dialogue.errors[playerID]='DIALOGUE_RECEIVE_EXCEPTION: '..tostring(accepted) end
      print('[SPC][B059][SAMPLE] '..tostring(accepted))
    end
    if factsOK and factsAccepted==true then
      -- Readiness fallback is not a second delivery attempt for failed callbacks.
      -- Keep legacy sample-pair confirmation independent of any one ability.
      for _,name in ipairs({'CultureMeaning','CultureInspiration'})do
        local consumer=shared[name]
        if consumer then
          local status=shared.GreatWorkFacts.ConsumerStatus(name)
          if not status or status.pending==0 then
            local ready=pcall(consumer.CollectionConfirmed,playerID)
            if not ready then consumer.error='GW_CONSUMER_READY_FAILED' end
          end
        end
      end
    end
    if factsOK and factsAccepted==true and ok and accepted==true then
      local paired,confirmed=pcall(shared.Dialogue.ConfirmSamplePair,playerID,params)
      if paired and confirmed==true and shared.CultureMeaningProbe then
        local notified,why=pcall(shared.CultureMeaningProbe.CollectionConfirmed,playerID,params)
        if not notified then shared.CultureMeaningProbe.error='ME_COLLECTION_UPDATE_FAILED: '..tostring(why):sub(1,180)end
      end
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
  if type(params.Action)=='string' and params.Action:find('^DEVELOPMENT_') then
    local ok,out=pcall(function()
      local d=assert(shared.DevelopmentInvestment,'DEVELOPMENT_MODULE_NOT_LOADED')
      d.Request(playerID,params)
      return d.Describe(playerID,assert(Players[playerID]:GetCities():FindID(params.CityID),'DEVELOPMENT_CITY_UNKNOWN'))
    end)
    shared.Snapshot=ok and out or '发展投资暂不可用，请查看合同面板。';shared.LastToken=params.Token;return
  end
  if type(params.Action)=='string' and params.Action:find('^CAPITAL_') then
    local ok,out=pcall(function()
      local d=assert(shared.CapitalInvestment,'CAPITAL_MODULE_NOT_LOADED')
      d.Request(playerID,params)
      return d.Describe(playerID,assert(Players[playerID]:GetCities():FindID(params.CityID),'CAPITAL_CITY_UNKNOWN'))
    end)
    shared.Snapshot=ok and out or '资本投资暂不可用，请查看合同面板。';shared.LastToken=params.Token;return
  end
  if type(params.Action)=='string' and params.Action:find('^COMMERCE_') then
    local ok,out=pcall(function()
      local d=assert(shared.Commerce,'COM_MODULE_NOT_LOADED')
      assert(params.Action=='COMMERCE_READ' or params.Action=='COMMERCE_SELECT','COM_LEGACY_RETIRED')
      d.Request(playerID,params)
      local c=assert(Players[playerID]:GetCities():FindID(params.CityID),'COM_CITY_UNKNOWN')
      return d.Describe(playerID,c)
    end)
    shared.Snapshot=ok and out or ('商业化暂不可用：'..(tostring(out):match('COM_[A-Z_]+') or 'COM_STATE_UNKNOWN'))
    shared.LastToken=params.Token;return
  end
  if params.Action=='GWA_READ' or params.Action=='GWA_OFF' or params.Action=='GWA_AUTO' then
    shared.RequestToken=params.Token
    local ok,out=pcall(function()
      assert(P.IsTestPlayer(playerID),'GWA_NOT_TEST_PLAYER')
      local c=Players[playerID]:GetCities():FindID(params.CityID)
      assert(c and c:GetOwner()==playerID,'GWA_CITY_UNAVAILABLE')
      local d=assert(shared.GreatWorkAdjacency,'GWA_MODULE_NOT_LOADED')
      assert(type(d.Describe)=='function','GWA_MODULE_INCOMPLETE')
      assert(not d.retired or params.Action=='GWA_READ','GWA_RETIRED')
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
    shared.Snapshot=shared.StandardizationEffects.Describe(playerID,c,params.Page);shared.LastToken=params.Token;return
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
  if params.Action=="STANDARDIZATION_READ" or params.Action=="INDUSTRY_HISTORY_READ" then
    if not P.IsTestPlayer(playerID) then return end
    local c=Players[playerID]:GetCities():FindID(params.CityID)
    if not c or c:GetOwner()~=playerID then return end
    shared.Snapshot=shared.Standardization.Describe(playerID,c,params.Page)
    if params.Action=="INDUSTRY_HISTORY_READ" then
      shared.Snapshot=shared.IndustryHistory.Describe(playerID,c)..'\n\n'..shared.CrewProjects.Describe(playerID,c)..'\n\n'..shared.Snapshot
    end
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
      local service=shared.PlayerActionReplies;local replies
      if params.ReplyChannel~=nil then
        replies=service and service.Views
        if not replies or not replies.Accepts(playerID,params)then return end
      end
      local view=shared.UnitActions.ReadView(playerID,params.UnitID,params.Token)
      if replies then
        local ok,accepted=false,false
        if shared.PlayerActionReplies==service and service.Views==replies then ok,accepted=pcall(replies.PublishView,playerID,params,view)end
        shared.ObserverErrors=shared.ObserverErrors or {}
        shared.ObserverErrors['unit-view-reply']=not(ok and accepted==true)and 'PLAYER_VIEW_REPLY_UNAVAILABLE'or nil
        if not(ok and accepted==true)and shared.PlayerActionReplies==service and service.Views==replies then pcall(replies.FailView,playerID,params)end
      end
    end
    return
  end
  if params.Action=="UNIT_ACTION_SPAWN" or params.Action=="UNIT_ACTION_PREPARE" or params.Action=="UNIT_ACTION_CONFIRM" then
    if not P.IsTestPlayer(playerID) then return end
    local replies
    if params.ReplyChannel~=nil then
      replies=shared.PlayerActionReplies
      if not replies or not replies.Accepts(playerID,params)then return end
    end
    local text,result,outcome=shared.UnitActions.Run(playerID,params)
    if replies then
      local ok,accepted=false,false
      if shared.PlayerActionReplies==replies then ok,accepted=pcall(replies.Publish,playerID,params,text,outcome)end
      shared.ObserverErrors=shared.ObserverErrors or {}
      shared.ObserverErrors['unit-action-reply']=not(ok and accepted==true)and 'PLAYER_REPLY_UNAVAILABLE'or nil
    else
      shared.Snapshot=text;shared.LastToken=params.Token -- Explicit DEV/legacy compatibility.
    end
    SPCSafeCallbacks.Call(shared,'request-facts',refreshInvestmentSupport,playerID,result)
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
    P.Observe('ui','received')
    if shared.NativeFacts then
     local workerOnly=params.WorkerOnly==true and params.FactsChanged==false
     if not workerOnly then
      local ok,err=pcall(function()
       local depth=assert(shared.DistrictCompleteness,'UI_DEPTH_PROVIDER_UNAVAILABLE')
       depth.MarkDirty(playerID,nil,'UI_FACTS_DIRTY')
      end)
      shared.ObserverErrors=shared.ObserverErrors or {}
      local safe,text=pcall(tostring,err)
      shared.ObserverErrors.UI_DEPTH_FACTS=not ok and (safe and text:sub(1,180) or 'UI_DEPTH_MARK_FAILED') or nil
     end
     shared.NativeFacts.Workers({player=playerID},workerOnly and 'UI_WORKERS_DIRTY' or 'UI_FACTS_DIRTY')
    end
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
    local result
    if params.Action=="INVEST_PREPARE" then
      shared.Snapshot=shared.InvestmentAction.Prepare(playerID,city,params.UnitID,params.Token)
    elseif type(params.PlanToken)=="string" and #params.PlanToken<=400 then
      shared.Snapshot,result=shared.InvestmentAction.Confirm(playerID,city,params.PlanToken)
    else shared.Snapshot="B033 REJECTED: PREPARE_FIRST" end
    shared.LastToken=params.Token -- primary result already returned; observers cannot revoke ACK
    SPCSafeCallbacks.Call(shared,'request-facts',refreshInvestmentSupport,playerID,result)
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
    shared.Snapshot=shared.NetworkBridge.Report(playerID,city,params.Action=="NETWORK_DETAIL",params.Page)
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
    if params.Action=="SPECIALISTS" then
      local ok,f=pcall(shared.EffectiveFacts.Read,playerID,city)
      if ok and f.specialization=='INDUSTRY' then
        shared.Snapshot=shared.Snapshot..'\n'..shared.IndustrySupport.Describe(playerID,city)
      else shared.Snapshot=shared.Snapshot..'\n'..shared.ResearchSupport.Run(playerID,city,'READ') end
      shared.Snapshot=shared.Snapshot..shared.Lv3Support.Describe(playerID,city)
    end
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
  shared.RequestDepth=(shared.RequestDepth or 0)+1 -- GC scheduling guard only; not transaction authority
  local ok,err=pcall(request,...)
  shared.RequestDepth=shared.RequestDepth-1
  if not ok then shared.FailureAt=shared.Stage;stage("ERROR "..P.Scalar(err)) end
end)
-- Completion status is reported by the protected startup epilogue.

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

-- Explicit ordered startup entries. Failure containment does not reorder dependencies.
composition.Run('TradeRouteProbe',{},{'AutoRouteProbe'},function() include('TradeRouteProbe');SPCTradeRouteProbe.Start(P,shared) end)

composition.Run('CompletionProbe',{},{'CompletionProbe'},function() include('CompletionProbe');SPCCompletionProbe.Start(P,shared) end)

composition.Run('StorageProbe',{},{'StorageProbe'},function() include('StorageProbe');SPCStorageProbe.Start(P,shared) end)

composition.Run('CityIdentityDefinition',{}, {},function()include('CityIdentityRead')end)

composition.Run('CitySequenceProbe',{},{'CitySequenceProbe'},function() include('CitySequenceProbe');SPCCitySequenceProbe.Start(P,shared) end)

composition.Run('FactChanges',{}, {'FactChanges'},function()
 include('FactChanges');local changes=SPCFactChanges.New(shared)
 local draining=false
 local function drain()
  if not composition.sealed or draining then return end;draining=true
  local function run()changes.Flush();if shared.FactBindings then shared.FactBindings.Flush()end end
  local facts=shared.EffectiveFacts
  local ok,err=pcall(function()if facts and facts.WithPhase then facts.WithPhase('FACT_PROPAGATION',run)else run()end end)
  draining=false
  if not ok then local safe,text=pcall(tostring,err);shared.FactPropagationError=safe and text:sub(1,180) or 'FACT_PROPAGATION_FAILED'end
 end
 local event=P.Field(Events,'GameCoreEventPublishComplete');if event and event.Add then event.Add(drain)end
end)

composition.Run('CityProgressionStore',{'CityIdentityDefinition','FactChanges'},{'CityProgressionStore'},function() include('CityProgressionStore');SPCCityProgressionStore.Start(P,shared) end)

composition.Run('LegacyCleanup',{'CityProgressionStore'},{'LegacyCleanup'},function()
 -- Register before include/Start: a failed owner must never remove the mandatory exit gate.
 local exit
 shared.CityProgressionStore.RegisterExit('LegacyCleanup',function(...)
  assert(exit,'LEGACY_CLEANUP_UNAVAILABLE');return exit(...)
 end)
 include('LegacyCleanup');local owner=SPCLegacyCleanup.Start(P,shared);exit=owner.Exit
end)

composition.Run('BindingProbe',{'CityProgressionStore'},{'BindingProbe'},function() include('BindingProbe');SPCBindingProbe.Start(P,shared) end)

composition.Run('CompletionRecordProbe',{'CityProgressionStore'},{'CompletionRecordProbe'},function() include('CompletionRecordProbe');SPCCompletionRecordProbe.Start(P,shared) end)

composition.Run('CityJournalProbe',{'CityProgressionStore'},{'CityJournalProbe'},function() include('CityJournalProbe');SPCCityJournalProbe.Start(P,shared) end)

composition.Run('EligibilityProbe',{},{'EligibilityProbe'},function() include('EligibilityProbe');SPCEligibilityProbe.Start(P,shared) end)

composition.Run('QualificationProbe',{},{'QualificationProbe'},function() include('QualificationProbe');SPCQualificationProbe.Start(P,shared) end)

composition.Run('EnvelopeProbe',{},{'EnvelopeProbe'},function() include('EnvelopeProbe');SPCEnvelopeProbe.Start(P,shared) end)

composition.Run('CityFlowProbe',{'CityProgressionStore'},{'CityFlowProbe'},function() include('FreshBindingHook');include('CityFlowProbe');SPCCityFlowProbe.Start(P,shared) end)

composition.Run('EffectiveFacts',{'CityFlowProbe','CityProgressionStore'},{'EffectiveFacts'},function() include('EffectiveFacts');SPCEffectiveFacts.Start(P,shared) end)

composition.Run('ResearchTradition',{'CityProgressionStore'},{'ResearchTradition'},function() SPCResearchTradition.Start(P,shared) end)

composition.Run('NativeFacts',{'FactChanges'},{'NativeFacts'},function()include('NativeFacts');SPCNativeFacts.New(P,shared)end)

composition.Run('ResearchTraditionEffects',{'CityProgressionStore','ResearchTradition','EffectiveFacts','NativeFacts'},{'ResearchTraditionEffects'},function() include('ResearchTraditionEffects');SPCResearchTraditionEffects.Start(P,shared) end)

composition.Run('DistrictCompleteness',{},{'DistrictCompleteness'},function() include('OrdinaryBuildingCatalog');include('DistrictCompleteness');include('CurrentSpecializationFacts');include('ResearchInfrastructureShadow');SPCDistrictCompleteness.Start(P,shared) end)

composition.Run('InvestmentAction',{'CityProgressionStore','EffectiveFacts'},{'InvestmentAction'},function() include('InvestmentAction');SPCInvestmentAction.Start(P,shared) end)

composition.Run('RuntimeRetirement',{'CityProgressionStore'}, {'RuntimeRetirement'},function()include('RuntimeWork');SPCRuntimeWork.StartRetirement(P,shared)end)

composition.Run('ResearchSupport',{'RuntimeRetirement','EffectiveFacts','NativeFacts'},{'ResearchSupport'},function() include('ResearchSupport');SPCResearchSupport.Start(P,shared) end)

composition.Run('Lv2Housing',{'RuntimeRetirement','EffectiveFacts','DistrictCompleteness','NativeFacts'},{'Lv2Housing'},function() include('Lv2Housing');SPCLv2Housing.Start(P,shared) end)

composition.Run('Lv2GPP',{'RuntimeRetirement','EffectiveFacts','NativeFacts'},{'Lv2GPP'},function() include('Lv2GPP');SPCLv2GPP.Start(P,shared) end)

composition.Run('CarrierHealthTrace',{},{'CarrierHealthTrace'},function() include('CarrierHealthTrace');SPCCarrierHealthTrace.Start(P,shared) end)

composition.Run('NetworkBridge',{'EffectiveFacts','NativeFacts'},{'NetworkBridge','RouteSignalRevision'},function() include('NetworkBridge');SPCNetworkBridge.Start(P,shared) end)

composition.Run('IndustrySupport',{'RuntimeRetirement','EffectiveFacts','CityProgressionStore','NativeFacts'},{'IndustrySupport'},function() include('IndustrySupport');SPCIndustrySupport.Start(P,shared) end)

composition.Run('Lv3Support',{'RuntimeRetirement','EffectiveFacts','LegacyCleanup'},{'Lv3Support'},function() include('Lv3Support');SPCLv3Support.Start(P,shared,{centralExit=true}) end)

composition.Run('Lv3Effects',{'RuntimeRetirement','EffectiveFacts','NativeFacts','LegacyCleanup'},{'Lv3Effects'},function() include('Lv3Effects');SPCLv3Effects.Start(P,shared,{retireCommerce=true,centralExit=true}) end)

composition.Run('ConstructionProbe',{},{'ConstructionProbe'},function() include('ConstructionProbe');SPCConstructionProbe.Start(P,shared) end)

composition.Run('UnitSiteProbe',{},{'UnitSiteProbe'},function() include('UnitActionSitePolicy');include('UnitSiteProbe');SPCUnitSiteProbe.Start(P,shared) end)

composition.Run('UnitTargets',{'EffectiveFacts','UnitSiteProbe'},{'UnitTargets'},function() include('UnitTargets');SPCUnitTargets.Start(P,shared) end)

composition.Run('UnitActions',{'CityProgressionStore','InvestmentAction','ConstructionProbe','UnitTargets'},{'UnitActions'},function() include('UnitActions');SPCUnitActions.Start(P,shared) end)

composition.Run('CrewProjects',{'CityProgressionStore','EffectiveFacts'},{'CrewProjects'},function() include('CrewProjects');SPCCrewProjects.Start(P,shared) end)

composition.Run('PlayerActionReplies',{'UnitActions'},{'PlayerActionReplies'},function() include('PlayerActionReplies');SPCPlayerActionReplies.Start(P,shared) end)

composition.Run('CrewPrecision',{'UnitActions','UnitTargets','CrewProjects','ConstructionProbe'},{'CrewPrecision'},function() include('CrewPrecision');SPCCrewPrecision.Start(P,shared) end,{{shared.UnitActions,'Run'}})

composition.Run('Lv4Percent',{'RuntimeRetirement','EffectiveFacts'},{'Lv4Percent'},function() include('Lv4Percent');SPCLv4Percent.Start(P,shared,{centralExit=true}) end)

composition.Run('ResearchInfrastructure',{'RuntimeRetirement','EffectiveFacts','DistrictCompleteness','NativeFacts'},{'ResearchInfrastructure'},function() include('ResearchInfrastructure');SPCResearchInfrastructure.Start(P,shared) end)

composition.Run('ResearchCross',{'RuntimeRetirement','EffectiveFacts','NativeFacts'},{'ResearchCross'},function() include('ResearchCross');SPCResearchCross.Start(P,shared) end)

composition.Run('ResearchApply',{'EffectiveFacts','DistrictCompleteness','NativeFacts'},{'ResearchApply'},function() include('ResearchApply');SPCResearchApply.Start(P,shared) end)

composition.Run('ResearchChair',{'EffectiveFacts','DistrictCompleteness','NativeFacts'},{'ResearchChair'},function() include('ResearchChair');SPCResearchChair.Start(P,shared) end)

composition.Run('HalfYieldProbe',{},{'HalfYieldProbe'},function() include('HalfYieldProbe');SPCHalfYieldProbe.Start(P,shared,{centralExit=true}) end)

composition.Run('CopyYields',{},{'CopyYields'},function() include('CopyYields');SPCCopyYields.Start(P,shared,{retired=true}) end)

composition.Run('IndustryHistory',{'CityProgressionStore'},{'IndustryHistory'},function() include('IndustryHistory');SPCIndustryHistory.Start(P,shared) end)

composition.Run('Standardization',{'CityProgressionStore','EffectiveFacts'},{'Standardization'},function() include('StandardizationCatalog');include('Standardization');SPCStandardization.Start(P,shared) end)

composition.Run('PurchaseProbe',{},{'PurchaseProbe'},function() include('PurchaseProbe');SPCPurchaseProbe.Start(P,shared,{centralExit=true}) end)

composition.Run('StandardizationDiscount',{},{'StandardizationDiscount'},function() include('StandardizationDiscount');SPCStandardizationDiscount.Start(P,shared,{retired=true}) end)

composition.Run('StandardizationEffects',{'CityProgressionStore','Standardization','NetworkBridge','EffectiveFacts','CopyYields','StandardizationDiscount','NativeFacts'},{'StandardizationEffects'},function() include('StandardizationEffects');SPCStandardizationEffects.Start(P,shared) end)

composition.Run('NetworkBoost',{},{'NetworkBoost'},function() include('NetworkBoost');SPCNetworkBoost.Start(P,shared,{retired=true,centralExit=true}) end)

composition.Run('GreatWorkProbe',{},{'GreatWorkProbe'},function() include('GreatWorkProbe');SPCGreatWorkProbe.Start(P,shared,{centralExit=true}) end)

composition.Run('GreatWorkFacts',{},{'GreatWorkFacts'},function() include('GreatWorkFacts');SPCGreatWorkFacts.Start(P,shared) end)

composition.Run('CultureAesthetic',{'CityProgressionStore','GreatWorkFacts','EffectiveFacts','DistrictCompleteness','Lv3Effects','Lv4Percent','NativeFacts'},{'CultureAesthetic'},function() include('CultureAesthetic');SPCCultureAesthetic.Start(P,shared) end)

composition.Run('Dialogue',{'GreatWorkFacts','LegacyCleanup'},{'Dialogue'},function() include('Dialogue');SPCDialogue.Start(P,shared,{centralExit=true}) end)

composition.Run('GreatWorkAdjacency',{},{'GreatWorkAdjacency'},function() include('GreatWorkAdjacency');SPCGWAdjacency.Start(P,shared,{retired=true,centralExit=true}) end)

composition.Run('CultureMeaning',{'CityProgressionStore','GreatWorkFacts','EffectiveFacts','DistrictCompleteness','GreatWorkAdjacency','Dialogue','NativeFacts'},{'CultureMeaning'},function() include('CultureMeaning');SPCCultureMeaning.Start(P,shared) end)

composition.Run('CultureInspirationProbe',{},{'CultureInspirationProbe'},function() include('CultureInspirationProbe');SPCCultureInspirationProbe.Start(P,shared,{retired=true}) end)

composition.Run('CultureInspiration',{'CityProgressionStore','GreatWorkFacts','EffectiveFacts','CultureInspirationProbe','NativeFacts'},{'CultureInspiration'},function() include('CultureInspiration');SPCCultureInspiration.Start(P,shared) end)

composition.Run('CommerceConvergence',{'RuntimeRetirement'},{'CommerceConvergence'},function() include('CommerceConvergence');SPCCommerceConvergence.Start(P,shared,{retired=true,centralExit=true}) end)


-- Preserve the deliberate legacy-inheritance isolation boundary and observer order.
shared.CityInheritanceRead=nil
shared.InheritanceShadow=nil
shared.CityInheritance=nil
shared.OnPermanentCityWrite=nil
shared.InheritanceIsolation=true


composition.Run('TimedProjectReaders',{'CityProgressionStore'},{'TimedProjectReaders'},function()include('TimedProjectReaders');SPCTimedProjectReaders.New(P,shared)end)

composition.Run('ClaimProjects',{'CityProgressionStore'},{'ClaimProjects'},function() include('ClaimProjects');SPCClaimProjects.Start(P,shared) end)

composition.Run('IndustrySupportBind',{'IndustrySupport'},{},function() shared.IndustrySupport.BindPermanentWrites() end)

composition.Run('EngineeringStudyProjects',{'CityProgressionStore','EffectiveFacts','IndustryHistory'},{'EngineeringStudy'},function() include('EngineeringStudyProjects');SPCEngineeringStudyProjects.Start(P,shared) end)

composition.Run('IndustryWonderEffects',{'CityProgressionStore','EffectiveFacts','NativeFacts'},{'IndustryWonderEffects'},function() include('IndustryWonderEffects');SPCIndustryWonderEffects.Start(P,shared) end)

composition.Run('CrewProjectsBind',{'CrewProjects'},{},function() shared.CrewProjects.BindPermanentWrites() end)

composition.Run('Commerce',{'CityProgressionStore','EffectiveFacts','NetworkBridge','CommerceConvergence','NativeFacts'},{'Commerce'},function() include('Commerce');SPCCommerce.Start(P,shared) end)

composition.Run('CommerceBind',{'Commerce'},{},function() shared.Commerce.BindPermanentWrites() end)

composition.Run('CapitalInvestment',{'CityProgressionStore','EffectiveFacts','Commerce','NetworkBridge'},{'CapitalInvestment'},function() include('CapitalInvestment');SPCCapitalInvestment.Start(P,shared) end)

composition.Run('DevelopmentInvestment',{'CityProgressionStore','EffectiveFacts','NetworkBridge'},{'DevelopmentInvestment'},function() include('DevelopmentInvestment');SPCDevelopmentInvestment.Start(P,shared) end)

composition.Run('DialogueProjects',{'CityProgressionStore','EffectiveFacts','GreatWorkFacts'},{'DialogueProjects'},function() include('DialogueProjects');SPCDialogueProjects.Start(P,shared) end)

-- New effect failure never reactivates the retired Dialogue writer.
if shared.Dialogue then shared.Dialogue.retired=true end

composition.Run('DialogueEffects',{'CityProgressionStore','Dialogue','EffectiveFacts','GreatWorkFacts','NativeFacts'},{'DialogueEffects'},function() include('DialogueEffects');SPCDialogueEffects.Start(P,shared) end)

composition.Run('CityIdentityRead',{},{'CityIdentityRead'},function() SPCCityIdentityRead.Start(P,shared) end)

composition.Run('CityIdentityMapping',{},{'CityIdentityExperiment'},function() include('CityIdentityExperiment');include('CityIdentityMapping');SPCCityIdentityMapping.Start(P,shared) end)

composition.Run('TimedProductionProbe',{},{'TimedProductionProbe'},function() include('TimedProductionProbe');SPCTimedProductionProbe.Start(P,shared) end)

composition.Run('OverflowStorageProbe',{},{'OverflowStorageProbe'},function() include('OverflowStorageProbe');SPCOverflowStorageProbe.Start(P,shared) end)

composition.Run('ProjectTurnObservation',{},{'ProjectTurnObservation'},function() include('ProjectTurnObservation');SPCProjectTurnObservation.Start(P,shared) end)

composition.Run('TimedProject',{},{'TimedProject'},function() include('TimedProject');SPCTimedProject.Start(P,shared) end)

composition.Run('NetworkIsolation',{'NetworkBridge'},{'NetworkIsolation'},function() include('NetworkIsolation');SPCNetworkIsolation.Start(P,shared) end)

composition.Run('MemoryObservation',{},{'MemoryObservation','MemoryEvidence'},function() SPCPerformance.StartMemory(P,shared) end)

composition.Run('CultureInsightsTourism',{'CityProgressionStore','EffectiveFacts','NativeFacts'},{'CultureInsightsTourism'},function() include('CultureInsightsTourism');SPCCultureInsightsTourism.Start(P,shared) end)

composition.Run('CultureNetwork',{'CityProgressionStore','EffectiveFacts','NetworkBridge','NativeFacts'},{'CultureNetwork'},function() include('CultureNetwork');SPCCultureNetwork.Start(P,shared) end)

composition.Run('ExpeditionSpyGate',{'CityProgressionStore','EffectiveFacts'},{'ExpeditionGate'},function() include('ExpeditionSpyStore');include('ExpeditionSpyGate');SPCExpeditionSpyGate.Start(P,shared) end)

composition.Run('ExpeditionTraining',{'ExpeditionSpyGate','CityProgressionStore','EffectiveFacts'},{'ExpeditionTraining'},function() include('ExpeditionTraining');SPCExpeditionTraining.Start(P,shared) end)

composition.Run('Restructuring',{'CityProgressionStore','EffectiveFacts'},{'Restructuring'},function() include('Restructuring');SPCRestructuring.Start(P,shared) end,{{ExposedMembers,'SPC_RestructuringViews'}})

composition.Run('LevelBannerState',{'CityProgressionStore','EffectiveFacts'},{'LevelBanners'},function() include('LevelBannerState');SPCLevelBannerState.Start(P,shared) end)


composition.Run('FactConsumerBindings',{'FactChanges'},{'FactBindings'},function()include('FactConsumerBindings');SPCFactConsumerBindings.New(shared)end)

-- Composition completion is diagnostic; it does not assert Store/effects readiness.
local startupFailures=composition.Complete()
if shared.TimedProjectReaders then pcall(shared.TimedProjectReaders.Seal)end
pcall(stage,startupFailures==0 and 'INITIALIZED ISOLATED_PROBES USER_GAME_TEST_REQUIRED'
 or ('INITIALIZED_PARTIAL STARTUP_FAILURES='..startupFailures..' USER_GAME_TEST_REQUIRED'))
if readiness then pcall(readiness.Seal)end

-- Install after original listeners; observational append only.
pcall(function()include('EventTimingDiagnostics');SPCEventTimingDiagnostics.Start(P,shared,'GAMEPLAY')end)
