"""B125 direct UI regression with current release stamp; historical assertions retained."""
from pathlib import Path
import unittest
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b124_project_ui.py').read_text().replace("'151'","'152'")
s=s.replace("if __name__=='__main__':unittest.main()",'')
exec(compile(s,str(R/'DevelopmentTests/test_b124_project_ui.py'),'exec'))
class ClaimSync(ClaimUI):
 def test_sync_once_no_begin(self):
  self.prepare_claim();self.runlua('claimUI.Sync(c);claimUI.Sync(c);claimUI.Pulse()')
  self.assertEqual(self.get('#packets'),1);self.assertEqual(self.get('packets[1].Action'),'CLAIM_SYNC')
  self.assertIsNone(self.get('shared.TimedProjectState'))
if __name__=='__main__':unittest.main()
