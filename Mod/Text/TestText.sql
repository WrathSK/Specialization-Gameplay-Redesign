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
('en_US','LOC_UNIT_SPC_CREW_250_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 一级施工队可提供260点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_NAME','一级施工队'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 一级施工队可提供260点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_250_NAME','Tier 1 Construction Crew');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_250_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 一级施工队可提供260点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_250_NAME','Form Tier 1 Construction Crew');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_250_DESCRIPTION','Industry ACTIVE III. Standard speed: 390 Production creates one 260-Production Crew. Both cost and output scale with game speed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_NAME','一级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 一级施工队可提供260点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_250_NAME','组建一级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_250_DESCRIPTION','工业ACTIVE III开放。标准速度：基础成本390生产力，生成1支260生产力的施工队。成本与生产力随游戏速度同比缩放。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_420_NAME','Tier 2 Construction Crew');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_420_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 二级施工队可提供420点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_420_NAME','Form Tier 2 Construction Crew');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_420_DESCRIPTION','Industry Lv1. Standard speed: 460 Production creates one 420-Production Crew. Both cost and output scale with game speed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_420_NAME','二级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_420_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 二级施工队可提供420点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_420_NAME','组建二级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_420_DESCRIPTION','工业专业Lv1开放。标准速度：成本460生产力，生成1支420生产力的施工队。成本与生产力随游戏速度同比缩放。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_750_NAME','Tier 3 Construction Crew');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_750_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 三级施工队可提供750点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_750_NAME','Form Tier 3 Construction Crew');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_750_DESCRIPTION','Industry Lv1. Standard speed: 820 Production creates one 750-Production Crew. Both cost and output scale with game speed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_750_NAME','三级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_750_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 三级施工队可提供750点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_750_NAME','组建三级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_750_DESCRIPTION','工业专业Lv1开放。标准速度：成本820生产力，生成1支750生产力的施工队。成本与生产力随游戏速度同比缩放。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_1000_NAME','Tier 4 Construction Crew');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_1000_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 四级施工队可提供1000点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_1000_NAME','Form Tier 4 Construction Crew');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_1000_DESCRIPTION','Industry Lv1. Standard speed: 1100 Production creates one 1000-Production Crew. Both cost and output scale with game speed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_1000_NAME','四级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_1000_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 四级施工队可提供1000点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_1000_NAME','组建四级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_1000_DESCRIPTION','工业专业Lv1开放。标准速度：成本1100生产力，生成1支1000生产力的施工队。成本与生产力随游戏速度同比缩放。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_1360_NAME','Tier 5 Construction Crew');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_1360_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 五级施工队可提供1360点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_1360_NAME','Form Tier 5 Construction Crew');
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
('zh_Hans_CN','LOC_SPC_CULTURE_INSIGHTS_TOOLTIP','查看所选己方城市的历史文化见闻与当前有效见闻。'),
('en_US','LOC_SPC_CULTURE_INSIGHTS_TOOLTIP','View recorded and currently effective Insights for the selected owned city. Citywide Tourism and network effects are not implemented yet.'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_1','文艺同好会'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_1','Arts Society'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_2','赞助人行会'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_2','Patrons’ Guild'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_3','人文联合会'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_3','Humanities Federation'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_4','博雅总院'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_4','Academy of the Liberal Arts'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_1_HELP','创作者与爱好者聚在一起，让城市的文化生活扎根成长。[NEWLINE][NEWLINE]基础专家支持：[NEWLINE][ICON_BULLET] 每名在岗文化专家额外提供 +3 [ICON_Food] 食物和 +3 [ICON_Production] 生产力。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_1_HELP','Artists and enthusiasts gather here to share their work.[NEWLINE][NEWLINE]Basic Specialist Support:[NEWLINE][ICON_BULLET] Each working Culture specialist provides +3 [ICON_Food] Food and +3 [ICON_Production] Production.'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_2_HELP','稳定的资助与委托，让文学、艺术与音乐在城中长久兴盛。[NEWLINE][NEWLINE]文艺赞助：[NEWLINE][ICON_BULLET] 本城剧院广场 +1 [ICON_Housing] 住房。每个已有合格普通建筑的等级再 +1，同级只计一次。[NEWLINE][ICON_BULLET] 每名在岗文化专家额外提供 +2 [ICON_GreatWriter] 大作家、+2 [ICON_GreatArtist] 大艺术家、+2 [ICON_GreatMusician] 大音乐家基础点数。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_2_HELP','Steady patronage and commissions help literature, art, and music flourish.[NEWLINE][NEWLINE]Arts Patronage:[NEWLINE][ICON_BULLET] This city''s Theater Square provides +1 [ICON_Housing] Housing, plus 1 for each tier of eligible buildings it contains. Each tier counts once.[NEWLINE][ICON_BULLET] Each working Culture specialist provides +2 base [ICON_GreatWriter] Great Writer points, +2 base [ICON_GreatArtist] Great Artist points, and +2 base [ICON_GreatMusician] Great Musician points.'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_3_HELP','不同时代的巨作在此汇聚，旧作有了新的诠释，艺术也渐渐融入城市生活。[NEWLINE][NEWLINE]时代对话：[NEWLINE][ICON_BULLET] 项目需 1 个完整生产回合。每城每个游戏时代限完成一次，按开工时的时代计。[NEWLINE][ICON_BULLET] 完成时，合格馆藏每涵盖一个作品时代，巨作本身的 [ICON_Tourism] 旅游业绩倍率永久累积 5 个百分点。文化启用等级达到三级时生效。@SPC_METRIC@[NEWLINE][NEWLINE]风雅熏陶：[NEWLINE][ICON_BULLET] 本城合格馆藏每涵盖一个作品时代，每座完好的合格普通建筑 +1 [ICON_Tourism] 旅游业绩。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_3_HELP','Great Works from many eras find new interpretations and enrich the life of the city.[NEWLINE][NEWLINE]Dialogue of Eras:[NEWLINE][ICON_BULLET] This project takes 1 full turn of Production. Each city can complete it once per game era. A completion counts toward the era in which the project began.[NEWLINE][ICON_BULLET] On completion, each distinct era represented in the city''s eligible collection adds 5 percentage points to its [ICON_Tourism] Tourism bonus for Great Works. The city keeps the accumulated bonus. It applies while Culture is active at Level 3 or higher.@SPC_METRIC@[NEWLINE][NEWLINE]Cultivated Taste:[NEWLINE][ICON_BULLET] Each eligible, unpillaged building gains +1 [ICON_Tourism] Tourism per era represented by the city''s current eligible Great Works.'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_4_HELP','学者借各领域的见解重读巨作，也把目光投向异国的风土与艺术。[NEWLINE][NEWLINE]意义延展：[NEWLINE][ICON_BULLET] 每件合格巨作从本城符合条件的专业领域获得额外产出。基础设施深度决定收益。可受主题化加成影响，不受「时代对话」放大。目前不计市政广场与外交区的文化追加。[NEWLINE][NEWLINE]巨作启迪：[NEWLINE][ICON_BULLET] 本城合格馆藏每涵盖一个作品时代，已有基础产出的 [ICON_GreatPerson] 伟人点数 +3%，最高 +24%。[NEWLINE][NEWLINE]人文考察团：[NEWLINE][ICON_BULLET] 可训练人文考察团，全国同时最多 1 支。派往已遇见的外国主要文明。每个来源城市对每个目标文明的每类任务首次成功时，取得 1 份文化见闻。[NEWLINE][ICON_BULLET] 有效见闻提高来源城市的 [ICON_Tourism] 旅游业绩，同一来源城市集齐同一文明的三类见闻后，可通过商路为合格的在岗专家提供 [ICON_Culture] 文化值。@SPC_METRIC@'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_4_HELP','Scholars draw on many fields to reinterpret Great Works and find inspiration in the art and customs of other civilizations.[NEWLINE][NEWLINE]Extended Meaning:[NEWLINE][ICON_BULLET] Eligible Great Works gain extra yields based on the infrastructure depth of this city''s qualifying district types. Theming bonuses apply. Dialogue of Eras boosts only the Great Works'' own Tourism. Government Plazas and Diplomatic Quarters currently grant no extra Culture through this ability.[NEWLINE][NEWLINE]Great Works Inspiration:[NEWLINE][ICON_BULLET] This city gains +3% [ICON_GreatPerson] Great Person points for each era represented in its eligible collection, up to +24%. Only types with base points in this city benefit.[NEWLINE][NEWLINE]Humanities Expedition:[NEWLINE][ICON_BULLET] Train a Humanities Expedition and send it to a foreign major civilization you have met. Your civilization can have 1 at a time. Each source city earns 1 Cultural Insight the first time each mission type succeeds in a given civilization.[NEWLINE][ICON_BULLET] Eligible Cultural Insights increase the source city''s [ICON_Tourism] Tourism. If that city collects all three types from a single civilization, Trade Routes can grant [ICON_Culture] Culture to eligible working specialists in connected cities.@SPC_METRIC@');

-- B233: read-only Industry history/typed knowledge, no new gameplay effect.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('en_US','LOC_SPC_INDUSTRY_HISTORY_BUTTON','工业历史 / 模板'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_HISTORY_BUTTON','工业历史 / 模板'),
('en_US','LOC_SPC_INDUSTRY_HISTORY_HINT','选中己方城市，查看本城奇观N、本文明时代E及模板；重复点击翻建筑页。关键结果自动写入有界日志。只读，不初始化或发放收益。'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_HISTORY_HINT','选中己方城市，查看本城奇观N、本文明时代E及模板；重复点击翻建筑页。关键结果自动写入有界日志。只读，不初始化或发放收益。');

-- B236: accepted Industry institution names; display only.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_1','匠作坊'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_1_HELP','工匠与劳动者在此聚集，将生产条件化为熟练的技艺。[NEWLINE][NEWLINE]基础专家支持：[NEWLINE][ICON_BULLET] 每名在岗工业专家额外提供 +3 [ICON_Food] 食物，并获得等同于本城工业区基础相邻加成的 [ICON_Production] 生产力，不计政策等倍率。'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_1','Artisans’ Workshop'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_1_HELP','Craftspeople gather here to share tools and perfect their trades.[NEWLINE][NEWLINE]Basic Specialist Support:[NEWLINE][ICON_BULLET] Each working Industry specialist provides +3 [ICON_Food] Food and [ICON_Production] Production equal to the Industrial Zone’s base adjacency bonus.'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_2','百工会馆'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_2_HELP','不同工种分工合作，共同培养城市的工程人才。[NEWLINE][NEWLINE]专业分工：[NEWLINE][ICON_BULLET] 本城工业区 +1 [ICON_Housing] 住房。每个已有合格普通建筑的等级再 +1，同级只计一次。[NEWLINE][ICON_BULLET] 每名在岗工业专家额外提供 +2 基础 [ICON_GreatEngineer] 大工程师点数。'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_2','Guildhall'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_2_HELP','The city’s trades work together and train new engineers.[NEWLINE][NEWLINE]Division of Labor:[NEWLINE][ICON_BULLET] Gain +1 [ICON_Housing] Housing from the Industrial Zone and +1 for each tier of eligible buildings it contains. Each tier counts once.[NEWLINE][ICON_BULLET] Each working Industry specialist provides +2 base [ICON_GreatEngineer] Great Engineer points.'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_3','工程局'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_3_HELP','工程师将建造经验编成规范，并组织施工队支援新的建设。[NEWLINE][NEWLINE]标准化：[NEWLINE][ICON_BULLET] 建造符合模板的区域和建筑时，+10% [ICON_Production] 生产力。模板可通过国内专业网络共享，同一目标只取最高加成。@SPC_METRIC@[NEWLINE][NEWLINE]施工队：[NEWLINE][ICON_BULLET] 解锁一级至三级施工队组建项目，工业启用三级时，组建成本为基础施工力的 150%。每个来源城市同时最多支持 2 支。[NEWLINE][ICON_BULLET] 消耗施工队，为当前在建奇观投入 [ICON_Production] 生产力。超出所需的部分不结转。'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_3','Engineering Bureau'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_3_HELP','Engineers turn construction experience into standards and organize crews for new projects.[NEWLINE][NEWLINE]Standardization:[NEWLINE][ICON_BULLET] +10% [ICON_Production] Production toward districts and buildings matching a template. Templates can be shared through the domestic specialization network. Only the highest bonus applies to a given target.@SPC_METRIC@[NEWLINE][NEWLINE]Construction Crews:[NEWLINE][ICON_BULLET] Unlocks the tier 1–3 Construction Crew projects. While Industry is active at Level 3, each crew costs 150% of its base Production contribution to form. Each source city can support up to 2 crews at a time.[NEWLINE][ICON_BULLET] Consume a crew to contribute [ICON_Production] Production to the Wonder the city is currently building. Excess Production does not carry over.'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_4','土木工程总局'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_4_HELP','工程师研习历代奇观的建造经验，把过去的巧思用到今天的大工程上。[NEWLINE][NEWLINE]工程传统：[NEWLINE][ICON_BULLET] 按本文明亲建奇观的所属时代计算。每涵盖一个时代，本城可研习一次。每次占用 1 个完整生产回合，完成后积累 1 层。[NEWLINE][ICON_BULLET] 四级启用时，每层成果使「标准化」的 [ICON_Production] 建造加成和合格建筑的购买折扣各提高 2 个百分点。@SPC_METRIC@[NEWLINE][NEWLINE]工程实践：[NEWLINE][ICON_BULLET] 解锁四级、五级施工队组建项目。本城累计建成 1、3、6 座奇观后，组建成本依次降至基础施工力的 140%、130%、120%。[NEWLINE][NEWLINE]巨构工程学：[NEWLINE][ICON_BULLET] 建造比本文明当前时代早 1、2 或至少 3 个时代的奇观时，分别获得 +10%、+20% 或 +30% [ICON_Production] 生产力。施工队的投入也享受此加成。'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_4','Directorate of Civil Engineering'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_4_HELP','Engineers study the Wonders of the past to inform the great works of today.[NEWLINE][NEWLINE]Engineering Tradition:[NEWLINE][ICON_BULLET] This city can complete 1 study for each distinct era of Wonders your civilization has built. Count each Wonder''s own era. Each study takes 1 full turn of Production.[NEWLINE][ICON_BULLET] While Industry is active at Level 4, each completed study raises the Standardization [ICON_Production] Production bonus and the purchase discount for eligible buildings by 2 percentage points each.@SPC_METRIC@[NEWLINE][NEWLINE]Engineering Practice:[NEWLINE][ICON_BULLET] Unlocks the tier 4 and 5 Construction Crew projects. At 1, 3, and 6 Wonders built in this city, crew costs fall to 140%, 130%, and 120% of their base Production contribution, respectively.[NEWLINE][NEWLINE]Macro-Engineering:[NEWLINE][ICON_BULLET] +10%, +20%, or +30% [ICON_Production] Production toward Wonders from 1, 2, or at least 3 eras before your civilization’s current era, respectively. This bonus also applies to Construction Crew contributions.');

-- B236 replaces old formation and general-construction wording exactly.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_DESCRIPTION','在城市当前建造的奇观地块上施工一次。标准速度下提供 260 点基础 [ICON_Production] 施工力，随游戏速度缩放，并在组建完成时锁定。适用的生产力加成可提高实际投入，溢出生产力不结转。[NEWLINE][NEWLINE]每个来源城市的当前所有者最多可保有 2 支本城组建的施工队。城市易主或失去组建资格后，已组建的队伍仍可使用。'),
('zh_Hans_CN','LOC_PROJECT_SPC_CREW_250_DESCRIPTION','组建一支一级施工队，标准速度下拥有 260 点基础 [ICON_Production] 施工力。[NEWLINE][NEWLINE]需要工业启用等级达到三级。开工时锁定成本，四级工业的「工程实践」可降低成本。成本和施工力随游戏速度缩放。每个来源城市的当前所有者最多可保有 2 支本城组建的施工队。'),
('en_US','LOC_UNIT_SPC_CREW_250_DESCRIPTION','Use once on the tile of a Wonder the city is building. Contributes 260 base [ICON_Production] Production at Standard Speed. The amount scales with game speed and locks when the Crew forms. Production bonuses can increase the contribution. Excess Production does not carry over.[NEWLINE][NEWLINE]Each source city supports up to 2 living Crews for its current owner. Formed Crews remain available if the city changes hands or loses eligibility.'),
('en_US','LOC_PROJECT_SPC_CREW_250_DESCRIPTION','Forms a Tier 1 Construction Crew with 260 base [ICON_Production] Production at Standard Speed.[NEWLINE][NEWLINE]Requires active Industry at Level 3 or higher. Cost locks at the start of production. At Active Level 4, Engineering Practice can reduce the cost. Cost and capacity scale with game speed. Each source city can support up to 2 living Crews for its current owner.'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_420_DESCRIPTION','在城市当前建造的奇观地块上施工一次。标准速度下提供 420 点基础 [ICON_Production] 施工力，随游戏速度缩放，并在组建完成时锁定。适用的生产力加成可提高实际投入，溢出生产力不结转。[NEWLINE][NEWLINE]每个来源城市的当前所有者最多可保有 2 支本城组建的施工队。城市易主或失去组建资格后，已组建的队伍仍可使用。'),
('zh_Hans_CN','LOC_PROJECT_SPC_CREW_420_DESCRIPTION','组建一支二级施工队，标准速度下拥有 420 点基础 [ICON_Production] 施工力。[NEWLINE][NEWLINE]需要工业启用等级达到三级。开工时锁定成本，四级工业的「工程实践」可降低成本。成本和施工力随游戏速度缩放。每个来源城市的当前所有者最多可保有 2 支本城组建的施工队。'),
('en_US','LOC_UNIT_SPC_CREW_420_DESCRIPTION','Use once on the tile of a Wonder the city is building. Contributes 420 base [ICON_Production] Production at Standard Speed. The amount scales with game speed and locks when the Crew forms. Production bonuses can increase the contribution. Excess Production does not carry over.[NEWLINE][NEWLINE]Each source city supports up to 2 living Crews for its current owner. Formed Crews remain available if the city changes hands or loses eligibility.'),
('en_US','LOC_PROJECT_SPC_CREW_420_DESCRIPTION','Forms a Tier 2 Construction Crew with 420 base [ICON_Production] Production at Standard Speed.[NEWLINE][NEWLINE]Requires active Industry at Level 3 or higher. Cost locks at the start of production. At Active Level 4, Engineering Practice can reduce the cost. Cost and capacity scale with game speed. Each source city can support up to 2 living Crews for its current owner.'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_750_DESCRIPTION','在城市当前建造的奇观地块上施工一次。标准速度下提供 750 点基础 [ICON_Production] 施工力，随游戏速度缩放，并在组建完成时锁定。适用的生产力加成可提高实际投入，溢出生产力不结转。[NEWLINE][NEWLINE]每个来源城市的当前所有者最多可保有 2 支本城组建的施工队。城市易主或失去组建资格后，已组建的队伍仍可使用。'),
('zh_Hans_CN','LOC_PROJECT_SPC_CREW_750_DESCRIPTION','组建一支三级施工队，标准速度下拥有 750 点基础 [ICON_Production] 施工力。[NEWLINE][NEWLINE]需要工业启用等级达到三级。开工时锁定成本，四级工业的「工程实践」可降低成本。成本和施工力随游戏速度缩放。每个来源城市的当前所有者最多可保有 2 支本城组建的施工队。'),
('en_US','LOC_UNIT_SPC_CREW_750_DESCRIPTION','Use once on the tile of a Wonder the city is building. Contributes 750 base [ICON_Production] Production at Standard Speed. The amount scales with game speed and locks when the Crew forms. Production bonuses can increase the contribution. Excess Production does not carry over.[NEWLINE][NEWLINE]Each source city supports up to 2 living Crews for its current owner. Formed Crews remain available if the city changes hands or loses eligibility.'),
('en_US','LOC_PROJECT_SPC_CREW_750_DESCRIPTION','Forms a Tier 3 Construction Crew with 750 base [ICON_Production] Production at Standard Speed.[NEWLINE][NEWLINE]Requires active Industry at Level 3 or higher. Cost locks at the start of production. At Active Level 4, Engineering Practice can reduce the cost. Cost and capacity scale with game speed. Each source city can support up to 2 living Crews for its current owner.'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_1000_DESCRIPTION','在城市当前建造的奇观地块上施工一次。标准速度下提供 1000 点基础 [ICON_Production] 施工力，随游戏速度缩放，并在组建完成时锁定。适用的生产力加成可提高实际投入，溢出生产力不结转。[NEWLINE][NEWLINE]每个来源城市的当前所有者最多可保有 2 支本城组建的施工队。城市易主或失去组建资格后，已组建的队伍仍可使用。'),
('zh_Hans_CN','LOC_PROJECT_SPC_CREW_1000_DESCRIPTION','组建一支四级施工队，标准速度下拥有 1000 点基础 [ICON_Production] 施工力。[NEWLINE][NEWLINE]需要工业启用等级达到四级。开工时锁定成本，四级工业的「工程实践」可降低成本。成本和施工力随游戏速度缩放。每个来源城市的当前所有者最多可保有 2 支本城组建的施工队。'),
('en_US','LOC_UNIT_SPC_CREW_1000_DESCRIPTION','Use once on the tile of a Wonder the city is building. Contributes 1,000 base [ICON_Production] Production at Standard Speed. The amount scales with game speed and locks when the Crew forms. Production bonuses can increase the contribution. Excess Production does not carry over.[NEWLINE][NEWLINE]Each source city supports up to 2 living Crews for its current owner. Formed Crews remain available if the city changes hands or loses eligibility.'),
('en_US','LOC_PROJECT_SPC_CREW_1000_DESCRIPTION','Forms a Tier 4 Construction Crew with 1,000 base [ICON_Production] Production at Standard Speed.[NEWLINE][NEWLINE]Requires active Industry at Level 4 or higher. Cost locks at the start of production. At Active Level 4, Engineering Practice can reduce the cost. Cost and capacity scale with game speed. Each source city can support up to 2 living Crews for its current owner.'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_1360_DESCRIPTION','在城市当前建造的奇观地块上施工一次。标准速度下提供 1360 点基础 [ICON_Production] 施工力，随游戏速度缩放，并在组建完成时锁定。适用的生产力加成可提高实际投入，溢出生产力不结转。[NEWLINE][NEWLINE]每个来源城市的当前所有者最多可保有 2 支本城组建的施工队。城市易主或失去组建资格后，已组建的队伍仍可使用。'),
('zh_Hans_CN','LOC_PROJECT_SPC_CREW_1360_DESCRIPTION','组建一支五级施工队，标准速度下拥有 1360 点基础 [ICON_Production] 施工力。[NEWLINE][NEWLINE]需要工业启用等级达到四级。开工时锁定成本，四级工业的「工程实践」可降低成本。成本和施工力随游戏速度缩放。每个来源城市的当前所有者最多可保有 2 支本城组建的施工队。'),
('en_US','LOC_UNIT_SPC_CREW_1360_DESCRIPTION','Use once on the tile of a Wonder the city is building. Contributes 1,360 base [ICON_Production] Production at Standard Speed. The amount scales with game speed and locks when the Crew forms. Production bonuses can increase the contribution. Excess Production does not carry over.[NEWLINE][NEWLINE]Each source city supports up to 2 living Crews for its current owner. Formed Crews remain available if the city changes hands or loses eligibility.'),
('en_US','LOC_PROJECT_SPC_CREW_1360_DESCRIPTION','Forms a Tier 5 Construction Crew with 1,360 base [ICON_Production] Production at Standard Speed.[NEWLINE][NEWLINE]Requires active Industry at Level 4 or higher. Cost locks at the start of production. At Active Level 4, Engineering Practice can reduce the cost. Cost and capacity scale with game speed. Each source city can support up to 2 living Crews for its current owner.'),
('zh_Hans_CN','LOC_SPC_CREW_FORMATION_HELP','本次开工锁价。同一玩家从每座来源城市最多保有2支存活施工队；队列中的施工队会预留名额。仅用于奇观，剩余施工力不结转。'),
('en_US','LOC_SPC_CREW_FORMATION_HELP','Price locks when ordered. Each player may have two surviving Crews from a source city; queued orders reserve capacity. Wonders only; unused transfer Production is discarded.');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CREW_FORMATION_ERROR','组建未确认：{1}。请查看工业报告或回传日志。'),
('en_US','LOC_SPC_CREW_FORMATION_ERROR','Could not confirm Crew formation ({1}). See the Industry report.');

-- B237 continuation labels; B238/D0053 base-input presentation below.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CREW_RESUME_NAME','{1_Name}（续建）'),
('en_US','LOC_SPC_CREW_RESUME_NAME','{1_Name} (resume)'),
('zh_Hans_CN','LOC_SPC_CREW_LOCKED_PRICE','已锁定成本：{1_Cost} [ICON_Production] 生产力。续建沿用已有进度。'),
('en_US','LOC_SPC_CREW_LOCKED_PRICE','Locked cost: {1_Cost} [ICON_Production] Production. Resume to continue from the saved progress.');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CREW_BASE_PREVIEW','已锁定基础施工力：{1_Capacity}[NEWLINE]本次投入基础施工力：{2_Input} ｜ 剩余未使用基础施工力：{3_Unused}[NEWLINE]实际转化的生产力可享受适用加成；未使用的余量不会结转。'),
('en_US','LOC_SPC_CREW_BASE_PREVIEW','Base capacity: {1_Capacity} [ICON_Production] Production[NEWLINE]Base contribution: {2_Input}[NEWLINE]Unused: {3_Unused}[NEWLINE]Applicable Production modifiers can increase the contribution. Excess Production does not carry over.'),
('zh_Hans_CN','LOC_SPC_CREW_BASE_CONFIRM','消耗此施工队，为当前正在建造的奇观投入 {1_Input} 点基础生产力（实际转化量可享受适用生产力加成）。[NEWLINE]此操作一旦确认无法撤销。'),
('en_US','LOC_SPC_CREW_BASE_CONFIRM','Consume this Construction Crew to contribute {1_Input} base [ICON_Production] Production to the Wonder the city is currently building. Applicable Production modifiers can increase the contribution.[NEWLINE]This cannot be undone.'),
('zh_Hans_CN','LOC_SPC_CREW_BASE_READY','已锁定基础施工力：{1_Capacity}（可享受适用的生产力加成）。[NEWLINE]点击以预览详情并确认施工。'),
('en_US','LOC_SPC_CREW_BASE_READY','Base capacity: {1_Capacity} [ICON_Production] Production. Applicable Production modifiers can increase the contribution.[NEWLINE]Select Construct to preview the contribution.');

-- B239: unfinished paid formation retains capacity.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CREW_OCCUPANCY','本城名额：{1} 支现存施工队，{2} 项未完成组建（{3} 项暂停）。'),
('zh_Hans_CN','LOC_SPC_CREW_RESUME_CAPACITY_HELD','施工队名额已满。开工成本和进度已保留，空出名额后可继续组建。'),
('zh_Hans_CN','LOC_SPC_CREW_FORMATION_HELP','现存施工队和未完成的组建共用本城名额。续建沿用已锁定的成本与进度。'),
('en_US','LOC_SPC_CREW_OCCUPANCY','This city’s slots: {1} living Crews, {2} unfinished formations ({3} paused).'),
('en_US','LOC_SPC_CREW_RESUME_CAPACITY_HELD','Crew slots are full. Cost and progress are saved. Resume when a slot opens.'),
('en_US','LOC_SPC_CREW_FORMATION_HELP','Living Crews and unfinished formations share this city’s slots. Resuming a formation keeps its cost and progress.');

-- B251 institution preview and bounded live summaries.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSTITUTION_PREVIEW','尚未建立');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSTITUTION_PREVIEW','Not yet established');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_TRADITION','学术传统');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_TRADITION','Academic Tradition');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_REPUTATION','商业信誉');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_REPUTATION','Commercial Reputation');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_DIALOGUE','时代对话');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_DIALOGUE','Dialogue of Eras');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_EXPEDITION','人文考察团');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_EXPEDITION','Humanities Expedition');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_ENGINEERING','工程传统');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_ENGINEERING','Engineering Tradition');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_STANDARDIZATION','标准化');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_STANDARDIZATION','Standardization');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_PENDING','当前数值待确认');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_PENDING','Value awaiting confirmation');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_PENDING_SHORT','待确认');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_PENDING_SHORT','Pending');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_NOT_STARTED','尚未开始积累');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_NOT_STARTED','Accumulation has not started');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_TRADITION_VALUE','已累计 {1} 回合；[ICON_Science]学术传统倍率 +{2}%。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_TRADITION_VALUE','Accumulated turns: {1}[NEWLINE]Academic Tradition at Active Level 4: +{2}% [ICON_Science] Science.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_TRADITION_NEXT','距下一档还需 {1} 回合。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_TRADITION_NEXT','{1} turns until the next threshold.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_ACCUMULATION_PAUSED','积累已暂停，历史保留。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_ACCUMULATION_PAUSED','Accumulation paused. History retained.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_REPUTATION_VALUE','已累计信誉 {1}/40；[ICON_Gold]商业化增幅 +{2}%。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_REPUTATION_VALUE','Accumulated Reputation {1}/40. [ICON_Gold] Commercialization bonus at Active Level 4: +{2}%.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_DIALOGUE_VALUE','[ICON_Tourism]已累计巨作旅游业绩倍率：+{1}%。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_DIALOGUE_VALUE','Accumulated bonus: +{1}% [ICON_Tourism] Tourism from Great Works.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_INSIGHTS_VALUE','文化见闻：{1} 份。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_INSIGHTS_VALUE','Cultural Insights: {1}');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_ENGINEERING_VALUE','已完成研习：{1} 层。[NEWLINE]四级启用时：[ICON_Production]标准化建造加成与合格建筑[ICON_Gold]金币折扣各增强 {2} 个百分点。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_ENGINEERING_VALUE','Completed study levels: {1}[NEWLINE]At Active Level 4, the [ICON_Production] Standardization bonus and eligible building [ICON_Gold] Gold discount each gain {2} percentage points.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_TEMPLATES_VALUE','本城已记录模板：建筑 {1} 项，区域 {2} 项。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_TEMPLATES_VALUE','Templates recorded: {1} buildings, {2} districts.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_STANDARDIZATION_VALUE','本城当前提供：[ICON_Production]生产力 +{1}%，合格建筑[ICON_Gold]金币购买折扣 {2}%。[NEWLINE]不含区域购买折扣。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_STANDARDIZATION_VALUE','Matching templates: +{1}% [ICON_Production] Production[NEWLINE]Eligible buildings: {2}% [ICON_Gold] Gold discount.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_STANDARDIZATION_PAUSED','本城当前不提供标准化加成；已记录模板保留。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_STANDARDIZATION_PAUSED','This city does not currently provide Standardization bonuses. Recorded templates are retained.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_ACTIVE_PENDING','当前启用等级暂待确认');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_ACTIVE_PENDING','Active Level awaiting confirmation');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_LEGACY_HELP','曾建立的历史机构（当前已脱离该专业，不提供对应能力）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_LEGACY_HELP','A historical institution from a former specialization. Its abilities are not active.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_PREVIEW_HELP','未来机构预览：专业潜力达到 {1} 级后建立；尚未授予本级能力。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_PREVIEW_HELP','Established at Potential Level {1}.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_ACTIVE_HELP','已达到本级机构的启用等级（具体收益仍需满足各能力的对应条件）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_ACTIVE_HELP','This institution is active. Individual abilities may have additional requirements.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_INACTIVE_HELP','尚未满足本级机构的启用条件（已建成的机构仍予以保留）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_INACTIVE_HELP','This institution is established. Its abilities require a higher Active Level.');

