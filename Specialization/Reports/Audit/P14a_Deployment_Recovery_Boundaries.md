# P14a — 部署事务权威与失败恢复边界

独立审计 IA20261007 / W09；slice覆盖完成，不是部署、游戏或总审计PASS。基线 `8711348a0f9cc32c51e769f3a2390992c3684a94`。只新增审计产物，工具、正式合同及运行包均未修改。

## 问题与结论

本slice回答：**main/develop与外部运行包如何在一次切换中保持来源、恢复责任及失败状态清楚；这些机制是否存在会影响后续工作的具体缺口？** 不重新核验真实运行包，也不扩展成完整部署框架审计。

常规路径具有明确的目标/UUID/链接/哈希门禁、整包暂存和恢复保护。确认一项局部缺口：稳定工具在“第一次目录rename已生效，但`moved=True`尚未执行”的可捕获中断窗口，会跳过回滚并删除pending marker。临时工具在同样注入下保留marker与`SWITCH_PENDING` receipt。两条路径的旧包均完整保留；未证明实际事故、文件丢失或信号触发概率。

**IA-P14a-F01：MEDIUM / DEFER。** 建议下一次授权使用稳定`deploy.apply`或修改该工具前定域修补；它不随新增专业放大，不需要中断当前功能开发或审计，也不授权本轮修复。当前登记的临时测试模式不能被直接等同于这个stable故障分支。

## 来源与事务责任

| 层 / 状态 | 真正负责的事实 | 不提供的保证 |
|---|---|---|
| Git main/develop | 已提交来源、分支隔离、恢复源码；工具要求对应worktree和clean | main HEAD不是当前游戏包；clean不证明已push或游戏退出 |
| source/runtime snapshot | 完整普通文件的路径/字节摘要、modinfo UUID、文件引用；复制前后再次比较 | 不证明native加载、存档兼容、原生玩法或掉电耐久性 |
| staging / backup | 独立目录内准备新包；整目录保留旧包，位于Mods之外 | 不是两次rename合成一个crash-atomic事务 |
| pending marker | 排他进入事务，记录stage/backup及切换中断线索，阻止盲目重试 | 不是自动恢复服务；F01揭示stable一个handled中断清理缺口 |
| temporary receipt | 精确stable backup、source commit/hash、阶段、恢复来源和去向 | receipt存在不证明今天仍可恢复；实际恢复还须核当前main/live/backup哈希 |
| Workflow / 操作者 | 实施/部署授权、commit/push、游戏完全退出、异常时停止并核对 | `--confirmed-game-exited`是对已核事实的声明，不是工具检测了进程 |

正式依据：[tools说明](../../../tools/README.md)、[Playtest合同](../../Architecture/Playtest_Workflow.md)。P01已记录当时source/live/stable/receipt事实；本slice没有再次读取外部config、receipt或包，不能将其升级为今天的运行包验证。

稳定源码部署与临时切换各有明确门禁。正常提交不部署；W0003持续权限仅适用于已授权实施批次，本次audit-only禁止仍优先。临时工具不支持develop→develop直接替换；现行流程要求按精确receipt先恢复stable，再启用新包。审计没有执行这些动作。

## 实际路径与恢复map

行号对应本slice基线；来源哈希保存在[复现结果](Evidence/W09/swap_interruption_result.json)。

| 路径 / 阶段 | 具体代码与已核行为 |
|---|---|
| stable：检查 | [deploy.py](../../../tools/deploy.py) 9–55：拒绝symlink、重叠路径、错误目标/UUID、重复Specialization包、pending事务、运行包独有文件；其它Mod仅只读查UUID，不删除 |
| stable：来源 | 57–77：显式授权、canonical `Mod`、main/HEAD/clean、审核过的双端hash；相同包在创建事务前返回`NO_CHANGE` |
| stable：准备 | 78–97：排他marker并fsync；stage/backup在Mods外且不与source重叠；复制后再核stage/source/target；首次rename前marker记录`SWAP_PENDING`与恢复路径 |
| stable：替换 | 98–103：target→backup，设置`moved`，stage→target；新target符合预期才清marker、返回成功 |
| stable：普通回滚 | 104–111：`moved=true`时移开失败新包、backup→target；恢复异常会在清marker前退出。**但`moved=false`分支无target恢复确认就清marker，见F01** |
| temporary：检查 | [temporary_playtest.py](../../../tools/temporary_playtest.py) 8–62：main/develop身份、target边界、双端hash、receipt外部位置。activate要求live=main且新receipt；restore要求phase/target/backup精确匹配，当前main与backup仍等于记录的stable包 |
| temporary：准备 | 63–78：先marker，再stage/三份包复核；首次rename前写`SWITCH_PENDING`或`RESTORE_PENDING` receipt及marker；记录精确backup/stage |
| temporary：完成 | 79–86：两次rename后验证新target与旧backup，写`DEVELOP_ACTIVE`或`STABLE_RESTORED`，最后清marker |
| temporary：失败 | 87–94：整包回滚，**再次核target=旧hash**才更新失败/恢复阶段并清marker；target缺失、回滚或记录写入失败时保留未完成线索，不自动宣称恢复 |
| hard termination | 不进入Python handler；首次rename前已经落下恢复路径。两次rename之间target可以暂时不存在；人工按marker/receipt核包恢复。文件系统掉电耐久性本轮未测 |

