# B020：用户四图复验

Document Owner: Codex
Build Observed: P0-B-020
Verification: USER_GAME_TEST_PASS（限定新城、同回合Cheat完成学院及正常重载只读）

用户明确报告人工验证无问题，并说明：学院在放置地基的同一回合，使用Cheat Panel“完成当前城市项目”完成。四张图均回合1，城市ID均458758。保存退出重载过程依用户按批次回报及计数变化确认，不冒充完整操作录像或事件日志。

| 时间（2026-09-11） | 观察 | DEV事实 | revision / 本次加载写入 | 模式 / 最近动作 |
|---|---|---|---|---|
| 22:30:33 | 新城，无生产项目 | NONE / 0 | 3 / 3 | LIVE_THIS_LOAD / FOUNDATION_DONE |
| 22:31:05 | 学院在建，城市UI显示60回合后完成 | NONE / 0 | 3 / 3 | LIVE_THIS_LOAD / FOUNDATION_DONE |
| 22:31:16 | 用户所述Cheat完成后 | RESEARCH / 1 | 6 / 6 | LIVE_THIS_LOAD / COMPLETION_DONE |
| 22:32:43 | 保存重载后 | RESEARCH / 1 | 6 / 0 | LOAD_READ_ONLY / NONE |

四图均DONE、stopped=false、load=true、complete=REGISTERED。第二张是额外的学院放置未完成证据，并非无意义重复；保留归档。B020-1和B020-2符合本批判据。

确认范围：已观察新城进入B020记录；放置不锁定，实际完成后记录RESEARCH/1；此Cheat同回合路径中B015→B020回调顺序兼容；正常重载保留记录且B020写入0。重复Read未有独立第五张截图，依用户整体通过回报登记，不要求补拍。

不扩大为自然跨回合生产、其它专业/替代区域、后续多区域竞争、全部Mod事件顺序、真实资格撤销、跨owner永久UID、崩溃原子性或重载后继续写入已通过。LOAD_READ_ONLY是当前DEV边界，正式跨读档历史恢复仍待实现。未启用专业收益。

[四张原图](../Evidence/B020/)逐张读取后已归档，保留默认文件名，移动前后SHA256一致，见manifest.json。运行B020/modinfo27、Design、Source、Tests未改，没有新增本地测试，未启动游戏。

下一项建议研究并实现跨加载历史检查与安全恢复，先做本地验证，再给必要最小实机批次；不再重复本批同回合Cheat路径。当前无补测，B010继续延后。唯一当前队列：[Status](../../Specialization_P0_Status.md)。
