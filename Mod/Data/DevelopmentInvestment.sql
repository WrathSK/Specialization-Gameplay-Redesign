-- B246: independent district-building Production owner. No purchase or yield modifier.
CREATE TABLE SPC_DevelopmentEffects(DistrictType TEXT PRIMARY KEY, CarrierType TEXT NOT NULL UNIQUE);
INSERT INTO SPC_DevelopmentEffects
 SELECT DISTINCT b.PrereqDistrict,'BUILDING_SPC_DEVELOPMENT_'||b.PrereqDistrict
 FROM Buildings b JOIN HD_BuildingTiers h ON b.BuildingType=h.BuildingType
 WHERE b.InternalOnly=0 AND b.IsWonder=0 AND b.MustPurchase=0
 AND NOT EXISTS(SELECT 1 FROM HD_DUMMY_BUILDINGS d WHERE d.BuildingType=b.BuildingType);
INSERT INTO Types(Type,Kind) SELECT CarrierType,'KIND_BUILDING' FROM SPC_DevelopmentEffects;
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 SELECT CarrierType,'Development Investment owned Production',1,'DISTRICT_CITY_CENTER',1,0,0 FROM SPC_DevelopmentEffects;
INSERT INTO Modifiers(ModifierId,ModifierType) SELECT CarrierType,'MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION' FROM SPC_DevelopmentEffects;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'DistrictType',DistrictType FROM SPC_DevelopmentEffects;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'Amount',50 FROM SPC_DevelopmentEffects;
INSERT INTO BuildingModifiers(BuildingType,ModifierId) SELECT CarrierType,CarrierType FROM SPC_DevelopmentEffects;
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_DEVELOPMENT_ACCESS','KIND_BUILDING'),('PROJECT_SPC_DEVELOPMENT_INVESTMENT','KIND_PROJECT');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 VALUES ('BUILDING_SPC_DEVELOPMENT_ACCESS','LOC_SPC_DEVELOPMENT_TITLE',1,'DISTRICT_CITY_CENTER',1,0,0);
INSERT INTO Projects(ProjectType,Name,ShortName,Description,Cost,CostProgressionModel,PrereqDistrict,RequiredBuilding)
 VALUES ('PROJECT_SPC_DEVELOPMENT_INVESTMENT','LOC_SPC_DEVELOPMENT_TITLE','LOC_SPC_DEVELOPMENT_TITLE','LOC_SPC_DEVELOPMENT_OPEN_HELP',1,'NO_PROGRESSION_MODEL','DISTRICT_CITY_CENTER','BUILDING_SPC_DEVELOPMENT_ACCESS');
