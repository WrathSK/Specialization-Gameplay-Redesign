-- Pure reliable-boundary arithmetic. Callers validate ordered turns and policy.
SPCTurnLedger={}
function SPCTurnLedger.Advance(cursor,turn,counting,unknown)
 local delta=turn-cursor
 if unknown or delta>1 then return turn,0,true end
 return turn,counting and delta or 0,false
end
