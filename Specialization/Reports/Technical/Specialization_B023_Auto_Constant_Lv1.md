# B023：常数型Lv1自动应用

Document Owner: Codex
Design Basis: D0008 / RES-001、CUL-001、COM-001
Build: P0-B-023 / modinfo30

## 已实现与范围

以B022用户通过的原生内部建筑方式，自动应用三种标准区域的专家支持；不按人数发城市补贴，不按回合累加。ResearchSupport.lua保留basename，内部改为统一三类对账；Research旧建筑ID保留，新增Culture/Commerce载体，零岗位/住房/维护，不修改其它建筑。Industry基础相邻与Crew未接入。

自动在B021完成回调之后，以及加载恢复之后对账；CityBuilt、回合与可用CityTransfered为额外核对入口。判定来自当前有效B021/B015事实与实际完成区域，建筑不是专业事实来源。先移除不匹配载体，再添加唯一匹配载体，已有则不写；无专业/停止/不匹配资格无效果，未跟踪旧城不补历史。已知创建/撤销失败该城本次加载停止自动重试，错误可由只读面板看到；并非已经解决引擎写失败或跨owner永久身份。

移除UI ON/OFF按钮；旧请求名仅返回只读诊断，不能手动覆盖自动模式。Read不触发对账，因此实机可区分“自动生效”与“点击后才生效”。正常重载已存在载体不重复创建；B022中有效却关闭的Research城在B023首次加载会自动添加，这是迁移行为，不要求这次修改次数为0。

当前范围仍为固定测试载体DEV记录与标准Campus/Theater/Commercial Hub；对应替代区域、通用ELIG、征服跨owner继承未宣称已完成，不能把这些限制写成Design例外。暂时只发Lv1；未部署Settler/Potential升级或高级收益。对所有城市检查旧载体用于撤销，深度区域读取仅在有效测试专业记录通过后执行；正式全参与者成本过滤仍需优化。

## 验证

STATIC_CONFIRMED：引用B022原生数据库路径，三种InternalOnly建筑各仅配置专家收益；SQL在缓存只读复制的内存数据库执行，外键差异为零。Make_Hash为测试替身，不证明原生hash。Lua语法、XML/manifest路径、UUID检查通过。

LOCAL_SIMULATION_PASS：test_auto_constant_support.py执行实际B013/B015/B021+B023模块组合，三种完成自动创建（没有UI请求）、重复/读取不写、读档不重复、已知暂停/非测试owner撤销、错误载体清理、创建失败停止重试、缺数据库错误；包含既有B021恢复场景。另test_city_journal_probe.py、test_native_fresh_hook.py通过。旧B022开关测试保留为历史代码，当前不声称通过其原开关契约。

商路设计本轮另重跑test_trade_route_state.py、test_network_multisource.py、test_d0005_models.py三组，通过的是MOCK拓扑/重建/去重/撤销/多源计算，不是实际路线权威来源。

USER_GAME_TEST_REQUIRED：[B023三案](../../Status/Validation/Cases/B023_Automatic_Constant_Lv1.md)。没有启动游戏。新增网络方案只为提案，见[连接与分发设计](../Proposals/Specialization_Network_Connection_Distribution_Plan.md)。

## 文件

运行：修改ResearchSupport.lua、Probe.lua、modinfo、UI/P0Panel.lua及xml；新增Data/ConstantSupport.sql。Gameplay既有请求接口保持，CityFlowProbe本轮不改。新增DevelopmentTests/test_auto_constant_support.py、本报告、B023案例与Network提案；更新Architecture A0052、Status S0054、README、AGENTS版本引用、技术索引。Design保持D0008，旧测试/历史原件不改。修改前备份DevelopmentBackups/Specialization-before-B023。
