-- B263: presentation-only American shell. The legacy Scotland identity is retained.
-- Explicit allow-list of presentation tables: never copy LeaderTraits, American
-- CivilizationTraits, agendas, biases, replacements or any original Modifiers.
INSERT INTO Types(Type,Kind) VALUES
 ('CIVILIZATION_SPC_AMERICA','KIND_CIVILIZATION'),
 ('LEADER_SPC_T_ROOSEVELT','KIND_LEADER');
INSERT INTO Civilizations
 (CivilizationType,Name,Description,Adjective,StartingCivilizationLevelType,RandomCityNameDepth,Ethnicity)
SELECT 'CIVILIZATION_SPC_AMERICA','LOC_SPC_AMERICA_NAME','LOC_SPC_AMERICA_DESCRIPTION',
 'LOC_SPC_AMERICA_ADJECTIVE',StartingCivilizationLevelType,RandomCityNameDepth,Ethnicity
FROM Civilizations WHERE CivilizationType='CIVILIZATION_AMERICA';
-- Gameplay inheritance stays neutral. Leaders.artdef supplies the Roosevelt model.
INSERT INTO Leaders(LeaderType,Name,InheritFrom,SceneLayers,Sex,SameSexPercentage)
SELECT 'LEADER_SPC_T_ROOSEVELT','LOC_SPC_ROOSEVELT_NAME','LEADER_DEFAULT',SceneLayers,Sex,SameSexPercentage
FROM Leaders WHERE LeaderType='LEADER_T_ROOSEVELT';
INSERT INTO CivilizationLeaders(CivilizationType,LeaderType,CapitalName)
SELECT 'CIVILIZATION_SPC_AMERICA','LEADER_SPC_T_ROOSEVELT',CapitalName
FROM CivilizationLeaders WHERE CivilizationType='CIVILIZATION_AMERICA' AND LeaderType='LEADER_T_ROOSEVELT';
INSERT INTO CivilizationTraits(CivilizationType,TraitType)
VALUES ('CIVILIZATION_SPC_AMERICA','TRAIT_CIVILIZATION_SPC_TEST');
INSERT INTO CityNames(CivilizationType,CityName,SortIndex)
SELECT 'CIVILIZATION_SPC_AMERICA',CityName,SortIndex
FROM CityNames WHERE CivilizationType='CIVILIZATION_AMERICA';
INSERT INTO CivilizationCitizenNames(CivilizationType,CitizenName,Female,Modern)
SELECT 'CIVILIZATION_SPC_AMERICA',CitizenName,Female,Modern
FROM CivilizationCitizenNames WHERE CivilizationType='CIVILIZATION_AMERICA';
INSERT INTO CivilizationInfo(CivilizationType,Header,Caption,SortIndex)
SELECT 'CIVILIZATION_SPC_AMERICA',Header,Caption,SortIndex
FROM CivilizationInfo WHERE CivilizationType='CIVILIZATION_AMERICA';
INSERT INTO LeaderInfo(LeaderType,Header,Caption,SortIndex)
SELECT 'LEADER_SPC_T_ROOSEVELT',Header,Caption,SortIndex
FROM LeaderInfo WHERE LeaderType='LEADER_T_ROOSEVELT';
INSERT INTO LeaderQuotes(LeaderType,Quote,QuoteAudio)
SELECT 'LEADER_SPC_T_ROOSEVELT',Quote,QuoteAudio
FROM LeaderQuotes WHERE LeaderType='LEADER_T_ROOSEVELT';
INSERT INTO LoadingInfo
 (LeaderType,ForegroundImage,BackgroundImage,LeaderText,PlayDawnOfManAudio,DawnOfManLeaderId)
VALUES ('LEADER_SPC_T_ROOSEVELT','LEADER_T_ROOSEVELT_NEUTRAL','LEADER_T_ROOSEVELT_BACKGROUND',
 'LOC_LOADING_INFO_LEADER_T_ROOSEVELT',1,'LEADER_T_ROOSEVELT');
INSERT INTO DiplomacyInfo(Type,BackgroundImage)
VALUES ('LEADER_SPC_T_ROOSEVELT','LEADER_T_ROOSEVELT_BACKGROUND');
-- GS map naming pools, not terrain/start biases.
INSERT INTO NamedRiverCivilizations(NamedRiverType,CivilizationType)
SELECT NamedRiverType,'CIVILIZATION_SPC_AMERICA'
FROM NamedRiverCivilizations WHERE CivilizationType='CIVILIZATION_AMERICA';
INSERT INTO NamedVolcanoCivilizations(NamedVolcanoType,CivilizationType)
SELECT NamedVolcanoType,'CIVILIZATION_SPC_AMERICA'
FROM NamedVolcanoCivilizations WHERE CivilizationType='CIVILIZATION_AMERICA';
INSERT INTO NamedMountainCivilizations(NamedMountainType,CivilizationType)
SELECT NamedMountainType,'CIVILIZATION_SPC_AMERICA'
FROM NamedMountainCivilizations WHERE CivilizationType='CIVILIZATION_AMERICA';
INSERT INTO NamedDesertCivilizations(NamedDesertType,CivilizationType)
SELECT NamedDesertType,'CIVILIZATION_SPC_AMERICA'
FROM NamedDesertCivilizations WHERE CivilizationType='CIVILIZATION_AMERICA';
INSERT INTO NamedLakeCivilizations(NamedLakeType,CivilizationType)
SELECT NamedLakeType,'CIVILIZATION_SPC_AMERICA'
FROM NamedLakeCivilizations WHERE CivilizationType='CIVILIZATION_AMERICA';
INSERT INTO NamedSeaCivilizations(NamedSeaType,CivilizationType)
SELECT NamedSeaType,'CIVILIZATION_SPC_AMERICA'
FROM NamedSeaCivilizations WHERE CivilizationType='CIVILIZATION_AMERICA';
