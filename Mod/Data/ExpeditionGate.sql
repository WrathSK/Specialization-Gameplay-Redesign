-- B178 / N1 gate only. Not normal training, no Spy identity/operation/capacity.
-- Native archaeologists provide the non-Great-Person retreat-field precedent.
INSERT INTO Types(Type,Kind) VALUES('UNIT_SPC_EXPEDITION_GATE','KIND_UNIT');
INSERT INTO Units(UnitType,Name,Description,BaseSightRange,BaseMoves,Domain,FormationClass,
 Cost,CanTrain,CanCapture,CanRetreatWhenCaptured,CanEarnExperience,Spy,ZoneOfControl)
VALUES('UNIT_SPC_EXPEDITION_GATE','LOC_SPC_EXPEDITION_GATE_UNIT_NAME','LOC_SPC_EXPEDITION_GATE_DESCRIPTION',
 2,4,'DOMAIN_LAND','FORMATION_CLASS_CIVILIAN',1,0,0,1,0,0,0);
INSERT INTO TypeTags(Type,Tag) VALUES('UNIT_SPC_EXPEDITION_GATE','CLASS_LANDCIVILIAN');

-- B182 separate fixture: retain the old retreat unit definition for old saves.
-- These independent fields are candidates, not a native immunity guarantee.
INSERT INTO Types(Type,Kind) VALUES('UNIT_SPC_EXPEDITION_ZERO','KIND_UNIT');
INSERT INTO Units(UnitType,Name,Description,BaseSightRange,BaseMoves,Domain,FormationClass,
 Cost,CanTrain,CanCapture,CanRetreatWhenCaptured,CanEarnExperience,Spy,ZoneOfControl,IgnoreMoves,Stackable)
VALUES('UNIT_SPC_EXPEDITION_ZERO','LOC_SPC_EXPEDITION_ZERO_NAME','LOC_SPC_EXPEDITION_ZERO_DESCRIPTION',
 2,4,'DOMAIN_LAND','FORMATION_CLASS_CIVILIAN',1,0,0,0,0,0,0,1,1);
INSERT INTO TypeTags(Type,Tag) VALUES('UNIT_SPC_EXPEDITION_ZERO','CLASS_LANDCIVILIAN');
