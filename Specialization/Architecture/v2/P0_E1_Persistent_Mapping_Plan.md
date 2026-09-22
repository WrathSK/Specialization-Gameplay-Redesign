# P0-E1 收尾计划：单城持久身份映射

Status: IMPLEMENTATION_COMPLETE_AWAITING_USER — 用户已授权，B093.120单城实验LOCAL_SIMULATION_PASS；原生自动保存/冷恢复待验证。下方为获准计划。
Baseline: B092.119 / modinfo119，源码cbf99b38894621fa345d68bb2ae4ba7df2b409be；Design D0035 / Architecture A0161。四专业范围不变。

## 1. 证据与剩余问题

- B088 USER_GAME_TEST：分城转自由城市后旧City Properties缺失，不能依赖其自动继承。
- B090 USER_GAME_TEST：独立Game实验记录在转移及冷读档后保留。
- B092 USER_GAME_TEST：T8单次0/131073→62/65536，Gameplay6条事件足以给出SHADOW_CANDIDATE；UI仅独立佐证，不需要新跨context桥。
- 以上不等于“已持久映射且可冷恢复”。B092的shadow没有保存，旧state HELD是getter判断。下一步只闭合这个缺口，不重新测试已经确认的getter或UI接口。

当前实现已读取：CityIdentityExperiment、CityIdentityRead、CityInheritanceRead及E1合同。保持W0001复用其它未变源码；正式实施前按manifest读精确写入点，不重审四专业全部实现。

## 2. 推荐范围与保存位置

在现有单城实验模块内增加小型schema2映射实验，不建通用事务框架、不启动全城登记。不使用外部文件：Game Property随游戏存档保存；外部文件无法可靠跟随加载较早存档/不同战局。城市名只用于显示，改名不影响身份，同名不建立关系。坐标用于定位，不独立证明同一城市。

拟用独立key `SPC_E1_IDENTITY_MAPPING_EXPERIMENT_V2`，只容纳一条记录。现有V1 key只读保留，不自动升级、覆盖或删除。新实验必须从具有完整原范围凭据的己方城显式启用；当前转移后已缺凭据的城市不能靠旧截图补建权威。

| 字段 | 用途 / 约束 |
|---|---|
| schema, revision, experiment | schema2、单调修订、ONE_CITY_MAPPING_ONLY；不被正式consumer读取 |
| candidateKey | 本存档单城实验命名空间中的固定身份候选，不冒充正式全局cityKey，不用城市名或owner:id生成后续身份 |
| requester, originRef, originToken | 原启用者、原owner/id/x/y与已验证DEV凭据；固定证据，不改原绑定 |
| currentRef, mappingState | 当前owner/id/x/y；ORIGIN_VERIFIED / TRANSFER_PENDING / MAPPED_EXPERIMENT / HELD；不同于专业Identity |
| transition | 至多一个：from/to引用、turn、证据类型、所需事件摘要、完成/冲突状态；无历史数组 |
| revision/readback | 保存前校验当前记录未被改写，保存后读回核对；失败停止，不无限重试 |

candidateKey只说明这条实验记录的连续性。它不授予Current Identity、Potential、History、模板、投资凭据或任何收益。generation无法独立证明时标明未知；不得把这个实验编号称为已经解决夷平再建的永久身份。

## 3. 事件与写入合同

1. 显式启用一次，验证原范围旧账本只读Preview，然后保存起点。加载恢复一次；无需再点击按钮开启监听。
2. 只接收观察城市相关事件，复用固定16条去重缓冲及B092证据组合。CityBuilt本身不判新城；实际已确认的Built→Removed→Added→Initialized→Converted→Transfered顺序可处理。
3. 第一次相关变化将实验标为TRANSFER_PENDING，旧已验证引用保留为fromRef，不向外提供新有效映射。相关事件到达后重新评估；证据完整时保存MAPPED_EXPERIMENT与toRef。每个逻辑状态变化最多一次写入，重复事件不写；没有timer/全图扫描/通用Publish轮询。
4. 同一转移的迟到补充通知不重复提交。后续冲突、额外移除/多个新引用/第二次转移使记录转HELD；不得仅因曾成功配对而忽略后来反证。单次实验不推进第二段链。
5. 原生事件回调中的对象暂不可用，保留pending，等待下一相关事件或手动按需核对；不采用帧级retry。写入失败锁定本次会话，禁止自动修补。事件到达前保存/引擎崩溃等未观察窗口不承诺恢复。
6. 冷加载MAPPED_EXPERIMENT时核对保存引用、当前位置对象及schema；一致显示“已保存映射恢复”，不是靠位置重新推导身份。不重放旧事件生成新映射。不一致、pending或损坏则HELD；缺记录显示未启用，不自动创造空历史。
7. 保存状态只有实验意义；UI截图和getter只诊断，不是提交authority。不恢复旧CityInheritance/InheritanceShadow。

