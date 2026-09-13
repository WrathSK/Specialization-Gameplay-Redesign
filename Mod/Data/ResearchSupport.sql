-- B022: native specialist yield carrier, explicitly enabled DEV experiment.
-- No slots, ordinary building yields, housing, GPP or production queue entry.
INSERT INTO Types (Type, Kind) VALUES ('BUILDING_SPC_DEV_RESEARCH_SUPPORT', 'KIND_BUILDING');
INSERT INTO Buildings (BuildingType, Name, Cost, PrereqDistrict, InternalOnly, CitizenSlots)
VALUES ('BUILDING_SPC_DEV_RESEARCH_SUPPORT', 'Research specialist support (Test)', 1, 'DISTRICT_CAMPUS', 1, 0);
INSERT INTO Building_CitizenYieldChanges (BuildingType, YieldType, YieldChange) VALUES
('BUILDING_SPC_DEV_RESEARCH_SUPPORT', 'YIELD_FOOD', 3),
('BUILDING_SPC_DEV_RESEARCH_SUPPORT', 'YIELD_PRODUCTION', 3);
