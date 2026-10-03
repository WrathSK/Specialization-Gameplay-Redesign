# B150.177 — P0-L2A单城意义延展原生精度验证包

Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；USER_GAME_TEST_REQUIRED。
Authority: Culture D0029 CUL_L4_MEANING、work_pool/domains；Shared D0035 ordinary/current eligibility、Absolute D及Yield Share；Spec D0037、Architecture A0161。用户明确授权仅L2A；L2B完整能力、全局旧GWA退休、L3/M/N/U2未授权。

## 已实施范围

- `CultureMeaningModel`只读当前Culture ACTIVE4、Shared最高单区域D和已确认合格W；九领域/六产出纯计算，K=0.5初版、金币份额3，不舍入。native probe仅Science/Gold，逐件配置，W仅用于理论合计。
- `CultureMeaningProbe`默认关闭，一个会话fixture，左键依次准备基线→启用→结束。没有新永久Property/账本/补偿记录。一个最后操作凭据防同token重复切换，错误有界。
- GWA自己提供单城精确156片段的hold/withdraw/release；旧退出未确认不启用新测试；测试退出未确认不恢复旧writer。其它城市、旧Dialogue/采集/ACK及其它收益继续原路径。恢复读取正常当前样本，不重放旧快照。
- native-only和未知作品限定仍是L2B门禁。L2A只接受受控馆藏；同类未知作品或类别未知拒绝。Relic/Product等原生Modifier不匹配的排除作品不会被此probe误计；不把整城拒绝变为正式能力规则。
- GreatWorkFacts确认比较补件数和两项native类别安全摘要；没有第二套槽位扫描。相同时代件数变化通知，L1相同投影零写。L1只新增忽略此probe精确十个非ordinary载体事件，规则/公式不变。
- 单城已确认馆藏、D/ACTIVE/引用变化，已有事实通知与玩家回合单城兜底触发；OFF普通事件早退。已知自有十个及旧156载体不触发probe自身事实重采；没有per-frame/hover Gameplay请求或新GC。
- 保存不保存测试模式。加载一次扫描当前城市，**仅撤销精确十个自有测试载体**（含foreign持有），然后OFF；这是冷加载遗留效果清理，不是AI资格/专业审计。确认失城走现有Store.IsExitTarget/RemoveOwned；UNKNOWN保留同引用最近确认状态，陌生引用不继承probe。

## 本地证据

| 检查 | 结果 / 限定 |
|---|---|
| 本轮真实Lua/SQL定向18项 | PASS：D0/1/3/6/10、cap/最高单区域、九映射、Gold×3、W0/1/2、精确半点编码；不证明Civ VI精度 |
| 生命周期/失败 | PASS：单城/切换fixture、旧writer互斥、duplicate action/event、同回合建筑/Governor、UNKNOWN、新引用、confirmed loss、load/foreign exact cleanup、部分退出失败；永久写入stub禁止 |
| GreatWorkFacts/producer/legacy相关26项 | PASS；已支持目录和原桥/旧消费者断言保持 |
| L1相关15项 | PASS，使用现有assertions。外部DB已含B149，仅在内存fixture精确重建L1定义；原数据库只读 |
| 两个旧L1方法 | 本轮不运行：旧era-only通知断言已被本批件数合同取代；旧modinfo176断言为版本固定。对应新合同/177注册在本批测试覆盖；没有改写历史assertions |
| 受影响Gameplay分发/原UI失败重试检查 | PASS：纯worker不触发无关计算，mixed/UNKNOWN/late/load/reentry保留。不是进程内存证据 |
| 定义 / 语法 | 新十个internal载体、70个single-city per-work Modifier；原156/1092 family静态核对。九个改动Lua语法、XML/file注册、本地化检查PASS |

本机只读DB中**集市BUILDING_FAIR为T1，市场BUILDING_MARKET为T2**；本批fixture为集市D1→加入市场D3。目录/Tier未修改，不把名称当深度。

## 一个最小实机流程

使用现有测试存档副本；只选一座Culture ACTIVE4城。优先准备：一件已支持著作、学院D1（图书馆）、商业D1（集市，尚无市场等更高建筑）、港口D0。以报告实际D为准；其它领域不会在此probe发放收益。

1. 选中城市，诊断面板**意义延展验证**左键一次：准备基线。旧巨作相邻仅本城暂停，测试收益0；报告自动记录原生巨作科研/金币基线。
2. 再左键一次启用：每件理论科研0.5、金币1.5。核对“每件载体配置”和下方原生作品差值；整城率含其它倍率，仅辅助比较。右键只读，普通过一回合后右键核对持续生效。配置正确≠引擎精度通过。
3. 加入第二件**同一时代**已支持作品，右键应显示W2、理论合计科研1、金币3；每件仍0.5/1.5。馆藏变化使差值基线失效属正常：左键结束→左键准备W2基线→左键启用，重新自动对照，普通过回合读一次。
4. 在同城将相关深度增加至D3（学院T1+T2；商业集市+市场），结束→准备新基线→启用；每件科研1.5、金币4.5，W2合计3/9。最后左键结束，测试配置清零，旧相邻按当前有效样本恢复；若后台样本未就绪，报告等待而不重放旧状态。

第一个可确认无法忠实结算的值出现就停止并回传该报告，不自行Floor。原生作品getter可能与城市率展示精度不同；若读数互相矛盾，只报告具体接口差异，不能据一个截断显示直接判全部原生收益FAIL。没有请求旧长测/四专业重测/所有城市验收。

冷加载已本地模拟：probe回OFF，保存的测试载体被清理，UI基线不恢复。此最小流程无需额外重复E2夺回；未做的原生load/loss/theming/未知作品组合不升级PASS。

## 当前边界与下一步

本批LOCAL就绪，原生Science/Gold 0.5/1.5/4.5实际精度、归属和正常持续生效待用户；六产出/native-only/theming/混合未知作品/完整L2仍未完成。未改Design、GC、永久账本、AI/MP或main；没有启动游戏。源码commit/实际部署receipt与当前任务以[Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state)为准。

验证结果后只记录L2A门禁并更新L2B方案，等待新授权，不自动实施完整能力。
