"""Read-only P09b micro-fixture: actual source boundaries, one injected exception.

No tests are discovered or batch-run. All engine state is memory-only; the script
and JSON result are audit artifacts only. Use --repo when running outside the audit folder.
"""
import argparse
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path)
args = parser.parse_args()
ROOT = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location('p09b_fixture', ROOT / 'DevelopmentTests/test_p0_k.py')
fixture_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture_module)
fx = fixture_module.Fixture()
lua = fx.lua
lua.execute(fixture_module.PRODUCER)
lua.execute("""
aeCalls=0;meCalls=0
aeData={ready=true,fail=true,Audit=function()
 aeCalls=aeCalls+1
 if aeData.fail then error('INJECTED_AE_ESCAPED_EXCEPTION')end
end}
meData={ready=true,Audit=function()meCalls=meCalls+1 end}
shared.CultureMeaning=meData
shared.Dialogue.Receive=function(pid,p)shared.Dialogue.seq[pid]=p.Seq;return true end
shared.Dialogue.ConfirmSamplePair=function()return true end
""")
ae = (ROOT / 'Mod/CultureAesthetic.lua').read_text().splitlines()
me = (ROOT / 'Mod/CultureMeaning.lua').read_text().splitlines()
# Verbatim actual registration fragments; effect Audit bodies are explicit stubs.
assert 'shared.GreatWorkFacts.OnConfirmed=function' in ae[230]
assert 'function d.CollectionConfirmed' in me[173]
assert 'local previous=shared.GreatWorkFacts.OnConfirmed' in me[232]
lua.execute('do local d=aeData\n' + '\n'.join(ae[230:246]) + '\nend')
lua.execute('do local d=meData\n' + '\n'.join(me[173:178]) + '\n'
            + '\n'.join(me[232:239]) + '\nend')
gameplay = (ROOT / 'Mod/Gameplay.lua').read_text()
start = gameplay.index("  if params.Action=='DIALOGUE_SAMPLE' then\n")
end = gameplay.index("  if params.Action=='SHADOW_SELECT'", start)
lua.execute('function sampleRoute(playerID,params)\n' + gameplay[start:end] + '\nend')
lua.execute("""
UI.RequestPlayerOperation=function(pid,op,p)
 requestLog[#requestLog+1]=p;lastPacket=p;sampleRoute(pid,p);return true
end
""")
lua.execute((ROOT / 'Mod/UI/DialogueRefresh.lua').read_text())
lua.execute("""
init()
local f=shared.GreatWorkFacts;local ui=ExposedMembers.SPC_DialogueBackground
assert(f.state=='VERIFIED' and f.ack==1 and shared.Dialogue.seq[0]==1 and ui.state=='IDLE')
assert(aeCalls==1 and meCalls==0 and f.consumerError=='GW_CONSUMER_UPDATE_FAILED')
first={ack=f.ack,state=f.state,uiState=ui.state,aeCalls=aeCalls,meCalls=meCalls,
 sends=ui.sends,consumerError=f.consumerError}
aeData.fail=false
for i=1,12 do fire('SystemUpdateUI')end
assert(ui.sends==1 and meCalls==0 and ui.retries==0)
local nextPacket={};for k,v in pairs(lastPacket)do nextPacket[k]=v end
nextPacket.Seq=2;nextPacket.Token='same-facts-new-seq';sampleRoute(0,nextPacket)
assert(f.ack==2 and meCalls==0 and aeCalls==1)
identical={ack=f.ack,aeCalls=aeCalls,meCalls=meCalls,sends=ui.sends,
 retries=ui.retries,consumerError=f.consumerError}
a.slots[10]={100};fire('GreatWorkCreated',0,999,a.x,a.y);fire('SystemUpdateUI')
assert(meCalls>0 and f.consumerError==nil and f.Read(0,7).count==1)
changed={ack=f.ack,aeCalls=aeCalls,meCalls=meCalls,sends=ui.sends,
 uiState=ui.state,factsCount=f.Read(0,7).count}
shutdown();f.Shutdown()
""")
source_files = {
    'DevelopmentTests/test_p0_k.py', 'Mod/CultureAesthetic.lua',
    'Mod/CultureMeaning.lua', 'Mod/Gameplay.lua', 'Mod/UI/DialogueRefresh.lua',
}
source_files.update('Mod/' + name + '.lua' for name in fx.loaded)
result = {
    'classification': 'LOCAL_SIMULATION_CONFIRMED_COUNTEREXAMPLE',
    'scope': 'Real GreatWorkFacts and UI sender, actual Gameplay branch and verbatim AE/Meaning callback registration plus actual Meaning CollectionConfirmed. Engine and effect Audit bodies are stubs; AE Audit deliberately throws once. Dialogue only supplies independent accepted ACK.',
    'limits': 'No native event timing, yield behavior, persistence, full consumer runtime, or probability of escaped AE exceptions established.',
    'first_exception': dict(lua.globals().first),
    'after_twelve_idle_pulses_and_identical_new_sequence': dict(lua.globals().identical),
    'after_real_changed_sample': dict(lua.globals().changed),
    'source_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sorted(source_files)},
}
print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
