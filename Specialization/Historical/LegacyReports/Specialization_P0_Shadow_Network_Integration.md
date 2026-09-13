# B009后续：标准Shadow路线到Network来源拓扑的离线衔接

## CURRENT AUTHORITATIVE STATE

运行包仍P0-B-009 / modinfo16，本轮没有修改运行文件，不需要重新加载或换包。新增离线衔接只在DevelopmentTests中执行，不注册modinfo；没有游戏收益或专业状态写入。

路线输入采用B009标准schema；本轮测试数据仍由fixture构造，不伪称读取了真实运行中的游戏缓存。中心/专业来源必须显式标记contextSource=MOCK_ONLY，未实现真实城市角色发现或专业锁定。

## STATIC_CONFIRMED：保持来源边界

NetworkState.lua提取共用派生算法，原Derive入口仍只接受READY，拒绝READY_UI_SHADOW。新增独立DeriveShadow入口只接受schemaVersion=1、READY_UI_SHADOW、UI/UI_SHADOW_ONLY及MOCK_ONLY角色上下文。

输出READY_SHADOW_PROVENANCE_ONLY，保留sourceContext=UI、authority=UI_SHADOW_ONLY、contextSource=MOCK_ONLY与OWNER_CITY_ID_SNAPSHOT_ONLY身份标记。shadow使用originCityKey/destinationCityKey和source.cityKey，未把owner:cityID重命名成永久UID，也未把UI状态伪装成GAMEPLAY_CURRENT。

保存每中心connectedSources/distributionRoutes；每种网络每接收城市的sources/centers/qualifications；各源owner、kind、activeLevel、templateRevision。输出routeRevision和contextRevision，角色变更独立于路线事实。strengthStatus仍DESIGN_DECISION_REQUIRED，不产生合并L、Boost、折扣或生产力。

## LOCAL_SIMULATION_PASS

运行test_shadow_network_state.py，覆盖：
- B009 ShadowRouteState真实模块生成标准记录，送入新离线入口；原入口仍拒绝UI。
- 同一个中心接入Research/Culture/Industry；每条分发路线携带全部三种。
- 同目的城市多路线只计一个N；外贸不计己方recipient。
- 中心接收到网络不递归转发给它的下游。
- 同类型两个不同ACTIVE源、两个中心覆盖同城时保留两源资格，N按城市去重；不计算合并等级或强度。
- 切断一个源，仅移除该源资格；另一Research源和Culture/Industry保留。
- ACTIVE与模板revision改变时更新来源信息，路线revision不变。
- 移除中心身份，无需改变路线事实就撤销其派生接收资格。
- 显式Commerce IV免费自接收资格的增加/撤销（仅fixture，不新增正式机制）。
- 路线UNKNOWN不产生旧拓扑，完整空集得到空接收集合；伪装Gameplay角色来源、外玩家角色输入被拒绝。

既有test_trade_route_state.py通过，原权威契约及NetworkState旧用例未破坏。所有本轮结果是本地模拟，不是新增USER_GAME_TEST_PASS。

## BLOCKED / DESIGN DECISION REQUIRED

正式Gameplay当前全集provider仍未找到；当前UI shadow不得自动升级为正式网络依据。多源Research/Culture合并L、Industry合并和跨征服城市身份规则仍未定。

下一步如继续在影子范围推进，应先提供真实城市角色的只读描述（中心身份、已有专业事实、潜力、ACTIVE门控），而不是长期用fixture或当前区域倒推“首次完成”顺序。现有存档若缺失首次完成历史，必须明确未知，不能猜选专业。该工作本轮仅记录为后续准备，不写入玩家城市。

## USER_GAME_TEST_REQUIRED

本轮没有新游戏代码或接口，不安排实机测试。此前B007/B008/B009已确认的范围保持，不重复。未验证的自然结束/掠夺/战争等仍在待验清单，需有方便、单变量案例时另行给小批次。

## 文件变更

修改DevelopmentTests/NetworkState.lua；新增DevelopmentTests/test_shadow_network_state.py与本报告；更新Architecture/Status。没有运行包/SQL/原版/第三方Mod变更。
