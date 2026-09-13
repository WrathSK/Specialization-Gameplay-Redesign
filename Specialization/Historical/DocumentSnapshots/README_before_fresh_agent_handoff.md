<!-- Frozen handoff snapshot. Historical assertions only; current README/Status supersede. Relative links rebased; exact original bytes in DevelopmentBackups/Specialization-before-fresh-agent-handoff. -->
# Specialization：唯一协作入口

Owner: Codex（规则变更须用户确认）
Phase: D0014 / A0110，B051.67科研全部非学院区域复制待最小复验；工业4.5/科研半点已按用户回报通过。
Governance Revision: G0006
Design Authority: User
Local File Writer: Codex

## 当前权威

当前：[D0014范围修正](../../Reports/Technical/Specialization_D0014_All_District_Copy.md)及Status顶部优先；不重复旧工业半点测试。

当前：[B051.66修正与单项复验](../../Reports/Technical/Specialization_B051_Background_Fix.md)。旧65实机失败，原三案暂停，不要求整批重测。

当前以[Status](../../Status/Specialization_P0_Status.md)为准：[B051实现报告](../../Reports/Technical/Specialization_B051_Automatic_Copy_Yields.md)与[三项最小测试](../../Status/Validation/Cases/B051_Automatic_Copy_Yields.md)。本轮恢复实施，仅两项50%复制；标准化待后续接入。

### 先前阶段链接（不覆盖当前Status）

当前：[剩余工作盘点与方案](../../Reports/Technical/Specialization_v01_Remaining_Work_Review.md)、[B050五图通过](../../Status/Validation/Results/Specialization_B050_User_Result.md)。D0013明确标准化学习规则，本轮不实际实现，无新增测试。

当前：[B050半点实验](../../Reports/Technical/Specialization_B050_Half_Yield_Experiment.md)、[标准化记录](../../Reports/Technical/Specialization_Standardization_Storage_Research.md)。仅[两项新测试](../../Status/Validation/Cases/B050_Half_Yield.md)，B049不重测。

最新：[B049用户结果与提示修正](../../Status/Validation/Results/Specialization_B049_User_Result.md)。当前批次已关闭，不重复原两项测试；固定50%收益尚未启用。

当前：[B049移民UX与Lv4复制准备](../../Reports/Technical/Specialization_B049_Settler_UX_Lv4_Copy.md)，[两项只读案例](../../Status/Validation/Cases/B049_Lv4_Copy_Basis.md)。B048已用户通过；以下旧阶段说明不覆盖Status顶部。

最新：[B048科研/文化Lv4百分比](../../Reports/Technical/Specialization_B048_Lv4_Percent.md)，[当前小批次](../../Status/Validation/Cases/B048_Lv4_Percent.md)。不是完整Lv4；施工队不重测。

最新：[D0012施工队整数金额](../../Reports/Technical/Specialization_D0012_Integer_Crews.md)，已接受并落实，快速五档167/281/502/670/911，无新独立测试批次。

最新：[B046口述结果](../../Status/Validation/Results/Specialization_B046_User_Result.md)。一级实际167，项目成本符合向下取整；排序通过。尚未修改金额公式，无新测试批次。

当前[B046快速速度精度测试](../../Status/Validation/Cases/B046_Crew_Precision.md)，B045已通过。五档连续排序顺带观察，不另派排序验收。

本轮仅[B045施工队UX](../../Reports/Technical/Specialization_B045_Crew_UX.md)：命名、提示和固定确认位置；不改机制。当前用户仅需报告末尾最小复验，不派旧整批重测。

当前交付：[B044五档施工队项目](../../Reports/Technical/Specialization_B044_Crew_Projects.md)，[三项用户测试](../../Status/Validation/Cases/B044_Crew_Projects.md)。B043全部正常已登记，四图已归档；提示改为分行中文。历史阶段描述不覆盖Status当前矩阵。

最新同步：Accepted **D0011** → **A0098**，见[D0010征服分流同步](../../Reports/Technical/Specialization_D0010_Architecture_Sync.md)。征服三类模式仅完成本地准备，尚无原生Claim/Conquest测试包；住房B034已按五图范围通过，显示延迟已接受。B027限定DEV direct接收两图按观察范围通过；未部署新Commerce IV。下方阶段历史不覆盖本说明。按用户新优先级恢复网络可读性与撤销；小数承载研究暂停。

