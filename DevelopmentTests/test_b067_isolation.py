from pathlib import Path
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
s=(R/'DevelopmentTests/test_b064_shadow.py').read_text().replace("replace('89','90')","replace('89','93')")
exec(compile(s,__file__,'exec'))
source=(M/'Gameplay.lua').read_text()
for name in ['SPCCityInheritanceRead.Start','SPCInheritanceShadow.Start','SPCCityInheritance.Start']:
 assert name not in source
assert 'shared.InheritanceIsolation=true' in source
l=LuaRuntime(unpack_returned_tuples=True)
l.execute("shared={CityInheritance={},InheritanceShadow={},CityInheritanceRead={},OnPermanentCityWrite=function() error('unexpected') end}")
l.execute(source[source.index('-- B067: ownership work'):])
l.execute("assert(shared.InheritanceIsolation and shared.CityInheritance==nil and shared.InheritanceShadow==nil and shared.CityInheritanceRead==nil and shared.OnPermanentCityWrite==nil)")
# Execute the actual paused request branch: it must not touch ledgers or city APIs.
a=source.index("  if params.Action=='SHADOW_SELECT'");b=source.index("  if params.Action=='INHERIT_RECORD'",a)
l.execute("params={Action='SHADOW_READ',Token='request'};function call()\n"+source[a:b]+"\nend;call();assert(shared.LastToken=='request' and shared.Snapshot:find('已暂停'))")
for f in ['CityInheritance.lua','InheritanceShadow.lua','CityInheritanceRead.lua']:
 assert (M/f).is_file()
assert 'P0-B-067.93' in (M/'Probe.lua').read_text()
assert 'P0-B-067.93' in (M/'UI/P0Panel.xml').read_text()
print('B067 PASS: no ownership Start calls/listeners from Gameplay, no backup callback/Resolve override active, source preserved, paused read has ACK/no city or ledger access; core regressions and D0025 25% checks pass.')
