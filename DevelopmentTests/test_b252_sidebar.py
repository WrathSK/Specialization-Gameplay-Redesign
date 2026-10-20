"""B252 actual presentation callbacks; no native layout/yield acceptance."""
from pathlib import Path
import hashlib,re,sqlite3,struct,unittest,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
from test_b239_commerce_ui import SETUP
ROOT=Path(__file__).resolve().parents[1];MOD=ROOT/'Mod'
def ui():
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(SETUP)
 l.execute((MOD/'UI/DevelopmentInvestmentUI.lua').read_text())
 l.execute(r'''
local old=getmetatable(Controls).__index
local function decorate(c)
 function c:SetSizeVal(w,h)self.width=w;self.height=h end
 function c:SetSizeY(h)self.height=h end
 function c:SetOffsetX(x)self.x=x end;function c:SetOffsetY(y)self.y=y end
 function c:SetTruncateWidth(w)self.truncate=w end;function c:SetWrapWidth(w)self.wrap=w end
 function c:SetColorByName(v)self.color=v end
 function c:GetSizeY()return self.height or math.max(18,math.ceil(#self.text/math.max(1,(self.wrap or 240)/9))*18)end
 function c:CalculateSize()end;function c:ReprocessAnchoring()end;function c:CalculateInternalSize()end
 return c
end
getmetatable(Controls).__index=function(t,k)return decorate(old(t,k))end
GameInfo={Buildings={BUILDING_LIB={Name='图书馆'},BUILDING_MARKET={Name='市场'}},Districts={DISTRICT_CAMPUS={Name='学院'},DISTRICT_HARBOR={Name='港口'}}}
width=1400;height=900;UIManager={GetScreenSizeVal=function()return width,height end};SystemUpdateUI={ScreenResize=7}
function target(id,x,y,name)return {GetID=function()return id end,GetX=function()return x end,GetY=function()return y end,GetName=function()return name end}end
nativeCities={[9]=c,[2]=target(2,20,21,'目标城'),[3]=target(3,30,31,'第二城')}
Players[0].GetCities=function()return {FindID=function(_,id)return nativeCities[id]end}end
managers={};InstanceManager={new=function(_,name)
 local m={items={},resets=0};managers[name]=m
 function m:ResetInstances()self.items={};self.resets=self.resets+1 end
 function m:GetInstance()local i=#self.items+1;local o={};for _,key in ipairs({'Root','Caption','State','Icon'})do o[key]=Controls[name..key..i]end;self.items[i]=o;return o end
 return m
end}
local r={owner=0,cityID=9,x=10,y=11,token='city',changes=0}
developmentView={available=true,stage='READY',canSign=true,token='city',reference=r,revision=1,balance=1000,used=0,workers=2,contracts={},options={
 {targetCity=2,targetName='目标城',domain='DISTRICT_CAMPUS',building='BUILDING_LIB',price=400,cost=60,candidates=2,canSign=true,reason='DEVELOPMENT_READY'},
 {targetCity=3,targetName='第二城',domain='DISTRICT_CAMPUS',canSign=false,reason='DEVELOPMENT_PRICE_UNAVAILABLE'}}}
backend={views={['0:9']=developmentView},revision=1};ExposedMembers.SPC_P0.DevelopmentInvestment=backend
function ack(ok,reason)local p=sent[#sent];backend.lastRequest={owner=0,city=9,token=p.Token,accepted=ok~=false,reason=reason};Events.GameCoreEventPublishComplete.Fire()end
function notify()developmentView.revision=developmentView.revision+1;Events.GameCoreEventPublishComplete.Fire()end
function pick(c,d)managers.DevelopmentCity.items[c].Root.click();managers.DevelopmentDistrict.items[d or 1].Root.click()end
''')
 l.execute((MOD/'UI/DevelopmentInvestmentPanel.lua').read_text());l.execute('ContextPtr.initialize();cityRows=managers.DevelopmentCity;domainRows=managers.DevelopmentDistrict')
 return l
