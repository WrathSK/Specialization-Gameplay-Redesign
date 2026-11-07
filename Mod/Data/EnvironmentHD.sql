-- The HD compatibility component supplies virtual-building exclusions.
-- The legacy HD Tier table is not an input to assembly.
INSERT INTO SPC_EnvironmentExcludedBuildings(BuildingType)
 SELECT b.BuildingType FROM HD_DUMMY_BUILDINGS h JOIN Buildings b USING (BuildingType)
 WHERE b.InternalOnly=0 AND b.IsWonder=0;
INSERT INTO SPC_EnvironmentSelection(Profile) VALUES ('HD');
