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

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_250_NAME','一级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_UNIT_SPC_CREW_250_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 一级施工队可提供260点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_250_NAME','组建一级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_PROJECT_SPC_CREW_250_DESCRIPTION','Industry ACTIVE III. Standard speed: 390 Production creates one 260-Production Crew. Both cost and output scale with game speed.');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_NAME','一级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_DESCRIPTION','施工队拥有1点劳动力。可消耗1点劳动力，在区域、建筑或奇观所在的单元格进行施工，为其提供生产力。[NEWLINE]• 一级施工队可提供260点生产力。[NEWLINE]• 超出当前建造项目剩余需求的生产力将被浪费。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_250_NAME','组建一级施工队');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_PROJECT_SPC_CREW_250_DESCRIPTION','工业ACTIVE III开放。标准速度：基础成本390生产力，生成1支260生产力的施工队。成本与生产力随游戏速度同比缩放。');
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
('zh_Hans_CN','LOC_SPC_CULTURE_INSIGHTS_TOOLTIP','查看所选己方城市的历史文化见闻与当前有效见闻。'),
('en_US','LOC_SPC_CULTURE_INSIGHTS_TOOLTIP','View recorded and currently effective Insights for the selected owned city. Citywide Tourism and network effects are not implemented yet.'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_1','文艺同好会'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_1','文艺同好会'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_2','赞助人行会'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_2','赞助人行会'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_3','人文联合会'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_3','人文联合会'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_4','博雅总院'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_4','博雅总院'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_1_HELP','创作者与爱好者因共同的艺文兴趣形成稳定社群，构成城市文化专业化的基础。[NEWLINE][NEWLINE]基础专家支持：[NEWLINE][ICON_BULLET] 每名正在工作的文化专家额外提供：+3 [ICON_Food]食物、+3 [ICON_Production]生产力。[NEWLINE][ICON_BULLET] 与原生专家收益叠加；更高等级继续沿用此基础支持。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_1_HELP','创作者与爱好者因共同的艺文兴趣形成稳定社群，构成城市文化专业化的基础。[NEWLINE][NEWLINE]基础专家支持：[NEWLINE][ICON_BULLET] 每名正在工作的文化专家额外提供：+3 [ICON_Food]食物、+3 [ICON_Production]生产力。[NEWLINE][ICON_BULLET] 与原生专家收益叠加；更高等级继续沿用此基础支持。'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_2_HELP','稳定的资助、委托与社会支持，使文学、艺术与音乐创作成为持续的城市事业。[NEWLINE][NEWLINE]文艺赞助：[NEWLINE][ICON_BULLET] 本城剧院广场提供+1 [ICON_Housing]住房；每有一个包含合格普通建筑的建筑等级，再提供+1 [ICON_Housing]住房，同级不重复。[NEWLINE][ICON_BULLET] 每名正在工作的文化专家额外提供：2点基础[ICON_GreatWriter]大作家点数、2点基础[ICON_GreatArtist]大艺术家点数、2点基础[ICON_GreatMusician]大音乐家点数。[NEWLINE][ICON_BULLET] 上述点数可受伟人点数百分比加成影响。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_2_HELP','稳定的资助、委托与社会支持，使文学、艺术与音乐创作成为持续的城市事业。[NEWLINE][NEWLINE]文艺赞助：[NEWLINE][ICON_BULLET] 本城剧院广场提供+1 [ICON_Housing]住房；每有一个包含合格普通建筑的建筑等级，再提供+1 [ICON_Housing]住房，同级不重复。[NEWLINE][ICON_BULLET] 每名正在工作的文化专家额外提供：2点基础[ICON_GreatWriter]大作家点数、2点基础[ICON_GreatArtist]大艺术家点数、2点基础[ICON_GreatMusician]大音乐家点数。[NEWLINE][ICON_BULLET] 上述点数可受伟人点数百分比加成影响。'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_3_HELP','作品不再只属于创作当下；历史不断赋予新的理解，艺术也逐渐塑造整座城市的审美。[NEWLINE][NEWLINE]时代对话：[NEWLINE][ICON_BULLET] 开展同名城市项目，占用1个完整生产回合；按启动时的游戏时代计算，每城每时代最多成功一次。[NEWLINE][ICON_BULLET] 完成时，合格馆藏每覆盖一个不同的作品时代，永久累加5个百分点的巨作原生[ICON_Tourism]旅游业绩倍率。[NEWLINE][ICON_BULLET] 不放大“意义延展”的追加产出。项目中断不消耗本时代成功次数。[NEWLINE][ICON_BULLET] 文化启用等级低于三级或转出文化身份时暂停加成，保留累计记录。[NEWLINE][NEWLINE]风雅熏陶：[NEWLINE][ICON_BULLET] 本城合格巨作每覆盖一个不同的作品时代，每座未遭掠夺的合格普通建筑额外提供+1 [ICON_Tourism]旅游业绩。[NEWLINE][ICON_BULLET] 按本城当前馆藏的时代覆盖数动态计算。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_3_HELP','作品不再只属于创作当下；历史不断赋予新的理解，艺术也逐渐塑造整座城市的审美。[NEWLINE][NEWLINE]时代对话：[NEWLINE][ICON_BULLET] 开展同名城市项目，占用1个完整生产回合；按启动时的游戏时代计算，每城每时代最多成功一次。[NEWLINE][ICON_BULLET] 完成时，合格馆藏每覆盖一个不同的作品时代，永久累加5个百分点的巨作原生[ICON_Tourism]旅游业绩倍率。[NEWLINE][ICON_BULLET] 不放大“意义延展”的追加产出。项目中断不消耗本时代成功次数。[NEWLINE][ICON_BULLET] 文化启用等级低于三级或转出文化身份时暂停加成，保留累计记录。[NEWLINE][NEWLINE]风雅熏陶：[NEWLINE][ICON_BULLET] 本城合格巨作每覆盖一个不同的作品时代，每座未遭掠夺的合格普通建筑额外提供+1 [ICON_Tourism]旅游业绩。[NEWLINE][ICON_BULLET] 按本城当前馆藏的时代覆盖数动态计算。'),
('zh_Hans_CN','LOC_SPC_CULTURE_INSTITUTION_4_HELP','成熟的人文体系从社会各领域理解文化，让巨作启发未来人才，并主动走向其它文明拓展自身视野。[NEWLINE][NEWLINE]意义延展：[NEWLINE][ICON_BULLET] 每件合格巨作，从本城各合格专业领域获得代表产出：每1点基础设施深度提供0.5份产出。[NEWLINE][ICON_BULLET] [ICON_Gold]金币每份3点，其它产出每份1点；同一领域取最高单区域深度。[NEWLINE][ICON_BULLET] 各领域收益分别向下取整后相加，再按合格巨作件数结算。[NEWLINE][ICON_BULLET] 可受原生主题化加成影响，不受“时代对话”放大。当前不计入市政广场与外交区的[ICON_Culture]文化追加。[NEWLINE][NEWLINE]巨作启迪：[NEWLINE][ICON_BULLET] 本城合格巨作每覆盖一个不同的作品时代，所有已有基础产出的伟人点数提高3%；最多7个时代，最高+21%。[NEWLINE][ICON_BULLET] 没有基础点数的伟人类别不会因此获得点数。[NEWLINE][NEWLINE]人文考察团：[NEWLINE][ICON_BULLET] 可训练人文考察团，全国同时最多拥有1支；采用间谍生产成本公式，训练次数独立累计。[NEWLINE][ICON_BULLET] 派遣至已遇见的外国主要文明，执行风土考察、艺文采撷、奇观巡礼；标准速度下均为2回合。[NEWLINE][ICON_BULLET] 每个来源城市对每个目标文明的每类任务，首次成功获得1份文化见闻并归档保留。[NEWLINE][ICON_BULLET] 当前有效见闻提供本城[ICON_Tourism]旅游业绩与文化网络加成。'),
('en_US','LOC_SPC_CULTURE_INSTITUTION_4_HELP','成熟的人文体系从社会各领域理解文化，让巨作启发未来人才，并主动走向其它文明拓展自身视野。[NEWLINE][NEWLINE]意义延展：[NEWLINE][ICON_BULLET] 每件合格巨作，从本城各合格专业领域获得代表产出：每1点基础设施深度提供0.5份产出。[NEWLINE][ICON_BULLET] [ICON_Gold]金币每份3点，其它产出每份1点；同一领域取最高单区域深度。[NEWLINE][ICON_BULLET] 各领域收益分别向下取整后相加，再按合格巨作件数结算。[NEWLINE][ICON_BULLET] 可受原生主题化加成影响，不受“时代对话”放大。当前不计入市政广场与外交区的[ICON_Culture]文化追加。[NEWLINE][NEWLINE]巨作启迪：[NEWLINE][ICON_BULLET] 本城合格巨作每覆盖一个不同的作品时代，所有已有基础产出的伟人点数提高3%；最多7个时代，最高+21%。[NEWLINE][ICON_BULLET] 没有基础点数的伟人类别不会因此获得点数。[NEWLINE][NEWLINE]人文考察团：[NEWLINE][ICON_BULLET] 可训练人文考察团，全国同时最多拥有1支；采用间谍生产成本公式，训练次数独立累计。[NEWLINE][ICON_BULLET] 派遣至已遇见的外国主要文明，执行风土考察、艺文采撷、奇观巡礼；标准速度下均为2回合。[NEWLINE][ICON_BULLET] 每个来源城市对每个目标文明的每类任务，首次成功获得1份文化见闻并归档保留。[NEWLINE][ICON_BULLET] 当前有效见闻提供本城[ICON_Tourism]旅游业绩与文化网络加成。');

-- B233: read-only Industry history/typed knowledge, no new gameplay effect.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('en_US','LOC_SPC_INDUSTRY_HISTORY_BUTTON','工业历史 / 模板'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_HISTORY_BUTTON','工业历史 / 模板'),
('en_US','LOC_SPC_INDUSTRY_HISTORY_HINT','选中己方城市，查看本城奇观N、本文明时代E及模板；重复点击翻建筑页。关键结果自动写入有界日志。只读，不初始化或发放收益。'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_HISTORY_HINT','选中己方城市，查看本城奇观N、本文明时代E及模板；重复点击翻建筑页。关键结果自动写入有界日志。只读，不初始化或发放收益。');

-- B236: accepted Industry institution names; display only.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_1','匠作坊'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_1_HELP','工匠与生产人口在此聚集，将区域的生产条件转化为熟练劳动。[NEWLINE][NEWLINE]基础专家支持：[NEWLINE][ICON_BULLET] 每名正在工作的工业专家额外提供+3 [ICON_Food]食物。[NEWLINE][ICON_BULLET] 额外[ICON_Production]生产力等于本城工业区基础相邻生产力加成，按1:1转化，不计政策等相邻加成倍率。[NEWLINE][ICON_BULLET] 与原生专家收益叠加；各专业等级均沿用此公式。'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_1','匠作坊'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_1_HELP','工匠与生产人口在此聚集，将区域的生产条件转化为熟练劳动。[NEWLINE][NEWLINE]基础专家支持：[NEWLINE][ICON_BULLET] 每名正在工作的工业专家额外提供+3 [ICON_Food]食物。[NEWLINE][ICON_BULLET] 额外[ICON_Production]生产力等于本城工业区基础相邻生产力加成，按1:1转化，不计政策等相邻加成倍率。[NEWLINE][ICON_BULLET] 与原生专家收益叠加；各专业等级均沿用此公式。'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_2','百工会馆'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_2_HELP','不同工种与技术职业形成稳定分工，共同培养城市的工程人才。[NEWLINE][NEWLINE]专业分工：[NEWLINE][ICON_BULLET] 本城工业区提供+1 [ICON_Housing]住房；每有一个包含合格普通建筑的建筑等级，再提供+1 [ICON_Housing]住房，同级不重复。[NEWLINE][ICON_BULLET] 每名正在工作的工业专家额外提供2点基础[ICON_GreatEngineer]大工程师点数，可受伟人点数百分比加成影响。'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_2','百工会馆'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_2_HELP','不同工种与技术职业形成稳定分工，共同培养城市的工程人才。[NEWLINE][NEWLINE]专业分工：[NEWLINE][ICON_BULLET] 本城工业区提供+1 [ICON_Housing]住房；每有一个包含合格普通建筑的建筑等级，再提供+1 [ICON_Housing]住房，同级不重复。[NEWLINE][ICON_BULLET] 每名正在工作的工业专家额外提供2点基础[ICON_GreatEngineer]大工程师点数，可受伟人点数百分比加成影响。'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_3','工程局'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_3_HELP','工程规范、资源统筹与施工组织，使生产经验能够重复，施工力量能够部署。[NEWLINE][NEWLINE]标准化：[NEWLINE][ICON_BULLET] 已完成的建设经验记录为可靠模板；建造符合模板的区域与建筑时，获得+10%[ICON_Production]生产力。[NEWLINE][ICON_BULLET] 三级不提供[ICON_Gold]金币购买折扣。贸易路线相连的城市按专业网络规则共享模板。[NEWLINE][ICON_BULLET] 同一目标有多个可用来源时，仅取最高加成，不叠加。[NEWLINE][NEWLINE]施工队：[NEWLINE][ICON_BULLET] 解锁一级至三级施工队组建项目，组建成本为基础施工力的150%。[NEWLINE][ICON_BULLET] 对于当前所有者，每个来源城市最多同时支持2支现存施工队。[NEWLINE][ICON_BULLET] 仅能向正在建造的奇观一次性投入基础[ICON_Production]施工力，可受适用生产力加成影响；超出剩余所需的部分不溢出结转。'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_3','工程局'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_3_HELP','工程规范、资源统筹与施工组织，使生产经验能够重复，施工力量能够部署。[NEWLINE][NEWLINE]标准化：[NEWLINE][ICON_BULLET] 已完成的建设经验记录为可靠模板；建造符合模板的区域与建筑时，获得+10%[ICON_Production]生产力。[NEWLINE][ICON_BULLET] 三级不提供[ICON_Gold]金币购买折扣。贸易路线相连的城市按专业网络规则共享模板。[NEWLINE][ICON_BULLET] 同一目标有多个可用来源时，仅取最高加成，不叠加。[NEWLINE][NEWLINE]施工队：[NEWLINE][ICON_BULLET] 解锁一级至三级施工队组建项目，组建成本为基础施工力的150%。[NEWLINE][ICON_BULLET] 对于当前所有者，每个来源城市最多同时支持2支现存施工队。[NEWLINE][ICON_BULLET] 仅能向正在建造的奇观一次性投入基础[ICON_Production]施工力，可受适用生产力加成影响；超出剩余所需的部分不溢出结转。'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_4','土木工程总局'),
('zh_Hans_CN','LOC_SPC_INDUSTRY_INSTITUTION_4_HELP','成熟的工程体系组织大型建设，并将实践经验与历史积累转化为更深厚的工程能力。[NEWLINE][NEWLINE]工程传统：[NEWLINE][ICON_BULLET] 本文明亲自建成的奇观，每覆盖一个不同的奇观时代，提供一份可供本城研习的经验。[NEWLINE][ICON_BULLET] 每次“工程传统研习”占用1个完整生产回合，永久积累1层成果。[NEWLINE][ICON_BULLET] 四级启用时，每层使“标准化”的[ICON_Production]建造加成与合格建筑的[ICON_Gold]购买折扣各提高2个百分点。[NEWLINE][ICON_BULLET] 已完成成果按城市历史保留，恢复四级启用后重新生效；购买折扣不包含区域本体。[NEWLINE][NEWLINE]工程实践：[NEWLINE][ICON_BULLET] 解锁四级、五级施工队组建项目。[NEWLINE][ICON_BULLET] 本城累计建成1、3、6座奇观时，组建成本由基础施工力的150%，依次降至140%、130%、120%。[NEWLINE][ICON_BULLET] 每支施工队的组建成本在开工时锁定。[NEWLINE][NEWLINE]巨构工程学：[NEWLINE][ICON_BULLET] 建造早于本文明当前时代的奇观时，按时代差获得[ICON_Production]建造生产力加成：[NEWLINE][ICON_BULLET] 落后1个时代：+10%；落后2个时代：+20%；落后3个及以上时代：+30%。[NEWLINE][ICON_BULLET] 符合条件时，此加成同样作用于施工队投入的基础施工力。'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_4','土木工程总局'),
('en_US','LOC_SPC_INDUSTRY_INSTITUTION_4_HELP','成熟的工程体系组织大型建设，并将实践经验与历史积累转化为更深厚的工程能力。[NEWLINE][NEWLINE]工程传统：[NEWLINE][ICON_BULLET] 本文明亲自建成的奇观，每覆盖一个不同的奇观时代，提供一份可供本城研习的经验。[NEWLINE][ICON_BULLET] 每次“工程传统研习”占用1个完整生产回合，永久积累1层成果。[NEWLINE][ICON_BULLET] 四级启用时，每层使“标准化”的[ICON_Production]建造加成与合格建筑的[ICON_Gold]购买折扣各提高2个百分点。[NEWLINE][ICON_BULLET] 已完成成果按城市历史保留，恢复四级启用后重新生效；购买折扣不包含区域本体。[NEWLINE][NEWLINE]工程实践：[NEWLINE][ICON_BULLET] 解锁四级、五级施工队组建项目。[NEWLINE][ICON_BULLET] 本城累计建成1、3、6座奇观时，组建成本由基础施工力的150%，依次降至140%、130%、120%。[NEWLINE][ICON_BULLET] 每支施工队的组建成本在开工时锁定。[NEWLINE][NEWLINE]巨构工程学：[NEWLINE][ICON_BULLET] 建造早于本文明当前时代的奇观时，按时代差获得[ICON_Production]建造生产力加成：[NEWLINE][ICON_BULLET] 落后1个时代：+10%；落后2个时代：+20%；落后3个及以上时代：+30%。[NEWLINE][ICON_BULLET] 符合条件时，此加成同样作用于施工队投入的基础施工力。');

-- B236 replaces old formation and general-construction wording exactly.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_UNIT_SPC_CREW_250_DESCRIPTION','拥有 1 次施工次数。标准速度下基础施工力为 260（随游戏速度缩放并在建成时锁定）。仅可用于正在建造的奇观；投入时可享受适用的生产力加成，超出奇观剩余所需的部分不会溢出结转。对于当前所有者，每个来源城市最多可同时拥有 2 支现存施工队；来源城市启用等级下降或易主不会移除已建成的施工队。'),
('zh_Hans_CN','LOC_PROJECT_SPC_CREW_250_DESCRIPTION','本城工业启用等级达到 3 级时解锁。项目开工时即锁定本次生产成本：工业启用 3 级时为基础施工力的 150%；启用 4 级时，根据本城可靠历史奇观数量（N）依次降至 150% / 140% / 130% / 120%。标准速度下基础施工力为 260（随游戏速度缩放）。对于当前所有者，每个来源城市最多可同时支持 2 支现存施工队。'),
('en_US','LOC_UNIT_SPC_CREW_250_DESCRIPTION','One construction use. Base transfer Production 260 at Standard speed, scaled and locked at formation. Wonders only; applicable Production modifiers can increase the transfer; surplus does not carry over. A source supports two living Crews for its current owner. Completed Crews survive source qualification and ownership changes.'),
('en_US','LOC_PROJECT_SPC_CREW_250_DESCRIPTION','Requires Industry ACTIVE III. Price locks at start: III 150%; IV 150/140/130/120% by local Wonder history. Base transfer Production 260 at Standard speed, scaled by game speed. Two surviving Crews per source for its current owner.'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_420_DESCRIPTION','拥有 1 次施工次数。标准速度下基础施工力为 420（随游戏速度缩放并在建成时锁定）。仅可用于正在建造的奇观；投入时可享受适用的生产力加成，超出奇观剩余所需的部分不会溢出结转。对于当前所有者，每个来源城市最多可同时拥有 2 支现存施工队；来源城市启用等级下降或易主不会移除已建成的施工队。'),
('zh_Hans_CN','LOC_PROJECT_SPC_CREW_420_DESCRIPTION','本城工业启用等级达到 3 级时解锁。项目开工时即锁定本次生产成本：工业启用 3 级时为基础施工力的 150%；启用 4 级时，根据本城可靠历史奇观数量（N）依次降至 150% / 140% / 130% / 120%。标准速度下基础施工力为 420（随游戏速度缩放）。对于当前所有者，每个来源城市最多可同时支持 2 支现存施工队。'),
('en_US','LOC_UNIT_SPC_CREW_420_DESCRIPTION','One construction use. Base transfer Production 420 at Standard speed, scaled and locked at formation. Wonders only; applicable Production modifiers can increase the transfer; surplus does not carry over. A source supports two living Crews for its current owner. Completed Crews survive source qualification and ownership changes.'),
('en_US','LOC_PROJECT_SPC_CREW_420_DESCRIPTION','Requires Industry ACTIVE III. Price locks at start: III 150%; IV 150/140/130/120% by local Wonder history. Base transfer Production 420 at Standard speed, scaled by game speed. Two surviving Crews per source for its current owner.'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_750_DESCRIPTION','拥有 1 次施工次数。标准速度下基础施工力为 750（随游戏速度缩放并在建成时锁定）。仅可用于正在建造的奇观；投入时可享受适用的生产力加成，超出奇观剩余所需的部分不会溢出结转。对于当前所有者，每个来源城市最多可同时拥有 2 支现存施工队；来源城市启用等级下降或易主不会移除已建成的施工队。'),
('zh_Hans_CN','LOC_PROJECT_SPC_CREW_750_DESCRIPTION','本城工业启用等级达到 3 级时解锁。项目开工时即锁定本次生产成本：工业启用 3 级时为基础施工力的 150%；启用 4 级时，根据本城可靠历史奇观数量（N）依次降至 150% / 140% / 130% / 120%。标准速度下基础施工力为 750（随游戏速度缩放）。对于当前所有者，每个来源城市最多可同时支持 2 支现存施工队。'),
('en_US','LOC_UNIT_SPC_CREW_750_DESCRIPTION','One construction use. Base transfer Production 750 at Standard speed, scaled and locked at formation. Wonders only; applicable Production modifiers can increase the transfer; surplus does not carry over. A source supports two living Crews for its current owner. Completed Crews survive source qualification and ownership changes.'),
('en_US','LOC_PROJECT_SPC_CREW_750_DESCRIPTION','Requires Industry ACTIVE III. Price locks at start: III 150%; IV 150/140/130/120% by local Wonder history. Base transfer Production 750 at Standard speed, scaled by game speed. Two surviving Crews per source for its current owner.'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_1000_DESCRIPTION','拥有 1 次施工次数。标准速度下基础施工力为 1000（随游戏速度缩放并在建成时锁定）。仅可用于正在建造的奇观；投入时可享受适用的生产力加成，超出奇观剩余所需的部分不会溢出结转。对于当前所有者，每个来源城市最多可同时拥有 2 支现存施工队；来源城市启用等级下降或易主不会移除已建成的施工队。'),
('zh_Hans_CN','LOC_PROJECT_SPC_CREW_1000_DESCRIPTION','本城工业启用等级达到 4 级时解锁。项目开工时即锁定本次生产成本：工业启用 3 级时为基础施工力的 150%；启用 4 级时，根据本城可靠历史奇观数量（N）依次降至 150% / 140% / 130% / 120%。标准速度下基础施工力为 1000（随游戏速度缩放）。对于当前所有者，每个来源城市最多可同时支持 2 支现存施工队。'),
('en_US','LOC_UNIT_SPC_CREW_1000_DESCRIPTION','One construction use. Base transfer Production 1000 at Standard speed, scaled and locked at formation. Wonders only; applicable Production modifiers can increase the transfer; surplus does not carry over. A source supports two living Crews for its current owner. Completed Crews survive source qualification and ownership changes.'),
('en_US','LOC_PROJECT_SPC_CREW_1000_DESCRIPTION','Requires Industry ACTIVE IV. Price locks at start: III 150%; IV 150/140/130/120% by local Wonder history. Base transfer Production 1000 at Standard speed, scaled by game speed. Two surviving Crews per source for its current owner.'),
('zh_Hans_CN','LOC_UNIT_SPC_CREW_1360_DESCRIPTION','拥有 1 次施工次数。标准速度下基础施工力为 1360（随游戏速度缩放并在建成时锁定）。仅可用于正在建造的奇观；投入时可享受适用的生产力加成，超出奇观剩余所需的部分不会溢出结转。对于当前所有者，每个来源城市最多可同时拥有 2 支现存施工队；来源城市启用等级下降或易主不会移除已建成的施工队。'),
('zh_Hans_CN','LOC_PROJECT_SPC_CREW_1360_DESCRIPTION','本城工业启用等级达到 4 级时解锁。项目开工时即锁定本次生产成本：工业启用 3 级时为基础施工力的 150%；启用 4 级时，根据本城可靠历史奇观数量（N）依次降至 150% / 140% / 130% / 120%。标准速度下基础施工力为 1360（随游戏速度缩放）。对于当前所有者，每个来源城市最多可同时支持 2 支现存施工队。'),
('en_US','LOC_UNIT_SPC_CREW_1360_DESCRIPTION','One construction use. Base transfer Production 1360 at Standard speed, scaled and locked at formation. Wonders only; applicable Production modifiers can increase the transfer; surplus does not carry over. A source supports two living Crews for its current owner. Completed Crews survive source qualification and ownership changes.'),
('en_US','LOC_PROJECT_SPC_CREW_1360_DESCRIPTION','Requires Industry ACTIVE IV. Price locks at start: III 150%; IV 150/140/130/120% by local Wonder history. Base transfer Production 1360 at Standard speed, scaled by game speed. Two surviving Crews per source for its current owner.'),
('zh_Hans_CN','LOC_SPC_CREW_FORMATION_HELP','本次开工锁价。同一玩家从每座来源城市最多保有2支存活施工队；队列中的施工队会预留名额。仅用于奇观，剩余施工力不结转。'),
('en_US','LOC_SPC_CREW_FORMATION_HELP','Price locks when ordered. Each player may have two surviving Crews from a source city; queued orders reserve capacity. Wonders only; unused transfer Production is discarded.');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CREW_FORMATION_ERROR','组建未确认：{1}。请查看工业报告或回传日志。'),
('en_US','LOC_SPC_CREW_FORMATION_ERROR','Formation unconfirmed: {1}. Check the Industry report or collect the trace.');

-- B237 continuation labels; B238/D0053 base-input presentation below.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CREW_RESUME_NAME','{1_Name}（续建）'),
('en_US','LOC_SPC_CREW_RESUME_NAME','{1_Name} (resume)'),
('zh_Hans_CN','LOC_SPC_CREW_LOCKED_PRICE','已锁定开工成本：{1_Cost}（续建将沿用原项目的既有进度）。'),
('en_US','LOC_SPC_CREW_LOCKED_PRICE','Started price: {1_Cost}. Resume the original project and its native progress.');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CREW_BASE_PREVIEW','已锁定基础施工力：{1_Capacity}[NEWLINE]本次投入基础施工力：{2_Input} ｜ 剩余未使用基础施工力：{3_Unused}[NEWLINE]实际转化的生产力可享受适用加成；未使用的余量不会结转。'),
('en_US','LOC_SPC_CREW_BASE_PREVIEW','Locked base Production: {1_Capacity}[NEWLINE]Base input: {2_Input}; unused base: {3_Unused}[NEWLINE]Applicable modifiers can increase actual Production; surplus does not carry over.'),
('zh_Hans_CN','LOC_SPC_CREW_BASE_CONFIRM','消耗此施工队，为当前正在建造的奇观投入 {1_Input} 点基础生产力（实际转化量可享受适用生产力加成）。[NEWLINE]此操作一旦确认无法撤销。'),
('en_US','LOC_SPC_CREW_BASE_CONFIRM','Consume this Crew to supply {1_Input} base Production to the current Wonder, subject to applicable modifiers.[NEWLINE]This cannot be undone.'),
('zh_Hans_CN','LOC_SPC_CREW_BASE_READY','已锁定基础施工力：{1_Capacity}（可享受适用的生产力加成）。[NEWLINE]点击以预览详情并确认施工。'),
('en_US','LOC_SPC_CREW_BASE_READY','Locked base Production: {1_Capacity}, subject to applicable Production modifiers.[NEWLINE]Prepare and confirm construction.');

-- B239: unfinished paid formation retains capacity.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CREW_OCCUPANCY','本城名额占用：现存队伍 {1} ｜ 未完成组建 {2}（含可续建 {3}；未完成项目仍占用名额）'),
('zh_Hans_CN','LOC_SPC_CREW_RESUME_CAPACITY_HELD','本城现存施工队及队列中的组建项目已占满名额上限；当前项目的锁定成本与已有进度已保留，待空出名额后即可继续建造。'),
('zh_Hans_CN','LOC_SPC_CREW_FORMATION_HELP','源于本城的现存施工队与已开工但未完成的组建项目共同占用本城名额（已有进度的暂停项目仍继续占位）。续建项目将沿用已锁定的原成本与既有进度，不会额外占用新名额。'),
('en_US','LOC_SPC_CREW_OCCUPANCY','来源名额：存活{1}，未完成组建{2}（含续建{3}）；未完成组建继续占用名额。'),
('en_US','LOC_SPC_CREW_RESUME_CAPACITY_HELD','现役施工队及已排队项目已占满可完成名额；保留本次成本与进度，释放名额后可续建。'),
('en_US','LOC_SPC_CREW_FORMATION_HELP','本城来源施工队及已接入的未完成组建共同占用名额；有进度的暂停项目继续占位。续建沿用原成本与已有进度，不额外申请名额。');

-- B251 institution preview and bounded live summaries.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INSTITUTION_PREVIEW','尚未建立');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INSTITUTION_PREVIEW','尚未建立');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_TRADITION','学术传统');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_TRADITION','学术传统');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_REPUTATION','商业信誉');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_REPUTATION','商业信誉');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_DIALOGUE','时代对话');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_DIALOGUE','时代对话');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_EXPEDITION','人文考察团');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_EXPEDITION','人文考察团');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_ENGINEERING','工程传统');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_ENGINEERING','工程传统');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_STANDARDIZATION','标准化');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_STANDARDIZATION','标准化');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_PENDING','当前数值待确认');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_PENDING','当前数值待确认');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_PENDING_SHORT','待确认');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_PENDING_SHORT','待确认');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_NOT_STARTED','尚未开始积累');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_NOT_STARTED','尚未开始积累');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_TRADITION_VALUE','已累计 {1} 回合；[ICON_Science]学术传统倍率 +{2}%。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_TRADITION_VALUE','已累计 {1} 回合；[ICON_Science]学术传统倍率 +{2}%。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_TRADITION_NEXT','距下一档还需 {1} 回合。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_TRADITION_NEXT','距下一档还需 {1} 回合。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_ACCUMULATION_PAUSED','积累已暂停，历史保留。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_ACCUMULATION_PAUSED','积累已暂停，历史保留。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_REPUTATION_VALUE','已累计信誉 {1}/40；[ICON_Gold]商业化增幅 +{2}%。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_REPUTATION_VALUE','已累计信誉 {1}/40；[ICON_Gold]商业化增幅 +{2}%。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_DIALOGUE_VALUE','[ICON_Tourism]已累计巨作旅游业绩倍率：+{1}%。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_DIALOGUE_VALUE','[ICON_Tourism]已累计巨作旅游业绩倍率：+{1}%。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_INSIGHTS_VALUE','文化见闻：{1} 份。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_INSIGHTS_VALUE','文化见闻：{1} 份。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_ENGINEERING_VALUE','已完成研习：{1} 层。[NEWLINE]四级启用时：[ICON_Production]标准化建造加成与合格建筑[ICON_Gold]金币折扣各增强 {2} 个百分点。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_ENGINEERING_VALUE','已完成研习：{1} 层。[NEWLINE]四级启用时：[ICON_Production]标准化建造加成与合格建筑[ICON_Gold]金币折扣各增强 {2} 个百分点。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_TEMPLATES_VALUE','本城已记录模板：建筑 {1} 项，区域 {2} 项。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_TEMPLATES_VALUE','本城已记录模板：建筑 {1} 项，区域 {2} 项。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_STANDARDIZATION_VALUE','本城当前提供：[ICON_Production]生产力 +{1}%，合格建筑[ICON_Gold]金币购买折扣 {2}%。[NEWLINE]不含区域购买折扣。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_STANDARDIZATION_VALUE','本城当前提供：[ICON_Production]生产力 +{1}%，合格建筑[ICON_Gold]金币购买折扣 {2}%。[NEWLINE]不含区域购买折扣。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_STANDARDIZATION_PAUSED','本城当前不提供标准化加成；已记录模板保留。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_STANDARDIZATION_PAUSED','本城当前不提供标准化加成；已记录模板保留。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_ACTIVE_PENDING','当前启用等级暂待确认');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_ACTIVE_PENDING','当前启用等级暂待确认');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_LEGACY_HELP','曾建立的历史机构（当前已脱离该专业，不提供对应能力）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_LEGACY_HELP','曾建立的历史机构（当前已脱离该专业，不提供对应能力）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_PREVIEW_HELP','未来机构预览：专业潜力达到 {1} 级后建立；尚未授予本级能力。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_PREVIEW_HELP','未来机构预览：专业潜力达到 {1} 级后建立；尚未授予本级能力。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_ACTIVE_HELP','已达到本级机构的启用等级（具体收益仍需满足各能力的对应条件）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_ACTIVE_HELP','已达到本级机构的启用等级（具体收益仍需满足各能力的对应条件）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_INST_INACTIVE_HELP','尚未满足本级机构的启用条件（已建成的机构仍予以保留）');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('en_US','LOC_SPC_INST_INACTIVE_HELP','尚未满足本级机构的启用条件（已建成的机构仍予以保留）');

