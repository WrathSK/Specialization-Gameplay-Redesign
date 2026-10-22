"""Actual UI read/intent/display path with deterministic engine-shaped fixtures.
No native cross-context or HD rendering proof. Existing Claim assertions unchanged.
"""
from pathlib import Path
import unittest
import test_b129_claim_sync as claim
from test_dialogue_projects import game

R=Path(__file__).resolve().parents[1]


def ui(l):
    def include(name):
        path=R/'Mod'/(name+'.lua')
        if not path.exists():path=R/'Mod/UI'/(name+'.lua')
        l.execute(path.read_text())
    l.globals().include=include
    l.execute((R/'Mod/UI/DialogueProjectUI.lua').read_text())
    l.execute(r'''
local old=P.Info;local works={}
for i,e in ipairs({'ERA_ANCIENT','ERA_CLASSICAL','ERA_MEDIEVAL'})do
 local t=({'GREATWORK_ARTIFACT_1','GREATWORK_ARTIFACT_10','GREATWORK_ARTIFACT_11'})[i]
 works[t]={GreatWorkType=t,GreatWorkObjectType='GREATWORKOBJECT_ARTIFACT',EraType=e,Name=t};works[i]=works[t]
end
P.Info=function(t,k)
 if t=='GreatWorks'then return works[k]end
 if t=='Eras'then return {EraType=type(k)=='string' and k or GameEra}end
 return old(t,k)
end
GameInfo.Projects={PROJECT_SPC_ERA_DIALOGUE={Hash=1999}}
GameInfo.Buildings=function()local done=false;return function()if not done then done=true;return {Index=998}end end end
c.b.present[998]=true;slots={1}
c.b.GetNumGreatWorkSlots=function()return #slots end
c.b.GetGreatWorkInSlot=function(_,bid,slot)return slots[slot+1]end
c.b.GetGreatWorkTypeFromIndex=function(_,id)return id end
PlayerOperations={EXECUTE_SCRIPT=1};packets={};notifies=0
function send(pid,op,p)
 packets[#packets+1]=p
 if not defer then
  if p.Action=='DIALOGUE_PROJECT_SYNC'then dp.Sync(pid,p.CityID,p.Token)else dp.Request(pid,p)end
 end
end
ui=SPCDialogueProjectUI.New(P,send,function()notifies=notifies+1 end)
''')
    return l


class DialogueUI(unittest.TestCase):
    def test_native_selection_confirms_once_with_fresh_completion_scan(self):
        l=ui(game());l.execute(r'''
ui.WarmStart();ui.Pulse();packets={};assert(ui.Before(c,{Type='PROJECT_SPC_ERA_DIALOGUE'},false))
ui.Pulse();assert(#packets==0)
c.q.target='PROJECT_SPC_ERA_DIALOGUE';c.q.size=0;ui.Pulse();assert(#packets==0)
c.q.size=1;ui.Pulse();ui.Pulse();assert(#packets==1 and packets[1].Action=='DIALOGUE_PROJECT_BEGIN')
assert((SPCDialogueProjectUI.Text(0,c:GetID()))=='1')
slots={1,2};endturn();assert(ledger(c).used.ERA_CLASSICAL.x==2 and ledger(c).total==10)
''')

    def test_fresh_sampler_uses_current_slots_not_background_cache(self):
        l=ui(game());l.execute(r'''
assert(ExposedMembers.SPC_DialogueProjectRead(0,c:GetID(),true).x==1)
slots={1,2,3};assert(ExposedMembers.SPC_DialogueProjectRead(0,c:GetID(),true).x==3)
slots={};assert(ExposedMembers.SPC_DialogueProjectRead(0,c:GetID(),true).x==0)
c.b.GetGreatWorkInSlot=function()error('unknown slot')end;slots={1}
assert(not pcall(ExposedMembers.SPC_DialogueProjectRead,0,c:GetID(),true))
''')

    def test_saved_load_sync_does_not_create_start(self):
        l=ui(game());l.execute(r'''
c.q.target='PROJECT_SPC_ERA_DIALOGUE';c.q.size=1
for i=1,20 do ui.Pulse()end
assert(not ledger(c));for _,p in ipairs(packets)do assert(p.Action=='DIALOGUE_PROJECT_SYNC')end
''')

    def test_retry_is_bounded_and_late_backend_waits(self):
        l=ui(game());l.execute(r'''
local saved=shared.DialogueProjects;shared.DialogueProjects=nil
for i=1,30 do ui.Pulse()end;assert(#packets==0)
shared.DialogueProjects=saved;defer=true
for i=1,50 do ui.Pulse()end
assert(#packets==6) -- at most three sync sends for each of the two fixture cities
for _,p in ipairs(packets)do assert(p.Action=='DIALOGUE_PROJECT_SYNC')end
''')

    def test_pending_click_cancels_for_ordinary_or_multi_queue(self):
        l=ui(game());l.execute(r'''
ui.WarmStart();ui.Pulse();packets={}
assert(not ui.Before(c,{Type='PROJECT_SPC_ERA_DIALOGUE'},true))
assert(ui.Before(c,{Type='PROJECT_SPC_ERA_DIALOGUE'},false));ui.Before(c,{Type='NORMAL'},false)
c.q.target='PROJECT_SPC_ERA_DIALOGUE';c.q.size=1;ui.Pulse();assert(#packets==0)
ui.Before(c,{Type='PROJECT_SPC_ERA_DIALOGUE'},false);c.q.size=2;ui.Pulse();c.q.size=1;ui.Pulse();assert(#packets==0)
''')

    def test_publish_without_changes_does_not_scan_works_or_notify(self):
        l=ui(game());l.execute(r'''
ui.WarmStart();ui.Pulse();ui.Pulse();local count=notifies;local sends=#packets
c.b.GetNumGreatWorkSlots=function()error('ordinary publish must not collect')end
for i=1,100 do ui.Pulse()end
assert(notifies==count and #packets==sends)
''')

    def test_changed_production_display_only_touches_owned_item(self):
        l=ui(game());l.execute((R/'Mod/UI/TimedProjectDisplay.lua').read_text());l.execute(r'''
local list={Owner=0,City=c,ProjectItems={{Type='PROJECT_SPC_ERA_DIALOGUE',TurnsLeft=999999},{Type='NORMAL',TurnsLeft=7,Progress=99}}}
SPCTimedProjectDisplay.Items(list)
assert(list.ProjectItems[1].TurnsLeft=='1' and list.ProjectItems[2].TurnsLeft==7 and list.ProjectItems[2].Progress==99)
begin(c);assert(SPCTimedProjectDisplay.IsCurrent(c));assert((SPCTimedProjectDisplay.Text(0,c:GetID()))=='1')
''')


