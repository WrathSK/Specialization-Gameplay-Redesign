# P0-D2 学以致用 — B085.112 / modinfo112

Status: IMPLEMENTATION_COMPLETE_AWAITING_USER / LOCAL_SIMULATION_PASS。不是引擎实机PASS。
Authority: D0035 / Research D0031 RES_L3_APPLY / Shared D0035；A0161。原计划 cb8a4c7 / B084.111。

## 用户确认与唯一计算合同

用户本批明确“按照Floor整数实施”，随后澄清“施加到每个专家身上……floor后，按照每专家计算”。因此原计划半点primitive门禁被本批独立授权的整数方案取代，不是自动继承D1结论。Design文件及0.5转换系数不改；记录为临时实现量化，未来精度方案另审。

按九领域映射先合并同产出原值，再对**每名工作科研专家**floor：
`coefficient[y] = floor(Σ 0.5 × D_domain × value_multiplier)`
`expectedTotal[y] = coefficient[y] × workingResearchSpecialists`
金币 multiplier=3，其它=1。不是整城汇总后floor，不是每个领域单独floor，不是城市/区域平铺补偿。

- 单工业D1：每名原值0.5→0；两名专家仍0。
- 工业D1＋军营D1：合并每名1→1；两名专家+2生产力。
- 商业D3：每名4.5→4；两名专家+8金币。
- ACTIVE III及IV均适用；低于III/Identity变化/学院确认不可用撤销。基础3F3P、Lv2、科研基础设施及跨学科研究独立保留。

## 实际模块与写入边界

- `ResearchApplyModel.lua`：纯规则计划；九领域、同领域最高单区域D、按yield合并和每名floor。
- `ResearchApply.lua`：唯一正式writer及按需解释；复用CurrentSpecializationFacts和DistrictCompleteness。25个原生Building_CitizenYieldChanges整数bit（5种产出×1/2/4/8/16），均放学院，internal、无住房/槽位、不进D。当前数学上限每名Food5/Production10/Gold30/Culture15/Faith5，超范围报错保留，不截断cap。
- `Data/ResearchApply.sql`：原生**科研专家**增量，不创建城市平铺或区域固定收益Modifier。P0-C整数专家路径已有用户证据；本批五产出组合仍USER_GAME_TEST_REQUIRED。
- `Gameplay.lua`：启动、既有显式progression/action刷新、选中城市READ/DETAIL。无跨context sample协议，无新Property/永久ledger。
- `UI/P0Panel.lua/xml`：复用空闲诊断位“学以致用”，明确Caption；左键摘要、右键组成。旧Boost入口代码保留但在当前面板隐藏；不是取消Network效果。
- `DistrictCompleteness.lua`：BuildingAdded/Removed识别已排除的SPC技术建筑，不让自身carrier写入使共享D失效；普通/未知建筑仍dirty。P0-C先登记、先确认D，本模块不再次mark dirty；同一事件复用该确认结果。
- 版本及RuntimeAudit元数据同步。无半点probe加入运行包，无P0-D3。

原有Research III人口8和IV复制/百分比48已经退出，本批无新增退休清单。非目标writer/SQL字节与cb8a4c7相同；旧附件不会复活。

## 有效性、事件与性能

坏/暂缺专业事实、D、worker或carrier读数：报可诊断状态，保留上次配置。确认失去资格/区域失效则撤销一次。load重新读当前事实，原生已存carrier按差异校正，不累加；无新save schema。空槽下原生无专家收益；系数可以保留，人数变化不重写相同系数。

建筑/区域/掠夺修复/资格事件、显式progression调用、worker事件驱动；PlayerTurnActivated每玩家每回合一次安全确认。签名无法精确城市定域时保留玩家/全局有限范围，不假装全部单城增量。无Publish/Playback/UI timer/单位移动监听，无hover请求、后台定时sample或逐事件日志。现有city_scan、dc_capture、building_check及Building计数复用。

测试中P0-C＋D2共用D，1/2/4/8城对应：