restore比较包hash而非要求main commit仍为旧SHA，因此main仅文档提交不自动使恢复失效。commit用于来源追踪，hash用于当次包完整性；两个职责不应合并。

临时CLI的`CHECK_ONLY`（108–110）仅返回快照/hash，没有运行完整branch/pending/duplicate UUID/receipt gate；apply会重新执行这些检查。不能把一次hash预览称为“所有部署门禁通过”，但当前输出也没有作此宣称。

## Confirmed finding — IA-P14a-F01

**稳定部署handled中断：实际rename结果与易失`moved`标记之间存在恢复遗漏。**

- 证据：`deploy.py:98`把`target.rename(backup)`与`moved=True`顺序执行；104–110捕获`BaseException`，只用`moved`决定是否恢复，随后无条件删除marker。`KeyboardInterrupt`属于此handler处理范围。
- 条件：第一次rename已经成功，但其后赋值尚未执行时发生可捕获异常。不是普通failpoint位置，也不是不运行handler的硬杀进程。
- 结果：target缺失、旧backup完整、异常对调用者可见，marker却消失。恢复资料中的预期hash/路径关联因此丢失；后续工具仍会因target缺失而拒绝，不会自动覆盖另一个Mod。
- 强度：**STATIC_CONFIRMED + LOCAL_STRUCTURAL_REPRODUCTION**，真实未修改工具函数及临时文件系统操作；明确注入结果窗口。未发送真实OS信号，未测发生概率、真实运行目录、磁盘故障或掉电。
- severity **MEDIUM**：错误删除事务恢复标记，增加人工核证负担；不是已毁坏数据，旧包仍可恢复。timing **DEFER**：局部于stable apply，未来增加专业不会增加修改面；下一次授权稳定部署/工具维护前宜处理。不是全项目停工或当前临时包必须回退。
- 反证：原failpoint位于`moved=True`之后，stable与temporary均正确恢复旧target并清marker；temporary同样前置中断会因target读回失败保留marker和pending receipt。

最小候选修复边界（**仅建议**）：stable异常处理依据已记录的named paths与实际target/stage/backup完整性确认恢复状态，不仅依赖`moved`；没有证明旧/新完整target恢复时不要清marker。模糊结果保留现场，不猜测、盲目重跑或自动覆盖。无需新建state machine、备份体系或跨专业重构。

未来修复验证：同一窗口、现有普通失败回滚、恢复自身失败保留marker、target与已知包hash一致、无关Mod不变。优先临时目录工具测试，不要求用户重做游戏生命周期。

## 最小复现与局限

[脚本](Evidence/W09/reproduce_swap_interruption.py)导入原工具；仅在可自动回收的`/private/tmp`夹具中创建两个文件的有效UUID包。Git admission以确定性fixture断言替代，不运行Git或CLI、不读取真实配置。`Path.rename`先调用真实rename，再在第一次target移走后注入`KeyboardInterrupt`，明确模拟结果已经生效而caller尚未赋值的窗口；不声称模拟完整OS中断时序。正常failpoint对照使用工具已有参数。

| 路径 | 注入位置 | 异常 | 最终target | marker / receipt | 旧包 |
|---|---|---|---|---|---|
| stable | `moved=True`之后的已有failpoint | RuntimeError | 旧包已恢复 | marker已清，无receipt | target hash=原包 |
| stable | 首次rename生效后、caller赋值前 | KeyboardInterrupt | 不存在 | **marker已清，无receipt** | backup hash=原包 |
| temporary | `moved=True`之后的已有failpoint | RuntimeError | 旧包已恢复 | marker已清，FAILED_ROLLED_BACK | target hash=原包 |
| temporary | 首次rename生效后、caller赋值前 | ValueError（缺target读回） | 不存在 | **marker保留，SWITCH_PENDING** | backup hash=原包 |

