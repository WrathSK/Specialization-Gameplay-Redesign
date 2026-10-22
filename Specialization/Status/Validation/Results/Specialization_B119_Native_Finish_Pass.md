# B119 — 独立原生完成承接项目，限定实机PASS

2026-09-28；B119.146。四张图已实际查看。USER_GAME_TEST_PASS仅覆盖本次手动FinishProgress、有7点项目进度、完成后换普通目标及用户确认的正常下一回合。

| 原图 | 可见证据 |
|---|---|
| 00:23:21 | 准备项目进度7，尚未完成 |
| 00:23:24 | 已调用一次原生FinishProgress，CALLED_NOT_PROVEN是调用记录 |
| 00:23:27 | 回合21、城131073、队列0、无生产目标、实验项目保留进度0、其它目标变化0项 |
| 00:23:40 | 回合21，城市当前普通目标纪念碑，原生面板0/50、6回合；队列(0)是界面的排队计数，不能误读为没有当前纪念碑 |

用户明确确认“过回合后正常”，无截图：作为用户实机陈述接受，不伪造下一回合精确进度或图像证据，不要求为归档重复测试。

因此，本Mod直接调用原生FinishProgress完成该无收益项目的受控路径通过；该次已投入7点没有可见地转入随后纪念碑，且后续一回合未报告异常。不扩大为所有隐藏池/任意数量/来源、chop/harvest、超量自然完成、取消/中断、存读或自动固定一回合系统PASS。没有证明关闭/卸载Cheat后的组合实测；源码无Cheat依赖是STATIC证据。

dummy仍显示高回合数符合本批范围：Cost1000000、原生按产能估计；尚未做自动定时或UI1T显示，不能把仅改文字当计时实现。下一建议先给出完整回合占用/结算时序＋专项目1T展示最小计划，并安排生产注入边界，不自动实施或发奖。

## 原图与SHA256

- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B119_Native_Finish_20260928/Screenshot 2026-09-28 at 12.23.21 AM.png`
  - `b407a9859f40dfd8475c6ca309af38548ac4794f958c809a11ce20bf6ed94ba5`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B119_Native_Finish_20260928/Screenshot 2026-09-28 at 12.23.24 AM.png`
  - `f3c21b789448634d152f5473db4e2e2bec9d884944db07ba512e398b53d952ce`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B119_Native_Finish_20260928/Screenshot 2026-09-28 at 12.23.27 AM.png`
  - `e57dce279aa8bf6b9a0f3806a29c0556eceadf1302dad9c8a59757da307ccdb1`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B119_Native_Finish_20260928/Screenshot 2026-09-28 at 12.23.40 AM.png`
  - `bd7552b38a0148d1a644a1e2b0e3fb711948fb9783c6a08fb2b0f081f4a1adb5`

4/4移动前后SHA256一致；未改原图。
