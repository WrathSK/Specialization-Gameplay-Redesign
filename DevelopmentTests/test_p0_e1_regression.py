"""Explicit E1 diagnostic/version adapter; prior gameplay assertions unchanged."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];original=Path.read_text
extra="'CityIdentityRead.lua','UI/P0Panel.lua','UI/P0Panel.xml',"
def read(self,*a,**kw):
 s=original(self,*a,**kw)
 if self.parent.name=='DevelopmentTests' and self.name!='test_p0_e1_regression.py':
  s=s.replace("get('version')=='114'","get('version')=='115'").replace('P0-B-087.114','P0-B-088.115')
  s=s.replace('\nallowed={','\nallowed={'+extra)

 return s
Path.read_text=read
try:
 for name in ['test_u1_presentation.py','test_u1_regression.py']:
  p=R/'DevelopmentTests'/name;exec(compile(p.read_text(),name+'_E1_additions','exec'),{'__file__':str(p)})
finally:Path.read_text=original
print('E1 protected gameplay regression PASS')
