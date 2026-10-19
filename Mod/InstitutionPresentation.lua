-- Shared institution display model. No gameplay calls or mutations.
SPCInstitutionPresentation={}
local M=SPCInstitutionPresentation
M.Rows={
{level=1,name="学者结社",text="学者在此结成稳定的研究共同体，奠定城市科研专业化的基础。[NEWLINE][NEWLINE]基础专家支持[NEWLINE]每名正在工作的科研专家额外提供 +3 食物、+3 生产力。"},
{level=2,name="研修院",text="系统的研修与人才培养，使科研从个人志业升华为城市的长期事业。[NEWLINE][NEWLINE]人才培养[NEWLINE]每名正在工作的科研专家额外提供 2 点基础大科学家点数（可受其它伟人点数百分比加成影响）。本城学院区域及其每一级建筑各提供 +1 住房。"},
{level=3,name="学术联合会",text="不同专业领域在此交流碰撞，使研究成果与城市实践相互促进。[NEWLINE][NEWLINE]跨学科研究[NEWLINE]本城除学院外的合格专业区域，将其基础相邻产出总和的 50% 转化为科技值（汇总后向下取整）。仅计入已建成且未被掠夺的区域；不计入政策等相邻加成倍率或其它非相邻产出（适用区域见专业领域表）。[NEWLINE][NEWLINE]学以致用[NEWLINE]每名正在工作的科研专家，可从本城每个其它合格专业领域获得对应产出：该领域每有 1 点基础设施深度，便提供 0.5 份对应产出（金币每份为 3 点，其它产出每份为 1 点）。同产出领域分别计算后相加，同一领域的多个区域取最高单区域基础设施深度。每名专家的各项收益先向下取整，再按专家人数结算。"},
{level=4,name="学术总署",text="完善的科研设施、学术组织与长期传统，共同支撑起深度的学术研究。[NEWLINE][NEWLINE]科研基础设施[NEWLINE]本城学院每有 1 点基础设施深度，每名正在工作的科研专家便额外提供 +1 基础科技值（基础设施深度上限为 10 点；达到 10 点时，5 名专家共提供 +50 基础科技值）。[NEWLINE][NEWLINE]学术主持[NEWLINE]每名正在工作的科研专家，使本城每座未遭掠夺的普通学院一至四级建筑额外提供 +1 基础科技值。被掠夺的建筑不计入且不享受此收益；此额外科技值不会提高基础设施深度。[NEWLINE][NEWLINE]学术传统[NEWLINE]本城首次达到科研专业潜力 4 级后，开始积累学术传统：初始使本城科技值提高 5%；标准速度下，累计满 10、20、30、40 回合时分别提高至 10%、15%、20%、25%（上限 25%；其它游戏速度按比例缩放各阶段回合数并向下取整）。只要仍保有科研专业身份，即使暂未启用 4 级能力，传统仍继续积累。转出科研专业后停止积累，但保留已累计回合数；重新转入科研专业时继续积累（不补算离开期间的回合）。启用 4 级能力时，按已保留的传统累计进度生效。"}
}
-- Keep row lists extensible: one level may contain multiple sibling institutions.
M.BySpecialization={RESEARCH=M.Rows,CULTURE={},INDUSTRY={},COMMERCE={}}
for level=1,4 do
 for _,kind in ipairs({'CULTURE','INDUSTRY','COMMERCE'})do
  M.BySpecialization[kind][level]={level=level,name='LOC_SPC_'..kind..'_INSTITUTION_'..level,
   text='LOC_SPC_'..kind..'_INSTITUTION_'..level..'_HELP',localized=true}
 end
