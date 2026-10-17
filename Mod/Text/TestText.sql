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
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_BUTTON_HINT','左键：基线→+0.1→+0.3→+0.6→+1→结束。右键：刷新读数和原生实例诊断。仅测试选中城市的科学家基础点数。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_BUTTON_HINT','Left: baseline, +0.1, +0.3, +0.6, +1, then end. Right: rates and native instance diagnostics. Selected city Scientist base points only.');
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
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_NEXT_HELP','右键读取原生诊断；允许过回合后刷新。随时点右列“结束启迪测试”撤销。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_NEXT_HELP','Right-click for native diagnostics; a turn-boundary refresh may be needed. End Inspiration test in the right column withdraws at any stage.');
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

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_FINAL_HELP','已到整数+1档。再点一次左键即可结束，也可点右列“结束启迪测试”。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_FINAL_HELP','Integer +1 is the final stage. Left-click once more to end, or use End Inspiration test in the right column.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_OFF_HELP','测试已停止，配置载体应为0。右键可继续核对原生残留；结束操作本身不证明延迟读数已刷新。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_OFF_HELP','Test stopped; owned carriers should be zero. Right-click to inspect native residue; withdrawal alone does not prove delayed rates have refreshed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_TITLE','原生实例诊断（只读；参数不是最终收益）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_TITLE','Native instance diagnostics (read-only; arguments are not final yields)');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_SCAN','定义读取：{1_Text}；本玩家匹配测试实例：{2_Num}；Owner玩家未知：{3_Num}。城市归属见明细。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_SCAN','Definition read: {1_Text}; matching test instances for this player: {2_Num}; unknown owner player: {3_Num}. See city attribution below.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_UNKNOWN','原生实例读取未完成：{1_Text}；不能据此认定零残留。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_UNKNOWN','Native instance read incomplete: {1_Text}; this cannot establish zero residue.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_PROBE','测试实例{1_Text}｜启用={2_Text}｜原生Amount={3_Text}｜定义Amount={4_Text}｜类别={5_Text}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_PROBE','Test instance {1_Text} | Active={2_Text} | native Amount={3_Text} | DB Amount={4_Text} | class={5_Text}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_PERCENT','倍率来源{1_Text}｜启用={2_Text}｜Amount={3_Text}｜类别={4_Text}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_PERCENT','Percent source {1_Text} | Active={2_Text} | Amount={3_Text} | class={4_Text}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_OWNER','Owner玩家={1_Text}｜{2_Text}｜{3_Text}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_OWNER','Owner player={1_Text} | {2_Text} | {3_Text}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_SUBJECT','接收对象{1_Num}｜玩家={2_Text}｜{3_Text}｜{4_Text}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_SUBJECT','Subject {1_Num} | player={2_Text} | {3_Text} | {4_Text}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_SUBJECTS','接收对象数：{1_Text}（最多展开2个；未核验格式不推断城市）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_SUBJECTS','Subjects: {1_Text} (up to two displayed; unverified formats do not establish a city)');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_MULTIPLIER','有效总倍率：未确认。以下仅为相关原生来源，不求和或反推倍率。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_MULTIPLIER','Effective total multiplier: unconfirmed. Related native sources below are not summed or used to infer a multiplier.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_LIMIT','另有{1_Num}项未展开；不能把省略项当作不存在。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_LIMIT','{1_Num} more entries not displayed; omission does not mean absence.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRE_DIAG_NONE','本次完整枚举在本玩家范围未观察到这四个测试ID；不是本城专属收益读数。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRE_DIAG_NONE','Complete enumeration found none of the four test IDs for this player; this is not a city-specific yield reading.');

