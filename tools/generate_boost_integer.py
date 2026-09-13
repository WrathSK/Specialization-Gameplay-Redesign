"""Formal D0018 integer interface catalog; raw formula remains runtime floating point."""
from pathlib import Path
import math,argparse
MAX_RECIPIENTS=129
MAX_APPLIED=math.floor(4*math.sqrt(MAX_RECIPIENTS)+0.5)
def render():
 sql=['-- B058 integer applied-Boost carriers. Legacy B055 carriers are cleanup-only.']
 lua=['SPCBoostIntegerConfig={maxApplied='+str(MAX_APPLIED)+',rows={}}']
 for kind,target,prop in [('RESEARCH','CIVIC','Civic'),('CULTURE','TECHNOLOGY','Tech')]:
  for amount in range(1,MAX_APPLIED+1):
   m=f'SPC_B058_{kind}_{amount}';b='BUILDING_'+m
   sql.extend([f"INSERT INTO Types(Type,Kind) VALUES ('{b}','KIND_BUILDING');",f"INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing) VALUES ('{b}','Specialization integer network boost',1,'DISTRICT_CITY_CENTER',1,0,0);",f"INSERT INTO Modifiers(ModifierId,ModifierType) VALUES ('{m}','MODIFIER_PLAYER_ADJUST_{target}_BOOST'),('{m}_HD','MODIFIER_PLAYER_ADJUST_PROPERTY');",f"INSERT INTO ModifierArguments(ModifierId,Name,Value) VALUES ('{m}','Amount','{amount}'),('{m}_HD','Key','HD_Player_Extra_{prop}_Boost'),('{m}_HD','Amount','{amount}');",f"INSERT INTO BuildingModifiers(BuildingType,ModifierId) VALUES ('{b}','{m}'),('{b}','{m}_HD');"])
   lua.append(f"SPCBoostIntegerConfig.rows['{kind}:{amount}']='{b}'")
 return {'Mod/Data/NetworkBoostInteger.sql':'\n'.join(sql)+'\n','Mod/BoostIntegerConfig.lua':'\n'.join(lua)+'\n'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();r=Path(__file__).resolve().parents[1]
 for name,text in render().items():
  if a.write:(r/name).write_text(text)
  else:assert (r/name).read_text()==text,name
 print('B058 integer catalog OK')
