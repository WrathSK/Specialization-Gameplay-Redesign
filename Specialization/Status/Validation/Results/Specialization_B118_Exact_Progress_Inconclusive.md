# B118 — 精确扣除截图与诊断时序缺口

2026-09-28，五张原图逐张查看。结论：NATIVE_RESULT_INCONCLUSIVE / DIAGNOSTIC_TIMING_BOUNDARY；不把缓存7→7当最终扣除失败，也不因未显示非零值宣布归零PASS。

1. 00:05:42：B118.145，队列1，溢出承接实验进度7；城市+8.3，预计119180回合。
2. 00:05:51：准备进度7，尚未执行。
3. 00:05:57：CALLED_NOT_PROVEN，调用一次后即时快照7→7，其它0项变化；显示停止。
4. 00:06:25：旧即时报告仍7→7；右键末行队列1、未读到新增非零目标进度；城市仍实验项目，预计119181回合。
5. 00:06:50：旧即时报告不变；末行同上，城市改为磨坊，预计8回合。

源码复核：Pulse缓存即时结果，Read复用缓存文本，再仅列出非零且相对before变化的目标。所以实验项目后来为0、或仍等于旧7，都可能被省略；后续报告不明确刷新当前目标名称和当前进度。工期增加支持状态后续更新的可能性，不能反推精确扣除或隐藏池归零。没有清晰的后续正常生产回合对照，不升级无负债/全清PASS。按钮hover仍残留B117说明（截图可见−1000），与B118实际执行−p不一致，属于显示缺陷；本轮仅记录，未修代码。

用户提出高成本无收益dummy项目承接全部生产，在计时结束时强制完成并发奖；作为方案讨论保存，尚未授权该新实现。B118项目已经是高成本无收益载体；剩下的是原生强制完成余量、完整回合时序、防提前完成及奖励一次性门禁。暂不要求用户重复当前含歧义诊断。

## 外部原图

- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B118_Exact_Progress_20260928/Screenshot 2026-09-28 at 12.05.42 AM.png`
  - SHA256 `2f9c0941e2130826b80b958e387fe2d5b0c53a3fe8b390de3952fc7325770c0b`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B118_Exact_Progress_20260928/Screenshot 2026-09-28 at 12.05.51 AM.png`
  - SHA256 `0a1ab94ae9388d63b0ce60be173afdfbd71b28f2ed213566cd84e86a64441930`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B118_Exact_Progress_20260928/Screenshot 2026-09-28 at 12.05.57 AM.png`
  - SHA256 `bf13d3b54083e87762c9c78fdde887a895c4b20b403d3e0449ce156d378b2ca5`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B118_Exact_Progress_20260928/Screenshot 2026-09-28 at 12.06.25 AM.png`
  - SHA256 `de6c3712038aa48124f4ba09bfce004c3dec46e4a02c4ae0fb82029069b90d3a`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B118_Exact_Progress_20260928/Screenshot 2026-09-28 at 12.06.50 AM.png`
  - SHA256 `14b6c0ef2adcad9794f8dab4e39c83ebe5bb3d389b55e6feecd841c268a0244e`

5/5移动前后SHA256一致，原件未编辑。