-- B172: normal automatic Inspiration; old probe strings remain historical.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_AUTO','巨作启迪');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_AUTO','Great Works Inspiration');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_BUTTON','巨作启迪报告');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_BUTTON','Inspiration report');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_HINT','自动生效，无需开关。左键：当前时代、倍率与全国点数；右键：原生实例明细。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_HINT','Automatic ability; no enable switch. Left: eras, bonus and empire points. Right: native instance details.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_PENDING','当前状态待核对；读取报告不会启用或重算能力。右键可查看原因。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_PENDING','Current state needs review. Reading does not enable or recompute the ability; right-click for details.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_INACTIVE','当前未生效：需要文化专业 Potential IV 且 ACTIVE IV。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_INACTIVE','Inactive: Culture Potential IV and ACTIVE IV required.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_CURRENT','当前馆藏：{1_Num}个不同合格时代；本城所有伟人点数 +{2_Num}%。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_CURRENT','Current collection: {1_Num} distinct eligible eras; all city GPP +{2_Num}%.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_NOTE','随当前馆藏和ACTIVE自动更新；上述为能力配置，不是实测点数增量。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_NOTE','Updates automatically with current collection and ACTIVE. The bonus above is configuration, not a measured points increment.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_READ_UNKNOWN','原生点数暂不可读，不能据此判断收益为零。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_READ_UNKNOWN','Native points unavailable; this does not establish zero output.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_NATIONAL','全国原生读数（回合{1_Num}，不是本城独占收益）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_NATIONAL','Native empire readings (turn {1_Num}; not this city alone)');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_RATE','{1_Text}：{2_Text}/回合；当前累计 {3_Text}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_RATE','{1_Text}: {2_Text}/turn; current total {3_Text}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_ZERO','当前可读类别均为0。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_ZERO','All readable categories currently show zero.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_READ_NOTE','点数可能在过回合后刷新。全国读数包含其它城市与既有倍率；招募或赞助会改变累计值。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_READ_NOTE','Points may refresh after a turn. Empire readings include other cities and existing bonuses; recruitment or patronage changes totals.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_DIAG_SCAN','枚举：{1_Text}；本玩家本模块/旧测试实例：{2_Num}；Owner未知：{3_Num}。城市归属须看明细。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_DIAG_SCAN','Enumeration: {1_Text}; owned/current or retired probe instances for this player: {2_Num}; unknown owner: {3_Num}. City attribution requires details.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_DIAG_NONE','完整枚举未观察到本玩家的新能力或旧测试ID；这不是本城点数为零的证据。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_DIAG_NONE','Complete enumeration found no current or retired owned IDs for this player; this does not prove zero city points.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_DIAG_PROBE','{1_Text}｜启用={2_Text}｜原生Amount={3_Text}｜定义Amount={4_Text}｜类别={5_Text}；ERA为城市%，PROBE为旧基础点数');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSPIRATION_DIAG_PROBE','{1_Text} | Active={2_Text} | native Amount={3_Text} | DB Amount={4_Text} | class={5_Text}; ERA uses city %, PROBE uses retired base points');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSPIRATION_CLEANUP_PENDING','有{1_Num}座城市的旧载体清理未确认；相关城市暂停新投影，不能宣称已无残留。'),('en_US','LOC_SPC_INSPIRATION_CLEANUP_PENDING','Old-carrier cleanup is unconfirmed in {1_Num} cities. New projection is paused there; zero residue is not established.');

