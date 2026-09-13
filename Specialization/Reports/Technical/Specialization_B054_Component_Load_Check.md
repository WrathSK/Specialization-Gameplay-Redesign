# B054 商路已接入但无折扣：组件加载检查

Document Owner: Codex
Evidence: STATIC_CONFIRMED; native retest USER_GAME_TEST_REQUIRED

用户描述：工业IV城市A拥有纪念碑/粮仓/磨坊模板，A→商业III城市B，Read network确认B接收工业网络，没有折扣；无截图。

只读本机证据（2026-09-13）：
- Startup.log此次InitialInit为00:15:55。
- 磁盘modinfo70修改时间00:18:26，包含SPC_B054_Discounts与SPC_B054_Eligibility；唯一UUID副本位于正确运行目录，备份位于Mods之外。
- Modding.log最近00:50加载仍注册SPC_B053_Purchase及旧组件，完全未列B054两组件或其SQL/后台XML；附近UserInterface组件错误属于其它Mod的UI组件，不冒认为本Mod错误。
- DebugGameplay.sqlite更新时间00:50:39，sqlite_master无SPC_B054_Targets，Buildings中BUILDING_SPC_B054_%数量0。
- 源码与运行副本哈希均为c2c641b65451ed930aad8aa4e5a09d6734f0063bf4b1872e6f84ed3288d62085。

结论：当前进程早于新组件清单，最近读档没有加载B054所需数据库/后台Context；可以看到既有工业网络，但无法据此确认自动折扣逻辑已运行。最符合证据的是进程沿用旧组件清单，需要完全退出应用重启，返回主菜单读档不足。不删除缓存，不改配置，不改机制或运行版本。

最小下一步：用户完全退出Civilization VI并重启，读原存档，仍用A→B原商路。先Read discounts确认不再DISCOUNT_DATABASE_MISSING/未初始化，再核对B中尚未建成、已匹配模板组建筑的购买价格；不重新要求建立网络或新建局。若仍失败，只需B的Read discounts报告。