这些写入只作用于新的实验key。普通诊断读取不制造重复修订；显式核对若补齐尚待确认对象，只执行同一个幂等评估器。

## 4. 支持矩阵 / E1退出边界

| 场景 | 本批目标 |
|---|---|
| 原范围显式登记、改名、原引用读档 | 候选key保持；不依赖显示名 |
| 已证实的单次自由城市转移、随后另存冷加载 | 事件完成自动保存，加载恢复同一候选；需一次原生闭环验证 |
| 无证据、缓冲超限、写入失败、schema损坏 | HELD，旧专业记录不变；只读诊断可解释 |
| 加载在转移尚未完成时 | 保留pending/HELD，不跨load拼凑旧事件成新证明 |
| 第二次转移、收复、赠送、解放、原生征服 | 本批不承诺MAPPED；定向模型验证拒绝/暂停，未来按具体所需路径逐步验证 |
| 夷平/同地重建/引用复用 | 有矛盾即拒绝；未观察到的同引用再生不能由位置证明，明确未支持 |

E1本轮可达到“持久单次转移映射原型PASS”，不能标普遍永久身份PASS。E2开始前必须另行审阅其支持存档范围及未支持易主如何安全停止旧/新writer；不能把原型门禁通过自动解释为E2已获实施授权。无需为了这一个实验立即要求用户做所有征服/重建组合。

## 5. 旧账本与未来cutover边界

本批绝不写Binding、Journal、Flow、Investment、Standardization keys，不迁移现有专业进度，不改任何carrier。City Properties在易主后丢失的旧数据也不补回。

未来E2必须在旧对象尚可读时建立有来源的持久专业记录，逐模块定义保存/切换；identity映射本身不能恢复已经丢失的账本。不从carrier、现有建筑或截图反推历史。旧档无法证明的数据继续UNKNOWN；是否只支持新测试档须在E2计划明确，不在本批擅自宣布全部兼容。每种专业Legacy独立，确认同一座城不等于新Owner继承成果。

## 6. 文件与验证

预期修改CityIdentityExperiment.lua、相应按需diagnostic/必要Localization、modinfo与定向测试；优先复用现有按钮。旧writer/收益SQL/Design/UI布局保持。若须改正式读取链，停止扩展并报告。

W0004 L3，但仅相关验证：真实Lua保存/加载模型、重复事件零重复提交、实际B092顺序与合理乱序/缺事件、保存前后冲突、迟到反证、第二次转移、pending冷加载、无效schema/读回失败、无City Property写和旧writer未启动。验证监听在加载后自动恢复、不依赖诊断开启。syntax/modinfo/context与部署工具完整性按惯例；不默认运行历史全回归。固定缓冲/大量重复通知只验证本模块幂等与有界性。

## 7. 一次最小实机闭环（实施后才安排）

使用独立的转移前测试存档：显式启用一座己方分城的映射实验→转为自由城市→**不点击转移后诊断，先另存并冷加载**→点击实验对照一次，截图。

报告直接给：候选编号保持、已保存映射恢复/暂停原因、原Owner→现Owner、专业迁移未执行。详情按需；不默认打印6条原始事件、4个getter或整份账本。这个顺序验证事件自动保存，而不是点击报告才保存。无需再重复左右键四图。

若不能正常自由城转移或加载，报告具体失败，不要求继续大量操作。现有B092截图不冒充该新闭环PASS。

## 8. 交付 / 回滚 / 下一步

本次仅计划文档，无runtime/build变化、无部署。后续获准实施后commit/push，再按W0003退出与部署事务门禁处理；不启动游戏。

运行包回滚B092及新实验前独立存档。新V2 key不影响旧程序，旧包会忽略它；回滚不自动清除存档里的新key，不声称引擎状态被逆转。

用户需要的下一项授权：**实施E1单城持久映射实验**。验证通过后提交E1支持范围结论和E2具体计划，不自动迁移，不启动F学术传统。

