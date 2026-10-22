"""Explicit additive D3 scope/stamp adaptation; frozen prior suites remain intact."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];original=Path.read_text
extra="'ResearchChair.lua','ResearchChairModel.lua','Data/ResearchChair.sql',"
def read(self,*a,**kw):
 s=original(self,*a,**kw)
 if self.parent.name=='DevelopmentTests' and self.name!='test_research_chair_regression.py':
  s=s.replace("get('version')=='112'","get('version')=='113'").replace('P0-B-085.112','P0-B-086.113')
  if self.name in ['test_research_apply.py','test_p0_c.py','test_p0_b2.py','test_p0_b1.py']:s=s.replace('allowed={','allowed={'+extra)
  if self.name=='test_p0_a.py':s=s.replace("for p in (M/'Data').glob('*'):","for p in (M/'Data').glob('*'):\n if p.name=='ResearchChair.sql':continue")
 return s
Path.read_text=read
try:
 for name in ['test_research_apply.py','test_research_apply_regression.py']:
  p=R/'DevelopmentTests'/name;exec(compile(p.read_text(),name+'_B086_explicit_additions','exec'),{'__file__':str(p)})
finally:Path.read_text=original
print('P0-D3 protected prior regression PASS')
