# B015 — 用户实机三图判读

Document Owner: Codex
Build: P0-B-015 / modinfo22
Verification: USER_GAME_TEST_PASS（本次新城、学院完成及重载观察范围）
Evidence: 用户“看起来没问题，复验截图”，三张截图逐张读取

USER_GAME_TEST_PASS表示用户实际游戏证据通过，不是本地模拟。原图见[Evidence/B015](../Evidence/B015/)，移动前后SHA256一致。

| 文件时间 / 阶段 | 专业 / potential | revision | 本次加载写入 | 最近动作 |
|---|---|---|---|---|
| 19:26:27 / 新城费城 | NONE / 0 | 0 | 1 | FOUNDATION_SAVED |
| 19:26:53 / 学院完成 | RESEARCH / 1 | 1 | 2 | DEV_SPECIALIZATION_SAVED |
| 19:27:51 / 重载后 | RESEARCH / 1 | 1 | 0 | NONE |

三图city=393221、token=DEV-B013-P0-2一致。后两图first=DISTRICT_CAMPUS、district=786443、turn=1一致。全部health=TRACKING、stopped=false、AFTER_LOAD_CLOSE、Constructed=REGISTERED，均显示ACK，未见ERROR/STOP/GAP。

## 判定

- B015-1新城分支：创建资格并保存NONE/0通过。未提供旧城UNTRACKED画面或明确数值，不把旧城分支登记为独立实机PASS；重复读取/放置也没有独立画面。无需因此重发整批，本次结果范围明确保留。
- B015-2：学院完成后正确保存Research候选/Potential1，累计写入1→2，通过。
- B015-3：按本批提交顺序的保存重载阶段，记录字段保持，当前加载写入0，通过；截图不包含退出菜单的过程。
- 三图同为游戏T1，未说明完成方式；可见Cheat Panel不等于证明使用了哪种完成指令。不外推自然跨回合生产或所有四族。
- DEV候选事实依然不是已启用正式收益。未测同时完成、故障/GAP、征服继承、永久UID、Mod中断或多人，不扩大结论。

## 本轮处理

三图已归档，当前Status/Architecture登记限定范围结果。未修改运行包或Tests，未运行测试、未启动游戏。无新增用户测试，B010继续延后。

另核对磁盘Accepted已更新为D0006，hash与ChangeLog一致；PROG章节与冻结D0005逐字一致，本次结果适用范围不变。Architecture整体仍同步至D0005，D0006技术映射待审；本轮不编辑Design。
