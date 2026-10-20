-- B263: independent GS selection; runtime access remains single-player human only.
-- Never overwrite native America.
-- A fresh configuration DB is rebuilt on mod activation.
INSERT INTO Players
 (Domain,CivilizationType,LeaderType,CivilizationName,CivilizationIcon,LeaderName,LeaderIcon,
 CivilizationAbilityName,CivilizationAbilityDescription,CivilizationAbilityIcon,
 LeaderAbilityName,LeaderAbilityDescription,LeaderAbilityIcon,Portrait,PortraitBackground)
VALUES ('Players:Expansion2_Players','CIVILIZATION_SPC_AMERICA','LEADER_SPC_T_ROOSEVELT',
 'LOC_SPC_AMERICA_NAME','ICON_CIVILIZATION_SPC_AMERICA','LOC_SPC_ROOSEVELT_NAME','ICON_LEADER_SPC_T_ROOSEVELT',
 'LOC_SPC_SYSTEM_NAME','LOC_SPC_SYSTEM_DESCRIPTION','ICON_CIVILIZATION_SPC_AMERICA',
 'LOC_SPC_BLANK_LEADER_NAME','LOC_SPC_BLANK_LEADER_DESCRIPTION','ICON_LEADER_SPC_T_ROOSEVELT',
 'LEADER_T_ROOSEVELT_NEUTRAL','LEADER_T_ROOSEVELT_BACKGROUND');
-- PlayerItems intentionally stays empty: no American unique unit/building promises.