end
function M.GetRows(v)
 local out={};if not v then return out end
 for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do
  local current=kind==v.specialization
  local established=math.max((v.institutionArchive or {})[kind] or 0,current and v.potential or 0)
  for _,entry in ipairs(M.BySpecialization[kind] or {})do
   if current or entry.level<=established then
    local row={};for k,x in pairs(entry)do row[k]=x end
    row.historical=not current;row.established=entry.level<=established;row.kind=kind
    row.icon='ICON_SPC_INSTITUTION_'..kind..'_'..entry.level;out[#out+1]=row
   end
  end
 end
 return out
end
function M.Signature(v)
 local parts={tostring(v.specialization),tostring(v.potential),tostring(v.active),tostring(v.activeStatus),tostring(v.progression)}
 for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do parts[#parts+1]=tostring(v.institutionArchive and v.institutionArchive[kind] or '')end
 local s=v.institutionSummary or {}
 for _,k in ipairs({'known','dialogue','engineering','insights','templatesKnown','buildingTemplates','districtTemplates'})do parts[#parts+1]=tostring(s[k])end
 for _,k in ipairs({'tradition','reputation'})do
  local t=s[k];parts[#parts+1]=tostring(type(t))
  for _,field in ipairs({'age','state','cursor','percent','nextAge'})do parts[#parts+1]=tostring(type(t)=='table' and t[field] or nil)end
 end
 return table.concat(parts,':')
end
function M.Label(entry,key)
 local value=entry[key]
 return entry.localized and Locale.Lookup(value) or value
end
function M.Matches(v,pid,cid,x,y)
 return type(v)=='table' and not v.error and v.owner==pid and v.cityID==cid and v.x==x and v.y==y
  and (M.BySpecialization[v.specialization]~=nil or type(v.institutionArchive)=='table') and type(v.potential)=='number' and v.potential>=0 and v.potential<=4
end
function M.Filter(data,owned)
 -- Copy only display tables we change; never edit CitySupport's shared data.
 local out={};for k,v in pairs(data) do out[k]=v end
 out.BuildingsAndDistricts={}
 for _,d in ipairs(data.BuildingsAndDistricts or {}) do
  local nd={};for k,v in pairs(d) do nd[k]=v end;nd.Buildings={}
  for _,b in ipairs(d.Buildings or {}) do if not owned[b.Type] then nd.Buildings[#nd.Buildings+1]=b end end
  out.BuildingsAndDistricts[#out.BuildingsAndDistricts+1]=nd
 end
 return out
end
local function loc(key,...)return Locale.Lookup('LOC_SPC_INST_'..key,...)end
local function metric(entry,v)
 local s=v.institutionSummary
 local available=s and s.known==true
 local results={}
 local function add(ability,value)results[#results+1]={title=loc(ability),text=value or loc('PENDING')}end
 if entry.kind=='RESEARCH' and entry.level==4 then
  local t=available and s.tradition
  local value
  if available and t==false then value=loc('NOT_STARTED')
  elseif type(t)=='table' and t.percent then
   value=loc('TRADITION_VALUE',t.age,t.percent)
   if t.nextAge then value=value..loc('TRADITION_NEXT',t.nextAge-t.age)end
   if t.state~='COUNTING' then value=value..loc('ACCUMULATION_PAUSED')end
  end
  add('TRADITION',value)
 elseif entry.kind=='COMMERCE' and entry.level==4 then
  local t=available and s.reputation;local value
  if available and t==false then value=loc('NOT_STARTED')
  elseif type(t)=='table' then
   value=loc('REPUTATION_VALUE',t.age,t.age/2)
   if t.state~='COUNTING'then value=value..loc('ACCUMULATION_PAUSED')end
  end
  add('REPUTATION',value)
 elseif entry.kind=='CULTURE' then
  if entry.level==3 then add('DIALOGUE',available and loc('DIALOGUE_VALUE',s.dialogue))
  elseif entry.level==4 then add('EXPEDITION',available and loc('INSIGHTS_VALUE',s.insights))end
 elseif entry.kind=='INDUSTRY' then
  if entry.level==3 then
   local value
   if available and s.templatesKnown then
    value=loc('TEMPLATES_VALUE',s.buildingTemplates,s.districtTemplates~=nil and tostring(s.districtTemplates) or loc('PENDING_SHORT'))
    if v.activeStatus=='KNOWN' and type(v.active)=='number' then
     if entry.historical or v.active<3 then value=value..'[NEWLINE]'..loc('STANDARDIZATION_PAUSED')
     else local boost=v.active>=4 and 2*s.engineering or 0
      value=value..'[NEWLINE]'..loc('STANDARDIZATION_VALUE',10+boost,boost)
     end
    else value=value..'[NEWLINE]'..loc('PENDING')end
   end
   add('STANDARDIZATION',value)
  elseif entry.level==4 then add('ENGINEERING',available and loc('ENGINEERING_VALUE',s.engineering,2*s.engineering))end
 end
 return results
end
local function help(entry,v)
 local text=M.Label(entry,'text')
 for _,m in ipairs(metric(entry,v))do
  local needle=m.title..'[NEWLINE]';local first=text:find(needle,1,true)
  local extra='[NEWLINE][COLOR_CYAN]'..m.text..'[ENDCOLOR]'
  if first then
   local finish=text:find('[NEWLINE][NEWLINE]',first+#needle,true) or #text+1
   text=text:sub(1,finish-1)..extra..text:sub(finish)
  else text=text..'[NEWLINE][NEWLINE]'..m.title..extra end
 end
 return text
end
function M.Tooltip(index,v)
 local entry=M.GetRows(v)[index];if not entry then return '' end
 local state=loc('ACTIVE_PENDING')
 if entry.historical then state=loc('LEGACY_HELP')
 elseif not entry.established then state=loc('PREVIEW_HELP',entry.level)
 elseif type(v.active)=='number' and v.activeStatus~='UNKNOWN' then
  state=v.active>=entry.level and loc('ACTIVE_HELP') or loc('INACTIVE_HELP')
 end
 return M.Label(entry,'name')..'[NEWLINE]'..state..'[NEWLINE][NEWLINE]'..help(entry,v)
end
