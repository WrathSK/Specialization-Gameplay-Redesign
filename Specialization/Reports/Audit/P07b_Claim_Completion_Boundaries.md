# P07b — Claim / 完整1T项目完成事务

独立审计 IA20261007 / W11；基线 `9904a9718c145388c095b71f474a0b6c8bc41ed0`。slice覆盖完成，不是总审计或新增native PASS；仅保存审计产物。

## 问题与结果

本slice回答：**正式Claim的持久计时、原生完成事件、身份提交与退出调度是否有清楚权威；未来完整1T永久奖励项目能继承哪些工程合同？** 不重测UI风格、所有砍树/溢出组合或其它能力。

正常路径明确：先持久CALLING，成功才调用原生FinishProgress；真实完成事件独立验资格，一次保存Identity/P1/receipt；调用返回和项目消失都不能单独发身份。持久Claim与session-only实验项目各自拥有精确项目ID，没有两个writer同时完成正式Claim。

新confirmed finding **IA-P07b-F01：LOW / DEFER**：原专业候选城夺回后再失城时，Claim退出用历史origin CityID清会话集合，可能留下当前旧CityID活动条目，反复进行失败lookup。永久timer和marker正确退出，无重复认领/收益；应在相关调度维护或复用前修补，不作为全项目阻塞。

条件边界 **IA-P07b-Q01：MEDIUM / MONITOR**：CALLING之后原生完成、最终身份写失败，coldboot仍CALLING/NONE且不自动重调；新的合法完成事件可以恢复，但系统没有持久保存先前完成事件供重试。既有合同明确未知结果停止，不能把它写成新的玩家事故或允许猜成功。

## 正式合同与证据范围

[Spec PROG-006至009](../../Design/Specialization_v0.1_Design_Spec.md)定义冻结候选、显式Claim、完成才建Identity/P1；[E2正式1T合同](../../Architecture/v2/P0_E2_Plan.md)973–1000、1043–1049、1195–1199、1229–1235规定完整回合、唯一队列、CALLING未知不重调、易主清计时、读档不从队列补BEGIN、current请求/origin receipt与有界ACK。

自然极端生产或Cheat真正完成可同回合认领，已经接受。**无timer完成事件不是授权绕过缺陷**；未来Dialogue/Study必须核各自规则，不能直接复制此例外。

现有原生依据：[B123项目原语](../../Status/Validation/Results/Specialization_B123_Project_Pass.md)是用户陈述的正常1T/所测砍树不溢出；[B126主流程](../../Status/Validation/Results/Specialization_B126_Claim_Core_Pass.md)与[B129商业夺回读档续接](../../Status/Validation/Results/Specialization_B129_Claim_Reload_Pass.md)各保留场景/陈述/截图边界。本轮只读记录，未重看原图，不新要求重复验收，也不外推所有资源/四专业/中途写失败均通过。

## Ownership / completion map

| 状态或事实 | 唯一权威及职责 |
|---|---|
| frozen LegacySet、UNASSIGNED、Identity/P1 | Store逐城Game record；Claim只请求合法转换，普通区域新增不改set |
| claimTimer | 同record version1：token、current reference、project/kind、start、deactivated、ACTIVE/CALLING/STOPPED；UI不保存玩法计时 |
| claim receipt | 同record一次提交，锚定origin；活动请求与timer用current，不把历史origin当当前endpoint |
| 当前队列/完成事件 | engine；Gameplay校当前project与size，缺GetSize时用明确UI供应器核owner/id/turn/project/size；未知不当成功 |
| active/dirty/errors/views/derived/syncAck | Claim会话调度/展示；不是永久权威。成功发布、退出与重建有各自责任；F01为其中一个清理key错误 |
| UI pending/synced/ACK | 明确选择、确认当前队列后发BEGIN；WarmStart发SYNC最多3次；ACK只表示调用返回，不证明timer或认领成功 |
| TimedProject实验 | 单城市session计时、used/inCall、target退出观察；无持久Identity/奖励，不替代正式receipt |

