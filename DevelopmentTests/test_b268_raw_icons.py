"""B268 artwork/SQL/package invariants and actual Lua UI behavior; no native render PASS."""
import hashlib,json,sqlite3,struct,unittest
from pathlib import Path
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]
M=R/'Mod'
MAN=json.loads((R/'tools/raw_icons_manifest.json').read_text())
BUILD=json.loads((R/'tools/raw_icons_build.json').read_text())

def db():
 d=sqlite3.connect(':memory:')
 d.executescript('CREATE TABLE IconDefinitions(Name TEXT PRIMARY KEY,Atlas TEXT,[Index] INTEGER); CREATE TABLE IconTextureAtlases(Name TEXT,IconSize INTEGER,IconsPerRow INTEGER,IconsPerColumn INTEGER,Filename TEXT,PRIMARY KEY(Name,IconSize));')
 for n,i in [('UNIT_BUILDER',1),('UNIT_SPY',17),('UNIT_LEU_INVESTOR',8),('UNIT_LEU_INVESTOR_WHITE',9),('DISTRICT_CAMPUS',2),('DISTRICT_THEATER',8),('DISTRICT_INDUSTRIAL_ZONE',9),('DISTRICT_COMMERCIAL_HUB',6)]:
  d.execute('INSERT INTO IconDefinitions VALUES(?,?,?)',('ICON_'+n,'NATIVE',i))
 for n in ['INDUSTRIAL_ZONE','COMMERCIAL_HUB','CAMPUS','THEATER']:
  d.execute('INSERT INTO IconDefinitions VALUES(?,?,?)',('ICON_PROJECT_ENHANCE_DISTRICT_'+n,'NATIVE_PROJECT',1))
 d.executescript((M/'Data/Icons.sql').read_text());return d

