-- Fixed validation ownership, with exactly the existing two Store phases.
-- No native discovery, hooks, writes or per-city registry. Explicit candidates
-- require the Store full-parent validator and exact storage readback before use.
-- CHECK_FAILED is a validation observation, never proof of permanent corruption.
SPCStoreSubrecords={}
local S=SPCStoreSubrecords
local definitions={
 {key='templateLifecycle',phase='PROFESSION',fields={'templateLifecycle','templates','templatesCaptured'},validate=function(r,same)
  -- B140: missing history is not proof of first initialization. The optional
  -- extension adopts only validated existing ledgers; old ambiguous nil stays held.
  if r.templateLifecycle then
   local t=r.templateLifecycle
   assert((r.base.specialization=='INDUSTRY' or r.restructuring and r.restructuring.established.INDUSTRY) and type(t)=='table' and t.version==1
    and (t.state=='UNINITIALIZED' or t.state=='INITIALIZED') and type(t.reconcilePending)=='boolean','TEMPLATES_LIFECYCLE_INVALID')
   assert(t.districtsKnown==nil or (t.districtsKnown==true and r.templates and r.templates.knowledgeVersion==1 and r.templates.districts),'TEMPLATES_DISTRICT_HISTORY_UNAVAILABLE')
   assert(t.state~='UNINITIALIZED' or (r.templates==nil and t.reconcilePending),'TEMPLATES_LIFECYCLE_CONFLICT')
  end
 end},
 {key='researchTradition',phase='PROFESSION',fields={'researchTradition'},validate=function(r,same)
  if r.researchTradition then SPCResearchTradition.Validate(r.researchTradition,r) end
 end},
 {key='dialogue',known='dialogueKnown',phase='PROFESSION',fields={'dialogueKnown','dialogue'},validate=function(r,same)
  if r.dialogueKnown~=nil or r.dialogue~=nil then
   assert(r.dialogueKnown==true and type(r.dialogue)=='table','DIALOGUE_HISTORY_UNAVAILABLE')
   SPCDialogueProjectModel.Validate(r.dialogue,r)
  end
 end},
 {key='engineering',known='engineeringKnown',phase='PROFESSION',fields={'engineeringKnown','engineering'},validate=function(r,same)
  if r.engineeringKnown~=nil or r.engineering~=nil then
   assert(r.engineeringKnown==true and type(r.engineering)=='table','EST_HISTORY_UNAVAILABLE')
   SPCEngineeringStudyModel.Validate(r.engineering,r)
  end
 end},
 {key='commerce',known='commerceKnown',phase='PROFESSION',fields={'commerceKnown','commerce'},validate=function(r,same)
  if r.commerceKnown~=nil or r.commerce~=nil then
   assert(r.commerceKnown==true and type(r.commerce)=='table','COMMERCE_HISTORY_UNAVAILABLE')
   SPCCommerceModel.Validate(r.commerce,r)
  end
 end},
 {key='capital',known='capitalKnown',phase='PROFESSION',fields={'capitalKnown','capital'},validate=function(r,same)
  if r.capitalKnown~=nil or r.capital~=nil then
   assert(r.capitalKnown==true and type(r.capital)=='table','CAPITAL_HISTORY_UNAVAILABLE')
   local capital=SPCCapitalInvestmentModel.Decode(r.capital)
   for _,c in pairs(capital.contracts)do
    assert(c.source.token==r.base.token and c.source.owner==r.origin.owner
     and c.source.x==r.origin.x and c.source.y==r.origin.y,'CAPITAL_SOURCE_REFERENCE_INVALID')
   end
  end
 end},
 {key='development',known='developmentKnown',phase='PROFESSION',fields={'developmentKnown','development'},validate=function(r,same)
  if r.developmentKnown~=nil or r.development~=nil then
   assert(r.developmentKnown==true and type(r.development)=='table','DEVELOPMENT_HISTORY_UNAVAILABLE')
   local value=SPCDevelopmentInvestmentModel.Decode(r.development)
   for _,c in pairs(value.contracts)do
    assert(c.source.token==r.base.token and c.source.owner==r.origin.owner
     and c.source.x==r.origin.x and c.source.y==r.origin.y,'DEVELOPMENT_SOURCE_REFERENCE_INVALID')
   end
  end
 end},
 {key='expeditionInsights',phase='EPISODES',fields={'expeditionInsights'},validate=function(r,same)
  -- B212: city-owned Expedition Insight history (Design: source city x foreign civ x
  -- category, first success only). History follows the city; never deleted here.
  if r.expeditionInsights~=nil then
   local e=r.expeditionInsights
   assert(type(e)=='table' and e.version==1 and type(e.records)=='table','EXPEDITION_INSIGHTS_INVALID')
   local n=0
   for k,v in pairs(e.records)do
    local civ,cat=tostring(k):match('^(CIVILIZATION_[A-Z0-9_]+):([A-Z]+)$')
    assert(civ and (cat=='PEOPLE' or cat=='WORKS' or cat=='PLACES') and type(v)=='table' and v.civ==civ and v.category==cat
     and type(v.turn)=='number' and v.turn>=0 and v.turn%1==0,'EXPEDITION_INSIGHT_RECORD_INVALID')
    n=n+1
   end
   assert(n<=3*64,'EXPEDITION_INSIGHTS_BOUND')
  end
 end},
 {key='claimTimer',phase='EPISODES',fields={'claimTimer'},validate=function(r,same)
  if r.claimTimer then
   local t=r.claimTimer
   local restored=r.restructuring and r.restructuring.phase=='UNASSIGNED' and next(r.restructuring.candidates)~=nil
   local candidates=restored and r.restructuring.candidates or r.acquisition and r.acquisition.legacySet
   assert((restored or r.schema==3 and r.acquisition.mode=='LEGACY_CLAIM' and r.progression=='UNASSIGNED')
    and t.version==1 and t.token==r.base.token and same(t.reference,r.current or r.origin)
    and candidates[t.kind] and t.project=='PROJECT_SPC_CLAIM_'..t.kind
    and type(t.start)=='number' and t.start%1==0 and t.start>=(restored and r.restructuring.recaptureTurn or r.acquisition.turn)
    and type(t.deactivated)=='boolean' and (t.stage=='ACTIVE' or t.stage=='CALLING' or t.stage=='STOPPED')
    and type(t.reason)=='string','CLAIM_TIMER_INVALID')
  end
 end},
}
local byKey={};for _,d in ipairs(definitions)do assert(not byKey[d.key],'SUBRECORD_DUPLICATE');byKey[d.key]=d end
local function fields(d)local out={};for i,key in ipairs(d.fields)do out[i]=key end;return out end
function S.Keys()
 local out={};for i,d in ipairs(definitions)do out[i]=d.key end;return out
