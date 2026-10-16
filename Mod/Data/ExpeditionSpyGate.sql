-- B184 dedicated, non-trainable probe; no ordinary Spy/operation/global changes.
INSERT INTO Types(Type,Kind) VALUES('UNIT_SPC_EXPEDITION_SPY','KIND_UNIT');
INSERT INTO Units(UnitType,Name,Description,BaseSightRange,BaseMoves,Domain,FormationClass,
 Cost,CanTrain,CanCapture,CanRetreatWhenCaptured,CanEarnExperience,Spy,ZoneOfControl,IgnoreMoves,Stackable,PromotionClass)
VALUES('UNIT_SPC_EXPEDITION_SPY','LOC_SPC_EXPEDITION_SPY_NAME','LOC_SPC_EXPEDITION_SPY_DESCRIPTION',
 2,4,'DOMAIN_LAND','FORMATION_CLASS_CIVILIAN',1,0,0,0,0,1,0,1,1,'PROMOTION_CLASS_SPY');
-- No CLASS_SPY association or Spy ability/promotion grant. PromotionClass alone
-- supplies the native shell's classification; isolation remains a native gate.
INSERT INTO TypeTags(Type,Tag) VALUES('UNIT_SPC_EXPEDITION_SPY','CLASS_LANDCIVILIAN');

-- B202: reuse the resolved Spy base cost. No ordinary Spy purchase or unlock inheritance.
-- B207 TEMPORARY DIAGNOSTIC EXPERIMENT (user-authorized, not a design decision):
-- fixed cost without previous-copy progression, to test whether the native
-- cost1 / population delta on creation comes from that progression.
UPDATE Units SET CanTrain=1,
 Cost=(SELECT Cost FROM Units WHERE UnitType='UNIT_SPY'),
 CostProgressionModel='NO_COST_PROGRESSION',
 CostProgressionParam1=0
 WHERE UnitType='UNIT_SPC_EXPEDITION_SPY';
INSERT INTO Types(Type,Kind) VALUES('BUILDING_SPC_EXPEDITION_TRAINING_ACCESS','KIND_BUILDING');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 VALUES('BUILDING_SPC_EXPEDITION_TRAINING_ACCESS','Expedition training reservation',1,'DISTRICT_CITY_CENTER',1,0,0);
INSERT INTO Unit_BuildingPrereqs(Unit,PrereqBuilding,NumSupported)
 VALUES('UNIT_SPC_EXPEDITION_SPY','BUILDING_SPC_EXPEDITION_TRAINING_ACCESS',1);
