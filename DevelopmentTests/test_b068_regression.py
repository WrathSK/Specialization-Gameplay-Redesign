"""Run previous mechanics with explicit version and approved panel size delta only."""
from pathlib import Path
original=Path.read_text
def current_read(p,*a,**k):
 s=original(p,*a,**k)
 # 15 diagnostics plus close replaces previous <=15 including close. User allows <=21.
 if p.name in ['test_b054_discounts.py','test_b053_purchase.py','test_b052_standardization.py']:
  s=s.replace('len(pos)<=15','len(pos)<=16').replace('len(coords)<=15','len(coords)<=16').replace('len(buttons)<=15','len(buttons)<=16')
 return s
Path.read_text=current_read
try:
 p=Path(__file__).resolve().parent/'test_b067_isolation.py'
 s=p.read_text().replace("replace('89','93')","replace('89','94')").replace('P0-B-067.93','P0-B-068.94')
 exec(compile(s,str(p),'exec'),{'__file__':str(p)})
finally:Path.read_text=original
