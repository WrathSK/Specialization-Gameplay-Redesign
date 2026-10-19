INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
 ('zh_Hans_CN','LOC_SPC_REST_TEAM','重组团队'),
 ('zh_Hans_CN','LOC_SPC_REST_TEAM_HELP','本城商业启用等级达到 4 级时可训练（仅能使用生产力组建）。可前往专业潜力至少为 2 级的己方城市，在其当前专业对应的区域执行「资产清算」（永久扣除该城 1 级专业潜力）；经过至少 5 个完整回合后，须在同一城市内另一个合格的专业区域执行「资产配置」并消耗本团队，完成专业转换（原专业的历史记录按各自规则保留）。此单位遭遇敌军时将自动撤退，不会被敌方俘获。'),
 ('zh_Hans_CN','LOC_SPC_REST_PHASE','资产重组中'),
 ('zh_Hans_CN','LOC_SPC_REST_LIQUIDATE','资产清算'),
 ('zh_Hans_CN','LOC_SPC_REST_CONFIGURE','资产配置'),
 ('zh_Hans_CN','LOC_SPC_REST_CONFIRM','确认{1_Name}'),
 ('zh_Hans_CN','LOC_SPC_REST_PREVIEW','目标城市：{1_City}[NEWLINE]清算后保留潜力：{2_Potential} 级[NEWLINE]执行「资产清算」将永久扣除该城 1 级专业潜力；资产重组期间，该城所有非食物产出及盈余食物增长均降低 75%。持续至少 5 个完整回合后，须将该团队移动至同城内另一个合格的专业区域，手动执行「资产配置」以完成重组。'),
 ('zh_Hans_CN','LOC_SPC_REST_WAIT','绑定城市：{1_City}[NEWLINE]当前保留潜力：{2_Potential} 级[NEWLINE]距离可执行「资产配置」还需等待 {3_Turns} 个完整回合（回合数届满后不会自动结束重组，须手动完成配置）。'),
 ('zh_Hans_CN','LOC_SPC_REST_MOVE','清算阶段：请将团队移动至专业潜力至少为 2 级的城市中，其当前专业对应的区域。[NEWLINE]配置阶段：请将团队移动至已绑定城市内另一个合格的专业区域。'),
 ('zh_Hans_CN','LOC_SPC_REST_PENDING','身份或事务尚未确认；请保留日志，不要重复确认。'),
 ('zh_Hans_CN','LOC_SPC_INSTITUTION_LEGACY','历史机构');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
 ('zh_Hans_CN','LOC_SPC_REST_WAIT_GATE','尚未满5个完整回合。'),
 ('zh_Hans_CN','LOC_SPC_REST_CURRENT_SITE','请将团队移动至目标城市当前专业所对应的已建成且未被掠夺的区域。'),
 ('zh_Hans_CN','LOC_SPC_REST_OTHER_SITE','请将该团队移动至同一城市内另一个合格专业所对应的区域。'),
 ('zh_Hans_CN','LOC_SPC_REST_SAME_CITY','资产配置必须在已绑定的同一城市完成。'),
 ('zh_Hans_CN','LOC_SPC_REST_POTENTIAL_GATE','目标城市须至少拥有 2 级专业潜力，且当前没有待确认的移民专业化投资。');
-- Existing English fallback; authoritative player-facing copy remains Chinese.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text)
 SELECT 'en_US',Tag,Text FROM LocalizedText WHERE Language='zh_Hans_CN' AND (Tag LIKE 'LOC_SPC_REST_%' OR Tag='LOC_SPC_INSTITUTION_LEGACY');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_1','商贾聚落'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_1','商贾聚落');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_1_HELP','零散商人与经营活动在此稳定聚集，形成自发的商业共同体。'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_1_HELP','零散商人与经营活动在此稳定聚集，形成自发的商业共同体。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_2','同业公会'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_2','同业公会');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_2_HELP','同业制度形成稳定职业共同体与商业人才体系。'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_2_HELP','同业制度形成稳定职业共同体与商业人才体系。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_3','交易所'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_3','交易所');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_3_HELP','商业组织发现不同领域的价值，并经营资本的时间与风险。'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_3_HELP','商业组织发现不同领域的价值，并经营资本的时间与风险。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_4','资本信托'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_4','资本信托');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_4_HELP','成熟商业组织配置发展资本、重组既有资产，以长期稳定经营积累信誉。'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_4_HELP','成熟商业组织配置发展资本、重组既有资产，以长期稳定经营积累信誉。');
