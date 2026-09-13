from pathlib import Path
import xml.etree.ElementTree as E
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
root=E.parse(r/'UI/P0Panel.xml').getroot();window=root.find("Container[@ID='Window']");legacy=window.find("Container[@ID='LegacyProbeButtons']");assert legacy.get('Hidden')=='1'
ids=[x.get('ID') for x in root.iter() if x.get('ID')];assert len(ids)==len(set(ids))
visible=[x for x in window.findall('GridButton') if x.get('ID')!='CloseButton'];assert len(visible)==9
for x in visible:
 left,bottom=map(int,x.get('Offset').split(','));width,height=map(int,x.get('Size').split(','));assert left+width<=840 and 664-bottom-height>=526
assert window.find("Label[@ID='Status']").get('Offset')=='18,62'
l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
include=function() end;SPCP0={VERSION='P0-B-036',IsTestPlayer=function() return true end}
Game={GetLocalPlayer=function() return 0 end};Mouse={eLClick=1};callbacks={};texts={}
Controls={};ContextPtr={SetHide=function() end,SetInitHandler=function(_,f) init=f end,SetShutdown=function() end}
Events={LoadScreenClose={Add=function() end,Remove=function() end}}
''')
for id in ids:
 l.execute('local id=...;Controls[id]={SetText=function(_,s) texts[id]=s end,SetHide=function() end,RegisterCallback=function(_,event,f) callbacks[id]=f end}',id)
l.execute((r/'UI/P0Panel.lua').read_text());l.execute("init();assert(texts.Title=='SPC P0-B-036 | B035 GPP tests')")
for x in root.iter('GridButton'): assert l.eval('callbacks')[x.get('ID')] is not None,x.get('ID')
manifest=E.parse(r/'SpecializationP0.modinfo').getroot();assert manifest.get('version')=='45'
print('PASS: 9 visible task buttons, 464px report-to-button gap, legacy controls retained/hidden, every actual Lua callback binds, dynamic build title, manifest45.')
