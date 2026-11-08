-- Run after the final loaded content and exactly one environment component.
-- This is a definition inventory. Consumer eligibility and chain depth belong
-- to their respective contracts. The two Holy Site overrides are D0060.
INSERT INTO SPC_EnvironmentBuildings(BuildingType,DistrictType,TierOverride)
 SELECT b.BuildingType,b.PrereqDistrict,
  CASE WHEN b.PrereqDistrict='DISTRICT_HOLY_SITE'
   AND b.BuildingType IN ('BUILDING_JNR_HOSPITIUM','BUILDING_JNR_GARDEN') THEN 4 END
 FROM Buildings b JOIN Districts d ON d.DistrictType=b.PrereqDistrict
 WHERE b.InternalOnly=0 AND b.IsWonder=0 AND d.InternalOnly=0
 AND NOT EXISTS (SELECT 1 FROM SPC_EnvironmentExcludedBuildings x WHERE x.BuildingType=b.BuildingType)
 AND (SELECT COUNT(*) FROM SPC_EnvironmentSelection)=1;

-- Publish only a complete, nonempty projection. An invalid selection or an
-- empty inventory produces NULL and fails the existing profile constraint.
-- The game parser requires GROUP BY with HAVING, so use a filtered lookup.
INSERT INTO SPC_EnvironmentAssembly(Id,Profile,SchemaVersion)
 VALUES (1,(SELECT Profile FROM SPC_EnvironmentSelection
  WHERE (SELECT COUNT(*) FROM SPC_EnvironmentSelection)=1
  AND EXISTS (SELECT 1 FROM SPC_EnvironmentBuildings)),1);
