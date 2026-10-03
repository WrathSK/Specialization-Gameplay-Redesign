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

-- B156: explicit UI read only. Never retain native handles/tables between reads.
include('CultureMeaningModel')
do
 local lastToken,cached,stamp
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
 -- B157: only the complete District format observed in B156 is interpreted.
 -- GameEffects object IDs are NOT city/district IDs. SubType/SubValue are opaque.
 local function mapDistrict(kind,raw,player,c)
  if kind~='LOC_MODIFIER_OBJECT_DISTRICT' or type(raw)~='string' or #raw>512 then return 'UNKNOWN:FORMAT' end
  local did,pid,sub,val,cid=raw:match('^District: (%d+), Owner: (%d+), SubType: (%d+), SubValue: (%d+), City: (%d+)$')
  if not did then return 'UNKNOWN:FORMAT' end
  did,pid,cid=tonumber(did),tonumber(pid),tonumber(cid)
  for _,n in ipairs({did,pid,cid})do if not integer(n) or n>9007199254740991 then return 'UNKNOWN:ID' end end
  if player~=pid then return 'UNKNOWN:OWNER_CONFLICT' end
  local ok,result=pcall(function()
   local city=assert(CityManager.GetCity(pid,cid),'CITY_UNAVAILABLE')
   assert(city:GetOwner()==pid and city:GetID()==cid,'CITY_CONFLICT')
   local district=assert(city:GetDistricts():FindID(did),'DISTRICT_UNAVAILABLE')
   assert(district:GetID()==did,'DISTRICT_CONFLICT')
   local parent=assert(district:GetCity(),'DISTRICT_CITY_UNAVAILABLE')
   local ref=SPCNetworkInput.Reference(city)
   assert(SPCNetworkInput.Reference(parent)==ref,'DISTRICT_CITY_CONFLICT')
   if pid==c:GetOwner() and cid==c:GetID() then
    assert(ref==SPCNetworkInput.Reference(c),'REFERENCE_CONFLICT')
    return '本城已核验'
   end
   return '其它城已核验: '..pid..'/'..cid
  end)
  return ok and result or 'UNKNOWN:OBJECT_CHECK'
 end
 local function signature(c,v)
  local selected=UI.GetHeadSelectedCity()
  assert(selected and selected:GetOwner()==Game.GetLocalPlayer() and c:GetOwner()==Game.GetLocalPlayer(),'STALE_CITY')
  local ref=SPCNetworkInput.Reference(c)
  assert(SPCNetworkInput.Reference(selected)==ref and v.owner==c:GetOwner() and v.cityID==c:GetID() and v.reference==ref,'STALE_REFERENCE')
  local parts={ref,tostring(Game.GetCurrentGameTurn())}
  for _,k in ipairs({'mode','variant','stamp','configuredScience','configuredGold','configuredCulture','dialoguePercent','count','error','configurationError'})do parts[#parts+1]=text(v[k])end
  return table.concat(parts,'|')
 end
 function SPCBoostGreatWorkRead.ClearModifierRead()
  cached=nil;stamp=nil -- Keep consumed token: redisplaying a released reply must not rescan.
 end
 local function allowlist()
  local allow={}
  local function add(id,building,label,priority)
   if GameInfo.Buildings[building] then allow[id]={building=building,label=label,priority=priority,attached=false}end
  end
  add('HD_AMPHITHEATER_WRITING_CULTURE_BOOST','BUILDING_AMPHITHEATER','剧场著作文化',1)
  add('HD_AMPHITHEATER_WRITING_TOURISM_BOOST','BUILDING_AMPHITHEATER','剧场著作旅游业',5)
  for _,b in ipairs(SPCCultureMeaningModel.Owned)do add(b:sub(10)..'_WRITING',b,'意义延展',2)end
  local eras=0;for _ in GameInfo.Eras()do eras=eras+1;assert(eras<=64,'ERA_LIMIT')end
  for n=2,eras do add('SPC_B059_WRITING_CULTURE_D'..n,'BUILDING_SPC_B059_D'..n,'旧对话文化',6)end
  for _,n in ipairs({25,50,100})do add('SPC_B059_WRITING_CULTURE_TEST'..n,'BUILDING_SPC_B059_TEST'..n,'旧对话测试',6)end
  for _,sign in ipairs({'P','N'})do for bit=0,12 do
   local b='BUILDING_SPC_B060_CULTURE_'..sign..bit;add(b:sub(10)..'_WRITING',b,'旧相邻文化',6)
  end end
  for row in GameInfo.BuildingModifiers()do local a=allow[row.ModifierId];if a and row.BuildingType==a.building then a.attached=true end end
  return allow
 end
 local function fixture(P,c,v)
  local lines={'所选城 '..text(c:GetName())..'｜玩家'..c:GetOwner()..' / 城市'..c:GetID(),
   '原型状态 '..text(v.mode)..' / '..text(v.variant)..'｜配置 S/G/C='..text(v.configuredScience)..'/'..text(v.configuredGold)..'/'..text(v.configuredCulture),
   '城市引用 '..text(v.reference)}
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
  local allow=allowlist();local rows,errors={},{};local objectReads={}
  local function object(id)
   local key=type(id)..':'..tostring(id);if objectReads[key] then return objectReads[key]end
   local pk,p=call('GetObjectsPlayerId',id);local tk,t=call('GetObjectType',id);local sk,raw=call('GetObjectString',id)
   local valid=pk and integer(p) and tk and type(t)=='string' and sk and type(raw)=='string'
   local o={player=pk and integer(p) and p or 'UNKNOWN',kind=tk and type(t)=='string' and t or 'UNKNOWN',raw=sk and type(raw)=='string' and text(raw) or 'UNKNOWN'}
   o.mapping=valid and mapDistrict(t,raw,p,c) or 'UNKNOWN:API';objectReads[key]=o;return o
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
      local row={mapping='UNKNOWN:OWNER',subjectRows={},id=def.Id,label=allow[def.Id].label,priority=allow[def.Id].priority,player='UNKNOWN',active='UNKNOWN',ownerType='UNKNOWN',raw='UNKNOWN',subjects='UNKNOWN'}
      if playerOK and integer(player) then row.player=player else unknown=unknown+1;fail('OWNER_PLAYER_UNKNOWN')end
      if ownOK and integer(owner) then
       local o=object(owner);row.ownerType=text(o.kind);row.raw=o.raw;row.mapping=o.mapping
       if o.player~=row.player then row.mapping='UNKNOWN:OWNER_CHANGED';fail('OWNER_CHANGED')end
       if o.kind=='UNKNOWN' then fail('OWNER_TYPE_UNKNOWN')end
       if o.raw=='UNKNOWN' then fail('OWNER_STRING_UNKNOWN')end
      else fail('OWNER_UNKNOWN')end
      local ak,a=call('GetModifierActive',id);if ak and type(a)=='boolean' then row.active=tostring(a)else fail('ACTIVE_UNKNOWN')end
      local args=def.Arguments
      if type(args)=='table' then
       if type(args.GreatWorkObjectType)~='string' or (args.YieldChange==nil and args.ScalingFactor==nil) then fail('ARGUMENTS_UNKNOWN')end
       for _,key in ipairs({'YieldType','YieldChange','ScalingFactor'})do local value=args[key];if value~=nil and type(value)~='string' and type(value)~='number' then fail('ARGUMENTS_UNKNOWN:'..key)end end
       row.args='对象='..text(args.GreatWorkObjectType)..' yield='..text(args.YieldType)..' flat='..text(args.YieldChange)..' scale='..text(args.ScalingFactor)
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
  table.sort(rows,function(a,b)if a.priority~=b.priority then return a.priority<b.priority end;if a.id~=b.id then return a.id<b.id end;return a.raw<b.raw end)
  local lines={'Modifier诊断｜'..(complete and '读取完整' or '读取不完整')..'｜实例城市归属见各项（未核验=UNKNOWN）',
   '只观察实例；Active=true不代表收益已入账。无需过回合，截图本报告即可。'}
  for _,s in ipairs(fixture(P,c,v))do lines[#lines+1]=s end
  lines[#lines+1]='本玩家匹配实例 '..(#rows-unknown)..'｜玩家未知 '..unknown..'｜其它玩家跳过 '..foreign..'｜已检查定义 '..defs
  if #rows==0 then lines[#lines+1]=complete and '本次未观察到匹配实例；不等于本城没有效果。' or '读取不完整，不能解释为零实例。'end
  local owners={};local ownerCount=0
  for i=1,math.min(12,#rows)do local row=rows[i];local key=tostring(row.player)..'|'..row.ownerType..'|'..row.raw
   if not owners[key] then ownerCount=ownerCount+1;owners[key]=ownerCount;lines[#lines+1]='归属对象'..ownerCount..'｜玩家 '..text(row.player)..'｜'..row.ownerType..'｜'..row.raw end
   lines[#lines+1]=row.label..'｜Active='..row.active..'｜归属对象'..owners[key]..'｜'..row.mapping..'｜subjects='..row.subjects
   lines[#lines+1]=row.id..'｜'..row.args
   for _,subject in ipairs(row.subjectRows)do lines[#lines+1]=subject end
  end
  if #rows>12 then lines[#lines+1]='另'..(#rows-12)..'个匹配实例未展开；本报告不声称完成全部效果核对。'end
  for _,e in ipairs(errors)do lines[#lines+1]='未确认：'..e end
  return table.concat(lines,'\n')
 end
 function SPCBoostGreatWorkRead.Modifiers(P,c,v,token,requestedReference)
  local ok,key=pcall(signature,c,v)
  if not ok or type(token)~='string' or v.token~=token or requestedReference~=v.reference then
   SPCBoostGreatWorkRead.ClearModifierRead();lastToken=token;return 'Modifier诊断已过期（STALE）；请重新选城并右键读取。'
  end
  if token==lastToken then return cached and stamp==key and cached or 'Modifier诊断已释放或过期；请右键重新读取。'end
  lastToken=token;cached=nil;stamp=nil
  local good,report=pcall(collect,P,c,v)
  local fresh,after=pcall(signature,c,v)
  if not fresh or key~=after then report='Modifier诊断已过期（STALE）；不采用本次实例。'
  elseif not good then report='Modifier诊断未完整（API_READ_BOUNDARY）：'..text(report)..'；未改变任何收益，请截图。'end
  cached=report;stamp=key;return report
 end
end
