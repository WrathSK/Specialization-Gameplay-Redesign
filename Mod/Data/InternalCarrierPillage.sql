-- B271 user decision 2026-10-23; data definitions only, no save migration.
INSERT INTO Buildings_XP2 (BuildingType, Pillage)
SELECT BuildingType, 0 FROM Buildings
WHERE InternalOnly = 1 AND substr(BuildingType, 1, 13) = 'BUILDING_SPC_'
AND NOT EXISTS (SELECT 1 FROM Buildings_XP2 x WHERE x.BuildingType = Buildings.BuildingType);
