# P0-A Shared District Completeness / Research shadow — B077.104

Document Owner: Codex
Architecture Revision: A0161 (A0160 target contracts unchanged)
Design Authority: Spec D0032; Shared D0028; Research D0031
Source baseline: 04a629ec61f677894eb28e642c81b9f16bc1c774 / B076.103
State: IMPLEMENTATION_COMPLETE / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED
Deployment: NONE; live remains B076.103, main remains B069.96

## 用户摘要

完成一个只读数据链：原生城市/建筑事实 → 统一区域完善度 → 当前专业只读适配 → 科研基础设施影子plan → 手动诊断。没有新的Gameplay收益、carrier、Property保存、旧writer退出或其它专业能力。P0-A本地门禁通过；没有把mock等同Civ VI引擎验证。

诊断入口：选择己方测试专业城市，打开现有专业化诊断，点击“区域完善度 / 科研影子”。按钮占用原诊断说明文字位置，不新建HUD或改布局体系。一次点击只发一次COMPLETENESS_READ，无hover/后台请求；原有“写入诊断日志”可保存已读取文本。报告显式标记SHADOW_ONLY和实际新增收益0。

## 新增模块 / 权威

| 模块 | 责任 | 不负责 |
|---|---|---|
| OrdinaryBuildingCatalog.lua | 115个明确审核的原版/HD集成普通建筑ID白名单；已加载HD Tier和BuildingReplaces解析；DistrictReplaces归一 | 不把任意有Tier或非InternalOnly对象自动当普通建筑；不改HD/SQL |
| DistrictCompleteness.lua | 一份完整city snapshot、纯D计算、领域最高单区域、session revision、8城LRU cache、lazy dirty/reconciliation | 不拥有专业历史、不发收益、不通知旧Audit、不写存档 |
| CurrentSpecializationFacts.lua | 只调用原EffectiveFacts，复制Identity/Potential/ACTIVE/token/anchor与UNKNOWN | 不重算投资、不写Flow/Journal、不引入新永久身份 |
| ResearchInfrastructureShadow.lua | 读取已索引Campus地块的working specialists，纯计算D×人数及诊断解释 | 不创建carrier、不执行科研能力、不改变城市Science |

Gameplay.lua只增加启动这四个只读模块及独立诊断dispatch；原writer Start/控制入口全保留。P0Panel仅增加按钮及click callback。PerformanceCounters增加6个固定指标。Probe/modinfo/RuntimeAudit元信息更新为B077.104/modinfo104；没有改自动log机制。

## Ordinary ontology / D合同

`SPCOrdinaryBuildingCatalog.REVISION=D0028-P0A-1`是实现目录版本，不是新Design revision。115条白名单覆盖当前Shared十个领域中已审核的具名普通建筑；数据来源为本机已安装HD环境的普通可建设建筑及替代定义。只读抽取的精简fixture位于DevelopmentTests/Fixtures/P0A/catalog.json；它是静态证据，不代表当前游戏加载组合，也不是运行时数据库副本。

- 本轮不建立全未来领域catalog。未审核ID、未来未映射领域明确排除/报告，不静默扩展。免费取得不改变已知普通建筑资格。
- Palace、Wonder、InternalOnly、HD dummy、SPC technical/presentation/carrier全部排除；不仅靠InternalOnly判断。
- 已知建筑Tier来自当前HD表；特色建筑按已审核替代链归一。多个替代目标必须同Tier；冲突、环、未知目标、未知或超出0–4的Tier均有原因，不猜值。
- Tier0可以是ordinary，但D贡献0；普通资格不是Tier>0。白名单不是Standardization的折扣启用目录。
- 使用原生City District集合与`GetBuildingsAtLocation(plot)`归属，逐实例计算，避免城市级HasBuilding重复归入每个同类区域。
- 每个已完成、未掠夺的合格普通建筑贡献其Tier；未完成/被掠夺建筑贡献0；未完成/被掠夺区域不参与有效领域选择。
- `uncapped=sum(contributions)`，`value=min(10,uncapped)`；同Tier多栋分别加；缺低Tier不补齐。同领域取最高单区域，平局按最小districtID稳定选择，绝不累加实例D。
- 当前未完成Building队列只作为排除证据，不读写生产进度。未知读取不是“空建筑列表”。

这个service是P0-A新增D事实的唯一来源，尚未被旧正式收益模块消费。现有Housing按Tier存在性、旧Copy按actual yield、旧GW按BASE adjacency继续独立运行；本轮不会强制把它们改读D。

## 样本 / 版本 / 性能

City reference包含owner、cityID、位置及现有confirmed token；不是跨Owner永久cityKey。完整原生读取成功后才替换snapshot。相同内容不增加revision。读取失败时返回last verified及TEMPORARILY_UNAVAILABLE，shadow返回HELD且不把失败解释为Science0。reference变更不能复用旧snapshot；LoadScreenClose清cache/catalog并增加epoch。返回副本，调用方不能改写authority。

缓存只保留最多8个最近按需查询城市，目录只依赖当前加载DB，均与事件历史无关。无关注意通知（Publish/Playback/SystemUpdateUI/单位操作）没有新listener。建筑/区域/掠夺等direct事件只标记已缓存条目dirty，不进行原生扫描；签名不确定的事件保守标记至多8条，不猜player参数。下一次显式读取才刷新。漏事件兜底为新回合第一次显式读取；没有自动每回合全城扫描。

同一失败输入每回合最多尝试一次，或新的真实dirty到达后再次尝试；不存在timer retry。反复真实事件也不会自动触发读取。补充counter为dc_read/capture/hit/dirty/publish/failure，放入现有固定counter描述，不新增逐事件日志。

