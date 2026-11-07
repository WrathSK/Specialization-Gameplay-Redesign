-- B246: independent district-building Production owner. No purchase or yield modifier.
CREATE TABLE SPC_DevelopmentEffects(DistrictType TEXT PRIMARY KEY, CarrierType TEXT NOT NULL UNIQUE);
INSERT INTO SPC_DevelopmentEffects
 SELECT DISTINCT b.PrereqDistrict,'BUILDING_SPC_DEVELOPMENT_'||b.PrereqDistrict
 FROM SPC_EnvironmentBuildings e JOIN Buildings b ON b.BuildingType=e.BuildingType
 WHERE b.MustPurchase=0 AND EXISTS (SELECT 1 FROM SPC_EnvironmentAssembly);
INSERT INTO Types(Type,Kind) SELECT CarrierType,'KIND_BUILDING' FROM SPC_DevelopmentEffects;
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 SELECT CarrierType,'Development Investment owned Production',1,'DISTRICT_CITY_CENTER',1,0,0 FROM SPC_DevelopmentEffects;
INSERT INTO Modifiers(ModifierId,ModifierType) SELECT CarrierType,'MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION' FROM SPC_DevelopmentEffects;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'DistrictType',DistrictType FROM SPC_DevelopmentEffects;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'Amount',50 FROM SPC_DevelopmentEffects;
INSERT INTO BuildingModifiers(BuildingType,ModifierId) SELECT CarrierType,CarrierType FROM SPC_DevelopmentEffects;
