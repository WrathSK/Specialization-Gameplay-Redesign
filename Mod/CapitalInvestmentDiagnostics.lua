-- B243 failure-only observations. No native reads, authority, retries or saved state.
SPCCapitalInvestmentDiagnostics={}
local M=SPCCapitalInvestmentDiagnostics
local files={['CapitalInvestment.lua']=true,['CapitalInvestmentModel.lua']=true,
 ['CityProgressionStore.lua']=true,['CurrentSpecializationFacts.lua']=true,['CapitalInvestmentDiagnostics.lua']=true}
local stages={DEBIT_INTENT=true,DEBIT_CALLING=true,ACTIVE=true,CREDIT_INTENT=true,
 CREDIT_CALLING=true,SETTLED=true,TERMINATED=true,HELD=true}
-- Store supplies copied plain tables; Mac GameCore does not guarantee rawget.
local function field(t,k)if type(t)=='table'then return t[k]end end
local function finite(v)return type(v)=='number' and v==v and v>-math.huge and v<math.huge end
function M.Error(err,phase)
 local s=type(err)=='string' and err or ''
 local code
 for _,prefix in ipairs({'CAPITAL_','COMMERCE_','STORE_','PROGRESSION_','EVIDENCE_'})do
  code=s:match('('..prefix..'[A-Z0-9_]+)');if code then break end
 end
 local class=code and 'CONTRACT' or s:find('nil value',1,true) and 'LUA_NIL'
  or s:find('attempt to',1,true) and 'LUA_TYPE' or 'UNKNOWN_ERROR'
 local file,line='UNKNOWN',nil
 for f,l in s:gmatch('([%w_]+%.lua):(%d+):')do if files[f]then file=f;line=tonumber(l)end end
 return {phase=phase,errorCode=code or 'CAPITAL_STATE_UNKNOWN',errorClass=class,errorFile=file,errorLine=line}
end
-- Inspect a fixed schema, never recursively traverse arbitrary saved content.
-- Values of names, requests, tokens, hidden outcomes and failure protection are omitted.
function M.Readback(point,readOK,observed,expected,domain,writeStatus,matches)
 local out={readPoint=point,readStatus=readOK and 'READABLE' or 'READ_ERROR',writeStatus=writeStatus,
  savedMatches=readOK and matches or false,recordType=readOK and type(observed) or 'UNKNOWN'}
 if not readOK then
  local e=M.Error(observed);out.readErrorCode=e.errorCode;out.readErrorClass=e.errorClass;return out
 end
 local actualCapital=field(observed,'capital');local wantedCapital=field(expected,'capital')
 local actual=field(field(actualCapital,'contracts'),domain);local wanted=field(field(wantedCapital,'contracts'),domain)
 out.capitalType=type(actualCapital);out.contractType=type(actual)
 local stage=field(actual,'stage');out.savedPhase=stages[stage] and stage or stage==nil and 'ABSENT' or 'INVALID'
 local function numeric(path,v)
  if finite(v)then return v end
  -- Decode only an allowlisted amount/probability, never emit arbitrary strings.
  local fieldName=path:match('^contract%.([%w]+)$')
  local model=SPCCapitalInvestmentModel
  return model and model.StoredNumber and model.StoredNumber(fieldName,v) or nil
 end
 local function difference(path,a,b,structure)
  if type(a)==type(b) and (structure or a==b)then return false end
  if not out.diffPath then
   out.diffPath=path;out.expectedType=type(b);out.actualType=type(a)
   out.expectedNumber=numeric(path,b);out.actualNumber=numeric(path,a)
  end
  out.diffCount=(out.diffCount or 0)+1;return true
 end
 if difference('record',observed,expected,true)then return out end
 if difference('capital',actualCapital,wantedCapital,true)then return out end
 if type(actualCapital)~='table'then
  for _,k in ipairs({'revision','capitalKnown'})do difference('record.'..k,field(observed,k),field(expected,k))end
  if not out.diffPath then out.diffPath=matches and 'NONE' or 'OTHER_RECORD_OR_UNLISTED'end;return out
 end
 for _,k in ipairs({'version','sequence','numberEncoding'})do difference('capital.'..k,field(actualCapital,k),field(wantedCapital,k))end
 if difference('capital.contracts',field(actualCapital,'contracts'),field(wantedCapital,'contracts'),true)then return out end
 if difference('contract',actual,wanted,true)then return out end
 if type(actual)=='table' and type(wanted)=='table'then
  for _,k in ipairs({'stage','principal','balanceBefore','balanceAfter','safe','success','failure','probability',
   'D','S','C','R','start','due','sequence','attained','creditBefore','creditAfter','paid','settledTurn','mode','domain'})do
   difference('contract.'..k,field(actual,k),field(wanted,k))
  end
  for _,k in ipairs({'source','sSource'})do
   local a,b=field(actual,k),field(wanted,k)
   if not difference('contract.'..k,a,b,true) and type(a)=='table' and type(b)=='table'then
    for _,f in ipairs({'owner','cityID','x','y','changes'})do difference('contract.'..k..'.'..f,field(a,f),field(b,f))end
   end
  end
 end
 for _,k in ipairs({'revision','capitalKnown'})do difference('record.'..k,field(observed,k),field(expected,k))end
 -- NONE is justified only by the Store's full equality check, not this projection.
 if not out.diffPath then out.diffPath=matches and 'NONE' or 'OTHER_RECORD_OR_UNLISTED'end
 return out
end
