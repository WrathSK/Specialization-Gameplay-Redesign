"""Static SQL/reference verification on isolated in-memory copies; never opens Civ6."""
from pathlib import Path
import sqlite3
import xml.etree.ElementTree as ET
import zlib
import json

workspace = Path(__file__).resolve().parents[1]
mod = workspace / "Sid Meier's Civilization VI/Mods/SpecializationP0"
cache = workspace / "Firaxis Games/Sid Meier's Civilization VI/Cache"
assets = Path("/Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets")
xp = assets / "DLC/Expansion1"

def database(name):
    source = sqlite3.connect((cache / name).as_uri() + "?mode=ro", uri=True)
    result = sqlite3.connect(":memory:")
    source.backup(result)
    source.close()
    # Schema triggers need the game's Make_Hash. This stub checks relational wiring,
    # NOT the game's binary hash algorithm. SQL IDs stay literal strings in this mod.
    result.create_function("Make_Hash", 1, lambda s: zlib.crc32(s.encode()))
    # A user run may have already loaded this mod into the cache. Remove only
    # its namespaced fixture rows from the IN-MEMORY copy before replaying SQL.
    # The source connection was read-only and is already closed.
    def owned(value):
        return isinstance(value, str) and (value.startswith(("SPC_P0_", "LOC_SPC_", "MODIFIER_SPC_", "ICON_CIVILIZATION_SPC_", "ICON_LEADER_SPC_"))
            or value in {"CIVILIZATION_SPC_TEST", "LEADER_SPC_TEST", "TRAIT_CIVILIZATION_SPC_TEST"})
    result.create_function("SPC_FIXTURE_OWNED", 1, owned)
    for (table,) in result.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall():
        quoted = '"' + table.replace('"', '""') + '"'
        columns = [row[1] for row in result.execute("PRAGMA table_info(" + quoted + ")")]
        predicate = " OR ".join('SPC_FIXTURE_OWNED("' + col.replace('"', '""') + '")' for col in columns)
        if predicate:
            result.execute("DELETE FROM " + quoted + " WHERE " + predicate)
    result.commit()
    return result

def apply(db, path):
    db.executescript((mod / path).read_text())

def rows(db, table):
    return set(db.execute('SELECT * FROM "' + table + '"').fetchall())

game = database("DebugGameplay.sqlite")
tables = [r[0] for r in game.execute("SELECT name FROM sqlite_master WHERE type='table'")]
before = {table: rows(game, table) for table in tables}
fk_before = set(game.execute("PRAGMA foreign_key_check"))
apply(game, "Data/Identity.sql")
apply(game, "Data/GovernorProbe.sql")
assert not (set(game.execute("PRAGMA foreign_key_check")) - fk_before)
for table in tables:
    assert before[table] <= rows(game, table), "Existing rows changed: " + table
assert game.execute("SELECT InheritFrom FROM Leaders WHERE LeaderType='LEADER_SPC_TEST'").fetchone() == ("LEADER_DEFAULT",)
assert game.execute("SELECT TraitType FROM CivilizationTraits WHERE CivilizationType='CIVILIZATION_SPC_TEST'").fetchall() == [("TRAIT_CIVILIZATION_SPC_TEST",)]
assert game.execute("SELECT * FROM LeaderTraits WHERE LeaderType='LEADER_SPC_TEST'").fetchall() == []
assert game.execute("SELECT count(*) FROM TraitModifiers WHERE TraitType='TRAIT_CIVILIZATION_SPC_TEST'").fetchone()[0] == 6
assert game.execute("SELECT count(*) FROM TraitModifiers WHERE ModifierId LIKE 'SPC_P0_GOV_%' AND TraitType!='TRAIT_CIVILIZATION_SPC_TEST'").fetchone()[0] == 0
for n in (2, 3, 4):
    args = dict(game.execute("SELECT Name,Value FROM RequirementArguments WHERE RequirementId=?", (f"SPC_P0_GOV_{n}",)))
    assert args == {"Amount": str(n), "Established": "1"}
    assert game.execute("SELECT Permanent FROM Modifiers WHERE ModifierId=?", (f"SPC_P0_GOV_{n}_MOD",)).fetchone()[0] == 0

for suffix, established in [("PRESENT", "0"), ("ESTABLISHED", "1")]:
    rid="SPC_P0_GOV_"+suffix
    assert game.execute("SELECT RequirementType FROM Requirements WHERE RequirementId=?", (rid,)).fetchone()==("REQUIREMENT_CITY_HAS_GOVERNOR",)
    assert dict(game.execute("SELECT Name,Value FROM RequirementArguments WHERE RequirementId=?",(rid,)))=={"Established":established}
assert game.execute("SELECT SubjectRequirementSetId,Permanent FROM Modifiers WHERE ModifierId='SPC_P0_GOV_CONTROL_MOD'").fetchone()==(None,0)
assert dict(game.execute("SELECT Name,Value FROM ModifierArguments WHERE ModifierId='SPC_P0_GOV_CONTROL_MOD'"))=={"Key":"SPC_P0_GOV_CONTROL_A007","Amount":"1"}