- [Design Spec](../../Design/Specialization_v0.1_Design_Spec.md)：D0013 / ACCEPTED，当前游戏设计意图权威（各条成熟度分别保留）。
- [Design ChangeLog](../../Design/Design_ChangeLog.md)：已登记D0010接受凭据及正式Spec SHA256，并保留旧版记录。
- [Architecture A0108](../../Architecture/Specialization_v0.1_Architecture.md)：已同步D0013的实现架构；技术限制不覆盖已接受Spec。
- [Status](../../Status/Specialization_P0_Status.md)：唯一当前验证矩阵/待办；B010未测且暂停。
- [技术索引](../../Reports/Technical/README.md)、[迁移报告](../../Reports/Proposals/Specialization_Phase1_Migration_Report.md)、[路径映射](../../Reports/Proposals/Phase1_Path_Map.json)。

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

- [唯一运行源码](../../../Sid%20Meier%27s%20Civilization%20VI/Mods/SpecializationP0)，B026 / manifest33，UUID不变。
- [Tests](../../../DevelopmentTests)；[Backups](../../../DevelopmentBackups)；[截图收件箱](../../../DevelopmentReports/ScreenshotInbox)均原地保留。
- 外层Mods目录不是当前运行目录；CityGPPProbe为另一个项目，不纳入本次整理。
- DevelopmentReports旧文档路径只保留跳转，不是第二份权威正文。

## 设计顾问与用户审阅

Codex是唯一本地文件维护者；外部Design Chat不再直接写本地文件，只提供proposal/review。用户可以转交分析，但未经用户明确接受不成为accepted Design。完整规则见[AGENTS](../../AGENTS.md)。

D0001已由用户明确接受，包含v0.1与Future；未决、候选和PROVISIONAL仍保持原状态。[首轮审阅说明](../../Reports/Proposals/Specialization_D0001_Draft_Review.md)仅保留历史审阅背景，当前规则以Spec为准。

Design=WHAT、Architecture=HOW、Status=实际实现/验证。Architecture A0077已同步D0002并保留WHAT/HOW边界；当前Sync Status为SYNCED_WITH_LIMITATIONS；[同步记录](../../Reports/Technical/Specialization_D0001_Architecture_Sync.md)列出规则覆盖。旧版本已原样归档；当前仅恢复离线计算，B010仍延后。

## 用户交付方式

