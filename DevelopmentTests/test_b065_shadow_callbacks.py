from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b064_shadow.py').read_text().replace("replace('89','90')","replace('89','91')")
exec(compile(s,__file__,'exec'))
assert 'P0-B-065.91' in (R/'Mod/Probe.lua').read_text()
assert 'P0-B-065.91' in (R/'Mod/UI/P0Panel.xml').read_text()
print('B065 PASS: callbacks with no unpack functions, nil/false/zero arguments, automatic load capture, bounded event logs; concise UI errors; displayed version matches manifest91.')
