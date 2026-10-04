-- Native UI-only observations. Baselines never affect research, civics or works.
include('NetworkInput')
SPCBoostGreatWorkRead={}
local baseline
local function snapshot(P)
 local player=Players[Game.GetLocalPlayer()];local result={}
 for _,def in ipairs({{'TECH','Technologies','GetTechs','GetResearchCost','GetResearchProgress'},{'CIVIC','Civics','GetCulture','GetCultureCost','GetCulturalProgress'}}) do
  local obj=player[def[3]](player)
  for r in GameInfo[def[2]]() do
   local id=r.Index;local key=def[1]..':'..id
   result[key]={name=Locale.Lookup(r.Name),cost=obj[def[4]](obj,id),progress=obj[def[5]](obj,id),boosted=obj:HasBoostBeenTriggered(id)}
  end
 end
 return result
end
function SPCBoostGreatWorkRead.Boost(P,mark)
 local ok,out=pcall(function()
  local now=snapshot(P);local turn=Game.GetCurrentGameTurn()
  if mark then baseline={pid=Game.GetLocalPlayer(),turn=turn,rows=now};return '已记录科技/市政原生进度基线。请同回合触发一次，然后 Read boosts。' end
  if not baseline or baseline.pid~=Game.GetLocalPlayer() then return '尚无本次会话基线；先点 Boost baseline。' end
  local rows={}
  for key,v in pairs(now) do local old=baseline.rows[key]
   if old and not old.boosted and v.boosted then
    local delta=v.progress-old.progress
    rows[#rows+1]=v.name..string.format(' | cost=%.4f | %.4f→%.4f | Δ=%.4f (%.6f%%)',v.cost,old.progress,v.progress,delta,v.cost>0 and delta/v.cost*100 or 0)
   end
  end
  table.sort(rows)
  if #rows==0 then rows[1]='未发现新触发的Boost。' end
  if #rows>3 then for i=#rows,4,-1 do rows[i]=nil end;rows[#rows+1]='本次多于3项；为便于比较，每次只触发一项。' end
  if turn~=baseline.turn then rows[#rows+1]='已跨回合：Δ含正常研究，不能据此判断Boost精度。' end
  rows[#rows+1]='百分比是总进度变化/成本，含原有Boost；临近完成会受剩余需求限制。'
  return table.concat(rows,'\n')
 end)
 return ok and out or ('原生Boost读取失败：'..tostring(out))
end
local workBaseline
function SPCBoostGreatWorkRead.Works(P,c,mark)
 local ok,out=pcall(function()
  local b=c:GetBuildings();local count,eligible,culture,tourism=0,0,0,0;local seen={};local names={};local themed=0;local themeUnknown=0;local signature={};local themedCulture,themedTourism=0,0
  local types={WRITING=true,SCULPTURE=true,PORTRAIT=true,LANDSCAPE=true,RELIGIOUS=true,ARTIFACT=true,MUSIC=true}
  for r in GameInfo.Buildings() do if P.HasBuilding(b,r.Index) then
   local n=b:GetNumGreatWorkSlots(r.Index)
   if n and n>0 then
    local tok,tval=pcall(function() return b:IsBuildingThemedCorrectly(r.Index) end)
    if tok and type(tval)=="boolean" then if tval then themed=themed+1 end else themeUnknown=themeUnknown+1 end
    local bc=b:GetBuildingYieldFromGreatWorks(P.Info('Yields','YIELD_CULTURE').Index,r.Index)
    local bt=b:GetBuildingTourismFromGreatWorks(false,r.Index)+b:GetBuildingTourismFromGreatWorks(true,r.Index)
    culture=culture+bc;tourism=tourism+bt
    if tok and tval==true then themedCulture=themedCulture+bc;themedTourism=themedTourism+bt end
    signature[#signature+1]='B'..r.Index..':'..tostring(tval)
    for slot=0,n-1 do local id=b:GetGreatWorkInSlot(r.Index,slot)
     if id and id~=-1 and not seen[id] then
      seen[id]=true;count=count+1;signature[#signature+1]='W'..id..'@'..r.Index
      local w=assert(P.Info('GreatWorks',b:GetGreatWorkTypeFromIndex(id)),'WORK_TYPE_UNKNOWN')
      if types[w.GreatWorkObjectType:gsub('GREATWORKOBJECT_','')] then eligible=eligible+1 end
      names[#names+1]=Locale.Lookup(w.Name)..' ['..w.GreatWorkObjectType..'/'..tostring(w.EraType)..']'
     end
    end
   end
  end end
  local total=c:GetYield(P.Info('Yields','YIELD_CULTURE').Index)
  table.sort(names);table.sort(signature)
  local sig=table.concat(signature,';');local turn=(mark or workBaseline) and Game.GetCurrentGameTurn() or nil;local pid=(mark or workBaseline) and Game.GetLocalPlayer() or nil
  if mark then workBaseline={pid=pid,city=c:GetID(),turn=turn,culture=culture,tourism=tourism,total=total,signature=sig,tc=themedCulture,tt=themedTourism} end
  local rows={string.format('作品=%d / 本实验合格=%d | 作品文化=%.4f | 作品旅游业=%.4f',count,eligible,culture,tourism),string.format('整城文化=%.4f（含宜居度等倍率）',total)}
  if workBaseline and workBaseline.pid==pid and workBaseline.city==c:GetID() then
   local a=workBaseline
   rows[#rows+1]=string.format('对照T%d → T%d：作品ΔC=%+.4f / ΔT=%+.4f；整城ΔC=%+.4f',a.turn,turn,culture-a.culture,tourism-a.tourism,total-a.total)
   rows[#rows+1]=(sig==a.signature and '收藏/所在建筑/主题状态一致；' or '注意：收藏或建筑/主题状态已变化；')..'跨回合差值可能含人口/专家等其它变化。'
  end
  local bg=ExposedMembers and ExposedMembers.SPC_DialogueBackground
  if bg then rows[#rows+1]='事件后台：扫描='..bg.scans..' / 发送='..bg.sends..' / '..bg.state..' / '..bg.reason;rows[#rows+1]='传输：重发='..tostring(bg.retries or 0)..' / API返回='..tostring(bg.transport or 'NONE') end
  rows[#rows+1]=string.format('主题化建筑=%d / 未知=%d；其中作品C=%.4f / T=%.4f',themed,themeUnknown,themedCulture,themedTourism)
  for i=1,math.min(2,#names) do rows[#rows+1]=names[i] end
  if #names>2 then rows[#rows+1]='另有'..(#names-2)..'件，完整名称请看巨作界面。' end
  return table.concat(rows,'\n')
 end)
 return ok and out or ('巨作读取失败：'..tostring(out))
end

function SPCBoostGreatWorkRead.Adjacency(P,c)
 local ok,result=pcall(function()
  local totals={};local b=c:GetBuildings();local ys={'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'}
  for _,y in ipairs(ys) do totals[y]=0 end
  for r in GameInfo.Buildings() do if P.HasBuilding(b,r.Index) and b:GetNumGreatWorkSlots(r.Index)>0 then
   for _,y in ipairs(ys) do totals[y]=totals[y]+b:GetBuildingYieldFromGreatWorks(P.Info('Yields','YIELD_'..y).Index,r.Index) end
  end end
  local rows={'原生作品收益 / 整城产出率（含其它来源与倍率）：'}
  for _,y in ipairs(ys) do rows[#rows+1]=string.format('%s %.4f / %.4f',y,totals[y],c:GetYield(P.Info('Yields','YIELD_'..y).Index)) end
  return table.concat(rows,'\n')
 end)
 return ok and result or ('原生六收益读取未完成：'..tostring(result))
end

-- One on-demand comparison for the current single-city fixture. Never persisted,
-- never a Gameplay source, and no native handles survive a read.
local function productionAbsolute(P,c)
 local b=c:GetBuildings();local y=assert(GameInfo.Yields.YIELD_PRODUCTION,'PRODUCTION_DEFINITION_MISSING');local total=0
 for r in GameInfo.Buildings()do
  local has=P.HasBuilding(b,r.Index);assert(type(has)=='boolean','BUILDING_UNKNOWN')
  if has then
   local slots=b:GetNumGreatWorkSlots(r.Index)
   assert(type(slots)=='number' and slots>=0 and slots%1==0 and slots<=16,'SLOTS_UNKNOWN')
   if slots>0 then
    local actual=b:GetBuildingYieldFromGreatWorks(y.Index,r.Index)
    assert(type(actual)=='number' and actual==actual and math.abs(actual)<math.huge,'WORK_YIELD_UNKNOWN');total=total+actual
   end
  end
 end
 assert(total==total and math.abs(total)<math.huge,'WORK_YIELD_UNKNOWN');return total
end
local meaningReadings,productionReading
function SPCBoostGreatWorkRead.ClearMeaningRead() meaningReadings=nil;productionReading=nil end
function SPCBoostGreatWorkRead.Meaning(P,c,v,mark)
 local ok,result=pcall(function()
  assert(v.owner==Game.GetLocalPlayer() and v.cityID==c:GetID() and v.reference==SPCNetworkInput.Reference(c),'ME_UI_REFERENCE_CHANGED')
  if v.mode=='OFF' then
   meaningReadings=nil
   if v.productionOnly then
    local turn=Game.GetCurrentGameTurn();local actual=productionAbsolute(P,c)
    assert(v.reference==SPCNetworkInput.Reference(c) and turn==Game.GetCurrentGameTurn(),'ME_UI_REFERENCE_CHANGED')
    return string.format('实验OFF｜首次清理 %s｜当前原生作品生产力 %.2f；撤销见下方精确实例，不作追加差值PASS。',tostring(v.cleanupStatus or 'UNKNOWN'),actual)
   end
   return '实验已关闭；实际撤销与旧系统恢复见本次实例读取。'
  end
  assert(v.mode=='BASELINE' or v.mode=='ACTIVE','ME_UI_MODE_UNKNOWN')
  assert(not v.error and not v.configurationError and not v.dialogueError and v.oldHeld and v.planStatus=='READY','ME_UI_CONFIGURATION_PENDING')
  assert(v.dialoguePercent==0,'ME_UI_CONFIGURATION_PENDING')
  if v.cultureDeferred or not v.finalValues then assert(v.configuredCulture==0,'ME_UI_CONFIGURATION_PENDING')end
  local function finite(n)return type(n)=='number' and n==n and math.abs(n)<math.huge end
  local function integer(n)return finite(n) and n>=0 and n%1==0 end
  assert(integer(v.count),'ME_UI_WORK_COUNT_UNKNOWN')
  local definitions={
   {'SCIENCE','科研','science','totalScience','configuredScience'},
   {'PRODUCTION','生产力','production','totalProduction','configuredProduction'},
   {'GOLD','金币','gold','totalGold','configuredGold'},
   {'FOOD','食物','food','totalFood','configuredFood'},
   {'FAITH','信仰','faith','totalFaith','configuredFaith'},
   {'CULTURE','文化','culture','totalCulture','configuredCulture'}
  }
  if v.productionOnly then definitions={definitions[2]}elseif v.cultureDeferred or not v.finalValues then table.remove(definitions,6)end
  local on=v.mode=='ACTIVE';local totals={};local expected={}
  for _,entry in ipairs(definitions)do
   local yield,each,total,configured=entry[1],v[entry[3]],v[entry[4]],v[entry[5]]
   assert(integer(each) and integer(total) and total==each*v.count and finite(configured) and configured==(on and each or 0),'ME_UI_CONFIGURATION_PENDING')
   totals[yield]=0;expected[yield]=on and total or 0
  end
  local b=c:GetBuildings();local signature={};local seen={};local workCount=0;local buildings,themedBuildings=0,0
  local categories={WRITING=true,MUSIC=true,SCULPTURE=true,PORTRAIT=true,LANDSCAPE=true,RELIGIOUS=true,ARTIFACT=true}
  for r in GameInfo.Buildings()do if P.HasBuilding(b,r.Index) then
   local n=b:GetNumGreatWorkSlots(r.Index);assert(integer(n),'ME_UI_SLOTS_UNKNOWN')
   if n>0 then
    local known,themed=pcall(b.IsBuildingThemedCorrectly,b,r.Index)
    assert(known and type(themed)=='boolean','ME_UI_THEME_UNKNOWN')
    signature[#signature+1]='B'..r.Index..':'..tostring(themed)
    local count=0
    for slot=0,n-1 do local id=b:GetGreatWorkInSlot(r.Index,slot)
     if id~=nil and id~=-1 then
      assert(integer(id) and not seen[id],'ME_UI_DUPLICATE_WORK');seen[id]=true
      local typ=b:GetGreatWorkTypeFromIndex(id);local row=GameInfo.GreatWorks[typ]
      assert(row and type(row.GreatWorkType)=='string' and type(row.GreatWorkObjectType)=='string','ME_UI_WORK_DEFINITION_UNKNOWN')
      signature[#signature+1]='W'..id..'@'..r.Index..':'..slot..':'..row.GreatWorkType
      local category=row.GreatWorkObjectType:gsub('GREATWORKOBJECT_','')
      if categories[category] then count=count+1;workCount=workCount+1 end
     end
    end
    for _,entry in ipairs(definitions)do
     local y=entry[1];local def=assert(P.Info('Yields','YIELD_'..y),'ME_UI_YIELD_DEFINITION_UNKNOWN')
     local value=b:GetBuildingYieldFromGreatWorks(def.Index,r.Index)
     assert(finite(value),'ME_UI_NATIVE_YIELD_UNKNOWN');totals[y]=totals[y]+value
    end
    if count>0 then buildings=buildings+1;if themed then themedBuildings=themedBuildings+1 end end
   end
  end end
  assert(workCount==v.count,'ME_UI_WORK_COUNT_MISMATCH')
  for _,entry in ipairs(definitions)do assert(finite(totals[entry[1]]),'ME_UI_NATIVE_YIELD_UNKNOWN')end
  local turn=Game.GetCurrentGameTurn();assert(integer(turn),'ME_UI_TURN_UNKNOWN')
  local populationOK,population=pcall(c.GetPopulation,c)
  local populationKnown=populationOK and integer(population)
  local qualificationKnown=v.currentIdentity=='CULTURE' and integer(v.currentPotential) and v.currentPotential>=4
    and v.currentActiveStatus=='KNOWN' and integer(v.currentActive) and v.currentActive>=4
  local depthKnown=type(v.stamp)=='string' and #v.stamp>0
  local qualification=table.concat({tostring(v.currentIdentity),tostring(v.currentPotential),tostring(v.currentActive),tostring(v.currentActiveStatus)},':')
  table.sort(signature)
  local key=v.reference..'|'..tostring(v.productionOnly==true)..'|'..tostring(v.cultureDeferred==true)..'|'..tostring(v.stamp)..'|'..v.count..'|'..turn..'|'..qualification..'|'..tostring(population)..'|'..table.concat(signature,';')
  assert(v.reference==SPCNetworkInput.Reference(c) and turn==Game.GetCurrentGameTurn(),'ME_UI_REFERENCE_CHANGED')
  local stable=populationKnown and qualificationKnown and depthKnown
  if mark and v.mode=='BASELINE' and stable then meaningReadings={key=key,baseline=totals,current=totals}end
  local valid=stable and meaningReadings and meaningReadings.key==key
  if valid then meaningReadings.current=totals else meaningReadings=nil end
  local lines={string.format('%s｜合格W=%d／%d座馆藏建筑｜%s',v.productionOnly and '生产力单值对照' or '意义延展原生读数',workCount,buildings,on and '追加中' or '基线')}
  if v.productionOnly then lines[#lines+1]='本次仅开启生产力；其它产出未验证。'end
  for _,entry in ipairs(definitions)do
   local y=entry[1];local delta=valid and on and (totals[y]-meaningReadings.baseline[y]) or nil
   lines[#lines+1]=string.format('%s｜每件 +%g／本城 +%g｜实测差值 %s｜当前原生 %.2f',entry[2],on and v[entry[3]] or 0,expected[y],delta~=nil and string.format('%+.2f',delta) or (on and '未确认' or '待启用追加'),totals[y])
    if delta~=nil and math.abs(delta-expected[y])>0.001 then lines[#lines+1]=entry[2]..'异常：实测追加与预期不符；保存本次报告，停止该项验收。'end
  end
  if not valid then
   local reason=not stable and '人口／资格／领域D未确认' or '回合／人口／馆藏位置／主题／领域D／资格已变，或尚无同回合基线'
   lines[#lines+1]='差值未确认：'..reason..'；可信原生绝对值仍显示。结束后重新准备基线。'
  else
   lines[#lines+1]=on and '右键只刷新当前读数；左键或结束按钮撤回追加。' or '同回合基线已记录；左键启用追加。'
  end
  if themedBuildings>0 then lines[#lines+1]='已主题化'..themedBuildings..'座；当前预期追加保持固定，不乘主题倍率。'end
  if v.cultureDeferred then lines[#lines+1]='文化追加暂隔离；HD原有效果保持。'
  elseif v.finalValues then lines[#lines+1]='文化：检验与古罗马剧场＋2共存；有配置不等于已生效。'end
  return table.concat(lines,'\n')
 end)
 if not ok then meaningReadings=nil end -- An unknown/error cannot retain a successful comparison.
 return ok and result or ((v.productionOnly and '生产力' or v.finalValues and not v.cultureDeferred and '六产出' or '五产出')..'原生读数未确认：'..(tostring(result):match('ME_[A-Z_]+') or '原生接口未知')..'；不记录成功基线。')
end

-- Fixed technical comparison only; this does not calculate Design D or Floor.
local function diagnosticFinite(n)return type(n)=='number' and n==n and math.abs(n)<math.huge end
local function diagnosticInteger(n)return diagnosticFinite(n) and n>=0 and n%1==0 end
local function diagnosticSnapshot(P,c,v)
 local selected=UI.GetHeadSelectedCity();local ref=SPCNetworkInput.Reference(c)
 assert(selected and c:GetOwner()==Game.GetLocalPlayer() and selected:GetOwner()==c:GetOwner()
  and SPCNetworkInput.Reference(selected)==ref and v.owner==c:GetOwner() and v.cityID==c:GetID() and v.reference==ref,'ME_UI_DIAG_REFERENCE')
 local turn=Game.GetCurrentGameTurn();assert(diagnosticInteger(turn),'ME_UI_DIAG_REFERENCE')
 local b=c:GetBuildings();local work,seen,workCount=nil,{},0
 for r in GameInfo.Buildings()do
  local has=P.HasBuilding(b,r.Index);assert(type(has)=='boolean','ME_UI_DIAG_WORK_UNKNOWN')
  if has then
   local n=b:GetNumGreatWorkSlots(r.Index);assert(diagnosticInteger(n) and n<=16,'ME_UI_DIAG_SLOTS_UNKNOWN')
   if n>0 then for slot=0,n-1 do
    local id=b:GetGreatWorkInSlot(r.Index,slot)
    if id~=nil and id~=-1 then
     assert(diagnosticInteger(id) and not seen[id],'ME_UI_DIAG_WORK_UNKNOWN');seen[id]=true;workCount=workCount+1
     assert(workCount<=1,'ME_UI_DIAG_WORK_COUNT')
     local def=GameInfo.GreatWorks[b:GetGreatWorkTypeFromIndex(id)]
     assert(def and type(def.GreatWorkType)=='string' and def.GreatWorkObjectType=='GREATWORKOBJECT_WRITING','ME_UI_DIAG_WORK_UNKNOWN')
     local ok,themed=pcall(b.IsBuildingThemedCorrectly,b,r.Index)
     assert(ok and type(themed)=='boolean','ME_UI_DIAG_THEME_UNKNOWN')
     local damaged=b:IsPillaged(r.Index);assert(type(damaged)=='boolean','ME_UI_DIAG_WORK_UNKNOWN')
     work={id=id,type=def.GreatWorkType,building=r.BuildingType,index=r.Index,slot=slot,themed=themed,pillaged=damaged}
    end
   end end
  end
 end
 assert(workCount==1 and work,'ME_UI_DIAG_WORK_COUNT')
 local expected=v.diagnosticWork
 local fixtureMatches=v.diagnosticStage=='OFF' or type(expected)=='table' and expected.id==work.id and expected.type==work.type
  and expected.slot==work.slot and (expected.building==work.building or expected.building==work.index)
 local y=assert(P.Info('Yields','YIELD_PRODUCTION'),'ME_UI_DIAG_NATIVE_UNKNOWN')
 local value=b:GetBuildingYieldFromGreatWorks(y.Index,work.index)
 assert(diagnosticFinite(value),'ME_UI_DIAG_NATIVE_UNKNOWN')
 selected=UI.GetHeadSelectedCity()
 assert(selected and SPCNetworkInput.Reference(selected)==ref and ref==SPCNetworkInput.Reference(c)
  and turn==Game.GetCurrentGameTurn(),'ME_UI_DIAG_REFERENCE')
 local qKnown=v.currentIdentity=='CULTURE' and diagnosticInteger(v.currentPotential) and v.currentPotential>=4
  and v.currentActiveStatus=='KNOWN' and diagnosticInteger(v.currentActive) and v.currentActive>=4
 local q=table.concat({tostring(v.currentIdentity),tostring(v.currentPotential),tostring(v.currentActive),tostring(v.currentActiveStatus)},':')
 local key=table.concat({ref,turn,work.id,work.type,work.building,work.slot,tostring(work.themed),tostring(work.pillaged),q},'|')
 return {key=key,value=value,work=work,qualified=qKnown,fixtureMatches=fixtureMatches}
end
local function diagnosticConfiguration(v)
 local M=SPCCultureMeaningModel
 local expected=type(M.DiagnosticExpected)=='table' and M.DiagnosticExpected[v.diagnosticStage]
 assert(v.diagnostic==true and diagnosticInteger(expected),'ME_UI_DIAG_CONFIGURATION')
 assert(v.diagnosticExpected==expected and diagnosticInteger(v.remainingOwned)
  and type(v.diagnosticCarriers)=='table' and #v.diagnosticCarriers<=#M.Owned,'ME_UI_DIAG_CONFIGURATION')
 local count,amount,names=0,0,{};local owned={}
 for _,name in ipairs(M.Owned)do owned[name]=true end
 for k,entry in pairs(v.diagnosticCarriers)do
  assert(diagnosticInteger(k) and k>=1 and k<=#v.diagnosticCarriers and type(entry)=='table'
   and type(entry.name)=='string' and owned[entry.name] and not names[entry.name]
   and type(entry.yield)=='string' and diagnosticFinite(entry.amount) and entry.amount>=0 and type(entry.pillaged)=='boolean','ME_UI_DIAG_CONFIGURATION')
  if M.DiagnosticSingle3 and entry.name==M.DiagnosticSingle3.name then
   assert((entry.yield=='PRODUCTION' or entry.yield=='YIELD_PRODUCTION') and entry.amount==M.DiagnosticSingle3.amount,'ME_UI_DIAG_CONFIGURATION')
  end
  for _,part in pairs(M.ProductionValues or {})do if entry.name==part.name then
   assert((entry.yield=='PRODUCTION' or entry.yield=='YIELD_PRODUCTION') and entry.amount==part.amount,'ME_UI_DIAG_CONFIGURATION')
  end end
  names[entry.name]=true;count=count+1
  if (entry.yield=='PRODUCTION' or entry.yield=='YIELD_PRODUCTION') and not entry.pillaged then amount=amount+entry.amount end
 end
 assert(count==#v.diagnosticCarriers and count==v.remainingOwned
  and (v.configuredProduction==nil or diagnosticInteger(v.configuredProduction) and amount==v.configuredProduction),'ME_UI_DIAG_CONFIGURATION')
 return expected,amount
end
function SPCBoostGreatWorkRead.ProductionDiagnostic(P,c,v,mark,token,requestedReference,inspect)
 local lines={};local configuration,expected,amount=pcall(diagnosticConfiguration,v)
 if configuration then
  lines[#lines+1]=string.format('生产力诊断｜%s｜预期 +%g｜载体配置 +%g｜精确载体 %d',v.diagnosticStage,expected,amount,v.remainingOwned)
 else
  lines[#lines+1]='生产力诊断｜配置未确认：ME_UI_DIAG_CONFIGURATION'
 end
 local good,now=pcall(diagnosticSnapshot,P,c,v)
 if good then
  local canMark=configuration and v.diagnosticStage=='BASELINE' and mark and amount==0 and v.remainingOwned==0
   and v.configuredProduction==0 and not v.error and not v.configurationError and not v.dialogueError and v.oldHeld==true and v.dialoguePercent==0
   and v.planStatus=='READY' and v.count==1 and now.qualified and now.fixtureMatches and not now.work.pillaged
  if canMark then productionReading={key=now.key,value=now.value}end
  local valid=now.qualified and now.fixtureMatches and not now.work.pillaged and productionReading and productionReading.key==now.key
  if not valid then productionReading=nil end
  local delta=valid and now.value-productionReading.value or nil
  if not now.fixtureMatches then lines[#lines+1]='当前作品与已确认fixture不同；保留真实绝对读数，不沿用旧差值。'end
  lines[#lines+1]=string.format('当前原生作品生产力 %.2f｜实测差值 %s',now.value,delta~=nil and string.format('%+.2f',delta) or '未确认')
  lines[#lines+1]=string.format('Writing %s｜ID %d｜宿主 %s｜槽位 %d｜主题 %s',now.work.type,now.work.id,now.work.building,now.work.slot,tostring(now.work.themed))
  if v.diagnosticStage=='OFF' then
   lines[#lines+1]='退出读数仅作对照：旧系统恢复后，不能把此差值直接归因为Meaning残留。'
  elseif delta~=nil and configuration and v.configuredProduction~=nil and not v.error and not v.configurationError and not v.dialogueError then
   lines[#lines+1]=math.abs(delta-expected)<0.000001 and '一致（仅即时读数）' or '不一致：实测差值未达到本阶段预期。'
  elseif not valid then lines[#lines+1]='差值未确认：尚无可靠同回合基线，或引用／作品／位置／主题／当前资格已变化。'end
  if canMark then lines[#lines+1]='同回合基线已记录。'end
 else
  productionReading=nil
  lines[#lines+1]='原生作品生产力未确认：'..(tostring(now):match('ME_UI_DIAG_[A-Z_]+') or 'ME_UI_DIAG_NATIVE_UNKNOWN')..'；不以0代替未知。'
 end
 if configuration then
  for i=1,math.min(4,#v.diagnosticCarriers)do local e=v.diagnosticCarriers[i]
   lines[#lines+1]=e.name..'｜'..e.yield..' +'..e.amount..'｜掠夺='..tostring(e.pillaged)
  end
  if #v.diagnosticCarriers>4 then lines[#lines+1]='另'..(#v.diagnosticCarriers-4)..'项载体未展开。'end
 end
 if v.diagnosticStage=='CLEAR1' then lines[#lines+1]='CLEAR1仅撤＋1；旧系统应继续hold，尚未结束。'
 elseif v.diagnosticStage=='REMAIN2' then lines[#lines+1]='仅撤＋1、保留健康＋2；用实例ID核对是否重建。'
 elseif v.diagnosticStage=='SINGLE3' then lines[#lines+1]='独立单片＋3；与两片＋1／＋2总量相同。'
 elseif v.diagnosticStage=='OFF' then lines[#lines+1]='OFF是控制状态；退出差值含旧系统恢复，载体为0仍需核对原生实例和真实收益。'end
 if v.configuredProduction==nil or v.error or v.configurationError or v.dialogueError then lines[#lines+1]='当前错误／配置待确认；即时读数不构成验证通过。'end
 if inspect then lines[#lines+1]=SPCBoostGreatWorkRead.Modifiers(P,c,v,token,requestedReference)end
 return table.concat(lines,'\n')
end

-- B156: explicit UI read only. Never retain native handles/tables between reads.
include('CultureMeaningModel')
do
 local lastToken,cached,stamp,cachedSummary
 local LIMIT,HITS,SUBJECTS=32768,64,64
 local function text(v)
  if v==nil then return 'nil' end
  if type(v)~='string' and type(v)~='number' and type(v)~='boolean' then return '<'..type(v)..'>' end
  -- Explicit ASCII controls: locale-dependent %c can corrupt UTF-8 city names.
  local s=tostring(v):gsub('[%z\1-\31\127]',' '):gsub('%[','('):gsub('%]',')')
  if #s>240 then local n=240;while n>0 and s:byte(n+1)>=128 and s:byte(n+1)<=191 do n=n-1 end;s=s:sub(1,n)..'…' end
  return s
 end
 local function integer(n)return type(n)=='number' and n==n and n>=0 and n%1==0 and n<math.huge end
 local function array(t,limit)
  if type(t)~='table' then return nil,'ARRAY_'..type(t) end
  local n,seen=0,{}
  for k,v in pairs(t)do
   n=n+1;if n>limit then return nil,'LIMIT' end
   if not integer(k) or k<1 or k>limit then return nil,'ARRAY_KEY' end
   if not integer(v) and type(v)~='string' then return nil,'ID_TYPE' end
   local key=type(v)..':'..tostring(v);if seen[key] then return nil,'DUPLICATE_ID' end;seen[key]=true
  end
  for i=1,n do if t[i]==nil then return nil,'SPARSE_ARRAY' end end
  return n
 end
 local function call(name,...)
  local f=GameEffects and GameEffects[name]
  if type(f)~='function' then return false,'API_MISSING:'..name end
  return pcall(f,...)
 end
 -- Complete observed District format only, including B160's signed SubValue.
 -- GameEffects object IDs are NOT city/district IDs. SubType/SubValue are opaque.
 local function mapDistrict(kind,raw,player,c)
  if kind~='LOC_MODIFIER_OBJECT_DISTRICT' or type(raw)~='string' or #raw>512 then return 'UNKNOWN:FORMAT' end
  local did,pid,sub,val,cid=raw:match('^District: (%d+), Owner: (%d+), SubType: (%d+), SubValue: (%-?%d+), City: (%d+)$')
  if not did then return 'UNKNOWN:FORMAT' end
  did,pid,cid=tonumber(did),tonumber(pid),tonumber(cid)
  for _,n in ipairs({did,pid,cid})do if not integer(n) or n>9007199254740991 then return 'UNKNOWN:ID' end end
  if player~=pid then return 'UNKNOWN:OWNER_CONFLICT' end
  local ok,result,districtType=pcall(function()
   local city=assert(CityManager.GetCity(pid,cid),'CITY_UNAVAILABLE')
   assert(city:GetOwner()==pid and city:GetID()==cid,'CITY_CONFLICT')
   local district=assert(city:GetDistricts():FindID(did),'DISTRICT_UNAVAILABLE')
   assert(district:GetID()==did,'DISTRICT_CONFLICT')
   local parent=assert(district:GetCity(),'DISTRICT_CITY_UNAVAILABLE')
   local ref=SPCNetworkInput.Reference(city)
   assert(SPCNetworkInput.Reference(parent)==ref,'DISTRICT_CITY_CONFLICT')
   if pid==c:GetOwner() and cid==c:GetID() then
    assert(ref==SPCNetworkInput.Reference(c),'REFERENCE_CONFLICT')
    local row=district.GetType and GameInfo.Districts and GameInfo.Districts[district:GetType()]
    return '本城已核验',row and row.DistrictType or 'UNKNOWN'
   end
   local row=district.GetType and GameInfo.Districts and GameInfo.Districts[district:GetType()]
   return '其它城已核验: '..pid..'/'..cid,row and row.DistrictType or 'UNKNOWN'
  end)
  return ok and result or 'UNKNOWN:OBJECT_CHECK',ok and districtType or 'UNKNOWN'
 end
 local function signature(c,v)
  local selected=UI.GetHeadSelectedCity()
  assert(selected and selected:GetOwner()==Game.GetLocalPlayer() and c:GetOwner()==Game.GetLocalPlayer(),'STALE_CITY')
  local ref=SPCNetworkInput.Reference(c)
  assert(SPCNetworkInput.Reference(selected)==ref and v.owner==c:GetOwner() and v.cityID==c:GetID() and v.reference==ref,'STALE_REFERENCE')
  local parts={ref,tostring(Game.GetCurrentGameTurn())}
  for _,k in ipairs({'mode','variant','stamp','configuredScience','configuredGold','configuredCulture','configuredProduction','configuredFood','configuredFaith','dialoguePercent','count','error','configurationError','diagnostic','diagnosticStage','diagnosticExpected','remainingOwned','productionOnly','finalValues','cultureDeferred','cleanupStatus','cleanupError'})do parts[#parts+1]=text(v[k])end
  return table.concat(parts,'|')
 end
 function SPCBoostGreatWorkRead.ClearModifierRead()
  cached=nil;stamp=nil;cachedSummary=nil -- Keep consumed token: redisplaying a released reply must not rescan.
 end
 local function allowlist(v)
  local allow={}
  local function add(id,building,label,priority,family)
   if GameInfo.Buildings[building] then allow[id]={building=building,label=label,priority=priority,family=family,attached=false}end
  end
  if v.diagnostic or v.productionOnly or v.finalValues then
   for _,b in ipairs(SPCCultureMeaningModel.Owned)do add(b:sub(10)..'_WRITING',b,'意义延展',2,'MEANING')end
   local yields=v.finalValues and SPCCultureMeaningModel.WriteYields or {'PRODUCTION'}
   for _,y in ipairs(yields)do for _,sign in ipairs({'P','N'})do for bit=0,12 do
    local b='BUILDING_SPC_B060_'..y..'_'..sign..bit;add(b:sub(10)..'_WRITING',b,'旧相邻'..y,6,'GWA')
   end end end
   if v.finalValues then
    add('HD_AMPHITHEATER_WRITING_CULTURE_BOOST','BUILDING_AMPHITHEATER','剧场著作文化',1,'HD')
   end
  else
  add('HD_AMPHITHEATER_WRITING_CULTURE_BOOST','BUILDING_AMPHITHEATER','剧场著作文化',1)
  add('HD_AMPHITHEATER_WRITING_TOURISM_BOOST','BUILDING_AMPHITHEATER','剧场著作旅游业',5)
  for _,b in ipairs(SPCCultureMeaningModel.Owned)do add(b:sub(10)..'_WRITING',b,'意义延展',2)end
  local eras=0;for _ in GameInfo.Eras()do eras=eras+1;assert(eras<=64,'ERA_LIMIT')end
  for n=2,eras do add('SPC_B059_WRITING_CULTURE_D'..n,'BUILDING_SPC_B059_D'..n,'旧对话文化',6)end
  for _,n in ipairs({25,50,100})do add('SPC_B059_WRITING_CULTURE_TEST'..n,'BUILDING_SPC_B059_TEST'..n,'旧对话测试',6)end
  for _,sign in ipairs({'P','N'})do for bit=0,12 do
   local b='BUILDING_SPC_B060_CULTURE_'..sign..bit;add(b:sub(10)..'_WRITING',b,'旧相邻文化',6)
  end end
  end
  for row in GameInfo.BuildingModifiers()do local a=allow[row.ModifierId];if a and row.BuildingType==a.building then a.attached=true end end
  return allow
 end
 local function fixture(P,c,v)
  if v.diagnostic then
   local lines={'所选城 '..text(c:GetName())..'｜玩家'..c:GetOwner()..' / 城市'..c:GetID(),
    '控制 '..text(v.diagnosticStage)..'｜预期 '..text(v.diagnosticExpected)..'｜载体Production配置 '..text(v.configuredProduction)..'｜remainingOwned '..text(v.remainingOwned),
    '城市引用 '..text(v.reference)}
   local ok,now=pcall(diagnosticSnapshot,P,c,v)
   lines[#lines+1]=ok and ('当前原生作品生产力 '..text(now.value)..'｜Writing '..text(now.work.type)..'｜宿主 '..text(now.work.building))
    or ('真实作品读取未确认：'..text(now))
   return lines
  end
  local lines={'所选城 '..text(c:GetName())..'｜玩家'..c:GetOwner()..' / 城市'..c:GetID(),
   v.productionOnly and ('原型状态 '..text(v.mode)..'｜每件Production '..text(v.production)..'｜载体配置 '..text(v.configuredProduction)..'｜合格W '..text(v.count)..'｜remainingOwned '..text(v.remainingOwned))
    or ('原型状态 '..text(v.mode)..' / '..text(v.variant)..'｜配置 S/G/C='..text(v.configuredScience)..'/'..text(v.configuredGold)..'/'..text(v.configuredCulture)),
   '城市引用 '..text(v.reference)}
  if v.productionOnly then
   lines[#lines+1]='首次清理 '..text(v.cleanupStatus)..(v.cleanupError and ('｜'..text(v.cleanupError:match('ME_[A-Z_]+') or 'UNKNOWN')) or '')
   local ok,value=pcall(productionAbsolute,P,c)
   lines[#lines+1]=ok and ('当前原生作品生产力 '..text(value)..'（本城馆藏建筑小计）')
    or ('生产力实际读数未确认：'..text(value)..'；不以0代替未知。')
   return lines
  end
  local ok,why=pcall(function()
   local r=assert(GameInfo.Buildings.BUILDING_AMPHITHEATER,'AMPHITHEATER_DEFINITION_MISSING');local b=c:GetBuildings()
   local has=P.HasBuilding(b,r.Index);lines[#lines+1]='古罗马剧场：存在='..text(has)..'｜掠夺='..(has and text(b:IsPillaged(r.Index)) or '不适用')
   lines[#lines+1]='建筑ID '..r.BuildingType..'｜名称 '..text(Locale.Lookup(r.Name))..' / '..text(r.Name)
   if not has then return end
   local y=assert(GameInfo.Yields.YIELD_CULTURE,'CULTURE_DEFINITION_MISSING')
   local actual=b:GetBuildingYieldFromGreatWorks(y.Index,r.Index)
   assert(type(actual)=='number' and actual==actual and math.abs(actual)<math.huge,'WORK_YIELD_UNKNOWN')
   lines[#lines+1]='剧场内作品实际文化 '..text(actual)..'（不含建筑本体）'
   local slots=b:GetNumGreatWorkSlots(r.Index);assert(integer(slots) and slots<=16,'SLOTS_UNKNOWN')
   local wanted,works={},{}
   for slot=0,slots-1 do local id=b:GetGreatWorkInSlot(r.Index,slot)
    if id~=nil and id~=-1 then local w=assert(GameInfo.GreatWorks[b:GetGreatWorkTypeFromIndex(id)],'WORK_UNKNOWN');wanted[w.GreatWorkType]=0;works[#works+1]=w end
   end
   for row in GameInfo.GreatWork_YieldChanges()do if wanted[row.GreatWorkType]~=nil and row.YieldType=='YIELD_CULTURE' then wanted[row.GreatWorkType]=wanted[row.GreatWorkType]+row.YieldChange end end
   for i=1,math.min(4,#works)do local w=works[i];lines[#lines+1]=text(w.GreatWorkType)..'｜定义基础文化 '..text(wanted[w.GreatWorkType])end
   if #works>4 then lines[#lines+1]='另'..(#works-4)..'件未展开。'end
  end)
  if not ok then lines[#lines+1]='建筑/作品读取未完整：'..text(why)end
  return lines
 end
 local function collect(P,c,v)
  local allow=allowlist(v);local rows,errors={},{};local objectReads={}
  local function object(id)
   local key=type(id)..':'..tostring(id);if objectReads[key] then return objectReads[key]end
   local pk,p=call('GetObjectsPlayerId',id);local tk,t=call('GetObjectType',id);local sk,raw=call('GetObjectString',id)
   local valid=pk and integer(p) and tk and type(t)=='string' and sk and type(raw)=='string'
   local o={player=pk and integer(p) and p or 'UNKNOWN',kind=tk and type(t)=='string' and t or 'UNKNOWN',raw=sk and type(raw)=='string' and text(raw) or 'UNKNOWN'}
   if valid then o.mapping,o.districtType=mapDistrict(t,raw,p,c)else o.mapping='UNKNOWN:API' end;objectReads[key]=o;return o
  end; local complete=true;local foreign,unknown,defs=0,0,0
  local function fail(reason)complete=false;if #errors<3 then errors[#errors+1]=text(reason)end end
  for id,a in pairs(allow)do if not a.attached then fail('ATTACHMENT_MISSING:'..id)end end
  local ok,ids=call('GetModifiers');local n,why
  if ok then n,why=array(ids,LIMIT)end
  if not n then fail(why or ids) else
   for i=1,n do
    local id=ids[i];local good,def=call('GetModifierDefinition',id);defs=defs+1
    if not good or type(def)~='table' or type(def.Id)~='string' then fail('DEFINITION_UNKNOWN')
    elseif allow[def.Id] then
     local ownOK,owner=call('GetModifierOwner',id);local playerOK,player=false,nil
     if ownOK and integer(owner) then playerOK,player=call('GetObjectsPlayerId',owner)end
     if playerOK and integer(player) and player~=c:GetOwner() then foreign=foreign+1
     else
      if #rows>=HITS then fail('MATCH_LIMIT');break end
      local row={mapping='UNKNOWN:OWNER',subjectRows={},instanceID=text(id),id=def.Id,family=allow[def.Id].family,label=allow[def.Id].label,priority=allow[def.Id].priority,player='UNKNOWN',active='UNKNOWN',ownerType='UNKNOWN',raw='UNKNOWN',subjects='UNKNOWN'}
      if playerOK and integer(player) then row.player=player else unknown=unknown+1;fail('OWNER_PLAYER_UNKNOWN')end
      if ownOK and integer(owner) then
       local o=object(owner);row.ownerType=text(o.kind);row.raw=o.raw;row.mapping=o.mapping;row.districtType=o.districtType
       if o.player~=row.player then row.mapping='UNKNOWN:OWNER_CHANGED';fail('OWNER_CHANGED')end
       if o.kind=='UNKNOWN' then fail('OWNER_TYPE_UNKNOWN')end
       if o.raw=='UNKNOWN' then fail('OWNER_STRING_UNKNOWN')end
      else fail('OWNER_UNKNOWN')end
      local ak,a=call('GetModifierActive',id);if ak and type(a)=='boolean' then row.active=tostring(a)else fail('ACTIVE_UNKNOWN')end
      local args=def.Arguments
      if type(args)=='table' then
       if type(args.GreatWorkObjectType)~='string' or (args.YieldChange==nil and args.ScalingFactor==nil) then fail('ARGUMENTS_UNKNOWN')end
       for _,key in ipairs({'YieldType','YieldChange','ScalingFactor'})do local value=args[key];if value~=nil and type(value)~='string' and type(value)~='number' then fail('ARGUMENTS_UNKNOWN:'..key)end end
       if v.finalValues and row.mapping=='本城已核验' and allow[def.Id].family=='MEANING' then
        local required=GameInfo.Buildings[allow[def.Id].building].PrereqDistrict
        if row.districtType=='UNKNOWN' or not row.districtType then fail('CARRIER_HOST_UNKNOWN')
        elseif row.districtType~=required then fail('CARRIER_HOST_MISMATCH')end
       end
       row.yield=text(args.YieldType);row.args='对象='..text(args.GreatWorkObjectType)..' yield='..text(args.YieldType)..' flat='..text(args.YieldChange)..' scale='..text(args.ScalingFactor)
      else row.args='Arguments UNKNOWN';fail('ARGUMENTS_UNKNOWN')end
      local sk,subjects=call('GetModifierSubjects',id)
      if not sk then fail('SUBJECTS_API_UNKNOWN')
      elseif subjects==nil then row.subjects='nil'
      else local count,err=array(subjects,SUBJECTS)
       if count then
        row.subjects=count==0 and 'empty' or tostring(count)..'对象'
        for j=1,math.min(count,3)do local o=object(subjects[j]);row.subjectRows[#row.subjectRows+1]='接收对象'..j..'｜'..o.mapping..'｜玩家'..text(o.player)..'｜'..text(o.kind)..'｜'..o.raw end
        if count>3 then row.subjectRows[#row.subjectRows+1]='另'..(count-3)..'个接收对象未展开，不声称全部recipient核验。'end
       else fail('SUBJECTS_'..err)end
      end
      rows[#rows+1]=row
     end
    end
   end
  end
  ids=nil
  table.sort(rows,function(a,b)
   if v.diagnostic or v.productionOnly or v.finalValues then
    local function rank(r)return (r.mapping=='本城已核验' and 0 or 10)+(r.yield=='YIELD_PRODUCTION' and 0 or 5)+(r.family=='MEANING' and 0 or 1)end
    local ar,br=rank(a),rank(b);if ar~=br then return ar<br end
   end
   if a.priority~=b.priority then return a.priority<b.priority end;if a.id~=b.id then return a.id<b.id end
   if a.raw~=b.raw then return a.raw<b.raw end;return a.instanceID<b.instanceID
  end)
  local lines={'Modifier诊断｜'..(complete and '读取完整' or '读取不完整')..'｜实例城市归属见各项（未核验=UNKNOWN）',
   '只观察实例；Active=true不代表收益已入账。无需过回合，截图本报告即可。'}
  for _,s in ipairs(fixture(P,c,v))do lines[#lines+1]=s end
  lines[#lines+1]='本玩家匹配实例 '..(#rows-unknown)..'｜玩家未知 '..unknown..'｜其它玩家跳过 '..foreign..'｜已检查定义 '..defs
  if #rows==0 then lines[#lines+1]=complete and '本次未观察到匹配实例；不等于本城没有效果。' or '读取不完整，不能解释为零实例。'end
  if v.diagnostic or v.productionOnly or v.finalValues then
   local meaning,active,gwa,unmapped=0,0,0,0
   for _,r in ipairs(rows)do
    if r.mapping=='本城已核验' then
     if r.family=='MEANING' then meaning=meaning+1;if r.active=='true' then active=active+1 end
     elseif r.family=='GWA' then gwa=gwa+1 end
    elseif r.mapping:sub(1,8)=='UNKNOWN:' then unmapped=unmapped+1 end
   end
   lines[#lines+1]='本城Meaning Writing实例 '..meaning..'（Active=true '..active..'）｜本城旧GWA '..(v.finalValues and '六产出' or 'Production')..'实例 '..gwa..'｜城市UNKNOWN '..unmapped
   if v.diagnosticStage=='OFF' or (v.productionOnly or v.finalValues) and v.mode=='OFF' then
    lines[#lines+1]=(meaning>0 or v.remainingOwned and v.remainingOwned>0) and '异常：OFF仍观察到本城Meaning实例或精确载体；不能确认撤销。'
     or ((not complete or unmapped>0) and '撤销未确认：读取不完整／城市UNKNOWN。' or '本次未观察到本城Meaning Writing实例；真实退出收益及旧系统恢复另行核对。')
   end
  end
  local owners={};local ownerCount=0
  for i=1,math.min(12,#rows)do local row=rows[i];local key=tostring(row.player)..'|'..row.ownerType..'|'..row.raw
   if not owners[key] then ownerCount=ownerCount+1;owners[key]=ownerCount;lines[#lines+1]='归属对象'..ownerCount..'｜玩家 '..text(row.player)..'｜'..row.ownerType..'｜'..row.raw end
   lines[#lines+1]=row.label..'｜Active='..row.active..'｜归属对象'..owners[key]..'｜'..row.mapping..'｜宿主区域='..text(row.districtType)..'｜subjects='..row.subjects
   lines[#lines+1]=((v.diagnostic or v.productionOnly or v.finalValues) and ('实例ID '..row.instanceID..'｜') or '')..row.id..'｜'..row.args
   for _,subject in ipairs(row.subjectRows)do lines[#lines+1]=subject end
  end
  if #rows>12 then lines[#lines+1]='另'..(#rows-12)..'个匹配实例未展开；本报告不声称完成全部效果核对。'end
  for _,e in ipairs(errors)do lines[#lines+1]='未确认：'..e end
  local meaning,gwa,hd,unmapped=0,0,0,0
  for _,r in ipairs(rows)do
   if r.mapping=='本城已核验' then
    if r.family=='MEANING' then meaning=meaning+1 elseif r.family=='GWA' then gwa=gwa+1 elseif r.family=='HD' then hd=hd+1 end
   elseif r.mapping:sub(1,8)=='UNKNOWN:' then unmapped=unmapped+1 end
  end
  local summary=string.format('本城著作实例：意义延展%d／旧系统%d／HD文化%d',meaning,gwa,hd)
  if not complete or unmapped>0 then summary=summary..'；读取不完整或归属未知，不能判定通过。'
  elseif v.mode=='OFF' and (meaning>0 or (v.remainingOwned or 0)>0) then summary=summary..'；异常：结束后仍有残留。'
  elseif v.mode=='ACTIVE' and gwa>0 then summary=summary..'；异常：旧系统仍有实例。'
  elseif v.mode=='OFF' then summary=summary..'；未见Meaning著作实例。'end
  return table.concat(lines,'\n'),summary
 end
 function SPCBoostGreatWorkRead.Modifiers(P,c,v,token,requestedReference)
  local ok,key=pcall(signature,c,v)
  if not ok or type(token)~='string' or v.token~=token or requestedReference~=v.reference then
   SPCBoostGreatWorkRead.ClearModifierRead();lastToken=token;return 'Modifier诊断已过期（STALE）；请重新选城并右键读取。'
  end
  if token==lastToken then
   if cached and stamp==key then return cached end
   SPCBoostGreatWorkRead.ClearModifierRead() -- Keep token consumed; drop stale summary/details without rescanning.
   return 'Modifier诊断已释放或过期；请右键重新读取。'
  end
  lastToken=token;cached=nil;stamp=nil
  local good,report,summary=pcall(collect,P,c,v)
  local fresh,after=pcall(signature,c,v)
  if not fresh or key~=after then report='Modifier诊断已过期（STALE）；不采用本次实例。'
  elseif not good then report='Modifier诊断未完整（API_READ_BOUNDARY）：'..text(report)..'；未改变任何收益，请截图。'end
  cached=report;stamp=key;cachedSummary=good and fresh and key==after and summary or report;return report
 end
 function SPCBoostGreatWorkRead.ModifierSummary(token)
  return token==lastToken and cachedSummary or '实例读取未确认；重新右键读取。'
 end
 function SPCBoostGreatWorkRead.ModifierDetails(token)
  return token==lastToken and cached or nil
 end
end
