-- Offline contract only: the caller must authorize acquisition; no inferred unlock policy.
local M={}
local function copy(t) if type(t)~='table' then return t end;local o={};for k,v in pairs(t) do o[k]=copy(v) end;return o end
function M.Record(old,cityUID,event,catalog)
 assert(type(cityUID)=='string' and #cityUID>0,'PERMANENT_CITY_UID_REQUIRED')
 assert(event.authorized==true and event.completed==true,'AUTHORIZED_COMPLETION_REQUIRED')
 assert(type(event.evidence)=='string' and #event.evidence>0,'EVIDENCE_REQUIRED')
 local row=assert(catalog.buildings[event.buildingType],'UNCLASSIFIED_BUILDING')
 assert(row.tier>=1 and row.tier%1==0 and not row.internal and not row.wonder,'INELIGIBLE_CATALOG_ENTRY')
 local out=old and copy(old) or {schema=1,cityUID=cityUID,catalogRevision=catalog.revision,revision=0,learned={}}
 assert(out.schema==1 and out.cityUID==cityUID,'LEDGER_IDENTITY_CONFLICT')
 assert(out.catalogRevision==catalog.revision,'CATALOG_MIGRATION_REQUIRED')
 if out.learned[event.buildingType] then return out,false end
 out.learned[event.buildingType]={district=row.district,tier=row.tier,evidence=event.evidence,learnedTurn=event.turn}
 out.revision=out.revision+1;return out,true
end
function M.ForRecipient(player,validSources,ledgers,catalog)
 local out={templates={},templateSources={},discount=0}
 for uid,s in pairs(validSources) do
  assert(s.owner==player and s.kind=='INDUSTRY' and type(s.active)=='number' and s.active%1==0 and s.active>=1 and s.active<=4,'INVALID_CURRENT_SOURCE')
  local ledger=assert(ledgers[uid],'LEDGER_UNKNOWN_NOT_EMPTY')
  assert(ledger.cityUID==uid and ledger.catalogRevision==catalog.revision,'LEDGER_MAPPING_CONFLICT')
  out.discount=math.max(out.discount,s.active*10)
  for building,row in pairs(ledger.learned) do
   local group=row.district..':'..row.tier
   out.templates[group]=true;out.templateSources[group]=out.templateSources[group] or {};out.templateSources[group][uid]=true
  end
 end
 return out
end
function M.Discount(result,building,currency,catalog)
 local row=catalog.buildings[building]
 if currency~='GOLD' or not row or row.internal or row.wonder or row.tier<1 then return 0 end
 return result.templates[row.district..':'..row.tier] and result.discount or 0
end
return M