每次先给独立中文用户摘要，再提供技术细节；摘要顺序与固定结尾遵循[AGENTS用户交付规则](../../AGENTS.md#用户交付规则g0003用户明确要求)。用户无需读源码理解结论。

当前结果：[B011两案实机记录](../../Status/Validation/Results/Specialization_B011_User_Result.md)，无需重复测试。B010继续延后，不重复已确认的旧测试。

用户本次投递截图的位置：[ScreenShots](../../ScreenShots)。可以继续按系统默认文件名投递；助手按时间与报告索引核对，不要求重命名。原DevelopmentReports/ScreenshotInbox仍原地保留，没有移动或删除。

最新本地进展：[D0002差异同步](../../Reports/Technical/Specialization_D0002_Architecture_Sync.md)、[新城写入计划与模拟](../../Reports/Technical/Specialization_City_Fact_Write_Plan.md)。没有部署新运行包，无新增用户测试。

新增本地结果：[身份账本与写入故障恢复](../../Reports/Technical/Specialization_City_Identity_Storage.md)。运行仍B011，存储探针尚未部署。

当前结果：[B012五图实机记录](../../Status/Validation/Results/Specialization_B012_User_Result.md)，无需重复测试。本节取代上方历史进展中的“运行仍B011/尚未部署”；本次只写专用DEV表，不写专业。

截图工作流已批准：你只向[ScreenShots](../../ScreenShots)投递；Codex读完登记后归档到[Evidence](../../Status/Validation/Evidence)，保持原名、不复制、不自动删除。当前[B012原图](../../Status/Validation/Evidence/B012)已归档，收件箱可继续投递。

当前结果：[B013五图实机记录](../../Status/Validation/Results/Specialization_B013_User_Result.md)，无需重复测试。只为加载后新建测试城市写DEV token，旧城不补写。上方更早“无新增测试/运行B012”属于历史交付记录，以本项及Status为准。

当前结果：[B014三图实机记录](../../Status/Validation/Results/Specialization_B014_User_Result.md)，两案按观察范围通过；[原图已归档](../../Status/Validation/Evidence/B014)。仅持久观察，不锁定正式专业；无新增测试，B010仍延后。

当前准备：[D0004与统一完成记录](../../Reports/Technical/Specialization_D0004_Completion_Journal.md)。有效通知先后规则已确认，离线准备通过；运行仍B014，无新增用户测试。

当前同步：[D0005与本地模型](../../Reports/Technical/Specialization_D0005_Architecture_Sync.md)，工业多源、首都source自接入及征服保留事实已适配；真实新城提交器仍待接入。运行B014，无新增实机批次。

当前结果：[B015三图判读](../../Status/Validation/Results/Specialization_B015_User_Result.md)，新城/学院/重载按观察范围通过，[原图已归档](../../Status/Validation/Evidence/B015)。无新增测试；D0006/7文档同步已完成，资格实现待接入。上方早期状态为阶段记录。

当前同步：[D0007（含D0006）](../../Reports/Technical/Specialization_D0007_Architecture_Sync.md)。通用参与资格、休眠成果、军事IV架构边界已登记；当前B015仍是固定测试载体实验，不代表新资格已部署。无新用户测试。

当前结果：[B019四图复验通过](../../Status/Validation/Results/Specialization_B019_User_Result.md)，原图已归档，无需补测；当前状态以Status为准。

当前结果：[B020四图复验通过](../../Status/Validation/Results/Specialization_B020_User_Result.md)，额外放置截图一并归档，无需补测；同回合Cheat完成路径，重载记录只读。

同步状态：D0008已完成架构同步，各项Future成熟度保留；当前v0.1范围不扩大。

当前结果：[B021正常恢复三图通过](../../Status/Validation/Results/Specialization_B021_User_Result.md)，原图已归档，无需补测。按用户要求优先Cheat机制测试，极端故障边界延后，必要保护保留。

当前测试：[B022 Research Lv1原生收益](../../Status/Validation/Cases/B022_Research_Lv1_Yields.md)，显式ON/OFF测岗位真实收益，完整自动专业系统未启用。

当前结果：[B022实机复验](../../Status/Validation/Results/Specialization_B022_User_Result.md)，无需补测；下一项常数型Lv1自动应用。上方B022测试入口保留为案例历史。

当前：[B023自动Lv1测试](../../Status/Validation/Cases/B023_Automatic_Constant_Lv1.md)；[Network连接与分发提案](../../Reports/Proposals/Specialization_Network_Connection_Distribution_Plan.md)等待后台UI桥接候选实验决定，未启用网络收益。

最新：[B024修复与现有存档复验](../../Reports/Technical/Specialization_B024_Auto_Scan_Fix.md)，取代B023原测试安排。

最新结果：[B024复验](../../Status/Validation/Results/Specialization_B024_User_Result.md)，无需补测；下一重点Network方案，桥接候选仍待决定。

当前Network方向：[后台来源已确认](../../Reports/Technical/Specialization_Network_Background_Source_Decision.md)，无需再次批准桥接，不依赖打开窗口；取代上方历史待决定说明，下一步接入网络重建。

当前新增：[B025后台网络测试](../../Status/Validation/Cases/B025_Background_Network.md)，现有存档可用，不打开贸易总览，不发网络收益。

当前复验：[B026首都与目的城](../../Reports/Technical/Specialization_B026_Trade_Count_Fix.md)，取代B025原多源测试顺序。

最新结果：[B026八图复验](../../Status/Validation/Results/Specialization_B026_User_Result.md)，无需重复本批；文化接入与全国接收N语义详见结果。下一项诊断可读性与撤销准备，未启用网络收益。

当前：[B027直接接收一个测试](../../Status/Validation/Cases/B027_Direct_Reception.md)，[实现及商业IV调查](../../Reports/Technical/Specialization_B027_Direct_Reception.md)。旧撤销批次继续延后。

最新：[B027两图通过](../../Status/Validation/Results/Specialization_B027_User_Result.md)，无需补测；[商业IV条件总产出方案与防循环研究](../../Reports/Technical/Specialization_CommerceIV_Basis_And_Cycles.md)，尚未启用汇聚收益。

当前：[B028只读来源产出](../../Status/Validation/Cases/B028_Source_Totals.md)。不升级专业或发放汇聚，旧网络实机批次继续延后。

最新：[B028两图通过](../../Status/Validation/Results/Specialization_B028_User_Result.md)，无需补测；高级专业收益未启用，下一步商业IV承载研究。

当前：[B029固定收益实验](../../Status/Validation/Cases/B029_Fixed_Yield_Carrier.md)，显式开启/关闭，非商业IV。

当前：[B029旧档失败记录](../../Status/Validation/Results/Specialization_B029_Old_Save_Failure.md)，改用[新局首都整数对照](../../Status/Validation/Cases/B029_New_Game_Control.md)，无需建区域。运行包未修改。

最新：[B029新局整数通过](../../Status/Validation/Results/Specialization_B029_New_Game_Result.md)，沿用本次新局做[半点/重复两图](../../Status/Validation/Cases/B029_Fractional_Followup.md)，无需再新建。

最新：[B029半点实际未体现](../../Status/Validation/Results/Specialization_B029_Fractional_Result.md)，OFF通过；不重复同组测试，不自动改整数化。
