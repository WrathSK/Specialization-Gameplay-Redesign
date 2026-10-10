-- B178 / N1 gate only. Not normal training, no Spy identity/operation/capacity.
-- Native archaeologists provide the non-Great-Person retreat-field precedent.
INSERT INTO Types(Type,Kind) VALUES('UNIT_SPC_EXPEDITION_GATE','KIND_UNIT');
INSERT INTO Units(UnitType,Name,Description,BaseSightRange,BaseMoves,Domain,FormationClass,
 Cost,CanTrain,CanCapture,CanRetreatWhenCaptured,CanEarnExperience,Spy,ZoneOfControl)
VALUES('UNIT_SPC_EXPEDITION_GATE','LOC_SPC_EXPEDITION_GATE_UNIT_NAME','LOC_SPC_EXPEDITION_GATE_DESCRIPTION',
 2,4,'DOMAIN_LAND','FORMATION_CLASS_CIVILIAN',1,0,0,1,0,0,0);
INSERT INTO TypeTags(Type,Tag) VALUES('UNIT_SPC_EXPEDITION_GATE','CLASS_LANDCIVILIAN');
