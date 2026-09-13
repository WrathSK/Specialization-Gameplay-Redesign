-- B044 fixed denomination units. No regular training/purchase.
INSERT INTO Types(Type,Kind) VALUES ('UNIT_SPC_CREW_250','KIND_UNIT');
INSERT INTO Units(UnitType,Name,Description,BaseSightRange,BaseMoves,Domain,FormationClass,Cost,CanTrain,CanCapture,BuildCharges,CanEarnExperience)
VALUES('UNIT_SPC_CREW_250','LOC_UNIT_SPC_CREW_250_NAME','LOC_UNIT_SPC_CREW_250_DESCRIPTION',2,2,'DOMAIN_LAND','FORMATION_CLASS_CIVILIAN',280,0,0,1,0);
-- Intentionally no CLASS_BUILDER, Improvement_ValidBuildUnits, purchase yield or replacement.

INSERT INTO Types(Type,Kind) VALUES ('UNIT_SPC_CREW_420','KIND_UNIT');
INSERT INTO Units(UnitType,Name,Description,BaseSightRange,BaseMoves,Domain,FormationClass,Cost,CanTrain,CanCapture,BuildCharges,CanEarnExperience) VALUES ('UNIT_SPC_CREW_420','LOC_UNIT_SPC_CREW_420_NAME','LOC_UNIT_SPC_CREW_420_DESCRIPTION',2,2,'DOMAIN_LAND','FORMATION_CLASS_CIVILIAN',460,0,0,1,0);

INSERT INTO Types(Type,Kind) VALUES ('UNIT_SPC_CREW_750','KIND_UNIT');
INSERT INTO Units(UnitType,Name,Description,BaseSightRange,BaseMoves,Domain,FormationClass,Cost,CanTrain,CanCapture,BuildCharges,CanEarnExperience) VALUES ('UNIT_SPC_CREW_750','LOC_UNIT_SPC_CREW_750_NAME','LOC_UNIT_SPC_CREW_750_DESCRIPTION',2,2,'DOMAIN_LAND','FORMATION_CLASS_CIVILIAN',820,0,0,1,0);

INSERT INTO Types(Type,Kind) VALUES ('UNIT_SPC_CREW_1000','KIND_UNIT');
INSERT INTO Units(UnitType,Name,Description,BaseSightRange,BaseMoves,Domain,FormationClass,Cost,CanTrain,CanCapture,BuildCharges,CanEarnExperience) VALUES ('UNIT_SPC_CREW_1000','LOC_UNIT_SPC_CREW_1000_NAME','LOC_UNIT_SPC_CREW_1000_DESCRIPTION',2,2,'DOMAIN_LAND','FORMATION_CLASS_CIVILIAN',1100,0,0,1,0);

INSERT INTO Types(Type,Kind) VALUES ('UNIT_SPC_CREW_1360','KIND_UNIT');
INSERT INTO Units(UnitType,Name,Description,BaseSightRange,BaseMoves,Domain,FormationClass,Cost,CanTrain,CanCapture,BuildCharges,CanEarnExperience) VALUES ('UNIT_SPC_CREW_1360','LOC_UNIT_SPC_CREW_1360_NAME','LOC_UNIT_SPC_CREW_1360_DESCRIPTION',2,2,'DOMAIN_LAND','FORMATION_CLASS_CIVILIAN',1500,0,0,1,0);
