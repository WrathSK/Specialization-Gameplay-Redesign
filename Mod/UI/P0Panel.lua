include("OverflowStorageRead")
include("BoostGreatWorkRead")
include("PurchaseProbeRead")
include("Probe")
include("GPPReadout")
include("Lv4CopyRead")
include("CityIdentityEvidence")
local P=SPCP0
local identityEvidence=SPCCityIdentityEvidence.New(P)
local projectReadPulse
local pendingToken,baseline
local readings={}
local localReport
local page=1
local pageAction,pageCity
local request
local uiStage="READY"
local function status(s) Controls.Status:SetText(s);if Controls.ReportScroll then Controls.ReportScroll:CalculateSize();Controls.ReportScroll:ReprocessAnchoring() end end
local overflowRead=SPCOverflowStorageRead.New(P,function(s) localReport=s;status(s) end,function(...) return UI.RequestPlayerOperation(...) end)
local function overflowPulse() overflowRead.Pulse() end
Events.GameCoreEventPublishComplete.Add(overflowPulse)
local function trace(s)
  uiStage=s
  print("[SPC]["..P.VERSION.."][UI] "..s)
  status(P.VERSION.." | "..s)
end
local pendingAction
local gwaFlight
local function gwaDiagnostics()
  local d=ExposedMembers.SPC_P0 or {};local i=d.RequestIngress or {}
  local bg=ExposedMembers.SPC_DialogueBackground or {}
  return "后台模块="..tostring(d.GreatWorkAdjacency~=nil).." / 最近收到="..tostring(i.action).." / 本次已收到="..tostring(i.token==pendingToken).."[NEWLINE]相邻采样="..tostring(bg.adjacencyError or "未报告错误")
