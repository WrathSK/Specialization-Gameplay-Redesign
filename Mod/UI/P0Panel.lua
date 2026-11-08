include("BoostGreatWorkRead")
include("Probe")
include("RuntimeGC")
include("GPPReadout")
pcall(include,"CultureDiagnostics") -- optional, never used by report/business decisions
include("InspirationReadout")
include("Lv4CopyRead")
local P=SPCP0
local projectReadPulse
local pendingToken
local readings={}
local localReport
local page=1
local pageAction,pageCity
local request
local uiStage="READY"
local function status(s) Controls.Status:SetText(s);if Controls.ReportScroll then Controls.ReportScroll:CalculateSize();Controls.ReportScroll:ReprocessAnchoring() end end
local function trace(s)
  uiStage=s
  print("[SPC]["..P.VERSION.."][UI] "..s)
  status(P.VERSION.." | "..s)
end
local pendingAction
local meaningReadReference
local meaningResponseToken,meaningResponseText,meaningResponseReference,meaningResponseTurn
local function displayResponse()
  local data=ExposedMembers.SPC_P0 or {}
  if pendingToken and data.Version==P.VERSION and data.LastToken==pendingToken then
    local report=tostring(data.Snapshot)
    if pendingAction and pendingAction:find('^INSPIRE_') then report=report..'\n'..SPCInspirationReadout.RenderAutomatic(P,data.CultureInspirationView,pendingToken,pendingAction=='INSPIRE_DETAIL') end
    if pendingAction=='MEMORY_BEGIN' or pendingAction=='MEMORY_READ' then
     local heap=SPCRuntimeGC and SPCRuntimeGC.Heap()
     report=report..'\nUI调用处 Lua（堆是否独立未证，勿相加）：'..(heap and string.format('%.2f MiB',heap) or '不可用')
    end
    if pendingAction=="LV2_GPP_READ" then
      report=SPCGPPReadout.Render(P,report);localReport=report;print("[SPC][B035][UI_RATE] "..report)
      pcall(function()local d=SPCCultureDiagnostics;if d and d.ENABLED then
       d.ObserveGPPUI(P,pendingToken,pageCity,report:match('city=%d+ (%u+) ACTIVE='))end end)
    end
    if pendingAction=="LV4_PERCENT_READ" then
      local f=data.Lv4PercentRead
      local ok,native=pcall(function()
        assert(f and f.owner==Game.GetLocalPlayer() and f.cityID==pageCity,'READ_CITY_CHANGED')
        local city=Players[f.owner]:GetCities():FindID(f.cityID)
        local yieldType=f.kind=='RESEARCH' and 'YIELD_SCIENCE' or (f.kind=='CULTURE' and 'YIELD_CULTURE')
        if not yieldType then return '该专业无本项加成。' end
        return city:GetYieldToolTip(GameInfo.Yields[yieldType].Index)
      end)
      local text=ok and tostring(native) or ('原生明细读取未完成：'..tostring(native))
      report=report..'\n\n原生城市产出明细：\n'..text
      localReport=report;print('[SPC][B048][NATIVE_YIELD] '..report)
    end
    if pendingAction=="LV4_COPY_READ" then
      local m=data.Lv4CopyRead
      if m and m.token==pendingToken and m.cityID==pageCity then report=report.."\n\n"..SPCLv4CopyRead.Render(P,m)
      else report='Lv4读取未完成：城市或请求已变化。' end
      localReport=report;print('[SPC][B049][COPY] '..report)
    end
    if pendingAction=='BOOST_READ' or pendingAction=='BOOST_BASELINE' then
      report=report..'\n'..SPCBoostGreatWorkRead.Boost(P,pendingAction=='BOOST_BASELINE');localReport=report
    elseif pendingAction and pendingAction:find('^CULTURE_MEANING_') then
      local v=data.CultureMeaningView
      local c=Players[Game.GetLocalPlayer()]:GetCities():FindID(pageCity)
      if c and v and v.token==pendingToken then
        local ref=SPCNetworkInput.Reference(c);local turn=Game.GetCurrentGameTurn()
        local selected=UI.GetHeadSelectedCity()
        local selectedMatch=not (v.diagnostic or v.productionOnly or v.finalValues) or selected and selected:GetOwner()==c:GetOwner() and SPCNetworkInput.Reference(selected)==ref
        if meaningResponseToken~=pendingToken and selectedMatch then
          if v.diagnostic then
            meaningResponseText=SPCBoostGreatWorkRead.ProductionDiagnostic(P,c,v,pendingAction=='CULTURE_MEANING_DIAGNOSTIC_ADVANCE',pendingToken,meaningReadReference,pendingAction=='CULTURE_MEANING_DIAGNOSTIC_READ')
          else
            meaningResponseText=SPCBoostGreatWorkRead.Meaning(P,c,v,pendingAction=='CULTURE_MEANING_ADVANCE' or pendingAction=='CULTURE_MEANING_GATE_ADVANCE')
            if (v.productionOnly or v.finalValues) and pendingAction=='CULTURE_MEANING_READ' then
              local detail=SPCBoostGreatWorkRead.Modifiers(P,c,v,pendingToken,meaningReadReference)
              meaningResponseText=meaningResponseText..'\n'..(v.finalValues and SPCBoostGreatWorkRead.ModifierSummary(pendingToken) or detail)
            end
          end
          meaningResponseToken=pendingToken;meaningResponseReference=ref;meaningResponseTurn=turn
        end
        if selectedMatch and ref==meaningResponseReference and ref==v.reference and turn==meaningResponseTurn then
          report=report..'\n'..meaningResponseText
        else
          SPCBoostGreatWorkRead.ClearMeaningRead();SPCBoostGreatWorkRead.ClearModifierRead()
          meaningResponseToken=pendingToken;meaningResponseText=nil;meaningResponseReference=nil;meaningResponseTurn=nil -- Consume stale token; never replay or rescan it.
          report=report..'\n本次原生报告已过期；重新右键读取，不复用旧差值。'
        end
      end
      localReport=report
    elseif pendingAction and (pendingAction:find('^GW_') or pendingAction:find('^DIALOGUE_')) then
      local c=Players[Game.GetLocalPlayer()]:GetCities():FindID(pageCity)
      if c then report=report..'\n'..SPCBoostGreatWorkRead.Works(P,c,pendingAction=='GW_BASELINE') end
      localReport=report
    end
    readings[(pendingAction and pendingAction:find('^CULTURE_MEANING_')) and 'CULTURE_MEANING' or (pendingAction and pendingAction:find('^MEMORY_GC_')) and 'MEMORY_GC' or ((pendingAction or "READ")..":"..tostring(pageCity)..":"..tostring(page))]=report
    status(P.VERSION.." | ACK | "..report:gsub("\n","[NEWLINE]"))
    return true
  end
  if pendingToken and data.RequestToken==pendingToken and data.Version==P.VERSION
    and type(data.Stage)=="string" and data.Stage:sub(1,5)=="ERROR" then
    status(P.VERSION.." | READ FAILED: "..P.Scalar(pendingAction).."[NEWLINE]At: "..P.Scalar(data.FailureAt)
      .."[NEWLINE]"..P.Scalar(data.Stage):gsub("\n","[NEWLINE]"))
    return true
  end
  return false
