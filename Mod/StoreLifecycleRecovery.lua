-- Fixed pure business delegates for approved deferred Store lifecycle work.
-- The caller owns parent validation, exact witness/CAS, catalogue availability,
-- applying returned fields and committing/clearing evidence. No native work here.
-- The Store includes every model used below before it loads this module.
SPCStoreLifecycleRecovery={}
local M=SPCStoreLifecycleRecovery
local function integer(n)return type(n)=='number'and n==n and n>=0 and n<9007199254740991 and n%1==0 end
function M.Plan(r,key,witness,turn)
 local D=SPCStoreDeferredLifecycle
 assert(integer(turn),'DEFERRED_RECOVERY_TURN_UNKNOWN')
 local nextEvidence=D.Clear(r.deferredLifecycle,key,witness,r) -- exact parent/owner/token/episode/scope
 assert(turn>=(witness.returnTurn or witness.lossTurn or witness.firstTurn),'DEFERRED_RECOVERY_TURN_REVERSED')
 local cp=SPCCityIdentityRead.Copy
 local identity
 if key=='researchTradition'or key=='commerce'or key=='templateLifecycle'then
  identity=assert(SPCRestructuringModel.Current(r).specialization,'DEFERRED_IDENTITY_UNKNOWN')
 end
 local returned=r.stage=='ACTIVE';local out={key=key,witness=cp(witness),set={},remove={},nextEvidence=nextEvidence}
 if key=='researchTradition'then
  local R=SPCResearchTradition;R.Validate(r.researchTradition,r)
  if returned then out.set.researchTradition=R.ResumeOwner(r.researchTradition,turn,identity)
  else local value=cp(r.researchTradition);value.state='OWNER_POLICY_UNRESOLVED';out.set.researchTradition=value end
  out.topic='TRADITION'
 elseif key=='dialogue'then
  local R=SPCDialogueProjectModel;assert(r.dialogue~=nil,'DEFERRED_PAYLOAD_UNAVAILABLE');R.Validate(r.dialogue)
  out.set.dialogue=R.Cancel(r.dialogue,'易主取消未完成对话；已成功历史保留');out.set.dialogueKnown=true;out.topic='DIALOGUE'
 elseif key=='engineering'then
  local R=SPCEngineeringStudyModel;assert(r.engineering~=nil,'DEFERRED_PAYLOAD_UNAVAILABLE');R.Validate(r.engineering)
  out.set.engineering=R.Cancel(r.engineering,'EST_OWNER_CHANGED');out.set.engineeringKnown=true;out.topic='ENGINEERING'
 elseif key=='capital'or key=='development'then
  local R=key=='capital'and SPCCapitalInvestmentModel or SPCDevelopmentInvestmentModel
  local value=R.Decode(r[key]);assert(value~=nil,'DEFERRED_PAYLOAD_UNAVAILABLE')
  out.set[key]=R.Encode(R.Terminate(value,key=='capital'and 'CAPITAL_OWNER_CHANGED'or'DEVELOPMENT_OWNER_CHANGED'))
  out.set[key..'Known']=true;out.topic=key=='capital'and 'CAPITAL_RECOVERY'or 'DEVELOPMENT_RECOVERY'
 elseif key=='commerce'then
  local R=SPCCommerceModel;assert(type(r.commerce)=='table','DEFERRED_PAYLOAD_UNAVAILABLE');R.Validate(r.commerce)
  local value
  if identity~='COMMERCE'then
   value=R.Exit(r.commerce)
   if returned then value=R.Resume(value,r.origin.owner,turn)
   else value=R.OwnerChanged(value,witness.lossTarget.owner,assert(witness.lossTurn,'DEFERRED_LOSS_TURN_UNKNOWN'))end
  elseif returned then value=R.Resume(r.commerce,r.origin.owner,turn)
  else value=R.OwnerChanged(r.commerce,witness.lossTarget.owner,assert(witness.lossTurn,'DEFERRED_LOSS_TURN_UNKNOWN'))end
  if witness.scope=='REPUTATION'then
   local previous=cp(r.commerce);previous.reputation=cp(value.reputation);value=previous
  end
  R.Validate(value,r);out.set.commerce=value;out.set.commerceKnown=true;out.topic='COMMERCE'
 elseif key=='claimTimer'then
  -- Original confirmed-loss policy clears this transient timer without reading it.
  -- It never creates a Claim receipt or calls FinishProgress.
  out.remove.claimTimer=true
 elseif key=='templateLifecycle'then
  local S=SPCStoreSubrecords
  assert(S.CheckOne(key,r,function(a,b)return SPCCapitalInvestmentModel.Same(a,b)end).status=='PASS','DEFERRED_TEMPLATE_HISTORY_UNAVAILABLE')
  if returned and identity=='INDUSTRY'then
   if r.templateLifecycle then local value=cp(r.templateLifecycle);value.reconcilePending=true;out.set.templateLifecycle=value end
   out.requiresTemplateValidation=r.templatesCaptured==true and r.templates~=nil or false
  end
  out.topic='TEMPLATES'
 elseif key=='expeditionInsights'then
  local S=SPCStoreSubrecords
  assert(S.CheckOne(key,r,function(a,b)return SPCCapitalInvestmentModel.Same(a,b)end).status=='PASS','DEFERRED_INSIGHTS_UNAVAILABLE')
  out.topic='INSIGHTS' -- city-owned permanent history itself has no owner mutation
 else error('DEFERRED_OWNER_UNKNOWN')end
 return out
end