-- B264: native-style institution presentation; no gameplay definitions.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_INST_LEVEL_1','一'),
('en_US','LOC_SPC_INST_LEVEL_1','1'),
('zh_Hans_CN','LOC_SPC_INST_LEVEL_2','二'),
('en_US','LOC_SPC_INST_LEVEL_2','2'),
('zh_Hans_CN','LOC_SPC_INST_LEVEL_3','三'),
('en_US','LOC_SPC_INST_LEVEL_3','3'),
('zh_Hans_CN','LOC_SPC_INST_LEVEL_4','四'),
('en_US','LOC_SPC_INST_LEVEL_4','4'),
('zh_Hans_CN','LOC_SPC_INST_CATEGORY','{1}专业·{2}级机构'),
('en_US','LOC_SPC_INST_CATEGORY','{1} Specialization · Level {2} Institution'),
('zh_Hans_CN','LOC_SPC_INST_REQUIREMENT','启用需求：{1}专业启用等级达到{2}级。'),
('en_US','LOC_SPC_INST_REQUIREMENT','Requires {1} active at Level {2}.'),
('zh_Hans_CN','LOC_SPC_INST_STATE','当前状态：{1}'),
('en_US','LOC_SPC_INST_STATE','Current status: {1}'),
('zh_Hans_CN','LOC_SPC_INST_RESEARCH','科研'),
('en_US','LOC_SPC_INST_RESEARCH','Research'),
('zh_Hans_CN','LOC_SPC_INST_CULTURE','文化'),
('en_US','LOC_SPC_INST_CULTURE','Culture'),
('zh_Hans_CN','LOC_SPC_INST_INDUSTRY','工业'),
('en_US','LOC_SPC_INST_INDUSTRY','Industry'),
('zh_Hans_CN','LOC_SPC_INST_COMMERCE','商业'),
('en_US','LOC_SPC_INST_COMMERCE','Commerce'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_1','学者结社'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_1','Scholarly Circle'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_1_HELP','学者在此结社研习，为城市的科研事业奠定基础。[NEWLINE][NEWLINE]基础专家支持：[NEWLINE]每名在岗科研专家额外提供 +3 [ICON_Food] 食物和 +3 [ICON_Production] 生产力。'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_1_HELP','Scholars gather here to study and lay the groundwork for the city''s research.[NEWLINE][NEWLINE]Basic Specialist Support:[NEWLINE]Each working Research specialist provides +3 [ICON_Food] Food and +3 [ICON_Production] Production.'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_2','研修院'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_2','Institute of Inquiry'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_2_HELP','系统的研修与人才培养，让科研成为城市的长期事业。[NEWLINE][NEWLINE]人才培养：[NEWLINE][ICON_BULLET] 每名在岗科研专家额外提供 +2 基础 [ICON_GreatScientist] 大科学家点数。[NEWLINE][ICON_BULLET] 本城学院及其每一级合格建筑各 +1 [ICON_Housing] 住房。'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_2_HELP','With places to study and train, scholars make research a lasting pursuit.[NEWLINE][NEWLINE]Scholarly Training:[NEWLINE][ICON_BULLET] Each working Research specialist provides +2 base [ICON_GreatScientist] Great Scientist points.[NEWLINE][ICON_BULLET] Gain +1 [ICON_Housing] Housing from the Campus and +1 for each tier of eligible buildings it contains.'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_3','学术联合会'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_3','Research Consortium'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_3_HELP','不同领域在此交流，让研究成果与城市实践相互促进。[NEWLINE][NEWLINE]跨学科研究：[NEWLINE][ICON_BULLET] 本城学院以外已建成且未遭掠夺的合格专业区域，其基础相邻产出总和的 50% 转化为 [ICON_Science] 科技值。[NEWLINE][NEWLINE]学以致用：[NEWLINE][ICON_BULLET] 每名在岗科研专家从本城其他合格专业领域获得额外产出，数量取决于各领域的基础设施深度。'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_3_HELP','Scholars bring discoveries from different fields into everyday use.[NEWLINE][NEWLINE]Interdisciplinary Research:[NEWLINE][ICON_BULLET] Gain [ICON_Science] Science equal to 50% of the combined base adjacency yields of this city’s other eligible specialization districts. Only completed, unpillaged districts count.[NEWLINE][NEWLINE]Applied Learning:[NEWLINE][ICON_BULLET] Each working Research specialist gains yields from this city’s other eligible specialization fields. The yields increase with each field’s infrastructure depth.'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_4','学术总署'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_4','Academic Directorate'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_4_HELP','完备的学院设施让学者得以深入研究，学术传统也随岁月积累。[NEWLINE][NEWLINE]科研基础设施：[NEWLINE][ICON_BULLET] 本城学院每 1 点基础设施深度，使每名在岗科研专家额外提供 +1 基础 [ICON_Science] 科技值，最高 +10。[NEWLINE][NEWLINE]学术主持：[NEWLINE][ICON_BULLET] 每名在岗科研专家使本城每座完好的普通学院一至四级建筑 +1 基础 [ICON_Science] 科技值。[NEWLINE][NEWLINE]学术传统：[NEWLINE][ICON_BULLET] 科研潜力达到四级后开始积累。四级启用时，本城初始 +5% [ICON_Science] 科技值。[NEWLINE][ICON_BULLET] 保有科研身份时持续积累，即使暂未启用四级。转出科研后暂停，转回后继续积累。标准速度下，每累计 10 回合再提高 5 个百分点，最高 +25%。@SPC_METRIC@'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_4_HELP','Well-equipped campuses support deeper inquiry and a lasting tradition of scholarship.[NEWLINE][NEWLINE]Research Infrastructure:[NEWLINE][ICON_BULLET] Each working Research specialist provides +1 base [ICON_Science] Science per point of infrastructure depth in this city''s Campus, up to +10 per specialist.[NEWLINE][NEWLINE]Academic Stewardship:[NEWLINE][ICON_BULLET] Each working Research specialist adds +1 base [ICON_Science] Science to each eligible, unpillaged tier 1–4 Campus building in this city.[NEWLINE][NEWLINE]Academic Tradition:[NEWLINE][ICON_BULLET] This city starts building Academic Tradition when its Research Potential reaches Level 4. It continues as long as the city specializes in Research, even while Level 4 is inactive. Progress pauses if the city leaves Research and resumes if it returns.[NEWLINE][ICON_BULLET] With Research active at Level 4, this city gains +5% [ICON_Science] Science, plus 5 percentage points for every 10 accumulated turns at Standard Speed, up to +25%.@SPC_METRIC@');

