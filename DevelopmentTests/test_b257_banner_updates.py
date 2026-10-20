"""B257 committed Potential-only publication; real request/transaction path, offline."""
import unittest
from test_investment_update_propagation import fixture,source
class InvestmentBanner(unittest.TestCase):
 def test_no_governor_potential_only_commit_normal_and_dev(self):
  for normal in (True,False):
   with self.subTest(normal=normal):
    l=fixture(2)
    l.execute("""
    c.governor=1
    -- Store-shaped adapter deliberately has no generic permanent-write notification.
    shared.CityProgressionStore={Owns=function()return true end,
     Investment=function(pid,city)return city:GetProperty('SPC_DEV_INVESTMENT_LEDGER_V1')end,
     WriteInvestment=function(pid,city,old,value)city:SetProperty('SPC_DEV_INVESTMENT_LEDGER_V1',value)end}
    """)
    l.execute(source('LevelBannerState'));l.execute("SPCLevelBannerState.Start(P,shared);banner=shared.LevelBanners;banner.Flush();oldRevision=banner.revision;oldOther=banner.views['0:2'];assert(banner.views['0:1'].potential==1)")
    l.execute(f"assert(invest(c,990,{str(normal).lower()}):find('INVESTED'));assert(banner.views['0:1'].potential==2 and banner.views['0:1'].active==1);assert(banner.revision==oldRevision+1 and banner.views['0:2']==oldOther)")
    l.execute(source('UI/LevelBannerModel'))
    l.execute("local m=SPCLevelBannerModel.View(banner.views['0:1'],0,1,c.x,c.y);assert(table.concat(m.segments,',')=='FILLED,OUTLINED,DIM,DIM');local n=banner.revision;notify(0,{status='REJECTED'});notify(0,{status='UNKNOWN'});notify(0,{status='ALREADY_COMMITTED'});assert(banner.revision==n and kills==1)")
if __name__=='__main__':unittest.main()
