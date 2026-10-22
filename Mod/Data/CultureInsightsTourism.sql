-- B216: one final city percentage; no stacking assumption and no saved derived bonus.
CREATE TEMP TABLE SPC_InsightTotals(N INTEGER PRIMARY KEY);
INSERT INTO SPC_InsightTotals WITH RECURSIVE totals(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM totals WHERE n<192) SELECT n FROM totals;
INSERT INTO Types(Type,Kind) SELECT 'BUILDING_SPC_INSIGHT_TOURISM_'||N,'KIND_BUILDING' FROM SPC_InsightTotals;
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 SELECT 'BUILDING_SPC_INSIGHT_TOURISM_'||N,'LOC_SPC_INSIGHT_TOURISM_NAME',1,'DISTRICT_CITY_CENTER',1,0,0 FROM SPC_InsightTotals;
INSERT INTO Modifiers(ModifierId,ModifierType) SELECT 'SPC_INSIGHT_TOURISM_'||N,'MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS' FROM SPC_InsightTotals;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT 'SPC_INSIGHT_TOURISM_'||N,'MinimumEra','ERA_ANCIENT' FROM SPC_InsightTotals;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT 'SPC_INSIGHT_TOURISM_'||N,'Modifier',2*N FROM SPC_InsightTotals;
INSERT INTO BuildingModifiers(BuildingType,ModifierId) SELECT 'BUILDING_SPC_INSIGHT_TOURISM_'||N,'SPC_INSIGHT_TOURISM_'||N FROM SPC_InsightTotals;
DROP TABLE SPC_InsightTotals;
