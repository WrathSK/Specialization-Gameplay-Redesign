-- B234: III baseline, specific legal production targets only. No purchase effect,
-- unlock, progress injection, Wonder target or permanent L value.
CREATE TABLE SPC_StandardizationTargets(Kind TEXT NOT NULL, TargetType TEXT NOT NULL,
 CarrierType TEXT NOT NULL UNIQUE, PRIMARY KEY(Kind,TargetType));
INSERT INTO SPC_StandardizationTargets
 SELECT DISTINCT 'BUILDING',BuildingType,'BUILDING_SPC_STD_BASE_B_'||BuildingType FROM SPC_B054_Targets;
WITH RECURSIVE Bases(TargetType,BaseType) AS (
 SELECT DistrictType,DistrictType FROM Districts WHERE InternalOnly=0
 UNION
 SELECT b.TargetType,r.ReplacesDistrictType FROM Bases b
 JOIN DistrictReplaces r ON r.CivUniqueDistrictType=b.BaseType
)
INSERT INTO SPC_StandardizationTargets
 SELECT 'DISTRICT',TargetType,'BUILDING_SPC_STD_BASE_D_'||TargetType FROM Bases b
 WHERE NOT EXISTS(SELECT 1 FROM DistrictReplaces r WHERE r.CivUniqueDistrictType=b.BaseType)
 AND BaseType IN ('DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE','DISTRICT_COMMERCIAL_HUB',
 'DISTRICT_ENCAMPMENT','DISTRICT_HARBOR','DISTRICT_HOLY_SITE','DISTRICT_AERODROME','DISTRICT_AQUEDUCT',
 'DISTRICT_DAM','DISTRICT_NEIGHBORHOOD','DISTRICT_ENTERTAINMENT_COMPLEX','DISTRICT_WATER_ENTERTAINMENT_COMPLEX',
 'DISTRICT_PRESERVE','DISTRICT_DIPLOMATIC_QUARTER');
INSERT INTO Types(Type,Kind) SELECT CarrierType,'KIND_BUILDING' FROM SPC_StandardizationTargets;
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 SELECT CarrierType,'Standardization construction carrier',1,'DISTRICT_CITY_CENTER',1,0,0 FROM SPC_StandardizationTargets;
INSERT INTO Modifiers(ModifierId,ModifierType)
 SELECT CarrierType,CASE Kind WHEN 'BUILDING' THEN 'MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION'
 ELSE 'MODIFIER_SINGLE_CITY_ADJUST_DISTRICT_PRODUCTION' END FROM SPC_StandardizationTargets;
INSERT INTO ModifierArguments(ModifierId,Name,Value)
 SELECT CarrierType,CASE Kind WHEN 'BUILDING' THEN 'BuildingType' ELSE 'DistrictType' END,TargetType FROM SPC_StandardizationTargets;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'Amount',10 FROM SPC_StandardizationTargets;
INSERT INTO BuildingModifiers(BuildingType,ModifierId) SELECT CarrierType,CarrierType FROM SPC_StandardizationTargets;
