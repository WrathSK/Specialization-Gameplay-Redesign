"""Display-only B068.95 regression; actual UI scripts, no native render claim."""
from pathlib import Path
import xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];M=R/'Mod'
p=R/'DevelopmentTests/test_b068_ui.py';s=p.read_text()
# Explicit labels and native-header mock are the authorized presentation delta.
s=s.replace('Controls.Badge.text','Controls.BadgeCaption.text')
s=s.replace('LookUpControl=function() return {} end','LookUpControl=function() return {GetSizeX=function() return 296 end} end')
exec(compile(s,str(p),'exec'),{'__file__':str(p)})
x=E.parse(M/'UI/P0Panel.xml').getroot();buttons=[x.find('./GridButton')]+[b for b in x.find('./Container').findall('./GridButton') if b.get('Hidden')!='1']
assert len(buttons)==17
source=(M/'UI/P0Panel.lua').read_text()
for b in buttons:
 label=b.find('./Label');assert label is not None and label.get('String') and label.get('Style')=='FontNormal14'
 assert b.get('String') is None
 assert 'Controls.'+label.get('ID')+':SetText(' in source
c=(M/'UI/CityPotential.lua').read_text()
assert "Controls.BadgeCaption:SetText(name..v.potential..'级')" in c
assert "'/InGame/WorldTracker/WorldTrackerHeader'" in c
assert 'SetOffsetVal(width+8,36)' in c
assert 'CityPanel/MainPanel' not in c
assert E.parse(M/'SpecializationP0.modinfo').getroot().get('version')=='95'
print('B068.95 PASS: 17 explicit Chinese captions incl open/close, unchanged callbacks; short Potential text, same header +36 vertical offset; existing UI mocks pass. Native text/placement USER_GAME_TEST_REQUIRED.')
