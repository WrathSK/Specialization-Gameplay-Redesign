INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_PROJECT_SPC_ERA_DIALOGUE_NAME','时代对话'),
('en_US','LOC_PROJECT_SPC_ERA_DIALOGUE_NAME','时代对话'),
('zh_Hans_CN','LOC_PROJECT_SPC_ERA_DIALOGUE_DESCRIPTION','需本城具备文化专业身份且启用等级达到 3 级。开启后将作为唯一当前生产目标，连续占用完整的 1 个回合（每城按项目启动时的游戏时代计算，每个时代最多成功完成一次）。完成时，本城合格馆藏每覆盖一个不同的作品时代，便为巨作原生旅游业绩倍率永久累加 5 个百分点（不放大「意义延展」的追加产出）。若中途打断将取消本轮项目，但不会消耗该时代的成功次数；项目开启前未分配的生产力及项目期间产生的生产力均不会结转至后续目标。'),
('en_US','LOC_PROJECT_SPC_ERA_DIALOGUE_DESCRIPTION','需要文化身份且ACTIVE III。选为唯一当前目标，连续占用完整一回合。完成时，每个合格馆藏时代记录+5个百分点；每城每个启动游戏时代最多成功一次。中断取消本轮，不消耗成功额度。已有未分配生产与项目期间生产不留给后续目标。本批验证项目、保存与额度；累计倍率尚未接入实际产出。'),
('zh_Hans_CN','LOC_SPC_DIALOGUE_PROJECT_REPORT','时代对话'),
('en_US','LOC_SPC_DIALOGUE_PROJECT_REPORT','时代对话');

INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_SPC_DIALOGUE_CARRIER_HINT','读取项目、已用时代、累计百分比与当前生效状态（左右键均只读）。收益自动启用；当前采用仅旅游业绩的技术备用方案。'),
('en_US','LOC_SPC_DIALOGUE_CARRIER_HINT','读取项目、已用时代、累计百分比与当前生效状态（左右键均只读）。收益自动启用；当前采用仅旅游业绩的技术备用方案。');
