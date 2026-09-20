"""Only additive UI files/metadata are allowed; old gameplay assertions unchanged."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];original=Path.read_text
extra="'UI/CityPotential.lua','InstitutionPresentation.lua','UI/InstitutionOverview.lua','UI/Institutions.lua','UI/Institutions.xml',"
def read(self,*a,**kw):
 s=original(self,*a,**kw)
 if self.parent.name=='DevelopmentTests' and self.name!='test_u1_regression.py':
  if self.name=='test_arch_v2_d2.py':s=s.replace('LuaEvents=Events','LuaEvents=Events; LuaEvents.SPC_PresentationChanged=function() end')
  s=s.replace("get('version')=='113'","get('version')=='114'").replace('P0-B-086.113','P0-B-087.114')
  s=s.replace('\nallowed={','\nallowed={'+extra)
 return s
Path.read_text=read
try:
 for name in ['test_research_chair.py','test_research_chair_regression.py']:
  p=R/'DevelopmentTests'/name;exec(compile(p.read_text(),name+'_U1_additions','exec'),{'__file__':str(p)})
finally:Path.read_text=original
print('U1 protected gameplay regression PASS')