P0-A报告按需构建完整解释；此详细read不是适合每帧调用的API。以后consumer可另取轻量投影，但不得用这一点绕过本批零idle工作合同。

## 诊断内容与示例

每个区域列出原始type、normalized domain、id、完成/掠夺状态；每个已列出建筑包含type/name、normalized Tier、tierSource、contribution、pillaged及reason；随后显示cap前后值和是否为该领域最高单区域。未知/内部/奇观等排除对象同样可见，不只给最终D。

下面是本地模型示例，不是实机截图：

```text
P0-A 区域完善度 / Research Infrastructure SHADOW_ONLY
只读影子计算；实际新增收益=0；旧writer保持运行。
RESEARCH Potential=4 ACTIVE=4
DISTRICT_CAMPUS #11 complete=true pillaged=false
  LIBRARY    Tier=1 contribution=1 pillaged=false reason=INCLUDED
  UNIVERSITY Tier=2 contribution=0 pillaged=true  reason=BUILDING_PILLAGED
  LAB        Tier=3 contribution=3 pillaged=false reason=INCLUDED
  cap前=4 cap后=4 /10；最高单区域=true
科研基础设施影子：READY | D=4 × working specialists=3 → Science=12
```

科研专家读取与D本身分离：对本城已确认、完成、未掠夺Campus实例，各读取一次workers。D仍取最高单区域，人数按working Campus specialists统计，不把多个D相加。没有建筑Science反馈，没有倍率、取整或新增production rule。

## 本地验证结果

运行：`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14 DevelopmentTests/test_p0_a.py --regression`。PYTHONPATH为本机既有Lupa环境，仓库不依赖此固定路径；其它环境按tests requirements安装。

| 场景 | 结果 |
|---|---|
| 空 / T1 / T1+T2 / +T3 / +T4 | D=0/1/3/6/10 |
| 仅T3 / 两座T1 / Tier总和13 | 3 / 2 / cap10，保留uncapped13 |
| 特色建筑/区域 | 已审核替代Tier及Domain归一正确 |
| 免费普通建筑 | 正常计入；不检查获取费用/来源 |
| 未完成/掠夺建筑与区域 | 贡献/领域资格正确排除，修复后direct dirty恢复 |
| Palace/Wonder/carrier/dummy/unknown | 排除且有明确原因 |
| Tier0/非法Tier/替代冲突 | 零贡献或带原因排除，不自行补Tier |
| 多个同领域区域 | 最高单区域；不相加 |
| 10k无关通知 | 新扫描/发送/写入=0 |
| 10k真实dirty通知 | 原生读取0；下一次手动读取仅1次capture |
| 重复snapshot/返回值被调用方修改 | revision不增；authority不受副本修改影响 |
| 暂不可用后10k读取 | 保留旧事实，capture不持续重试，shadow HELD |
| 确认移除 / 漏事件到下一回合 | 正确更新0 / 有界按需恢复 |
| ref变化 / load epoch | 不借用旧城市样本；cache清空，epoch变化 |
| D10、5专家 | shadow50 Science，applied0 |
| 双Campus最高D3、合计6专家 | shadow18，非D相加；applied0 |
| ACTIVE3 / UNKNOWN / worker0 | INACTIVE0 / UNKNOWN不伪造0 / READY0 |
| 原EffectiveFacts实际Lua | 投资ledger＋总督得到Potential4/ACTIVE4，适配全程只读 |
| 实际Gameplay dispatch / 实际P0Panel callback | 一点击一次请求；10k UI事件不追加请求；无旧Audit调用 |
| 1/2/4/8城，各1区域1建筑 | capture=1/2/4/8，区域枚举=1/2/4/8，建筑条目检查=1/2/4/8；Network查询0 |
| 查询1000个不同城市 | cache始终≤8；无保存写入 |

全Lua编译、manifest引用/version104通过；旧效果Lua及全部Data文件字节对照通过。D2的1728正常载体对照、10k idle、30k Network读、C2/C1/D1/A/B/B069合同回归通过，历史测试只在内存调整build断言，没有改写历史文件。部署/临时切包安全测试仅在临时目录运行并通过，没有执行实际部署。

## 证据与剩余原生验证

- **STATIC_CONFIRMED**：代码/DB分类与方法静态线索。HD CitySupport.lua使用City District集合及GetBuildingsAtLocation；HD Gameplay/RegionalYields.lua使用HasBuilding/IsPillaged及GetBuildingLocation，原生接口的Gameplay context组合仍不能靠mock确认。
- **LOCAL_SIMULATION_PASS**：上述实际Lua+原生mock、本地调用计数、UI/dispatch和历史回归通过，不是引擎PASS。
- **USER_GAME_TEST_REQUIRED**：Gameplay context是否提供本批采用的方法、原生建筑归属与掠夺/修复事件实际到达、按钮显示；未部署、未测试。
- **TECHNICAL_LIMITATION**：当前目录限审核的115 ID/十领域，UNKNOWN不猜；当前测试文明/32城限制未改。这不是对未来通用Shared服务永久范围的Design改写。

下一次若用户授权临时部署，只需一次小流程：现有Research IV城市准备Library＋University及已知专家人数，读报告；同回合掠夺University再读（D3→1），修复再读（→3）；若事件未刷新，下一回合读一次判断兜底。检查建筑条目、原因、shadow数值及实际新增收益标记0，不要求多城/特色/全部Tier分别跑游戏。把UNKNOWN原文回传即可，不让用户调试Lua。

P0-A判定：**本地PASS，实机证据待补**。无新的Design blocker。当前用户无需操作现有B076运行包。下一推荐实施批次P0-B1（全等级基础支持适配），但本批结束即停止，先由用户审阅及决定最小实机/后续实施授权。P0-C真正收益cutover未开始。
