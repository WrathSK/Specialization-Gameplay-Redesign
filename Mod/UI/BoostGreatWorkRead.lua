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
local meaningBaseline
function SPCBoostGreatWorkRead.Meaning(P,c,v,mark)
 local ok,text=pcall(function()
  assert(v.owner==Game.GetLocalPlayer() and v.cityID==c:GetID() and v.reference==SPCNetworkInput.Reference(c),'ME_UI_REFERENCE_CHANGED')
  if v.mode=='OFF' then meaningBaseline=nil;return '测试已关闭；未保留原生收益基线。'end
  local b=c:GetBuildings();local totals={SCIENCE=0,GOLD=0};local signature={}
  for r in GameInfo.Buildings()do if P.HasBuilding(b,r.Index) then
   local n=b:GetNumGreatWorkSlots(r.Index);assert(type(n)=='number' and n>=0,'ME_UI_SLOTS_UNKNOWN')
   if n>0 then
    local known,themed=pcall(b.IsBuildingThemedCorrectly,b,r.Index)
    signature[#signature+1]='B'..r.Index..':'..(known and tostring(themed) or 'UNKNOWN')
    for slot=0,n-1 do local id=b:GetGreatWorkInSlot(r.Index,slot)
     if id~=nil and id~=-1 then signature[#signature+1]='W'..id..'@'..r.Index..':'..slot..':'..tostring(b:GetGreatWorkTypeFromIndex(id))end
    end
    for _,y in ipairs({'SCIENCE','GOLD'})do
     local value=b:GetBuildingYieldFromGreatWorks(P.Info('Yields','YIELD_'..y).Index,r.Index)
     assert(type(value)=='number' and value==value,'ME_UI_NATIVE_YIELD_UNKNOWN');totals[y]=totals[y]+value
    end
   end
  end end
  table.sort(signature);local sig=table.concat(signature,';');local turn=Game.GetCurrentGameTurn()
  local rates={};local ratesOK=pcall(function()
   for _,y in ipairs({'SCIENCE','GOLD'})do local n=c:GetYield(P.Info('Yields','YIELD_'..y).Index);assert(type(n)=='number' and n==n,'ME_UI_CITY_YIELD_UNKNOWN');rates[y]=n end
  end)
  if mark and v.mode=='BASELINE' and not v.error and v.oldHeld then
   meaningBaseline={reference=v.reference,signature=sig,turn=turn,totals=totals,rates=ratesOK and rates or nil}
  end
  local lines={string.format('原生巨作收益：科研 %.4f / 金币 %.4f',totals.SCIENCE,totals.GOLD)}
  if v.mode=='BASELINE' then lines[#lines+1]=meaningBaseline and '已记录关闭测试收益时的本城基线。' or '基线未确认，先处理上方异常。'
  elseif meaningBaseline and meaningBaseline.reference==v.reference and meaningBaseline.signature==sig then
   lines[#lines+1]=string.format('相同馆藏基线 → 当前：科研 Δ%+.4f / 金币 Δ%+.4f',totals.SCIENCE-meaningBaseline.totals.SCIENCE,totals.GOLD-meaningBaseline.totals.GOLD)
  else lines[#lines+1]='馆藏/所在建筑/主题或会话已变；差值基线不可用。可结束→准备→启用重新对照。'end
  if ratesOK then
   lines[#lines+1]=string.format('整城原生率：科研 %.4f / 金币 %.4f（含其它来源与倍率）',rates.SCIENCE,rates.GOLD)
   if v.mode=='ACTIVE' and meaningBaseline and meaningBaseline.reference==v.reference and meaningBaseline.signature==sig and meaningBaseline.rates then
    lines[#lines+1]=string.format('整城率对照 Δ%+.4f 科研 / Δ%+.4f 金币；仅在其它事实不变时比较。',rates.SCIENCE-meaningBaseline.rates.SCIENCE,rates.GOLD-meaningBaseline.rates.GOLD)
   end
  else lines[#lines+1]='整城原生率不可读；未将未知记为0。'end
  lines[#lines+1]='作品分项和整城率是原生读取；正常过回合核对持续生效，未自动判定实机PASS。'
  return table.concat(lines,'\n')
 end)
 return ok and text or ('原生作品科研/金币暂不可读：'..(tostring(text):match('ME_[A-Z_]+') or '原生接口未知')..'；不将未知记为0。')
end
