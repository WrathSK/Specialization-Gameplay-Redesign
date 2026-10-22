-- B118 disposable primitive fixture. Finite cost is not an infinite sink guarantee.
INSERT INTO Types(Type,Kind) VALUES ('PROJECT_SPC_OVERFLOW_SINK_TEST','KIND_PROJECT');
INSERT INTO Projects(ProjectType,Name,ShortName,Description,Cost,CostProgressionModel,PrereqDistrict)
VALUES ('PROJECT_SPC_OVERFLOW_SINK_TEST','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_NAME','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_NAME','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_DESCRIPTION',1000000,'NO_PROGRESSION_MODEL','DISTRICT_CITY_CENTER');
-- No completion modifiers, conversions, GPP, unlock effects or rewards.

-- B267: retain prototype definitions/readers but never grant ordinary availability.
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_OVERFLOW_TEST_DISABLED','KIND_BUILDING');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
VALUES ('BUILDING_SPC_OVERFLOW_TEST_DISABLED','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_NAME',1,'DISTRICT_CITY_CENTER',1,0,0);
UPDATE Projects SET RequiredBuilding='BUILDING_SPC_OVERFLOW_TEST_DISABLED'
WHERE ProjectType='PROJECT_SPC_OVERFLOW_SINK_TEST';
