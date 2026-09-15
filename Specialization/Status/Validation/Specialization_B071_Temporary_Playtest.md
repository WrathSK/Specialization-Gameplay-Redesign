# B071.98 temporary develop playtest

Document Owner: Codex
State: USER_GAME_TEST_REQUIRED — 用户游戏验证尚未进行
Authorization: 用户明确要求临时develop测试并保留当前版本；已确认游戏完全退出。
Gameplay source checkpoint: a9302a591ee33c14d9e4fbfd48c8ce1dff6b2ca6
Stable: main e3651f9 / B069.96 / modinfo96
Stable package SHA256: 7f75a44e4bfaad461570600219f9b4d6b7f5388aefaeb4a2114c3f9ab15159df
Develop package SHA256: 87ed79bded5c4786050dbd26297d3e5fd8f142418c33e705195996278b3e131b

切换是否完成以外部SpecializationDeploymentBackups/B071.98-20260914-playtest.json的phase与运行包hash为准。本页记录授权/测试，不提前宣称DEPLOYED或实机PASS。工具改动不修改上述Mod字节；本轮不启动游戏。

## 最小测试

1. 用户启动游戏，确认诊断标题P0-B-071.98。可用已有43T存档但另存测试slot，或新开测试局；不要覆盖正常长期存档。新局需要已有网络后再判断Network cache行为。
2. 有至少一条网络连接时读取Counters并截图，记录当前回合与活动监视器内存。
3. 不移动、不结束回合，静置约1分钟，再读取一次Counters并记录内存。derive_executed在完整输入未变时不增加；derived_cache_hit可增加。fact/city scans仍可能增长，不是Batch B失败。
4. 正常短玩一小段后再记录Counters/内存；新输入变化允许一次新派生。若仍明显持续增长/卡顿，停止本次测试，不要求撑完一局或等到几十GB。

若便于单变量检验，读取数次工业网络折扣再看Counters：已缓存同输入的完整derive应为0增量。无需刻意新增/删除路线或反复改总督。

本测试包含A+B，不能把与B069的全部差异仅归因B，也不能把derive减少等同于55GB泄漏解决。内存趋势独立验收。保存截图仍用原ScreenShots收件箱；用户说明回合、内存、是否静置/正常操作即可。

## 恢复

测试结束用户完全退出游戏后，使用W0002恢复入口和外部receipt，整包恢复至上述stable hash。保留stable原始备份及出去的develop包，main不变。实际恢复未执行前不宣称已恢复；用户当前授权只执行测试切换，不提前撤销测试包。
