"""B213 selected-city Insight reporting: actual read function, no native effects."""
from pathlib import Path
import unittest
from lupa.lua55 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]

def fixture():
    lua=LuaRuntime(unpack_returned_tuples=True)
    lua.execute('include=function()end;SPCPerformance={Count=function()end,Observe=function()end}')
    lua.execute((ROOT/'Mod/Probe.lua').read_text())
    lua.execute("""
    logs={};print=function(s)logs[#logs+1]=s end
    Locale={Lookup=function(k)return k end};GameInfo={Civilizations={}}
    PlayerConfigurations={[2]={GetCivilizationTypeName=function()return 'CIVILIZATION_OWN' end}}
    city={GetOwner=function()return 2 end,GetID=function()return 9 end,GetName=function()return 'Archive City' end}
    records={};reads=0;store={ExpeditionInsights=function(pid,c)assert(pid==2 and c==city);reads=reads+1;return records end}
    function add(civ,cat)records[civ..':'..cat]={civ=civ,category=cat,turn=5}end
    function read()return SPCP0.DescribeCultureInsights(2,city,store)end
    """)
    return lua

class InsightReportTests(unittest.TestCase):
    def test_no_team_and_empty_history(self):
        l=fixture();text=l.eval('read()');self.assertIn('历史记录：0份',text);self.assertIn('网络接收状态',text);self.assertNotIn('尚未实施',text)
        self.assertEqual(l.eval('reads'),1);self.assertEqual(l.eval('#logs'),1)
    def test_history_owner_filter_and_completed_categories(self):
        l=fixture();l.execute("add('CIVILIZATION_OWN','WORKS');add('CIVILIZATION_FOREIGN','PEOPLE');add('CIVILIZATION_FOREIGN','PLACES')")
        text=l.eval('read()');self.assertIn('历史记录：3份　当前有效：2份',text)
        self.assertIn('风土考察：已完成',text);self.assertIn('艺文采撷：未完成',text)
        self.assertEqual(l.eval('#logs'),4)
        l.execute("assert(records['CIVILIZATION_OWN:WORKS'].turn==5)")
    def test_missing_or_corrupt_history_is_unknown_not_zero(self):
        for fault in ["error('unavailable')","return nil","return {bad={civ='CIVILIZATION_X',category='WORKS'}}"]:
            with self.subTest(fault=fault):
                l=fixture();l.execute('store.ExpeditionInsights=function()'+fault+' end')
                text=l.eval('read()');self.assertIn('UNKNOWN',text);self.assertNotIn('历史记录：0',text)
                self.assertEqual(l.eval('#logs'),1)
    def test_wrong_owner_does_not_read_history(self):
        l=fixture();l.execute('city.GetOwner=function()return 8 end')
        self.assertIn('UNKNOWN',l.eval('read()'));self.assertEqual(l.eval('reads'),0)
    def test_report_deterministic_bounded_without_writes(self):
        l=fixture();l.execute("for i=1,64 do for _,c in ipairs({'PEOPLE','WORKS','PLACES'})do add('CIVILIZATION_X'..i,c)end end")
        a=l.eval('read()');self.assertEqual(l.eval('#logs'),193);self.assertEqual(l.eval('read()'),a)
        l.execute("add('CIVILIZATION_OVER','WORKS');logs={}")
        self.assertIn('UNKNOWN',l.eval('read()'));self.assertEqual(l.eval('#logs'),1)
    def test_city_lookup_failure_still_acknowledges_request(self):
        l=fixture()
        source=(ROOT/'Mod/Gameplay.lua').read_text()
        block=source.split("  if params.Action=='CULTURE_INSIGHTS_READ' then",1)[1].split("  if params.Action=='RESEARCH_TRADITION_READ'",1)[0].rsplit('  end',1)[0]
        l.execute("Players={[2]={GetCities=function()error('native unavailable')end}};shared={};params={CityID=9,Token='insight-read'};playerID=2;P=SPCP0")
        l.execute('function dispatch() '+block+' end;dispatch()')
        self.assertEqual(l.eval('shared.LastToken'),'insight-read')
        self.assertIn('UNKNOWN',l.eval('shared.Snapshot'))

    def test_gameplay_action_only_routes_to_reader(self):
        source=(ROOT/'Mod/Gameplay.lua').read_text()
        block=source.split("if params.Action=='CULTURE_INSIGHTS_READ' then",1)[1].split("if params.Action=='RESEARCH_TRADITION_READ'",1)[0]
        self.assertIn('P.DescribeCultureInsights',block)
        for forbidden in ['AddExpeditionInsight','Import(','.Request(','.Refresh(','.Write(']:self.assertNotIn(forbidden,block)

if __name__=='__main__':unittest.main()
