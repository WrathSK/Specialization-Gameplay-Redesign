"""B254 event-driven detached state, native lifetime bridge and presentation delta."""
from pathlib import Path
import unittest, xml.etree.ElementTree as ET, sqlite3, struct, hashlib
from lupa.lua51 import LuaRuntime
from test_culture_institutions import display
ROOT=Path(__file__).resolve().parents[1]
def load(l,path):l.execute((ROOT/path).read_text())
COMMON='''
function event()local e={fs={}};function e.Add(f)e.fs[#e.fs+1]=f end;function e.Remove(f)for i=#e.fs,1,-1 do if e.fs[i]==f then table.remove(e.fs,i)end end end;return setmetatable(e,{__call=function(_,...)local fs={};for i,f in ipairs(e.fs)do fs[i]=f end;for _,f in ipairs(fs)do f(...)end end})end
Events=setmetatable({},{__index=function(t,k)local e=event();t[k]=e;return e end})
LuaEvents=setmetatable({},{__index=function(t,k)local e=event();t[k]=e;return e end})
function include()end
Game={GetLocalPlayer=function()return 0 end}
'''
def state():
 l=LuaRuntime();l.execute(COMMON+'''
reads=0;priorWrites=0;cities={};facts={}
function city(id,x)local c={};function c:GetOwner()return 0 end;function c:GetID()return id end;function c:GetX()return x or id end;function c:GetY()return 9 end;return c end
for i=1,2 do cities[i]=city(i);facts[i]={specialization='CULTURE',potential=4,active=2,activeStatus='KNOWN'}end
local collection={FindID=function(_,id)return cities[id]end,Members=function()return pairs(cities)end}
Players={[0]={GetCities=function()return collection end}}
P={Field=function(s,k)return s[k]end,IsTestPlayer=function(pid)return pid==0 end}
shared={OnPermanentCityWrite=function()priorWrites=priorWrites+1 end,EffectiveFacts={Read=function(pid,c)reads=reads+1;if fault then error('UNKNOWN')end;return facts[c:GetID()]end}}
''');load(l,'Mod/LevelBannerState.lua');l.execute('SPCLevelBannerState.Start(P,shared);d=shared.LevelBanners');return l

def ui():
 l=LuaRuntime();l.execute(COMMON+'''
function control()local c={};function c:SetHide(v)self.hidden=v end;function c:SetIcon(v,size)self.icon=v;self.iconSize=size end;function c:SetSizeVal(x,y)self.w=x;self.h=y end;function c:SetColor(v)self.color=v end;function c:SetToolTipString(v)self.tip=v end;return c end
UI={GetColorValue=function(r,g,b,a)assert(r>=0 and r<=1 and g<=1 and b<=1 and a==1);return r..':'..g..':'..b end}
Locale={Lookup=function(k,...)return k..'|'..table.concat({...},'|')end}
created=0;destroyed=0;parents={}
function parent()local p={};function p:DestroyChild(c)assert(not c.destroyed);c.destroyed=true;destroyed=destroyed+1 end;return p end
p1=parent();p2=parent()
ContextPtr={SetInitHandler=function(_,f)init=f end,SetShutdown=function(_,f)shutdown=f end,
BuildInstanceForControl=function(_,name,c,p)created=created+1;last=c;c.Root=control();c.Badge=control();for i=1,4 do c['Rim'..i]=control();c['Fill'..i]=control()end end}
v={owner=0,cityID=1,x=1,y=9,specialization='CULTURE',potential=4,active=2,activeStatus='KNOWN'}
ExposedMembers={SPC_P0={LevelBanners={revision=1,views={['0:1']=v}}}}
''');load(l,'Mod/UI/LevelBannerModel.lua');load(l,'Mod/UI/LevelBanners.lua');l.execute('init()');return l