源码：[ClaimProjects](../../../Mod/ClaimProjects.lua)、[Store](../../../Mod/CityProgressionStore.lua)、[TimedProject](../../../Mod/TimedProject.lua)、[UI桥接](../../../Mod/UI/ClaimProjectUI.lua)。[精确项目SQL](../../../Mod/Data/ClaimProjects.sql)只有四个cost1,000,000零原生奖励项目与四个InternalOnly访问marker；这是已接受技术容器，不是玩家等待百万生产。

| 真实步骤 | 正常/失败与恢复 |
|---|---|
| Claim100–117 BEGIN | 冻结候选、当回合、唯一当前project、FinishProgress capability；同ACTIVE同项目重发不写，CALLING禁止再开始 |
| Claim161–162结束确认 | 保存deactivated；未确认完整回合不能结算 |
| Claim163–168下一回合 | 恰好start+1且deactivated与队列匹配→保存CALLING→FinishProgress；latch写失败零原生调用 |
| Claim139–150完成callback | 精确project/current资格/完整唯一对应区域；Store完成true才排derived；允许同步reentry，不主动Flush |
| Store334–349提交 | 同record写Identity/P1、first、origin receipt，清timer；readback后永久写hook；重复receipt=false，不重复写 |
| Claim74–90派生 | 先dirty审计，再按player派生；每consumer独立pcall，Identity不因收益失败回滚。失败日志不等于具名pending ACK |
| load/Sync | 重新建访问/活动集合，只结算已保存的due ACTIVE；不从队列猜启动、不重调CALLING |
| loss/return | Store600清timer；exact module marker退出；原候选保留，返回必须重选新timer/current，不重放中断计时 |

prototype与正式项目在Gameplay启动/请求分离（56–65、795–818）。原型target退出观察没有奖励，因此不能宣称它已证明未来永久奖励的 exactly-once。

## Confirmed — IA-P07b-F01

**夺回后的第二次失城清理了历史key，遗漏当前活动key。**

1. Store583保存`current.cityID`，origin保持首次记录端点。
2. Claim36/58以`pid:currentID`维护active。
3. Store600–602第二次loss清timer，但`loss.origin=cp(root.origin)`。
4. Claim206按`loss.origin.cityID`清active/dirty/view；foreign CityTransfered经mark被拒绝，不排旧currentID。
5. 下一玩家turn154–156复制残留active并找已失城市；safe69–72仅覆盖error/STOPPED view，不剪active。所以该条目继续参加activation/deactivation。

真实未修改Lua的最小fixture：origin1101→可靠原binding返回current500→新ACTIVE timer→再次失城。持久timer=nil、marker0，但active500仍1；3次activation实际测得FindID(500)失败3次，这3次activation区间额外Store写/原生完成均0。显式旧key dirty+Flush剪除后，再activation lookup0；这里只核active剪除，没有证明errors或全部UI历史key也被清。

**LOW / DEFER。** 已核当前合法生命周期的会话退出错误；未测native耗时/内存，不称已卡顿、无界原生泄漏或资产损坏。现在调整面限Claim退出/缓存key；未来重复照抄到多个1T项目会增加维护面。建议在此调度维护/新增项目复用前对齐departing current endpoint与historical origin语义，不造新的cityKey或统一Gameplay继承规则。

强反证：第一次loss的origin=current正确；额外旧key dirty可清；冷Start清session；timer与marker真实退出，不再Finish；同STOPPED文本不不断增view revision。这里保留的是历史ID会话工作，不是永久历史应被删。

hot-path口径：每activation/deactivation复制O(A)活动表；残留H个key增加O(H)失败lookup/异常字符串构造。真实H频率、20–40城native成本未测，不把3次fixture查询转换成进程内存归因或全城扫描次数。

## Provisional — IA-P07b-Q01

CALLING是**调用意图**，当前没有另存“真实完成已经观察、业务待提交”的阶段。若q完成并回调，最终Store写未成功，旧Game record仍CALLING。coldboot/Sync/BEGIN保持未知且不重调；新的独立合法CityProjectCompleted仍能提交。

