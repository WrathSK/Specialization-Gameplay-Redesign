# B156.183 — 按需 Modifier 只读诊断

Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；USER_GAME_TEST_REQUIRED。
Scope: 用户授权的最小诊断，非Meaning收益修复／新primitive／正式cutover。W0004 L1＋直接UI请求/缓存边界；Design D0042、Gameplay writer、SQL收益定义、永久数据与GC均未改。

## 实际修改与边界

- `Mod/UI/BoostGreatWorkRead.lua`复用现有UI文件与Meaning精确owned目录，新增Modifiers/ClearModifierRead。读取HD古罗马剧场Writing文化／旅游业、Meaning Writing三yield和旧Dialogue/GWA Writing Culture精确附件；不对全库按前缀找效果，不撤销任何效果。
- `Mod/UI/P0Panel.lua`仅右键“意义延展验证”的现有READ回复进入诊断。OFF／配置错误仍能读取；左键四态实验保持原路径。Show/Copy同token仅复用一份字符串，Copy只导出本诊断；新请求、关闭、shutdown释放。换城/回合/reference变化在下一次读取或展示时判过期，不另加事件订阅；没有常驻或每帧扫描。
- `Mod/Text/TestText.sql`只更新已有中英文`LOC_SPC_CULTURE_MEANING_PROBE_HINT`，没有新本地化key；Probe/modinfo仅build更新。
- 全局GetModifiers每个显式token最多一次；32768枚举项、64匹配、每项64 subjects后处理限制，最多12详细实例、raw字段240 UTF-8安全字节。不能据此声称限制引擎全局列表初始分配。报告只缓存字符串/标量，不保留原生句柄／全局表。
- 本玩家实例不等于所选城实例；首版始终标实例城市归属UNKNOWN，不按城市名或猜测ID映射。Active=true不证明requirement、recipient或实际结算。nil/空/未知/错误/超限分别报告，不冒充0或PASS。剧场内作品实际文化与定义基础文化单列；建筑本体Culture不混入。

## 本地验证

- `DevelopmentTests/test_modifier_read.py`：18项PASS（独立实际Lua/SQL fixture，0.087s），覆盖OFF、配置错误、同token/新token、实际Panel dispatch/Copy、引用/owner/回合变化、读取中变更、foreign/未知owner、Active非boolean、Subjects nil/空/异常、缺API/Definition/Arguments/附件、稀疏/重复/超限、UTF-8名字与输出限长、语法/导入。
- 原`test_culture_meaning_probe.py`中11项直接相关原生读数模拟回归PASS（3.211s）：四态配对、延迟读数、整城辅助不可用、主题已知/未知、数量变化、非有限yield、有界分建筑报告与基线失效。外部DebugGameplay只读复制到内存fixture，未改外部DB或旧断言。
- 这29项仅LOCAL，不证明GameEffects在真实Civ VI本UI context可用，也不证明文化flat可以共存。无玩法全回归／stress／游戏启动。
- XML全部打包引用、Text SQL、41个相关本地链接/锚点与diff检查通过；W0001当前manifest/selector/hash PASS（182 runtime / 402 guarded context），不因此推导玩法授权或native PASS。
- 本地发现Lua locale `%c`会破坏中文UTF-8字节，诊断新sanitize采用明确ASCII控制范围；原有其它路径不扩展修改。

## 用户只需一次读取

1. 载入此前测试存档，选中那座有古罗马剧场和著作的我方文化城。
2. 打开P0面板，**右键“意义延展验证”一次**。无需先左键启动、切换配置或过回合。
3. 截图以“Modifier诊断”开头的报告；若较长可滚动补下半部分。到此停止。

“复制/导出报告”可将本次结果写入Lua.log，不再次枚举；不是必须操作。即使报告显示UNKNOWN／接口未完整也提交这份报告，不重复旧四态测试。第一步仅采集原生schema、owner描述和当前实例；关闭原型时未出现Meaning实例并非FAIL。严格同城映射未确认前不作共存结论。

## 保留门禁

[B155原生FAIL](Specialization_B155_P0L2B_Scale100_Native_Stopped.md)和[来源调查](../../../Reports/Technical/Specialization_B155_Meaning_Culture_Path.md)保持。两个Culture候选未因此修复；市政/外交暂排仍条件后备，未正式采用。精准recipient、Dialogue/theming隔离、最终结算/冷加载/退出及完整L2仍待证；不自动继续下一能力。

## 部署

本地完成，部署状态以Status/Authority的既有receipt登记为准；本记录不从源码存在推断已部署。
