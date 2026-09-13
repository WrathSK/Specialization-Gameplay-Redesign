"""B054 legacy effect/ledger contracts against bootstrap-fix package."""
from pathlib import Path
w=Path(__file__).resolve().parents[1]
s=(w/'DevelopmentTests/test_b054_regression.py').read_text().replace("70", "71")
exec(compile(s,str(w/'DevelopmentTests/test_b054_regression.py'),'exec'))
