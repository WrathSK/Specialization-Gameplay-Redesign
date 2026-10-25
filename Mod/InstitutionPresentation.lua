-- Shared institution display model. No gameplay calls or mutations.
SPCInstitutionPresentation={}
local M=SPCInstitutionPresentation
-- Keep row lists extensible: one level may contain multiple sibling institutions.
M.Rows={}
M.BySpecialization={RESEARCH=M.Rows,CULTURE={},INDUSTRY={},COMMERCE={}}
for level=1,4 do
 for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do
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
 for _,k in ipairs({'known','dialogue','engineering','insights','insightsKnown','templatesKnown','buildingTemplates','districtTemplates'})do parts[#parts+1]=tostring(s[k])end
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
   if t.nextAge then value=value..'[NEWLINE]'..loc('TRADITION_NEXT',t.nextAge-t.age)end
   if t.state~='COUNTING' then value=value..'[NEWLINE]'..loc('ACCUMULATION_PAUSED')end
  end
  add('TRADITION',value)
 elseif entry.kind=='COMMERCE' and entry.level==4 then
  local t=available and s.reputation;local value
  if available and t==false then value=loc('NOT_STARTED')
  elseif type(t)=='table' then
   value=loc('REPUTATION_VALUE',t.age,t.age/2)
   if t.state~='COUNTING'then value=value..'[NEWLINE]'..loc('ACCUMULATION_PAUSED')end
  end
  add('REPUTATION',value)
 elseif entry.kind=='CULTURE' then
  if entry.level==3 then add('DIALOGUE',available and loc('DIALOGUE_VALUE',s.dialogue))
  elseif entry.level==4 then add('EXPEDITION',available and s.insightsKnown~=false and loc('INSIGHTS_VALUE',s.insights))end
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
local metricColors={RESEARCH='ResScienceLabelCS',CULTURE='ResCultureLabelCS',COMMERCE='ResGoldLabelCS',INDUSTRY='ResProductionLabelCS'}
local function help(entry,v)
 local text=M.Label(entry,'text')
 for _,m in ipairs(metric(entry,v))do
  local needle=m.title..'：[NEWLINE]';local first=text:find(needle,1,true)
  local extra='[NEWLINE][COLOR:'..metricColors[entry.kind]..']'..m.text..'[ENDCOLOR]'
  if first then
   local finish=text:find('[NEWLINE][NEWLINE]',first+#needle,true) or #text+1
   text=text:sub(1,finish-1)..extra..text:sub(finish)
  else text=text..'[NEWLINE][NEWLINE]'..m.title..'：'..extra end
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
 local level=({'一','二','三','四'})[entry.level] or tostring(entry.level)
 local kind=loc(entry.kind)
 return M.Label(entry,'name')..'[NEWLINE]'..loc('CATEGORY',kind,level)
  ..'[NEWLINE][NEWLINE]'..help(entry,v)
  ..'[NEWLINE][NEWLINE]'..loc('REQUIREMENT',kind,level)..'[NEWLINE]'..loc('STATE',state)
end
