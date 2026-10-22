-- B235: normal full-turn study, transient access only; Store owns history.
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_ENGINEERING_STUDY_ACCESS','KIND_BUILDING'),('PROJECT_SPC_ENGINEERING_STUDY','KIND_PROJECT');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 VALUES ('BUILDING_SPC_ENGINEERING_STUDY_ACCESS','LOC_PROJECT_SPC_ENGINEERING_STUDY_NAME',1,'DISTRICT_CITY_CENTER',1,0,0);
INSERT INTO Projects(ProjectType,Name,ShortName,Description,Cost,CostProgressionModel,PrereqDistrict,RequiredBuilding)
 VALUES ('PROJECT_SPC_ENGINEERING_STUDY','LOC_PROJECT_SPC_ENGINEERING_STUDY_NAME','LOC_PROJECT_SPC_ENGINEERING_STUDY_NAME','LOC_PROJECT_SPC_ENGINEERING_STUDY_DESCRIPTION',1000000,'NO_PROGRESSION_MODEL','DISTRICT_CITY_CENTER','BUILDING_SPC_ENGINEERING_STUDY_ACCESS');
-- A single final-value carrier per target, not a stack of percentage pieces.
-- Values derive from the loaded era catalog (the maximum possible distinct E),
-- not a five-layer gameplay cap. Saved L is never clamped to this definition set.
CREATE TABLE SPC_StandardizationLevels(Kind TEXT NOT NULL,TargetType TEXT NOT NULL,Level INTEGER NOT NULL,
 CarrierType TEXT NOT NULL UNIQUE,PRIMARY KEY(Kind,TargetType,Level));
WITH RECURSIVE Levels(L) AS (SELECT 1 UNION ALL SELECT L+1 FROM Levels WHERE L<(SELECT COUNT(*) FROM Eras))
INSERT INTO SPC_StandardizationLevels SELECT t.Kind,t.TargetType,L,t.CarrierType||'_L' ||L FROM SPC_StandardizationTargets t CROSS JOIN Levels;
INSERT INTO Types(Type,Kind) SELECT CarrierType,'KIND_BUILDING' FROM SPC_StandardizationLevels;
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 SELECT CarrierType,'Standardization final-value carrier',1,'DISTRICT_CITY_CENTER',1,0,0 FROM SPC_StandardizationLevels;
INSERT INTO Modifiers(ModifierId,ModifierType) SELECT CarrierType,CASE Kind WHEN 'BUILDING' THEN 'MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION' ELSE 'MODIFIER_SINGLE_CITY_ADJUST_DISTRICT_PRODUCTION' END FROM SPC_StandardizationLevels;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,CASE Kind WHEN 'BUILDING' THEN 'BuildingType' ELSE 'DistrictType' END,TargetType FROM SPC_StandardizationLevels;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'Amount',10+2*Level FROM SPC_StandardizationLevels;
INSERT INTO BuildingModifiers(BuildingType,ModifierId) SELECT CarrierType,CarrierType FROM SPC_StandardizationLevels;
-- Existing target-specific native building cost effect applies only where purchase
-- is already legal. No CAN_PURCHASE/CAN_FAITH_PURCHASE permissions are introduced.
INSERT INTO Modifiers(ModifierId,ModifierType) SELECT CarrierType||'_PURCHASE','MODIFIER_CITY_ADJUST_BUILDING_PURCHASE_COST' FROM SPC_StandardizationLevels WHERE Kind='BUILDING';
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType||'_PURCHASE','BuildingType',TargetType FROM SPC_StandardizationLevels WHERE Kind='BUILDING';
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType||'_PURCHASE','Amount',2*Level FROM SPC_StandardizationLevels WHERE Kind='BUILDING';
INSERT INTO BuildingModifiers(BuildingType,ModifierId) SELECT CarrierType,CarrierType||'_PURCHASE' FROM SPC_StandardizationLevels WHERE Kind='BUILDING';
-- No all-district purchase substitute: a per-template district purchase primitive
-- has not been established. The construction writer remains exact and available.
CREATE TABLE SPC_IndustryWonderEffects(EraType TEXT NOT NULL,Amount INTEGER NOT NULL,CarrierType TEXT NOT NULL UNIQUE,PRIMARY KEY(EraType,Amount));
INSERT INTO SPC_IndustryWonderEffects SELECT EraType,Amount,'BUILDING_SPC_WONDER_'||EraType||'_'||Amount FROM Eras CROSS JOIN (SELECT 10 Amount UNION ALL SELECT 20 UNION ALL SELECT 30);
INSERT INTO Types(Type,Kind) SELECT CarrierType,'KIND_BUILDING' FROM SPC_IndustryWonderEffects;
INSERT INTO Types(Type,Kind) VALUES ('MODIFIER_SPC_CITY_WONDER_ERA_PRODUCTION','KIND_MODIFIER');
INSERT INTO DynamicModifiers(ModifierType,CollectionType,EffectType) VALUES ('MODIFIER_SPC_CITY_WONDER_ERA_PRODUCTION','COLLECTION_OWNER','EFFECT_ADJUST_WONDER_ERA_PRODUCTION');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 SELECT CarrierType,'Industry Wonder era carrier',1,'DISTRICT_CITY_CENTER',1,0,0 FROM SPC_IndustryWonderEffects;
INSERT INTO Modifiers(ModifierId,ModifierType) SELECT CarrierType,'MODIFIER_SPC_CITY_WONDER_ERA_PRODUCTION' FROM SPC_IndustryWonderEffects;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'Amount',Amount FROM SPC_IndustryWonderEffects;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'StartEra',EraType FROM SPC_IndustryWonderEffects;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'EndEra',EraType FROM SPC_IndustryWonderEffects;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'IsWonder',1 FROM SPC_IndustryWonderEffects;
INSERT INTO BuildingModifiers(BuildingType,ModifierId) SELECT CarrierType,CarrierType FROM SPC_IndustryWonderEffects;