end
local function waitForResponse()
  if displayResponse() then return end
  local elapsed=0
  ContextPtr:SetUpdate(function(dt)
    elapsed=elapsed+dt
    if displayResponse() then ContextPtr:ClearUpdate()
    elseif elapsed>=10 then
      ContextPtr:ClearUpdate()
      status(P.VERSION.." | NO RESPONSE: "..P.Scalar(pendingAction).."[NEWLINE]Click Show / Copy to check a late response.")
    end
  end)
end
request=function(action,advance)
  meaningResponseToken=nil;meaningResponseText=nil;meaningResponseReference=nil;meaningResponseTurn=nil
  SPCBoostGreatWorkRead.ClearModifierRead()
  meaningReadReference=nil
  if (pendingAction=='CULTURE_MEANING_READ' or pendingAction=='CULTURE_MEANING_DIAGNOSTIC_READ') then readings.CULTURE_MEANING=nil;localReport=nil end
  ContextPtr:ClearUpdate()
  local playerID=Game.GetLocalPlayer()
  local eligible,reason=P.IsTestPlayer(playerID)
  if not eligible then trace("玩家资格检查未通过："..tostring(reason));return end
  local storageAction=action=='EVENT_ORDER_TOGGLE' or action=='NETWORK_ISOLATE' or action=='NETWORK_ISOLATION_READ' or action=='MEMORY_GC_READ' or action=='MEMORY_GC_COLLECT' or action=='MEMORY_GC_AUTO_ON' or action=='MEMORY_GC_AUTO_OFF' or action=="IDENTITY_EXPERIMENT_READ" or action=="IDENTITY_COMPARE" or action=="IDENTITY_DETAIL" or action=="SHADOW_READ" or action=="INHERIT_READ"
  local city=not storageAction and UI.GetHeadSelectedCity() or nil
  local investmentUnitID,investmentPlanToken
  if action=="INVEST_PREPARE" then
    local unit=UI.GetHeadSelectedUnit()
    if not unit or unit:GetOwner()~=playerID then trace("Select an owned Settler at a city center.");return end
    city=CityManager.GetCityAt(unit:GetX(),unit:GetY());investmentUnitID=unit:GetID()
  elseif action=="INVEST_CONFIRM" then
    local preview=ExposedMembers.SPC_P0 and ExposedMembers.SPC_P0.InvestmentPreview
    if not preview or preview.owner~=playerID then trace("Prepare an investment first.");return end
    city=Players[playerID]:GetCities():FindID(preview.cityID);investmentPlanToken=preview.token
  end
  if not storageAction and (not city or city:GetOwner()~=playerID) then trace("Select an owned test city.");return end
  if advance and pageAction==action and city and pageCity==city:GetID() then page=page%512+1 else page=1 end
  pageAction=action;pageCity=city and city:GetID();localReport=nil
  ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
  pendingToken=P.VERSION..":"..tostring(Game.GetCurrentGameTurn())..":"..tostring(ExposedMembers.SPC_P0_UISequence)
  pendingAction=action
  if action=='CULTURE_MEANING_READ' or action=='CULTURE_MEANING_DIAGNOSTIC_READ' then meaningReadReference=SPCNetworkInput.Reference(city)end
  trace("BEFORE_DISPATCH "..action.." city="..tostring(city and city:GetID()))
  local packet={OnStart="SPC_P0_Request",Action=action,Token=pendingToken,CityID=city and city:GetID(),Page=page,UnitID=investmentUnitID,PlanToken=investmentPlanToken}
  if action=='NETWORK_ISOLATE' then
    local g=ExposedMembers.SPC_P0;local bridge=g and g.NetworkBridge
    local epoch=bridge and bridge.epoch
    local ok,err=pcall(function()
      assert(g and g.Version==P.VERSION and bridge.ready,'Gameplay尚未就绪')
      for _,key in ipairs({'SPC_P0_BackgroundRoutes','SPC_CopyBackground','SPC_DiscountEligibility'}) do
        local u=ExposedMembers[key];assert(u and type(u.StopNetwork)=='function','UI未就绪：'..key)
        assert(u.StopNetwork(epoch)==true,'UI退出未确认：'..key)
      end
    end)
    if not ok then pendingToken=nil;status('Network隔离未启动；停止本次对照，冷启动原存档。\n'..tostring(err));return end
    packet.Epoch=epoch
  end
  local ok,err=pcall(UI.RequestPlayerOperation,playerID,PlayerOperations.EXECUTE_SCRIPT,packet)
  trace(ok and ("READING "..action) or ("DISPATCH_ERROR "..P.Scalar(err)))
  if ok then waitForResponse() end