class Artwork(unittest.TestCase):
 def test_exact_seventeen_approved_choices(self):
  self.assertEqual([i['id']for i in MAN['items']],['01-06','02-02','03-09','04-01','05-01','06-01','07-02','08-01','09-02','10-05','11-05','12-02','13-05','14-08','15-02','16-02','17-01'])
 def test_fixed_dds_hashes_dimensions_rgba_masks_and_total(self):
  total=0
  for f in BUILD['files']:
   data=(M/'Textures'/f['file']).read_bytes();total+=len(data)
   self.assertEqual(hashlib.sha256(data).hexdigest(),f['sha256']);self.assertEqual(data[:4],b'DDS ')
   h,w,pitch=struct.unpack_from('<III',data,12)
   self.assertEqual((w,h,pitch),(f['width'],f['height'],f['width']*4))
   self.assertEqual(len(data),128+w*h*4);self.assertTrue(f['decoded_pixel_match'])
   self.assertEqual(struct.unpack_from('<8I',data,76),(32,0x41,0,32,0xff0000,0xff00,0xff,0xff000000))
  self.assertEqual(total,BUILD['total_bytes'])
 def test_visible_art_stays_inside_cells_and_unused_cells_empty(self):
  data=(M/'Textures/SPC_Raw_Icons_32.dds').read_bytes()[128:];width=160
  for n in range(20):
   alphas=[data[((n//5*32+y)*width+n%5*32+x)*4+3]for y in range(32)for x in range(32)]
   if n>=17:self.assertFalse(any(alphas));continue
   points=[(i%32,i//32)for i,a in enumerate(alphas)if a>=8]
   self.assertTrue(points)
   self.assertTrue(all(1<=x<=30 and 1<=y<=30 for x,y in points))
 def test_all_required_sizes_and_resources_are_packaged_once(self):
  root=ET.parse(M/'SpecializationP0.modinfo').getroot()
  listed=[x.text for x in root.findall('./Files/File')];imports=[x.text for x in root.findall('./InGameActions/ImportFiles/File')]
  self.assertEqual(len(listed),len(set(listed)))
  actual={str(p.relative_to(M))for p in M.rglob('*')if p.is_file()and p.name not in('.DS_Store','SpecializationP0.modinfo')}
  self.assertEqual(set(listed),actual)
  self.assertEqual(set(MAN['sizes']),{12,16,20,22,24,30,32,38,40,48,50,64,70,80,95,128,200,256})
  for f in BUILD['files']:self.assertEqual(listed.count('Textures/'+f['file']),1);self.assertEqual(imports.count('Textures/'+f['file']),1)
  for context in ['InGameActions','FrontEndActions']:
   nodes=[n for n in root.findall('./'+context+'/UpdateIcons')if n.findtext('File')=='Data/RawIcons.sql']
   self.assertEqual(len(nodes),1);self.assertEqual(nodes[0].findtext('Properties/LoadOrder'),'10001200')

class IconSQL(unittest.TestCase):
 def setUp(self):self.d=db();self.addCleanup(self.d.close)
 def apply(self):self.d.executescript((M/'Data/RawIcons.sql').read_text())
 def icon(self,name):return self.d.execute('SELECT Atlas,[Index] FROM IconDefinitions WHERE Name=?',(name,)).fetchone()
 def test_native_and_legacy_definitions_unchanged(self):
  before=dict((n,(a,i))for n,a,i in self.d.execute('SELECT * FROM IconDefinitions')if not n.startswith('ICON_UNIT_SPC_CREW_')and n not in ['ICON_UNIT_SPC_EXPEDITION_SPY','ICON_UNIT_SPC_RESTRUCTURING_TEAM','ICON_UNIT_SPC_RESTRUCTURING_TEAM_WHITE']and not n.startswith('ICON_PROJECT_SPC_'))
  self.apply()
  for n,v in before.items():self.assertEqual(self.icon(n),v,n)
 def test_all_crew_project_variants_and_unit_aliases(self):
  projects=[n for n, in self.d.execute("SELECT Name FROM IconDefinitions WHERE Name GLOB 'ICON_PROJECT_SPC_CREW_*'")]
  self.assertEqual(len(projects),27);self.apply()
  for n in projects:self.assertEqual(self.icon(n),('ICON_ATLAS_SPC_RAW',2),n)
  for kind,index in [('EXPEDITION_SPY',0),('RESTRUCTURING_TEAM',1)]+[('CREW_'+str(t),2)for t in(250,420,750,1000,1360)]:
   for suffix in('','_PORTRAIT','_WHITE','_FOW'):self.assertEqual(self.icon('ICON_UNIT_SPC_'+kind+suffix),('ICON_ATLAS_SPC_RAW',index))
 def test_claims_reuse_native_districts_and_all_raw_slots_resolve(self):
  self.apply()
  for c in MAN['claims']:self.assertEqual(self.icon('ICON_PROJECT_SPC_CLAIM_'+c['key']),self.icon('ICON_DISTRICT_'+c['district']))
  for item in MAN['items']:self.assertEqual(self.icon(item['icon']),('ICON_ATLAS_SPC_RAW',item['index']))
 def test_sql_idempotent_and_project_mapping(self):
  self.apply();before=list(self.d.iterdump());self.apply();self.assertEqual(before,list(self.d.iterdump()))
  for key,index in [('COMMERCIALIZATION',11),('CAPITAL_INVESTMENT',12),('DEVELOPMENT_INVESTMENT',13),('ERA_DIALOGUE',14),('ENGINEERING_STUDY',15)]:self.assertEqual(self.icon('ICON_PROJECT_SPC_'+key),('ICON_ATLAS_SPC_RAW',index))

def action_panel(kind):
 l=LuaRuntime();l.execute("""
 include=function()end
 SPCP0={VERSION='B268',IsTestPlayer=function(n)return n==0 end,CrewBase=function(k)if k=='UNIT_SPC_CREW_250' then return 250 end end,Field=function(t,k)return t[k]end}
 Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return 1 end}
 unit={GetOwner=function()return 0 end,GetID=function()return 7 end,GetX=function()return 2 end,GetY=function()return 3 end,GetType=function()return 1 end}
 GameInfo={Units={[1]={UnitType=KIND}}};ExposedMembers={SPC_P0={Version='B268'}};requests={}
 Mouse={eLClick=1};PlayerOperations={EXECUTE_SCRIPT=1};InterfaceModeTypes={SELECTION=1};Events={}
 Locale={Lookup=function(k)return k end}
 parent={CalculateSize=function()end,ReprocessAnchoring=function()end}
 Controls=setmetatable({},{__index=function(t,k)local c={SetHide=function(s,v)s.hide=v end,SetDisabled=function(s,v)s.disabled=v end,
 SetIcon=function(s,v,n)s.icon=v;s.cell=n end,SetToolTipString=function(s,v)s.tip=v end,ChangeParent=function()end,
 RegisterCallback=function(s,_,f)s.click=f end,SetSizeX=function(s,v)s.width=v end,SetOffsetX=function(s,v)s.offset=v end};t[k]=c;return c end})
 ContextPtr={SetInitHandler=function(_,f)init=f end,SetShutdown=function()end,SetUpdate=function(_,f)tick=f end,SetHide=function()end,LookUpControl=function()return parent end}
 UI={GetHeadSelectedUnit=function()return unit end,GetInterfaceMode=function()return 1 end,RequestPlayerOperation=function(_,_,p)
 requests[#requests+1]=p;local s=ExposedMembers.SPC_P0
 if p.Action=='UNIT_ACTION_VIEW'then s.UnitActionView={token=p.Token,owner=0,unitID=7,x=2,y=3,turn=1,legal=true,prepared=plan~=nil,planToken=plan,amount=250,baseInput=100,baseUnused=0,progress=20,cost=400,targetName='WONDER',specialization='RESEARCH',potential=1,nextPotential=2}
 elseif p.Action=='UNIT_ACTION_PREPARE'then plan='PLAN';s.UnitActionPreview={owner=0,unitID=7,x=2,y=3,turn=1,token=plan};s.LastToken=p.Token;s.Snapshot='PREPARED'
 elseif p.Action=='UNIT_ACTION_CONFIRM'then assert(plan and p.PlanToken==plan);confirmed=(confirmed or 0)+1;plan=nil;s.UnitActionPreview=nil;s.LastToken=p.Token;s.Snapshot='DONE'end
 end}
 function refresh()for n=1,4 do tick(.3)end end
 """.replace('KIND',repr(kind)))
 l.execute((M/'UI/UnitPanelActions.lua').read_text());l.execute('init();refresh()');return l

class ActualUI(unittest.TestCase):
 def test_split_prepare_confirm_icons_preserve_exact_request(self):
  l=action_panel('UNIT_SPC_CREW_250');l.execute("assert(Controls.PrepareIcon.icon=='ICON_SPC_RAW_CREW_PREPARE' and Controls.ConfirmIcon.icon=='ICON_SPC_RAW_CREW_CONFIRM' and Controls.PrepareIcon.cell==38);assert(Controls.ConfirmButton.hide);Controls.PrepareButton.click();refresh();assert(not Controls.ConfirmButton.hide and not confirmed);Controls.ConfirmButton.click();Controls.ConfirmButton.click();refresh();assert(confirmed==1)")
 def test_split_settler_pair_preserves_two_step_request(self):
  l=action_panel('UNIT_SETTLER');l.execute("assert(Controls.PrepareIcon.icon=='ICON_SPC_RAW_INVEST_PREPARE' and Controls.ConfirmIcon.icon=='ICON_SPC_RAW_INVEST_CONFIRM');Controls.PrepareButton.click();refresh();assert(not Controls.ConfirmButton.hide and not confirmed);Controls.ConfirmButton.click();refresh();assert(confirmed==1)")
 def test_restructuring_icons_follow_phase_in_both_steps(self):
  from test_b247_ui_package import ui
  l=ui();l.execute("oldAdd=AddActionToTable;function AddActionToTable(a,row,...)oldAdd(a,row,...);a.SPECIFIC[#a.SPECIFIC].icon=row.Icon end")
  for action,icon in [('LIQUIDATE','LIQUIDATE'),('CONFIGURE','CONFIGURE')]:
   l.execute("v.action='%s';v.prepared='plan';local a=SPCRestructuringUI.Actions(u,make());assert(a.SPECIFIC[2].icon=='ICON_SPC_RAW_%s' and a.SPECIFIC[3].icon=='ICON_SPC_RAW_%s');a.SPECIFIC[3].CallbackFunc();assert(sent[#sent].Action=='REST_CONFIRM' and sent[#sent].PlanToken=='plan')"%(action,icon,icon))
 def test_claim_overlay_recycling_scale_and_stop(self):
  l=LuaRuntime();l.execute("function event()local e={};function e.Add(f)e.f=f end;function e.Remove(f)if e.f==f then e.f=nil end end;return setmetatable(e,{__call=function(_,...)if e.f then e.f(...)end end})end\nLuaEvents={SPC_ClaimIconDecorate=event()};alloc=0\nfunction control()return {SetHide=function(s,v)s.hide=v end,SetSizeVal=function(s,w,h)s.w=w;s.h=h end,SetIcon=function(s,n,c)s.icon=n;s.cell=c end}end\nContextPtr={BuildInstanceForControl=function(_,name,e,parent)assert(name=='SPCClaimIconInstance');alloc=alloc+1;e.Root=control();e.Mark=control();last=e end}\nparent={GetSizeX=function()return width end,GetSizeY=function()return width end};width=32\n")
  l.execute((M/'UI/ClaimIconOverlay.lua').read_text())
  l.execute("a=SPCClaimIconOverlay.New();LuaEvents.SPC_ClaimIconDecorate(parent,'ICON_PROJECT_SPC_CLAIM_RESEARCH');assert(alloc==1 and last.Mark.icon=='ICON_SPC_RAW_CLAIM_MARK' and last.Root.w==16 and last.Mark.w==16 and last.Mark.cell==16 and not last.Root.hide);LuaEvents.SPC_ClaimIconDecorate(parent,'ICON_UNIT_BUILDER');assert(last.Root.hide);width=95;LuaEvents.SPC_ClaimIconDecorate(parent,'ICON_PROJECT_SPC_CLAIM_CULTURE');assert(alloc==1 and last.Mark.w==48 and last.Mark.cell==48 and not last.Root.hide);a.Stop();assert(not LuaEvents.SPC_ClaimIconDecorate.f)")

if __name__=='__main__':unittest.main()
