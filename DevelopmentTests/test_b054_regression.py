"""Frozen ledger/effect tests, current package and exact B054 network notification delta."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'DevelopmentTests/test_b052_standardization.py').read_text().replace("manifest.get('version')=='68'","manifest.get('version')=='70'")
exec(compile(s,str(root/'DevelopmentTests/test_b052_standardization.py'),'exec'))
s=(root/'DevelopmentTests/test_b051_all_districts.py').read_text().replace('"root.get(\'version\')==\'67\'"','"root.get(\'version\')==\'70\'"')
old=" assert (r/name).read_bytes()==(b/name).read_bytes(),name"
new=""" expected=(b/name).read_bytes()
 if name=='NetworkBridge.lua':
  anchor=b'  if shared.Lv3Effects then shared.Lv3Effects.Audit() end'
  assert expected.count(anchor)==2
  expected=expected.replace(anchor,anchor+b'\\n  if shared.StandardizationDiscount then shared.StandardizationDiscount.Audit() end')
 assert (r/name).read_bytes()==expected,name"""
injection='s=s.replace('+repr(old)+','+repr(new)+')\nexec(compile(s,'
prefix='wrapper=wrapper.replace("exec(compile(s,",'+repr(injection)+')\n'
s=s.replace('exec(compile(wrapper,',prefix+'exec(compile(wrapper,')
exec(compile(s,str(root/'DevelopmentTests/test_b051_all_districts.py'),'exec'))