end
local function copy()
  if (pendingAction=='CULTURE_MEANING_READ' or pendingAction=='CULTURE_MEANING_DIAGNOSTIC_READ') then
    if displayResponse() and localReport then
      print('[SPC][MEANING_READ] '..P.VERSION..'\n'..localReport..'\n'..(SPCBoostGreatWorkRead.ModifierDetails(pendingToken) or ''))
      status('本次诊断报告已写入Lua.log；也可直接截图。')
    else status('尚无本次意义延展回复；请稍后重新右键读取。')end
    return
  end
  local lines={'SPC_DIAGNOSTIC_REPORT_BEGIN',P.VERSION,'turn='..Game.GetCurrentGameTurn()}
  local c=UI.GetHeadSelectedCity();local u=UI.GetHeadSelectedUnit()
  lines[#lines+1]='city='..tostring(c and c:GetID())..' unit='..tostring(u and u:GetID())
  for k,v in pairs(readings) do lines[#lines+1]='['..k..']\n'..v end
  if localReport then lines[#lines+1]='[LATEST UI]\n'..localReport end
  local seen={};local count=0
  local function dump(path,v,depth)
    local t=type(v)
    if t=='function' or t=='userdata' or t=='thread' then return end
    if count>=12000 then return end
    if t=='table' then
      if seen[v] then return end;seen[v]=true
      if depth>12 then lines[#lines+1]=path..'=<depth limit>';return end
      for k,x in pairs(v) do if type(k)=='string' or type(k)=='number' then dump(path..'.'..tostring(k),x,depth+1) end end
    else count=count+1;lines[#lines+1]=path..'='..tostring(v) end
  end
  dump('GAME',ExposedMembers.SPC_P0 or {},0)
  dump('ROUTES_UI',ExposedMembers.SPC_P0_BackgroundRoutes or {},0)
  dump('COLLECTION_UI',ExposedMembers.SPC_DialogueBackground or {},0)
  dump('UI_LOG_REPETITIONS',ExposedMembers.SPC_UILog or {},0)
  lines[#lines+1]='TARGETS='..tostring(ExposedMembers.SPC_TargetMarkerStatus)
  lines[#lines+1]='UNIT='..tostring(ExposedMembers.SPC_UnitPanelStatus)
  lines[#lines+1]='scalar_count='..count..(count>=12000 and ' REPORT_LIMIT_REACHED' or '')
  lines[#lines+1]='SPC_DIAGNOSTIC_REPORT_END'
  for _,line in ipairs(lines) do print(line) end
  status('诊断报告已输出到游戏 Lua.log。[NEWLINE]请保存该日志后回传；不依赖剪贴板。[NEWLINE]包含已读取报告与当前后台缓存，不会重建或修改游戏状态。')
end

local entryHeader,entryWidth,anchorWarning
local function placeEntry()
  if not entryHeader then
    entryHeader=ContextPtr:LookUpControl('/InGame/WorldTracker/WorldTrackerHeader')
    if entryHeader then Controls.OpenButton:ChangeParent(entryHeader)
    elseif not anchorWarning then
      anchorWarning=true;print('[SPC][UI_ANCHOR] WorldTrackerHeader unavailable; upper-left fallback')
    end
  end
  if entryHeader then
    local width=entryHeader:GetSizeX()
    if width~=entryWidth then entryWidth=width;Controls.OpenButton:SetOffsetVal(width+8,0) end
  end
end
local function cancelMeaningReply()
  if pendingAction and pendingAction:match('^CULTURE_MEANING_') then
    ContextPtr:ClearUpdate();pendingToken=nil;pendingAction=nil;localReport=nil
    readings.CULTURE_MEANING=nil;meaningReadReference=nil
  end
end
local function showRoot()
  cancelMeaningReply()
  SPCBoostGreatWorkRead.ClearModifierRead();SPCBoostGreatWorkRead.ClearMeaningRead()
  meaningResponseToken=nil;meaningResponseText=nil;meaningResponseReference=nil;meaningResponseTurn=nil
  local enabled=P.IsTestPlayer(Game.GetLocalPlayer())
  ContextPtr:SetHide(not enabled);placeEntry();Controls.OpenButton:SetHide(not enabled)
end
local function closeWindow()
  Controls.Window:SetHide(true);SPCBoostGreatWorkRead.ClearModifierRead();SPCBoostGreatWorkRead.ClearMeaningRead()
  meaningResponseToken=nil;meaningResponseText=nil;meaningResponseReference=nil;meaningResponseTurn=nil
  cancelMeaningReply() -- A late ACK cannot recreate a released diagnostic baseline.
end
local function initialize()
  -- Explicit labels bypass GridButton style-owned text rendering.
  Controls.CompletenessButtonCaption:SetText('科研基础设施')
  Controls.CompletenessButton:SetToolTipString('科研基础设施')
  Controls.OpenButtonCaption:SetText('专业化诊断')
  Controls.OpenButton:SetToolTipString('专业化诊断')
  Controls.CloseButtonCaption:SetText('关闭')
  Controls.CloseButton:SetToolTipString('关闭')
  Controls.SourceYieldButtonCaption:SetText('城市专业 / 潜力')
  Controls.SourceYieldButton:SetToolTipString('城市专业 / 潜力')
  Controls.GovernorButtonCaption:SetText('总督条件')
  Controls.GovernorButton:SetToolTipString('总督条件')
  Controls.SpecialistsButtonCaption:SetText('专家与岗位')
  Controls.SpecialistsButton:SetToolTipString('专家与岗位')
  Controls.MeaningConfigButtonCaption:SetText(Locale.Lookup('LOC_SPC_INSPIRATION_BUTTON'))
  Controls.MeaningConfigButton:SetToolTipString(Locale.Lookup('LOC_SPC_INSPIRATION_HINT'))
  Controls.MeaningConfigButton:SetHide(false)
  Controls.MeaningProbeButtonCaption:SetText(Locale.Lookup('LOC_SPC_CULTURE_MEANING_AUTO'))
  Controls.MeaningProbeButton:SetToolTipString(Locale.Lookup('LOC_SPC_CULTURE_MEANING_AUTO_HINT'))
  Controls.AestheticButtonCaption:SetText(Locale.Lookup('LOC_SPC_CULTURE_AESTHETIC'))
  Controls.AestheticButton:SetToolTipString('左键：本城时代数、普通建筑与旅游配置；右键：时代和建筑组成，继续右键翻页。配置不是原生实测。')
  Controls.GWReadButtonCaption:SetText(Locale.Lookup('LOC_SPC_GREAT_WORK_FACTS'))
  Controls.GWReadButton:SetToolTipString('左键：本城巨作件数与历史时代；右键：作品组成和国内来源，继续右键翻页。只读确认缓存，不重新采集。')
  Controls.Lv4CopyButtonCaption:SetText('四级区域收益')
  Controls.Lv4CopyButton:SetToolTipString('四级区域收益')
  Controls.BackgroundRoutesButtonCaption:SetText('当前商路')
  Controls.BackgroundRoutesButton:SetToolTipString('当前商路')
  Controls.NetworkButtonCaption:SetText('网络概况')
  Controls.NetworkButton:SetToolTipString('网络概况')
  Controls.CarrierStepButtonCaption:SetText('网络来源 / 接收')
  Controls.CarrierStepButton:SetToolTipString('只读公共网络来源、中心、本城接收和商路方向；再次点击翻页。关键记录写入有界日志。')
  Controls.BoostReadButtonCaption:SetText('尤里卡 / 鼓舞')
  Controls.BoostReadButton:SetToolTipString('尤里卡 / 鼓舞')
  Controls.CommerceREADButtonCaption:SetText(Locale.Lookup('LOC_SPC_COMMERCE_TITLE'))
  Controls.CommerceREADButton:SetToolTipString(Locale.Lookup('LOC_SPC_COMMERCE_OPEN_HELP'))
  Controls.TemplatesButtonCaption:SetText(Locale.Lookup('LOC_SPC_INDUSTRY_HISTORY_BUTTON'))
  Controls.TemplatesButton:SetToolTipString(Locale.Lookup('LOC_SPC_INDUSTRY_HISTORY_HINT')..'\n左键同时查看工程传统研习L/E与巨构工程学；右键：工业标准化，再次右键翻页。')
  Controls.CopyButtonCaption:SetText('写入诊断日志')
  Controls.CopyButton:SetToolTipString('写入诊断日志')
  showRoot();Controls.Window:SetHide(true)
  Controls.Title:SetText("SPC "..P.VERSION.." | Specialization diagnostics")
  Controls.OpenButton:RegisterCallback(Mouse.eLClick,function() Controls.Window:SetHide(false) end)
  Controls.OpenButton:RegisterCallback(Mouse.eRClick,function() Controls.Window:SetHide(false);request('EVENT_ORDER_TOGGLE') end)
  Controls.OpenButton:SetToolTipString('左键打开专业化诊断；右键独立开关事件顺序记录（每次加载默认关闭，前6个本地回合有效）。')
  Controls.CloseButton:RegisterCallback(Mouse.eLClick,closeWindow)
  Controls.CultureInsightsButtonCaption:SetText(Locale.Lookup('LOC_SPC_CULTURE_INSIGHTS_BUTTON'))
  Controls.CultureInsightsButton:SetToolTipString(Locale.Lookup('LOC_SPC_CULTURE_INSIGHTS_TOOLTIP'))
  Controls.CultureInsightsButton:RegisterCallback(Mouse.eLClick,function() request('CULTURE_INSIGHTS_READ') end)
  Controls.ExpeditionGateButtonCaption:SetText(Locale.Lookup('LOC_SPC_EXPEDITION_GATE_OPEN'))
  -- B220: movement comparison deferred; retain only the normal diagnostic entry.
  Controls.ExpeditionGateButton:RegisterCallback(Mouse.eLClick,function()
    if ExposedMembers.SPC_ExpeditionGateUIVersion~=P.VERSION then
      status(Locale.Lookup('LOC_SPC_EXPEDITION_GATE_UI_UNAVAILABLE',P.VERSION));return
    end
    -- UI-only synchronous acknowledgement; never hide P0 on a stale ready flag
    -- or a failed/missing listener. No Gameplay request is retried here.
    ExposedMembers.SPC_ExpeditionGateUIOpenVersion=nil
    local ok,err=pcall(function()LuaEvents.SPC_ExpeditionGateOpen()end)
    if not ok or ExposedMembers.SPC_ExpeditionGateUIOpenVersion~=P.VERSION then
      if not ok then print('[SPC][N1_UI_OPEN] '..tostring(err):sub(1,240))end
      status(Locale.Lookup('LOC_SPC_EXPEDITION_GATE_UI_OPEN_FAILED'));return
    end
    closeWindow()
  end)
  Controls.CarrierStepButton:RegisterCallback(Mouse.eLClick,function() request("NETWORK_DETAIL",true) end)
  Controls.CommerceREADButton:RegisterCallback(Mouse.eLClick,function() request("COMMERCE_READ") end)
  Controls.InheritReadButton:RegisterCallback(Mouse.eLClick,function() request("PROGRESSION_STORE_READ") end)
  Controls.InheritReadButtonCaption:SetText('E2往返')
  Controls.InheritReadButton:SetToolTipString('左键：读取选中城市的专业、潜力和投资；新城自动登记，无需迁移。')
  Controls.SourceYieldButton:RegisterCallback(Mouse.eLClick,function() request("PROGRESSION_READ") end)
  Controls.Lv2HousingButton:RegisterCallback(Mouse.eLClick,function() request("LV2_HOUSING_READ") end)
  Controls.InvestPrepareButton:RegisterCallback(Mouse.eLClick,function() request("INVEST_PREPARE") end)
  Controls.InvestConfirmButton:RegisterCallback(Mouse.eLClick,function() request("INVEST_CONFIRM") end)
  Controls.NetworkButtonCaption:SetText('网络概况')
  Controls.NetworkButton:RegisterCallback(Mouse.eLClick,function() request('NETWORK_READ') end)
  Controls.NetworkButton:RegisterCallback(Mouse.eRClick,function() request('NETWORK_DETAIL') end)
  Controls.NetworkButton:SetToolTipString('只读公共网络商路与拓扑，并单独显示文化收益状态；文化模块失败仍可查看。右键查看来源，明细按钮翻页。')
  Controls.Lv4PercentButton:RegisterCallback(Mouse.eLClick,function() request("LV4_PERCENT_READ") end)
  Controls.ResearchReadButton:RegisterCallback(Mouse.eLClick,function() request("RESEARCH_READ") end)
  Controls.BoostReadButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_READ') end)
  Controls.BoostBaseButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_BASELINE') end)
  Controls.GWBaselineButton:RegisterCallback(Mouse.eLClick,function() request('GW_BASELINE') end)
  Controls.MeaningConfigButton:RegisterCallback(Mouse.eLClick,function() request('INSPIRE_STATUS') end)
  Controls.MeaningConfigButton:RegisterCallback(Mouse.eRClick,function() request('INSPIRE_DETAIL') end)
  Controls.MeaningProbeButton:RegisterCallback(Mouse.eLClick,function() request('CULTURE_MEANING_STATUS') end)
  Controls.MeaningProbeButton:RegisterCallback(Mouse.eRClick,function() request('CULTURE_MEANING_STATUS') end)
  Controls.AestheticButton:RegisterCallback(Mouse.eLClick,function() request('CULTURE_AESTHETIC_READ') end)
  Controls.AestheticButton:RegisterCallback(Mouse.eRClick,function() request('CULTURE_AESTHETIC_DETAIL',true) end)
  Controls.GWReadButton:RegisterCallback(Mouse.eLClick,function() request('GREAT_WORK_FACTS_READ') end)
  Controls.GWReadButton:RegisterCallback(Mouse.eRClick,function() request('GREAT_WORK_FACTS_DETAIL',true) end)
  Controls.DialogueProjectCaption:SetText(Locale.Lookup('LOC_SPC_DIALOGUE_PROJECT_REPORT'))
  Controls.GWCityButton:SetToolTipString(Locale.Lookup('LOC_SPC_DIALOGUE_CARRIER_HINT'))
  Controls.GWCityButton:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_PROJECT_READ') end)
  Controls.GWCityButton:RegisterCallback(Mouse.eRClick,function() request('DIALOGUE_PROJECT_READ') end)
  Controls.TemplatesButton:RegisterCallback(Mouse.eLClick,function() request("INDUSTRY_HISTORY_READ",true) end)
  Controls.TemplatesButton:RegisterCallback(Mouse.eRClick,function() request("DISCOUNT_READ",true) end)
  Controls.Lv4CopyButton:RegisterCallback(Mouse.eLClick,function() request("LV4_COPY_READ") end)
  Controls.BackgroundRoutesButton:RegisterCallback(Mouse.eLClick,function()
    ContextPtr:ClearUpdate();pendingToken=nil
    if not P.IsTestPlayer(Game.GetLocalPlayer()) then return end
    local data=ExposedMembers.SPC_P0_BackgroundRoutes
    localReport=P.VERSION.." | 后台路线（只看已有缓存）\n"
      ..((data and data.version==P.VERSION and data.text) or "没有后台记录。请截图；此按钮不会启动读取。")
    status(localReport:gsub("\n","[NEWLINE]"))
  end)
  Controls.GovernorButton:RegisterCallback(Mouse.eLClick,function() request("GOVERNOR") end)
  Controls.SpecialistsButton:RegisterCallback(Mouse.eLClick,function() request("SPECIALISTS") end)
  Controls.SpecialistsButton:RegisterCallback(Mouse.eRClick,function() request('LV2_GPP_READ') end)
  Controls.SpecialistsButton:SetToolTipString('左键：专家与岗位。右键：二级伟人点数与实际/锁定人数只读对照。')
  Controls.CopyButton:RegisterCallback(Mouse.eLClick,copy)
  status(Locale.Lookup('LOC_SPC_EXPEDITION_GATE_PANEL_HINT'))
end
local oldInitialize=initialize
initialize=function()
 oldInitialize()
 Controls.DP05ButtonCaption:SetText('主持 / 学术传统')
 Controls.DP05Button:RegisterCallback(Mouse.eLClick,function() request('RESEARCH_CHAIR_DETAIL') end)
 Controls.DP05Button:RegisterCallback(Mouse.eRClick,function() request('RESEARCH_TRADITION_READ') end)
 Controls.DP05Button:SetToolTipString('左键：学术主持及逐建筑明细；右键：学术传统年龄、门槛与本项收益配置（只读）。')
 Controls.DP03ButtonCaption:SetText('学以致用')
 Controls.DP03Button:RegisterCallback(Mouse.eLClick,function() request('RESEARCH_APPLY_READ') end)
 Controls.DP03Button:RegisterCallback(Mouse.eRClick,function() request('RESEARCH_APPLY_DETAIL') end)
 Controls.DP03Button:SetToolTipString('左键：每名专家floor及全城预期；右键：领域D与建筑组成。只读。')
 Controls.DPReadButtonCaption:SetText('跨学科研究')
 Controls.DPReadButton:RegisterCallback(Mouse.eLClick,function() request('RESEARCH_CROSS_READ') end)
 Controls.DPReadButton:RegisterCallback(Mouse.eRClick,function() request('RESEARCH_CROSS_DETAIL') end)
 Controls.DPReadButton:SetToolTipString('左键：BASE×50%及临时floor；右键：各区域BASE组成。只读，不开启实验。')
 Controls.CompletenessButton:RegisterCallback(Mouse.eLClick,function() request("COMPLETENESS_READ") end)
 if Mouse.eRClick then Controls.CompletenessButton:RegisterCallback(Mouse.eRClick,function() request("RESEARCH_INFRA_DETAIL") end) end
 Controls.CompletenessButton:SetToolTipString("左键：科研基础设施摘要；右键：学院建筑组成")
 Controls.GWAReadButtonCaption:SetText("内存观测")
 Controls.GWAReadButton:RegisterCallback(Mouse.eLClick,function()request('MEMORY_BEGIN')end)
 Controls.GWAReadButton:RegisterCallback(Mouse.eRClick,function()request('MEMORY_READ')end)
 Controls.GWAReadButton:SetToolTipString('左键开始一次短观测；右键读取事件用量。最多6回合，不清内存、不改存档。')
 include("ProjectTurnRead")
 SPCProjectTurnRead.New()
 include("TimedProjectRead")
 local timer=SPCTimedProjectRead.New(P,function(s) localReport=s;status(s) end,function(...)return UI.RequestPlayerOperation(...)end)
 projectReadPulse=timer.Pulse
 Events.GameCoreEventPublishComplete.Add(projectReadPulse)
 Controls.TurnProbeReadCaption:SetText("自动项目报告")
 Controls.TurnProbeArmCaption:SetText('GC试运行')
 Controls.PerformanceSnapshotButton:RegisterCallback(Mouse.eLClick,function()request('MEMORY_GC_READ')end)
 Controls.PerformanceSnapshotButton:RegisterCallback(Mouse.eRClick,function()
  local g=ExposedMembers.SPC_P0;local d=g and g.MemoryObservation;local a=d and d.AutoGC
  request(a and a.enabled==false and 'MEMORY_GC_AUTO_ON' or 'MEMORY_GC_AUTO_OFF')
 end)
 Controls.PerformanceSnapshotButton:SetToolTipString('受控自动GC试运行。左键只读结果；右键开启/关闭本次加载的自动调用，不会立即回收。不修改专业数据；失败后保持停用。')
 local function projectAction(fn)
  ContextPtr:ClearUpdate();pendingToken=nil;pendingAction=nil;fn()
 end
 Controls.PerformanceReadButton:RegisterCallback(Mouse.eLClick,function()projectAction(timer.Read)end)
 Controls.PerformanceReadButton:RegisterCallback(Mouse.eRClick,function()projectAction(timer.Cancel)end)
 Controls.PerformanceReadButton:SetToolTipString('左键只读计时报告；右键取消计时，不清空生产。已调用完成后不重试。')

end
ContextPtr:SetInitHandler(initialize)
Events.LoadScreenClose.Add(showRoot)
Events.SystemUpdateUI.Add(placeEntry)
ContextPtr:SetShutdown(function() SPCBoostGreatWorkRead.ClearModifierRead();SPCBoostGreatWorkRead.ClearMeaningRead();meaningResponseToken=nil;meaningResponseText=nil;meaningResponseReference=nil;meaningResponseTurn=nil;if projectReadPulse then Events.GameCoreEventPublishComplete.Remove(projectReadPulse) end;Controls.OpenButton:SetHide(true);Events.SystemUpdateUI.Remove(placeEntry);ContextPtr:ClearUpdate();Events.LoadScreenClose.Remove(showRoot) end)