## B093.120 实施记录

新增`Mod/CityIdentityMapping.lua`；Gameplay保留旧实验纯Shadow函数但不启动V1 writer，转而启动V2单城模块。V1保存记录不读写、不迁移；旧专业writer及InheritanceIsolation保持。新key `SPC_E1_IDENTITY_MAPPING_EXPERIMENT_V2`，只存单条实验候选编号、原/现引用、修订与最多16条单次证据；编号不等于正式cityKey。无新收益、carrier或专业迁移。

开启一次写ORIGIN_VERIFIED；首个相关变化写TRANSFER_PENDING；证据完整自动写MAPPED_EXPERIMENT。典型完整流程共3次新key写入，之后重复/正常同回合迟到通知不写。额外变化转HELD一次。冷加载立即恢复监听，不依赖诊断或LoadScreenClose必达；pending冷加载停止、不重放证据。对象暂不可读只报告未核对，不伪造失效；引用确实冲突停止。已有保存证据仅校验已提交记录，不作为新转移输入。

诊断复用右键“记录城市身份”启用、左键“实验对照”读取；右键对照仍是旧V1/UI观察，不是本轮验收入口。摘要只给是否恢复、候选编号、Owner变化、修订及对象一致性。旧V1记录不妨碍在同一转移前档建立V2，但必须当前旧凭据完整。

LOCAL_SIMULATION_PASS（实际Lua，非Civ VI实机）：自动保存/不点诊断即冷加载、加载监听、原引用恢复、实际B092事件顺序和匹配逆序、迟到初始化、临时对象不可读、pending冷加载、缺证据/跨回合/错误Owner/额外移除/第二次转移/征服解放暂停、坏schema/篡改记录/写后读回失败停止。10,000次重复通知无新增写入，证据固定上限16。所有Lua语法、modinfo120及文件清单检查通过。与d81623f相比旧writer/Design逐字节不变。旧V1功能、实际UI分发和共享Shadow定向回归通过（历史版本断言不沿用，由新测试单独检查120）。部署工具临时目录回滚/恢复测试通过；无历史全量Gameplay回归。

实现边界：仅实验单段；同回合完全相同事件无法区分“重复通知”与不可观察的同引用再生。未观察窗口/跨次转移/征服/解放不获通用身份保证。新模块没有UI请求、timer、通用pulse监听或全城扫描。事件只查询观察位置、写有变化的独立Game记录。

用户测试：**转移前独立档→选己方分城→右键记录城市身份→转自由城市→不点诊断，另存并冷加载→左键实验对照截图。** 预期“已保存映射恢复”，Owner发生变化、当前对象一致。无需左右键四图，不要求测试专业继承。存档含V2只是实验，不作为长局迁移承诺。测试后停止，不自动进入E2/F。

B093 W0003部署：源码`fc43df158ace9be4e5d7cc674210d96ee79f186b`；OS确认游戏退出，151/151文件hash一致；B092完整恢复包及stable恢复点保留并核验。Receipt：`SpecializationDeploymentBackups/B093.120-fc43df1-playtest.json`。main未改，未启动游戏。

## B094.121 — 授权事件入口修复

针对B093截图函数调用错误，移除新包装器table.unpack依赖，直接pcall(fn,...)传参；未初始化/未登记/已暂停事件提前返回。guard显示加载、登记、事件名或核对阶段，仍无逐事件日志。身份判定、schema2、独立key和专业账本隔离不变。B093原生具体nil调用点尚未确认，故这是针对已复现缺陷的修复，不冒充实机根因已完全证明。

LOCAL_SIMULATION_PASS：现有实际Lua映射/保存/冷加载/冲突回归，外加table.unpack及全局unpack均缺失时的未启用无关事件、登记→转移→冷恢复；四种故障阶段提示。旧writer/Design字节保护、全部Lua语法、modinfo121及清单通过。未跑无关历史全回归。

最小用户测试不变：转移前独立档，右键记录城市身份→转自由城→不点诊断先另存读档→左键实验对照一张截图。若再次暂停，阶段名用于定位，不要求继续操作。等待USER_GAME_TEST，E2/F不开放。

B094 W0003部署：源码`a113a6096e141112a5a7ef67453afd8cdc00ac3c`，OS确认退出，151/151文件hash一致；B093/stable完整恢复点核验。Receipt `SpecializationDeploymentBackups/B094.121-a113a60-playtest.json`。main未改，无游戏启动。