class Sidebar(unittest.TestCase):
 def test_city_domain_details_never_autoselect_or_request(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();assert(#cityRows.items==2 and #domainRows.items==0 and Controls.Confirm.disabled);cityRows.items[1].Root.click();assert(#domainRows.items==1 and Controls.Confirm.disabled);domainRows.items[1].Root.click();assert(not Controls.Confirm.disabled and Controls.Quote.text:find('60') and #sent==1);cityRows.items[2].Root.click();assert(Controls.Confirm.disabled and Controls.QuoteCard.hidden);domainRows.items[1].Root.click();assert(Controls.Confirm.disabled and #sent==1)")
 def test_confirmation_scalar_identity_and_pending_double_click(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);Controls.Confirm.click();Controls.Confirm.click();cityRows.items[2].Root.click();assert(#sent==2 and sent[2].TargetCity==2 and sent[2].Domain=='DISTRICT_CAMPUS' and sent[2].Revision==1 and Controls.Confirm.disabled)")
 def test_reordered_added_options_preserve_selected_identity(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);local a,b=developmentView.options[1],developmentView.options[2];developmentView.options={b,{targetCity=2,targetName='目标城',domain='DISTRICT_HARBOR',canSign=true,price=500,cost=75,building='BUILDING_MARKET',candidates=1},a};notify();assert(#cityRows.items==2 and #domainRows.items==2 and Controls.Quote.text:find('60'));Controls.Confirm.click();assert(sent[2].TargetCity==2 and sent[2].Domain=='DISTRICT_CAMPUS')")
 def test_removed_domain_and_replaced_city_clear_selection(self):
  for change in ["developmentView.options={developmentView.options[2]}","developmentView.options[1].domain='DISTRICT_HARBOR'","nativeCities[2]=target(2,22,23,'同ID新城')"]:
   ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);"+change+";notify();assert(Controls.Confirm.disabled);Controls.Confirm.click();assert(#sent==1)")
 def test_reject_stale_held_requires_explicit_refresh_no_replay(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);Controls.Confirm.click();ack(false,'DEVELOPMENT_QUOTE_STALE');assert(Controls.Error.text:find('STALE') and #sent==2);developmentView.quoteStale=true;notify();Controls.Confirm.click();assert(#sent==2);Controls.Refresh.click();assert(#sent==3 and sent[3].Action=='DEVELOPMENT_REFRESH');ack();developmentView.stage='HELD';developmentView.reason='DEVELOPMENT_MONEY_UNCONFIRMED';notify();assert(Controls.Error.text:find('MONEY_HELD') and Controls.Confirm.disabled)")
 def test_contract_without_route_is_visible_and_snapshot_not_modified(self):
  ui().execute("developmentView.options={};developmentView.canSign=false;developmentView.contracts.target={target={cityID=2,x=20,y=21,token='t'},domain='DISTRICT_CAMPUS',cost=60,debited=59.999,stage='ACTIVE'};LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);assert(Controls.Contract.text:find('59.999') and not Controls.ContractCard.hidden and Controls.Confirm.disabled and #sent==1);assert(not developmentView.contracts.target.canSign)")
 def test_completed_contract_does_not_erase_new_quote_or_duplicate_domain(self):
  ui().execute("developmentView.contracts.target={target={cityID=2,x=20,y=21,token='t'},domain='DISTRICT_CAMPUS',cost=50,debited=50,stage='COMPLETED'};LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);assert(#domainRows.items==1 and Controls.Quote.text:find('60') and Controls.Contract.text:find('COMPLETED') and not Controls.Confirm.disabled);assert(developmentView.options[1].contract==nil)")
 def test_foreign_source_owner_load_and_shutdown_close(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(1,9);assert(#sent==0);LuaEvents.SPC_DevelopmentOpen(0,9);ack();owner=1;Events.GameCoreEventPublishComplete.Fire();assert(Controls.Window.hidden);owner=0;LuaEvents.SPC_DevelopmentOpen(0,9);ack();Events.LoadScreenClose.Fire();assert(Controls.Window.hidden);ContextPtr.shutdown();LuaEvents.SPC_DevelopmentOpen(0,9);assert(#sent==2)")
 def test_only_resize_event_reflows_without_transport(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();local n=cityRows.resets;for i=1,100 do Events.SystemUpdateUI.Fire(99);Events.GameCoreEventPublishComplete.Fire()end;assert(n==cityRows.resets);width=960;height=600;Events.SystemUpdateUI.Fire(7);assert(not Controls.CityColumn.hidden and not Controls.DetailColumn.hidden and Controls.Window.width<=width and Controls.DetailScroll.height>50 and #sent==1);pick(1);assert(Controls.Confirm.y>=Controls.Error:GetSizeY()+8)")
 def test_narrow_navigation_keeps_refresh_and_close_available(self):
  ui().execute("width=700;LuaEvents.SPC_DevelopmentOpen(0,9);ack();assert(not Controls.CityColumn.hidden and Controls.DetailColumn.hidden and not Controls.CompactBar.hidden);cityRows.items[1].Root.click();assert(Controls.CityColumn.hidden and not Controls.DistrictColumn.hidden);domainRows.items[1].Root.click();assert(not Controls.DetailColumn.hidden and not Controls.DetailBack.hidden);Controls.DetailBack.click();assert(not Controls.DistrictColumn.hidden and Controls.Confirm.disabled);Controls.DistrictBack.click();assert(not Controls.CityColumn.hidden);Controls.CompactRefresh.click();assert(#sent==2);ack();Controls.CompactClose.click();assert(Controls.Window.hidden)")
class Package(unittest.TestCase):
 def test_controls_and_chinese_keys(self):
  s=(MOD/'UI/DevelopmentInvestmentPanel.lua').read_text();ids={x.get('ID')for x in ET.parse(MOD/'UI/DevelopmentInvestmentPanel.xml').iter()if x.get('ID')}
  self.assertTrue(set(re.findall(r'Controls\.([A-Za-z0-9_]+)',s))<=ids)
  db=sqlite3.connect(':memory:');db.execute('create table LocalizedText(Language text,Tag text,Text text,primary key(Language,Tag))');db.executescript((MOD/'Text/DevelopmentInvestment.sql').read_text())
  keys=set(re.findall(r"L\('([A-Z_]+)'",s))|set(re.findall(r"\{'\w+','([A-Z_]+)'\}",s))|{'SELECT_CITY','SELECT_DISTRICT'}
  for key in keys:
   if not key.endswith('_'):self.assertIsNotNone(db.execute('select Text from LocalizedText where Tag=?',('LOC_SPC_DEVELOPMENT_'+key,)).fetchone(),key)
 def test_art_header_gradient_native_numeral_and_closure(self):
  db=sqlite3.connect(':memory:')
  db.executescript('CREATE TABLE IconDefinitions(Name TEXT PRIMARY KEY,Atlas TEXT,"Index" INTEGER);CREATE TABLE IconTextureAtlases(Name TEXT,IconSize INTEGER,IconsPerRow INTEGER,IconsPerColumn INTEGER,Filename TEXT,PRIMARY KEY(Name,IconSize));')
  db.executescript((MOD/'Data/Icons.sql').read_text())
  rows=db.execute('SELECT Name,"Index" FROM IconDefinitions WHERE Atlas=? ORDER BY "Index"',('ICON_ATLAS_SPC_INSTITUTION_BASES',)).fetchall()
  self.assertEqual(rows,[(f'ICON_SPC_INSTITUTION_{kind}_BASE',i)for i,kind in enumerate(('RESEARCH','CULTURE','INDUSTRY','COMMERCE'))])
  for size in (32,64):
   self.assertEqual(db.execute('SELECT IconsPerRow,IconsPerColumn,Filename FROM IconTextureAtlases WHERE Name=? AND IconSize=?',('ICON_ATLAS_SPC_INSTITUTION_BASES',size)).fetchone(),(4,1,f'SPC_Institution_Backdrops_{size}.dds'))
  db.close()
  for size,digest in [(32,'d6ced03eb0a7a91717eb008269c859a5da4efe99471b80902e223aa2c0458eec'),(64,'912e8f148ea8698941d5e0be5482b70fdef9966340364b806b9b05c3ff03b0ce')]:
   b=(MOD/f'Textures/SPC_Institution_Backdrops_{size}.dds').read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),digest);self.assertEqual(b[:4],b'DDS ');self.assertEqual(struct.unpack_from('<II',b,12),(size,4*size));self.assertEqual(len(b),128+4*size*size*4)
   # Actual atlas pixels contain distinct opaque top and bottom gradient colors.
   for index in range(4):
    x=index*size+size//2;top=128+4*((size//4)*4*size+x);bottom=128+4*((3*size//4)*4*size+x)
    self.assertNotEqual(b[top:top+3],b[bottom:bottom+3]);self.assertEqual(b[top+3],255)
  tree=ET.parse(MOD/'UI/Institutions.xml');ids={e.get('ID'):e for e in tree.iter()if e.get('ID')};self.assertEqual(ids['Stage'].get('Style'),ids['Name'].get('Style'))
  root=ET.parse(MOD/'SpecializationP0.modinfo').getroot();self.assertEqual(root.get('version'),'279');files=[x.text for x in root.findall('./Files/File')];actual={str(p.relative_to(MOD))for p in MOD.rglob('*')if p.is_file()and p.name not in('.DS_Store','SpecializationP0.modinfo')};self.assertEqual(set(files),actual);self.assertEqual(len(files),len(set(files)))
  imports={e.text for e in root.findall('./InGameActions/ImportFiles/File')};self.assertTrue({f'Textures/SPC_Institution_Backdrops_{s}.dds'for s in(32,64)}<=imports)
 def test_native_language_compilation_and_no_gameplay_writer(self):
  from lupa.lua51 import LuaRuntime as Lua51
  c=Lua51(unpack_returned_tuples=True).eval('function(s)local f,e=loadstring(s);return f~=nil,e end')
  for name in ['UI/DevelopmentInvestmentPanel.lua','UI/Institutions.lua']:
   s=(MOD/name).read_text();ok,err=c(s);self.assertTrue(ok,err)
   for bad in ['SetUpdate(', 'ChangeGoldBalance(', 'SetProperty(', 'CreateBuilding(', 'RemoveBuilding(']:self.assertNotIn(bad,s)
if __name__=='__main__':unittest.main()