config = database("DebugConfiguration.sqlite")
config_before = rows(config, "Players")
apply(config, "Config/Players.sql")
assert config_before <= rows(config, "Players")
assert config.execute("SELECT Domain,LeaderType FROM Players WHERE CivilizationType='CIVILIZATION_SPC_TEST'").fetchall() == [("Players:Expansion2_Players", "LEADER_SPC_TEST")]
assert config.execute("SELECT * FROM PlayerItems WHERE CivilizationType='CIVILIZATION_SPC_TEST'").fetchall() == []

# Add the official Scotland frontend row in a second isolated fixture where it was
# absent in the cache; show the added test identity leaves that row byte-for-byte intact.
official = ET.parse(xp / "Config/Expansion1_Players.xml")
scotland = next(r.attrib for r in official.findall("./Players/Row")
    if r.attrib.get("CivilizationType") == "CIVILIZATION_SCOTLAND" and r.attrib["Domain"] == "Players:Expansion2_Players")
if not config.execute("SELECT 1 FROM Players WHERE CivilizationType='CIVILIZATION_SCOTLAND' AND Domain='Players:Expansion2_Players'").fetchone():
    cols = list(scotland)
    config.execute("INSERT INTO Players (" + ','.join(cols) + ") VALUES (" + ','.join('?' for _ in cols) + ")", [scotland[k] for k in cols])
assert config.execute("SELECT count(*) FROM Players WHERE Domain='Players:Expansion2_Players' AND CivilizationType IN ('CIVILIZATION_SCOTLAND','CIVILIZATION_SPC_TEST')").fetchone()[0] == 2

loc = database("DebugLocalization.sqlite")
apply(loc, "Text/TestText.sql")
for lang in ("en_US", "zh_Hans_CN"):
    assert loc.execute("SELECT Text FROM LocalizedText WHERE Language=? AND Tag='LOC_SPC_CIV_NAME'", (lang,)).fetchone()[0] == "Scotland (Specialization Test)"
    assert loc.execute("SELECT Text FROM LocalizedText WHERE Language=? AND Tag='LOC_SPC_LEADER_NAME'", (lang,)).fetchone()[0] == "Robert the Bruce (Test)"
    assert all("Test" in r[0] for r in loc.execute("SELECT Text FROM LocalizedText WHERE Language=? AND Tag LIKE 'LOC_SPC_%'", (lang,)))

icons = sqlite3.connect(":memory:")
icons.execute('CREATE TABLE IconDefinitions (Name TEXT PRIMARY KEY, Atlas TEXT, "Index" INTEGER)')
apply(icons, "Data/Icons.sql")
for file, old, new in [("Data/Expansion1_Icons_Civilizations.xml", "ICON_CIVILIZATION_SCOTLAND", "ICON_CIVILIZATION_SPC_TEST"),
                       ("Data/Expansion1_Icons_Leaders.xml", "ICON_LEADER_ROBERT_THE_BRUCE", "ICON_LEADER_SPC_TEST")]:
    original = next(r.attrib for r in ET.parse(xp / file).iter("Row") if r.attrib.get("Name") == old)
    assert icons.execute('SELECT Atlas,"Index" FROM IconDefinitions WHERE Name=?', (new,)).fetchone() == (original["Atlas"], int(original["Index"]))
    assert any(r.attrib.get("Name") == original["Atlas"] for r in ET.parse(xp / file).iter("Row")), "Atlas definition absent"

loading = next(r.attrib for r in ET.parse(xp / "Data/Expansion1_LoadingInfo.xml").iter("Row") if r.attrib.get("LeaderType") == "LEADER_ROBERT_THE_BRUCE")
assert game.execute("SELECT ForegroundImage,BackgroundImage FROM LoadingInfo WHERE LeaderType='LEADER_SPC_TEST'").fetchone() == (loading["ForegroundImage"], loading["BackgroundImage"])
color_before = rows(game, "PlayerColors")
apply(game, "Data/Colors.sql")
assert color_before <= rows(game, "PlayerColors")
color_row = next(r for r in ET.parse(xp / "Data/Expansion1_PlayerColors.xml").iter("Row") if r.findtext("Type") == "LEADER_ROBERT_THE_BRUCE")
assert game.execute("SELECT PrimaryColor,SecondaryColor FROM PlayerColors WHERE Type='LEADER_SPC_TEST'").fetchone() == (color_row.findtext("PrimaryColor"), color_row.findtext("SecondaryColor"))

manifest = ET.parse(mod / "SpecializationP0.modinfo")
for stage in ("FrontEndActions", "InGameActions"):
    assert manifest.find(f"./{stage}/UpdateDatabase") is not None
    assert manifest.find(f"./{stage}/UpdateText") is not None
    assert manifest.find(f"./{stage}/UpdateIcons") is not None
    assert manifest.find(f"./{stage}/UpdateColors") is not None
for node in manifest.findall("./Files/File"):
    assert (mod / node.text).is_file()

print("STATIC_CONFIRMED: SQL parses against cached schema; no new foreign-key violations; existing rows preserved; independent IDs/traits; native icons/loading/color references match official Scotland XML; both languages and both manifest stages wired.")
print("LOCAL_SIMULATION_PASS: isolated SQLite execution. Make_Hash is a stub, icon schema is a minimal fixture. Actual selection, art rendering, game initialization and save identity: USER_GAME_TEST_REQUIRED.")
