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
  -- Return a bounded diagnostic failure instead of silently dropping an eligible UI's request.
  local eligible,eligibilityReason=P.IsTestPlayer(playerID)
  if not eligible then
    shared.RequestToken=params.Token
    shared.FailureAt="PLAYER_ELIGIBILITY"
    shared.Stage="ERROR 玩家资格检查未通过："..tostring(eligibilityReason)
    return
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
  if params.Action=='MEMORY_BEGIN' or params.Action=='MEMORY_READ' then
    local ok,out=pcall(shared.MemoryObservation.Read,playerID,params.Action=='MEMORY_BEGIN')
    shared.Snapshot=ok and out or ('内存观测不可用：'..tostring(out));shared.LastToken=params.Token;return
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
      return shared.EffectiveFacts.Read(playerID,c)
    end)
    shared.CityPresentationView={token=params.Token,owner=playerID,cityID=params.CityID,
      specialization=ok and f.specialization or nil,potential=ok and f.potential or nil,
      investments=ok and f.investmentCount or nil,active=ok and f.active or nil,activeStatus=ok and f.activeStatus or nil,
      x=ok and Players[playerID]:GetCities():FindID(params.CityID):GetX() or nil,
      y=ok and Players[playerID]:GetCities():FindID(params.CityID):GetY() or nil,error=not ok and tostring(f) or nil}
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
    if shared.Lv2Housing then shared.Lv2Housing.Audit({player=playerID}) end
    if shared.Lv2GPP then shared.Lv2GPP.Audit({player=playerID}) end
    if shared.ResearchInfrastructure then shared.ResearchInfrastructure.Audit({player=playerID}) end
    if shared.ResearchCross then shared.ResearchCross.Audit({player=playerID}) end
    if shared.ResearchApply then shared.ResearchApply.Audit({player=playerID}) end
    if shared.ResearchChair then shared.ResearchChair.Audit({player=playerID}) end
    if shared.CultureAesthetic then shared.CultureAesthetic.Audit({player=playerID}) end
    if shared.CultureMeaning then shared.CultureMeaning.Audit({player=playerID})end
    if shared.CultureInspiration then shared.CultureInspiration.Audit({player=playerID,city=params.CityID})end
    if shared.ResearchSupport then shared.ResearchSupport.Audit({player=playerID}) end
    if shared.IndustrySupport then shared.IndustrySupport.Audit({player=playerID}) end
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
    P.Observe('ui','received')
    if params.FactsChanged and shared.CultureMeaning then shared.CultureMeaning.Audit({player=playerID})end
    if params.FactsChanged and shared.CultureInspiration then shared.CultureInspiration.Audit({player=playerID})end
    if params.FactsChanged and shared.ResearchTraditionEffects then shared.ResearchTraditionEffects.Mark(playerID)end
    if params.FactsChanged and shared.NetworkBridge then shared.NetworkBridge.Refresh(playerID) end
    if params.FactsChanged and P.IsTestPlayer(playerID) and shared.Lv2Housing then shared.Lv2Housing.Audit({player=playerID}) end
    if P.IsTestPlayer(playerID) and shared.Lv2GPP then shared.Lv2GPP.Audit({player=playerID}) end
    if P.IsTestPlayer(playerID) and shared.Lv3Effects then shared.Lv3Effects.Audit({player=playerID}) end
    if P.IsTestPlayer(playerID) and shared.Lv4Percent then shared.Lv4Percent.Audit({player=playerID}) end
    if P.IsTestPlayer(playerID) and shared.ResearchInfrastructure then shared.ResearchInfrastructure.Audit({player=playerID}) end
    if not (params.WorkerOnly==true and params.FactsChanged==false) and P.IsTestPlayer(playerID) and shared.CultureAesthetic then shared.CultureAesthetic.Audit({player=playerID}) end
    if not (params.WorkerOnly==true and params.FactsChanged==false) and shared.CultureMeaningProbe then shared.CultureMeaningProbe.Audit({player=playerID})end
    -- Cross has no worker/focus input. Missing/mixed/contradictory provenance retains the fallback.
    if not (params.WorkerOnly==true and params.FactsChanged==false) and P.IsTestPlayer(playerID) and shared.ResearchCross then shared.ResearchCross.Audit({player=playerID}) end
    if P.IsTestPlayer(playerID) and shared.ResearchApply then shared.ResearchApply.Audit({player=playerID}) end
    if P.IsTestPlayer(playerID) and shared.ResearchChair then shared.ResearchChair.Audit({player=playerID}) end
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
    if shared.Lv2Housing then shared.Lv2Housing.Audit({player=playerID}) end
    if shared.Lv2GPP then shared.Lv2GPP.Audit({player=playerID}) end
    if shared.ResearchInfrastructure then shared.ResearchInfrastructure.Audit({player=playerID}) end
    if shared.ResearchCross then shared.ResearchCross.Audit({player=playerID}) end
    if shared.ResearchApply then shared.ResearchApply.Audit({player=playerID}) end
    if shared.ResearchChair then shared.ResearchChair.Audit({player=playerID}) end
    if shared.CultureAesthetic then shared.CultureAesthetic.Audit({player=playerID}) end
    if shared.CultureMeaning then shared.CultureMeaning.Audit({player=playerID})end
    if shared.CultureInspiration then shared.CultureInspiration.Audit({player=playerID,city=params.CityID})end
    if shared.ResearchSupport then shared.ResearchSupport.Audit({player=playerID}) end
    if shared.IndustrySupport then shared.IndustrySupport.Audit({player=playerID}) end
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

