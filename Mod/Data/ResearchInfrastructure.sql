-- P0-C specialist BASE Science; 4 internal bits, no slots/housing/flat city yield.
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_RESEARCH_INFRA_0','KIND_BUILDING');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing) VALUES ('BUILDING_SPC_RESEARCH_INFRA_0','Research infrastructure (internal)',1,'DISTRICT_CAMPUS',1,0,0);
INSERT INTO Building_CitizenYieldChanges(BuildingType,YieldType,YieldChange) VALUES ('BUILDING_SPC_RESEARCH_INFRA_0','YIELD_SCIENCE',1);
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_RESEARCH_INFRA_1','KIND_BUILDING');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing) VALUES ('BUILDING_SPC_RESEARCH_INFRA_1','Research infrastructure (internal)',1,'DISTRICT_CAMPUS',1,0,0);
INSERT INTO Building_CitizenYieldChanges(BuildingType,YieldType,YieldChange) VALUES ('BUILDING_SPC_RESEARCH_INFRA_1','YIELD_SCIENCE',2);
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_RESEARCH_INFRA_2','KIND_BUILDING');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing) VALUES ('BUILDING_SPC_RESEARCH_INFRA_2','Research infrastructure (internal)',1,'DISTRICT_CAMPUS',1,0,0);
INSERT INTO Building_CitizenYieldChanges(BuildingType,YieldType,YieldChange) VALUES ('BUILDING_SPC_RESEARCH_INFRA_2','YIELD_SCIENCE',4);
INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_RESEARCH_INFRA_3','KIND_BUILDING');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing) VALUES ('BUILDING_SPC_RESEARCH_INFRA_3','Research infrastructure (internal)',1,'DISTRICT_CAMPUS',1,0,0);
INSERT INTO Building_CitizenYieldChanges(BuildingType,YieldType,YieldChange) VALUES ('BUILDING_SPC_RESEARCH_INFRA_3','YIELD_SCIENCE',8);
