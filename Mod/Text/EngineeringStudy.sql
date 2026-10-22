-- Descriptive project label, not a new frozen institution/ability name.
INSERT OR REPLACE INTO LocalizedText(Language,Tag,Text) VALUES
('zh_Hans_CN','LOC_PROJECT_SPC_ENGINEERING_STUDY_NAME','工程传统研习'),
('en_US','LOC_PROJECT_SPC_ENGINEERING_STUDY_NAME','工程传统研习'),
('zh_Hans_CN','LOC_PROJECT_SPC_ENGINEERING_STUDY_DESCRIPTION','需本城工业启用等级达到 4 级，且本城已完成的研习层数（L）少于本文明奇观历史覆盖的时代数（E）。开启后将连续占用 1 个完整的生产回合，完成后本城研习层数（L）永久 +1。当工业启用等级为 4 级时，每层研习成果使本城持有可靠模板的建造生产力加成与合格建筑金币购买折扣各提高 2 个百分点（当前版本暂未实装目标区域的逐模板购买折扣）。若中途打断、城市易主或启用等级下降，将取消未完成的当前轮次，但已积累的历史层数不会清零。项目将吸收开启前未分配的生产力及项目期间产生的生产力，不会结转至后续目标。'),
('en_US','LOC_PROJECT_SPC_ENGINEERING_STUDY_DESCRIPTION','工业ACTIVE IV，且本城已完成研习层数L小于全国奇观时代知识E时可用。完整占用一个生产回合，完成后本城L永久+1。ACTIVE IV时每层令持有模板的建造与合法建筑购买折扣各增加2个百分点。中断、易主或资格下降取消未完成轮次；历史层数不清零。项目吸收已有未分配及期间生产，不转给后续目标。区域逐模板购买折扣本批尚未接入。');