-- Culture uses the existing cumulative institution display; no new gameplay effects.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CULTURE_INSIGHTS_BUTTON','文化见闻'),
('en_US','LOC_SPC_CULTURE_INSIGHTS_BUTTON','Cultural Insights'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSIGHTS_TITLE','文化见闻'),
('en_US','LOC_SPC_CULTURE_INSIGHTS_TITLE','Cultural Insights'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSIGHTS_TOOLTIP','查看所选己方城市的历史与当前有效见闻；整城旅游与网络效果尚未实施。'),
('en_US','LOC_SPC_CULTURE_INSIGHTS_TOOLTIP','View recorded and currently effective Insights for the selected owned city. Citywide Tourism and network effects are not implemented yet.'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_1','文艺同好会'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_1','文艺同好会'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_2','赞助人行会'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_2','赞助人行会'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_3','人文联合会'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_3','人文联合会'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_4','博雅总院'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_4','博雅总院'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_1_HELP','基础专家支持[NEWLINE]每名实际工作的文化专家额外获得3食物、3生产力。原生收益另算；高等级继续使用这一档基础支持。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_1_HELP','Specialist support[NEWLINE]Each working Culture specialist receives +3 Food and +3 Production in addition to native yields. Higher levels retain this same support.'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_2_HELP','文艺赞助[NEWLINE]本城剧院广场提供1住房；每个存在合格普通建筑的等级再提供1住房，同等级不重复。每名工作的文化专家额外提供2基础大作家、2基础大艺术家和2基础大音乐家点数，接受其它伟人点数百分比修正。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_2_HELP','Arts patronage[NEWLINE]The Theater Square provides +1 Housing, plus +1 per eligible ordinary building tier, once per tier. Each working Culture specialist adds 2 base Writer, Artist and Musician points, subject to GPP percentage modifiers.'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_3_HELP','时代对话[NEWLINE]同名城市项目完整占用1回合。每城每个启动时代最多成功一次；按完成时本城合格馆藏的不同作品时代数，每时代永久累计5个百分点的巨作原生产出倍率。ACTIVE低于三级或离开文化身份时效果暂停，历史保留；中断项目不消耗成功机会。当前运行范围：原生巨作旅游业绩倍率，不放大意义延展追加值。[NEWLINE][NEWLINE]风雅熏陶[NEWLINE]本城每覆盖一个合格巨作时代，每座合格普通建筑额外提供1旅游业绩。按当前时代覆盖动态计算，被掠夺的建筑不计入。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_3_HELP','Dialogue of Eras[NEWLINE]The city project occupies one full turn. Once per starting game era, it permanently adds 5 percentage points per distinct eligible work era present at completion. Below Culture ACTIVE III or outside Culture, the effect pauses while history remains; cancellation does not spend the successful-era allowance. Current runtime scope: native Great Work Tourism, excluding Meaning additions.[NEWLINE][NEWLINE]Aesthetic Influence[NEWLINE]Each distinct eligible work era currently present adds 1 Tourism to every eligible ordinary building. Pillaged buildings are excluded.'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_4_HELP','意义延展[NEWLINE]每件合格巨作从本城各合格领域获得0.5×基础设施深度份代表产出：金币每份3点，其它每份1点。各领域分别向下取整后合计，再按作品件数结算；同领域取最高单区域深度。时代对话不放大追加值，原生主题化可作用于追加。当前运行范围暂不计入政府广场、外交区的文化追加，其它领域照常生效。[NEWLINE][NEWLINE]巨作启迪[NEWLINE]本城当前每覆盖一个不同巨作时代，所有伟人点数产出提高3%；最多7时代、21%。没有基础点数的类别不会凭空获得点数。[NEWLINE][NEWLINE]人文考察团[NEWLINE]可训练考察团，按间谍成本公式、独立训练次数计价，全国同时最多1支。派遣到已遇见外国主要文明，进行风土考察、艺文采撷、奇观巡礼；标准速度任务各2回合。每个来源城对每文明、每类别首次成功获得1份文化见闻，归档历史保留。当前批次提供任务与见闻记录；见闻的整城旅游业绩及文化网络收益尚未实施。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_4_HELP','Meaning Extension[NEWLINE]Each eligible work receives 0.5 times infrastructure depth in representative yield shares from each eligible domain. Gold is 3 per share; other yields are 1. Floor each domain separately, combine, then multiply by work count; use the deepest single district per domain. Dialogue does not amplify additions; native theming may. Current runtime excludes Culture additions from the Government Plaza and Diplomatic Quarter; other domains remain active.[NEWLINE][NEWLINE]Great Works Inspiration[NEWLINE]Each distinct eligible work era currently present adds 3% to all city GPP, up to 7 eras and 21%. Categories without base points gain none.[NEWLINE][NEWLINE]Humanities Expedition[NEWLINE]Train an Expedition using the Spy cost formula with independent production history; the player may have one existing team. Send it to met foreign major civilizations for People, Works or Places missions, each 2 turns at Standard speed. First success per archive city, civilization and category records one Insight. Current implementation provides missions and preserved records; citywide Tourism and Culture network rewards are not implemented yet.');
