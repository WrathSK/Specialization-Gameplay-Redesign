"""B253 presentation delta and inherited protocol; no native layout certification."""
from pathlib import Path
import unittest, xml.etree.ElementTree as ET
from test_b252_sidebar import ui
from test_culture_institutions import display
ROOT=Path(__file__).resolve().parents[1]
class Presentation(unittest.TestCase):
 def test_original_badges_full_opacity_all_states_and_native_font(self):
  l=display();l.execute("v.potential=1;v.active=1;LuaEvents.SPC_PresentationChanged();for _,row in ipairs(rows.items)do assert(row.Icon.alpha==1)end;assert(rows.items[4].State.text=='尚未建立' and rows.items[4].Name.alpha<1);v.potential=4;v.active=2;LuaEvents.SPC_PresentationChanged();for _,row in ipairs(rows.items)do assert(row.Icon.alpha==1)end;assert(rows.items[2].State.text=='当前' and rows.items[4].State.text=='未激活')")
  t=ET.parse(ROOT/'Mod/UI/Institutions.xml');ids={e.get('ID'):e for e in t.iter() if e.get('ID')}
  self.assertEqual(ids['Stage'].get('Style'),ids['Name'].get('Style'))
 def test_columns_bottom_equal_sections_and_footer_clearance(self):
  for w,h in [(1400,900),(960,600),(820,720),(700,600),(360,600)]:
   with self.subTest(size=(w,h)):
    l=ui();l.execute(f"width={w};height={h};LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1)")
    l.execute("assert(Controls.Window.height+27==height);assert(Controls.CityColumn.width==Controls.DistrictColumn.width and Controls.DistrictColumn.width==Controls.DetailColumn.width);assert(Controls.QuoteCard.height==Controls.TermsCard.height and Controls.TermsCard.height==Controls.HelpCard.height);assert(Controls.HelpCard.y+Controls.HelpCard.height+58<=Controls.DetailColumn.height-Controls.Footer.height);for _,n in ipairs({'Quote','Terms','Help'})do assert(Controls[n..'Scroll'].height>0)end;assert(Controls.Confirm.y>=Controls.Error:GetSizeY()+8)")
 def test_integer_display_never_mutates_money_or_confirmation(self):
  l=ui();l.execute("developmentView.balance=19665.363281;developmentView.options[1].price=401.25;developmentView.options[1].cost=60.1875;LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);assert(Controls.Balance.text=='LOC_SPC_DEVELOPMENT_TREASURY|19665');assert(Controls.Capacity.text=='LOC_SPC_DEVELOPMENT_CAPACITY|0|2');assert(Controls.CityName.text=='CITY_TEST');assert(not Controls.Quote.text:find('60.1875',1,true));Controls.Confirm.click();assert(sent[2].TargetCity==2 and sent[2].Domain=='DISTRICT_CAMPUS' and sent[2].Amount==nil and developmentView.balance==19665.363281 and developmentView.options[1].cost==60.1875)")
 def test_city_district_strip_paging_no_request_or_selection(self):
  l=ui();l.execute("developmentView.options={};for i=1,10 do developmentView.options[i]={targetCity=2,domain=string.format('DISTRICT_%02d',i),canSign=false,reason='DEVELOPMENT_NO_BUILDING'}end;LuaEvents.SPC_DevelopmentOpen(0,9);ack();assert(cityRows.items[1].DistrictIcon1.icon=='ICON_DISTRICT_01' and not cityRows.items[1].NextIcons.hidden);cityRows.items[1].NextIcons.click();assert(cityRows.items[1].DistrictIcon1.icon=='ICON_DISTRICT_08' and cityRows.items[1].DistrictIcon4.hidden and #sent==1 and #domainRows.items==0);cityRows.items[1].PreviousIcons.click();assert(cityRows.items[1].DistrictIcon7.icon=='ICON_DISTRICT_07');cityRows.items[1].NextIcons.click();developmentView.options={developmentView.options[1]};notify();assert(cityRows.items[1].DistrictIcon1.icon=='ICON_DISTRICT_01' and cityRows.items[1].NextIcons.hidden and #sent==1)")
 def test_empty_city_reason_and_sections_remain_visible(self):
  l=ui();l.execute("developmentView.options={{targetCity=2,reason='DEVELOPMENT_TARGET_OCCUPIED'}};LuaEvents.SPC_DevelopmentOpen(0,9);ack();assert(not cityRows.items[1].State.hidden and cityRows.items[1].State.text:find('OCCUPIED'));cityRows.items[1].Root.click();assert(#domainRows.items==0 and Controls.Quote.text:find('SELECT_DISTRICT') and Controls.Confirm.disabled);for _,n in ipairs({'Quote','Terms','Help'})do assert(not Controls[n..'Card'].hidden)end")
 def test_native_banner_geometry_and_three_independent_scrolls(self):
  tree=ET.parse(ROOT/'Mod/UI/DevelopmentInvestmentPanel.xml');ids={e.get('ID'):e for e in tree.iter()if e.get('ID')}
  self.assertNotIn('Subject',ids);self.assertNotIn('DetailScroll',ids)
  city={e.get('ID'):e for e in tree.find(".//Instance[@Name='DevelopmentCity']").iter() if e.get('ID')}
  self.assertEqual(city['Caption'].get('Offset'),'34,-3')
  self.assertEqual(city['Icon'].get('Offset'),'10,-3')
  for n in ['Quote','Terms','Help']:
   self.assertEqual(ids[n+'Scroll'].get('FullClip'),'1')
   self.assertIsNotNone(ids[n+'Card'].find(".//Grid[@Texture='CityPanel_BannerNone']"))
  self.assertEqual(ids['Window'].get('Offset'),'0,27')
  self.assertEqual(ids['Balance'].get('Offset'),'26,52');self.assertEqual(ids['Capacity'].get('Offset'),'26,74')
 def test_runtime_closure_build_and_unchanged_assets(self):
  import hashlib
  mod=ROOT/'Mod';tree=ET.parse(mod/'SpecializationP0.modinfo');self.assertEqual(tree.getroot().get('version'),'280')
  files=[e.text for e in tree.findall('./Files/File')];actual={str(p.relative_to(mod))for p in mod.rglob('*')if p.is_file()and p.name not in('.DS_Store','SpecializationP0.modinfo')}
  self.assertEqual(set(files),actual);self.assertEqual(len(files),len(set(files)))
  for size,digest in [(32,'d6ced03eb0a7a91717eb008269c859a5da4efe99471b80902e223aa2c0458eec'),(64,'912e8f148ea8698941d5e0be5482b70fdef9966340364b806b9b05c3ff03b0ce')]:
   self.assertEqual(hashlib.sha256((mod/f'Textures/SPC_Institution_Backdrops_{size}.dds').read_bytes()).hexdigest(),digest)
if __name__=='__main__': unittest.main()
