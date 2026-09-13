"""Run frozen B051 regression against B052 packaging, without changing effect expectations."""
from pathlib import Path
w=Path(__file__).resolve().parents[1]
s=(w/'DevelopmentTests/test_b051_all_districts.py').read_text()
assert '"root.get(\'version\')==\'67\'"' in s
s=s.replace('"root.get(\'version\')==\'67\'"','"root.get(\'version\')==\'68\'"')
exec(compile(s,str(w/'DevelopmentTests/test_b051_all_districts.py'),'exec'))
