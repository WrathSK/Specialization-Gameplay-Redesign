# 区域完成与城市事实接入研究

Document Owner: Codex
Design Rule ID: PROG-001至004 / ID-002
Architecture Revision: A0006
Runtime Build: P0-B-010 / modinfo17 (UNCHANGED)

## 本轮结论

STATIC_CONFIRMED：官方和HD的Gameplay使用GameEvents.OnDistrictConstructed(playerID, districtType, x, y)；第二参数为区域类型，不是district实例ID。GameEvents.CityBuilt有官方/HD Gameplay先例。可作为下一轮只读探针的有根据候选，但事件读档重放、对象就绪、建造/修复/征服时序尚未由用户验证。

LOCAL_SIMULATION_PASS：新增区域族解析及完成候选分类通过真实缓存数据库与Lua模拟。没有游戏事件注册、Property写入、UID生成、真实单位消费或新游戏测试结果。

## 本机源码证据

游戏Assets根：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/common/Sid Meier's Civilization VI/Civ6.app/Contents/Assets`。
HD根：`/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070`。

- 官方DLC/BlackDeathScenario/Scripts/BlackDeathScenario.lua:56/63注册CityBuilt与OnDistrictConstructed；255/429为回调定义。场景modinfo通过AddGameplayScripts加载。429以下的某个分支有参数名与使用变量不一致的原码，不能直接复制为可靠对象解析实现。
- 官方DLC/NubiaScenario/Scripts/NubiaScenario.lua:971–986用区域类型判断圣地建成；不提供完整实例ID/存档时序契约。
- HD Gameplay/CivilizationTraits.lua:2945–2959的德川区域完成回调按区域类型判断；Gameplay/Misc.lua:164及765注册CityBuilt。
- HD Gameplay/HD_Common.lua:182–199通过district:IsComplete()检查完成，但同时对IsPillaged返回false。这个helper表达当前可用性，不宜直接替代首次完成事实。
- HD Gameplay/HD_Common.lua:552–570用DistrictReplaces定位通用区域。本模块独立解析替代链，不依赖TraitType非空；链循环、缺失端点或冲突定义拒绝，不猜类型。
- HD Gameplay/CityYield.lua:46/102与161/171有table型城市Property读取/写回先例；DL.modinfo的AddGameplayScripts加载CityYield。现有Specialization Gameplay.lua:48–54仅marker读写，并非专业账本。

## 数据库与区域族

以本机DebugGameplay.sqlite只读读取Districts和DistrictReplaces，得到36个区域、16条替代关系；其中10个类型落在v0.1四族：

| 族 | 缓存中的类型 |
|---|---|
| CAMPUS | DISTRICT_CAMPUS、DISTRICT_SEOWON、DISTRICT_OBSERVATORY |
| THEATER_SQUARE | DISTRICT_THEATER、DISTRICT_ACROPOLIS |
| INDUSTRIAL_ZONE | DISTRICT_INDUSTRIAL_ZONE、DISTRICT_HANSA、DISTRICT_OPPIDUM |
| COMMERCIAL_HUB | DISTRICT_COMMERCIAL_HUB、DISTRICT_SUGUBA |

这是当前缓存内容，不是承诺未来任何Mod组合都是这张表。未来每次加载应从当局GameInfo建立映射，不持久保存Index或硬编码全部替代类型。原生事件索引必须先由GameInfo.Districts解析成Type，再到本模块归族。未列入数据库的类型UNKNOWN，数据库已知但不属于四族的类型NON_V01；这只表示当前范围外，不否定Future设计。

## 接入方案与未证明部分

1. CityBuilt作为新城观察候选，核对测试文明、当前owner/cityID/坐标。不能仅凭CityAddedToMap或CityInitialized建立freshFoundationObserved，因为它们不是已证明只在建城时触发的事实。实际事件是否读档重放/征服触发仍需日志。
2. OnDistrictConstructed提供通知；再只读解析当前位置的区域实例与所属城市，核对owner/type/位置和IsComplete。通知与对象不一致时记录UNKNOWN，不锁定。
3. 已建立有效城市身份与事实账本后，事件适配才能提供CitySpecializationState所需完整有序批次；候选通知本身不构成首个完成历史。跨事件同时完成如何排序依OPEN-04，不用回调先后默认解决。
4. Property写入方向：单独命名空间、版本化城市事实表；先读/校验→生成新副本→写入→读回核对。仅保存永久事实，不保存ACTIVE为权威。table先例与marker实测不能证明这个新账本保存/重载、完整写入和多人同步全部通过。
5. City UID需独立身份分配方案与持久凭据；坐标/current owner:cityID不可冒充跨征服稳定身份。旧档缺失事实依OPEN-04拒绝补造，既有标记不能当专业事实。
6. Settler必须先检资格并在执行时重检；单位消耗与Property提交之间没有已证实原子事务。读回一致也不等于崩溃恢复保证。当前仅保留离线计划/已提交receipt模型，不编造实际消费API保证。

## 本地候选模块

DevelopmentTests/DistrictFamily.lua：Build/Resolve，解析当局数据库表对应结构；支持替代链，拒绝循环/缺失/冲突，返回独立结果。
DevelopmentTests/DistrictCompletionCandidate.lua：只接受MOCK_ONLY事件/对象观察，校验类型/位置/所属/完成布尔值与生命周期资格。输出仅CANDIDATE_COMPLETION，不输出COMPLETE_ORDERED_BATCH，不调用State.Complete，不授予永久专业或收益。被掠夺但IsComplete的对象仍只能算候选；是否修复回调是需验证的时序问题，不把pillaged作为抹去历史的理由。

## 下一轮最小探针准备（本轮未安装，用户暂不执行）

建议监听CityBuilt与OnDistrictConstructed，仅测试文明；每条显示事件序号、回合、owner/cityID、区域Type/实例ID、family、IsComplete、已有事实是否存在、是否处于加载阶段。对象ID直接显示，不要求用户手抄。初期不生成永久专业、不消耗Settler、不把此探针与B010绑在一起。

最小验证目标：①普通放置/建成对照，放置不能出现已确认完成；②保存并读取，检查是否重放建城/区域完成事件。可优先沿用现有存档完成一个区域；只有专门验证CityBuilt时才需新建城市，而非强制新开局。探针部署并完成本地mock验证后再提供正式步骤与PASS/FAIL判据；现在不派发用户测试。

## 本轮检查

`PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/test_district_family.py`通过：真实SQLite只读表、10类型匹配、合成多级替代、缺失/循环/冲突图、未知类型、非v0.1、进度/放置过滤、事件与对象不一致、缺ID、加载/征服未知上下文、被掠夺但完整对象、UI/Gameplay真实执行入口拒绝。

原CitySpecializationState模型回归另执行，输出LOCAL_SIMULATION_PASS。这些都不是游戏验证。运行源码和UUID、Accepted Design与既有备份不改。
