# D0007：参与资格、永久成果与休眠的离线分离

Document Owner: Codex
Design Reference: D0007 / ELIG-001..006, PROG-004, COMPAT-001
Architecture Reference: A0024
Implementation Scope: MOCK_ONLY / NOT_DEPLOYED

## 结果与证据

LOCAL_SIMULATION_PASS：本地模拟通过，不等于Civ VI实机通过。新增资格测试与城市状态、写入计划、完成日志、D0005模型四组回归均exit=0。实际B015运行包、Design逐文件hash保持；无新游戏结果，无新实机批次。当前验证矩阵和后续队列只由[Status](../../Status/Specialization_P0_Status.md)维护。

规则只引用[Accepted Design](../../Design/Specialization_v0.1_Design_Spec.md)，本报告描述实现契约，不另建游戏数值权威。

## 实现接口

- `PlayerEligibility.Resolve(snapshot, player)`消费显式MOCK_ONLY、COMPLETE参与者配置，返回ENABLED / DISABLED / UNKNOWN。缺失记录、非法player、部分配置均不启用；不根据Human、文明、领袖或已存专业推断资格。这个snapshot是本地输入，不是UI商路快照，也不是已经发现的游戏API。
- `Dispatch(snapshot, visit)`仅向enabled玩家调用昂贵工作的入口，按player编号确定本地调用顺序。测试计数确认disabled/unknown不收到回调；没有接入真实城市/网络循环，不宣称已验证实际性能或多人确定性。
- `CitySpecializationState`删除固定测试文明身份要求。`Participation(id)`独立验证当前owner与显式资格；真实适配器将来必须即时读取资格，不能永久复用旧ENABLED结果。
- `Restore`和验证同城后的`TransferOwnership`只读取/复制永久事实，不以启用资格为前提，也不授予效果。owner变更仍需显式MOCK同城凭据，不能冒充跨owner永久UID已解决。
- `NewCity / Complete / PlanInvestment / CommitInvestment`先检查enabled。`Derive`遇disabled返回DORMANT、active=0、effectsEnabled=false，unknown返回UNKNOWN且不启用；两个分支在读取城市事实和总督输入前返回。这个0不是修改Potential或增加Lv0。
- `AcquireUnassigned`为取得城市单独提供离线入口：要求`VERIFIED_NEVER_ENABLED_NO_FACTS`及同城/fromOwner/toOwner证据，不伪造新建城通知，不扫描已有区域推专业；有现存事实必须走保留路径。证据获取方式尚未实现，Property为空不能生成该凭据。
- `CityCompletionJournal`的Foundation、Complete（含重复通知）、Gap及`CityFactWritePlan`写入入口也先门控，避免上层绕过。只读Restore保留。未新增实际Property写入。
- 旧档缺失事实在该状态模型返回`UNKNOWN / OLD_SAVE_COMPATIBILITY_REQUIRED`，不再冒充玩法待决。旧身份/绑定实验未整体改造，其历史状态名称不能充当D0007正式契约。

## 本地检查覆盖

1. 不同文明标记下enabled人类与AI得到同样的专业/Potential；不按Human过滤。
2. disabled/unknown不会建立或追加成果；不可读取的事实/总督输入仍被提前跳过。
3. 有成果转给disabled保留Potential、投资凭据、自有模板，ACTIVE完全停用；恢复到enabled按新总督上限重算。enabled间转移也保留，原输入不变。
4. 从未启用且无成果的取得证据形成未专业化事实；空Property、错误owner、已有成果不被误当成该证据。后续合法完成可锁定专业。
5. 重复Foundation、完成及Gap不会绕过资格；只读恢复不因休眠被拒绝。
6. 配置不完整不调度；disabled/unknown不进入模拟工作回调；资格变化后用新配置重新筛选。
7. JSON保存后创建新Lua VM，休眠事实恢复，再启用时按当前总督计算；永久Potential和模板不变。
8. 四组既有回归保留完成顺序、账本防重复、投资上限、历史缺口、首都自接入及工业分项合并检查。

## 未完成的实际接入边界

- 未确定真实启用资格carrier，也没有从实际Game对象产生上述MOCK凭据。
- 未接入真实征服/丢城/重载事件、跨owner同城识别、首次取得历史证据或未专业化取得的Journal历史资格。AcquireUnassigned只是状态层入口，不能直接连到Property写入。
- 尚无正式收益，所以没有附着Modifier可供撤销；本地active=0不等于游戏内已撤销旧收益。未来停用必须移除已有运行效果并阻止缓存继续结算。
- NetworkState/NetworkStrength/IndustryNetwork和旧身份/绑定实验尚未全面接入统一资格门控；生产接入前必须覆盖所有入口。Dispatch回调测试不代表这些模块已完成适配。
- 当前独立B015仍用固定测试载体探针，不提高其证据等级；无新实机测试，B010继续延后。

上述是IMPLEMENTATION_PENDING / IMPLEMENTATION_LIMITATION，不要求改变Design，也不重开已经确认的AI与征服规则。

## 文件与审计

新增PlayerEligibility.lua、test_player_eligibility.py；修改CitySpecializationState.lua、CityCompletionJournal.lua、CityFactWritePlan.lua及四组既有测试的资格fixture/旧档预期。均位于DevelopmentTests，未注册modinfo。

修改前文件备份及Design/运行保护hash见`DevelopmentBackups/Specialization-before-D0007-eligibility-model/`；本轮执行输出、最终修改hash与保护核对见该目录新增`verification_result.json`。没有改UUID、游戏配置、运行源码或Design；没有启动Civ VI。
