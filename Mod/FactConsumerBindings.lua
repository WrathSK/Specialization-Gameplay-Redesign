-- Explicit committed-history adapters. No discovery, timers, stored native objects or new policies.
SPCFactConsumerBindings={}
function SPCFactConsumerBindings.New(shared)
 local d={};shared.FactBindings=d
 local declarations={
  {name='HistoryStandardization',target='StandardizationEffects',topics={'TEMPLATES','ENGINEERING'},method='SourceChanged'},
  {name='HistoryDialogue',target='DialogueEffects',topics={'DIALOGUE'},method='Audit'},
  {name='HistoryInsightsTourism',target='CultureInsightsTourism',topics={'INSIGHTS'},method='Audit'},
  {name='HistoryCultureNetwork',target='CultureNetwork',topics={'INSIGHTS'},method='SourceChanged'},
  {name='HistoryEngineeringCredit',target='EngineeringStudy',topics={'WONDER_CREDIT'},method='CreditChanged'},
  {name='HistoryTradition',target='ResearchTraditionEffects',topics={'TRADITION'},method='Mark'},
 }
 for _,declaration in ipairs(declarations)do
  local row=declaration
  shared.FactChanges.RegisterConsumer(row.name,function(e)
   local target=shared[row.target];local status=shared.StartStatus and shared.StartStatus[row.target]
   if not target or target.startupError or status and (status.state=='FAILED' or status.state=='SKIPPED_DEPENDENCY')then return end
   local method=target[row.method];if type(method)~='function'then return end
   if row.method=='Audit'then return method({player=e.player,city=e.city})end
   return method(e.player,e.city)
  end,{kinds={'HISTORY'},topics=row.topics})
 end
 return d
end
