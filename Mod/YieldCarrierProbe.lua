-- Isolated fixed-amount experiment, not network settlement. Plot flags persist until OFF.
SPCYieldCarrierProbe={}
local baseline={}
local function plotFor(pid,c)
 assert(c:GetOwner()==pid,'OWNER_CHANGED')
 local p=Map.GetPlot(c:GetX(),c:GetY());assert(p and p:GetOwner()==pid,'PLOT_OWNER_CHANGED');return p
end
local function read(c)
 local values={}
 for _,y in ipairs({'SCIENCE','CULTURE','PRODUCTION'}) do
  local v=c:GetYield(YieldTypes[y]);assert(type(v)=='number' and v==v and math.abs(v)<math.huge,'INVALID_YIELD');values[y]=v
 end
 return values
end
local function flags(p) return p:GetProperty('SPC_B029_ONE')==1,p:GetProperty('SPC_B029_HALF')==1 end
function SPCYieldCarrierProbe.Run(pid,c,action)
 local ok,out=pcall(function()
  local p=plotFor(pid,c);local one,half=flags(p)
  if action=='OFF' then
   -- OFF always available, even if the SQL definitions are missing in this save.
   p:SetProperty('SPC_B029_ONE',0);p:SetProperty('SPC_B029_HALF',0)
  elseif action=='STEP' then
   for _,bit in ipairs({'ONE','HALF'}) do for _,y in ipairs({'SCIENCE','CULTURE','PRODUCTION'}) do
    assert(GameInfo.Modifiers['SPC_B029_'..bit..'_'..y],'DEFINITIONS_ABSENT_RELOAD_OR_NEW_TEST_GAME')
   end end
   if not one and not half then baseline[pid..':'..c:GetID()]=read(c) end
   p:SetProperty('SPC_B029_ONE',1)
   p:SetProperty('SPC_B029_HALF',one and 1 or 0)
  else assert(action=='READ','ACTION') end
  return SPCYieldCarrierProbe.Describe(pid,c)
 end)
 return ok and out or ('B030 CARRIER UNKNOWN: '..tostring(out):sub(1,200))
end
function SPCYieldCarrierProbe.Describe(pid,c)
 local ok,out=pcall(function()
  local p=plotFor(pid,c);local one,half=flags(p);local configured=(one and 1 or 0)+(half and 1.5 or 0)
  local current=read(c);local base=baseline[pid..':'..c:GetID()]
  local lines={'B030 PRECISION CONTROL | city='..c:GetID()..' configured='..configured..' each S/C/P',
   'Test only: ONE=1, second slot=1.5. New B030 game required.',
   'Read source totals: combined delta 2.5 / 2 / 1 distinguishes outcomes.'}
  for _,y in ipairs({'SCIENCE','CULTURE','PRODUCTION'}) do
   lines[#lines+1]=y..' total='..string.format('%.6f',current[y])..' delta='..(base and string.format('%.6f',current[y]-base[y]) or 'NO_BASELINE_THIS_LOAD')
  end
  lines[#lines+1]='OFF required after test. Modifiers may amplify base amounts.'
  return table.concat(lines,'\n')
 end)
 return ok and out or ('B030 CARRIER UNKNOWN: '..tostring(out):sub(1,200))
end
