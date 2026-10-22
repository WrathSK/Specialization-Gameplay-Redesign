# P03a/P10a — Research合同、当前writer与长期记录

独立审计 IA20261007 / W16；基线 `d208ecc0f0340a614e4a12a5676ef81adb83309d`。科研slice覆盖完成，非所有native边界或总审计PASS；只读项目本体。

## 结论与范围

完整[Research D0040](../../Design/Content/Research_D0040.json)、[Spec RES](../../Design/Specialization_v0.1_Design_Spec.md)与现行Support/Infrastructure/Cross/Apply/Chair/Tradition的主要公式及资格一致；未确认新的独立计算错误。当前科研本地writer已接入，不再靠P0开关试用。

**Research K01 MEDIUM / DEFER仍是实际Design适配缺口**：accepted年龄随城/重新合格恢复，旧OWNER_POLICY_UNRESOLVED却持久保持并阻止效果。B164/P06已经登记，不重开Gameplay TBD。保留网络仍待重设计；正常用户PASS不覆盖跨Owner、任意异常或全部环境。

## Rule→actual→evidence

| 包 / 门槛 | accepted与实际计算 | 当前来源 / 限定证据 |
|---|---|---|
| 基础1–4 | 每实际科研专家3F3P，不再III升5F5P | [ResearchSupport](../../../Mod/ResearchSupport.lua)共享anchor＋native CitizenYieldChanges；B079用户overall口述，无逐边界截图 |
| II人才培养 | actual专业anchor本体/每正Tier住房1，每worker Scientist基础GPP2 | Lv2共享路径/P02a已核，独立class与percentage证据继承，不重审全部 |
| IV科研基础设施 | 每worker额外Science=D，Dcap10；工作槽为空收益0，无building Science反馈 | [Infrastructure](../../../Mod/ResearchInfrastructure.lua)inspect/四bit系数＋[Shadow](../../../Mod/ResearchInfrastructureShadow.lua)纯计划；B081overall PASS限原场景 |
| III跨学科研究 | 九非Campus领域、六BASE adjacency完整总和×0.5，最后整城floor一次 | [CrossModel](../../../Mod/ResearchCrossModel.lua)/writer/sample/UI BASE reader；B084overall PASS，不能外推每policy/负值/native源 |
| III学以致用 | 每域D×0.5份、Gold3，其它1；先同yield相加→每expert floor→×W | [ApplyModel](../../../Mod/ResearchApplyModel.lua)/[writer](../../../Mod/ResearchApply.lua)5yield×5bits；B085overall PASS，Neighborhood后补只STATIC/LOCAL |
| IV学术主持 | 每合格普通Campus T1–4建筑各Science=W，逐栋，不Tier加权/不Dcap | [ChairModel](../../../Mod/ResearchChairModel.lua)/[writer](../../../Mod/ResearchChair.lua)具体BuildingType Modifier；B086overall PASS，B144伴随4栋×5读数不是全能力重验 |
| IV学术传统 | first永久P4可靠receipt起age0，5%起；独立floor(10*j*s)门槛，10/20/30/40标准turn到10/15/20/25%；仅ACTIVEIV效应 | Store年龄唯一authority，纯[Tradition](../../../Mod/ResearchTradition.lua)及独立[Effects](../../../Mod/ResearchTraditionEffects.lua)五档；F1/F2具名native范围见下 |
| Network | 保留NET-RC Inspiration，最高ACTIVE/去重N/最终half-up | P02b已核，NETWORK_REDESIGN_REQUIRED，不误退Research或虚构新payload |

Cross不读取Actual/城市总yield、D、Gold份额、专家或人口；新RES内容取代旧IV Actual复制/专家城市百分比。Floor是独立实施授权，原Design公式无全局舍入仍保留：[D1授权边界](../../Architecture/v2/P0_D1_Research_Cross_Cutover.md)、[D2 per-expert量化](../../Architecture/v2/P0_D2_Research_Apply.md)。不能套Meaning逐domain floor或把全部yield视作原生不支持小数。

正式writer保留当前单Campus合同；Shadow可算最高D/多Campus workers，不证明正式多Campus已支持。编码范围、已审building目标与unsupported模式明确HOLD，不静默设Gameplay cap。Apply perexpert最大F5/P10/G30/C15/Faith5；Chair0–255 workers，256拒；Cross signed16bit，negative native效果未独立验收。没有读取外部DB，因此不声称当前loaded Chair目标数=所有13候选。

## Input / writer / exit分层

- 当前facts/ACTIVE沿共享门槛；D是普通当前基础设施，BASE采集是独立原语，不能为DRY共用一份无声明结果cache。
- Infrastructure核实际unique Campus/first/ordinary tier/worker；Apply用domain最高单区D与actual Campus worker；Chair逐target BuildingType；Cross的完整sample核generation/epoch/seq/turn/reference/pillage/live集合，整包成功才替换。
- 纯模型与普通投影、按需诊断分开；原生存在/health读回确认与native收益测量不同。
- exact module-owned退出/retired名单防止新旧同时正向输出；UNKNOWN保留已确认投影，确认失效退出。多bit替换不是引擎原子事务，部分创建失败可留已写bit并报错/下一Audit收敛。
- 当前Gameplay有正常Start/dispatch/事实变化consumer调用；consumer fallback名单与player-wide资格读取成本沿P13/F03，不因“不写”就声明无采集。

