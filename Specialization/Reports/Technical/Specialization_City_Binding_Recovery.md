# 城市标记与总账的绑定恢复准备

Document Owner: Codex
Design Reference: D0002 PROG-004 / OPEN-04
Runtime: B012 / modinfo19（未修改）

## 本轮结论

B012表保存实机证据允许继续研究绑定，但对象引用不能直接冒充永久身份。建议总账预留编号→写城市专用token→双方读回一致后确认。当前只实现离线恢复判定，不写Game/City Property，不锁定专业；缺一侧时拒绝自动补齐，避免把旧城记录绑到复用引用的新城。

## STATIC_CONFIRMED

静态源码证据，不等于游戏API实测：HD Gameplay/HD_StateUtils.lua:56在UI取得GetComponentID，71经Game.GetObjectFromComponentID定位后调用SetObjectState；Gameplay分支63直接SetProperty。官方BlackDeathScenario_StateUtils.lua:70也有对象引用传递先例。它们证明对象定位模式存在，不证明ComponentID跨读档/征服/毁城永久稳定；缓存以对象为key亦不作存档身份依据。

官方Base/Assets/UI/PartialScreens/WorldRankings.lua:1842与Popups/RazeCity.lua:83使用city:GetOriginalOwner，但原始owner不能区分同玩家多座城或同地重建，且UI先例不自动证明Gameplay可调用。初次路径查找有拼写错误，修正实际Assets路径后核对上述文件；未获得GetGameTurnFounded/Acquired的可用Gameplay证据。

HD根为Steam/steamapps/workshop/content/289070/2465378070，官方根为Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets。

## 拟议恢复协议

总账保留uid、当前owner/cityID/位置、RESERVED或CONFIRMED状态；城市自身保存相同opaque token。编号不回收；总账先持久预留，避免城市已写token而分配器尚未推进。跨Property仍非原子事务，部分成功必须显式处理。

| 当前完整读取 | 离线决定 |
|---|---|
| 双方无记录，且确认加载后真实建城、总账已验证 | 仅计划预留编号 |
| 双方无记录，旧城/加载或缺建城证据 | OPEN-04，不从区域补造 |
| 总账有记录，城市无token；或反向 | UNKNOWN，不自动补齐 |
| 双方token相同、owner/当前引用一致，总账RESERVED | 仅计划确认，不重复分配 |
| 双方一致且总账CONFIRMED | BOUND_CANDIDATE，尚不是实际绑定通过 |
| token冲突、引用变化、对象不存在、读取失败 | UNKNOWN，保留数据 |
| token匹配但owner变化 | OPEN-04，不决定征服继承 |

当前CityBindingRecovery只接受MOCK_ONLY，校验当前数字引用后返回上述计划。它不实现allocator、完整账本验证、Property读写或多城token唯一性扫描。registryValidated/freshFoundationObserved均为外部前提；不得在真实adapter无证据时直接填true。坐标是附加冲突检查，不是永久UID。

## LOCAL_SIMULATION_PASS

仅本地模拟：test_city_binding_recovery.py覆盖预留前、总账预留后但城市未写、双方已写未确认、确认后重读、加载、缺一侧、冲突、易主、引用变化及读失败。test_city_identity_registry.py回归通过；均通过既有lupa执行，exit=0。实际崩溃、城市标记随征服/毁城/重建生命周期及双Property重载一致性仍未实机验证。

## 下一步范围

准备只给加载后新建测试城市写DEV token的窄探针，显示总账/城市双方状态，沿用旧存档但不为其中旧城补造专业历史。缺一侧先报告，不自行自动重绑。先完成写入/加载扫描本地模拟与备份，再交用户最小实机案例。本轮不部署新包，无新增实机测试，也不接专业收益。

## 截图归档

用户明确批准读后按批次归档，规则G0004已登记。B012五张移至Status/Validation/Evidence/B012，逐文件hash与原结果报告一致，保持原名，不复制和删除；manifest.json及README指向原结果。历史结果原件保留判读时位置，当前位置由归档索引补充。
