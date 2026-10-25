-- One attempt and one postread only. Callers own CAS, schema and acceptance.
SPCPropertyCell={}
function SPCPropertyCell.WriteReadback(writeOnce,readOnce)
 local returned,result=pcall(writeOnce)
 local readReturned,observed,readReason=pcall(readOnce)
 return {writeReturned=returned,writeResult=result,readReturned=readReturned,
  observed=observed,readReason=readReason}
end