include("CityIdentityRead")
include("CitySequenceProbe")
SPCCitySequenceProbe.Start(P,shared)

include("CityProgressionStore")
SPCCityProgressionStore.Start(P,shared)
SPCYieldCarrierProbe.RegisterExit(shared)

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
SPCResearchTradition.Start(P,shared)
include('ResearchTraditionEffects')
SPCResearchTraditionEffects.Start(P,shared)

-- P0-A shared facts and pure shadow consumer; no old writer is replaced.
include("OrdinaryBuildingCatalog")
include("DistrictCompleteness")
include("CurrentSpecializationFacts")
include("ResearchInfrastructureShadow")
SPCDistrictCompleteness.Start(P,shared)

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
include("ResearchInfrastructure")
SPCResearchInfrastructure.Start(P,shared)

include("ResearchCross")
SPCResearchCross.Start(P,shared)
include("ResearchApply")
SPCResearchApply.Start(P,shared)
include("ResearchChair")
SPCResearchChair.Start(P,shared)
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

include("GreatWorkFacts")
SPCGreatWorkFacts.Start(P,shared)
include('CultureAesthetic')
SPCCultureAesthetic.Start(P,shared)

include("Dialogue")
SPCDialogue.Start(P,shared)

include("GreatWorkAdjacency")
SPCGWAdjacency.Start(P,shared,{retired=true})
include('CultureMeaning')
SPCCultureMeaning.Start(P,shared)
include('CultureInspirationProbe')
SPCCultureInspirationProbe.Start(P,shared,{retired=true})
include('CultureInspiration')
SPCCultureInspiration.Start(P,shared)

include("CommerceConvergence")
SPCCommerceConvergence.Start(P,shared)

-- B067: ownership work is isolated for the self-founded-city playable scope.
-- Keep source and saved ledgers intact; no inheritance/backup listeners are installed.
shared.CityInheritanceRead=nil
shared.InheritanceShadow=nil
shared.CityInheritance=nil
shared.OnPermanentCityWrite=nil
shared.InheritanceIsolation=true

-- Formal Claim must not depend on initialization of optional historical experiments.
local claimOK,claimError=pcall(function()include("ClaimProjects");SPCClaimProjects.Start(P,shared)end)
if not claimOK then
 shared.ClaimProjects=shared.ClaimProjects or {views={},revision=0}
 shared.ClaimProjects.startupError=tostring(claimError):gsub('^.-:%d+: ',''):match('[^\r\n]+')
 print('[SPC][Claim startup] '..tostring(claimError))
end

-- Independent read-only evidence; never start the isolated inheritance writers.
SPCCityIdentityRead.Start(P,shared)

include("CityIdentityExperiment")
include("CityIdentityMapping")
SPCCityIdentityMapping.Start(P,shared)

include("TimedProductionProbe")
SPCTimedProductionProbe.Start(P,shared)

include("OverflowStorageProbe")
SPCOverflowStorageProbe.Start(P,shared)

include("ProjectTurnObservation")
SPCProjectTurnObservation.Start(P,shared)
include("TimedProject")
SPCTimedProject.Start(P,shared)

include("NetworkIsolation")
SPCNetworkIsolation.Start(P,shared)
SPCPerformance.StartMemory(P,shared)
