"""O2 actual investment refresh owners and their existing transaction boundaries."""
import unittest

from test_refactor_s6f import combined


def composition():
    lua = combined()
    lua.execute("""
fc=shared.FactChanges;bindings=shared.FactBindings
capital=shared.CapitalInvestment;development=shared.DevelopmentInvestment
-- This composition has investment owners, with no Tradition projection.
shared.ResearchTraditionEffects={AcceptFact=function(e)
 return fc.Receipt(e,'IRRELEVANT','FIXTURE_OUTSIDE_SCOPE')
end}
for _,name in ipairs({'ResearchInfrastructure','ResearchSupport','Lv2Housing','Lv2GPP','ResearchApply','ResearchChair',
 'CultureAesthetic','CultureMeaning','CultureInspiration','CultureInsightsTourism','DialogueEffects','ResearchCross','IndustrySupport','StandardizationEffects','CultureNetwork'})do
 shared[name]={AcceptFact=function()return true end}
end
function deliver()
 fc.Flush();bindings.Flush()
end
function cause(kind,topic,city)
 fc.Emit({owner=0,cityID=city,kinds={kind},topic=topic,cause='FIXTURE_COMMITTED'})
end
""")
    return lua


class InvestmentFactResponsibility(unittest.TestCase):
    def test_failed_capital_target_keeps_committed_recovery_and_wakes_once(self):
        lua = composition()
        lua.execute("""
local mark=capital.Mark;local calls=0
capital.Mark=function(...)calls=calls+1;return mark(...)end
shared.StartStatus={CapitalInvestment={state='FAILED'}}
cause('HISTORY','CAPITAL_RECOVERY',source:GetID());deliver()
assert(fc.retained==1 and calls==0 and bindings.errors.CapitalInvestment,'CAPITAL_SCOPE_DROPPED')
local n=fc.delivered
for i=1,50 do deliver()end
assert(fc.retained==1 and fc.delivered==n and moneyCalls==0)
shared.StartStatus.CapitalInvestment.state='OK'
assert(bindings.Wake('CapitalInvestment','OWNER_READY',fc.sequence,{player=0,city=source:GetID()}))
deliver();assert(fc.retained==0 and calls==1 and moneyCalls==0 and not bindings.errors.CapitalInvestment)
deliver();assert(calls==1)
""")

    def test_development_failed_registration_does_not_consume_new_network_fact(self):
        lua = composition()
        lua.execute("""
local real=development.Mark;local calls=0
development.Mark=function(pid,id)calls=calls+1;return false end
cause('NETWORK');deliver()
assert(calls==1 and fc.retained==1 and bindings.errors.DevelopmentInvestment,'DEVELOPMENT_SCOPE_DROPPED')
local n=fc.delivered;for i=1,50 do deliver()end;assert(fc.delivered==n and calls==1)
development.Mark=real
assert(bindings.Wake('DevelopmentInvestment','OWNER_READY',fc.sequence,{player=0}))
deliver();assert(fc.retained==0 and moneyCalls==0 and not bindings.errors.DevelopmentInvestment)
""")

    def test_ordinary_history_not_used_as_quote_or_transaction_credential(self):
        lua = composition()
        lua.execute("""
local raw=capital.Mark;local calls=0
capital.Mark=function(...)calls=calls+1;return raw(...)end
cause('HISTORY','ENGINEERING',source:GetID());deliver()
assert(calls==0 and fc.retained==0 and moneyCalls==0)
cause('HISTORY','CAPITAL_RECOVERY',source:GetID());deliver()
assert(calls==1 and fc.retained==0 and moneyCalls==0)
""")
