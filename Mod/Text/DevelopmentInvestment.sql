INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_TITLE','发展投资'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_OPEN_HELP','打开发展投资面板：依托从本城出发的国内贸易路线，为目标城市的指定区域建筑提供 +50% 建造生产力加成。'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_CLOSE','关闭'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_CONFIRM','确认发展投资'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_REFRESH','刷新报价'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_BALANCE','国库：{1} [ICON_Gold]　已占用名额：{2} / {3}'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_CITY_ID','城市 #{1}'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_SELECT','请选择目标城市与区域'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_QUOTE','报价基准建筑：{1}[NEWLINE]最低理论购买价：{2} [ICON_Gold][NEWLINE]本次投资费用（15%）：{3} [ICON_Gold]（同阶候选建筑：{4}）'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_TERMS','合同效果：目标区域的合格建筑获得 +50% 建造生产力加成（与工业「标准化」加成相加计算）。[NEWLINE]结束条件：该区域完成下一座合格建筑后合同即告结束（不强制绑定报价时的基准建筑）。[NEWLINE]补充说明：中途改建其它目标不会取消合同；若通过金币购买或其它方式直接完成该区域建筑，合同同样随之结束。'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_CONTRACT','生效合同：{1}[NEWLINE]核定投入：{2} [ICON_Gold] ｜ 实际扣款：{3} [ICON_Gold]'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_HELP','发起签约需满足：本城商业启用等级达到 4 级、拥有从本城出发前往目标城市的直接国内贸易路线，且本城有空余的在岗商业专家名额。[NEWLINE]签约生效后，贸易路线变动或本城启用等级下降均不会取消合同；但若签约双方任一城市易主，合同将立即终止且不退还已投金币。'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_ACTIVE_REQUIRED','发起新合同需本城商业启用等级达到 4 级'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_CAPACITY_FULL','当前无空余的商业专家名额（已生效的合同仍继续维持）'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_OCCUPIED','目标城市已有未结束的发展投资'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_NO_BUILDING','该区域当前没有可建造的下一阶合格建筑'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_NO_OUTGOING','当前没有从本城出发的直接国内贸易路线目标城市'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_NETWORK_PENDING','等待本城出发商路核验'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_PRICE_UNKNOWN','暂无法获取可靠的理论购买价格，该领域当前无法签约'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_STALE','签约条件或建筑报价已发生变动，请刷新面板后重新核对'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_NO_GOLD','金币不足'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_WORKERS_UNKNOWN','商业专家名额暂不可确认'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_SPEED','本版发展投资仅支持标准速度'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_MONEY_HELD','扣款回执待核对，已阻止重复扣款，请保留日志'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_STATE_HELD','已暂停'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_WAITING','正在读取／确认…'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_STATE_DEBIT_INTENT','确认中'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_STATE_DEBIT_CALLING','扣款回执待核对'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_STATE_ACTIVE','执行中'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_STATE_COMPLETED','已完成'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_STATE_TERMINATED','已终止');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES ('zh_Hans_CN','LOC_SPC_DEVELOPMENT_STATE_UNKNOWN','状态暂不可确认：{1}');

-- B252 three-column presentation. No new transaction or gameplay state.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_CITIES','目标城市'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_DISTRICTS','投资区域'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_DETAILS','投资详情'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_SELECT_CITY','请选择目标城市'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_SELECT_DISTRICT','请选择投资区域'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_CITY_OPTIONS','{1} 个区域可投资'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_DISTRICT_READY','可签约 · {1} [ICON_Gold]'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_QUOTE_TITLE','报价与投入'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_EFFECT_TITLE','合同效果与完成条件'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_RULES_TITLE','签约与延续'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_CONTRACT_TITLE','最近一份合同'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_SOURCE','发起城市：{1}'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_BACK','返回上一级'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_NO_OPTIONS','当前没有可展示的目标城市，请查看签约条件或刷新报价。'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_NO_DISTRICTS','当前没有可投资的区域。'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_STATUS_TITLE','当前状态');

-- B253 display-only source summary. Monetary authority is unchanged.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_TREASURY','国库：{1} [ICON_Gold]'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_CAPACITY','已占用名额：{1} / {2}'),
('zh_Hans_CN','LOC_SPC_DEVELOPMENT_NO_QUOTE','当前没有可用报价，请查看合同状态或刷新报价。');
