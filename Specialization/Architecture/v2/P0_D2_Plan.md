# P0-D2 — Research III「学以致用」实施计划

Status: IMPLEMENTATION_COMPLETE_AWAITING_USER。B085.112本地通过；[实施报告](P0_D2_Research_Apply.md)。

**实施授权增量（优先于下文原始计划）：** 用户独立授权D2整数floor，并明确每名专家先floor再按人数结算。各领域按yield合并后每名floor，原生专家载体，无城市平铺。取消半点probe门禁；保留原计划为可追溯背景。Design系数/文件不改。下文“未授权/半点必须实测/不继承floor”均属于授权前计划，不再派发测试。正式最小测试改为0/1/2专家整数增量、D变化和撤销/读档。
Authority: Design D0035 / Research D0031 RES_L3_APPLY、yield_mapping、district_qualification / Shared D0035 DISTRICT_DEVELOPMENT / Architecture A0161。Baseline: B084.111/modinfo111，runtime33dc5cd；P0-D1用户整体验收通过。现有W0001 hashes复用，非目标模块不做无必要全量重审。四专业scope不扩到Military。

## 1. 唯一Gameplay目标

当前Identity=Research，Potential>=3且ACTIVE>=3；IV继承。每名**正在工作的科研专家**，从本城每个合格非学院领域获得：

`perSpecialist[y] = Σ(domain maps to y) (0.5 × D_domain × value_multiplier)`
`cityExpected[y] = workingResearchSpecialists × perSpecialist[y]`

D由既有DistrictCompleteness提供：合格普通建筑Tier权重之和、单区域cap10、同领域最高单区域。它是**区域基础设施深度**，不是完成百分比，不归一化纯HD三层D6与扩展四层D10。区域本体D0不提供本能力收益。完成/未掠夺、特色替代、免费普通建筑、同Tier逐栋及不补缺失低Tier沿用Shared。

| 领域 | 对应产出 | 每名专家贡献 |
|---|---|---|
| 工业区、军营 | 生产力 | 各0.5D，再相加 |
| 剧院、市政广场、外交区 | 文化 | 各0.5D，再相加 |
| 商业中心、港口 | 金币 | 各1.5D，再相加 |
| 圣地 | 信仰 | 0.5D |
| 社区 | 食物 | 0.5D；沿用当前已接受非阻塞默认映射 |

学院排除；未知领域排除并说明，不自行扩展映射。只社区需要实际多实例模型，同领域用最高D，不相加。一个学院环境沿用用户确认，不要求用户造多个学院。

例：工业D3、军营D1、商业D3、港口D1、圣地D1时，每名专家+2生产力、+6金币、+0.5信仰；两名专家分别+4、+12、+1。专家基础3F3P独立保留，不把本能力算作替代。P0-C科技与P0-D1区域科技独立共存。

## 2. 专家小数承载门禁（第一步）

STATIC_CONFIRMED：P0-C通过Building_CitizenYieldChanges给学院专家整数Science，并已用户验收；当前只读数据库该表YieldChange声明INTEGER。SQLite可存某种值不证明引擎结算保留该精度。B083/B084区域固定收益整数结果、HD per-population小数和旧Copy半点均不构成本接口PASS。

P0-D2设计值自然为0.5步长，不需要任意0.1精度。优先调查/验证原生专家yield接口或等价按工作专家结算的区域路径；不能用人口、所有专家或城市平铺补偿冒充科研专家收益。既有每专家carrier结构可复用，不机械复用整数参数类型。

顺序：静态数据库/HD先例 → 纯模型/真实Lua与SQL验证 → 若仍无引擎证据，最小隔离primitive（需后续实施授权） → 验证0/1/2名专家的0.5及Gold1.5实际增量、撤销和存读档。可用同一小城完成，并覆盖正式公式；若先做隔离probe，明确该包只是probe，cleanup后才正式发布。

**D1临时floor不继承到D2。** 不提前round/floor，不把系数改1，不用两名专家的整数总额掩盖一名专家半点失败。若专家半点无法可靠实现，停在技术门禁报告，提出所需决定；保留B084正式能力，不部署伪完整D2。当前无Design矛盾，不必预先要求用户选fallback。

## 3. 模块与旧效果边界

- 新增窄范围ResearchApply纯计划/唯一writer和独立internal carrier SQL（文件名暂定）；复用CurrentSpecializationFacts、DistrictCompleteness、OrdinaryBuildingCatalog与RuntimeWork。无需跨context BASE样本，不复用Cross的yield公式。
- Gameplay只增加启动、必要显式progression/action刷新及按需诊断入口；panel复用合适位置，明确中文caption，摘要/详情分层。不改现有C2采样合同。
- 单次城市处理读取一次D快照并给九领域共享；worker只读一次。尽量让原生专家carrier跟随人数，避免每次人数变化重写相同每人系数。
- ResearchInfrastructureShadow.WithWorkers当前硬限制ACTIVE4，不可直接拿来用于III；写最小III/IV读取或精确兼容适配，必须保持P0-C回归，不扩大成generic ability engine。
- 当前没有独立RES_L3_APPLY writer。D1已停Research人口分支及8附件，P0-C已退48旧IV效果。因此本批原则上**无新增旧能力退休清单**；实施前仍对动态ID/SQL/间接调用精确搜索，测试这些旧效果不会复活。
- 保留：ResearchCross及临时floor、ResearchInfrastructure、全等级支持、Lv2住房/GPP、Research旧Network（新设计仍deferred）、Culture/Commerce Lv3、Industry采样/Copy/Standardization。不能整文件撤销Lv3Effects。
- 所有新carrier继续internal、无slot/Housing、从ordinary D目录排除，避免写入自身改变D。载体ID及有限数量在primitive定型后锁定，不在此凭空定实现cap。

