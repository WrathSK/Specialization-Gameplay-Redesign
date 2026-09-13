# B009：独立的标准化Shadow Route State

> 本批B9-1已USER_GAME_TEST_PASS：3→4、+1/-0，标准缓存rev 1→2。以[最新用户结果](Specialization_P0_B009_User_Result.md)为准；下文待测步骤为历史计划，无需重复。

## CURRENT AUTHORITATIVE STATE

运行P0-B-009 / modinfo16。将已验证UI后台采样的输出复制进独立、纯Lua的标准缓存；不是将UI升级成Gameplay权威源。原DevelopmentTests/TradeRouteState.lua的GAMEPLAY_CURRENT准入不变，正式网络/收益未接入。没有永久属性、城市建筑或存档事实写入。

B007初始化/读档、B008的Cheat Panel删城重建PASS作为此前证据保留；B009新增模块的实机装载与输出仍USER_GAME_TEST_REQUIRED，不能自动继承为全模块PASS。

## 内部结构 / STATIC_CONFIRMED

ShadowRouteState.lua只接收后台采集器已经复制和校验的标量记录，不访问游戏对象。成功读取状态READY_UI_SHADOW，schemaVersion=1，sourceContext=UI，authority=UI_SHADOW_ONLY；包含player、turn、revision、count、orderedKeys、routes、addedCount、removedCount。

Route record：key、traderUnitID、originPlayer/originCityID、destinationPlayer/destinationCityID、originCityKey/destinationCityKey、domestic、current、validity。没有UI名称/路径plot/Great Work等无关字段。

城市key是owner:cityID，仅当前快照身份；identityKind=OWNER_CITY_ID_SNAPSHOT_ONLY，绝不冒充跨征服/重建的永久UID。复合路线key由商人owner/id与端点构成。current=true仅表示来自本次完整UI当前集合并经上游端点与计数校验，不代表另外发现了Gameplay active API。

## 生命周期

- 每次完整采样先标准化成功，再发布完整诊断快照。路线字典整体替换。
- 相同集合（含顺序改变）revision不增加；增删/端点变化时增加。
- dirty/失败立即使Read返回UNKNOWN，无routes，不回退lastGood。
- Read返回独立深复制，调用者不能污染内部缓存。输入也是复制的标量。
- reset/player切换/context关闭清空缓存与比较基线；不序列化，读档从当前集合重建。
- ExposedMembers.SPC_P0_BackgroundRoutes.ReadNormalizedRoutes()为纯读取出口，不采样、不发送Gameplay请求；目前没有正式消费者。
- 面板增加一行“标准缓存：READY_UI_SHADOW；rev=…；count=…”。原始路线快照保留为诊断兼容接口，不作为标准状态消费者的写入口。

NetworkState来源保留结构与多源L未定规则不变；当前未将UI标准缓存接入该原型，也未注入假专业数据。正式采用UI来源的权限、单机/多人同步和永久UID仍需独立设计。

## LOCAL_SIMULATION_PASS

- test_shadow_route_state.py：空集合、全量替换、顺序无关幂等、3→1撤销、同数量端点改变、国内/国际、输入与返回值修改隔离、错误authority/缺行/多行/商人冲突拒绝、UNKNOWN隔离、reset。
- test_background_routes.py：加入真实标准模块，验证后台输出、重复集合revision不变、dirty即时失效、关闭后已持有的reader也只返回UNKNOWN；已有事件批次与读档/撤销模拟仍通过。
- test_specialization_p0.py：Lua/XML/manifest与已有探针、按钮只读回归通过。
- test_trade_route_state.py：原GAMEPLAY_CURRENT严格准入与来源拓扑原型仍通过，未放宽UI来源准入。

未启动游戏，未新增引擎API调用。此次本地测试是mock/纯Lua，不扩大为实机PASS。

## USER_GAME_TEST_REQUIRED：单项B9-1，后台新增一条路线

目标是验证新增标准模块装载与尚未单独确认的后台新增路线刷新，不重复初始化/读档/删除城市案例。

1. 手动加载现有Test存档，确认B009。可使用上次删城后仅剩Aberdeen→Stirling的一路线存档；没有该存档时使用任意现有测试存档，不要求新局。
2. 打开Background routes只看一次基线，记住“当前商路”数量和“标准缓存”rev；无需抄ID或专门截图。如果标准缓存不是READY_UI_SHADOW，请直接截图并停止。
3. 关闭P0，使用现有闲置商人建立一条己方城市之间的商路，尽量选与已有路线不同的方向，如Stirling→Aberdeen。正常选择商路目的地的界面允许使用；不打开贸易总览或点Read routes (UI)。不要同时改城市或旧路线。
4. 建立后重新查看Background routes，回传一张截图。若没有方便可用的闲置商人/容量，请告诉我，先不做，不要求等待旧路线结束或另开新局。

PASS：原有N条变为N+1，原路线仍在，新路线方向正确；标准缓存READY_UI_SHADOW且count同为N+1，rev大于基线；本次变化通常+1/-0。无需过回合，按钮不触发采样。Gameplay PENDING允许单独保留。新建路线可能经过多个引擎阶段，所以不硬性要求revision恰好+1。

FAIL：UNKNOWN持续、标准缓存缺失、两处count不一致、新路线不出现或旧路线丢失。首次UNKNOWN可约1秒后只再查看一次；仍异常则停止并保留截图，包含标准缓存、触发/采样入口和错误。无需Clipboard/Lua.log。

## 文件变更

新增运行ShadowRouteState.lua、DevelopmentTests/test_shadow_route_state.py及本报告。修改UI/BackgroundRoutes.lua、Probe.lua、UI/P0Panel.xml、SpecializationP0.modinfo、DevelopmentTests/test_background_routes.py、Architecture/Status。备份DevelopmentBackups/SpecializationP0-P0-B-008。SQL未改，未改原版或其它Mod。
