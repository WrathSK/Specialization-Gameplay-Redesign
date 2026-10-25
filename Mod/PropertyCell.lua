-- One attempt and one postread only. Callers own CAS, schema and acceptance.
SPCPropertyCell={}
function SPCPropertyCell.WriteReadback(writeOnce,readOnce)
 local returned,result=pcall(writeOnce)
 local readReturned,observed,readReason=pcall(readOnce)
 return {writeReturned=returned,writeResult=result,readReturned=readReturned,
  observed=observed,readReason=readReason}
end

-- Scoped storage-number mechanics, not a native numeric quantization rule.
function SPCPropertyCell.NonnegativeFinite(n)
 return type(n)=='number'and n==n and n>=0 and n<math.huge
end
function SPCPropertyCell.CanonicalDecimal17(text)
 if type(text)~='string'or #text>32 then return nil end
 local n=tonumber(text)
 if SPCPropertyCell.NonnegativeFinite(n)and string.format('%.17g',n)==text then return n end
 return nil
end