四个场景的无关Mod sentinel均保持；断言只支持上述结果。temporary的ValueError来自异常处理中的缺target检查，不是部署成功。临时夹具测试结束后清理，与历史/真实backup无关。结果保留相对路径、源码hash和脚本hash，不保存本机配置或凭据。

可重跑示例（从仓库根，输出到调用者指定的临时文件）：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 Specialization/Reports/Audit/Evidence/W09/reproduce_swap_interruption.py --repo "$PWD" --output /private/tmp/spc-w09-result.json
```

不依赖Lupa/游戏/外部DB。不触发部署CLI；只调用函数处理脚本自身的临时fixture。复现不是正式DeploymentTests替代品，也没有修改其断言。

## 现有验证的真实范围

两份短测试静态全文审阅，**本轮没有重新运行它们**：

- [test_deployment.py](../../../DevelopmentTests/test_deployment.py) 12–17使用临时包与真实临时Git；18–51检查授权/branch/dirty、duplicate UUID、no-op、hash拒绝、普通异常整包回滚、正常替换/备份、未知runtime文件、手写pending拒绝、symlink/UUID和无关Mod隔离。34–36 failpoint在赋值之后，不能覆盖F01。
- [test_temporary_playtest.py](../../../DevelopmentTests/test_temporary_playtest.py) 11–21为独立临时main/develop包；23–37覆盖缺授权、activate普通失败回滚、正常activate/restore、未知runtime修改拒绝、develop-only清除与stable backup保留。它没有单独断言失败receipt阶段；本轮复现给出该窄观察。
- 未覆盖：restore故障注入、receipt写入失败、rollback失败、并发外部写入、掉电/权限变化及真实人工恢复。这些未测不自动构成新defect；发生相关工具修改时按具体风险补最小测试，不补全巨大故障矩阵求“全绿”。

## 保留机制、导航边界与未决

- **NO_ACTION**：exact target/UUID、路径隔离、运行额外文件拒绝、两端/暂存hash复核、整包备份、临时receipt精确恢复与unrelated Mods保护，均有独立职责；Git不能替代外部包恢复。
- **NO_ACTION（有范围）**：Git clean不纳入ignored文件，而snapshot/copy纳入全部普通文件。故commit身份不能独自证明包全部来自tracked HEAD；但额外文件仍进入审核hash并再次校验。没有发现当前包含此类内容，不报告“未审核字节绕过”。
- **已知限制**：完整rollback包保留、bounded retention尚未实现，tools README与W0004 v2已明示。不是本轮新发现，不自动清理或删除历史备份。
- **IA-P01-Q03补证，原LOW/DEFER保持**：Playtest合同仍含旧“本阶段不进行develop实机”“当前长玩包不变”，但W0003前置段明确覆盖旧权限文案。属于已登记导航风险；结合CURRENT/Authority可确定当前边界，不据此推导实际违规部署。工具README也引用较旧W0002名称，本轮不改正式合同。
- **NOT_YET_AUDITED**：当下外部运行包/backup/receipt可恢复性、OS真实中断/掉电耐久性、任意并行写入、完整部署历史与promotion流程执行。没有新增部署/native PASS，不重开性能专项或B168待办。

## 实际阅读与续接

主任务及三路独立只读复核覆盖：`deploy.py`全128行、`temporary_playtest.py`全114行、两份测试全52/38行、tools README全35行、Playtest Workflow全66行；根/项目AGENTS、项目入口、Workflow启动/恢复段、Authority/Status真正CURRENT及ledger/P01直接部署证据。子审阅另核`.gitignore`和Tests README相关fixture说明。没有通读Mod、历史报告、运行包或私人配置。

本slice问题已收束，P14a覆盖完成不等于整个P14或总审计完成。下一逻辑问题：**P07a投资事务：永久receipt、Potential提交与单位消耗之间的权威/失败边界**。

准确入口：`Mod/InvestmentAction.lua`、`Mod/UnitActions.lua`，沿其调用进入`CityProgressionStore`的投资读写/receipt/consume接口；复用P06a已核root/record/保存/unique reference结论，不重扫Store。直接测试从`DevelopmentTests/test_investment_store_bridge.py`、`test_settler_investment_executor.py`、`test_native_investment.py`按实际call site选择；必要时复用B108多城fixture，完整Claim/1T项目另作P07b。先回答事务阶段、重复请求、消耗前后错误与Owner/UNKNOWN对正在提交事务的影响，不重做逐能力save/load。以上文件本轮仅确认存在，未开始读取下一slice。
