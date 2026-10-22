-- Culture D0029 风雅熏陶. Building contributions aggregate on their actual district.
-- One city-owned master, no permanent benefit ledger or global trait modifier.
CREATE TABLE IF NOT EXISTS SPC_CultureAestheticBits (Bit INTEGER PRIMARY KEY, Amount INTEGER NOT NULL);
INSERT INTO SPC_CultureAestheticBits VALUES (0,1);
INSERT INTO SPC_CultureAestheticBits VALUES (1,2);
INSERT INTO SPC_CultureAestheticBits VALUES (2,4);
INSERT INTO SPC_CultureAestheticBits VALUES (3,8);
INSERT INTO SPC_CultureAestheticBits VALUES (4,16);
INSERT INTO SPC_CultureAestheticBits VALUES (5,32);
INSERT INTO SPC_CultureAestheticBits VALUES (6,64);
INSERT INTO SPC_CultureAestheticBits VALUES (7,128);
INSERT INTO SPC_CultureAestheticBits VALUES (8,256);
INSERT INTO SPC_CultureAestheticBits VALUES (9,512);
INSERT INTO SPC_CultureAestheticBits VALUES (10,1024);
INSERT INTO SPC_CultureAestheticBits VALUES (11,2048);
INSERT INTO SPC_CultureAestheticBits VALUES (12,4096);
INSERT INTO SPC_CultureAestheticBits VALUES (13,8192);
INSERT INTO SPC_CultureAestheticBits VALUES (14,16384);
INSERT INTO SPC_CultureAestheticBits VALUES (15,32768);

INSERT INTO Types(Type,Kind) VALUES ('BUILDING_SPC_CULTURE_AESTHETIC','KIND_BUILDING');
INSERT INTO Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing)
 VALUES ('BUILDING_SPC_CULTURE_AESTHETIC','LOC_SPC_CULTURE_AESTHETIC',1,'DISTRICT_CITY_CENTER',1,0,0);
INSERT INTO Requirements(RequirementId,RequirementType)
 SELECT 'SPC_CULTURE_AESTHETIC_'||Bit||'_REQ','REQUIREMENT_PLOT_PROPERTY_MATCHES' FROM SPC_CultureAestheticBits;
INSERT INTO RequirementArguments(RequirementId,Name,Value)
 SELECT 'SPC_CULTURE_AESTHETIC_'||Bit||'_REQ','PropertyName','SPC_CULTURE_AESTHETIC_'||Bit FROM SPC_CultureAestheticBits;
INSERT INTO RequirementArguments(RequirementId,Name,Value)
 SELECT 'SPC_CULTURE_AESTHETIC_'||Bit||'_REQ','PropertyMinimum',1 FROM SPC_CultureAestheticBits;
INSERT INTO RequirementSets(RequirementSetId,RequirementSetType)
 SELECT 'SPC_CULTURE_AESTHETIC_'||Bit||'_SET','REQUIREMENTSET_TEST_ALL' FROM SPC_CultureAestheticBits;
INSERT INTO RequirementSetRequirements(RequirementSetId,RequirementId)
 SELECT 'SPC_CULTURE_AESTHETIC_'||Bit||'_SET','SPC_CULTURE_AESTHETIC_'||Bit||'_REQ' FROM SPC_CultureAestheticBits;
INSERT INTO Modifiers(ModifierId,ModifierType,SubjectRequirementSetId)
 SELECT 'SPC_CULTURE_AESTHETIC_'||Bit,'MODIFIER_CITY_DISTRICTS_ADJUST_TOURISM_CHANGE','SPC_CULTURE_AESTHETIC_'||Bit||'_SET' FROM SPC_CultureAestheticBits;
INSERT INTO ModifierArguments(ModifierId,Name,Value)
 SELECT 'SPC_CULTURE_AESTHETIC_'||Bit,'Amount',Amount FROM SPC_CultureAestheticBits;
INSERT INTO BuildingModifiers(BuildingType,ModifierId)
 SELECT 'BUILDING_SPC_CULTURE_AESTHETIC','SPC_CULTURE_AESTHETIC_'||Bit FROM SPC_CultureAestheticBits;
