# P0-L2 —「意义延展」计划与接口调查

State: PLANNING_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED / NATIVE_PRECISION_GATE_OPEN。
Authority: Culture D0029 `CUL_L4_MEANING`、`contracts.work_pool/domains`；Shared D0035 `DISTRICT_DEVELOPMENT/YIELD_SHARE`。当前运行状态仅见[准备入口](Culture_Preparation.md#当前切片与停止点)。

## 范围与完整规则

只接Culture ACTIVE4的意义延展；每件合格巨作，逐领域追加：

`shares_d = meaning_K × D_d`；`yield_per_work_d = shares_d × share_value(yield_d)`。

meaning_K=0.5为初版参数；金币一份=3，其它普通产出一份=1。同产出领域分别计算相加；同领域多个区域按Shared最高单区域D，不合并D；D是绝对深度cap10，不按规则环境归一化。不要求该领域成为本城Identity，不以工作专家数/人口/作品时代数代替D或件数。

| 领域 | 代表产出 | 对L3的GPP映射（不在L2发放） |
|---|---|---|
| Campus | Science | Scientist |
| Industrial Zone | Production | Engineer |
| Commercial Hub | Gold | Merchant |
| Harbor | Gold | Admiral |
| Encampment | Production | General |
| Holy Site | Faith | Prophet |
| Government Plaza | Culture | 无 |
| Diplomatic Quarter | Culture | 无 |
| Neighborhood | Food | 无 |

不包括Theater自身。完整作品资格只复用K的已支持七类/历史时代目录；Relic、Product、Wonder及未知定义排除。普通建筑完工/未掠夺、免费/特色及缺Tier规则按Shared；不使用旧BASE相邻、旧Actual复制或额外填值。例：Campus D10→每件5Science，Industry D6→3Production，Commercial D3→4.5Gold；Gold并非1.5。

Meaning是追加产出，未来Dialogue只放大作品原生产出，**不得放大本项**。未知原生theming/其它倍率不能被假定为已接受叠加规则；需要对实际路径做组合核对，不能借配置读数替代回合入账。

## 已有实现与可复用部分

`GreatWorkAdjacency.lua/Model`当前读取全部完成专业区域的BASE向量，借Dialogue样本挂`BUILDING_SPC_B060_{yield}_{P/N}{0..12}`，SQL为七类GreatWork的±0.5二进制YieldChange。它仍是旧效果，不符合D输入。模块有精确owned撤销及E2 exit/return，能复用writer/退出结构；旧公式不能保留补空缺。

`GreatWorkFacts`已有confirmed作品/件数，`DistrictCompleteness.Read`已有D及单区域选择。新例程取必要小型输入；不构造整份诊断、国内来源或第二套区域/槽位枚举。

原生分类Modifier只按GreatWorkObjectType限定，不直接按K支持的具体work type限定；**未知同类Mod作品可能误受益**，需处理到一致，不能将UI排除当成效果排除。

## 最小接口门禁及停止条件

1. **精度：** 使用真实GreatWork加值路径分别探0.5、1.5及Gold4.5；一件作品与两件作品区分逐件截断/汇总截断，确认普通城市结算。B055整数文化加值/撤销通过可以复用；B059百分比floor及科研district/per-specialist floor均不授权L2取整。
2. **资格：** 一件已支持作品与同类别未支持定义作本地/native必要对照；禁止“目录数正确但全类Modifier仍影响排除作品”。路径若无法限定，停止并报告具体primitive边界。
3. **隔离：** 同城同时配置作品native倍率与本项附加值，验证Dialogue百分比不放大追加。先静态/模拟划清attachment与origin，再给一次最小原生对照。所测Culture一类不扩大为六yield/所有theming。
4. 原生路径不满足时登记TECHNICAL_INVESTIGATION_REQUIRED；备选不同primitive可以调查，**不能自行floor、改系数、造补偿永久账本或采用整城补贴**。真正需要改Gameplay才交用户决定。

在全部门禁可表达前只做后续获授权的可逆接口probe，不宣称L2完成。此文档轮没有执行probe或本地收益测试。

## 实施切片与旧writer退出

- 第一步纯模型：同一次Shared快照→每领域D与份额→每件各yield值；记录资格/UNKNOWN，模型不用旧DialogueModel的作品时代判断。测试精度保留，不在模型提前舍入。
- 第二步原生门禁：隔离旧Adjacency，仅该probe范围由旧模块自己撤销；未通过不进行正式新旧切换。不能把探针收益与正式L2叠加。
- 第三步明确cutover：读全Mod内上述精确carrier、SQL附件、旧READ/OFF/AUTO、load/Start/Audit及AdjData消费者调用点；旧模块撤销成功后新writer施加。旧退出不确认则本城不启用新效果。carrier定义可留惰性清理ID，生成/恢复入口必须退出。
- **只退出旧GreatWorkAdjacency。** 保留旧Dialogue到M，Culture Eureka到N3，保留L1、Lv1支持/Lv2住房/GPP、科研和商业。`DialogueRefresh`是K/旧Dialogue共用producer：只在最后AdjData消费者退出后停止该投影，不能关整条巨作采集/ACK路径。
- 最后按需诊断→相关本地回归→提交；部署/测试仍等待新授权，不自动启动L3。

候选责任落在`CultureMeaningModel/Effects`或有明确职责的原模块适配，不强制新文件数量。真实影响范围：旧GWA Lua/SQL、Shared轻量读取、K通知/输出、Gameplay/modinfo、P0Panel/Text及定向测试；M仅作收益隔离接口约束，不在L2建立其永久账本。

## 更新、生命周期与回滚

事件原因：本城馆藏资格/位置、领域D/掠夺修复、ACTIVE/引用、明确失城/恢复、load。按确认事实定域更新；同一输入零写，同回合真实变化保留。无专家变化依赖，不为纯资格判断全国重算。

UNKNOWN同一可靠引用可保留最近verified配置待核对；确认空馆藏/资格失效/loss由模块owned path撤销。陌生引用和cold load不能重放旧配置。模块保存当前计划/已施加片段及有界错误，按当前城市集合替换/退出，不保存收益快照为永久成果。自身已知carrier事件精确隔离，不过滤真实建筑变动。

回滚边界为Git中的本批前已验包及部署receipt；撤销新owned effects再恢复前包，不能留下old+new。无需新增永久schema；不删除普通建筑或E2记录。运行补丁失败不会用Design变更补洞。

## 验证与退出

W0004 L2；实际触及E2/引用时补相关L3状态断言，不默认历史full/stress。

| 本地定向矩阵 | 核对 |
|---|---|
| D0/1/3/6/10、cap前后、特色/免费/掠夺/同领域多个区域 | Shared事实被忠实消费，金币份额3、同yield加总 |
| W0/1/2、同一时代多作品、支持/排除类型 | 逐件值不被再次乘件数；最终理论合计只乘一次W |
| ACTIVE3/4、UNKNOWN、两个城市、same-turn修改/重复通知 | 无串城、无变化零写、明确失效退出 |
| native-only组合与精确退休 | 旧BASE作用不残留/重建；K/旧Dialogue及Research、L1直接相关回归不破坏 |
| load/loss/return、writer错误/技术编码容量 | 按当前事实派生；失败不混合、不静默clamp或floor |

后续一个最小实机流程：同一Culture4馆藏城，选能得到半点的D领域，一件→两件→移走一件，观察原生追加及一次ACTIVE撤销/冷加载；组合隔离仅补同一城必要的native倍率对照。接口失败第一项即停。具体流程在probe包就绪时固定，不现在要求用户另做。

诊断先显示`合格W件｜每件Science/Gold…｜D来源｜预期/实际配置｜已确认/待核对`，组成分页；不以“已挂carrier”宣称原生收益通过。

Exit：精度/recipient/native-only门禁、精确cutover和本地范围通过，再由用户确认原生对应场景。当前规则已定义，技术门禁开放；未获Culture量化许可，无新决策要求用户现在回答。

来源：[Culture正式Content](../../Design/Content/Culture_D0029.json)、[Shared](../../Design/Content/Shared_D0035.json)、[总cutover合同](D0032_Implementation_Plan.md#明确的旧效果切换责任)、[旧加值实现/限制](../../Reports/Technical/Specialization_B060_GW_Adjacency_Implementation.md)、[B055整数实机范围](../../Status/Validation/Results/Specialization_B055_GW_Stable_User_Result.md)、[精度待办](Yield_Precision_Backlog.md)。
