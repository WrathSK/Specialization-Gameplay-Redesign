-- Front-end selection, loading and Civilopedia copy for the test civilization.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_AMERICA_NAME','美国（专业测试）'),
('zh_Hans_CN','LOC_SPC_AMERICA_DESCRIPTION','美国（专业测试）'),
('zh_Hans_CN','LOC_SPC_AMERICA_ADJECTIVE','美国'),
('zh_Hans_CN','LOC_SPC_ROOSEVELT_NAME','罗斯福（进步党·专业测试）'),
('zh_Hans_CN','LOC_SPC_SYSTEM_NAME','城市专业化'),
('zh_Hans_CN','LOC_SPC_SYSTEM_DESCRIPTION','城市可使用科研、文化、商业和工业专业系统。各专业的机构、投资与网络能力按专业规则启用。'),
('zh_Hans_CN','LOC_SPC_BLANK_LEADER_NAME','专业测试领袖'),
('zh_Hans_CN','LOC_SPC_BLANK_LEADER_DESCRIPTION','采用罗斯福（进步党）的外观与人物介绍，不拥有美国或罗斯福的特色能力、特色单位和特色建筑。'),
('zh_Hans_CN','LOC_SPC_ABILITY_NAME','城市专业化'),
('zh_Hans_CN','LOC_SPC_ABILITY_DESCRIPTION','城市可使用科研、文化、商业和工业专业系统。各专业的机构、投资与网络能力按专业规则启用。'),
('en_US','LOC_SPC_AMERICA_NAME','America (Specialization Test)'),
('en_US','LOC_SPC_AMERICA_DESCRIPTION','America (Specialization Test)'),
('en_US','LOC_SPC_AMERICA_ADJECTIVE','American'),
('en_US','LOC_SPC_ROOSEVELT_NAME','Teddy Roosevelt (Bull Moose, Specialization Test)'),
('en_US','LOC_SPC_SYSTEM_NAME','City Specialization'),
('en_US','LOC_SPC_SYSTEM_DESCRIPTION','Cities can specialize in Research, Culture, Commerce, or Industry. Each specialization grants its own institutions and abilities.'),
('en_US','LOC_SPC_BLANK_LEADER_NAME','Specialization Test Leader'),
('en_US','LOC_SPC_BLANK_LEADER_DESCRIPTION','Uses the appearance and biography of Teddy Roosevelt (Bull Moose). America’s and Roosevelt’s unique abilities, units, and buildings are disabled.'),
('en_US','LOC_SPC_ABILITY_NAME','City Specialization'),
('en_US','LOC_SPC_ABILITY_DESCRIPTION','Cities can specialize in Research, Culture, Commerce, or Industry. Each specialization grants its own institutions and abilities.'),
('zh_Hans_CN','LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_TITLE','罗斯福（进步党·专业测试）'),
('zh_Hans_CN','LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_CHAPTER_CAPSULE_BODY','罗斯福（进步党）的城市专业化测试版本。'),
('zh_Hans_CN','LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_CHAPTER_DETAILED_BODY','此测试领袖不拥有美国或罗斯福的特色能力、特色单位和特色建筑。城市可使用科研、文化、商业和工业专业系统。'),
('zh_Hans_CN','LOC_PEDIA_CIVILIZATIONS_PAGE_CIVILIZATION_SPC_AMERICA_TITLE','美国（专业测试）'),
('en_US','LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_TITLE','Teddy Roosevelt (Bull Moose, Specialization Test)'),
('en_US','LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_CHAPTER_CAPSULE_BODY','A city specialization test version of Teddy Roosevelt (Bull Moose).'),
('en_US','LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_CHAPTER_DETAILED_BODY','Cities can specialize in Research, Culture, Commerce, or Industry. America’s and Roosevelt’s unique abilities, units, and buildings are disabled.'),
('en_US','LOC_PEDIA_CIVILIZATIONS_PAGE_CIVILIZATION_SPC_AMERICA_TITLE','America (Specialization Test)');

-- Use each installed language's historical biography in the corresponding locale.
-- Native strategy text remains with the original leader and civilization.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text)
SELECT Language,REPLACE(Tag,'LEADER_T_ROOSEVELT','LEADER_SPC_T_ROOSEVELT'),Text
FROM LocalizedText
WHERE Language IN ('en_US','zh_Hans_CN')
 AND Tag GLOB 'LOC_PEDIA_LEADERS_PAGE_LEADER_T_ROOSEVELT_CHAPTER_HISTORY_*';
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text)
SELECT Language,REPLACE(Tag,'CIVILIZATION_AMERICA','CIVILIZATION_SPC_AMERICA'),Text
FROM LocalizedText
WHERE Language IN ('en_US','zh_Hans_CN')
 AND Tag GLOB 'LOC_PEDIA_CIVILIZATIONS_PAGE_CIVILIZATION_AMERICA_CHAPTER_HISTORY_*';