end
local function displayResponse()
  local data=ExposedMembers.SPC_P0 or {}
  if pendingToken and data.Version==P.VERSION and data.LastToken==pendingToken then
    local report=tostring(data.Snapshot)
    if pendingAction=='MEMORY_BEGIN' or pendingAction=='MEMORY_READ' then
     local heap=SPCPerformance.Heap and SPCPerformance.Heap()
     report=report..'\nUI调用处 Lua（堆是否独立未证，勿相加）：'..(heap and string.format('%.2f MiB',heap) or '不可用')
    end
    if pendingAction=="LV2_GPP_READ" then report=SPCGPPReadout.Render(P,report);localReport=report;print("[SPC][B035][UI_RATE] "..report) end
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
    if pendingAction and pendingAction:find('^PURCHASE_') then
      local c=Players[Game.GetLocalPlayer()]:GetCities():FindID(pageCity)
      if c then report=report.."\n"..SPCPurchaseProbeRead.Render(P,c) end
      localReport=report;print("[SPC][B053][PRICES] "..report)
    end
    if pendingAction=='BOOST_READ' or pendingAction=='BOOST_BASELINE' then
      report=report..'\n'..SPCBoostGreatWorkRead.Boost(P,pendingAction=='BOOST_BASELINE');localReport=report
    elseif pendingAction and pendingAction:find('^CULTURE_MEANING_') then
      local v=data.CultureMeaningView
      local c=Players[Game.GetLocalPlayer()]:GetCities():FindID(pageCity)
      if c and v and v.token==pendingToken then report=report..'\n'..SPCBoostGreatWorkRead.Meaning(P,c,v,pendingAction=='CULTURE_MEANING_ADVANCE')end
      localReport=report
    elseif pendingAction and pendingAction:find('^GWA_') then
      gwaFlight=nil
      local ok,native=pcall(function()
        local c=Players[Game.GetLocalPlayer()]:GetCities():FindID(pageCity)
        return c and SPCBoostGreatWorkRead.Adjacency(P,c) or '城市不可用'
      end)
      report=report..'\n'..tostring(native)
      report=report..'\n'..gwaDiagnostics()
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
-- B060 read/control requests are idempotent. Only an outstanding click may retry;
-- event pulses do not collect works or adjacency and never create a scan loop.
local function gwaPulse()
  local f=gwaFlight;if not f then return end
  if f.busy then P.Count('busy_skip');return end
  if displayResponse() then gwaFlight=nil;ContextPtr:ClearUpdate();return end
  f.pulses=f.pulses+1
  if f.pulses<3 then return end
  f.pulses=0
  if f.retries>=2 then
    gwaFlight=nil;ContextPtr:ClearUpdate()
    status(P.VERSION.." | 相邻请求未收到回复[NEWLINE]"..gwaDiagnostics())
    return
  end
  f.retries=f.retries+1;f.busy=true
  local ok,err=pcall(UI.RequestPlayerOperation,f.pid,PlayerOperations.EXECUTE_SCRIPT,f.packet)
  f.busy=false
  if displayResponse() then gwaFlight=nil;ContextPtr:ClearUpdate()
  elseif not ok then status('相邻发送失败：'..tostring(err)..'[NEWLINE]'..gwaDiagnostics()) end
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
  ContextPtr:ClearUpdate()
  gwaFlight=nil
  local playerID=Game.GetLocalPlayer()
  local eligible,reason=P.IsTestPlayer(playerID)
  if not eligible then trace("玩家资格检查未通过："..tostring(reason));return end
  local storageAction=action=='NETWORK_ISOLATE' or action=='NETWORK_ISOLATION_READ' or action=='MEMORY_GC_READ' or action=='MEMORY_GC_COLLECT' or action=='MEMORY_GC_AUTO_ON' or action=='MEMORY_GC_AUTO_OFF' or action=="CITY_SEQUENCE_READ" or action=="CITY_SEQUENCE_BEGIN" or action=="IDENTITY_EXPERIMENT_READ" or action=="IDENTITY_COMPARE" or action=="IDENTITY_DETAIL" or action=="UNIT_SITE_READ" or action=="SHADOW_READ" or action=="INHERIT_READ" or action=="STORAGE_READ" or action=="STORAGE_WRITE" or action=="ENVELOPE_READ" or action=="ENVELOPE_NEXT"
  local city=not storageAction and UI.GetHeadSelectedCity() or nil
  local investmentUnitID,investmentPlanToken
  if action=='CITY_SEQUENCE_BEGIN' then
    local u=UI.GetHeadSelectedUnit()
    if u and u:GetOwner()==playerID then investmentUnitID=u:GetID()
    else city=UI.GetHeadSelectedCity();if not city or city:GetOwner()~=playerID then status('先选中己方移民或城市。');return end end
  end
  if action=="UNIT_SITE_READ" then
    local u=UI.GetHeadSelectedUnit()
    if not u or u:GetOwner()~=playerID then status('请先选中己方移民或施工队。');return end
    investmentUnitID=u:GetID()
  end
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
  if advance and pageAction==action and ((action=="CITY_SEQUENCE_READ") or (city and pageCity==city:GetID())) then page=page%512+1 else page=1 end
  pageAction=action;pageCity=city and city:GetID();localReport=nil
  if action=="ADJACENCY" or action=="TRADE" then
    pendingToken=nil
    local last="START"
    local ok,value=pcall(P.NetworkProbe,city,action,function(v) last=v end,page)
    localReport=P.VERSION.." | UI "..(ok and "OBSERVATION\n"..value or "READ FAILED at "..last.."\n"..P.Scalar(value))
    status(localReport:gsub("\n","[NEWLINE]"));print(localReport);return
  end
  ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
  pendingToken=P.VERSION..":"..tostring(Game.GetCurrentGameTurn())..":"..tostring(ExposedMembers.SPC_P0_UISequence)
  pendingAction=action
  trace("BEFORE_DISPATCH "..action.." city="..tostring(city and city:GetID()))
  local envelope=ExposedMembers.SPC_P0 and ExposedMembers.SPC_P0.EnvelopeProbe
  local expectedStage=envelope and envelope.players[playerID] and envelope.players[playerID].step
  local packet={OnStart="SPC_P0_Request",Action=action,Token=pendingToken,ExpectedStage=action=="ENVELOPE_NEXT" and expectedStage or nil,CityID=city and city:GetID(),Page=page,UnitID=investmentUnitID,PlanToken=investmentPlanToken}
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
  if action:find('^GWA_') then gwaFlight={pid=playerID,packet=packet,pulses=0,retries=0,busy=true} end
  local ok,err=pcall(UI.RequestPlayerOperation,playerID,PlayerOperations.EXECUTE_SCRIPT,packet)
  if gwaFlight then gwaFlight.busy=false end
  trace(ok and ("READING "..action) or ("DISPATCH_ERROR "..P.Scalar(err)))
  if ok then waitForResponse() end
  if gwaFlight then status(P.VERSION.." | READING "..action.."[NEWLINE]"..gwaDiagnostics()) end
