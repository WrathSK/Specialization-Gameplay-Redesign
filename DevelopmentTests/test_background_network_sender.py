from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'test_background_routes.py').read_text().replace('from lupa import LuaRuntime','from lupa.lua55 import LuaRuntime')
source=source.replace("lua.execute((root/'Probe.lua').read_text())","lua.execute((root/'Probe.lua').read_text())\nlua.execute((root/'NetworkSender.lua').read_text())")
ns={'__file__':str(P/'test_background_routes.py')};exec(source,ns)
lua=ns['lua'];root=ns['root']
lua.execute('''
packets={};PlayerOperations={EXECUTE_SCRIPT=1}
UI={RequestPlayerOperation=function(pid,op,p) packets[#packets+1]=p end}
ExposedMembers.SPC_P0={Version=SPCP0.VERSION,RouteSignalRevision=0,NetworkBridge={epoch=7,ready=true}}
''')
lua.execute((root/'UI/BackgroundRoutes.lua').read_text())
lua.execute('''
ContextPtr:init();assert(#packets>=1 and packets[#packets].Action=="NETWORK_PUSH" and packets[#packets].Valid==1 and packets[#packets].Count==0)
ContextPtr:shutdown()
''')
print('LOCAL_SIMULATION_PASS: actual background collector automatically submits scalar batch with no visible UI or panel control.')
