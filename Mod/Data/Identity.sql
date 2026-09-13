-- Independent gameplay identity; Scotland supplies presentation references only.
INSERT INTO Types (Type, Kind) VALUES
 ('CIVILIZATION_SPC_TEST','KIND_CIVILIZATION'),
 ('LEADER_SPC_TEST','KIND_LEADER'),
 ('TRAIT_CIVILIZATION_SPC_TEST','KIND_TRAIT');
INSERT INTO Civilizations
 (CivilizationType,Name,Description,Adjective,StartingCivilizationLevelType,RandomCityNameDepth,Ethnicity)
VALUES ('CIVILIZATION_SPC_TEST','LOC_SPC_CIV_NAME','LOC_SPC_CIV_NAME','LOC_SPC_ADJECTIVE',
 'CIVILIZATION_LEVEL_FULL_CIV',1,'ETHNICITY_EURO');
INSERT INTO Leaders (LeaderType,Name,InheritFrom,SceneLayers)
VALUES ('LEADER_SPC_TEST','LOC_SPC_LEADER_NAME','LEADER_DEFAULT',4);
INSERT INTO CivilizationLeaders (CivilizationType,LeaderType,CapitalName)
VALUES ('CIVILIZATION_SPC_TEST','LEADER_SPC_TEST','LOC_SPC_CITY_STIRLING');
INSERT INTO CityNames (CivilizationType,CityName) VALUES
 ('CIVILIZATION_SPC_TEST','LOC_SPC_CITY_STIRLING'),
 ('CIVILIZATION_SPC_TEST','LOC_SPC_CITY_EDINBURGH'),
 ('CIVILIZATION_SPC_TEST','LOC_SPC_CITY_ABERDEEN');
INSERT INTO Traits (TraitType,Name,Description)
VALUES ('TRAIT_CIVILIZATION_SPC_TEST','LOC_SPC_ABILITY_NAME','LOC_SPC_ABILITY_DESCRIPTION');
INSERT INTO CivilizationTraits (CivilizationType,TraitType)
VALUES ('CIVILIZATION_SPC_TEST','TRAIT_CIVILIZATION_SPC_TEST');
INSERT INTO LoadingInfo
 (LeaderType,ForegroundImage,BackgroundImage,LeaderText,PlayDawnOfManAudio)
VALUES ('LEADER_SPC_TEST','LEADER_ROBERT_THE_BRUCE_NEUTRAL',
 'LEADER_ROBERT_THE_BRUCE_BACKGROUND','LOC_SPC_LOADING',0);
INSERT INTO DiplomacyInfo (Type,BackgroundImage)
VALUES ('LEADER_SPC_TEST','LEADER_ROBERT_THE_BRUCE_BACKGROUND');
-- No Scottish Enlightenment, Bannockburn, Highlander, Golf Course or Robert inheritance.