-- B264: native-style institution presentation; no gameplay definitions.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_INST_CATEGORY','{1}专业·{2}级机构'),
('en_US','LOC_SPC_INST_CATEGORY','{1}专业·{2}级机构'),
('zh_Hans_CN','LOC_SPC_INST_REQUIREMENT','启用需求：{1}专业启用等级达到{2}级。'),
('en_US','LOC_SPC_INST_REQUIREMENT','启用需求：{1}专业启用等级达到{2}级。'),
('zh_Hans_CN','LOC_SPC_INST_STATE','当前状态：{1}'),
('en_US','LOC_SPC_INST_STATE','当前状态：{1}'),
('zh_Hans_CN','LOC_SPC_INST_RESEARCH','科研'),
('en_US','LOC_SPC_INST_RESEARCH','科研'),
('zh_Hans_CN','LOC_SPC_INST_CULTURE','文化'),
('en_US','LOC_SPC_INST_CULTURE','文化'),
('zh_Hans_CN','LOC_SPC_INST_INDUSTRY','工业'),
('en_US','LOC_SPC_INST_INDUSTRY','工业'),
('zh_Hans_CN','LOC_SPC_INST_COMMERCE','商业'),
('en_US','LOC_SPC_INST_COMMERCE','商业'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_1','学者结社'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_1','学者结社'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_1_HELP','学者在此结成稳定的研究共同体，构成城市科研专业化的基础。[NEWLINE][NEWLINE]基础专家支持：[NEWLINE][ICON_BULLET] 每名正在工作的科研专家额外提供：+3 [ICON_Food]食物、+3 [ICON_Production]生产力。'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_1_HELP','学者在此结成稳定的研究共同体，构成城市科研专业化的基础。[NEWLINE][NEWLINE]基础专家支持：[NEWLINE][ICON_BULLET] 每名正在工作的科研专家额外提供：+3 [ICON_Food]食物、+3 [ICON_Production]生产力。'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_2','研修院'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_2','研修院'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_2_HELP','系统的研修与人才培养，使科研从个人志业成为城市的长期事业。[NEWLINE][NEWLINE]人才培养：[NEWLINE][ICON_BULLET] 每名正在工作的科研专家额外提供2点基础[ICON_GreatScientist]大科学家点数，可受伟人点数百分比加成影响。[NEWLINE][ICON_BULLET] 本城学院区域及其每一级合格建筑各提供+1 [ICON_Housing]住房。'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_2_HELP','系统的研修与人才培养，使科研从个人志业成为城市的长期事业。[NEWLINE][NEWLINE]人才培养：[NEWLINE][ICON_BULLET] 每名正在工作的科研专家额外提供2点基础[ICON_GreatScientist]大科学家点数，可受伟人点数百分比加成影响。[NEWLINE][ICON_BULLET] 本城学院区域及其每一级合格建筑各提供+1 [ICON_Housing]住房。'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_3','学术联合会'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_3','学术联合会'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_3_HELP','不同专业领域在此交流，使研究成果与城市实践相互促进。[NEWLINE][NEWLINE]跨学科研究：[NEWLINE][ICON_BULLET] 将本城除学院外的合格专业区域的基础相邻产出总和，按50%转化为[ICON_Science]科技值；汇总后向下取整。[NEWLINE][ICON_BULLET] 仅计入已建成且未被掠夺的区域；不计政策等相邻加成倍率及非相邻产出。适用区域见专业领域表。[NEWLINE][NEWLINE]学以致用：[NEWLINE][ICON_BULLET] 每名正在工作的科研专家，从本城每个其它合格专业领域获得对应产出。[NEWLINE][ICON_BULLET] 每1点基础设施深度提供0.5份产出：[ICON_Gold]金币每份3点，其它产出每份1点。[NEWLINE][ICON_BULLET] 同一领域取最高单区域深度；提供同种产出的不同领域分别计算后相加。[NEWLINE][ICON_BULLET] 每名专家的各项收益先向下取整，再按专家人数结算。'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_3_HELP','不同专业领域在此交流，使研究成果与城市实践相互促进。[NEWLINE][NEWLINE]跨学科研究：[NEWLINE][ICON_BULLET] 将本城除学院外的合格专业区域的基础相邻产出总和，按50%转化为[ICON_Science]科技值；汇总后向下取整。[NEWLINE][ICON_BULLET] 仅计入已建成且未被掠夺的区域；不计政策等相邻加成倍率及非相邻产出。适用区域见专业领域表。[NEWLINE][NEWLINE]学以致用：[NEWLINE][ICON_BULLET] 每名正在工作的科研专家，从本城每个其它合格专业领域获得对应产出。[NEWLINE][ICON_BULLET] 每1点基础设施深度提供0.5份产出：[ICON_Gold]金币每份3点，其它产出每份1点。[NEWLINE][ICON_BULLET] 同一领域取最高单区域深度；提供同种产出的不同领域分别计算后相加。[NEWLINE][ICON_BULLET] 每名专家的各项收益先向下取整，再按专家人数结算。'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_4','学术总署'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_4','学术总署'),
('zh_Hans_CN','LOC_SPC_RESEARCH_INSTITUTION_4_HELP','完善的科研设施、学术组织与长期传统，共同支撑深入研究。[NEWLINE][NEWLINE]科研基础设施：[NEWLINE][ICON_BULLET] 本城学院每1点基础设施深度，使每名正在工作的科研专家额外提供+1基础[ICON_Science]科技值。[NEWLINE][ICON_BULLET] 深度上限10点；达到上限时，5名专家共提供+50基础[ICON_Science]科技值。[NEWLINE][NEWLINE]学术主持：[NEWLINE][ICON_BULLET] 每名正在工作的科研专家，使本城每座未遭掠夺的普通学院一至四级建筑额外提供+1基础[ICON_Science]科技值。[NEWLINE][ICON_BULLET] 被掠夺的建筑不计入且不享受收益；额外科技值不提高基础设施深度。[NEWLINE][NEWLINE]学术传统：[NEWLINE][ICON_BULLET] 首次达到科研潜力四级后开始积累。启用四级时，初始提供+5%[ICON_Science]科技值。[NEWLINE][ICON_BULLET] 标准速度下，累计10、20、30、40回合，依次提高至10%、15%、20%、25%，上限25%。其它速度按比例缩放阶段回合数并向下取整。[NEWLINE][ICON_BULLET] 保有科研身份时持续积累；暂未启用四级不影响积累。转出科研后暂停并保留进度，转回后继续，不补算离开期间的回合。'),
('en_US','LOC_SPC_RESEARCH_INSTITUTION_4_HELP','完善的科研设施、学术组织与长期传统，共同支撑深入研究。[NEWLINE][NEWLINE]科研基础设施：[NEWLINE][ICON_BULLET] 本城学院每1点基础设施深度，使每名正在工作的科研专家额外提供+1基础[ICON_Science]科技值。[NEWLINE][ICON_BULLET] 深度上限10点；达到上限时，5名专家共提供+50基础[ICON_Science]科技值。[NEWLINE][NEWLINE]学术主持：[NEWLINE][ICON_BULLET] 每名正在工作的科研专家，使本城每座未遭掠夺的普通学院一至四级建筑额外提供+1基础[ICON_Science]科技值。[NEWLINE][ICON_BULLET] 被掠夺的建筑不计入且不享受收益；额外科技值不提高基础设施深度。[NEWLINE][NEWLINE]学术传统：[NEWLINE][ICON_BULLET] 首次达到科研潜力四级后开始积累。启用四级时，初始提供+5%[ICON_Science]科技值。[NEWLINE][ICON_BULLET] 标准速度下，累计10、20、30、40回合，依次提高至10%、15%、20%、25%，上限25%。其它速度按比例缩放阶段回合数并向下取整。[NEWLINE][ICON_BULLET] 保有科研身份时持续积累；暂未启用四级不影响积累。转出科研后暂停并保留进度，转回后继续，不补算离开期间的回合。');

-- B265: native city-panel shortcut; the badge numeral always represents ACTIVE.
INSERT OR REPLACE INTO LocalizedText (Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_CITY_INSTITUTION_SHORTCUT','{1}专业 · 启用等级 {2}[NEWLINE]打开城市详情：专业机构、建筑、区域与奇观。'),
('en_US','LOC_SPC_CITY_INSTITUTION_SHORTCUT','{1}专业 · 启用等级 {2}[NEWLINE]打开城市详情：专业机构、建筑、区域与奇观。');
