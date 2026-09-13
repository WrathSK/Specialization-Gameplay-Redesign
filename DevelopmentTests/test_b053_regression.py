"""Preserve prior effect and ledger tests; only package version expectation advances."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'DevelopmentTests/test_b052_standardization.py').read_text().replace("manifest.get('version')=='68'","manifest.get('version')=='69'")
exec(compile(s,str(root/'DevelopmentTests/test_b052_standardization.py'),'exec'))
s=(root/'DevelopmentTests/test_b052_existing_effects.py').read_text().replace("==\\'68\\'","==\\'69\\'")
exec(compile(s,str(root/'DevelopmentTests/test_b052_existing_effects.py'),'exec'))