| 城市 | shared D captures | 专业事实读数（两个consumer） | 区域读数 | 建筑检查 | 初次两consumer载体写入 |
|---:|---:|---:|---:|---:|---:|
|1|1|2|2|245|2|
|2|2|4|4|490|4|
|4|4|8|8|980|8|
|8|8|16|16|1960|16|

这是明确fixture（每城学院＋商业中心）工作量，不是任意城市数/真实DB常数承诺。D缓存上限8未扩大。10,000次无关Publish/Playback/UI/单位通知：新增扫描/读取/写入0。UI10,000 idle：发送0；两次手动摘要/详情各发送1。同回合10,000 turn通知只允许首个确认；新回合恢复一次。内部Building事件不capture，普通建筑事件两consumer合计一次capture。

## Catalog复核：没有声称全环境完整

本批不修改ontology名单：Data Center、集市BUILDING_FAIR、Art Publisher实际已由P0-B2加入，沿用当前DB Tier；原计划的泛指缺口不应误读为它们仍全缺失。

只读当前DB＋安装文件仍发现11个未审目录对象：HD Villa/Mansion/Bus Stop、HD Alchemy Room、El Escorial Palace、Human Rights Council、Ministry of National Defense、JNR Lighthouse Fishing/Entrepot/Fish Market/Offshore Terminal。部分对象存在HD/扩展领域变更，不能仅凭Tier自动收录。本批保持UNREVIEWED_BUILDING排除并在诊断提示；目录补齐是独立最小适配待办，不是D归一化理由。已知ordinary但Tier/位置不明会保留旧值，不伪造完整0。

静态来源：HD `UpdateDataBase/DL_BuildingDefinations.sql`，区域扩展 `Database/commerce_JNR.sql`、`Database/diplomacy_JNR.sql`；当前DebugGameplay只读。没有修改HD/数据库。未审对象环境不纳入完整目录PASS。

## 验证证据

STATIC_CONFIRMED：所有Lua编译、完整modinfo112/文件清单、25新SQL整数专家行、旧writer/SQL/Design逐字节保护；实际DebugGameplay schema复制到内存执行SQL成功（仅注册Make_Hash替身，不能证明引擎收益）。

LOCAL_SIMULATION_PASS：`test_research_apply.py`实际Lua/SQL/事件/诊断/UI；120种D0/1/2/3/6/10、ACTIVE0–4、workers0/1/2/5模型；五yield最大编码5/10/30/15/5与撤销；每人floor、合并顺序、Gold3、社区最高D、unique学院、未知保持/失效撤销/掠夺修复/epoch引用/load、正常无隐藏module error、幂等。`test_research_apply_regression.py`复用前序D1及P0-C/B2/B1/A与Architecture v2 A/B/C1/D1/C2/D2回归；只显式适配版本/新增文件预期，历史测试未改。部署/临时切换安全测试通过。

USER_GAME_TEST_REQUIRED：本批真实五产出专家结算/显示，不根据本地配置冒充native读数。不宣称55GB根因或全部目录覆盖已经解决。

## 诊断与一次最小验收

“学以致用”左键只列：ACTIVE、工作专家数、每种有贡献产出的原值→floor、每名配置、总预期；右键列领域D/选中区域/cap前后/普通建筑Tier和贡献。示例：`金币：每名4.5 →4；全城预期+8；每名配置4`。总预期不含基础支持或其它能力；不是原生实测。

同一科研ACTIVE III城：学院＋一个已知目录工业/商业领域；0→1→2名科研专家，对照原生专家/城市收益与诊断增量（含基础3F3P需分开）。增加一个对应普通建筑，观察D和每人floor变化；便利时降ACTIVE再恢复、保存读档一次确认不叠加。无需手动掠夺/九域逐个建城。不运行旧精度实验按钮。

回滚需完整B084包及切换前另存档：新增carrier已经入档后的向后存档兼容不作承诺。W0003部署另有完整hash/恢复记录。完成后停，不自动P0-D3。
