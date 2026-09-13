# Specialization：唯一协作入口

Owner: Codex（规则变更须用户确认）
Phase: D0002已接受；Architecture A0012已同步D0002并记录技术限制，已完成离线多源max与城市专业状态；运行包B012独立DEV表存储探针，两案已实机通过；B011结果保留。
Governance Revision: G0003
Design Authority: User
Local File Writer: Codex

## 当前权威

- [Design Spec](Design/Specialization_v0.1_Design_Spec.md)：D0002 / ACCEPTED，当前游戏设计意图权威。
- [Design ChangeLog](Design/Design_ChangeLog.md)：已登记D0002接受凭据及正式Spec SHA256，并保留D0001记录。
- [Architecture A0012](Architecture/Specialization_v0.1_Architecture.md)：已同步D0002的实现架构；技术限制不覆盖已接受Spec。
- [Status](Status/Specialization_P0_Status.md)：唯一当前验证矩阵/待办；B010未测且暂停。
- [技术索引](Reports/Technical/README.md)、[迁移报告](Reports/Proposals/Specialization_Phase1_Migration_Report.md)、[路径映射](Reports/Proposals/Phase1_Path_Map.json)。

## Single writer

| 路径/类别 | 唯一日常写入者 |
|---|---|
| Design内Spec与ChangeLog | Codex维护；用户是最终Design Authority，仅用户明确接受才能标ACCEPTED |
| Architecture / Status / Validation / Reports | Codex；Design Chat只读/Review |
| 运行源码 / Tests | Codex，离线多源计算和城市状态已恢复；仅新增B011只读探针，正式机制未启用 |
| README / AGENTS / 路径及owner说明 | Codex；规则变更由用户确认 |
| Historical / Backups / 冻结结果原件 | 冻结，不就地改；纠正写新记录并由Status引用 |
| ScreenshotInbox | 用户投递；助手读证据，不默认删除/改名 |

## 物理工程位置（不另建Source/Runtime）

- [唯一运行源码](../Sid%20Meier%27s%20Civilization%20VI/Mods/SpecializationP0/)，B012 / manifest19，UUID不变。
- [Tests](../DevelopmentTests/)；[Backups](../DevelopmentBackups/)；[截图收件箱](../DevelopmentReports/ScreenshotInbox/)均原地保留。
- 外层Mods目录不是当前运行目录；CityGPPProbe为另一个项目，不纳入本次整理。
- DevelopmentReports旧文档路径只保留跳转，不是第二份权威正文。

## 设计顾问与用户审阅

Codex是唯一本地文件维护者；外部Design Chat不再直接写本地文件，只提供proposal/review。用户可以转交分析，但未经用户明确接受不成为accepted Design。完整规则见[AGENTS](AGENTS.md)。

D0001已由用户明确接受，包含v0.1与Future；未决、候选和PROVISIONAL仍保持原状态。[首轮审阅说明](Reports/Proposals/Specialization_D0001_Draft_Review.md)仅保留历史审阅背景，当前规则以Spec为准。

Design=WHAT、Architecture=HOW、Status=实际实现/验证。Architecture A0012已同步D0002并保留WHAT/HOW边界；当前Sync Status为SYNCED_WITH_LIMITATIONS；[同步记录](Reports/Technical/Specialization_D0001_Architecture_Sync.md)列出规则覆盖。旧版本已原样归档；当前仅恢复离线计算，B010仍延后。

## 用户交付方式

每次先给独立中文用户摘要，再提供技术细节；摘要顺序与固定结尾遵循[AGENTS用户交付规则](AGENTS.md#用户交付规则g0003用户明确要求)。用户无需读源码理解结论。

当前结果：[B011两案实机记录](Status/Validation/Results/Specialization_B011_User_Result.md)，无需重复测试。B010继续延后，不重复已确认的旧测试。

用户本次投递截图的位置：[ScreenShots](ScreenShots/)。可以继续按系统默认文件名投递；助手按时间与报告索引核对，不要求重命名。原DevelopmentReports/ScreenshotInbox仍原地保留，没有移动或删除。

最新本地进展：[D0002差异同步](Reports/Technical/Specialization_D0002_Architecture_Sync.md)、[新城写入计划与模拟](Reports/Technical/Specialization_City_Fact_Write_Plan.md)。没有部署新运行包，无新增用户测试。

新增本地结果：[身份账本与写入故障恢复](Reports/Technical/Specialization_City_Identity_Storage.md)。运行仍B011，存储探针尚未部署。

当前结果：[B012五图实机记录](Status/Validation/Results/Specialization_B012_User_Result.md)，无需重复测试。本节取代上方历史进展中的“运行仍B011/尚未部署”；本次只写专用DEV表，不写专业。
