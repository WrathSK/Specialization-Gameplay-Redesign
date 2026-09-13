# 第一阶段文档迁移交付

Owner: Codex
State: COMPLETED_PHASE1 / WAITING_DESIGN_CHAT

仅文档与协作结构变更；未开发功能、未启动游戏、未运行功能测试。

## 迁移与校验

- 迁移前完整备份：`DevelopmentBackups/Specialization-Phase1-Before-20260911-144718`，含Reports、Tests、B010运行包及SHA256.json。备份内容逐项校验通过。
- 移动35份Specialization报告/文档，basename保持；旧入口为单向跳转。完整[路径映射](Phase1_Path_Map.json)。
- 34份冻结文档/结果/快照内容SHA256保持原样；263个受保护文件（运行Mods、Tests、既有Backups、截图、GPP资料及发现的ini配置）内容不变。
- 新建Design两个DRAFT_SHELL，没有设计正文、没有D0001、没有ACCEPTED。Architecture A0001保留完整过渡WHAT，已登记Research/Culture多源max用户确认；Status收敛为唯一验证矩阵/待办。
- 新建README/AGENTS、技术索引、Cases入口与Historical说明；当前三份短技术报告只写HOW，原始全文冻结归档。
- 源码、Tests、Backups、ScreenshotInbox原地保留；不新增Source/Runtime，不改变UUID、modinfo17或任何游戏加载配置。未执行会产生pyc/报告的测试。
- 原提案已加批准补充和实际交付指引，旧提案全文在迁移前备份中。

## 引用与历史缺件

内部Markdown链接检查未发现迁移造成的新断链。历史A005报告仍有两张迁移前就缺失的截图，不恢复、不伪造，冻结原文保持不变：
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/DevelopmentReports/Screenshot 2026-09-10 at 9.49.24 PM.png`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/DevelopmentReports/Screenshot 2026-09-10 at 9.49.52 PM.png`

历史冻结文档中的裸文件名/旧路径文字不批量改写，按Path Map及旧入口跳转定位。原Reports/Historical旧位置也只留跳转。技术source的外部链接仍按原位置检查，不改本机Steam/Workshop内容。

## 下一步

B010验证=USER_GAME_TEST_REQUIRED、Task State=DEFERRED_USER_PAUSE。当前没有要用户执行的P0批次。
Design Chat仅写Design中的Spec/ChangeLog，以Architecture A0001为过渡来源，用户确认D0001后Codex再进行正式hash/sync和WHAT去重。Research/Culture多源设计已确认但代码未实现；Industry合并不自动沿用。

## 实际路径

