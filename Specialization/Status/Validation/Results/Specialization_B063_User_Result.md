# B063 自由城市转换观察结果

Document Owner: Codex
Evidence: 2026-09-13 用户两图及明确口述Cheat Panel转自由城市；回合24。

| 字段 | Record 1.32.55 PM | Read 1.33.13 PM |
|---|---|---|
| Owner/CityID | 0/393221 | 62/65536 |
| 位置 | 65,31 | 65,31 |
| 当前玩家启用 | true | false |
| TOKEN | DEV-B013-P0-6 | nil |
| FLOW / JOURNAL / INVEST / TEMPLATES | 全部存在 | 全部不存在 |
| 原始专业 | INDUSTRY | nil |
| 投资笔数 | 3 | 0（记录缺失的默认计数，不是实际退款或已迁移） |
| 模板数 | 6 | 0（同上） |
| 区域 | City Center / Industrial Zone 均完成 | 两者仍完成 |

USER_GAME_TEST_PASS：B063只读报告在Cheat转自由城市后正确定位原地城市并返回五项Property缺失；不等于正式专业继承通过。本场景不能依赖新City对象自动携带旧Property。没有普通军事征服、外交转交或取回/重载证据，不扩大结论。

STATIC_CONFIRMED（源码证据，非其它场景实机）：本机Cheat1528155583的Base/UI/Script/Cheat_Menu_Panel_Script.lua MakeFreeCity调用CityManager.TransferCityToFreeCities(pCity)，不是该函数中手工删除重建城市。B063观察模块没有SetProperty。内部引擎是否重建对象/清除Property尚不能从Lua与截图断定。

技术后续：必须研究独立于被替换City对象的持久账本，以及可验证的转移事件映射、Owner/CityID重新绑定。仅把旧Owner字段改为新Owner不足以恢复已丢失的数据。坐标可用于核验，不应作为永不失效的唯一身份，避免毁城重建串账；读档恢复不能依赖本次Record内存。此次不凭快照手动恢复，不改Design/Mod。

原图已按原文件名移动至外部旧工作区Specialization/Status/Validation/Evidence/B063-Free-City-Property-Loss；SHA256/大小见manifest.json，原件冻结，Git不纳入PNG。用户当前无需补测试。