| 临时注入 / 对照 | boot前原生调用 | boot后累计 | boot后业务 | 结论 |
|---|---:|---:|---|---|
| 正常 | 1 | 1 | RESEARCH/receipt | 不重复完成 |
| CALLING写失败 | 0 | 1 | RESEARCH/receipt | 没有先调用；合法due ACTIVE可恢复 |
| 最终Identity写失败 | 1 | 1 | NONE/CALLING | 不猜成功，不自动重调；补一条新合法完成事件后可提交 |

**MEDIUM / MONITOR，非confirmed事故。** E2原合同明确锁存未知结果不重试、保存失败暂停。此处补齐联合场景证据，不据此删除保护或要求现在搭通用transaction engine。未来永久奖励项目需明确真实完成证明、业务receipt、失败后的核证与重试owner；只有具体失败或新consumer依赖此保证时升级定域动作。不把CALLING当已经完成，也不默认以queue消失重发奖励。

[复现脚本](Evidence/W11/reproduce_claim_boundaries.py)／[原始JSON](Evidence/W11/claim_boundary_result.json)共3完成场景及1退出场景，复用W03/B111/B124声明，未执行旧case。existing Lupa Lua5.5；native队列/Property/Events是mock，FinishProgress同步发完成事件。debug仅观察既有active upvalue，FindID wrapper只计调用，不改业务代码。没有真实存档序列化、跨context原生调用、OS故障或实际用户事故证据。

## 扩展合同与既有finding补证

不建议为DRY合并prototype、Claim、投资的不同成功凭据。未来模块可复用的是小型工程职责：明确timer/当前reference owner；原生调用前锁存；完成事件独立合法验证；业务结果与receipt同record提交；commit后dirty/derive及退出失败责任明确。额度、START-era、收益、owner归属仍按各专业合同。

- Claim手列consumer名单补证IA-P13a-F03，原MEDIUM/FIX_BEFORE_NEXT_PROFESSION保持；首Claim只有P1，不因未唤醒所有高级consumer制造遗漏。
- Store业务耦合补证IA-P06a-F03；exact Claim接口不是通用项目状态机。
- call-wide inCall/commit-hook逃逸是条件接口提醒，当前没有native nested publish或现行hook抛错证据，沿用P06a/P09 MONITOR；不新造重复finding。
- queue跨contextfallback guard完整，但当前B124始终GetSize成功，UI测试手填backend；它们不能联合证明真实调用/迟到读数。缺具体异常时不新增人测或全套fallback重验。

## 已有测试与覆盖限制

三路只读审阅，正式测试本轮未跑：B124执行实际Claim/Store，同步Finish回调、双城、保存、重复、改选、loss/UNKNOWN、CALLING无事件及无timer完成写失败均有断言；B127/B129恢复/ACK/B128返回各有范围。它们没有组合覆盖CALLING＋同步完成＋Identity写失败；本轮最小注入补这条，不改断言。

B127 missed-load新建Claim并fixture取消重复exit注册，保留Store/旧event环境；B124 boot重建事件/shared但保留内存props/q；这些不是native冷进程。B129 UI包收集/手填views/ACK不代替Gameplay联合路径。正常用户B126/B129场景可继承，不能要求再每能力重复保存/冷启。

实际读取：Claim/TimedProject/ClaimProjectUI全文，Store timer/Claim/loss/current/return具名段；Gameplay startup/dispatch、SQL精确四项目；六份Claim定域测试与直接helper/当前反证片段；E2上述完整相关条款，Spec PROG及B123/B126/B129结果。没有通读所有B12x、全部Mod/历史或截图；截断搜索不计完整阅读。

## 续接

P07b问题收束；P07整体尚未完成。下一 **P07c施工队：来源绑定、当前Owner容量、单位消耗与原生生产注入的receipt**。从`Mod/UnitActions.lua` CREW分支、`Mod/CrewProjects.lua`、`Mod/CrewPrecision.lua`、`Mod/ConstructionProbe.lua`具名队列读写进入，核当前D0045/D0044规则与已落地旧路径区别；定域测试从crew_unit_actions/crew_projects/crew_precision按真实调用选，不全跑旧wrapper。先核native grant不重放与保存权威、队来源归属/退出、当前旧实现与新设计的deferred边界；不实施成本/层级新规则。不发新实机任务。