class State(unittest.TestCase):
 def test_event_burst_coalescing_and_empty_publish_zero_reads(self):
  state().execute("Events.LoadScreenClose();assert(reads==2 and d.revision==2);for i=1,100 do Events.GameCoreEventPublishComplete()end;assert(reads==2);for i=1,100 do shared.OnPermanentCityWrite(cities[1],'write')end;assert(reads==2 and priorWrites==100);facts[1].active=3;Events.GameCoreEventPublishComplete();assert(reads==3 and d.views['0:1'].active==3 and d.revision==3);Events.GameCoreEventPlaybackComplete();assert(reads==3)")
 def test_canonical_levels_unknown_and_removal(self):
  state().execute("d.Flush();facts[1].potential=3;Events.GovernorPromoted(0);d.Flush();assert(d.views['0:1'].potential==3);fault=true;shared.OnPermanentCityWrite(cities[1]);d.Flush();assert(d.views['0:1'].active==nil);fault=false;cities[1]=nil;Events.CityRemovedFromMap(0,1);d.Flush();assert(d.views['0:1']==nil and d.views['0:2'])")
 def test_view_detached_from_facts_and_reference(self):
  state().execute("d.Flush();facts[1].active=4;assert(d.views['0:1'].active==2);cities[1]=city(1,10);Events.CityAddedToMap(0,1);d.Flush();assert(d.views['0:1'].x==10 and d.views['0:1'].active==4)")
 def test_non_target_player_and_turn_fallback(self):
  state().execute("d.Flush();Events.GovernorAssigned(9);d.Flush();assert(reads==2);Events.PlayerTurnActivated(0);d.Flush();assert(reads==4 and d.revision==2)")
class CanonicalRead(unittest.TestCase):
 def test_real_store_effective_facts_no_writes_and_governor_change(self):
  from test_store_write_boundaries import fixture
  l=fixture();l.execute("T.start();c=T.research(1);T.governor(2);before=T.writes();savedRecord=T.encode(T.record(c))")
  load(l,'Mod/LevelBannerState.lua')
  l.execute("SPCLevelBannerState.Start(P,shared);d=shared.LevelBanners;d.Flush();assert(d.views['0:'..c:GetID()].active==2 and d.views['0:'..c:GetID()].potential==4);assert(T.writes()==before and T.encode(T.record(c))==savedRecord);T.governor(4);shared.OnPermanentCityWrite(c,'changed');d.Flush();assert(d.views['0:'..c:GetID()].active==4 and T.writes()==before)")
class Presentation(unittest.TestCase):
 def test_five_accepted_cases_and_invalid_identity(self):
  l=LuaRuntime();load(l,'Mod/UI/LevelBannerModel.lua');l.execute("""
  for _,c in ipairs({{1,4,'FILLED,OUTLINED,OUTLINED,OUTLINED'},{2,4,'FILLED,FILLED,OUTLINED,OUTLINED'},{3,3,'FILLED,FILLED,FILLED,DIM'},{2,2,'FILLED,FILLED,DIM,DIM'},{4,4,'FILLED,FILLED,FILLED,FILLED'}})do
   v={owner=0,cityID=1,x=2,y=3,specialization='RESEARCH',active=c[1],potential=c[2],activeStatus='KNOWN'}
   local m=SPCLevelBannerModel.View(v,0,1,2,3);assert(table.concat(m.segments,',')==c[3] and m.icon=='ICON_SPC_LEVEL_RESEARCH_'..c[1])
  end
  for _,a in ipairs({-1,0,5,1.5})do v.active=a;assert(not SPCLevelBannerModel.View(v,0,1,2,3))end
  v.active=2;assert(not SPCLevelBannerModel.View(v,0,1,3,3));v.activeStatus='UNKNOWN_GOVERNOR';assert(not SPCLevelBannerModel.View(v,0,1,2,3))
  """)
 def test_lifetime_attach_update_replace_detach_shutdown(self):
  ui().execute("""
  LuaEvents.SPC_LevelBannerAttach(0,1,1,9,p1);assert(created==1 and not last.Root.hidden and last.Badge.icon=='ICON_SPC_LEVEL_CULTURE_2' and last.Badge.w==40)
  assert(last.Fill1.color==last.Rim1.color and last.Fill3.color~=last.Rim3.color)
  LuaEvents.SPC_LevelBannerAttach(0,1,1,9,p1);assert(created==1)
  v.active=3;ExposedMembers.SPC_P0.LevelBanners.revision=2;Events.GameCoreEventPublishComplete();assert(last.Badge.icon=='ICON_SPC_LEVEL_CULTURE_3')
  LuaEvents.SPC_LevelBannerAttach(0,1,1,9,p2);assert(created==2 and destroyed==1)
  LuaEvents.SPC_LevelBannerDetach(p1);assert(destroyed==1)
  LuaEvents.SPC_LevelBannerDetach(p2);assert(destroyed==2)
  LuaEvents.SPC_LevelBannerAttach(0,1,1,9,p2);shutdown();assert(destroyed==3 and #Events.GameCoreEventPublishComplete.fs==0)
  """)
 def test_unknown_withdrawal_backend_reload_and_foreign_exclusion(self):
  ui().execute("LuaEvents.SPC_LevelBannerAttach(1,1,1,9,p1);assert(created==0);LuaEvents.SPC_LevelBannerAttach(0,1,1,9,p1);ExposedMembers.SPC_P0={};Events.GameCoreEventPlaybackComplete();assert(last.Root.hidden);ExposedMembers.SPC_P0={LevelBanners={revision=1,views={['0:1']=v}}};Events.GameCoreEventPublishComplete();assert(not last.Root.hidden);v.x=99;ExposedMembers.SPC_P0.LevelBanners.revision=2;Events.GameCoreEventPublishComplete();assert(last.Root.hidden)")
 def test_institution_embedded_icon_all_tiers(self):
  display().execute("for i,row in ipairs(rows.items)do assert(row.Icon.icon=='ICON_SPC_LEVEL_CULTURE_'..i and row.Icon.alpha==1 and row.Stage.text==nil)end")
 def test_native_wrapper_preserves_callbacks_and_ready_bootstrap(self):
  l=LuaRuntime();l.execute(COMMON+'''
  named=0;gone=0;attached=0;detached=0
  c={GetOwner=function()return 0 end,GetID=function()return 1 end,GetX=function()return 2 end,GetY=function()return 3 end}
  CityBanner={UpdateName=function()named=named+1 end,Uninitialize=function()gone=gone+1 end,GetCity=function()return c end}
  b=setmetatable({m_Instance={CityBannerButton={},Container={}}},{__index=CityBanner})
  Players={[0]={GetCities=function()return {Members=function()return ipairs({c})end}end}}
  function GetCityBanner()return b end
  LuaEvents.SPC_LevelBannerAttach.Add(function()attached=attached+1 end);LuaEvents.SPC_LevelBannerDetach.Add(function()detached=detached+1 end)
  ''');load(l,'Mod/UI/CityBannerManager_SPC_Levels.lua');l.execute("b:UpdateName();assert(named==1 and attached==1);LuaEvents.SPC_LevelBannerReady();assert(attached==2);b:Uninitialize();assert(gone==1 and detached==1);OnShutdown();assert(#LuaEvents.SPC_LevelBannerReady.fs==0)")
