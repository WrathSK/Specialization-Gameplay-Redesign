-- B184 dedicated, non-trainable probe; no ordinary Spy/operation/global changes.
INSERT INTO Types(Type,Kind) VALUES('UNIT_SPC_EXPEDITION_SPY','KIND_UNIT');
INSERT INTO Units(UnitType,Name,Description,BaseSightRange,BaseMoves,Domain,FormationClass,
 Cost,CanTrain,CanCapture,CanRetreatWhenCaptured,CanEarnExperience,Spy,ZoneOfControl,IgnoreMoves,Stackable,PromotionClass)
VALUES('UNIT_SPC_EXPEDITION_SPY','LOC_SPC_EXPEDITION_SPY_NAME','LOC_SPC_EXPEDITION_SPY_DESCRIPTION',
 2,4,'DOMAIN_LAND','FORMATION_CLASS_CIVILIAN',1,0,0,0,0,1,0,1,1,'PROMOTION_CLASS_SPY');
-- No CLASS_SPY association or Spy ability/promotion grant. PromotionClass alone
-- supplies the native shell's classification; isolation remains a native gate.
INSERT INTO TypeTags(Type,Tag) VALUES('UNIT_SPC_EXPEDITION_SPY','CLASS_LANDCIVILIAN');