end
function S.Fields(key)return fields(assert(byKey[key],'SUBRECORD_UNKNOWN'))end
function S.Validate(r,phase,same)
 assert(phase=='PROFESSION'or phase=='EPISODES','SUBRECORD_PHASE_UNKNOWN')
 for _,d in ipairs(definitions)do if d.phase==phase then d.validate(r,same)end end
end
-- Explicit inspection only. Independent failures can be reported without
-- mutating the record or classifying a transient exception as irrecoverable.
function S.CheckOne(key,r,same)
 local d=assert(byKey[key],'SUBRECORD_UNKNOWN')
 local ok,why=pcall(function()
  d.validate(r,same)
  -- Only failed-restore inspection needs this extra shape/provenance check.
  -- Healthy full validation retains M.Preview's original order and workload.
  if key=='templateLifecycle'and r.templates~=nil then
   SPCCityIdentityRead.ValidateTemplates(r.templates,r.base.token,r.origin.x,r.origin.y)
  end
 end);local text
 if not ok then local safe,value=pcall(tostring,why);text=safe and type(value)=='string'and value:sub(1,180)or'SUBRECORD_VALIDATION_UNKNOWN'end
 return {key=d.key,fields=fields(d),status=ok and 'PASS'or'CHECK_FAILED',reason=text}