class Package(unittest.TestCase):
 def test_package_closure_syntax_and_assets(self):
  mod=ROOT/'Mod';tree=ET.parse(mod/'SpecializationP0.modinfo');self.assertEqual(tree.getroot().get('version'),'281')
  files=[e.text for e in tree.findall('./Files/File')];actual={str(p.relative_to(mod))for p in mod.rglob('*')if p.is_file()and p.name not in('.DS_Store','SpecializationP0.modinfo')}
  self.assertEqual(set(files),actual);self.assertEqual(len(files),len(set(files)))
  l=LuaRuntime();check=l.eval('function(s)return assert(loadstring(s))end')
  for path in ['LevelBannerState.lua','UI/LevelBanners.lua','UI/LevelBannerModel.lua','UI/CityBannerManager_SPC_Levels.lua','UI/Institutions.lua','Gameplay.lua']:check((mod/path).read_text())
  for size,digest in [(32,'b08fe38e9a66bb0b157d9baf0b6ab818cb6431e4fdaa39cb6a801273559fde89'),(64,'308bdf3bad9e027da81b9284c7b3a11c37fbb6312819995c9be763f1437e778e')]:
   b=(mod/f'Textures/SPC_Level_Icons_{size}.dds').read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),digest);self.assertEqual(len(b),128+16*size*size*4);self.assertEqual(struct.unpack_from('<II',b,12),(size*4,size*4))
  t=ET.parse(mod/'UI/LevelBanners.xml');self.assertEqual(t.find('.//Container[@ID="Root"]').get('AnchorSide'),'O,I')
  for name in ['LevelBannerState.lua','UI/LevelBanners.lua','UI/CityBannerManager_SPC_Levels.lua']:
   source=(mod/name).read_text();self.assertNotIn('SetUpdate',source);self.assertNotIn('SetProperty',source);self.assertNotIn('RequestPlayerOperation',source)
 def test_atlas_and_localization_sql(self):
  d=sqlite3.connect(':memory:');d.executescript('create table LocalizedText(Language text,Tag text,Text text,primary key(Language,Tag));create table IconDefinitions(Name text,Atlas text,"Index" int);create table IconTextureAtlases(Name text,IconSize int,IconsPerRow int,IconsPerColumn int,Filename text);')
  d.executescript((ROOT/'Mod/Text/LevelBanners.sql').read_text());d.executescript((ROOT/'Mod/Data/Icons.sql').read_text());self.assertEqual(d.execute("select count(*) from IconDefinitions where Atlas='ICON_ATLAS_SPC_LEVELS'").fetchone()[0],16);d.close()
if __name__=='__main__':unittest.main()
