# B020：限定真实新城DEV集成

Document Owner: Codex
Architecture Revision: A0045
Build: P0-B-020 / modinfo27
Verification: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

## 部署内容

新增唯一运行目录FreshBindingHook.lua与CityFlowProbe.lua。前者由已验证NativeFreshHookCandidate逐字适配为DEV_ONLY/global include模块，保留旧回调及本次成功核对；后者为限定DEV处理器，不是把MOCK Gate改名冒充正式引擎适配。

Gameplay在B013/B015 Start之后安装hook并注册额外OnDistrictConstructed监听；既有脚本不改。新城回调已确认B015写入初始化记录后，B020把本次核对的B015候选事实保存在独立City Property SPC_DEV_CITY_FLOW_B020。表内before/target/facts与BEFORE_PENDING→TARGET_PENDING→DONE逐阶段整表保存和读回，初建rev3；首个完成后rev6。各阶段不重试；不确定结果停止本玩家B020实例，B015继续独立执行。没有正式收益、资源消耗、城市UID分配或旧表迁移。

完成通知独立核对对象、owner/type/IsComplete、区域替代族与B015本次first的district/type/turn/revision。若B015还未先处理此通知，不会把专业区域误作NON_V01，而是暂停。后续专业不覆盖首个锁定。原生监听交付顺序由本批实机确认；本地已模拟反序后安全停止。

## 加载与资格边界

active token集合仅本次加载的新城回调加入，加载只读所有测试玩家城市记录，不恢复写资格。持有B020表但不在active集合的城市显示LOAD_READ_ONLY，后续完成不改变B020表。B015行为不变，因此读档后两份DEV记录未来可能不同，不能把它们当双重正式权威。旧城无B020表不补建。

当前固定IsTestPlayer只用于DEV范围，不取代D0007通用资格；B018共享诊断bool未用作正式授权。B013绑定和B015验证路径都是DEV依赖，跨owner永久UID、跨加载历史连续性、未交付通知、崩溃原子性和多人同步均未解决。只读限制是实验边界，不是正式玩法降级或已接受fallback。

## 本地证据与用户测试

八脚本exit0。test_city_flow_probe执行实际B013/B015/hook/B020代码，保留旧journal回归；新城3/学院6、首个锁定、重复/重载只读、丢写隔离、监听反序停止、坏表/owner拒绝，并执行实际UI按钮→请求→Gameplay ACK。全运行Lua编译、XML/manifest引用/UUID检查通过。LOCAL_SIMULATION_PASS仅本地模拟，不等于Civ VI实机。

[用户两案](../../Status/Validation/Cases/B020_City_Flow.md)等待验证，尚无新USER_GAME_TEST_PASS。只需现有局新建一城、学院放置/完成、正常保存重载，共三张关键图。此批新增点是实际回调与三阶段记录集成，不重新验收B019合成表。

## 文件与保护

新增两个运行Lua、test_city_flow_probe.py、本报告/案例；修改Gameplay、Probe版本、P0Panel.lua/xml和modinfo，文档A0045/S0047。UUID、Design、SQL和配置不改，既有Tests未改。备份/测试输出/校验：DevelopmentBackups/Specialization-before-B020。未启动游戏；交付后等待用户结果。
