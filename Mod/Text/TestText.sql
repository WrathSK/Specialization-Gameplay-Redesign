INSERT INTO LocalizedText (Language,Tag,Text)
SELECT Language,Tag,Text FROM
 (SELECT 'en_US' AS Language UNION ALL SELECT 'zh_Hans_CN') CROSS JOIN
 (SELECT 'LOC_SPC_CIV_NAME' AS Tag,'Scotland (Specialization Test)' AS Text
 UNION ALL SELECT 'LOC_SPC_LEADER_NAME','Robert the Bruce (Test)'
 UNION ALL SELECT 'LOC_SPC_ADJECTIVE','Scottish (Test)'
 UNION ALL SELECT 'LOC_SPC_ABILITY_NAME','Specialization Test: P0'
 UNION ALL SELECT 'LOC_SPC_ABILITY_DESCRIPTION','Specialization Test: diagnostic identity only. No Scottish abilities. Specialization gameplay is not yet enabled.'
 UNION ALL SELECT 'LOC_SPC_LOADING','Specialization Test: P0. Independent civilization; Scotland presentation only. USER_GAME_TEST_REQUIRED.'
 UNION ALL SELECT 'LOC_SPC_CITY_STIRLING','Stirling (Test)'
 UNION ALL SELECT 'LOC_SPC_CITY_EDINBURGH','Edinburgh (Test)'
 UNION ALL SELECT 'LOC_SPC_CITY_ABERDEEN','Aberdeen (Test)');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('en_US','LOC_UNIT_SPC_CREW_250_NAME','一级施工队'),
('en_US','LOC_UNIT_SPC_CREW_250_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 一级施工队可提供250点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_NAME','一级施工队'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 一级施工队可提供250点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_250_NAME','一级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_250_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 一级施工队可提供250点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_250_NAME','组建一级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_250_DESCRIPTION','Industry Lv1. Standard speed: 280 Production creates one 250-Production Crew. Both cost and output scale with game speed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_NAME','一级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 一级施工队可提供250点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_250_NAME','组建一级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_250_DESCRIPTION','工业专业Lv1开放。标准速度：成本280生产力，生成1支250生产力的施工队。成本与生产力随游戏速度同比缩放。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_420_NAME','二级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_420_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 二级施工队可提供420点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_420_NAME','组建二级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_420_DESCRIPTION','Industry Lv1. Standard speed: 460 Production creates one 420-Production Crew. Both cost and output scale with game speed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_420_NAME','二级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_420_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 二级施工队可提供420点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_420_NAME','组建二级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_420_DESCRIPTION','工业专业Lv1开放。标准速度：成本460生产力，生成1支420生产力的施工队。成本与生产力随游戏速度同比缩放。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_750_NAME','三级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_750_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 三级施工队可提供750点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_750_NAME','组建三级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_750_DESCRIPTION','Industry Lv1. Standard speed: 820 Production creates one 750-Production Crew. Both cost and output scale with game speed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_750_NAME','三级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_750_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 三级施工队可提供750点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_750_NAME','组建三级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_750_DESCRIPTION','工业专业Lv1开放。标准速度：成本820生产力，生成1支750生产力的施工队。成本与生产力随游戏速度同比缩放。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_1000_NAME','四级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_1000_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 四级施工队可提供1000点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_1000_NAME','组建四级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_1000_DESCRIPTION','Industry Lv1. Standard speed: 1100 Production creates one 1000-Production Crew. Both cost and output scale with game speed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_1000_NAME','四级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_1000_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 四级施工队可提供1000点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_1000_NAME','组建四级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_1000_DESCRIPTION','工业专业Lv1开放。标准速度：成本1100生产力，生成1支1000生产力的施工队。成本与生产力随游戏速度同比缩放。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_1360_NAME','五级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_1360_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 五级施工队可提供1360点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_1360_NAME','组建五级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_1360_DESCRIPTION','Industry Lv1. Standard speed: 1500 Production creates one 1360-Production Crew. Both cost and output scale with game speed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_1360_NAME','五级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_1360_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 五级施工队可提供1360点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_1360_NAME','组建五级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_1360_DESCRIPTION','工业专业Lv1开放。标准速度：成本1500生产力，生成1支1360生产力的施工队。成本与生产力随游戏速度同比缩放。');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_LV4_RESEARCH_PERCENT_NAME','四级专业专家科技加成');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_LV4_RESEARCH_PERCENT_NAME','四级专业专家科技加成');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_LV4_CULTURE_PERCENT_NAME','四级专业专家文化加成');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_LV4_CULTURE_PERCENT_NAME','四级专业专家文化加成');

-- B118 experiment labels, not formal Culture project localization.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_NAME','溢出承接实验（无收益）'),
('zh_Hans_CN','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_DESCRIPTION','仅独立测试存档。选为唯一当前生产目标后自动计时，正常经过一个回合后完成，无奖励。本批仅单城；读档不续算，需重新选择。进入本项目会放弃原有溢出生产力；砍树/收获隔离仍待专项验证。'),
('en_US','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_NAME','Overflow sink experiment (no reward)'),
('en_US','LOC_PROJECT_SPC_OVERFLOW_SINK_TEST_DESCRIPTION','Test save only. Select as the sole current production target to start automatically; completes after one normal turn, with no reward. Single city, no timer persistence across reload. Existing overflow is forfeited; chop/harvest isolation remains unverified.');