end
local function legacyCopy(asBaseline)
  if localReport then
    print(localReport)
    P.Call(UIManager,"SetClipboardString",localReport)
    status(localReport:gsub("\n","[NEWLINE]").."[NEWLINE]Clipboard delivery UNVERIFIED; screenshot is sufficient.")
    return
  end
  if not pendingToken then status("No reading requested. Select a city, then click Read governor or Read specialists.");return end
  local data=ExposedMembers.SPC_P0 or {}
  local matched=pendingToken~=nil and data.LastToken==pendingToken and data.Version==P.VERSION
  local full="SPC_P0_EXPORT_BEGIN\n"..P.VERSION.." ISOLATED_PROBES\n[UI] "..uiStage
    .."\nrequest="..P.Scalar(pendingToken).."\nresponse="..P.Scalar(data.LastToken)
    .."\nmatched="..tostring(matched).."\n[GAMEPLAY] stage="..P.Scalar(data.Stage)
    .."\n"..(matched and tostring(data.Snapshot) or "PENDING_OR_ERROR: previous snapshot excluded")
    .."\n"..table.concat(data.Events or {},"\n").."\nSPC_P0_EXPORT_END\n"
  if asBaseline and matched then baseline=full end
  local output=(baseline and not asBaseline and ("BASELINE\n"..baseline.."\nAFTER\n") or "")..full
  -- Export is small and scalar-only. Console logging is a fallback when available;
  -- a successful API invocation is not proof of OS clipboard delivery.
  print(output)
  local ok,result=P.Call(UIManager,"SetClipboardString",output)
  local delivery=(ok and result~=false) and "Clipboard requested; delivery UNVERIFIED. Screenshot ACK if paste is empty."
    or "Clipboard unavailable/rejected. Screenshot ACK; console export attempted."
  status((matched and "ACK | "..tostring(data.Snapshot):gsub("\n","[NEWLINE]") or "PENDING_OR_ERROR | "..P.Scalar(data.Stage))
    .."[NEWLINE]"..delivery)

end
local function copy()
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

