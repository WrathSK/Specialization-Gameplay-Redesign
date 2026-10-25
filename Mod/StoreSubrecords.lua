-- Fixed validation ownership, with exactly the existing two Store phases.
-- No native discovery, hooks, writes, automatic repair or per-city registry.
-- CHECK_FAILED is a validation observation, never proof of permanent corruption.
SPCStoreSubrecords={}
local S=SPCStoreSubrecords
local definitions={
 {key='templateLifecycle',phase='PROFESSION',fields={'templateLifecycle'},validate=function(r,same)
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
 {key='dialogue',phase='PROFESSION',fields={'dialogueKnown','dialogue'},validate=function(r,same)
  if r.dialogueKnown~=nil or r.dialogue~=nil then
   assert(r.dialogueKnown==true and type(r.dialogue)=='table','DIALOGUE_HISTORY_UNAVAILABLE')
   SPCDialogueProjectModel.Validate(r.dialogue,r)
  end
 end},
 {key='engineering',phase='PROFESSION',fields={'engineeringKnown','engineering'},validate=function(r,same)
  if r.engineeringKnown~=nil or r.engineering~=nil then
   assert(r.engineeringKnown==true and type(r.engineering)=='table','EST_HISTORY_UNAVAILABLE')
   SPCEngineeringStudyModel.Validate(r.engineering,r)
  end
 end},
 {key='commerce',phase='PROFESSION',fields={'commerceKnown','commerce'},validate=function(r,same)
  if r.commerceKnown~=nil or r.commerce~=nil then
   assert(r.commerceKnown==true and type(r.commerce)=='table','COMMERCE_HISTORY_UNAVAILABLE')
   SPCCommerceModel.Validate(r.commerce,r)
  end
 end},
 {key='capital',phase='PROFESSION',fields={'capitalKnown','capital'},validate=function(r,same)
  if r.capitalKnown~=nil or r.capital~=nil then
   assert(r.capitalKnown==true and type(r.capital)=='table','CAPITAL_HISTORY_UNAVAILABLE')
   local capital=SPCCapitalInvestmentModel.Decode(r.capital)
   for _,c in pairs(capital.contracts)do
    assert(c.source.token==r.base.token and c.source.owner==r.origin.owner
     and c.source.x==r.origin.x and c.source.y==r.origin.y,'CAPITAL_SOURCE_REFERENCE_INVALID')
   end
  end
 end},
 {key='development',phase='PROFESSION',fields={'developmentKnown','development'},validate=function(r,same)
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
function S.Check(r,same)
 local out={}
 for _,d in ipairs(definitions)do
  local ok,why=pcall(d.validate,r,same);local text
  if not ok then local safe,value=pcall(tostring,why);text=safe and value:sub(1,180)or'SUBRECORD_VALIDATION_UNKNOWN'end
  out[#out+1]={key=d.key,fields=fields(d),status=ok and 'PASS'or'CHECK_FAILED',reason=text}
 end
 return out
end