## Tradition持久状态及已知冲突

`{version,start,age,cursor,state,receipt}`由Store记录拥有。首次第三个Research receipt提交仅在旧pending已CONSUMED_CONFIRMED时，同一次record保存age0，防止P4与起点分开；旧P4无可靠receipt起点不推补。

Store按本地turn/load写年龄，不读Gov/worker/D；ACTIVE下降仍计龄，效应仅ACTIVE4。相同turn不加龄，可靠单turn按前身份区间结算；未来真实Identity writer须提供有序转换，不能只让下回合发现新身份。当前没有重组/转专业动作，纯模型暂停/恢复不代表对应UI已实现。

**K01既有适配冲突**：Research D0040明确城市年龄跟城、unsupported Owner冻结、不补失城区间、重新合格恢复。Store601仍写OWNER_POLICY_UNRESOLVED；return复制保留，Advance27吸收，Effects29不给收益。旧B143/B144 owner测试断言这一hold，不能用其PASS关闭D0040。Describe/F旧计划“归属待定”是实现残留，非需要用户再次决定。级别MEDIUM/DEFER，当前未修。

**UNKNOWN_INTERVAL OBSERVATION / MONITOR**：missed delta>1持久置此状态，Advance之后保持、Effects非COUNTING为0；F1既有合同明确保护。保留年龄不等于自动恢复作用，不能凭后来的当前身份补缺区间。与一瞬间getter不可读、session worker写故障不同；不称新的存档损坏或native事故。

依赖身份变更的前置约束：Validate仍要求历史start≥当前base.first.turn、恰好3当前投资receipt。未来REALLOCATING/P−1/新Identity改变first或投资模型时不能直接复用，否则已保存Research历史会与新当前事实冲突。这是P06a-F03实际返工面补证：明确每资产历史origin与当前progression校验责任，在依赖切片前适配，不把它们合成统一年龄/owner规则。

## 结构风险复用

| 既有项 | severity / timing | 本slice具体补证 |
|---|---|---|
| P06a-F01保存每写全record检查 | MEDIUM / FIX_NOW | 多P4/ACTIVE1正常年龄写是合法工作集，不能用单城F1反证N×T；不重跑已核规模 |
| P06a-F03业务进入保存核心 | MEDIUM / FIX_BEFORE_NEXT_PROFESSION | Validate/Begin/Tick/loss字段与历史receipt绑定；新Identity/资产新增会扩大迁移闭包 |
| P13a-F03事实/调度重复 | MEDIUM / FIX_BEFORE_NEXT_PROFESSION | C/Cross/Support独立player-wide采集；Cross每ACTIVEIII/IV城inspect、UI sample、Receiver重复读同loaded DistrictReplaces。inactive早退/clean UI不采集，不能夸大所有城市每frame |
| P13a-F02 rich D/逐presence | 原timing保持 | 当前需校related ordinary rows/reference，未来compactAPI带availability/原因，不能删资格校验 |
| P08a-F01/Q01多bit失败/重入 | MEDIUM / BEFORE_NEXT；Q01 MONITOR | 既有失败/ACTIVE写中变化反例保持，native可达未知，不重复finding或声明已经收益泄漏 |

可优先明确静态metadata owner/loaded revision、cause/scope、只读借用与mutation后失效；不新建通用ability engine、粗限每城每turn一次或为优化改变BASE/D/效果公式。没有新nativeCPU/分配测量。

## 验证声明及成熟度

只审现成断言，未跑Gameplay tests/新复现：C实际D/Infrastructure/SQL，Cross actualUI→sample→writer，Apply/Chair model＋SQL-backed writer，F actualStore/Investment/Effects都有定域断言。模板/worker/Property/transport/Modifier容器多数mock；不能把模型配置矩阵作原生结果。静态schema/hash只是完整性。

native记录只读文字，未重看截图：[F1](../../Status/Validation/Results/Specialization_B143_F1_Pass.md)起点、ACTIVE1下age0→2和用户确认冷重启；[F2](../../Status/Validation/Results/Specialization_B144_F2_Pass.md)5→10%/age10，与综合大学20%相加为30%、总督撤销、用户确认重启。其它速度/15–25%档/异常保存/跨Owner未扩为nativePASS。伴随Cross/Chair/Apply报告不替代各自完整验收。

Content整体NOT_IMPLEMENTED与旧交付“待测”不是今天Status；已接入/具名PASS也不是所有科研边界完成。名字/英文参考/Balance成熟度照正式source，不因源码可用升级。当前B168为Culture延期测试，没有恢复用户测试。

实际readscope：完整Research469行/RES；Support/Infrastructure/Shadow/Cross模型/样本/UI与Apply/Chair/Tradition/Effects直接计算/gate/reconcile保存闭包；对应SQL、Gameplay注册、C/D/F合同、定域断言与具名结果。P06/P07/P08/P13复用，未全扫Mod、全历史、DB或运行包。

下一 **P03b/P10b Industry accepted规则→历史/模板/折扣/施工链对照**：Industry_D0045、SpecIND与Shared已核A/B/E/G条款→Standardization/Catalog/Discount与IndustrySupport、已有Crew链，N/E/L/三工程能力当前缺实现按准备矩阵。P07c已经核source/receipt，不重新跑；优先每模板holder、自身来源与旧全局max/Copy退出的规则和扩展边界。仍audit-only，不进入J/H等实现。
