"""Frozen existing tests with only version + explicit new network read/notification delta."""
from pathlib import Path
w=Path(__file__).resolve().parents[1]
s=(w/'DevelopmentTests/test_b054_discounts.py').read_text().replace("get('version')=='71'","get('version')=='72'")
exec(compile(s,str(w/'DevelopmentTests/test_b054_discounts.py'),'exec'))
s=(w/'DevelopmentTests/test_b054_regression.py').read_text().replace('70','72')
# This replaces the wrapper's injection source, leaving every old effect assertion intact.
a=' assert (r/name).read_bytes()==expected,name'
extra=r""" if name=='NetworkBridge.lua':
  anchor=b'  if shared.StandardizationDiscount then shared.StandardizationDiscount.Audit() end'
  assert expected.count(anchor)==2
  expected=expected.replace(anchor,anchor+b'\\n  if shared.NetworkBoost then shared.NetworkBoost.Audit() end')
  addition=(Path(__file__).resolve().parents[1]/'DevelopmentTests/Fixtures/B055/NationalNetworkAddition.lua.txt').read_bytes()
  expected=expected.replace(b' -- B049 readonly current source identities, never a history/event-derived list.',addition+b' -- B049 readonly current source identities, never a history/event-derived list.')
"""
assert a in s;s=s.replace(a,extra+a)
exec(compile(s,str(w/'DevelopmentTests/test_b054_regression.py'),'exec'))
