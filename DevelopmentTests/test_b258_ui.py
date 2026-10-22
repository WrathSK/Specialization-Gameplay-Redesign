"""B258 UI-only regression; fixture geometry is not native raster acceptance."""
from pathlib import Path
import unittest,struct,hashlib,xml.etree.ElementTree as ET
from test_b252_sidebar import ui, Sidebar, Package
from test_b254_levels import ui as banner
ROOT=Path(__file__).resolve().parents[1]
class Refinement(unittest.TestCase):
 def test_banner_uses_matching_image_cell_and_size(self):
  banner().execute("LuaEvents.SPC_LevelBannerAttach(0,1,1,9,p1);assert(last.Badge.iconSize==58 and last.Badge.w==58 and last.Badge.h==58 and not last.Root.hidden)")
  b=(ROOT/'Mod/Textures/SPC_Level_Icons_58.dds').read_bytes()
  self.assertEqual(hashlib.sha256(b).hexdigest(),'9d3277bca2704363223d7346592cbbcadd793883a851a2f190a1c0434258ad54')
  self.assertEqual(struct.unpack_from('<III',b,12),(232,232,928));self.assertEqual(len(b),215424)
 def test_active_first_completed_not_active_and_identity_preserved(self):
  l=ui();l.execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);developmentView.contracts.c={target={cityID=3,x=30,y=31,token='t'},domain='DISTRICT_CAMPUS',cost=60,debited=60,stage='ACTIVE'};notify();assert(cityRows.items[1].Caption.text=='第二城' and not cityRows.items[1].Investing.hidden and cityRows.items[2].Investing.hidden);Controls.Confirm.click();assert(sent[2].TargetCity==2);ack();developmentView.contracts.c.stage='COMPLETED';notify();assert(cityRows.items[1].Caption.text=='目标城' and cityRows.items[2].Investing.hidden);assert(developmentView.options[2].investing==nil)")
 def test_held_and_pending_are_not_claimed_active(self):
  for stage in ['HELD','DEBIT_CALLING','DEBIT_INTENT','TERMINATED']:
   l=ui();l.execute("developmentView.contracts.c={target={cityID=3,x=30,y=31,token='t'},domain='DISTRICT_CAMPUS',cost=60,stage='"+stage+"'};LuaEvents.SPC_DevelopmentOpen(0,9);ack();assert(cityRows.items[1].Caption.text=='目标城' and cityRows.items[2].Investing.hidden)")
 def test_geometry_content_flow_footer_and_resize_no_transport(self):
  for w,h in [(1400,900),(960,600),(820,720),(700,600),(360,600)]:
   with self.subTest(size=(w,h)):
    l=ui();l.execute(f"width={w};height={h};LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1)")
    l.execute("assert(Controls.Window.height+39==height);local narrow=width-16<800;assert(Controls.DetailColumn.y==(narrow and 0 or 150));assert(Controls.DetailColumn.width==Controls.CityColumn.width);assert(Controls.Confirm.y>=Controls.Error:GetSizeY()+8);assert(Controls.Refresh.y+25<=Controls.Footer.height-20);assert(Controls.HelpCard.y==Controls.TermsCard.y+Controls.TermsCard.height+12);assert(Controls.DetailScroll.height>0 and Controls.DetailScroll.height+54+Controls.Footer.height+8==Controls.DetailColumn.height);local n=#sent;Events.SystemUpdateUI.Fire(7);assert(#sent==n)")
 def test_xml_one_detail_scroll_left_titles_and_visible_quote_header(self):
  t=ET.parse(ROOT/'Mod/UI/DevelopmentInvestmentPanel.xml');ids={x.get('ID'):x for x in t.iter() if x.get('ID')}
  for name in ['Quote','Terms','Help']:
   self.assertNotIn(name+'Scroll',ids);self.assertEqual(ids[name+'Title'].get('Anchor'),'L,C');self.assertEqual(ids[name+'Body'].get('Offset'),'12,46')
  self.assertEqual(ids['DetailScroll'].get('AutoScrollBar'),'1')
  self.assertEqual(ids['DetailScroll'].find('ScrollBar').get('Anchor'),'R,C')
  for name in ['DistrictTitle','DetailTitle']:self.assertEqual(ids[name].get('Anchor'),'L,C')
  self.assertIsNotNone(ids['QuoteBuildingRow'].find('Image'));self.assertIsNotNone(ids['QuoteBuildingRow'].find('Label'))
if __name__=='__main__':unittest.main()
