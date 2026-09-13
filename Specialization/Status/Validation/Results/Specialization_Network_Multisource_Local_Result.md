# Research/Culture多源强度本地结果

Document Owner: Codex
Design Revision: D0001
Architecture Revision: A0003
Verification: LOCAL_SIMULATION_PASS
Runtime Build: P0-B-010 / modinfo17 (UNCHANGED)

LOCAL_SIMULATION_PASS仅表示本地Lua模拟通过，不是Civ VI游戏通过。使用既有`/tmp/city-gpp-test-runtime`中的lupa，无新安装；运行命令前缀`PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/`。

## 已执行（均exit 0）

- test_network_multisource.py：真实Lua NetworkState→NetworkStrength离线集成。多中心不同等级源统一max；跨中心/重复路线去重；独立k、零k、小数；未接入高级源及Potential不影响L；ACTIVE变更无需改路线revision；并列最高源；无分发的已接入高级源；断开回退；免费/路线资格独立撤销；中心角色撤销；空集合重建；重复调用/返回值修改无累积；非法输入UNKNOWN；Industry来源保留且不合并；后台影子身份不升级。
- test_specialization_network.py：单级sqrt、8/16接收城市示例、独立k、递减收益、去重、无效级别；既有SQLite只读复制到内存测试TEXT存储，不写原库，不证明引擎执行表达式。
- test_trade_route_state.py：MOCK完整来源的撤销/恢复/幂等/所有权；角色拓扑及UNKNOWN隔离回归。
- test_shadow_network_state.py：现有ShadowRouteState→MOCK角色拓扑回归；多源来源列表与UI隔离。

## 修改边界

NetworkStrength新增FromState；NetworkState的Research/Culture状态改为NOT_CALCULATED，Industry未决独立保留；两个既有集成测试仅同步该状态断言，新测试覆盖聚合。没有引擎Modifier、量化、正式收益或UI按钮，没有改动运行modinfo或源码。

已接受Spec与Design ChangeLog未改，既有冻结历史/备份/截图未改。当前Architecture和Status更新；旧版本新增原样快照。正式Gameplay当前商路全集、真实角色/永久UID、Boost小数应用仍未通过，不给用户派发实机测试，B010仍延后。
