include('Probe')
local P=SPCP0
local token,elapsed,selection
local precisionVisible=false
local function selected()
 local pid=Game.GetLocalPlayer()
 if not P.IsTestPlayer(pid) then return nil end
 local u=UI.GetHeadSelectedUnit()
 if not u or u:GetOwner()~=pid then return nil end
 local r=GameInfo.Units[u:GetType()]
 if r and (r.UnitType=='UNIT_SETTLER' or r.UnitType=='UNIT_BUILDER' or P.CrewBase(r.UnitType)~=nil) then return u end
end
local function refresh()
 local u=selected();Controls.ReadButton:SetHide(true)
 local now=u and (u:GetID()..':'..u:GetX()..':'..u:GetY()) or nil
 if now~=selection then
  selection=now;if not token then Controls.Window:SetHide(true) end
 end
end
local function read(action)
 precisionVisible=false;refresh()
 action=action or 'UNIT_SITE_READ'
 local u=selected();local city=UI.GetHeadSelectedCity()
 if (action=='UNIT_ACTION_SPAWN' and not city) or (action~='UNIT_ACTION_SPAWN' and not u) then
  Controls.Window:SetHide(false);Controls.Report:SetText('Spawn: select own city with empty center. Action: select Settler or Crew.');return
 end
 ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
 token=P.VERSION..':SITE:'..Game.GetCurrentGameTurn()..':'..ExposedMembers.SPC_P0_UISequence
 elapsed=0;Controls.Window:SetHide(false);Controls.Report:SetText('Processing '..action..'...')
 local ok,err=pcall(UI.RequestPlayerOperation,Game.GetLocalPlayer(),PlayerOperations.EXECUTE_SCRIPT,
  {OnStart='SPC_P0_Request',Action=action,UnitID=u and u:GetID(),CityID=city and city:GetID(),Token=token,PlanToken=ExposedMembers.SPC_P0 and ExposedMembers.SPC_P0.UnitActionPreview and ExposedMembers.SPC_P0.UnitActionPreview.token})
 if not ok then token=nil;Controls.Report:SetText('Dispatch error: '..tostring(err)) end
end
local function precision()
 refresh();precisionVisible=true;token=nil;Controls.Window:SetHide(false)
 local ok,text=pcall(function()
  local pid=Game.GetLocalPlayer();assert(P.IsTestPlayer(pid),'请选择测试文明')
  local sample=(ExposedMembers.SPC_P0 or {}).CrewPrecision
  local city=UI.GetHeadSelectedCity()
  if not city and sample and sample.owner==pid and sample.cityID then city=Players[pid]:GetCities():FindID(sample.cityID) end
  assert(city and city:GetOwner()==pid,'请先选中工业专业城市，再读取精度')
  local speed=GameInfo.GameSpeeds[GameConfiguration.GetGameSpeedType()];local multiplier=speed.CostMultiplier
  local function n(v) return type(v)=='number' and string.format('%.17g',v) or tostring(v) end
  local out={'B046 施工队精度（只读） | 城市：'..Locale.Lookup(city:GetName()),'游戏速度系数：'..n(multiplier)..'%；下列为引擎读取值', '档位：理论成本 / 引擎成本 / 项目当前进度 / 本局生产力'}
  local q=city:GetBuildQueue()
  for i,s in ipairs(P.Specs) do
   local project=GameInfo.Projects['PROJECT_SPC_CREW_'..s.charge];assert(project,'B044项目定义缺失')
   out[#out+1]=i..'：'..n(s.cost*multiplier/100)..' / '..n(q:GetProjectCost(project.Index))..' / '..n(q:GetProjectProgress(project.Index))..' / '..n(P.CrewAmount('UNIT_SPC_CREW_'..s.charge))
  end
  local counts={};for _,u in Players[pid]:GetUnits():Members() do
   local row=GameInfo.Units[u:GetType()];local base=row and P.CrewBase(row.UnitType)
   if base then counts[base]=(counts[base] or 0)+1 end
  end
  local parts={};for i,s in ipairs(P.Specs) do parts[#parts+1]=i..'级='..(counts[s.charge] or 0) end
  out[#out+1]='当前己方施工队数量：'..table.concat(parts,'，')
  if sample and sample.owner==pid then
   out[#out+1]='最近一次确认（回合'..n(sample.turn)..'，城市ID '..n(sample.cityID)..'）：'
   if sample.error then out[#out+1]='施工前读取未知：'..sample.error end
   out[#out+1]='原进度='..n(sample.before)..'；施工后='..n(sample.after)..'；原成本='..n(sample.cost)
   out[#out+1]='预期增加='..n(sample.expected)..'；实际增加='..n(sample.observed)..'；差值='..n(sample.difference)
   out[#out+1]='单位仍存在='..tostring(sample.unitPresent)..'；'..tostring(sample.note or sample.afterReadError or '同一目标可比较')
   if sample.difference then out[#out+1]=math.abs(sample.difference)<0.000001 and '本次读取数值相符；仍请核对实际游戏结果。' or '本次存在数值差异，请回传此报告；尚未采用取整规则。' end
  else out[#out+1]='尚无本次加载后的施工确认记录。' end
  return table.concat(out,'[NEWLINE]')
 end)
 Controls.Report:SetText(ok and text or ('精度读取未完成：'..tostring(text)))
end
local function showRoot()
 ContextPtr:SetHide(not P.IsTestPlayer(Game.GetLocalPlayer()))
end
local function initialize()
 showRoot();refresh()
 Controls.PrecisionButton:RegisterCallback(Mouse.eLClick,precision)
 Controls.ReadButton:RegisterCallback(Mouse.eLClick,function() read() end)
 Controls.SpawnCrewButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_SPAWN') end)
 Controls.PrepareUnitButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_PREPARE') end)
 Controls.ConfirmUnitButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_CONFIRM') end)
 Controls.BuilderTargetsButton:RegisterCallback(Mouse.eLClick,function() LuaEvents.SPC_ToggleBuilderTargets() end)
 Controls.CloseButton:RegisterCallback(Mouse.eLClick,function() token=nil;Controls.Window:SetHide(true) end)
 local timer=0
 ContextPtr:SetUpdate(function(dt)
  timer=timer+dt;if timer<0.2 then return end
  local step=timer;timer=0;refresh()
  if not token and not precisionVisible and ExposedMembers.SPC_UnitPanelStatus then Controls.Report:SetText(tostring(ExposedMembers.SPC_UnitPanelStatus):gsub("\n","[NEWLINE]")) end
  Controls.TargetStatus:SetText(ExposedMembers.SPC_TargetMarkerStatus or "操作已移到单位面板；这里保留诊断与DEV生成。")
  if token then
   elapsed=elapsed+step
   local s=ExposedMembers.SPC_P0 or {}
   if s.Version==P.VERSION and s.LastToken==token then
    local text=tostring(s.Snapshot);Controls.Report:SetText(text:gsub('\n','[NEWLINE]'))
    print('[SPC][B040][UNIT_SITE] '..text);token=nil
   elseif elapsed>=10 then token=nil;Controls.Report:SetText('No response. Send Lua.log; no action was executed.') end
  end
 end)
 print('[SPC][B040][UNIT_SITE_UI_READY] visibility fix 52')
end
ContextPtr:SetInitHandler(initialize)
Events.LoadScreenClose.Add(showRoot)
ContextPtr:SetShutdown(function() ContextPtr:ClearUpdate();Events.LoadScreenClose.Remove(showRoot) end)
