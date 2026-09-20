-- P0-D3: local building-specific Science; never citizen/flat city compensation.
CREATE TABLE IF NOT EXISTS SPC_ResearchChairTargets(BuildingType TEXT PRIMARY KEY);
INSERT INTO SPC_ResearchChairTargets(BuildingType)
SELECT BuildingType FROM Buildings WHERE BuildingType IN ('BUILDING_HD_DATA_CENTER','BUILDING_JNR_ACADEMY','BUILDING_JNR_ARCHITECTURE','BUILDING_JNR_EDUCATION','BUILDING_JNR_LABORATORY','BUILDING_JNR_LIBERAL_ARTS','BUILDING_JNR_REAL_ACADEMY','BUILDING_JNR_SCHOOL','BUILDING_LIBRARY','BUILDING_MADRASA','BUILDING_NAVIGATION_SCHOOL','BUILDING_RESEARCH_LAB','BUILDING_UNIVERSITY');
CREATE TEMP TABLE SPC_ChairBits(Bit INTEGER,Amount INTEGER);
INSERT INTO SPC_ChairBits VALUES (0,1),(1,2),(2,4),(3,8),(4,16),(5,32),(6,64),(7,128);
INSERT INTO Types(Type,Kind)
SELECT 'BUILDING_SPC_RESEARCH_CHAIR_'||t.BuildingType||'_'||b.Bit,'KIND_BUILDING' FROM SPC_ResearchChairTargets t CROSS JOIN SPC_ChairBits b;
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
SELECT 'BUILDING_SPC_RESEARCH_CHAIR_'||t.BuildingType||'_'||b.Bit,'Research Chair (internal)',1,'DISTRICT_CAMPUS',1,0,0 FROM SPC_ResearchChairTargets t CROSS JOIN SPC_ChairBits b;
INSERT INTO Modifiers(ModifierId,ModifierType)
SELECT 'SPC_RESEARCH_CHAIR_'||t.BuildingType||'_'||b.Bit,'MODIFIER_BUILDING_YIELD_CHANGE' FROM SPC_ResearchChairTargets t CROSS JOIN SPC_ChairBits b;
INSERT INTO ModifierArguments(ModifierId,Name,Value)
SELECT 'SPC_RESEARCH_CHAIR_'||t.BuildingType||'_'||b.Bit,'BuildingType',t.BuildingType FROM SPC_ResearchChairTargets t CROSS JOIN SPC_ChairBits b;
INSERT INTO ModifierArguments(ModifierId,Name,Value)
SELECT 'SPC_RESEARCH_CHAIR_'||t.BuildingType||'_'||b.Bit,'YieldType','YIELD_SCIENCE' FROM SPC_ResearchChairTargets t CROSS JOIN SPC_ChairBits b;
INSERT INTO ModifierArguments(ModifierId,Name,Value)
SELECT 'SPC_RESEARCH_CHAIR_'||t.BuildingType||'_'||b.Bit,'Amount',b.Amount FROM SPC_ResearchChairTargets t CROSS JOIN SPC_ChairBits b;
INSERT INTO BuildingModifiers(BuildingType,ModifierId)
SELECT 'BUILDING_SPC_RESEARCH_CHAIR_'||t.BuildingType||'_'||b.Bit,'SPC_RESEARCH_CHAIR_'||t.BuildingType||'_'||b.Bit FROM SPC_ResearchChairTargets t CROSS JOIN SPC_ChairBits b;
DROP TABLE SPC_ChairBits;
