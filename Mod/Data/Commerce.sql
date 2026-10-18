-- B239: transient base Gold after the accepted per-domain Floor; never historical state.
CREATE TABLE SPC_CommerceGold(Bit INTEGER PRIMARY KEY,Amount INTEGER NOT NULL,CarrierType TEXT NOT NULL UNIQUE);
WITH RECURSIVE Bits(Bit,Amount) AS (SELECT 0,1 UNION ALL SELECT Bit+1,Amount*2 FROM Bits WHERE Bit<30)
INSERT INTO SPC_CommerceGold SELECT Bit,Amount,'BUILDING_SPC_COMMERCE_GOLD_'||Bit FROM Bits;
INSERT INTO Types(Type,Kind) SELECT CarrierType,'KIND_BUILDING' FROM SPC_CommerceGold;
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 SELECT CarrierType,'Commercialization owned Gold',1,'DISTRICT_CITY_CENTER',1,0,0 FROM SPC_CommerceGold;
INSERT INTO Modifiers(ModifierId,ModifierType) SELECT CarrierType,'MODIFIER_SINGLE_CITY_ADJUST_YIELD_CHANGE' FROM SPC_CommerceGold;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'YieldType','YIELD_GOLD' FROM SPC_CommerceGold;
INSERT INTO ModifierArguments(ModifierId,Name,Value) SELECT CarrierType,'Amount',Amount FROM SPC_CommerceGold;
INSERT INTO BuildingModifiers(BuildingType,ModifierId) SELECT CarrierType,CarrierType FROM SPC_CommerceGold;
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_COMMERCIALIZATION_ACCESS','KIND_BUILDING'),('PROJECT_SPC_COMMERCIALIZATION','KIND_PROJECT');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 VALUES ('BUILDING_SPC_COMMERCIALIZATION_ACCESS','LOC_SPC_COMMERCE_TITLE',1,'DISTRICT_CITY_CENTER',1,0,0);
-- The UI intercepts this configuration opener before native enqueue.
INSERT INTO Projects(ProjectType,Name,ShortName,Description,Cost,CostProgressionModel,PrereqDistrict,RequiredBuilding)
 VALUES ('PROJECT_SPC_COMMERCIALIZATION','LOC_SPC_COMMERCE_TITLE','LOC_SPC_COMMERCE_TITLE','LOC_SPC_COMMERCE_OPEN_HELP',1,'NO_PROGRESSION_MODEL','DISTRICT_CITY_CENTER','BUILDING_SPC_COMMERCIALIZATION_ACCESS');
