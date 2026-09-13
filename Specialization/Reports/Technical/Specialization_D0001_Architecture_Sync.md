# D0001 → A0002 架构同步记录

Document Owner: Codex
Design Revision: D0001
Architecture Revision: A0002
Sync Status: SYNCED_WITH_LIMITATIONS
Accepted Spec SHA256: 10323a0350ff5b97be179b25c1c315b42aa7c6a41cb4cf6d55b9c7a34aee2ae6

## 范围与证据边界

本轮仅同步文档。104个正式Rule ID全部列入下表；18个OPEN条目仍以[Spec](../../Design/Specialization_v0.1_Design_Spec.md)为权威，不重复另建设计待决表。表中“适配”是方案/边界，不是实现或测试PASS。已有证据等级仅见[Status](../../Status/Specialization_P0_Status.md)。

## Rule ID覆盖

| Rule IDs | 架构适配 / 限制 |
|---|---|
| SCOPE-001, SCOPE-002, SCOPE-003, SCOPE-004 | 范围和治理约束；仅v0.1进入当前实现计划，Future/provisional不升级。 |
| ID-001, ID-002 | 现有独立数据库身份/展示资源；原Mod UUID与加载路径保留。 |
| TERMS-001, TERMS-002, TERMS-003 | 分别存专业/Potential/ACTIVE；Base与原生复制基数分接口。特殊范围见OPEN-08。 |
| PROG-001, PROG-002, PROG-003, PROG-004 | 完成事件、Property事实与防重复动作；UID/继承/旧档未解决。 |
| SHARED-001, SHARED-002, SHARED-003 | 专家计数有证据；住房/基础GPP/层级替换尚未接正式效果。 |
| RES-001, RES-002, RES-003, RES-004, RES-005 | 专家基础层+城市效果+Boost适配；复制基数与精度仍待验证。 |
| CUL-001, CUL-002, CUL-003, CUL-004, CUL-005 | 专家GPP多类型分别建模；保值和相邻补贴由GW独立处理。 |
| GW-001, GW-002, GW-003 | 隔离城市补贴方案；时代表、类型与Tourism/theming语义仍待明确/验证。 |
| IND-001, IND-002, IND-003, IND-004 | Base专家效果与Actual网络输出分离；多源输出未定。 |
| IND-NET-001, IND-NET-002, IND-NET-003 | 永久模板与当前来源资格分离；Gold-only接口及多源规则待解决。 |
| CREW-001, CREW-002, CREW-003, CREW-004 | 固定规格项目/单位；目标合法性、定额注入、防重放与浪费溢出待验证。 |
| COM-001, COM-002, COM-003, COM-004 | 角色层+按类型去重的专家效果；免费接收以资格原因建模，尚未接收益。 |
| NET-001, NET-002, NET-003, NET-004 | 当前全集→去重→资格派生；Gameplay权威全集尚缺，后台影子不可偷换。 |
| NET-RC-001, NET-RC-002, NET-RC-003, NET-RC-004, NET-RC-005 | 聚合层按有效源ACTIVE选择max后一次计算；k分离；未实现max，Modifier精度未决。 |
| LAND-001, LAND-002, LAND-003, LAND-004, LAND-005, LAND-006 | Future：资源/改良Appeal覆盖、分阶段经济转换、解锁和Amenities效果分别适配；精确参数未定。 |
| REL-001, REL-002, REL-003, REL-004, REL-005, REL-006 | Future：训练时神学属性、压力过滤、信条选择账本与贸易压力分模块；引擎接口未调查完整，不加Prophet对称奖励。 |
| MIL-001, MIL-002, MIL-003, MIL-004, MIL-005, MIL-006 | Future：基础专家/GPP、训练XP、晋升补偿及动员进度分离；候选XP不登记正式参数。 |
| HARB-001, HARB-002, HARB-003, HARB-004, HARB-005 | Future：商业与海军保留双线；资源归属/Base汇总、Export与海军训练各设适配，不缩成半套。 |
| GOV-001, GOV-002, GOV-003, GOV-004 | Future：完成建筑防重入；Potential永久授予账本；ACTIVE槽位效果分离。互斥/一次性效果尚待引擎验证，Loyalty参数未定。 |
| DIP-001, DIP-002, DIP-003, DIP-004, DIP-005 | Future：外交资格/保护约束、使者层、能见度和间谍结果分别研究；永久性/多源见OPEN-12。 |
| DIP-MISSION-001, DIP-MISSION-002, DIP-MISSION-003 | Future：盟友任务资格与独立结果处理；九类区域任务保留，等级解锁/奖励未定。 |
| COMM-001, COMM-002, COMM-003, COMM-004, COMM-005 | Future PROVISIONAL：专业资格仲裁、人口转移事务/目的地权重/底线；不执行候选阈值。 |
| ENT-001, ENT-002, ENT-003 | Future：真实/有效专家分离，Local与Regional参数独立；映射未定前不扩展GPP。 |
| AQ-001 | Future：消费减免适配，不以Food倍率替代；未验证接口。 |
| DAM-001 | Future：条件电力效果，参数X未定；未验证接口。 |
| CAN-001, CAN-002 | Future：改良邻接与城市归属适配，保留原贸易/Product；重复/跨城规则待定。 |
| AIR-001, AIR-002 | Future：复用训练层及Appeal/Gold/Tourism分段适配；不增加自动联网。 |
| SPACE-001, SPACE-002 | Future：玩家完成事实+城市区域资格，双向资格去重；不扩为全国自动接收。 |

## 本轮发现与处理

- Gameplay全集仍无已确认来源；后台UI影子读取与Gameplay任务数量交叉比对保留原上下文边界。不是把无可见窗口等同纯Gameplay。本轮未选择替代权威源。
- DevelopmentTests/NetworkState.lua仍明确只保留来源；源码“无merge”说明是实现缺项，不是Research/Culture设计未决。A0002已指向NET-RC规则；本轮不改源码。
- GOV-002已确认永久Potential授予，未来防重放账本与ACTIVE效果分开，不再询问按哪种等级或是否回收。此处只是架构预留。
- 移除当前Architecture重复的专业数值表、网络公式说明和Crew规格表，以Rule ID适配表替代；原始正文逐字保存在A0001快照。
- 清除当前入口中的空Design、旧Design Chat本地写入者、未分配Rule ID、等待D0001接受等过期说法。冻结Historical/旧结果不重写。
- 尚未证实任何必须改变已接受设计的不可实现性；已知技术缺口不假装解决。若精度、Faith隔离或作品补贴存在语义差异，先报告并取得设计决定，不能直接降级玩法。

## 同步核对

Accepted Spec与ChangeLog保持逐字不变；Architecture/Status旧版本新增冻结快照。运行包仍B010/modinfo17；DevelopmentTests、DevelopmentBackups及ScreenshotInbox不修改。只执行文档、链接、Rule ID和hash检查，没有运行功能测试或游戏。

## 接受记录与当前状态

Spec/ChangeLog中接受时的“Architecture尚未同步”是接受时记录，不为更新同步状态而改动已接受文件。当前同步状态只以Architecture header与Status为准。SYNCED_WITH_LIMITATIONS不清除Spec的TBD/PROVISIONAL，也不升级任何实机验证结果。

## 本轮实际校验结果

只读校验确认：104个Rule ID全部覆盖；当前修改文档的本地链接目标存在；368个纳入保护的既有文件hash未变（包括Design、既有Historical、源码、Tests、Backups、ScreenshotInbox）；Status原有CONFIRMED矩阵及证据索引逐字未变。未重跑本地功能模拟，不新增任何游戏PASS。
