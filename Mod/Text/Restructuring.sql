INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
 ('zh_Hans_CN','LOC_SPC_REST_TEAM','重组团队'),
 ('zh_Hans_CN','LOC_SPC_REST_TEAM_HELP','商业专业启用四级后可训练。只能用生产力组建。前往专业潜力至少2级城市的当前专业区域进行资产清算，永久降低1级潜力；至少5个完整回合后，在同城另一个合格专业区域完成资产配置并消耗团队。原专业历史按各自规则保留。遭敌军接触时撤退，不转为敌方单位。'),
 ('zh_Hans_CN','LOC_SPC_REST_PHASE','资产重组中'),
 ('zh_Hans_CN','LOC_SPC_REST_LIQUIDATE','资产清算'),
 ('zh_Hans_CN','LOC_SPC_REST_CONFIGURE','资产配置'),
 ('zh_Hans_CN','LOC_SPC_REST_CONFIRM','确认{1_Name}'),
 ('zh_Hans_CN','LOC_SPC_REST_PREVIEW','目标：{1_City}[NEWLINE]完成后潜力：{2_Potential}级[NEWLINE]清算永久扣除1级潜力；重组期间全部非食物产出及净盈余食物增长降低75%。至少5个完整回合后，须在同城另一个合格专业区域主动完成配置。'),
 ('zh_Hans_CN','LOC_SPC_REST_WAIT','目标：{1_City}[NEWLINE]保留潜力：{2_Potential}级[NEWLINE]距离可配置还有{3_Turns}个完整回合。时间到达不会自动结束重组。'),
 ('zh_Hans_CN','LOC_SPC_REST_MOVE','将团队移动至潜力至少2级城市的当前专业区域。配置时须前往绑定城市内的另一个合格专业区域。'),
 ('zh_Hans_CN','LOC_SPC_REST_PENDING','身份或事务尚未确认；请保留日志，不要重复确认。'),
 ('zh_Hans_CN','LOC_SPC_INSTITUTION_LEGACY','历史机构');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
 ('zh_Hans_CN','LOC_SPC_REST_WAIT_GATE','尚未满5个完整回合。'),
 ('zh_Hans_CN','LOC_SPC_REST_CURRENT_SITE','请前往目标城市当前专业对应的已建成、未被掠夺区域。'),
 ('zh_Hans_CN','LOC_SPC_REST_OTHER_SITE','请选择同城内另一个专业对应的区域。'),
 ('zh_Hans_CN','LOC_SPC_REST_SAME_CITY','资产配置必须在已绑定的同一城市完成。'),
 ('zh_Hans_CN','LOC_SPC_REST_POTENTIAL_GATE','目标城市须至少有2级专业潜力，且没有未确认的移民投资。');
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
