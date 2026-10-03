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

-- One on-demand UI baseline, never a Gameplay source or a persistent snapshot.
-- Four UI-only readings for one current fixture. Never persisted or used by Gameplay.
local meaningReadings
function SPCBoostGreatWorkRead.Meaning(P,c,v,mark)
 local ok,text=pcall(function()
  assert(v.owner==Game.GetLocalPlayer() and v.cityID==c:GetID() and v.reference==SPCNetworkInput.Reference(c),'ME_UI_REFERENCE_CHANGED')
  if v.mode=='OFF' then meaningReadings=nil;return '测试已关闭；本次四态读数已释放。'end
  assert(not v.error and not v.configurationError and not v.dialogueError and v.oldHeld and v.planStatus=='READY','ME_UI_CONFIGURATION_PENDING')
  local percent=(v.mode=='SCALED' or v.mode=='SCALED_BASELINE') and 100 or 0
  assert(v.dialoguePercent==percent,'ME_UI_DIALOGUE_PENDING')
  local on=v.mode=='ACTIVE' or v.mode=='SCALED'
  assert(v.configuredScience==(on and v.science or 0) and v.configuredGold==(on and v.gold or 0) and v.configuredCulture==(on and v.culture or 0),'ME_UI_CONFIGURATION_PENDING')
  local b=c:GetBuildings();local totals={SCIENCE=0,GOLD=0,CULTURE=0};local signature={};local baseCulture=0;local baseKnown=true;local themeBuildings,themeWorks,workCount=0,0,0;local buildingRows={}
  local nativeBase={}
  if GameInfo.GreatWork_YieldChanges then for row in GameInfo.GreatWork_YieldChanges()do if row.YieldType=='YIELD_CULTURE' then nativeBase[row.GreatWorkType]=(nativeBase[row.GreatWorkType] or 0)+row.YieldChange end end else baseKnown=false end
  for r in GameInfo.Buildings()do if P.HasBuilding(b,r.Index) then
   local n=b:GetNumGreatWorkSlots(r.Index);assert(type(n)=='number' and n>=0,'ME_UI_SLOTS_UNKNOWN')
   if n>0 then
    local known,themed=pcall(b.IsBuildingThemedCorrectly,b,r.Index)
    assert(known and type(themed)=='boolean','ME_UI_THEME_UNKNOWN')
    signature[#signature+1]='B'..r.Index..':'..tostring(themed)
    local count=0;local rowYields={}
    for slot=0,n-1 do local id=b:GetGreatWorkInSlot(r.Index,slot)
     if id~=nil and id~=-1 then
      local typ=b:GetGreatWorkTypeFromIndex(id);local row=GameInfo.GreatWorks[typ]
      assert(row,'ME_UI_WORK_DEFINITION_UNKNOWN')
      signature[#signature+1]='W'..id..'@'..r.Index..':'..slot..':'..row.GreatWorkType
      local cat=(row.GreatWorkObjectType or ''):gsub('GREATWORKOBJECT_','')
      if ({WRITING=true,MUSIC=true,SCULPTURE=true,PORTRAIT=true,LANDSCAPE=true,RELIGIOUS=true,ARTIFACT=true})[cat] then count=count+1;workCount=workCount+1;baseCulture=baseCulture+(nativeBase[row.GreatWorkType] or 0)end
     end
    end
    for _,y in ipairs({'SCIENCE','GOLD','CULTURE'})do
     local value=b:GetBuildingYieldFromGreatWorks(P.Info('Yields','YIELD_'..y).Index,r.Index)
     assert(type(value)=='number' and value==value and math.abs(value)<math.huge,'ME_UI_NATIVE_YIELD_UNKNOWN');totals[y]=totals[y]+value;rowYields[y]=value
    end
    if count>0 then
     if themed then themeBuildings=themeBuildings+1;themeWorks=themeWorks+count end
     buildingRows[#buildingRows+1]=string.format('%s｜%d件／%s｜科研%.2f 金币%.2f 文化%.2f',Locale.Lookup(r.Name or r.BuildingType),count,themed and '已主题化' or '未主题化',rowYields.SCIENCE,rowYields.GOLD,rowYields.CULTURE)
    end
   end
  end end
  assert(workCount==v.count,'ME_UI_WORK_COUNT_MISMATCH')
  local turn=Game.GetCurrentGameTurn()
  local populationOK,population=pcall(c.GetPopulation,c)
  local qualification=table.concat({tostring(v.currentIdentity),tostring(v.currentPotential),tostring(v.currentActive),tostring(v.currentActiveStatus)},':')
  table.sort(signature);local key=tostring(v.variant or 'SPLIT')..'|'..v.reference..'|'..v.stamp..'|'..v.count..'|'..turn..'|'..qualification..'|'..(populationOK and tostring(population) or 'UNKNOWN')..'|'..table.concat(signature,';')
  -- Optional second native readout; unavailable is never a successful zero.
  local cityOK,cityCulture=pcall(c.GetYield,c,P.Info('Yields','YIELD_CULTURE').Index)
  if cityOK and type(cityCulture)=='number' and cityCulture==cityCulture and math.abs(cityCulture)<math.huge then totals.cityCulture=cityCulture end
  local lines={string.format('原生作品收益：科研 %.2f / 金币 %.2f / 文化 %.2f',totals.SCIENCE,totals.GOLD,totals.CULTURE),totals.cityCulture and string.format('整城文化 %.2f（辅助读数，含其它修正）',totals.cityCulture) or '整城文化未确认；作品读数仍保留。'}
  lines[#lines+1]=string.format('主题化%d座／%d件；追加预期保持固定，不乘主题倍率。',themeBuildings,themeWorks)
  for i=1,math.min(#buildingRows,4)do lines[#lines+1]=buildingRows[i]end
  if #buildingRows>4 then lines[#lines+1]='另有'..(#buildingRows-4)..'座馆藏建筑；合计已包含，明细仅显示前4座。'end
  if mark and v.mode=='BASELINE' then meaningReadings={key=key,rows={}}end
  local valid=meaningReadings and meaningReadings.key==key
  if valid then meaningReadings.rows[v.mode]=totals end -- Explicit read can refresh this phase; previous phases remain fixed.
  if not valid then
   meaningReadings=nil;lines[#lines+1]='回合/人口/馆藏/位置/主题/领域D/资格已变，四态对照无效；结束后重新准备。'
  else
   local q=meaningReadings.rows
   lines[#lines+1]='本阶段'..(q[v.mode] and '已记录；右键只刷新当前阶段读数，不推进实验。' or '未记录；只读不能补造基线。')
   if q.BASELINE and q.ACTIVE then
    lines[#lines+1]=string.format('关闭旧对话：作品文化 Δ%+.2f；预期 +%g。',q.ACTIVE.CULTURE-q.BASELINE.CULTURE,v.totalCulture)
    for _,y in ipairs({'SCIENCE','GOLD'})do
     local label=y=='SCIENCE' and '科研' or '金币'
     lines[#lines+1]=string.format('关闭旧对话：作品%s Δ%+.2f；预期 +%g。',label,q.ACTIVE[y]-q.BASELINE[y],y=='SCIENCE' and v.totalScience or v.totalGold)
    end
    if q.BASELINE.cityCulture~=nil and q.ACTIVE.cityCulture~=nil then lines[#lines+1]=string.format('对应整城文化 Δ%+.2f（含其它修正，不代替作品／结算门禁）。',q.ACTIVE.cityCulture-q.BASELINE.cityCulture)end
   end
   if q.BASELINE and q.ACTIVE and q.SCALED and q.SCALED_BASELINE then
    lines[#lines+1]=string.format('旧对话100%%：作品文化 Δ%+.2f；应与上行相等。',q.SCALED.CULTURE-q.SCALED_BASELINE.CULTURE)
    for _,y in ipairs({'SCIENCE','GOLD'})do
     local label=y=='SCIENCE' and '科研' or '金币'
     lines[#lines+1]=string.format('旧对话100%%：作品%s Δ%+.2f；预期 +%g。',label,q.SCALED[y]-q.SCALED_BASELINE[y],y=='SCIENCE' and v.totalScience or v.totalGold)
    end
    if q.SCALED.cityCulture~=nil and q.SCALED_BASELINE.cityCulture~=nil then lines[#lines+1]=string.format('对应整城文化 Δ%+.2f（含其它修正）。',q.SCALED.cityCulture-q.SCALED_BASELINE.cityCulture)end
    lines[#lines+1]=string.format('旧对话增幅：无追加 Δ%+.2f / 有追加 Δ%+.2f。',q.SCALED_BASELINE.CULTURE-q.BASELINE.CULTURE,q.SCALED.CULTURE-q.ACTIVE.CULTURE)
    lines[#lines+1]=baseKnown and string.format('定义原生文化合计 %g；用于区分HD平加与原生基值。',baseCulture) or '作品定义基值不可读；不把未知记为0。'
   end
  end
  lines[#lines+1]='同回合同一馆藏对照；右键仅刷新当前阶段。读数可延迟，其它修正须保持不变，不自动判定结算PASS。'
  return table.concat(lines,'\n')
 end)
 if not ok then meaningReadings=nil end -- Unknown/error invalidates previously accepted comparisons too.
 return ok and text or ('四态原生读数未确认：'..(tostring(text):match('ME_[A-Z_]+') or '原生接口未知')..'；不记录成功基线。')
end
