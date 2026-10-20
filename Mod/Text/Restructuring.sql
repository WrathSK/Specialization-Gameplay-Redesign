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
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_1_HELP','零散商人与经营活动在此稳定聚集，形成自发的商业共同体。[NEWLINE][NEWLINE]基础专家支持[NEWLINE]每名正在工作的商业专家额外提供 +3 食物、+3 生产力。'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_1_HELP','零散商人与经营活动在此稳定聚集，形成自发的商业共同体。[NEWLINE][NEWLINE]基础专家支持[NEWLINE]每名正在工作的商业专家额外提供 +3 食物、+3 生产力。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_2','同业公会'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_2','同业公会');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_2_HELP','同业制度形成稳定职业共同体与商业人才体系。[NEWLINE][NEWLINE]同业制度[NEWLINE]每名正在工作的商业专家额外提供 2 点基础大商人点数，可受伟人点数百分比加成影响。本城商业中心区域及其每一级合格建筑各提供 +1 住房。'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_2_HELP','同业制度形成稳定职业共同体与商业人才体系。[NEWLINE][NEWLINE]同业制度[NEWLINE]每名正在工作的商业专家额外提供 2 点基础大商人点数，可受伟人点数百分比加成影响。本城商业中心区域及其每一级合格建筑各提供 +1 住房。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_3','交易所'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_3','交易所');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_3_HELP','商业组织发现不同领域的价值，并经营资本的时间与风险。[NEWLINE][NEWLINE]商业化[NEWLINE]每名在岗商业专家允许同时商业化一个不同领域，本城须拥有对应区域。各领域从本城及有直接国内商路相连、持有对应专业身份的己方城市中，选取对应城市总产出最高值；不要求来源专业当前激活。学院、剧院广场、工业区、圣地、港口分别读取科技、文化、生产力、信仰、总粮食，转化为本城额外金币，不扣除来源产出。每领域金币＝0.05×本城对应基础设施深度×最高来源产出×商业信誉倍率，各领域分别向下取整后相加。[NEWLINE][NEWLINE]资本投资[NEWLINE]可投资科研、文化或工业；每份合同以签约时国库余额的 25% 为本金，标准速度下 10 回合到期，每城每领域同时限一份未结合同。稳健投资返还本金与核定利润；风险投资成功时利润为稳健投资的 3 倍，失败时返还 50% 本金（可由商业信誉提高）。利润受本城对应基础设施、专业网络内对应专业的启用等级及该领域商业化影响；具体报价在「资本投资」中查看，签约后锁定。'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_3_HELP','商业组织发现不同领域的价值，并经营资本的时间与风险。[NEWLINE][NEWLINE]商业化[NEWLINE]每名在岗商业专家允许同时商业化一个不同领域，本城须拥有对应区域。各领域从本城及有直接国内商路相连、持有对应专业身份的己方城市中，选取对应城市总产出最高值；不要求来源专业当前激活。学院、剧院广场、工业区、圣地、港口分别读取科技、文化、生产力、信仰、总粮食，转化为本城额外金币，不扣除来源产出。每领域金币＝0.05×本城对应基础设施深度×最高来源产出×商业信誉倍率，各领域分别向下取整后相加。[NEWLINE][NEWLINE]资本投资[NEWLINE]可投资科研、文化或工业；每份合同以签约时国库余额的 25% 为本金，标准速度下 10 回合到期，每城每领域同时限一份未结合同。稳健投资返还本金与核定利润；风险投资成功时利润为稳健投资的 3 倍，失败时返还 50% 本金（可由商业信誉提高）。利润受本城对应基础设施、专业网络内对应专业的启用等级及该领域商业化影响；具体报价在「资本投资」中查看，签约后锁定。');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_4','资本信托'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_4','资本信托');
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_COMMERCE_INSTITUTION_4_HELP','成熟商业组织配置发展资本、重组既有资产，以长期稳定经营积累信誉。[NEWLINE][NEWLINE]发展投资[NEWLINE]沿本城出发的直接国内贸易路线，投资目标城市的合格区域：支付其可建下一阶建筑中最低理论金币购买价的 15%，使该区域建筑获得 +50% 建造生产力，可与标准化加算。该区域下一座合格建筑完成后结束，不绑定报价建筑。每名在岗商业专家提供一个签约名额；每座目标城市同时限一份发展投资。已签合同不因商路、专家或启用等级变化而取消。[NEWLINE][NEWLINE]资产重组[NEWLINE]可用 500 生产力训练重组团队（标准速度）。在潜力至少为 2 的己方专业城市执行资产清算，永久扣除 1 级潜力；重组期间非食物产出及盈余食物增长降低 75%。至少 5 个完整回合后，在同城另一个合格专业区域执行资产配置，消耗团队并转换专业，不自动结束重组。[NEWLINE][NEWLINE]商业信誉[NEWLINE]首次建立四级商业机构后，只要保有商业身份，每个完整回合累计 1 点信誉，上限 40（标准速度）。启用四级时，每点信誉使商业化收益提高 0.5%，风险投资失败的本金返还比例提高 0.5 个百分点，最高分别为 +20% 与返还 70%。暂时失去启用等级不清除信誉；退出商业身份则清零。'),('en_US','LOC_SPC_COMMERCE_INSTITUTION_4_HELP','成熟商业组织配置发展资本、重组既有资产，以长期稳定经营积累信誉。[NEWLINE][NEWLINE]发展投资[NEWLINE]沿本城出发的直接国内贸易路线，投资目标城市的合格区域：支付其可建下一阶建筑中最低理论金币购买价的 15%，使该区域建筑获得 +50% 建造生产力，可与标准化加算。该区域下一座合格建筑完成后结束，不绑定报价建筑。每名在岗商业专家提供一个签约名额；每座目标城市同时限一份发展投资。已签合同不因商路、专家或启用等级变化而取消。[NEWLINE][NEWLINE]资产重组[NEWLINE]可用 500 生产力训练重组团队（标准速度）。在潜力至少为 2 的己方专业城市执行资产清算，永久扣除 1 级潜力；重组期间非食物产出及盈余食物增长降低 75%。至少 5 个完整回合后，在同城另一个合格专业区域执行资产配置，消耗团队并转换专业，不自动结束重组。[NEWLINE][NEWLINE]商业信誉[NEWLINE]首次建立四级商业机构后，只要保有商业身份，每个完整回合累计 1 点信誉，上限 40（标准速度）。启用四级时，每点信誉使商业化收益提高 0.5%，风险投资失败的本金返还比例提高 0.5 个百分点，最高分别为 +20% 与返还 70%。暂时失去启用等级不清除信誉；退出商业身份则清零。');
