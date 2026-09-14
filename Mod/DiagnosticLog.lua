-- B068 UI-only repetition filter. First full message + repeat counters retained.
SPCDiagnosticLog=SPCDiagnosticLog or {}
function SPCDiagnosticLog.For(scope)
 local emit=print
 ExposedMembers.SPC_UILog=ExposedMembers.SPC_UILog or {}
 local store={rows={},order={},dropped=0};ExposedMembers.SPC_UILog[scope]=store
 return function(message)
  local text=tostring(message);local row=store.rows[text]
  if row then row.count=row.count+1;row.lastTurn=Game.GetCurrentGameTurn();return end
  if #store.order>=128 then local old=table.remove(store.order,1);store.rows[old]=nil;store.dropped=store.dropped+1 end
  store.order[#store.order+1]=text
  store.rows[text]={count=1,firstTurn=Game.GetCurrentGameTurn(),lastTurn=Game.GetCurrentGameTurn()}
  emit(text)
 end
end
