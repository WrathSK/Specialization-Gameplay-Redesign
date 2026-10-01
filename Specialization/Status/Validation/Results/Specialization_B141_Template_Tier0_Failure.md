# B141.168 — 模板首次初始化失败：合法Tier 0与持久记录校验冲突

2026-09-30，三图逐张读取并归档于外部 `Specialization/Status/Validation/Evidence/B141_Template_Tier0_Failure_20260930/`，manifest保留原名及SHA256；3/3移动前后MATCH。用户说明已另读工业认领前存档并重新认领，征服前已有集市和粮仓。这些是用户操作陈述，不伪称截图展示完整征服/认领过程。

## 原生观察及验收边界

| 图 | 观察 |
|---|---|
| 16:53:47 | B141.168，city=131073；“标准化模板”入口可见且返回报告。尚无账本、当前建筑同步待完成、本次加载扫描1/写入0、最近无新增、状态STD_FACTS_NOT_READY。扫描/写入为模块本次加载总计，不是该城逐建筑计数。 |
| 16:55:45 | 同城工业网络折扣：有效来源空、最高0%、匹配建筑0、DISCOUNT_SAMPLE_SIZE。只能确认当时报告状态；未展示ACTIVE3/有效路线/接收资格，不能仅凭0%单独判定折扣机制失败。 |
| 16:59:58 | 城市建筑列表可见市中心粮仓、商业中心集市及工业区。普通建筑确实存在；工业支持carrier仍可见不等于模板已写入或ACTIVE3。 |

只读按钮可见/返回所测报告 **USER_GAME_TEST_PASS（该范围）**。模板初始化 **USER_GAME_TEST_FAIL**；折扣与冷加载没有完成验收。暂停当前流程，无需再重复征服/认领；B129既有Claim范围PASS保留，不能扩成全部E2失败或全部E2通过。

## 具体原因与本地复现

- [StandardizationCatalog](../../../../Mod/StandardizationCatalog.lua)原有目录接受HD非负整数Tier；粮仓属于CENTER_BASIC，当前真实运行DB中HD Tier=0、非InternalOnly、非Wonder、非dummy，目录启用。这不是Shared D普通区域T1权重，不能把粮仓模板强改成T1绕过问题。
- [Standardization](../../../../Mod/Standardization.lua)学习当前实际建筑，允许该Tier 0行进入候选账本；其账本校验也没有Tier≥1要求。
- [CityProgressionStore](../../../../Mod/CityProgressionStore.lua)提交前通过[CityIdentityRead.Preview](../../../../Mod/CityIdentityRead.lua)验证记录。该旧证据校验器却要求每条模板Tier≥1。因此包含粮仓的候选账本被拒绝为TEMPLATES，Store抛出STORE_RECORD_INVALID；原身份及待初始化标记保留，未确认模板写入。
- Standardization.guard仅识别STD_/TEMPLATES_字符串；STORE_RECORD_INVALID被归入通用STD_FACTS_NOT_READY，隐藏了实际记录拒绝原因。

**STATIC_CONFIRMED + LOCAL_SIMULATION_PASS（失败复现/对照断言，不是修复PASS）**：临时fixture执行当前实际Catalog/Store/Standardization/Claim/CityIdentityRead，目录使用已有本机配置指向的实际HD数据库并只读查询。合法首次工业Claim、当前粮仓Tier0＋合格Tier1商业建筑→身份仍INDUSTRY、UNINITIALIZED/pending、扫描1/写入0、STD_FACTS_NOT_READY；隔离Preview的拒绝理由为TEMPLATES。仅去掉粮仓的Tier1对照→INITIALIZED、写入1。没有修改源码、永久游戏数据或真实存档，没有在Civ VI中读取到对应内部堆栈；不能把本地堆栈当原生日志。

实际部署的CityIdentityRead/Store/Standardization/Catalog与当前develop四文件hash一致。当前配置指向的运行DB包含HD_BuildingTiers和HD_DUMMY_BUILDINGS；前轮缺表发生在外层旧缓存DB。本次已复核正确DB与真实目录，不修改旧报告/runner断言，不将旧完整B052测试标PASS。

B140生命周期模拟使用Tier1/2受控目录，遗漏了原有Tier0市中心模板与持久validator的交互；其A–G证据保留为该fixture范围，不能代表真实HD完整目录PASS。

## 下一最小修复（建议，未实施、待授权）

1. 对齐持久模板结构校验与原有目录的非负整数Tier语义，保留所有身份、绑定、账本、目录/历史损坏保护；不新增目录对象、组、折扣或Gameplay规则。
2. 让报告保留确切的记录拒绝原因，避免再将持久化拒绝伪装成普通事实未就绪；不扩张清理/重建。
3. 补粮仓Tier0＋商业普通建筑首次认领/并集同步/冷加载/重复通知回归，及负数、损坏/缺失历史仍拒绝的负对照。复用现有本地生命周期与退出隔离检查，不要求旧长测。

已认领而保留UNINITIALIZED/pending的记录可作为修复后的续测对象；不因本次失败清除Identity/Potential/投资或把历史缺失一概当首次。修复前不要求重复测试。无新Design决定；不推进F、不部署。本轮仅归档与调查/状态文档。
