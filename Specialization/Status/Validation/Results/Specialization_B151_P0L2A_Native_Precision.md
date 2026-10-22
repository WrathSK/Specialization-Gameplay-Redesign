# B151.178 — L2A原生精度结果与Floor方向

Evidence: USER_GAME_TEST_PASS（所测入口及整数追加） / USER_GAME_TEST_FAIL（所测半点精度）；完整L2、六产出、cold load/失城/native-only尚未通过。
Baseline: develop 482d08a；source/live B151.178 / modinfo178，已记录部署source438ca9d与receipt不变。本轮仅读图、归档、记录用户方向和计划；未改运行源码、未部署。

## 原件与观察

已逐张原分辨率读取10图，按默认文件名移动到develop的`local/legacy-workspace/Specialization/Status/Validation/Evidence/B151_P0L2A_Precision_20261002/`；manifest记录文件名/大小/SHA256/结果关联，10/10移动前后匹配。图片与manifest均Git忽略；不从截图推定未展示的操作。

均为Edinburgh (Test)、P0-B-151.178报告、Culture ACTIVE4；Harbor D0。表中S/G为原生巨作分项（不是整城总率）；Δ仅在同馆藏基线仍有效时记录。

| 图/时间 | 回合/模式 | W | Campus/Commercial D | 理论每件S/G | 原生分项S/G | 可读事实 |
|---|---|---:|---|---|---|---|
| 1 21:36:38 | T60 BASELINE | 1 | 1/1 | 0.5/1.5 | 0/0 | 正常基线入口，配置0/0 |
| 2 21:36:55 | T60 ACTIVE | 1 | 1/1 | 0.5/1.5 | 0/1 | 同馆藏Δ0/+1 |
| 3 21:38:07 | T61 ACTIVE | 1 | 1/1 | 0.5/1.5 | 0/1 | 下一正常回合仍0/1 |
| 4 21:39:02 | T61 ACTIVE | 2 | 1/1 | 0.5/1.5 | 0/2 | 馆藏变化使旧基线失效；不虚构Δ |
| 5 21:39:25 | T61 OFF | — | — | — | 未展示 | 显示已关闭；单图不证明旧writer完整重建 |
| 6 21:39:26 | T61 BASELINE | 2 | 1/1 | 0.5/1.5 | 0/0 | 新基线，前次追加2G已不在分项中 |
| 7 21:39:28 | T61 ACTIVE | 2 | 1/1 | 0.5/1.5 | 0/2 | 同馆藏Δ0/+2 |
| 8 21:40:00 | T62 ACTIVE | 2 | 1/1 | 0.5/1.5 | 0/2 | 下一正常回合仍0/2 |
| 9 21:40:39 | T62 BASELINE | 2 | 3/3 | 1.5/4.5 | 0/0 | D变化正确，重新建立基线 |
| 10 21:40:42 | T62 ACTIVE | 2 | 3/3 | 1.5/4.5 | 2/8 | 同馆藏Δ+2/+8；所测整数部分生效 |

## 结论边界

- 入口修复在所测实际报告与操作流程中可用；基线→启用→关闭→重新准备均有可见结果，旧B150入口失败不再阻塞这次精度观察。
- W1/2、D1/3的所测结果与每件截断一致：0.5→0、1.5→1、4.5→4；W2时0.5×2仍0，不能宣称按整城汇总保留小数。TECHNICAL_LIMITATION限定当前GreatWork flat YieldChange片段路径、Science/Gold和所测配置，不外推所有引擎接口。
- 半点精度FAIL不等于整数primitiveFAIL。复用2G/8G/2S原生追加及D1情况下下一回合保持的证据；D3启用后未见下一回合截图，不扩大其结算持久性范围。
- 整城总率受其它来源/倍率及刷新影响。图3总Gold较旧基线增加13.5977不能全归本项；图8整城Gold差1.5977不能改写为分项应有2G的实际收益倍率。图10同操作整城率尚未刷新；分项证明可见追加，不单独证明所有最终入账/倍率。
- 图5/6支持退出后测试分项归零，不独立证明全部旧GWA回补、UNKNOWN/loss/cold load、未知作品排除、Culture/其它四yield、theming/native-only。原LOCAL检查点及冻结原件不重写。

## 用户方向与下一边界

用户明确：采用Floor，要求下一步计划；**只针对意义延展，不沿用或扩大到GPP/其它能力。** Floor是新确认方向，不是本轮已实现的模型行为。

精确位置待用户确认：推荐每件同yield各领域贡献求和→Floor→乘W。例如Commercial D1+Harbor D1：推荐每件3G，逐领域Floor为2G；Campus D1/W2：推荐0S，整城Floor为1S。这些差异是Gameplay边界，不能由截图或旧科研许可决定。

当前Culture D0029正式Content仍写no Design rounding；本轮不静默改写或造新revision。在口径确认后，按现有Design同步流程记录明确例外并同步受影响阅读正文/引用，才修改模型。K0.5、Gold份额3、Shared D、作品资格保持。

[下一最小切片与停止条件](../../../Architecture/v2/P0_L2_Meaning.md#推荐下一切片--p0-l2b门禁原型)：复用已测S/G，先处理同类未知作品writer排除及追加Culture与旧Dialogue的隔离；不自动正式六yield切换，不进入L3/M/N/U2。不要求重做L1、E2或长测。
