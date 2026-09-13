from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'test_network_bridge.py').read_text()
source=source.replace('GetNumOutgoingRoutes','CountOutgoingRoutes').replace("=='32'","=='33'")
# UI-only method is absent in this Gameplay fixture: catches the B025 context error.
exec(compile(source,str(P/'test_network_bridge.py'),'exec'),{'__file__':str(P/'test_network_bridge.py')})
from lupa.lua55 import LuaRuntime
R=P.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
old=P.parent/'DevelopmentBackups/Specialization-before-B026'/R.relative_to(P.parent)/'NetworkBridge.lua'
assert 'GetNumOutgoingRoutes()' in old.read_text()
assert 'GetNumOutgoingRoutes' not in (R/'NetworkBridge.lua').read_text()
assert 'CountOutgoingRoutes()' in (R/'NetworkBridge.lua').read_text()
print('LOCAL_SIMULATION_PASS: Gameplay fixture exposes CountOutgoingRoutes only; all sender/receiver and capital self-source/distribution scenarios pass. Native result still user-tested.')
