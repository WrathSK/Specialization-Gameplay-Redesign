-- O5a: selected profile inputs and the final, read-only building projection.
CREATE TABLE SPC_EnvironmentSelection (
 Profile TEXT NOT NULL PRIMARY KEY CHECK (Profile IN ('OFFICIAL', 'HD'))
);
CREATE TABLE SPC_EnvironmentExcludedBuildings (
 BuildingType TEXT NOT NULL PRIMARY KEY REFERENCES Buildings(BuildingType)
);
CREATE TABLE SPC_EnvironmentBuildings (
 BuildingType TEXT NOT NULL PRIMARY KEY REFERENCES Buildings(BuildingType),
 DistrictType TEXT NOT NULL REFERENCES Districts(DistrictType),
 TierOverride INTEGER CHECK (TierOverride > 0)
);
CREATE TABLE SPC_EnvironmentAssembly (
 Id INTEGER PRIMARY KEY CHECK (Id = 1),
 Profile TEXT NOT NULL REFERENCES SPC_EnvironmentSelection(Profile),
 SchemaVersion INTEGER NOT NULL CHECK (SchemaVersion = 1)
);
