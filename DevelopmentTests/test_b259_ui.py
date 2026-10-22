"""B259 measured presentation checks; native raster/layout remains user-tested."""
from pathlib import Path
import unittest,hashlib,struct,xml.etree.ElementTree as ET
from test_b252_sidebar import ui
from test_b254_levels import ui as banner
ROOT=Path(__file__).resolve().parents[1]
class Presentation(unittest.TestCase):
 def test_exact_badge_and_preserved_bottom(self):
  banner().execute("LuaEvents.SPC_LevelBannerAttach(0,1,1,9,p1);assert(last.Badge.iconSize==49 and last.Badge.w==49 and last.Badge.h==49)")
  b=(ROOT/'Mod/Textures/SPC_Level_Icons_49.dds').read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),'f4f3e925dd3f1d58027fdbd792099f64a7000a16c23b8fed859078ed6db3bcb6');self.assertEqual(len(b),153792);self.assertEqual(struct.unpack_from('<III',b,12),(196,196,784))
 def test_error_contract_separate_card_and_no_protocol_change(self):
  l=ui();l.execute("developmentView.contracts.c={target={cityID=2,x=20,y=21,token='t'},domain='DISTRICT_CAMPUS',stage='ACTIVE',cost=240,debited=239.999};LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);assert(not Controls.ContractTitle.hidden and Controls.Contract.text:find('240'));developmentView.quoteStale=true;notify();assert(Controls.Error.text:find('STALE') and not Controls.Error.hidden and Controls.Footer.height==90 and Controls.Confirm.disabled);local count=#sent;Controls.Confirm.click();assert(#sent==count);developmentView.quoteStale=false;notify();assert(Controls.Error.hidden);assert(developmentView.contracts.c.debited==239.999)")
 def test_empty_contract_state_is_explicit(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);assert(Controls.ContractTitle.hidden and Controls.Contract.text:find('NO_CONTRACT') and not Controls.CurrentCard.hidden)")
 def test_bottom_alignment_four_cards_and_resize(self):
  for w,h in [(1400,900),(960,600),(820,720),(700,600),(360,600)]:
   l=ui();l.execute(f"width={w};height={h};LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1)")
   l.execute("local narrow=width-16<800;assert(Controls.Window.height+27==height);assert(Controls.DetailColumn.y==(narrow and 0 or 148));assert(Controls.DetailColumn.y+Controls.DetailColumn.height+(narrow and 40 or 0)==Controls.Window.height);assert(Controls.Footer.height==90 and Controls.Confirm.height==41 and Controls.Refresh.height==24);assert(Controls.CurrentCard.y==Controls.HelpCard.y+Controls.HelpCard.height+12);assert(Controls.Details.height==Controls.CurrentCard.y+Controls.CurrentCard.height);local count=#sent;Events.SystemUpdateUI.Fire(7);assert(#sent==count)")
 def test_native_footer_structure_left_scrolls_and_contract_parent(self):
  t=ET.parse(ROOT/'Mod/UI/DevelopmentInvestmentPanel.xml');ids={x.get('ID'):x for x in t.iter()if x.get('ID')};self.assertNotIn('DistrictCity',ids)
  footer=ids['Footer'];self.assertIsNone(footer.find('.//Label[@ID="Error"]'));self.assertEqual(footer.get('Size'),'parent,90')
  for name,size,offset in [('Confirm','285,41','0,-3'),('Refresh','285,24','0,4')]:
   self.assertEqual(ids[name].get('Size'),size);self.assertEqual(ids[name].get('Offset'),offset);self.assertEqual(ids[name].get('Anchor'),'C,B')
  for name in ['CityScroll','DistrictScroll']:
   self.assertEqual(ids[name].get('AutoScrollBar'),'0');self.assertEqual(ids[name].find('ScrollBar').get('Anchor'),'L,C')
  self.assertEqual(ids['DistrictScroll'].get('Offset'),'16,54')
  self.assertIsNotNone(ids['CurrentCard'].find('.//Label[@ID="Error"]'));self.assertIsNone(ids['HelpCard'].find('.//Label[@ID="Contract"]'))
  sql=(ROOT/'Mod/Text/DevelopmentInvestment.sql').read_text();self.assertIn('[NEWLINE]实际扣款：',sql);self.assertNotIn(' ｜ 实际扣款：',sql)
if __name__=='__main__':unittest.main()
