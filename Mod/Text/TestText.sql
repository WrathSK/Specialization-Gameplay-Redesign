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

-- Institution list UI labels; no gameplay/localized name changes.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSTITUTIONS_HEADER','专业机构');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSTITUTION_CURRENT','当前');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSTITUTION_ENABLED','启用');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSTITUTION_INACTIVE','未激活');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSTITUTION_UNKNOWN','待确认');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSTITUTIONS_HEADER','Institutions');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSTITUTION_CURRENT','Current');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSTITUTION_ENABLED','Active');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSTITUTION_INACTIVE','Inactive');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSTITUTION_UNKNOWN','Pending');

-- P0-K read-only fact diagnostic.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_GREAT_WORK_FACTS','巨作事实'),
('en_US','LOC_SPC_GREAT_WORK_FACTS','Great Work facts');

-- P0-L1 ability/diagnostic label.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CULTURE_AESTHETIC','风雅熏陶'),
('en_US','LOC_SPC_CULTURE_AESTHETIC','Aesthetic influence');

-- L2A single-city reversible experiment; native precision is pending.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CULTURE_MEANING_CONFIG','结束验证'),
('en_US','LOC_SPC_CULTURE_MEANING_CONFIG','End yield gate'),
('zh_Hans_CN','LOC_SPC_CULTURE_MEANING_CONFIG_HINT','左／右键均结束本城实验：先撤销追加，再按当前事实恢复旧系统；不再切换文化候选。'),
('en_US','LOC_SPC_CULTURE_MEANING_CONFIG_HINT','Either click ends this city probe: withdraw additions before restoring legacy consumers from current facts. Legacy Culture candidates are not cycled.'),
('zh_Hans_CN','LOC_SPC_CULTURE_MEANING_PROBE','意义延展·接入门禁'),
('en_US','LOC_SPC_CULTURE_MEANING_PROBE','Meaning: Integration Gates'),
('zh_Hans_CN','LOC_SPC_CULTURE_MEANING_PROBE_HINT','文化ACTIVE4及确认馆藏；先核对当前已加载作品定义。左键：正常时代对话基线 → 五产出追加 → 结束。主题状态保持，逐领域Floor不变。右键查看差值与普通建筑真实进度；文化追加暂隔离，HD保持。可随时结束。'),
('en_US','LOC_SPC_CULTURE_MEANING_PROBE_HINT','Culture ACTIVE4 with confirmed works. Verify loaded definitions before baseline, five final yields, and end. Normal Dialogue and theming remain in effect. Right click reads differences and normal-building progress. Culture additions are deferred; HD is unchanged. End at any stage.'),
('zh_Hans_CN','LOC_SPC_MEANING_PROBE_CARRIER','意义延展验证载体'),
('en_US','LOC_SPC_MEANING_PROBE_CARRIER','Meaning probe carrier');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CULTURE_MEANING_AUTO','意义延展'),
('en_US','LOC_SPC_CULTURE_MEANING_AUTO','Meaning Extension'),
('zh_Hans_CN','LOC_SPC_CULTURE_MEANING_AUTO_HINT','左／右键只读本城资格、每件与全城追加基值。文化ACTIVE IV时自动生效，无需开启实验；市政／外交文化追加暂延期。'),
('en_US','LOC_SPC_CULTURE_MEANING_AUTO_HINT','Either click reads current eligibility and pre-theming per-work and city additions. Automatic at Culture ACTIVE IV; Government and Diplomatic Culture additions remain deferred.');

-- B167 L3-A native precision gate.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_TITLE','巨作启迪：小数伟人点数测试');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_TITLE','Inspiration: fractional GPP test');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_BUTTON','巨作启迪测试');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_BUTTON','Inspiration test');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_BUTTON_HINT','左键依次准备基线、+0.1、+0.3、+0.6、+1；右键只读刷新。仅测试选中城市的科学家基础点数。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_BUTTON_HINT','Left: baseline, +0.1, +0.3, +0.6, +1. Right: refresh only. Selected city Scientist base points only.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_END_BUTTON','结束启迪测试');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_END_BUTTON','End Inspiration test');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_BUSY','测试处理中，请稍后读取。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_BUSY','Test busy; read again shortly.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_STAGE','阶段{1_Num}：配置新增基础科学家点数 +{2_Num}/回合');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_STAGE','Stage {1_Num}: configured added Scientist base points +{2_Num}/turn');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_OFF','已关闭；未启用正式巨作启迪能力。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_OFF','Off; the full Inspiration ability is not enabled.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_INSTANCES','本模块载体数：{1_Num}（基线/结束应为0，测试值应为1）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_INSTANCES','Owned carriers: {1_Num} (baseline/end: 0; active value: 1)');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_CONTROL','这是固定值接口对照，不按当前D或作品数自动计算；+1是可选整数对照。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_CONTROL','Fixed-value interface control, not automatic D/work-count calculation. +1 is an optional integer control.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_NEXT_HELP','同回合保持其他条件不变。右键刷新读数；完成后点“结束启迪测试”。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_NEXT_HELP','Keep other conditions fixed in the same turn. Right-click to refresh; finish with End Inspiration test.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_STOP','测试暂停：{1_Text}。不要继续切换；请保留本报告。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_STOP','Test paused: {1_Text}. Stop switching values and keep this report.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_READ_UNKNOWN','原生科学家点数暂不可读；配置成功不代表原生生效。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_READ_UNKNOWN','Native Scientist rate unavailable; configuration does not prove native effect.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_NATIVE','原生全国科学家点数：{1_Text}/回合');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_NATIVE','Native empire Scientist points: {1_Text}/turn');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DELTA','相对本次同回合基线差值：{1_Text}/回合');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DELTA','Difference from this same-turn baseline: {1_Text}/turn');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_NO_BASELINE','无有效同回合对照基线；全国读数不能当成本城增量。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_NO_BASELINE','No valid same-turn baseline; the empire rate is not a city increment.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_SCOPE','差值包含当前正常倍率。若其他城市、政策或总督同时变化，对照失效；不要把载体值当实测。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_SCOPE','The delta includes normal modifiers. Other city, policy or governor changes invalidate comparison; carrier configuration is not measured output.');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_TURN','读取回合：{1_Num}（可能延迟一回合刷新）'),('en_US','LOC_SPC_INSPIRE_TURN','Read turn: {1_Num} (a one-turn refresh delay is possible)');
