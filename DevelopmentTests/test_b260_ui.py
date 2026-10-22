"""B260 layout bounds and retained protocol; native rendering remains pending."""
from pathlib import Path
import unittest,xml.etree.ElementTree as ET,hashlib
from test_b252_sidebar import ui
from test_b254_levels import ui as banner
ROOT=Path(__file__).resolve().parents[1]
class Presentation(unittest.TestCase):
 def test_badge_uses_existing_exact_size_and_segments_above(self):
  banner().execute("LuaEvents.SPC_LevelBannerAttach(0,1,1,9,p1);assert(last.Badge.iconSize==32 and last.Badge.w==32 and last.Badge.h==32)")
  t=ET.parse(ROOT/'Mod/UI/LevelBanners.xml');root=t.find('.//Container[@ID="Root"]');badge=root.find('Image');self.assertEqual(badge.get('Offset'),'0,5')
  for c in root.findall('Container'):
   x,y=map(int,c.get('Offset').split(','));w,h=map(int,c.get('Size').split(','));self.assertLessEqual(y+h,5);self.assertLessEqual(x+w,32)
  self.assertEqual(hashlib.sha256((ROOT/'Mod/Textures/SPC_Level_Icons_32.dds').read_bytes()).hexdigest(),'b08fe38e9a66bb0b157d9baf0b6ab818cb6431e4fdaa39cb6a801273559fde89')
 def test_refresh_label_has_no_double_offset_or_smallcaps(self):
  t=ET.parse(ROOT/'Mod/UI/DevelopmentInvestmentPanel.xml');label=t.find('.//Label[@ID="RefreshCaption"]')
  self.assertEqual(label.get('Anchor'),'C,C');self.assertIsNone(label.get('Offset'));self.assertIsNone(label.get('SmallCaps'));self.assertIsNone(label.get('SmallCapsType'))
  ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();pick(1);local n=#sent;Controls.Refresh.click();assert(#sent==n+1)")
 def test_native_district_icon_backing_and_text_clearance(self):
  t=ET.parse(ROOT/'Mod/UI/DevelopmentInvestmentPanel.xml');row=t.find('.//Instance[@Name="DevelopmentDistrict"]/GridButton');frame=row.find('Grid');self.assertEqual(frame.get('Size'),'55,55');self.assertEqual(frame.get('Offset'),'7,7')
  caption=row.find('Label[@ID="Caption"]');self.assertEqual(caption.get('Offset'),'70,7');self.assertGreater(70,7+55)
  self.assertEqual(row.get('Size'),'parent,76');self.assertEqual(frame.find('Image').get('Size'),'32,32')
if __name__=='__main__':unittest.main()
