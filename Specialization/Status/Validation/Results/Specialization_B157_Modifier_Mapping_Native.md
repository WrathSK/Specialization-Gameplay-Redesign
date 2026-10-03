# B157.184 — District归属与subject原生核验

Evidence: USER_GAME_TEST_PASS，限定本次OFF、所见三个District对象及五个Modifier的映射/subject读取；不是Meaning收益或完整L2 PASS。

## 两图确认

2026-10-03 10:23:52 / 10:24:02，同T62/B157.184、玩家0/City393220；OFF/SPLIT，配置S/G/C=0。剧场未掠夺，GREATWORK_QU_YUAN_1基础文化2、剧场作品实际4。7083定义，匹配5，未知玩家0、其它玩家跳过0。

| Modifier | owner和唯一subject共同的District / City | 当前映射 | Active |
|---|---|---|---|
| HD Writing Culture +2 | 1114126 /393220 | 本城已核验 | true |
| HD Writing Culture +2 | 1179663 /65536 | 其它城已核验：0/65536 | true |
| HD Writing Tourism scaling150 | 1114126 /393220 | 本城已核验 | true |
| HD Writing Tourism scaling150 | 1179663 /65536 | 其它城已核验：0/65536 | true |
| 旧GWA SPC_B060_CULTURE_P1_WRITING，flat1 | 1048589 /393220 | 本城已核验 | true |

每项subjects=1，展开的subject类型均DISTRICT，玩家0；其District/City/raw与该项owner相同。B157实际执行当前CityManager城市、该城区域FindID、区域父城及full reference检查后显示以上结果，不再仅根据raw数字相等归组。其它城没有混作本城；不外推所有格式、易主或其它存档情况。

## 意义与边界

- 已跨过本次原生District映射/subject读取门禁，可以用当前包观察Meaning启用实例，无需新增诊断代码或重部署。
- HD＋2与旧GWA＋1虽然同城，但属于不同District对象。这个差异是观测事实；截图未给区域名称/类型，不自行把它们命名为剧院/市中心，不解释SubValue，也不直接归因为跨区域限制。
- 作品仍4，不是简单2+2+1=5；Active/subject均已核对依然不能证明全部数值叠加。覆盖/取最大/其它资格或读取时序尚无法区分。前次OFF正常恢复旧writer的边界保持，不误清旧GWA。
- 当前OFF，没有Meaning实例；没有验证它的owner/subject、收益组合或退出。旧B155两个候选FAIL保持；不因这次诊断PASS升级能力状态。

## 当前包下一最小对照

目的：只区分Meaning实例未进入/挂载不同/正常存在但数值未叠加，以及退出是否恢复。保持同一回合、同城、同一著作和建筑/总督，不砍树、不推进回合、不启动100%Dialogue或主题化。

1. 从本图OFF/SPLIT开始，左键“切换验证配置”一次，确认显示“单一+3”（SINGLE3，不是倍率100%候选）。若不是该配置或报错，停在此处提供报告，不继续点。
2. 左键“意义延展验证”一次，进入“①基线”；随后右键同按钮读取Modifier诊断，截图第一组。
3. 再左键“意义延展验证”一次，进入“②追加”；随后右键同按钮读取，截图第二组。
4. **右键“切换验证配置”**直接退出（不要再左键“意义延展验证”进入③）；右键“意义延展验证”读取，截图第三组。

长报告补下半即可。异常/UNKNOWN时停止推进，记录报告；若实验已开启可用配置按钮右键结束。不要为了凑期望7反复点击/过回合。预期对照：HD同城文化实例在基线/追加持续；旧GWA在实验内退出，结束后正常重算恢复；Meaning只在②出现，观察其owner/subject和作品差值。此流程不是重复猜数值，而是用新增原生实例证据区分原因。精确recipient、倍率隔离、结算/冷加载仍另属未通过门禁，不自动延长本次测试。

## 归档与当前状态

两图逐张查看，原名原字节移至ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B157_Modifier_Mapping_20261003/`，manifest关联本记录，2/2 SHA256 MATCH。原图不提交Git。

source/live沿B157.184/source f75494b、既有receipt B157.184-f75494b-playtest.json DEVELOP_ACTIVE引用；本轮未重核外部运行包、未部署或启动游戏。只更新证据/当前状态/计划与已审阅hash，不改Mod/Design/GC/永久数据/main；没有新模拟或玩法回归。此前[本地证据](Specialization_B157_Modifier_Mapping_Local.md)及[B156原生记录](Specialization_B156_Modifier_Native_Read.md)不改写。
