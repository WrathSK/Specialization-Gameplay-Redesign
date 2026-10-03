# B153.180 — 意义延展原生测试中止

Evidence: USER_GAME_TEST_PARTIAL / USER_GAME_TEST_BLOCKED_C11；STATIC_CONFIRMED。完整文化追加与旧Dialogue四态门禁 **NOT_PASSED**。原53 Meaning＋26 K LOCAL结果保留其范围；不宣布正式能力、Floor公式或引擎primitive失败。
Baseline: develop `6a3bfa8`；runtime source `16b036d`，B153.180 / modinfo180。D0039 / Culture D0038不变。本轮仅读图、定域源码与只读数据库、归档和停止点记录；修复尚未授权。

## 三张截图直接证据

2026-10-03收到三图，已逐张查看并原样移入Git忽略目录 `local/legacy-workspace/Specialization/Status/Validation/Evidence/B153_P0L2B_Native_Stopped_20261003/`。manifest记录原名、大小、SHA256与观察；移动前后 **3/3 MATCH**。原图不进Git。

三图均显示T62、EDINBURGH (TEST)、P0-B-153.180，合格2件；每件理论追加1科研／4金币／3文化，预期文化追加合计6。图中“文化4级”按钮不是另一份独立ACTIVE权威。

| 截图／阶段 | 每件配置 S/G/C | 对话配置 | 原生作品总读数 S/G/C | 可证明范围 |
|---|---|---|---|---|
| 06:43:39／C00 | 0/0/0 | 0%已确认 | 0/0/8 | 基线入口成功、已记录，无原B152入口错误 |
| 06:43:47／C10 | 1/4/3 | 0%已确认 | 2/8/8 | 科研、金币即时作品读数增量匹配2/8；文化读数Δ0，预期6 |
| 06:43:58／仍C10 | 1/4/3 | 未确认 | 不采成功读数 | `ME_DIALOGUE_QUALIFICATION_CHANGED`、`ME_UI_CONFIGURATION_PENDING`；未进入C11 |

第二图的文化差值是当前作品API读数异常，不能升级为已证明整城结算没有收益或原生接口不支持。UI底部其它产出也有变化；同一显示回合不证明所有修正保持固定或面板已经完成刷新。本组没有跨回合结算、C11、C01、OFF或冷加载证据，也不声称中止后旧AUTO已恢复。

## 两个独立问题与直接依据

### 文化追加读数

[UI读取](../../../../Mod/UI/BoostGreatWorkRead.lua)对有巨作槽位的建筑汇总 `GetBuildingYieldFromGreatWorks`，没有使用整城Culture或实际市政进度作为第二口径。因此截图能够确认该接口文化合计不变，尚不能区分原生应用失败、读取口径或刷新时序。

[SQL](../../../../Mod/Data/CultureMeaningProbe.sql)的Culture片段使用 `MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD`、`YieldType=YIELD_CULTURE`、`YieldChange=1/2/4/8`；本次外部DebugGameplay数据库以只读方式核对代表性1/2片段及动态类型，定义存在且效应为 `EFFECT_ADJUST_CITY_GREATWORK_YIELD`。这仅是STATIC定义证据。旧Dialogue使用同类型的 `ScalingFactor`，不能据类型相同推导两套参数的原生Culture行为相同。未改数据库、SQL或收益公式。

### 对话阶段切换

[Meaning Advance](../../../../Mod/CultureMeaningProbe.lua)先在ACTIVE阶段要求Hold100，成功后才切SCALED；[Dialogue Hold/Read](../../../../Mod/Dialogue.lua)先替换holder，再Audit/核对当前投影。Read的 `ME_DIALOGUE_QUALIFICATION_CHANGED`精确含义是当前投影的 `applied` 不等于holder要求值，并非证明用户移动了总督。

两模块都读取同一个EffectiveFacts authority：Meaning经[只读facade](../../../../Mod/CurrentSpecializationFacts.lua)，Dialogue直接读取。同一有效事实时点没有两套互斥资格定义，但读取时点和保存的lastPlan／最新投影不同。C00的0%在Dialogue资格成立或不成立时都可能得到applied0，不能证明其独立资格读取一定为ACTIVE4。

还确认一条STATIC重入风险：Advance要求Hold100时Meaning.busy仍false且mode仍ACTIVE；Dialogue Audit的载体写入若同步发 `CityBuildingsChanged`，Meaning现有回调会Audit，按ACTIVE调用Hold0。嵌套Hold先把holder改0，再遇Dialogue BUSY失败；外层可能保留applied100，于是随后Read比较100与holder0报上述错误。BuildingAdded/Removed路径已有Dialogue owned过滤，不能把它们混为此链；原生Create/Remove是否在本次同步发CityBuildingsChanged尚未实测。这是源码存在的具体风险，**不是本组截图唯一原生根因已证实**。

现有53项LOCAL测试包含实际request/pair/iterator/失败路径，但其EffectiveFacts fixture仍mock城市active，且本次未验证上述原生重入时序；原PASS不扩大为所有资格读取或原生事件均已覆盖。

## 下一最小修复建议 — 等待授权

1. 限定Meaning／Dialogue阶段切换：避免未完成转换被现有更新路径按旧阶段重入，失败不能留下与阶段不一致的holder；保持正常当前事实、精确owned撤销、UNKNOWN和结束路径。资格诊断显示本次实际ACTIVE／原因，而非只给泛化错误码。补当前事实与同步建筑事件的少量定向回归。
2. 单独核对Culture整数追加原生路径与读数口径，按需加入有界、按需的整城Culture／进度辅助读数以区分应用和读取；先用既有正式接口及数据库定义，不改Floor、不补整城收益、不擅自更换Gameplay。不能把组合切换修好等同Culture收益已修好。
3. 本轮不要求立即重测。修复后再给一次同城最小对照；先确认C10文化追加确实可读／可结算，再续C11/C01倍率门禁，复用已取得的科研/金币整数证据，不重做旧小数或长测。

精确recipient仍为独立TECHNICAL_INVESTIGATION_REQUIRED；完整六yield/all-city/global旧GWA cutover及L3/M/N/U2未授权。未知对象保护仍只是实验边界，不变成正式资格规则。本轮没有新的Design决定。

## 状态与完整性

源码/live仍B153.180 / modinfo180；已有 `B153.180-16b036d-playtest.json` receipt的DEVELOP_ACTIVE、182/182 MATCH只按前次记录引用，本轮未重核外部包。没有运行Gameplay测试/模拟、改Mod/Design/GC/永久记录/main、部署或启动/关闭游戏。

文档selector/hash/链接与diff只验证本次记录一致性，不替代原生门禁。用户已暂停测试；当前只允许证据记录与只读调查，**等待定域修复授权**，不自动进入下一能力。保留[B153 LOCAL/部署记录](Specialization_B153_P0L2B_Entry_Repair.md)与[B152入口失败](Specialization_B152_P0L2B_Entry_Blocked.md)原件。
