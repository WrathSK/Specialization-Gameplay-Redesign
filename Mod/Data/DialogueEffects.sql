-- B177: all reachable earned totals, one Tourism-only final carrier per city.
-- Game Era quota (once each) * at most seven collection eras * five points.
CREATE TABLE SPC_DialogueTotals (Bonus INTEGER PRIMARY KEY);
INSERT INTO SPC_DialogueTotals WITH RECURSIVE values_(n) AS (
 SELECT 5 WHERE (SELECT COUNT(*) FROM Eras)>0
 UNION ALL SELECT n+5 FROM values_ WHERE n<35*(SELECT COUNT(*) FROM Eras)
) SELECT n FROM values_;
CREATE TEMP TABLE SPC_DialogueKinds (Kind TEXT PRIMARY KEY);
INSERT INTO SPC_DialogueKinds VALUES ('WRITING'),('MUSIC'),('SCULPTURE'),('PORTRAIT'),('LANDSCAPE'),('RELIGIOUS'),('ARTIFACT');
INSERT INTO Types(Type,Kind) SELECT 'BUILDING_SPC_DIALOGUE_TOTAL_'||Bonus,'KIND_BUILDING' FROM SPC_DialogueTotals;
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 SELECT 'BUILDING_SPC_DIALOGUE_TOTAL_'||Bonus,'LOC_SPC_DIALOGUE_PROJECT_REPORT',1,'DISTRICT_CITY_CENTER',1,0,0 FROM SPC_DialogueTotals;
INSERT INTO Modifiers(ModifierId,ModifierType)
 SELECT 'SPC_DIALOGUE_TOTAL_'||Bonus||'_'||Kind,'MODIFIER_SINGLE_CITY_ADJUST_TOURISM' FROM SPC_DialogueTotals CROSS JOIN SPC_DialogueKinds;
INSERT INTO ModifierArguments(ModifierId,Name,Value)
 SELECT 'SPC_DIALOGUE_TOTAL_'||Bonus||'_'||Kind,'GreatWorkObjectType','GREATWORKOBJECT_'||Kind FROM SPC_DialogueTotals CROSS JOIN SPC_DialogueKinds;
INSERT INTO ModifierArguments(ModifierId,Name,Value)
 SELECT 'SPC_DIALOGUE_TOTAL_'||Bonus||'_'||Kind,'ScalingFactor',100+Bonus FROM SPC_DialogueTotals CROSS JOIN SPC_DialogueKinds;
INSERT INTO BuildingModifiers(BuildingType,ModifierId)
 SELECT 'BUILDING_SPC_DIALOGUE_TOTAL_'||Bonus,'SPC_DIALOGUE_TOTAL_'||Bonus||'_'||Kind FROM SPC_DialogueTotals CROSS JOIN SPC_DialogueKinds;
DROP TABLE SPC_DialogueKinds;
