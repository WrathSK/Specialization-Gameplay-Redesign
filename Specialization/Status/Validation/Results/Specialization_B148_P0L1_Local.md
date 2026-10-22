# B148.175 — P0-L1风雅熏陶本地验证与原生门禁

Date: 2026-10-02
Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED
State: P0_L1_PARTIAL_NATIVE_GATE_REQUIRED；不是完整L1 PASS。
Source/deployment: [Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state)及对应receipt；源码存在不证明部署。
Contract: [L1实际检查点](../../../Architecture/v2/P0_L1_Aesthetic.md#b148175--implementation-checkpoint)。

## 本地范围与结果

`DevelopmentTests/test_culture_aesthetic.py`真实Lua55模块＋两城native stub，外部DebugGameplay只读复制至内存、执行新SQL。Make_Hash为fixture模拟，不是引擎哈希证明；特定旧catalog对照需要Git `caa5ec3`。

| 覆盖 | 结果 |
|---|---|
| ACTIVE1–4 / X0、1、2、4、8；K1逐栋公式与两城不同X | PASS；配置总量=合格栋数×X，不读取D/人口/专家/国内union |
| 市中心/城墙、剧院/商业/社区、同城两社区实际位置，普通身份与Tier0/未审D分离 | PASS；属于同一actual district的逐栋贡献汇总，不把技术投影当原生逐栋读数 |
| Palace/内部载体/未完成/掠夺排除、移除/修复、旧catalog深度定义及各领域D值/cap一致 | PASS；新增ordinary未增加旧深度值，未知Mod对象保持保守排除 |
| 当前ResearchApply兼容新ordinary；真正缺Tier的原深度对象仍HOLD | PASS；既有Gold coefficient与重复零写正确，非深度对象不误停科研 |
| 同回合时代变化/重复零写/确认通知；轻量Summary无整份作品与时代副本 | PASS；真实K接收路径只通知变化城市，例程一次共享建筑快照 |
| UNKNOWN同引用HOLD、陌生引用/冷加载未确认撤销、恢复/ACTIVE重新计算 | PASS；没有新永久账本写入，local load fixture不是原生存档实测 |
| confirmed loss/重复退出/return当前资格/两城隔离 | PASS；只撤销本模块效果与精确旧Culture对象，不删除永久身份或ordinary |
| 精确旧Culture8+8退休（含低ACTIVE）、旧Commerce connected-kind保持 | PASS；SQL不再附加旧人口/worker%效果；B1/B2定义未改 |
| 撤销失败/创建失败、编码超界、移除区域与错误条目清理 | PASS；失败不施混合新效果、不截断数值、不无界保留无当前城错误 |
| modinfo175/Lua语法/XML/精确文件列表/按需按钮与无禁用高频路径 | STATIC PASS；不证明原生字体/控件或Tourism primitive |

合计13项本批定向测试PASS；26项`test_p0_k.py`事实/采集/桥/旧Dialogue-GWA隔离回归PASS。没有运行历史full/stress、进程内存长测或启动游戏；当前GC策略未改。

本地SQL确认原生DynamicModifier/Effect、固定Amount、city district collection和Property requirement的定义与精确映射。**未确认该requirement对District subject的Plot读取、原生城市/区域限定、旅游增量及撤销**；载体存在、bit配置匹配和本地模拟不能代替这些证据。

## 一个最小原生验收流程

复用馆藏存档。一座Culture ACTIVE≥3城拥有两种合格历史时代、至少市中心和剧院两类普通建筑；另一城用于作品移动。尽可能使用ACTIVE3，避免把尚保留的旧Lv4路径混入对照。

1. 选中文化城，P0面板左键“风雅熏陶”，右键查看时代/逐栋组成；记录X、栋数、预期和配置。核对原生旅游业绩视图/明细在相应区域的实际增量，城墙等原有旅游和其它倍率另看，不凭合计猜来源。
2. **首项若预期为正但原生没有相应变化，或出现串城/错误归属，就停止。** 只回传当前诊断和原生视图；不用继续整套测试。这会判定当前原生技术路径未通过，不能以配置一致作为PASS。
3. 首项可见后，将最后一种时代作品移到另一城：原城X应下降1，每栋贡献随之下降；两城按各自资格/馆藏计算。调离总督使原城ACTIVE<3，检查本项退出，重新具备资格后正常恢复。
4. 保存、完全退出并冷加载；重新查看同城诊断与原生旅游，确认按当前事实恢复。无需重跑K10图、随机掠夺或旧长测。

这是一次流程；相同流程同时核对旧人口/worker%不再出现，普通基础能力保持。若原生明细不足以区分来源，报告该具体观测限制，不把待验写成PASS或默认要求另一轮长测。测试由用户执行，Codex不启动游戏。

## 当前结论与停止点

本地实现和配置检查通过；L1仍partial，原生门禁待验。无新Gameplay决策；不改K1成熟度、D公式或能力范围。下一动作仅为本批最小用户验收，不自动开始L2/M/N/U2。
