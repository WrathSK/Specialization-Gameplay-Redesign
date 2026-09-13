"""Pure Lua + isolated SQLite checks; no game launched and no engine precision claim."""
from pathlib import Path
import math
import sqlite3
from lupa import LuaRuntime
base=Path(__file__).resolve().parents[1]
lua=LuaRuntime(unpack_returned_tuples=True)
model=lua.execute((base/'DevelopmentTests/NetworkStrength.lua').read_text())
def strength(n,level=4,kind='CULTURE',k=None):
    return model.Calculate(kind,level,lua.table_from([f'owner0:city{i}' for i in range(n)]),k)['networkStrength']
assert strength(0)==0 and strength(1)==4 and strength(16)==16
assert math.isclose(strength(8),11.313708498984761)
assert math.isclose(strength(7,4,'RESEARCH'),4*math.sqrt(7))
assert math.isclose(strength(7,3,'CULTURE'),3*math.sqrt(7))
assert strength(16,2)==8  # ACTIVE, not potential IV
assert strength(16,4,'RESEARCH',2)==32 and strength(16,4,'CULTURE')==16
increments=[strength(n+1)-strength(n) for n in range(32)]
assert all(a>b>0 for a,b in zip(increments,increments[1:]))
# Same city via multiple routes/centers/legal providers remains one recipient.
result=model.Calculate('CULTURE',4,lua.table_from(['p0:c1','p0:c1','p0:c2','p0:c2']))
assert result['N']==2 and math.isclose(result['networkStrength'],4*math.sqrt(2))
assert model.Calculate('RESEARCH',3,lua.table_from(['p0:c1','p0:c2']))['N']==2
# Disconnection / free-self receiver removal is represented by rebuilding the set.
assert strength(2)>strength(1)>strength(0)
for bad in [0,5,2.5,float('nan')]:
    try:model.Calculate('RESEARCH',bad,lua.table_from([]))
    except Exception:pass
    else:raise AssertionError('invalid active level accepted')
# Reuse the REAL cached schema in memory, preserving FK-related rows. Source is read-only.
source=sqlite3.connect((base/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite").as_uri()+'?mode=ro',uri=True)
db=sqlite3.connect(':memory:');source.backup(db);source.close()
row=db.execute("SELECT a.ModifierId,a.Name FROM ModifierArguments a JOIN Modifiers m USING(ModifierId) WHERE a.Name='Amount' AND m.ModifierType='MODIFIER_PLAYER_ADJUST_TECHNOLOGY_BOOST' LIMIT 1").fetchone()
assert row
for value in ['0.5','11.313708498984761','sqrt(8)']:
    db.execute('UPDATE ModifierArguments SET Value=? WHERE ModifierId=? AND Name=?',(value,*row))
    assert db.execute('SELECT Value FROM ModifierArguments WHERE ModifierId=? AND Name=?',row).fetchone()[0]==value
# Even sqrt(8) stores as text: storage acceptance proves NO expression evaluation.
print('LOCAL_SIMULATION_PASS: sqrt, deduplicated recipients, independent k, ACTIVE level, diminishing marginal gain, removal, invalid inputs; real-schema in-memory text storage.')
print('USER_GAME_TEST_REQUIRED: decimal boost precision, dynamic effect refresh/revocation, trigger ordering. No rounding policy or runtime effects implemented.')
