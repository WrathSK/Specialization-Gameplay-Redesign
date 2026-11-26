# Specialization P0 Status

Document Owner: Codex
Status Revision: S1145
Implementation Build: develop B540.567 / modinfo567. Installed temporary B539.566 / modinfo566. Stable B528.555 / modinfo555.
Architecture Revision Reviewed: A0192
Design Revision Reviewed: D0067
Latest Accepted Design Revision: D0067
Design Sync State: D0067_MANAGEMENT_CAPACITY_DESIGN_ONLY
Work State: MANAGEMENT_CAPACITY_LAYOUT_PREVIEW

## CURRENT AUTHORITATIVE STATE

| Area | Current state |
|---|---|
| Source and installation | Develop B540.567 / modinfo567 [改用主界面层](#management-capacity-preview-screen-layer--s1145)。本机仍为 B539.566 临时包，main 稳定包是 B528.555。 |
| Recovery | 本次临时安装回执绑定了已核对的 B528.555 原包。更早的 B489、B527 回退凭据见[稳定版部署记录](#b528555-stable-playtest-package-deployed--s1123)。 |
| Validation | B539 实机确认下排按钮可打开预览、顶栏随试调变化。B540 主界面层通过本地模拟，实机层级与输入待复验。考察团归档仍沿用[先前的证据边界](#expedition-archive-city-choice--s1138)。 |
| Next action | B540 临时安装核验后，查看居中主窗口、地图暗幕、关闭与重开。布局使用固定示例到位点数。 |

Use [Authority](../Workflow/Authority.json) for the active task and version pointers and the [resumption guide](../Workflow/README.md#action-scoped-reading-and-interruption-recovery) when picking up after a pause.

2026-11-05 Owner明确授权按现行统一计划持续推进，普通片段完成后不再逐片请求授权；遇到规定的外部审计检查点、新的玩法／核心职责／保存或不可逆操作取舍、无法安全解决的问题或现有明确门禁时停止并报告。每片保留定域调查、Runtime Impact Contract、本地验证、独立commit/push develop和当前状态记录。此授权不自动部署、不晋升main、不启动游戏，也不把本地结果当实机通过。

## Recent checkpoints

### Management capacity preview screen layer — S1145

B539 实机确认开启面板和顶栏试调更新。用户以总督和世界气候页说明目标层级。B540 将预览挂至原生 Screens 父节点，使用与总督页相同的弹窗队列参数及原生暗幕，内容居中并支持 Esc 和关闭按钮。试调使用独立示例数据，真实回合推进属后续容量实施。四项专项 Lua 5.1 检查通过，含挂载、队列、暗幕、关闭重开、示例数据与包引用。原生层级待复验。

### Management capacity click preview installed — S1144

B539.566 / modinfo566 temporary, 301/301 MATCH at 2d03822eee842e8f5051ecc91e6d98b640c8661430f3be6389345c4629fd068b. Receipt B539.566-9de3f36-playtest.json DEVELOP_ACTIVE. B528.555 backup verified. 安装来源 9de3f36cc3b24b57fdd264b218a3aca32ec9e72a。游戏内点击待复验。
### Management capacity preview panel opening — S1143

B538 实机显示两处入口，点击下排按钮时没有面板。原回调只显示子窗口，挂载时也没有显式显示其原 UI 上下文。B539 挂载和打开时均显式显示该上下文，关闭通过子窗口完成。Lua 5.1 夹具以隐藏父界面复现，覆盖点击及重复开启。实机显示待复验。
### Management capacity preview installed — S1142

开发包 B538.565 / modinfo565 已临时安装。安装包 301 个文件与源码 `b33e7284bb68dfe756e723ae81b2ce4acb446e8b` 一致，SHA256 `46faf4af6eb94d54381266e79316db7e1a9fdc15be27d245cf0471e5239da952`。回执 `B538.565-b33e728-playtest.json` 记录了本次换包、12 个先前已退役的开发版路径及可还原的 B528.555 原包（310 个文件，SHA256 `1722ed6e5e93b4d320345248cb29778c1a108e3fc51b515ad2eff3aef0cb3095`）。事务标记已清除。游戏内显示由负责人接下来核对。

### Management capacity layout preview — S1141

顶端商路名额旁显示示例用量 6/10。下排使用原版启动栏按钮打开专业管理侧栏，四座示例城市允许试调、撤销和确认。徽记暂用原版市政广场图案。调配只存在于界面内存，重载后回到示例。真实容量授点、城市数据、回合和保存均未接入。玩法继续采用当前总督门槛。[设计规则](../Design/Shared.md#开拓者投资与专业管理容量)

运行影响限于受支持玩家的界面。读档界面完成时挂载两个控件，同一界面的重复加载通知不会增加控件，卸载时归还顶栏与启动栏空间。四行固定示例与按钮响应没有城市扫描或持续轮询。

本地验证（`LOCAL_SIMULATION_PASS`）使用 Python 3.14 和 Lupa 2.8 的 Lua 5.1。运行 `python3.14 -B -m unittest discover -s DevelopmentTests -p test_management_capacity_preview.py`，4 项通过，覆盖控件位置、重复挂载、卸载、测试文明范围、试调与双语装配。按现行固定 HD 数据库输入运行 `python3.14 -B DevelopmentTests/run_refactor.py --stage CurrentGameplay`，42 项通过。174 份 Lua 编译、25 份 XML 解析及 301 文件包的清单引用检查通过。实机排版待负责人查看。

完整本地回归记录 `local/refactor/CurrentGameplay-939a9ae40dcd440d97bad570618cf2cf/closure.json`，SHA256 `89e664d42e4b9c1e08f4434730684bf714c01f15b7a75de4586c0b1ab6251701`。已测源码快照 `98671372481c0a1372c20b7ec0c49d77692fba03041c29ab26467314eb9a54f4`。

### Expedition archive city choice — S1138

归档城确认易主后，原主人选中存续的人文考察团，可从行动栏选择新的己方文化城。目的地可以没有总督。旧见闻留在原城，未完成任务结束，下一次任务按新城自己的见闻名额判断。没有合格城市时，保留原团与全国名额。[玩家规则](../Design/Culture.md#来源易主与重新挂靠) · [城市和单位各自的责任](../Architecture/Specialization_v0.1_Architecture.md#已成团的考察团更换归档城)

**运行影响。** 复用已有的交割退出回调和单位存储。确认同一归档城时写一次单位记录。只在玩家打开选择器时遍历本方城市，确认时重读选中的城市与单位。单城读数不可用时提示列表可能不完整。保留现有到达与活动释放协议，旧请求不能代另一支团或替已经易主的城市确认。没有新增引擎监听、轮询、保存字段或玩家付款。

**本地验证。** Python 3.14、Lupa 2.8。运行 `python3.14 -B DevelopmentTests/run_refactor.py --stage CurrentGameplay`，42 项通过。定域套件 183 项通过，与前者有重叠。新加的 9 项以 Lua 5.1 测试真实城市存储交割、同构建冷读、原团身份、无总督与低潜力、未决城市、失效的选择、任务取消与名额、已派遣单位到达及行动栏。原行动栏夹具补载随界面使用的重组助手，任务图标断言对齐已发布的素材，两种 Lua 测试环境各自加载隔离的作品读取器。173 份 Lua 在 5.1 编译通过，24 份 XML 解析通过，298 个包文件的清单引用可解析，新增 7 个文本键均有简体中文与英文。

定域复现时在 `DevelopmentTests` 下运行 `python3.14 -B -m unittest test_expedition_archive test_expedition_spy_actions_ui test_expedition_spy_sidebar_ui test_expedition_training_source_loss test_expedition_missions.Missions test_expedition_spy_binding test_expedition_spy_store test_expedition_spy_recovery_activity test_expedition_spy_auto_open test_expedition_spy_selection_ui test_b414_crew_unit_panel`。外部数据库及依赖配置见[测试环境](../../DevelopmentTests/README.md#environment-and-dependencies)。

本地完整运行记录位于 `local/refactor/CurrentGameplay-3c4aff7191f84a139c6e477df0c5517a/closure.json`，SHA256 `87ceb9af3f9ea1719c35b163ad54fc77b5cede8b51e0d5fbbeb0df7f8763848a`。输入文件摘要为 `160f7438b90a2fbc60e51daf540a3d724d5adb10a14ee8e3fd76aa745bf45fbe`。

**实机范围。** 本地通过（`LOCAL_SIMULATION_PASS`）。归档城交割的原生事件顺序与原版／HD 界面仍待实机。永久毁城的独立证据入口和边境位移沿用现有待办。安装仍为稳定 B528.555。

### B528.555 stable playtest package deployed — S1123

On 2026-11-18 the Owner approved the bilingual README and the promotion of B528.555, then separately authorized stable installation. [PR #9](https://github.com/WrathSK/Specialization-Gameplay-Redesign/pull/9) merged at `0beca3138b58595bfa02749e4f5ba3662736b9e9`. Its parents are prior main `8a6aaa29` and approved head `e82f20bb`. Its tree matches the reviewed head and its Mod files match B528 source `e42caca0`.

**STATIC_CONFIRMED deployment.** With the game closed, the B527 receipt `B527.554-1495cbd-playtest.json` reached `STABLE_RESTORED` before local main advanced. The stable tool then deployed the 310-file B528 package with the 29 reviewed outgoing paths. All installed files match main at SHA256 `1722ed6e5e93b4d320345248cb29778c1a108e3fc51b515ad2eff3aef0cb3095`. Receipt `.SpecializationP0-backup-f1x7zfau.receipt.json` reached `DEPLOYED`. The retained B489 rollback package matches its original 337 files at `fe601208d9fcdc359c3f8b46a017f5caa19b1284f952c9f7b60e986899b6de30`, and the outgoing B527 matches its 314 files. The final check found no pending transaction.

**Playtest scope.** [B489](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Status/Specialization_P0_Status.md#b489-two-profile-native-acceptance-complete--s1047) covers the recorded HD and official Gathering Storm scenarios. The official game used two testing aids. [B527 HD](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Status/Specialization_P0_Status.md#b527-hd-great-work-and-cold-load-evidence-reviewed--s1091) covers city-local Great Works and cold loading. The positive [B527 no-HD Culture Network observation](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Status/Specialization_P0_Status.md#b527-no-hd-culture-network-and-load-readiness-verified--s1093) used 69 loaded targets. The pinned 28-target B527 cold check, continuation across reload after that positive benefit, and the precise HD Study uplift remain open. The B528 cleanup has 35 recorded local checks and inherits native evidence only in its prior scopes. This release ran no new game test. Supported saves start and reload on the same build.

[历史全文](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/36eceb2bf6d5d619783c02546a053a8c25896f33/Specialization/Status/Specialization_P0_Status.md)
