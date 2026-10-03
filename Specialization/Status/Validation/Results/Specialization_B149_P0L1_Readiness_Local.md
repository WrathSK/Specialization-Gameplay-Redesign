# B149.176 — 风雅熏陶就绪修复与本地验证

Date: 2026-10-02
Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED
State: P0_L1_PARTIAL_NATIVE_GATE_REQUIRED；尚非完整L1 PASS。
Contract: [当前修复检查点](../../../Architecture/v2/P0_L1_Aesthetic.md#b149176--readiness-repair-checkpoint)
Source/deployment: [Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state)与实际receipt；源码存在不证明部署。

## 修复与证据

用户确认漏计印刷术，并选择固定巨作、用总督切换风雅熏陶做差值验收。[B148失败证据](Specialization_B148_P0L1_Native_Fail.md)仍保留ACTIVE3/正预期/配置0事实；不会把原馆藏的3倍旅游或用户报告的125→118变化归为本能力新增/撤销。

旧writer仅LoadScreenClose设置ready；隔离fixture略去该通知、发确认样本与本地玩家回合后仍未就绪，可复现预期+12/配置0及误导的“已启用”。这是LOCAL_SIMULATION复现，不是B148实际缺通知的原生因果证明。

新writer沿用原加载事件，并由可靠当前馆藏确认或本地玩家回合补首次就绪。UNKNOWN/foreign/旧引用保护保留；当前资格与master/plot配置分层显示，面板只读。没有SQL/新carrier/公式/普通目录/永久账本/GC变更。

## 本地验证

`DevelopmentTests/test_culture_aesthetic.py`：**17/17 PASS**，复用已有Lupa2.8 / Lua5.5；显式只读DebugGameplay复制到临时数据库，仅在可丢弃副本卸载上批Aesthetic定义后执行原SQL验证，外部数据库不写。旧writer复现取Git `b5ce132`；原catalog对照仍需要Git `caa5ec3`。不将Lua5.5 fixture当作Civ VI实际Lua版本或native生命周期证明。

| 范围 | 结果 |
|---|---|
| 漏加载：只读面板不启动、可靠当前样本启动、重复零写 | LOCAL PASS |
| 首个本地回合兜底、foreign不启动、UNKNOWN不发新收益、后补确认 | LOCAL PASS |
| 同回合总督ACTIVE3→2→3退出/恢复、重复通知幂等、其它城市隔离 | LOCAL PASS |
| UNKNOWN/foreign/过期引用确认不能开启样本就绪入口 | LOCAL PASS |
| 资格/原始标记/master缺失或不健康、同总量错plot分别诊断；面板零写 | LOCAL PASS |
| 原13项公式/逐栋→实际区域投影/ordinary-D分离/ResearchApply、精确旧效果退出、ownership/return/load及失败保护 | LOCAL PASS；旧断言保留 |
| 修改Lua语法、modinfo176/XML与179项精确包文件集 | STATIC PASS |

默认测试改由真实LoadScreenClose进入，不再手动开启Aesthetic ready。ResearchApply夹具人工加图书馆后补共享cache失效通知；保留全部原收益/HOLD断言，未改该运行模块。原26项K结果按[B148本地记录](Specialization_B148_P0L1_Local.md)范围继承，本轮未重跑；没有full/stress、内存长测或游戏启动。

## 一个最小原生验收流程

沿用当前文化城和存档，固定所有巨作、建筑与政策；优先Culture Potential≥3、ACTIVE3，用没有自身旅游加成的总督作切换，避免其它旅游倍率混入比较。无需移动作品或重新制造两城。

1. 总督就位后看“风雅熏陶”：X/合格栋数不变，预期为正，配置应等于预期，显示“配置已进入”。同时记录同城旅游或可辨认的原生旅游来源。若等待启动，可进入下一本地玩家回合让既有兜底执行；面板点击本身不会启动效果。
2. 调离总督使ACTIVE<3：本项配置应归0，固定馆藏/建筑对应的旅游应下降；重新派驻并等建立、ACTIVE≥3后恢复同样配置与旅游。你原来的2栋/1时代是基础+2，2时代是基础+4；这是未叠其它旅游倍率前的贡献，不承诺全国读数必然精确同幅。没有其它变化时差值可以判断本项是否生效。
3. 保存、完全退出并冷加载：确认同城当前资格、配置和旅游恢复。若配置仍0、失配或正配置下无原生差值，停止，仅投递诊断及对应旅游画面；无需继续旧长测。

该一次流程验证就绪、资格退出/恢复和冷加载；巨作移动、掠夺及其它场景保留相应本地证据，不把本次固定馆藏通过扩展为全组合原生PASS。全国旅游混入其它来源变化时，只记录观测限制，不据合计猜增量。

## 当前边界

本地修复通过，原生旅游primitive/城市限定/plot读取及真实撤销仍待用户测试。无新Design决定；K1仍为初版平衡值。只交付L1修复，不进入L2/L3/M/N/U2或重开性能专项。