local completionPage=1
local function showCompletion(older)
  ContextPtr:ClearUpdate();pendingToken=nil
  local pid=Game.GetLocalPlayer()
  if not P.IsTestPlayer(pid) then return end
  local data=(ExposedMembers.SPC_P0 or {}).CompletionProbe
  if not data or data.version~=P.VERSION then status(P.VERSION.." | 尚无完成事件探针记录；请截图版本号。");return end
  local b=data.players[pid] or {rows={},built=0,constructed=0,added=0,dropped=0,errors=0}
  local pages=math.max(1,math.ceil(#b.rows/2))
  completionPage=older and (completionPage%pages+1) or 1
  local lines={P.VERSION.." | 完成事件（只读已有记录） "..completionPage.."/"..pages,
    "建城="..b.built.." 完成通知="..b.constructed.." 区域加入="..b.added.." 错误="..b.errors.." 丢弃旧条目="..b.dropped,
    "CityBuilt="..tostring(data.hooks.CityBuilt).." Constructed="..tostring(data.hooks.OnDistrictConstructed),
    "Added="..tostring(data.hooks.DistrictAddedToMap).." Load="..tostring(data.hooks.LoadScreenClose).." / "..data.phase}
  local last=#b.rows-(completionPage-1)*2
  for i=last,math.max(1,last-1),-1 do lines[#lines+1]=b.rows[i].text end
  if #b.rows==0 then lines[#lines+1]="本次脚本加载后无记录；不代表城市从未建过区域。" end
  lines[#lines+1]="计数每次读档重置；未写专业/Potential。截图即可。"
  localReport=table.concat(lines,"\n");status(localReport:gsub("\n","[NEWLINE]"))
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
local function showRoot()
  local enabled=P.IsTestPlayer(Game.GetLocalPlayer())
  ContextPtr:SetHide(not enabled);placeEntry();Controls.OpenButton:SetHide(not enabled)
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
  Controls.MeaningProbeButtonCaption:SetText(Locale.Lookup('LOC_SPC_CULTURE_MEANING_PROBE'))
  Controls.MeaningProbeButton:SetToolTipString(Locale.Lookup('LOC_SPC_CULTURE_MEANING_PROBE_HINT'))
  Controls.AestheticButtonCaption:SetText(Locale.Lookup('LOC_SPC_CULTURE_AESTHETIC'))
  Controls.AestheticButton:SetToolTipString('左键：本城时代数、普通建筑与旅游配置；右键：时代和建筑组成，继续右键翻页。配置不是原生实测。')
  Controls.GWReadButtonCaption:SetText(Locale.Lookup('LOC_SPC_GREAT_WORK_FACTS'))
  Controls.GWReadButton:SetToolTipString('左键：本城巨作件数与历史时代；右键：作品组成和国内来源，继续右键翻页。只读确认缓存，不重新采集。')
  Controls.GWAReadButtonCaption:SetText('巨作相邻')
  Controls.GWAReadButton:SetToolTipString('巨作相邻')
  Controls.Lv4CopyButtonCaption:SetText('四级区域收益')
  Controls.Lv4CopyButton:SetToolTipString('四级区域收益')
  Controls.BackgroundRoutesButtonCaption:SetText('当前商路')
  Controls.BackgroundRoutesButton:SetToolTipString('当前商路')
  Controls.NetworkButtonCaption:SetText('网络概况')
  Controls.NetworkButton:SetToolTipString('网络概况')
  Controls.CarrierStepButtonCaption:SetText('网络来源 / 接收')
  Controls.CarrierStepButton:SetToolTipString('网络来源 / 接收')
  Controls.BoostReadButtonCaption:SetText('尤里卡 / 鼓舞')
  Controls.BoostReadButton:SetToolTipString('尤里卡 / 鼓舞')
  Controls.CommerceREADButtonCaption:SetText('商业四汇聚')
  Controls.CommerceREADButton:SetToolTipString('商业四汇聚')
  Controls.DiscountsButtonCaption:SetText('工业网络折扣')
  Controls.DiscountsButton:SetToolTipString('工业网络折扣')
  Controls.TemplatesButtonCaption:SetText('标准化模板')
  Controls.TemplatesButton:SetToolTipString('选中己方城市后读取永久标准化模板；重复点击翻页。只读，不改变模板、专业或收益。')
  Controls.UnitReadButtonCaption:SetText('移民 / 施工队')
  Controls.UnitReadButton:SetToolTipString('移民 / 施工队')
  Controls.CopyButtonCaption:SetText('写入诊断日志')
  Controls.CopyButton:SetToolTipString('写入诊断日志')
  showRoot();Controls.Window:SetHide(true)
  Controls.Title:SetText("SPC "..P.VERSION.." | Specialization diagnostics")
  Controls.OpenButton:RegisterCallback(Mouse.eLClick,function() Controls.Window:SetHide(false) end)
  Controls.CloseButton:RegisterCallback(Mouse.eLClick,function() Controls.Window:SetHide(true) end)
  Controls.QualificationButton:RegisterCallback(Mouse.eLClick,function()
    ContextPtr:ClearUpdate();pendingToken=nil
    local shared=ExposedMembers.SPC_P0 or {}
    local d=shared.QualificationProbe
    local pid=Game.GetLocalPlayer()
    localReport=P.VERSION.." | 当前名单与诊断许可（只看自动记录）\n"
    if shared.Version==P.VERSION and d and d.version==P.VERSION then
      localReport=localReport.."本玩家="..tostring(pid).." 诊断许可="..tostring(d.permissions[pid]).."\n"..d.text
    else localReport=localReport.."没有当前版本自动记录；按钮不会采样。" end
    status(localReport:gsub("\n","[NEWLINE]"))
  end)
  local unknownPage=0
  Controls.EligibilityUnknownButton:RegisterCallback(Mouse.eLClick,function()
    ContextPtr:ClearUpdate();pendingToken=nil
    local shared=ExposedMembers.SPC_P0 or {}
    local d=shared.EligibilityProbe
    local sample=d and d.samples.LOAD_CLOSE
    local lines={P.VERSION.." | 未知槽位（仅查看LOAD_CLOSE缓存）"}
    if shared.Version~=P.VERSION or not d or d.version~=P.VERSION or not sample then
      lines[#lines+1]="无当前版本加载结束记录；此按钮不会采样。"
    else
      local ids={}
      for pid,row in pairs(sample.rows) do if row.status=="UNKNOWN" then ids[#ids+1]=pid end end
      table.sort(ids)
      local pages=math.max(1,math.ceil(#ids/8))
      unknownPage=unknownPage%pages+1
      lines[#lines+1]="汇总="..sample.status.." 未知="..sample.unknown.." 页="..unknownPage.."/"..pages
      for i=(unknownPage-1)*8+1,math.min(#ids,unknownPage*8) do
        local pid=ids[i];local row=sample.rows[pid]
        local raw=tostring(row.reason or "NO_REASON")
        -- Known assert codes stay compact; full original reason stays in the cache/log.
        local code=raw:match("(CIV_NOT_READY)") or raw:match("(CONFIG_NOT_READY)")
          or raw:match("(PLAYER_NOT_READY)") or raw:match("(CARRIER_NOT_DEFINED)") or raw:match("(BAD_TRAIT_ROW)")
        lines[#lines+1]="player="..pid.." | "..(code or raw:sub(1,90))
      end
      if #ids==0 then lines[#lines+1]=sample.reason or "没有逐槽位UNKNOWN记录。" end
    end
    localReport=table.concat(lines,"\n");status(localReport:gsub("\n","[NEWLINE]"))
  end)
  Controls.EligibilityButton:RegisterCallback(Mouse.eLClick,function()
    ContextPtr:ClearUpdate();pendingToken=nil
    local pid=Game.GetLocalPlayer()
    local shared=ExposedMembers.SPC_P0 or {}
    local d=shared.EligibilityProbe
    local lines={P.VERSION.." | 启用资格（只看自动记录） 玩家="..tostring(pid)}
    if shared.Version~=P.VERSION or not d or d.version~=P.VERSION then
      lines[#lines+1]="没有当前版本记录；此按钮不会启动采样。"
    else
      lines[#lines+1]="LoadScreenClose="..tostring(d.hooks.LoadScreenClose)
      for _,phase in ipairs({"INITIALIZE","LOAD_CLOSE"}) do
        local sample=d.samples[phase]
        local row=sample and sample.rows[pid]
        lines[#lines+1]=phase.." | "..(row and row.status or "NO_RECORD")
          .." | "..(row and row.reason or (sample and sample.reason) or "等待自动采样")
        if sample then
          lines[#lines+1]="汇总="..sample.status.." 启用="..sample.enabled.." 未启用="..sample.disabled.." 未知="..sample.unknown
        end
      end
    end
    lines[#lines+1]="只读；未写资格或城市成果。截图即可。"
    localReport=table.concat(lines,"\n");status(localReport:gsub("\n","[NEWLINE]"))
  end)
  Controls.CityJournalButton:RegisterCallback(Mouse.eLClick,function() request("CITY_JOURNAL_READ") end)
  Controls.CompletionRecordButton:RegisterCallback(Mouse.eLClick,function() request("COMPLETION_RECORD_READ") end)
  Controls.BindingReadButton:RegisterCallback(Mouse.eLClick,function() request("BINDING_READ") end)
  Controls.CarrierStepButton:RegisterCallback(Mouse.eLClick,function() request("NETWORK_DETAIL",true) end)
  Controls.CarrierOffButton:RegisterCallback(Mouse.eLClick,function() request("CARRIER_OFF") end)
  for _,a in ipairs({"READ","OFF","AUTO","TEST5"}) do local action=a;Controls["Commerce"..a.."Button"]:RegisterCallback(Mouse.eLClick,function() request("COMMERCE_"..action) end) end
  Controls.InheritRecordButton:RegisterCallback(Mouse.eLClick,function() request("IDENTITY_RECORD") end)
  Controls.InheritRecordButton:RegisterCallback(Mouse.eRClick,function() request("PROGRESSION_IMPORT") end)
  Controls.InheritReadButton:RegisterCallback(Mouse.eLClick,function() request("PROGRESSION_STORE_READ") end)
  Controls.InheritReadButton:RegisterCallback(Mouse.eRClick,function() request('CITY_SEQUENCE_READ',true) end)
  Controls.InheritRecordButtonCaption:SetText('旧记录核对')
  Controls.InheritRecordButton:SetHide(true) -- retired migration UI; Gameplay rejects import too
  Controls.InheritReadButtonCaption:SetText('E2往返')
  Controls.InheritRecordButton:SetToolTipString('历史诊断入口已隐藏；本版本不提供旧档迁移。')
  Controls.InheritReadButton:SetToolTipString('左键：读取选中城市的专业、潜力和投资；新城自动登记，无需迁移。右键：事件证据，只读/翻页。')
  Controls.SourceYieldButton:RegisterCallback(Mouse.eLClick,function() request("PROGRESSION_READ") end)
  Controls.ConstructionPreviewButton:RegisterCallback(Mouse.eLClick,function() request("CONSTRUCTION_PREVIEW") end)
  Controls.ConstructionApplyButton:RegisterCallback(Mouse.eLClick,function() request("CONSTRUCTION_APPLY") end)
  Controls.Lv2GPPButton:RegisterCallback(Mouse.eLClick,function() request("LV2_GPP_READ") end)
  Controls.Lv2HousingButton:RegisterCallback(Mouse.eLClick,function() request("LV2_HOUSING_READ") end)
  Controls.InvestPrepareButton:RegisterCallback(Mouse.eLClick,function() request("INVEST_PREPARE") end)
  Controls.InvestConfirmButton:RegisterCallback(Mouse.eLClick,function() request("INVEST_CONFIRM") end)
  Controls.NetworkButtonCaption:SetText('Network 隔离对照')
  Controls.NetworkButton:RegisterCallback(Mouse.eLClick,function() request('NETWORK_ISOLATION_READ') end)
  Controls.NetworkButton:RegisterCallback(Mouse.eRClick,function() request('NETWORK_ISOLATE') end)
  Controls.NetworkButton:SetToolTipString('左键查看模式/退出结果；右键明确停用本次会话的网络分支。不要保存实验结果；冷启动原存档恢复。')
  Controls.Lv4PercentButton:RegisterCallback(Mouse.eLClick,function() request("LV4_PERCENT_READ") end)
  Controls.ResearchReadButton:RegisterCallback(Mouse.eLClick,function() request("RESEARCH_READ") end)
  Controls.CityFlowButton:RegisterCallback(Mouse.eLClick,function() request("CITY_FLOW_READ") end)
  Controls.EnvelopeReadButton:RegisterCallback(Mouse.eLClick,function() request("ENVELOPE_READ") end)
  Controls.EnvelopeNextButton:RegisterCallback(Mouse.eLClick,function() request("ENVELOPE_NEXT") end)
  Controls.StorageReadButton:RegisterCallback(Mouse.eLClick,function() request("STORAGE_READ") end)
  Controls.StorageWriteButton:RegisterCallback(Mouse.eLClick,function() request("STORAGE_WRITE") end)
  Controls.CompletionButton:RegisterCallback(Mouse.eLClick,function() showCompletion(false) end)
  Controls.CompletionNextButton:RegisterCallback(Mouse.eLClick,function() showCompletion(true) end)
  Controls.CaptureButton:RegisterCallback(Mouse.eLClick,function() request("CAPTURE") end)
  Controls.HalfReadButton:RegisterCallback(Mouse.eLClick,function() request('HALF_READ') end)
  Controls.HalfOnButton:RegisterCallback(Mouse.eLClick,function() request('HALF_ON') end)
  Controls.HalfOffButton:RegisterCallback(Mouse.eLClick,function() request('HALF_OFF') end)
  Controls.BoostTestZeroButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_ZERO') end)
  Controls.BoostTestHalfButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_HALF') end)
  Controls.BoostTestHighButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_HIGH') end)
  Controls.BoostTestAutoButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_TEST_AUTO') end)
  Controls.BoostReadButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_READ') end)
  Controls.BoostBaseButton:RegisterCallback(Mouse.eLClick,function() request('BOOST_BASELINE') end)
  Controls.DialogueTest25Button:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_TEST25') end)
  Controls.DialogueTest50Button:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_TEST50') end)
  Controls.DialogueTest100Button:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_TEST100') end)
  Controls.GWAReadButton:RegisterCallback(Mouse.eLClick,function() request('GWA_READ') end)
  Controls.GWAOffButton:RegisterCallback(Mouse.eLClick,function() request('GWA_OFF') end)
  Controls.GWAAutoButton:RegisterCallback(Mouse.eLClick,function() request('GWA_AUTO') end)
  Controls.GWBaselineButton:RegisterCallback(Mouse.eLClick,function() request('GW_BASELINE') end)
  Controls.MeaningProbeButton:RegisterCallback(Mouse.eLClick,function() request('CULTURE_MEANING_ADVANCE') end)
  Controls.MeaningProbeButton:RegisterCallback(Mouse.eRClick,function() request('CULTURE_MEANING_READ') end)
  Controls.AestheticButton:RegisterCallback(Mouse.eLClick,function() request('CULTURE_AESTHETIC_READ') end)
  Controls.AestheticButton:RegisterCallback(Mouse.eRClick,function() request('CULTURE_AESTHETIC_DETAIL',true) end)
  Controls.GWReadButton:RegisterCallback(Mouse.eLClick,function() request('GREAT_WORK_FACTS_READ') end)
  Controls.GWReadButton:RegisterCallback(Mouse.eRClick,function() request('GREAT_WORK_FACTS_DETAIL',true) end)
  Controls.GWCityButton:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_AUTO') end)
  Controls.GWObjectButton:RegisterCallback(Mouse.eLClick,function() request('GW_OBJECT') end)
  Controls.GWOffButton:RegisterCallback(Mouse.eLClick,function() request('DIALOGUE_OFF') end)
  Controls.DiscountsButton:RegisterCallback(Mouse.eLClick,function() request('DISCOUNT_READ',true) end)
  Controls.NextDiscountsButton:RegisterCallback(Mouse.eLClick,function() request('DISCOUNT_READ',true) end)
  Controls.PurchaseBaseButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_BASE') end)
  Controls.PurchaseOnButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_ON') end)
  Controls.PurchaseOffButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_OFF') end)
  Controls.PurchaseReadButton:RegisterCallback(Mouse.eLClick,function() request('PURCHASE_READ') end)
  Controls.TemplatesButton:RegisterCallback(Mouse.eLClick,function() request("STANDARDIZATION_READ",true) end)
  Controls.NextTemplatesButton:RegisterCallback(Mouse.eLClick,function() request("STANDARDIZATION_READ",true) end)
  Controls.Lv4CopyButton:RegisterCallback(Mouse.eLClick,function() request("LV4_COPY_READ") end)
  Controls.AdjacencyButton:RegisterCallback(Mouse.eLClick,function() request("ADJACENCY") end)
  Controls.BackgroundRoutesButton:RegisterCallback(Mouse.eLClick,function()
    ContextPtr:ClearUpdate();pendingToken=nil
    if not P.IsTestPlayer(Game.GetLocalPlayer()) then return end
    local data=ExposedMembers.SPC_P0_BackgroundRoutes
    localReport=P.VERSION.." | 后台路线（只看已有缓存）\n"
      ..((data and data.version==P.VERSION and data.text) or "没有后台记录。请截图；此按钮不会启动读取。")
    status(localReport:gsub("\n","[NEWLINE]"))
  end)
  Controls.RouteStateButton:RegisterCallback(Mouse.eLClick,function()
    ContextPtr:ClearUpdate();pendingToken=nil
    local pid=Game.GetLocalPlayer()
    if not P.IsTestPlayer(pid) then return end
    local data=ExposedMembers.SPC_P0 or {}
    local snapshot=data.AutoRouteProbe and data.AutoRouteProbe[pid]
    localReport=P.VERSION.." | GAMEPLAY 自动探针（只查看缓存）\n"
      ..((data.Version==P.VERSION and snapshot and snapshot.text)
        or (data.Version==P.VERSION and data.AutoRouteProbeError and ("自动采样失败："..P.Scalar(data.AutoRouteProbeError)))
        or "尚无自动记录；截图即可。此按钮不会触发采样。")
    status(localReport:gsub("\n","[NEWLINE]"))
  end)
  Controls.RouteEventsButton:RegisterCallback(Mouse.eLClick,function() request("TRADE_EVENTS") end)
  Controls.TradeButton:RegisterCallback(Mouse.eLClick,function() request("TRADE") end)
  Controls.NextButton:RegisterCallback(Mouse.eLClick,function()
    if pageAction=="ADJACENCY" or pageAction=="TRADE" then request(pageAction,true) end
  end)
  Controls.GovernorButton:RegisterCallback(Mouse.eLClick,function() request("GOVERNOR") end)
  Controls.SpecialistsButton:RegisterCallback(Mouse.eLClick,function() request("SPECIALISTS") end)
  Controls.MarkButton:RegisterCallback(Mouse.eLClick,function() request("MARK_CITY") end)
  Controls.CopyButton:RegisterCallback(Mouse.eLClick,function() copy(false) end)
  Controls.BaselineButton:RegisterCallback(Mouse.eLClick,function() copy(true) end)
  Controls.UnitReadButton:RegisterCallback(Mouse.eLClick,function() request('UNIT_SITE_READ') end)
  Controls.UnitReadButton:RegisterCallback(Mouse.eRClick,function() request('CITY_SEQUENCE_BEGIN') end)
  Controls.UnitReadButton:SetToolTipString('左键：移民/施工队读取。右键：在选中己方移民或城市位置开始本次事件观察（替换上次观察）；不建专业记录。之后右键E2往返读取。')
  status('P0-D1：跨学科研究已自动运行。[NEWLINE]选中科研城市，左键看摘要、右键看区域组成。诊断只读。')
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
 Controls.GWAReadButton:SetHide(false)
 Controls.GWAReadButtonCaption:SetText("内存观测")
 Controls.GWAReadButton:RegisterCallback(Mouse.eLClick,function()request('MEMORY_BEGIN')end)
 Controls.GWAReadButton:RegisterCallback(Mouse.eRClick,function()request('MEMORY_READ')end)
 Controls.GWAReadButton:SetToolTipString('左键开始一次短观测；右键读取事件用量。最多6回合，不清内存、不改存档。')
 include("ProjectTurnRead")
 -- Retain its independent UI queue reader; B120 observer still exists for reference.
 SPCProjectTurnRead.New(P,function()end,function(...)return UI.RequestPlayerOperation(...)end)
 include("TimedProjectRead")
 local timer=SPCTimedProjectRead.New(P,function(s) localReport=s;status(s) end,function(...)return UI.RequestPlayerOperation(...)end)
 projectReadPulse=timer.Pulse
 Events.GameCoreEventPublishComplete.Add(projectReadPulse)
 Controls.TurnProbeReadCaption:SetText("自动项目报告")
 Controls.PerformanceSnapshotButton:SetHide(false)
 Controls.TurnProbeArmCaption:SetText('GC试运行')
 Controls.PerformanceSnapshotButton:RegisterCallback(Mouse.eLClick,function()request('MEMORY_GC_READ')end)
 Controls.PerformanceSnapshotButton:RegisterCallback(Mouse.eRClick,function()
  local g=ExposedMembers.SPC_P0;local d=g and g.MemoryObservation;local a=d and d.AutoGC
  request(a and a.enabled==false and 'MEMORY_GC_AUTO_ON' or 'MEMORY_GC_AUTO_OFF')
 end)
 Controls.PerformanceSnapshotButton:SetToolTipString('受控自动GC试运行。左键只读结果；右键开启/关闭本次加载的自动调用，不会立即回收。不修改专业数据；失败后保持停用。')
 local function projectAction(fn)
  ContextPtr:ClearUpdate();gwaFlight=nil;pendingToken=nil;pendingAction=nil;fn()
 end
 Controls.PerformanceReadButton:RegisterCallback(Mouse.eLClick,function()projectAction(timer.Read)end)
 Controls.PerformanceReadButton:RegisterCallback(Mouse.eRClick,function()projectAction(timer.Cancel)end)
 Controls.PerformanceReadButton:SetToolTipString('左键只读计时报告；右键取消计时，不清空生产。已调用完成后不重试。')

end
ContextPtr:SetInitHandler(initialize)
Events.LoadScreenClose.Add(showRoot)
Events.SystemUpdateUI.Add(gwaPulse)
Events.SystemUpdateUI.Add(placeEntry)
ContextPtr:SetShutdown(function() if projectReadPulse then Events.GameCoreEventPublishComplete.Remove(projectReadPulse) end;Events.GameCoreEventPublishComplete.Remove(overflowPulse);Controls.OpenButton:SetHide(true);Events.SystemUpdateUI.Remove(placeEntry);gwaFlight=nil;Events.SystemUpdateUI.Remove(gwaPulse);ContextPtr:ClearUpdate();Events.LoadScreenClose.Remove(showRoot) end)