end
function S.Check(r,same)
 local out={};for _,d in ipairs(definitions)do out[#out+1]=S.CheckOne(d.key,r,same)end;return out
end

-- Redundant known flags have no false-valued producer. Complete preserved
-- payloads may prove them true; no payload, amount, serial or receipt is reset.
local knownFailures={DIALOGUE_HISTORY_UNAVAILABLE=true,EST_HISTORY_UNAVAILABLE=true,
 COMMERCE_HISTORY_UNAVAILABLE=true,CAPITAL_HISTORY_UNAVAILABLE=true,DEVELOPMENT_HISTORY_UNAVAILABLE=true}
function S.IsKnownFlagFailure(why)
 local code=type(why)=='string'and why:match('([A-Z][A-Z_]+)$')
 return code and knownFailures[code]==true or false
end
function S.KnownCandidate(r,copy)
 local candidate,changes
 for _,d in ipairs(definitions)do if d.known and r[d.key]~=nil and r[d.known]~=true then
  candidate=candidate or copy(r);changes=changes or {}
  changes[#changes+1]={key=d.key,field=d.known,previousType=type(r[d.known])}
  candidate[d.known]=true
 end end
 return candidate,changes -- never a confirmed value or permanent-fault verdict
end

-- Redundant template metadata may be rebuilt only from a complete current saved
-- ledger, never from present buildings, catalogue classification or an exception.
local function brokenTemplateMetadata(t)
 return type(t)~='table'or t.version~=1 or t.state~='INITIALIZED'or type(t.reconcilePending)~='boolean'
  or t.districtsKnown~=nil and t.districtsKnown~=true
end
function S.NeedsTemplateMetadata(r)
 if type(r)~='table'or type(r.templates)~='table'then return false end
 local t=r.templateLifecycle
 if type(t)=='table'and t.version~=nil and t.version~=1 then return false end -- unknown explicit version
 return r.templatesCaptured~=true or brokenTemplateMetadata(t)
end
function S.TemplateMetadataCandidate(r,copy)
 if not S.NeedsTemplateMetadata(r)then return end
 local ok,candidate,fields=pcall(function()
  local n=copy(r) -- complete bounded input, including unknown extensions
  assert(n.base.specialization=='INDUSTRY'or n.restructuring and n.restructuring.established.INDUSTRY,'TEMPLATES_INDUSTRY_PROOF_REQUIRED')
  local v=n.templates
  assert(v.knowledgeVersion==1 and type(v.districts)=='table','TEMPLATES_COMPLETE_HISTORY_REQUIRED')
  SPCCityIdentityRead.ValidateTemplates(v,n.base.token,n.origin.x,n.origin.y)
  local old=n.templateLifecycle;local changes={}
  if n.templatesCaptured~=true then
   changes[#changes+1]={key='templateLifecycle',field='templatesCaptured',previousType=type(n.templatesCaptured),basis='COMPLETE_SAVED_LEDGER'}
   n.templatesCaptured=true
  end
  if brokenTemplateMetadata(old)then
   local t=type(old)=='table'and copy(old)or {}
   t.version=1;t.state='INITIALIZED';t.reconcilePending=true;t.districtsKnown=true;n.templateLifecycle=t
   changes[#changes+1]={key='templateLifecycle',field='templateLifecycle',previousType=type(old),basis='COMPLETE_SAVED_LEDGER',
    previousState=type(old)=='table'and type(old.state)=='string'and old.state:sub(1,80)or nil}
  end
  return n,changes
 end)
 if ok then return candidate,fields end -- failure/UNKNOWN is no reconstruction proof
end