class PackageAndPanel(unittest.TestCase):
    def test_schema_sql_registration_and_localized_entry(self):
        import sqlite3
        import xml.etree.ElementTree as ET
        from project_paths import external_database
        source=sqlite3.connect(external_database(R).as_uri()+'?mode=ro',uri=True)
        memory=sqlite3.connect(':memory:')
        for table in ('Types','Buildings','Projects'):
            ddl=source.execute('SELECT sql FROM sqlite_master WHERE type=? AND name=?',('table',table)).fetchone()[0]
            memory.execute(ddl)
        # The game assigns Type hashes outside SQLite DDL. Supply distinct test-only hashes.
        memory.execute('CREATE TRIGGER fixture_type_hash AFTER INSERT ON Types BEGIN UPDATE Types SET Hash=rowid WHERE rowid=NEW.rowid; END')
        memory.executescript((R/'Mod/Data/DialogueProjects.sql').read_text())
        row=memory.execute('SELECT Cost,CostProgressionModel,RequiredBuilding FROM Projects WHERE ProjectType=?',('PROJECT_SPC_ERA_DIALOGUE',)).fetchone()
        self.assertEqual(row,(1000000,'NO_PROGRESSION_MODEL','BUILDING_SPC_ERA_DIALOGUE_ACCESS'))
        self.assertEqual(memory.execute('SELECT InternalOnly,CitizenSlots,Housing FROM Buildings').fetchone(),(1,0,0))
        memory.execute('CREATE TABLE LocalizedText(Language TEXT,Tag TEXT,Text TEXT,PRIMARY KEY(Language,Tag))')
        memory.executescript((R/'Mod/Text/DialogueProjects.sql').read_text())
        self.assertEqual(memory.execute('SELECT COUNT(*) FROM LocalizedText').fetchone()[0],6)
        source.close();memory.close()
        tree=ET.parse(R/'Mod/SpecializationP0.modinfo');self.assertEqual(tree.getroot().get('version'),'202')
        files=[e.text for e in tree.findall('./Files/File')]
        self.assertEqual(len(files),len(set(files)))
        self.assertEqual(set(files),{p.relative_to(R/'Mod').as_posix() for p in (R/'Mod').rglob('*') if p.is_file() and p.name not in ('SpecializationP0.modinfo','.DS_Store')})
        for parent,name in (('UpdateDatabase','Data/DialogueProjects.sql'),('UpdateText','Text/DialogueProjects.sql')):
            self.assertEqual([e.text for e in tree.findall('./InGameActions/'+parent+'/File')].count(name),1)
        imports={e.text for e in tree.findall('./InGameActions/ImportFiles/File')}
        self.assertTrue({'DialogueProjectModel.lua','DialogueProjects.lua','UI/DialogueProjectUI.lua'}<=imports)

    def test_actual_panel_button_is_visible_read_only_and_nonoverlapping(self):
        from test_p0_panel_current_layout import panel_runtime
        tree,l=panel_runtime();controls=l.globals().Controls
        self.assertFalse(controls.GWCityButton.hidden)
        self.assertTrue(controls.InspirationEndButton.hidden)
        l.execute("Controls.GWCityButton.callbacks[Mouse.eLClick]();assert(requests[#requests].Action=='DIALOGUE_PROJECT_READ')")
        rects=[]
        for e in tree.getroot().find("Container[@ID='Window']").findall('GridButton'):
            if e.get('ID')=='CloseButton' or controls[e.get('ID')].hidden:continue
            x,y=map(int,e.get('Offset').split(','));w,h=map(int,e.get('Size').split(','));rects.append((x,y,x+w,y+h))
        for i,a in enumerate(rects):
            for b in rects[i+1:]:self.assertTrue(a[2]<=b[0] or b[2]<=a[0] or a[3]<=b[1] or b[3]<=a[1])


class ClaimUIRegression(claim.Sync):
    """Run existing Claim intent/handshake/filter assertions with the new include loaded.
    The inherited fixture replaces include with a no-op, so load only its new direct
    dependency here; native tables support an empty building catalogue for this test.
    """
    def setUp(self):
        super().setUp()
        self.runlua('GameInfo.Buildings=function()return function()end end')
        self.runlua((R/'Mod/GreatWorkFacts.lua').read_text())
        self.runlua((R/'Mod/UI/DialogueProjectUI.lua').read_text())


if __name__=='__main__':unittest.main()
