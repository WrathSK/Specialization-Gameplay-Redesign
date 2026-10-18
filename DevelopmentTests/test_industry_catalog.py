"""B233 current read-only DB/catalog checks and unchanged B142 assertions.
Requires the existing external DB configuration. Does not connect to a live game.
"""
from pathlib import Path
import json
import sqlite3
import unittest
from lupa.lua55 import LuaRuntime
from project_paths import external_database

R=Path(__file__).resolve().parents[1]

def lua(value):
    if value is None: return 'nil'
    if isinstance(value,bool): return 'true' if value else 'false'
    if isinstance(value,(int,float)): return str(value)
    if isinstance(value,str): return json.dumps(value,ensure_ascii=False)
    if isinstance(value,list): return '{'+','.join(lua(v) for v in value)+'}'
    return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in value.items())+'}'

def tables():
    with sqlite3.connect(external_database(R).as_uri()+'?mode=ro',uri=True) as db:
        db.row_factory=sqlite3.Row
        return {table:[dict(r) for r in db.execute('SELECT rowid AS "Index", * FROM '+table)]
                for table in ('Buildings','Districts','DistrictReplaces','Technologies','Civics','Eras','HD_BuildingTiers','HD_DUMMY_BUILDINGS')}

class CurrentIndustryCatalog(unittest.TestCase):
    def test_current_catalog_normalization_and_wonder_metadata(self):
        data=tables();l=LuaRuntime(unpack_returned_tuples=True)
        l.execute((R/'Mod/StandardizationCatalog.lua').read_text())
        l.execute('tables='+lua(data)+r'''
GameInfo={};local indexed={}
for name,rows in pairs(tables)do
 GameInfo[name]=function()local i=0;return function()i=i+1;return rows[i]end end
 local key=({Buildings='BuildingType',Districts='DistrictType',Technologies='TechnologyType',Civics='CivicType',Eras='EraType'})[name]
 indexed[name]={};for _,row in ipairs(rows)do indexed[name][row.Index]=row;if key then indexed[name][row[key]]=row end end
end
P={Field=function(t,k)return t and t[k]end,Info=function(t,k)return indexed[t] and indexed[t][k]end}
local cat=SPCStandardizationCatalog.Build(P);assert(cat.count>0)
assert(cat.buildings.BUILDING_GRANARY.tier==0)
assert(not cat.districts.DISTRICT_CITY_CENTER and cat.districts.DISTRICT_INDUSTRIAL_ZONE.base=='DISTRICT_INDUSTRIAL_ZONE')
for _,r in ipairs(tables.DistrictReplaces)do
 local unique,base=cat.districts[r.CivUniqueDistrictType],cat.districts[r.ReplacesDistrictType]
 if base then assert(unique and unique.base==base.base)end
end
local n,unknown=0,0
for _,b in ipairs(tables.Buildings)do if b.IsWonder==1 and b.InternalOnly~=1 then
 n=n+1;assert(b.MaxWorldInstances==1,'history key needs a new non-unique Wonder contract')
 local source=b.PrereqTech and P.Info('Technologies',b.PrereqTech) or b.PrereqCivic and P.Info('Civics',b.PrereqCivic)
 if not source or not P.Info('Eras',source.EraType)then unknown=unknown+1 end
end end
assert(n>0);wonderCount=n;unknownEras=unknown;buildingTemplates=cat.count
''')
        print('Current DB: %s unique Wonders, %s unresolved own-era metadata, %s building templates' %
              (l.globals().wonderCount,l.globals().unknownEras,l.globals().buildingTemplates))

    def test_inherited_b142_tier_zero_and_retained_classification_assertions(self):
        data=tables();p=R/'DevelopmentTests/test_b142_templates.py';source=p.read_text()
        source=source.replace("cases = r'''", "setup += 'local dbDistricts='+"+repr(lua(data['Districts']))+"+'\\nlocal dbReplacements='+"+repr(lua(data['DistrictReplaces']))+"+'\\n'\ncases = r'''",1)
        source=source.replace("GameInfo.HD_DUMMY_BUILDINGS=iterator(dbDummy)","GameInfo.HD_DUMMY_BUILDINGS=iterator(dbDummy);GameInfo.Districts=iterator(dbDistricts);GameInfo.DistrictReplaces=iterator(dbReplacements)")
        source=source.replace('local originalBoot=boot',r'''local originalFresh=fresh
function fresh(...)
 local c=originalFresh(...);c.GetDistricts=function()return {GetNumDistricts=function()return 0 end}end;return c
end
local originalBoot=boot''',1)
        # B142's minimal P.Info stub already accepts District keys; the actual DB
        # classification is inspected independently above, without replacing it.
        exec(compile(source,str(p),'exec'),{'__file__':str(p)})

if __name__=='__main__': unittest.main(verbosity=2)