- `DevelopmentReports/Specialization_P0_B005_Unit_Type_Fix.md` → `Specialization/Historical/LegacyReports/Specialization_P0_B005_Unit_Type_Fix.md`
- `DevelopmentReports/Specialization_P0_Batch_A.md` → `Specialization/Historical/LegacyReports/Specialization_P0_Batch_A.md`
- `DevelopmentReports/Specialization_P0_Network_Sqrt.md` → `Specialization/Reports/Technical/Specialization_P0_Network_Sqrt.md`
- `DevelopmentReports/Specialization_P0_A007_NewGame_Result.md` → `Specialization/Status/Validation/Results/Specialization_P0_A007_NewGame_Result.md`
- `DevelopmentReports/Specialization_P0_Batch_B006.md` → `Specialization/Historical/LegacyReports/Specialization_P0_Batch_B006.md`
- `DevelopmentReports/Specialization_P0_A007_Result_Analysis.md` → `Specialization/Status/Validation/Results/Specialization_P0_A007_Result_Analysis.md`
- `DevelopmentReports/Specialization_P0_Shadow_Network_Integration.md` → `Specialization/Historical/LegacyReports/Specialization_P0_Shadow_Network_Integration.md`
- `DevelopmentReports/Specialization_P0_B007_Background_Dispatch_Fix.md` → `Specialization/Historical/LegacyReports/Specialization_P0_B007_Background_Dispatch_Fix.md`
- `DevelopmentReports/Specialization_P0_B009_Shadow_State.md` → `Specialization/Historical/LegacyReports/Specialization_P0_B009_Shadow_State.md`
- `DevelopmentReports/Specialization_B004_Binary_Evidence.txt` → `Specialization/Historical/LegacyReports/Specialization_B004_Binary_Evidence.txt`
- `DevelopmentReports/Specialization_P0_A005_Reading_Fix.md` → `Specialization/Historical/LegacyReports/Specialization_P0_A005_Reading_Fix.md`
- `DevelopmentReports/Specialization_P0_Marker_Storage.md` → `Specialization/Reports/Technical/Specialization_P0_Marker_Storage.md`
- `DevelopmentReports/Specialization_P0_B010_City_Role_Facts.md` → `Specialization/Historical/LegacyReports/Specialization_P0_B010_City_Role_Facts.md`
- `DevelopmentReports/Specialization_P0_A006_Governor_Fix.md` → `Specialization/Historical/LegacyReports/Specialization_P0_A006_Governor_Fix.md`
- `DevelopmentReports/Specialization_P0_B003_Readability.md` → `Specialization/Historical/LegacyReports/Specialization_P0_B003_Readability.md`
- `DevelopmentReports/Specialization_P0_A007_Native_Governor.md` → `Specialization/Historical/LegacyReports/Specialization_P0_A007_Native_Governor.md`
- `DevelopmentReports/Specialization_P0_B008_Batch_Flush.md` → `Specialization/Historical/LegacyReports/Specialization_P0_B008_Batch_Flush.md`
- `DevelopmentReports/Specialization_P0_B005_User_Result.md` → `Specialization/Status/Validation/Results/Specialization_P0_B005_User_Result.md`
- `DevelopmentReports/Specialization_P0_Batch_A004.md` → `Specialization/Historical/LegacyReports/Specialization_P0_Batch_A004.md`
- `DevelopmentReports/Specialization_P0_B002_User_Result.md` → `Specialization/Status/Validation/Results/Specialization_P0_B002_User_Result.md`
- `DevelopmentReports/Specialization_P0_Deferred_Cases.md` → `Specialization/Historical/LegacyReports/Specialization_P0_Deferred_Cases.md`
- `DevelopmentReports/Specialization_P0_B008_User_Result.md` → `Specialization/Status/Validation/Results/Specialization_P0_B008_User_Result.md`
- `DevelopmentReports/Specialization_P0_Status.md` → `Specialization/Status/Specialization_P0_Status.md`
- `DevelopmentReports/Specialization_P0_B007_User_Result.md` → `Specialization/Status/Validation/Results/Specialization_P0_B007_User_Result.md`
- `DevelopmentReports/Specialization_P0_B002_Findings.md` → `Specialization/Historical/LegacyReports/Specialization_P0_B002_Findings.md`
- `DevelopmentReports/Specialization_P0_Batch_B001.md` → `Specialization/Historical/LegacyReports/Specialization_P0_Batch_B001.md`
- `DevelopmentReports/Specialization_v0.1_Architecture.md` → `Specialization/Architecture/Specialization_v0.1_Architecture.md`
- `DevelopmentReports/Specialization_P0_B006_Background_Routes.md` → `Specialization/Historical/LegacyReports/Specialization_P0_B006_Background_Routes.md`
- `DevelopmentReports/Specialization_P0_BTS_Background_Read.md` → `Specialization/Reports/Technical/Specialization_P0_BTS_Background_Read.md`
- `DevelopmentReports/Specialization_File_Structure_Proposal.md` → `Specialization/Reports/Proposals/Specialization_File_Structure_Proposal.md`
- `DevelopmentReports/Specialization_P0_B004_Trade_Route_State.md` → `Specialization/Historical/LegacyReports/Specialization_P0_B004_Trade_Route_State.md`
- `DevelopmentReports/Specialization_P0_Batch_B004.md` → `Specialization/Historical/LegacyReports/Specialization_P0_Batch_B004.md`
- `DevelopmentReports/Specialization_P0_B009_User_Result.md` → `Specialization/Status/Validation/Results/Specialization_P0_B009_User_Result.md`
- `DevelopmentReports/Historical/Specialization_P0_Status_through_B003.md` → `Specialization/Historical/DocumentSnapshots/Specialization_P0_Status_through_B003.md`
- `DevelopmentReports/Historical/Specialization_v0.1_Architecture_through_B003.md` → `Specialization/Historical/DocumentSnapshots/Specialization_v0.1_Architecture_through_B003.md`

## 新建入口与维护文件

- `Specialization/AGENTS.md`
- `Specialization/Design/Design_ChangeLog.md`
- `Specialization/Design/Specialization_v0.1_Design_Spec.md`
- `Specialization/Historical/DocumentSnapshots/Specialization_P0_Status_before_phase1_B010.md`
- `Specialization/Historical/DocumentSnapshots/Specialization_v0.1_Architecture_before_phase1_B010.md`
- `Specialization/Historical/LegacyReports/Specialization_P0_B007_User_Result.md`
- `Specialization/Historical/LegacyReports/Specialization_P0_B008_User_Result.md`
- `Specialization/Historical/LegacyReports/Specialization_P0_B009_User_Result.md`
- `Specialization/Historical/LegacyReports/Specialization_P0_BTS_Background_Read.md`
- `Specialization/Historical/LegacyReports/Specialization_P0_Marker_Storage.md`
- `Specialization/Historical/LegacyReports/Specialization_P0_Network_Sqrt.md`
- `Specialization/Historical/README.md`
- `Specialization/README.md`
- `Specialization/Reports/Proposals/Phase1_Path_Map.json`
- `Specialization/Reports/Proposals/Specialization_Phase1_Migration_Report.md`
- `Specialization/Reports/Technical/README.md`
- `Specialization/Status/Validation/Cases/B010_Deferred.md`
- `Specialization/Status/Validation/Cases/Deferred_Mechanics.md`
- `Specialization/Status/Validation/README.md`

冻结原件的basename可能同时用于短技术报告；两者分别明确为当前HOW摘要与历史全文，后者不是第二份设计权威。
