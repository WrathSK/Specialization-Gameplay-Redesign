-- Read the same cost API used by the native ProductionPanel. No purchase operation.
SPCPurchaseProbeRead={}
function SPCPurchaseProbeRead.Render(P,c)
 local out={'原生价格读取（不是购买资格判定）：'}
 for _,id in ipairs({'BUILDING_MONUMENT','BUILDING_GRANARY'}) do
  local ok,v=pcall(function()
   local b=P.Info('Buildings',id);local gold=P.Info('Yields','YIELD_GOLD').Index;local faith=P.Info('Yields','YIELD_FAITH').Index
   if P.HasBuilding(c:GetBuildings(),b.Index) then return Locale.Lookup(b.Name)..'：已拥有，换未建此建筑的城市测试。' end
   return Locale.Lookup(b.Name)..' | Gold='..tostring(c:GetGold():GetPurchaseCost(gold,b.Hash))..' | Faith='..tostring(c:GetGold():GetPurchaseCost(faith,b.Hash))
  end)
  out[#out+1]=ok and v or '价格接口不可读，请查看原生购买面板并回传截图。'
 end
 out[#out+1]='请分别打开金币/信仰购买页核对；不要实际购买。'
 return table.concat(out,'\n')
end
