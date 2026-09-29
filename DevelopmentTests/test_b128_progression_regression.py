"""Current release wrapper: B109 accepted start-enabled contract and inherited B108 regressions."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b109_session_origin.py').read_text().replace("'136'", "'155'").replace('modinfo136','modinfo155')
exec(compile(s,str(R/'DevelopmentTests/test_b109_session_origin.py'),'exec'))
