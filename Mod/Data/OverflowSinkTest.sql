-- B118 disposable primitive fixture. Finite cost is not an infinite sink guarantee.
INSERT INTO Types(Type,Kind) VALUES ('PROJECT_SPC_OVERFLOW_SINK_TEST','KIND_PROJECT');
INSERT INTO Projects(ProjectType,Name,ShortName,Description,Cost,CostProgressionModel,PrereqDistrict)
VALUES ('PROJECT_SPC_OVERFLOW_SINK_TEST','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_NAME','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_NAME','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_DESCRIPTION',1000000,'NO_PROGRESSION_MODEL','DISTRICT_CITY_CENTER');
-- No completion modifiers, conversions, GPP, unlock effects or rewards.
