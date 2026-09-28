# B117 — 空队列负数调用形成负生产进度

2026-09-27；B117.144 / modinfo144。四张原图均已实际查看。本次清零候选 **USER_GAME_TEST_FAIL / NATIVE_NEGATIVE_STORAGE_BOUNDARY**；不是所有存储清除路径均不可行的证明。

## 原生观察

| 图 | 实际可见事实 |
|---|---|
| 1，22:09:30 | 城131073，回合22，自然空队列；准备尚未执行，扫描3134类目标；城市生产力+8.3，自动溢出A |
| 2，22:09:35 | 同回合，CALLED_NOT_PROVEN，单次−1000；即时可读目标进度未变化，仍空队列 |
| 3，22:09:49 | 选择磨坊后队列1，磨坊进度−992；城市界面剩余126回合 |
| 4，22:10:22 | 回合23，磨坊−984；原生生产面板−984/60，剩余125回合 |

负数随后作用到新目标，且跨回合保留并由正常生产逐步填补。因此本环境空队列AddProgress(-1000)没有自动截断到零。“当前目标进度即时未变化”只描述选择目标前的时点，不能证明没有延后损害。8−1000=−992与此前存储8的观察相容，但不是精确存储接口、内部存储布局或任意小数舍入规则的证明。

## 门禁与停止

- 进入时可靠清零：FAIL；不留负债：FAIL。
- 普通目标已有非零progress保护：未完整覆盖，不能依据即时快照升级PASS。
- chop/harvest及其它注入隔离：未测；第一门禁失败，不继续该候选后续测试。
- 原77项LOCAL_SIMULATION_PASS及STATIC证据仅证明调用、保护和报告路径；不能替代原生语义。
- 停止重复负数、加大扣除或猜测加回1000。回到实验前存档；只回滚Mod不能修复已保存负进度。

用户接受的“进入放弃全部未分配存储、占用期生产不得转移”合同不变。下一步仅调查可验证的直接重置、可靠读取实际存储后精确扣除，或独立承接/清理路径；这些都未证实，不自动实施。当前测试按钮仍存在于B117运行包，本次没有禁用或部署修改；不要继续点击该实验按钮。Claim/F未推进。

## 原图与SHA256

- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B117_Negative_Production_20260927/Screenshot 2026-09-27 at 10.09.30 PM.png`
  - `4e5f0a843e91b12835946e3e28d792f5ed8b5eaa43eed67f83ab84c5077d2b17`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B117_Negative_Production_20260927/Screenshot 2026-09-27 at 10.09.35 PM.png`
  - `11d37435b59296d777e8dba508cb0750d53e39c0c69344666759a79b509f9b7c`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B117_Negative_Production_20260927/Screenshot 2026-09-27 at 10.09.49 PM.png`
  - `61219ee2f770f17019c04935d983a7baa6648616a378dd6c5d6453d3d7d178e7`
- `/Users/xutingzheng/Library/Application Support/Sid Meier's Civilization VI/Specialization/Status/Validation/Evidence/B117_Negative_Production_20260927/Screenshot 2026-09-27 at 10.10.22 PM.png`
  - `fe36d3a5fb4be4d30543798db03fd8ef3bd1a25093788ad0b52ac826cd3174fb`

4/4原图移动归档，移动前后SHA256一致；收件箱无重复副本。
