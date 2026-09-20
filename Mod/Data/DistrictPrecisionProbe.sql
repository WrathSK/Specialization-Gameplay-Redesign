-- B082 isolated district precision probe. No trait/automatic attachment.
-- Direct Campus replacements share the test predicate. No balance/ability cutover.
INSERT INTO RequirementSets(RequirementSetId,RequirementSetType) VALUES ('SPC_B082_CAMPUS','REQUIREMENTSET_TEST_ANY');
INSERT INTO Requirements(RequirementId,RequirementType)
SELECT 'SPC_B082_' || DistrictType,'REQUIREMENT_DISTRICT_TYPE_MATCHES' FROM Districts
WHERE DistrictType='DISTRICT_CAMPUS' OR DistrictType IN (SELECT CivUniqueDistrictType FROM DistrictReplaces WHERE ReplacesDistrictType='DISTRICT_CAMPUS');
INSERT INTO RequirementArguments(RequirementId,Name,Value)
SELECT 'SPC_B082_' || DistrictType,'DistrictType',DistrictType FROM Districts
WHERE DistrictType='DISTRICT_CAMPUS' OR DistrictType IN (SELECT CivUniqueDistrictType FROM DistrictReplaces WHERE ReplacesDistrictType='DISTRICT_CAMPUS');
INSERT INTO RequirementSetRequirements(RequirementSetId,RequirementId)
SELECT 'SPC_B082_CAMPUS',RequirementId FROM Requirements WHERE RequirementId LIKE 'SPC_B082_DISTRICT_%';
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_B082_DISTRICT_03','KIND_BUILDING');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing) VALUES ('BUILDING_SPC_B082_DISTRICT_03','District precision experiment (internal)',1,'DISTRICT_CITY_CENTER',1,0,0);
INSERT INTO Modifiers(ModifierId,ModifierType,SubjectRequirementSetId) VALUES ('SPC_B082_DISTRICT_03','MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE','SPC_B082_CAMPUS');
INSERT INTO ModifierArguments(ModifierId,Name,Value) VALUES ('SPC_B082_DISTRICT_03','YieldType','YIELD_SCIENCE'),('SPC_B082_DISTRICT_03','Amount','0.3');
INSERT INTO BuildingModifiers(BuildingType,ModifierId) VALUES ('BUILDING_SPC_B082_DISTRICT_03','SPC_B082_DISTRICT_03');
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_B082_DISTRICT_05','KIND_BUILDING');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing) VALUES ('BUILDING_SPC_B082_DISTRICT_05','District precision experiment (internal)',1,'DISTRICT_CITY_CENTER',1,0,0);
INSERT INTO Modifiers(ModifierId,ModifierType,SubjectRequirementSetId) VALUES ('SPC_B082_DISTRICT_05','MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE','SPC_B082_CAMPUS');
INSERT INTO ModifierArguments(ModifierId,Name,Value) VALUES ('SPC_B082_DISTRICT_05','YieldType','YIELD_SCIENCE'),('SPC_B082_DISTRICT_05','Amount','0.5');
INSERT INTO BuildingModifiers(BuildingType,ModifierId) VALUES ('BUILDING_SPC_B082_DISTRICT_05','SPC_B082_DISTRICT_05');
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_B082_DISTRICT_1','KIND_BUILDING');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing) VALUES ('BUILDING_SPC_B082_DISTRICT_1','District precision experiment (internal)',1,'DISTRICT_CITY_CENTER',1,0,0);
INSERT INTO Modifiers(ModifierId,ModifierType,SubjectRequirementSetId) VALUES ('SPC_B082_DISTRICT_1','MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE','SPC_B082_CAMPUS');
INSERT INTO ModifierArguments(ModifierId,Name,Value) VALUES ('SPC_B082_DISTRICT_1','YieldType','YIELD_SCIENCE'),('SPC_B082_DISTRICT_1','Amount','1');
INSERT INTO BuildingModifiers(BuildingType,ModifierId) VALUES ('BUILDING_SPC_B082_DISTRICT_1','SPC_B082_DISTRICT_1');
