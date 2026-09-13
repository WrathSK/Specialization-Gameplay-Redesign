-- B028 read-only city total-yield diagnostic. No Convergence grant or level override.
SPCSourceYieldProbe={}
function SPCSourceYieldProbe.Read(playerID,city,shared)
 local ok,result=pcall(function()
  assert(city:GetOwner()==playerID,'OWNER_CHANGED')
  local id=city:GetID()
  local role='UNKNOWN'
  local good,f=pcall(shared.CityFlowProbe.SupportFacts,playerID,city)
  if good and type(f)=='table' and type(f.specialization)=='string' then role=f.specialization end
  local lines={'B028 SOURCE TOTALS (Game) | city='..id..' specialty='..role,
   'READ ONLY / NO Lv4 activation / NO yields granted'}
  local nameOK,name=pcall(function() return city:GetName() end)
  if nameOK and type(name)=='string' then lines[#lines+1]='name='..name end
  for _,key in ipairs({'SCIENCE','CULTURE','PRODUCTION'}) do
   local index=YieldTypes and YieldTypes[key]
   if index==nil and GameInfo and GameInfo.Yields then
    local row=GameInfo.Yields['YIELD_'..key];index=row and row.Index
   end
   local got,value=pcall(function() assert(index~=nil,'YIELD_ENUM_ABSENT');return city:GetYield(index) end)
   if got and type(value)=='number' and value==value and math.abs(value)<math.huge then
    lines[#lines+1]=key..' total='..string.format('%.6f',value)
   else
    local err=tostring(value):match('[^\r\n]+') or 'INVALID_VALUE'
    lines[#lines+1]=key..' UNKNOWN: '..err:sub(1,100)
   end
  end
  lines[#lines+1]='Includes outside inputs; NOT verified local-only basis.'
  return table.concat(lines,'\n')
 end)
 return ok and result or ('B028 SOURCE UNKNOWN: '..tostring(result):sub(1,180))
end
