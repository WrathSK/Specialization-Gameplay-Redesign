SPCReadFailure={}
local M=SPCReadFailure
-- B231: allowlisted failure metadata only; never retain a path or raw error here.
function M.Classify(value,phase)
 local s=type(value)=='string' and value or ''
 local code=s:match('(CN_[A-Z0-9_]+)') or s:match('(NETWORK_[A-Z0-9_]+)')
  or s:match('(PROGRESSION_[A-Z0-9_]+)') or s:match('(EFFECTIVE_[A-Z0-9_]+)')
  or s:match('(PRESENTATION_[A-Z0-9_]+)')
 local class=code and 'CONTRACT' or s:find('nil value',1,true) and 'LUA_NIL'
  or s:find('attempt to',1,true) and 'LUA_TYPE' or 'READ_ERROR'
 local file,line=s:match('([%w_]+%.lua):(%d+):')
 local allowed={CultureNetwork=true,NetworkBridge=true,NetworkInput=true,CurrentSpecializationFacts=true,
  CityProgressionStore=true,EffectiveFacts=true,CityFlowProbe=true,BindingProbe=true,PropertyCell=true,StoreSubrecords=true,Gameplay=true,CityPotential=true}
 if not file or not allowed[file:gsub('%.lua$','')]then file='UNKNOWN'end
 line=tonumber(line or s:match(':(%d+):'))
 local symbol=s:match("attempt to call %w+ '([%w_]+)' %(a nil value%)")
 local symbols={rawget=true,rawset=true,rawequal=true,getmetatable=true,setmetatable=true,unpack=true,select=true}
 if not symbols[symbol]then symbol=nil end
 return {phase=phase,errorCode=code or class,errorClass=class,errorFile=file,errorLine=line,errorSymbol=symbol}
end
