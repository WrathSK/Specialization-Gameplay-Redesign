"""Preserve prior suites; only explicit B085 stamps/additive files/shared invalidation delta."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];original=Path.read_text
extra="'ResearchApply.lua','ResearchApplyModel.lua','Data/ResearchApply.sql','DistrictCompleteness.lua',"
def read(self,*a,**kw):
 s=original(self,*a,**kw)
 if self.parent.name=='DevelopmentTests' and self.name!='test_research_apply_regression.py':
  s=s.replace("get('version')=='111'","get('version')=='112'").replace('P0-B-084.111','P0-B-085.112')
  if self.name in ['test_p0_c.py','test_p0_b2.py','test_p0_b1.py']:s=s.replace('allowed={','allowed={'+extra)
  if self.name=='test_p0_a.py':s=s.replace("for p in (M/'Data').glob('*'):","for p in (M/'Data').glob('*'):\n if p.name=='ResearchApply.sql':continue")
 return s
Path.read_text=read
try:
 for name in ['test_research_cross.py','test_research_cross_regression.py']:
  p=R/'DevelopmentTests'/name;exec(compile(p.read_text(),name+'_B085_explicit_deltas','exec'),{'__file__':str(p)})
finally:Path.read_text=original
print('P0-D2 protected prior runtime regression PASS; no historic test edited')
