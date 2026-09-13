"""B056 formal-profile assertions + unchanged B055 behavior suite, frozen original preserved."""
from pathlib import Path
import math, runpy
R=Path(__file__).resolve().parents[1]
g=runpy.run_path(str(R/'tools/generate_boost.py'))
assert g['LEVEL_WEIGHTS']==(1,2,3,4)
assert g['K']=={'RESEARCH':1.0,'CULTURE':1.0}
# Independently verify all 1,032 SQL amounts, including non-integral sqrt(N).
import re
sql=(R/'Mod/Data/NetworkBoost.sql').read_text()
rows=re.findall(r"\('SPC_B055_(RESEARCH|CULTURE)_([1-4])_([0-9]+)','Amount','([^']+)'\)",sql)
assert len(rows)==1032 and len({(k,l,n) for k,l,n,a in rows})==1032
for kind,level,n,amount in rows:
 assert float(amount)==int(level)*math.sqrt(int(n)),(kind,level,n,amount)
s=(R/'DevelopmentTests/test_b055_boost_gw.py').read_text()
# Only explicit profile/version expectations differ; retain native readout test decimals.
for old,new in [("[0]=='4.5'","[0]=='4.0'"),('2.2*math.sqrt(8)','2*math.sqrt(8)'),("get('version')=='72'","get('version')=='73'"),('4.5*math.sqrt(2)','4*math.sqrt(2)'),('RESEARCH.amount==2.2','RESEARCH.amount==2')]:
 assert s.count(old)==1,old
 s=s.replace(old,new)
exec(compile(s,str(R/'DevelopmentTests/test_b055_boost_gw.py'),'exec'))
s=(R/'DevelopmentTests/test_b055_regression.py').read_text()
assert s.count("'72'")==2
s=s.replace("'72'","'73'")
exec(compile(s,str(R/'DevelopmentTests/test_b055_regression.py'),'exec'))
print('B056 LOCAL_SIMULATION_PASS: formal 1/2/3/4 full table and prior behavior regression.')
