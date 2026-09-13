-- UI-only native empire rate readout. Never used as gameplay input or a city rate.
SPCGPPReadout={}
function SPCGPPReadout.Render(P,report)
 local classes={RESEARCH={"SCIENTIST"},CULTURE={"WRITER","ARTIST","MUSICIAN"},INDUSTRY={"ENGINEER"},COMMERCE={"MERCHANT"}}
 local kind=report:match("city=%d+ (%u+) ACTIVE=")
 if not classes[kind] then return report end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return report end
 local parts={}
 for _,cl in ipairs(classes[kind]) do
  local ok,value=pcall(function()
   local row=P.Info("GreatPersonClasses","GREAT_PERSON_CLASS_"..cl)
   return Players[pid]:GetGreatPeoplePoints():GetPointsPerTurn(row.Index)
  end)
  parts[#parts+1]=cl..":"..(ok and type(value)=="number" and tostring(value) or "UNKNOWN")
 end
 local line="UI EMPIRE GPP/turn: "..table.concat(parts," | ")
 return (report:gsub("Native EMPIRE GPP/turn:[^\n]*",function() return line end))
end
