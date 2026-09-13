from pathlib import Path
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
p=w/'DevelopmentTests/test_b049_settler_copy.py'
t=p.read_text().replace("m.get('version')=='62'","m.get('version')=='63'")
t=t.replace("find('SOURCE_DISTRICT_UNAVAILABLE',1,true)","find('详情已记录到日志',1,true)")
t=t.replace("find('工业来源暂不可用',1,true)","find('工业网络数据正在刷新',1,true)")
exec(compile(t,str(p),'exec'),globals())
v.execute('''
local function metadata() return {owner=0,cityID=1,turn=1,kind='RESEARCH',active=4,sources={}} end
local m=metadata();m.industryRecipient=false
assert(SPCLv4CopyRead.Render(P,m):find('尚未接收工业网络',1,true))
m.industryRecipient=true
assert(SPCLv4CopyRead.Render(P,m):find('没有有效的工业四级来源',1,true))
for _,code in ipairs({'NETWORK_REFRESH_PENDING','CURRENT_COUNT_CHANGED','NETWORK_NOT_READY_OR_OWNER','UNEXPECTED'}) do
 m=metadata();m.networkError=code..'\\nstack traceback:\\n/Users/private/NetworkBridge.lua:97'
 local text=SPCLv4CopyRead.Render(P,m)
 assert(not text:find('stack traceback',1,true) and not text:find('/Users/',1,true))
 assert(not text:find('生产力预期为0',1,true))
 assert(text:find('科研：',1,true)) -- local calculation is still visible
end
m=metadata();m.error='bad metadata /Users/private'
assert(not SPCLv4CopyRead.Render(P,m):find('/Users/',1,true))
''')
b=w/'DevelopmentBackups/Specialization-before-B049-network-notice/RuntimeSnapshot'
for p in b.rglob('*'):
 if p.is_file() and str(p.relative_to(b)) not in ['Lv4CopyRead.lua','SpecializationP0.modinfo']:
  assert p.read_bytes()==(r/p.relative_to(b)).read_bytes(),p
print('LOCAL_SIMULATION_PASS B049.63: no-network vs no-IV vs unknown; no stack/path in display; local Research result retained; all other runtime files unchanged.')