-- B265: native city-panel shortcut; the badge numeral always represents ACTIVE.
INSERT OR REPLACE INTO LocalizedText (Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CITY_INSTITUTION_SHORTCUT','{1}专业 · 启用等级 {2}[NEWLINE]打开城市详情：专业机构、建筑、区域与奇观。'),
('en_US','LOC_SPC_CITY_INSTITUTION_SHORTCUT','{1}专业 · 启用等级 {2}[NEWLINE]打开城市详情：专业机构、建筑、区域与奇观。');

-- Production queue status labels and explanations.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_LABEL_UNAVAILABLE','暂不可用'),
('en_US','LOC_SPC_TIMED_QUEUE_LABEL_UNAVAILABLE','Unavailable'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_LABEL_WAITING_TO_QUEUE','待入队'),
('en_US','LOC_SPC_TIMED_QUEUE_LABEL_WAITING_TO_QUEUE','Awaiting queue'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_LABEL_INELIGIBLE','不可开始'),
('en_US','LOC_SPC_TIMED_QUEUE_LABEL_INELIGIBLE','Unavailable'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_LABEL_VERIFYING','待确认'),
('en_US','LOC_SPC_TIMED_QUEUE_LABEL_VERIFYING','Awaiting confirmation'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_LABEL_PAUSED','已暂停'),
('en_US','LOC_SPC_TIMED_QUEUE_LABEL_PAUSED','Paused'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_LABEL_ALREADY_QUEUED','已排队'),
('en_US','LOC_SPC_TIMED_QUEUE_LABEL_ALREADY_QUEUED','Queued'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_LABEL_UNCONFIRMED','待确认'),
('en_US','LOC_SPC_TIMED_QUEUE_LABEL_UNCONFIRMED','Awaiting confirmation'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_LABEL_QUEUED','排队中'),
('en_US','LOC_SPC_TIMED_QUEUE_LABEL_QUEUED','Queued'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_LABEL_WAITING_TO_START','待开始'),
('en_US','LOC_SPC_TIMED_QUEUE_LABEL_WAITING_TO_START','Awaiting start'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_LABEL_CONFIRMING','确认中'),
('en_US','LOC_SPC_TIMED_QUEUE_LABEL_CONFIRMING','Confirming'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_CANDIDATE_LIMIT','当前排队候选已达安全容量上限；请保留日志。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_CANDIDATE_LIMIT','Too many pending project requests. Keep the logs.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_STUDY_KNOWLEDGE_REACHED','本城已完成所有可研习的经验。若队列中仍有项目，请移除。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_STUDY_KNOWLEDGE_REACHED','All available studies are complete. Remove this project if it is still queued.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_DIALOGUE_ERA_USED','本游戏时代的时代对话已完成。若队列中仍有项目，请移除。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_DIALOGUE_ERA_USED','Dialogue of Eras is complete for this era. Remove this project if it is still queued.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_INELIGIBLE','当前专业资格不满足，项目不会计时或产生收益。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_INELIGIBLE','The city does not meet the requirements for this project.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_QUEUE_REQUEST_PENDING','入队请求待确认，不会重复加入。请等待队列更新。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_QUEUE_REQUEST_PENDING','Waiting for the queue to confirm the request.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_CANNOT_CONFIRM_SELECTION','生产队列待确认，请稍后重新选择。不会重复加入项目。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_CANNOT_CONFIRM_SELECTION','Could not confirm the queue. Select the project again later.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_DUPLICATE_PROJECT','队列中有重复项目，请只保留一项。不会重复发放收益。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_DUPLICATE_PROJECT','Keep only one copy in the Production queue. The reward can be granted only once.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_ALREADY_QUEUED','项目已在队列中，不会重复加入。成为唯一当前项目后才开始计时。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_ALREADY_QUEUED','Already queued. Timing starts when this is the only item in the queue.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_QUEUE_INSERT_PENDING','等待生产队列确认；尚未开始计时。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_QUEUE_INSERT_PENDING','Waiting for the queue. The timer has not started.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_ALREADY_COMPLETED_THIS_TURN','本回合已有完成记录，无法确认此队列项是否为新一轮。请重新选择项目。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_ALREADY_COMPLETED_THIS_TURN','Could not verify this as a new attempt after this turn’s completion. Select the project again.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_QUEUE_UNCONFIRMED','生产队列待确认。请等待相关状态更新，项目暂不结算。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_QUEUE_UNCONFIRMED','Waiting to confirm the Production queue. The project cannot complete yet.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_REQUIRES_SOLE_ENTRY','项目须独占生产队列。移除其他项目后自动核对计时。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_REQUIRES_SOLE_ENTRY','Remove the other items from the Production queue so the game can check the timer again.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_WAITS_TURN_IN_QUEUE','项目尚未成为唯一当前目标，不会计时。轮到时自动核对。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_WAITS_TURN_IN_QUEUE','The game checks the timer when this becomes the only item in the Production queue.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_WAITING_FOR_NEXT_TURN','本回合已结束。须等到下一回合确认可开始后才计时。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_WAITING_FOR_NEXT_TURN','Timing can start when your next turn is available.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_WAITING_FOR_ACTIVE_TURN','等待本地回合可操作状态确认。排队时间不计入项目。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_WAITING_FOR_ACTIVE_TURN','Timing waits until your turn is available. Time spent queued does not count.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_CONFIRMING_FULL_TURN','正在确认完整回合计时。不会重复提交本轮。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_CONFIRMING_FULL_TURN','Confirming the start of the 1-turn timer.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_START_REQUEST_UNCONFIRMED','启动请求结果待确认。状态没有变化时，系统会等待确认。请保留日志。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_START_REQUEST_UNCONFIRMED','Could not confirm the start request. Keep the logs.'),
('zh_Hans_CN','LOC_SPC_TIMED_QUEUE_HELP_AWAITING_PROJECT_FACTS','等待专业资格与计时状态确认。'),
('en_US','LOC_SPC_TIMED_QUEUE_HELP_AWAITING_PROJECT_FACTS','Waiting to confirm eligibility and the project timer.');

-- Timed project previews, current status and production progress text.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_CLAIM_PREVIEW','项目须持续 1 个完整回合，完成后才确立专业。未分配及项目期间产生的生产力不会结转。'),
('en_US','LOC_SPC_TIMED_PROJECT_CLAIM_PREVIEW','Complete 1 full turn to establish the specialization. Unassigned Production and Production earned during this project do not carry over.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_CLAIM_START_PENDING','等待项目状态确认。若持续如此，请查看当前项目提示。'),
('en_US','LOC_SPC_TIMED_PROJECT_CLAIM_START_PENDING','Waiting to confirm the project start.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_DIALOGUE_PREVIEW','时代对话需持续 1 个完整生产回合。完成时，本城合格馆藏每涵盖一个作品时代，巨作原生 [ICON_Tourism] 旅游业绩加成永久累积 5 个百分点。加成在文化启用等级达到三级时生效。'),
('en_US','LOC_SPC_TIMED_PROJECT_DIALOGUE_PREVIEW','Complete 1 full turn. Each distinct era in this city’s eligible collection permanently adds 5 percentage points to its bonus to original [ICON_Tourism] Tourism from Great Works.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_DIALOGUE_TIMER_PENDING','待计时'),
('en_US','LOC_SPC_TIMED_PROJECT_DIALOGUE_TIMER_PENDING','Awaiting start'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_DIALOGUE_START_PENDING','此项目须独占生产队列并持续 1 个完整回合。计时待确认，确认前不会完成项目。'),
('en_US','LOC_SPC_TIMED_PROJECT_DIALOGUE_START_PENDING','Keep Dialogue of Eras alone in the Production queue for 1 full turn. Timing is awaiting confirmation.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_STUDY_ACTIVE','工程传统研习：完成 1 个完整生产回合后，本城永久积累 1 层成果。'),
('en_US','LOC_SPC_TIMED_PROJECT_STUDY_ACTIVE','Complete 1 full turn to gain 1 permanent study level in this city.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_STUDY_COMPLETION_PENDING','原生完成回执待确认；不会重复发放。'),
('en_US','LOC_SPC_TIMED_PROJECT_STUDY_COMPLETION_PENDING','Waiting to confirm completion. The study level can be granted only once.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_STUDY_REQUIRES_SOLE_ENTRY','工程传统研习须独占生产队列。移除其他项目后自动核对计时。'),
('en_US','LOC_SPC_TIMED_PROJECT_STUDY_REQUIRES_SOLE_ENTRY','Remove the other items from the Production queue so the game can check the timer again.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_STUDY_PAUSED','研习未确认，请查看工业历史报告。'),
('en_US','LOC_SPC_TIMED_PROJECT_STUDY_PAUSED','Could not confirm the study. See the Industry History report.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_STUDY_START_PENDING','请选择为唯一当前项目。中断后须重新选择。'),
('en_US','LOC_SPC_TIMED_PROJECT_STUDY_START_PENDING','Keep this project alone in the Production queue. Select it again after an interruption.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_STUDY_PREVIEW','需要工业启用等级达到四级，且本城研习层数少于本文明亲建奇观覆盖的时代数。中断会取消本轮。'),
('en_US','LOC_SPC_TIMED_PROJECT_STUDY_PREVIEW','Requires Industry active at Level 4 and an unused study opportunity. Wonders your civilization built provide one opportunity per distinct era.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_TIMER_ACTIVE','计时已开启：1回合'),
('en_US','LOC_SPC_TIMED_PROJECT_TIMER_ACTIVE','Timer started: 1 turn'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_TIMER_STATUS','计时：{1}'),
('en_US','LOC_SPC_TIMED_PROJECT_TIMER_STATUS','Timer: {1}');

-- Construction Crew and Settler action tooltips.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_UNIT_CREW_PREVIEW','施工预览[NEWLINE]当前目标：{1_Wonder}[NEWLINE]当前进度：{2_Progress} / {3_Cost}[NEWLINE]{4_Preview}'),
('en_US','LOC_SPC_UNIT_CREW_PREVIEW','Construction Preview[NEWLINE]Current Wonder: {1_Wonder}[NEWLINE]Progress: {2_Progress} / {3_Cost}[NEWLINE]{4_Preview}'),
('zh_Hans_CN','LOC_SPC_UNIT_CREW_CONFIRM','确认施工[NEWLINE]{1_Confirmation}'),
('en_US','LOC_SPC_UNIT_CREW_CONFIRM','Confirm Construction[NEWLINE]{1_Confirmation}'),
('zh_Hans_CN','LOC_SPC_UNIT_CREW_CONFIRM_TITLE','确认施工'),
('en_US','LOC_SPC_UNIT_CREW_CONFIRM_TITLE','Confirm Construction'),
('zh_Hans_CN','LOC_SPC_UNIT_CREW_READY','施工[NEWLINE]{1_Ready}'),
('en_US','LOC_SPC_UNIT_CREW_READY','Construct[NEWLINE]{1_Ready}'),
('zh_Hans_CN','LOC_SPC_UNIT_CREW_SITE','施工[NEWLINE]将施工队移动至正在建造奇观的单元格，即可预览施工。'),
('en_US','LOC_SPC_UNIT_CREW_SITE','Construct[NEWLINE]Move the Crew to the tile of the Wonder the city is building to preview its contribution.'),
('zh_Hans_CN','LOC_SPC_UNIT_INVEST_PREVIEW','专业投资预览[NEWLINE]当前专业：{1_Profession}[NEWLINE]当前潜力：{2_Potential}级[NEWLINE]投资后潜力：{3_Next}级[NEWLINE]本次消耗：1 名移民[NEWLINE][NEWLINE]更高等级的专业能力仍需满足相应的总督就职与晋升条件。'),
('en_US','LOC_SPC_UNIT_INVEST_PREVIEW','Specialization Investment Preview[NEWLINE]Current specialization: {1_Profession}[NEWLINE]Current Potential: Level {2_Potential}[NEWLINE]Potential after investment: Level {3_Next}[NEWLINE]Cost: 1 Settler[NEWLINE][NEWLINE]Higher-level abilities still require an established Governor with the appropriate promotions.'),
('zh_Hans_CN','LOC_SPC_UNIT_INVEST_CONFIRM','确认专业投资[NEWLINE]消耗此移民，将本城专业潜力永久提升至 {1_Next} 级。[NEWLINE]确认后无法撤销。'),
('en_US','LOC_SPC_UNIT_INVEST_CONFIRM','Confirm Specialization Investment[NEWLINE]Consume this Settler to permanently increase this city’s Potential to Level {1_Next}.[NEWLINE]This cannot be undone.'),
('zh_Hans_CN','LOC_SPC_UNIT_INVEST_CONFIRM_TITLE','确认投资'),
('en_US','LOC_SPC_UNIT_INVEST_CONFIRM_TITLE','Confirm Investment'),
('zh_Hans_CN','LOC_SPC_UNIT_INVEST_READY','投资专业化[NEWLINE]消耗 1 名移民，使本城专业潜力永久提升 1 级。[NEWLINE]潜力变化：{1_Potential} 级 → {2_Next} 级[NEWLINE]点击查看投资预览，再确认投资。'),
('en_US','LOC_SPC_UNIT_INVEST_READY','Invest in Specialization[NEWLINE]Consume 1 Settler to permanently raise this city’s Potential by 1 level.[NEWLINE]Potential: Level {1_Potential} → Level {2_Next}[NEWLINE]Select to preview the investment.'),
('zh_Hans_CN','LOC_SPC_UNIT_INVEST_FULL','投资专业化[NEWLINE]专业潜力已达 4 级，无法继续投资。'),
('en_US','LOC_SPC_UNIT_INVEST_FULL','Invest in Specialization[NEWLINE]This city has reached Potential Level 4.'),
('zh_Hans_CN','LOC_SPC_UNIT_INVEST_PENDING','投资专业化[NEWLINE]上一次投资结果待确认，暂时无法再次投资。'),
('en_US','LOC_SPC_UNIT_INVEST_PENDING','Invest in Specialization[NEWLINE]The previous investment is awaiting confirmation.'),
('zh_Hans_CN','LOC_SPC_UNIT_INVEST_SITE','投资专业化[NEWLINE]将移民移动至本城的专业区域，即可预览投资。'),
('en_US','LOC_SPC_UNIT_INVEST_SITE','Invest in Specialization[NEWLINE]Move a Settler to this city’s specialization district to preview the investment.'),
('zh_Hans_CN','LOC_SPC_UNIT_INVEST_GOVERNMENT','政府'),
('en_US','LOC_SPC_UNIT_INVEST_GOVERNMENT','Government'),
('zh_Hans_CN','LOC_SPC_UNIT_INVEST_MILITARY','军事'),
('en_US','LOC_SPC_UNIT_INVEST_MILITARY','Military');

-- Timed project captions in the native city panel.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_CITY_PANEL_TURNS','回合后完成'),
('en_US','LOC_SPC_TIMED_PROJECT_CITY_PANEL_TURNS','turn remaining'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_CITY_PANEL_TITLE','计时项目'),
('en_US','LOC_SPC_TIMED_PROJECT_CITY_PANEL_TITLE','Project Timer');

-- Existing Claim and Era Dialogue notes, translated when displayed.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CURRENT_PRODUCTION_UNKNOWN','当前生产不可读'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CURRENT_PRODUCTION_UNKNOWN','Current production is awaiting confirmation.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_ACTIVE','1回合；保存读档继续计时'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_ACTIVE','1 full turn. An eligible saved timer can resume after loading.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_SWITCHED','已改选目标；重新选择须完整占用一回合'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_SWITCHED','Production changed. Select the project again for 1 full turn.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_QUEUE_UNKNOWN','当前队列未确认；不完成项目'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_QUEUE_UNKNOWN','Waiting to confirm the Production queue. The project cannot complete yet.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_WINDOW_MISSED','错过完整回合窗口；请重新选择'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_WINDOW_MISSED','Select this project again to start a full turn.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_QUEUE_FACT_REQUIRED','当前队列未确认；等待相关事件，不完成项目'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_QUEUE_FACT_REQUIRED','Waiting to confirm the Production queue. The project cannot complete yet.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_NO_TIMER','当前项目没有计时；请先改选普通目标，再重选认领项目，重新占用完整一回合'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_NO_TIMER','The timer has not started. Select another production target, then select the claim project again.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_DIFFERENT_CLAIM','改选另一认领项目'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_DIFFERENT_CLAIM','Another claim project was selected.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_TARGET_CHANGED','当前目标已改变'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_TARGET_CHANGED','The current production target changed.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_FULL_TURN_UNCONFIRMED','未确认完整生产回合；请重新选择'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_FULL_TURN_UNCONFIRMED','A full turn of production could not be confirmed. Select the project again.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_COMPLETION_PENDING','等待原生完成事件；结果未知时不重复调用'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_COMPLETION_PENDING','Completion is awaiting confirmation. The request is sent only once.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_RESTART','已改选目标；需重新占用完整回合'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_RESTART','The production target changed. Select the project again to start a full turn.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_DISTRICT_UNAVAILABLE','找不到对应已完成区域；暂停认领'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_DISTRICT_UNAVAILABLE','Claim paused. Could not find the required completed district.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_SOLE_QUEUE','认领项目不能排在队列后面；请选为唯一当前目标'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_SOLE_QUEUE','Select the claim project as the only item in the Production queue.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_TARGET_PENDING','等待原生选择确认'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_TARGET_PENDING','Waiting to confirm the production target.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_RELOAD_PENDING','读档同步等待确认；不会自动重发'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_RELOAD_PENDING','Waiting to verify the project after loading.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_START_TIMEOUT','启动确认超时；请重新选择项目'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_START_TIMEOUT','The project start was not confirmed. Select it again.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_ACTIVE','完整一回合计时中'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_ACTIVE','The 1-turn timer has started.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_SOLE_QUEUE','时代对话必须为唯一当前生产目标'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_SOLE_QUEUE','Keep Dialogue of Eras alone in the Production queue.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_ELIGIBILITY_UNKNOWN','当前资格尚不可确认；未清除历史，也不完成项目'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_ELIGIBILITY_UNKNOWN','Waiting to confirm eligibility. Recorded history is retained and the project cannot complete yet.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_FACT_REQUIRED','当前资格或生产未确认；等待相关事件，不完成项目'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_FACT_REQUIRED','Waiting to confirm eligibility or production. The project cannot complete yet.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_COMPLETION_PENDING','原生完成已请求；结果不明时不重复调用'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_COMPLETION_PENDING','Completion was requested. The request is sent only once.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_COMPLETION_SOURCE_UNKNOWN','完成来源已不确定；不重放或补取之后的馆藏'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_COMPLETION_SOURCE_UNKNOWN','Could not confirm completion. The collection will not be checked again for this attempt.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_COLLECTION_UNKNOWN','完成时事实未确认；不以之后的馆藏补算'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_DIALOGUE_COLLECTION_UNKNOWN','Could not confirm the collection at completion. Later changes do not count toward this attempt.'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_SOLE_QUEUE_COUNT','认领必须为唯一当前目标；队列数量={1}'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_SOLE_QUEUE_COUNT','Keep the claim project alone in the Production queue. Items queued: {1}'),
('zh_Hans_CN','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_QUEUE_COUNT_PENDING','等待队列确认；数量={1}'),
('en_US','LOC_SPC_TIMED_PROJECT_REASON_CLAIM_QUEUE_COUNT_PENDING','Waiting for the Production queue. Items queued: {1}');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('en_US','LOC_SPC_UNIT_ACTION_CONFIRM_LABEL','Confirm'),
('zh_Hans_CN','LOC_SPC_UNIT_ACTION_CONFIRM_LABEL','确认');