## 4. Catalog与有效性

已知Data Center/集市/Art Publisher/Harbor扩展/HD社区覆盖问题仍属catalog适配，不属D归一化，也不是P0-A完整环境PASS。授权实施后先核对D2九领域将实际读取的目录；缺项按现有分类证据登记，必要最小适配单列审计，禁止把所有未知建筑猜作普通建筑。若事实不足，显式显示未审对象/受影响领域；已知普通建筑Tier或位置不可确认时不得静默输出“完整D=0”。不能靠局部fixture宣称全HD环境已覆盖。

Current Identity / ACTIVE / Campus有效性 / D事实和current reference共同决定结果。UNKNOWN/暂不可用保留上次确认投影；确认失去资格、学院失效或建筑真实移除才更新/撤销。读档重建派生缓存，复核载体；同输入/同结果不重复写。不要引入新永久存档或ownership规则。

## 5. 事件与性能

建筑建成/删除/掠夺修复、区域变化→相应D dirty→受影响城市重算；总督/正式progression→资格重算；专家分配→更新预期总量，能交原生结算的系数不重复写。实际事件签名先核对，无法城市定域的事件沿用有界安全范围。每本地回合保留一次有限reconciliation，不以Publish/Playback/UI timer为每帧扫描入口。

注意当前P0-C某些回调先MarkDirty再读；D2必须验证listener顺序不会同批重复完整capture，也不能由internal carrier的Building通知循环重算。优先城市批次共享快照/提前无变化停止，只做必要窄适配。No hover request、no periodic sample、no Network Capture、no每事件日志。按需诊断允许选中城市一次读取，空闲面板零请求。

## 6. 本地验收矩阵

1. D0/1/2/3/6/10，九领域、特色、免费普通建筑、同Tier、缺低Tier、未完成、掠夺、internal/unknown排除。
2. 同产出领域相加、商业/港口Gold×3、社区多实例取最高；不把其它领域的D转成Science，不用区域种类数X。
3. ACTIVE0–4、Identity非科研、0/1/2/多名科研专家；空槽与非科研专家不受益；III和IV系数一致。
4. 无效/UNKNOWN/重复/存读档/当前引用变化；同结果zero writes；真撤销一次；正常测试不得隐藏module errors。
5. 1/2/4/8城：记录D capture、事实读取、城市处理、carrier writes；无C²读取。10k无关通知和UI计时回调不新增昂贵扫描/发送/写入；跨回合fallback有界。
6. P0-A/B1/B2/C/D1、AV2生命周期回归；8+48退休附件持续为零；非目标模块新旧输出一致；SQL/manifest/Lua/部署安全。
7. 期望、carrier配置、引擎读数分开；本地半点模型PASS不是native半点PASS。

## 7. 最小用户测试（实施后，当前无需启动游戏）

一座科研ACTIVE III城市，学院及工业/商业领域，准备至少一个奇数D领域；用0→1→2名科研专家验证每人0.5/1.5步长及总量。增加一座领域普通建筑观察D增长；ACTIVE降级恢复、保存读档覆盖撤销/重复。可在同一短流程确认P0-D1不变；不要求手动掠夺、不要求多学院。其它域与社区highest先本地覆盖，不给用户九城测试清单。

诊断左键仅：资格、工作专家数、各yield每人增量/预期总增量、配置是否一致。右键：领域→选中区域→D→份数→对应产出，按需列建筑组成和排除原因。例“商业D3→1.5份→每人+4.5金币”，不堆内部bit名字。

## 8. 完成、回滚与停止

静态/本地回归通过、primitive有可靠依据、唯一writer及撤销明确、无旧收益复活、文档/manifest更新 → coherent develop commit/push。若需实机才可确认primitive，诚实标USER_GAME_TEST_REQUIRED，不能称最终Gameplay PASS。正式批次和probe状态明确分开。

回滚边界为完整B084.111包+切换前独立存档；新增carrier入档后不保证直接降级存档兼容。W0003只在后续用户授权实施且本地验证/退出/恢复点/hash门禁满足时允许测试部署；本轮不部署。

不包含：D1公式/D方案、学术主持(P0-D3)、传统、Research Network重设计、其它专业、Military、ownership/save迁移、UI polish、全环境catalog重构。完成D2后停止，不自动D3。

结论：可授权开始P0-D2；无新增阻塞Design问题。专家半点是TECHNICAL_SPIKE_REQUIRED，不是已证明失败或已获floor授权。
