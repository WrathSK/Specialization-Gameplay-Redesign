"""Manual currency probe: local contracts only, engine currency semantics remain user-tested."""
from pathlib import Path
import sqlite3,os,zlib,xml.etree.ElementTree as E
from project_paths import external_database
from lupa.lua55 import LuaRuntime
root=Path(__file__).resolve().parents[1];r=Path(os.environ.get('SPC_TEST_MOD_DIR',root/'Mod'))
c=sqlite3.connect(external_database(root).as_uri()+'?mode=ro',uri=True);m=sqlite3.connect(':memory:');c.backup(m);c.close();m.create_function("Make_Hash",1,lambda s:zlib.crc32(s.encode()))
m.executescript((r/'Data/PurchaseProbe.sql').read_text())
assert m.execute("select count(*) from BuildingModifiers where BuildingType like 'BUILDING_SPC_B053_%'").fetchone()[0]==3
assert m.execute("select count(*) from Modifiers m left join DynamicModifiers d on m.ModifierType=d.ModifierType where m.ModifierId like 'SPC_B053_%' and d.ModifierType is null").fetchone()[0]==0
assert m.execute("select group_concat(distinct Name) from ModifierArguments where ModifierId in ('SPC_B053_MONUMENT','SPC_B053_GRANARY')").fetchone()[0] in ('Amount,BuildingType','BuildingType,Amount')
l=LuaRuntime(unpack_returned_tuples=True);l.execute((r/'PurchaseProbe.lua').read_text())
l.execute('''
rows={};for _,k in ipairs({'FIXTURE','DISCOUNT'}) do rows['BUILDING_SPC_B053_'..k]={Index=k} end
P={Info=function(t,k) return rows[k] end,Field=function(t,k) return t[k] end,IsTestPlayer=function(p) return p==0 end}
shared={};load=nil;Events={LoadScreenClose={Add=function(f) load=f end}};writes=0
c={owner=0,has={}}
c.GetID=function() return 1 end;c.GetOwner=function() return c.owner end
c.GetBuildings=function() return {HasBuilding=function(_,k) return c.has[k]==true end,RemoveBuilding=function(_,k) c.has[k]=nil;writes=writes+1 end} end
c.GetBuildQueue=function() return {CreateBuilding=function(_,k) c.has[k]=true;writes=writes+1 end} end
Players={[0]={GetCities=function() return {Members=function() return ipairs({c}) end} end}}
SPCPurchaseProbe.Start(P,shared);d=shared.PurchaseProbe
assert(writes==0);d.Run(0,c,'PURCHASE_READ');assert(writes==0)
assert(not pcall(d.Run,0,c,'PURCHASE_ON'))
d.Run(0,c,'PURCHASE_BASE');assert(c.has.FIXTURE and not c.has.DISCOUNT)
d.Run(0,c,'PURCHASE_ON');local n=writes;d.Run(0,c,'PURCHASE_ON');assert(writes==n and c.has.DISCOUNT)
d.Run(0,c,'PURCHASE_BASE');assert(not c.has.DISCOUNT and c.has.FIXTURE)
d.Run(0,c,'PURCHASE_ON');d.Run(0,c,'PURCHASE_OFF');assert(not c.has.DISCOUNT and not c.has.FIXTURE)
d.Run(0,c,'PURCHASE_BASE');d.Run(0,c,'PURCHASE_ON');c.owner=1
assert(not pcall(d.Run,0,c,'PURCHASE_ON'));load();assert(not c.has.FIXTURE and not c.has.DISCOUNT)
''')
# Fresh runtime because mock above intentionally uses load as event callback.
a=LuaRuntime();
for p in r.rglob('*.lua'):
 result=a.eval('load')(p.read_text(),str(p));assert not isinstance(result,tuple),(p,result)
manifest=E.parse(r/'SpecializationP0.modinfo').getroot();assert manifest.get('version')=='69'
for p in r.rglob('*.xml'):E.parse(p)
for name in ['PurchaseProbe.lua','PurchaseProbeRead.lua','Data/PurchaseProbe.sql']:assert any(x.text==name for x in manifest.findall('./Files/File'))
window=E.parse(r/'UI/P0Panel.xml').getroot().find('./Container');buttons=[x for x in window.findall('./GridButton') if x.get('Hidden')!='1'];coords=[(x.get('Anchor'),x.get('Offset')) for x in buttons];assert len(coords)==len(set(coords)) and len(coords)<=15
print('LOCAL_SIMULATION_PASS B053 SQL references, manual gating, no read writes, idempotent ON, OFF, reload cleanup, owner guard, Lua/XML and panel layout. Gold/Faith semantics NOT simulated as proof.')
