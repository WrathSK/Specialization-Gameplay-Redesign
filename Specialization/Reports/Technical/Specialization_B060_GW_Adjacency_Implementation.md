# B060.84 原生巨作基础相邻

Document Owner: Codex

D0023已按用户明确确认接受：GW002七类作品含Artifact不含Relic/Product；全部已完成专业区域含Theater/特色替代，按原yield各50%BASE。B060.84实现自动逐作品基础相邻能力，后台复用Dialogue事件样本，新增六yield区域向量，Gameplay重验端点/类别/完成/全集。与时代对话独立开关，原生GreatWork YieldChange载体，非城市补贴。

STATIC_CONFIRMED：每个piece七类六yield定义、±0.5及二进制目录；RequiresPopulation分类覆盖已确认本机专业区域。LOCAL_SIMULATION_PASS：真实Lua/内存SQL、完工/特色/非专业排除、BASE独立于Actual、作品数不平方、负/半点配置无丢精、重复/空作品/ACTIVE降级/OFF/无效端点/过期样本/重载清理及前批回归。配置不是实际收益PASS。

USER_GAME_TEST_REQUIRED：原存档主菜单重载B060.84，GW adjacency Read/Off/Auto。建议当前Culture4城两著作放非主题化槽，先Dialogue OFF隔离上一能力；Adj Off/Auto两图包含偶数/奇数BASE对照；相邻翻倍卡不改BASE/单件配置；总督调离撤销，原生整城更新允许下回合。详细步骤见[本批测试](../../Status/Validation/Specialization_B060_User_Tests.md)。无新局要求，缺数据库/采样报告一图即停。

IMPLEMENTATION_LIMITATION：本批每yield BASE须为整数且绝对合计≤8191，目录上限仅当前技术支持，不是Design cap；超范围/非整数报告错误并清除本项，不静默clamp/floor。原生0.5与普通/时代对话/主题倍率的关系待用户数据，不自行改城市补贴。当前测试优先验证前者，用户已要求停止主题化深挖。


Files: GreatWorkAdjacencyModel.lua收集BASE六yield与精确目录拆分；GreatWorkAdjacency.lua验证当前区域全集/作品类别与ACTIVE，旧片段先移除再挂新；Data/GreatWorkAdjacency.sql生成156隐藏建筑/1092 Modifier，以YieldChange逐作品配置，±0.5到±2048片段。DialogueRefresh在同一事件采样携带AdjData/AdjCount，签名包含adj值，沿用seq/ACK有界恢复；无新定时扫描器。Gameplay注册GWA_READ/OFF/AUTO；六yield原生读取不反向作为计算来源。

保持正式每件值，不先乘作品数；count仅理论合计与无作品清理。原生倍率/theming自然行为仍保留。未知非整数BASE不能表示为本目录半点，当前明确报错，非玩法cap。逻辑支持负基础片段，但负YieldChange原生表现未实测，不扩展PASS。

Tests: DevelopmentTests/test_b060_gw_adjacency.py，继承83既有回归、独立实际Lua/内存SQL；Make_Hash仅内存测试函数，不改外部DB。用户测试结束前不宣称原生半点通过。
