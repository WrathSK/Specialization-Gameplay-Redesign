# 城市编号账本与写入故障恢复 — A0010

Document Owner: Codex
Design Reference: D0002 PROG-004 / OPEN-04
Runtime: B011 / modinfo18（未修改）

## 用户摘要

本轮核对Game/City Property表存储先例，新增城市编号账本的离线故障模拟。写入报错但已保存、写入被丢弃、读回失败、损坏数据、重复请求等场景均按预期处理。不能确认时不重发编号、不清空账本。用户现在无需操作。

这还不是可用于正式城市的永久身份系统：游戏中如何证明相同城市对象、怎样识别缺失账本是首次创建还是异常丢失，仍需实际接入验证。后续先准备独立存储探针，不用假身份绑定专业。

## STATIC_CONFIRMED — 仅源码证据

本机HD根：/Users/xutingzheng/Library/Application Support/Steam/steamapps/workshop/content/289070/2465378070。

- Gameplay/Buildings.lua:221–223、234：Game:GetProperty / SetProperty保存和读取playerList表。DL.modinfo:1884为Gameplay脚本加载项。
- Gameplay/CityYield.lua:46、102、161、171：城市Property读取、嵌套表更新和写回；DL.modinfo:1870加载。
- 当前Specialization Gameplay.lua:48–54仅marker读写；旧marker实机通过不等于新账本通过。

STATIC_CONFIRMED表示代码存在这些用法，不证明任意嵌套表、序列化键、游戏保存时机、多人确定性或事务原子性。

## 离线方案与范围

新增DevelopmentTests/CityIdentityRegistry.lua，仅接受MOCK_ONLY。当前单个envelope包含schema/counter/revision/records，编号序列与身份记录同时作为一个值写入，减少分开写两份数据导致不同步的机会。它不保存专业/Potential，也未替代既有CityFactWritePlan。若未来把专业事实另存城市Property，两者仍不是跨对象事务；身份确认后才能提交专业事实，失败必须能恢复，不能声称单envelope已解决全部事务。

records以owner:cityID寻址，保存owner/cityID/instanceProof/serial/uid。uid只在同一存档分支内有意义；读旧存档后另开分支可以出现相同编号，不承诺跨存档全局唯一。当前不删除记录/回收编号；记录删除和继承不在此实验范围，registry大小随建城增长的成本亦待评估。

instanceProof是**外部fixture提供的已验证城市代际凭据**，不是已发现的引擎API；不得用owner:cityID、坐标或B011会话事件序号代替它。同一引用遇到不同凭据返回未知，同一凭据出现在不同owner/引用则保留OPEN-04。空账本须额外registryBootstrapConfirmed前提，不能因GetProperty返回nil就断定是新游戏。本模块没有解决这些前提如何由真实游戏可靠提供。

当前编号格式、Property容器选择均为离线实现实验，不改变Design的征服继承/旧档规则，也不自动将新城市归专业。

## 写入协议

1. 读取并校验整个账本；损坏/读异常不能当空。先复制数据，避免原地修改引擎可能共享的table引用。
2. 相同已验证对象的重复调用返回原编号；缺少身份且未确认新建时拒绝分配。
3. 生成编号与新账本；写前重新读取，内容有变化则拒绝过期计划。同一模块实例拒绝重入。
4. 仅调用一次模拟setter，无自动写入循环。无论setter是否报错，均尝试读回。
5. 读回等于拟写数据：当前可见提交已确认；等于旧值：NOT_COMMITTED；读取失败、其它内容：UNKNOWN。UNKNOWN不发奖、不返回成功身份供正式机制使用。
6. 后续正常读回已有相同身份可恢复结果，不凭上一条报错重新分配编号。读回一致不代表磁盘崩溃持久性。

单值替换、读后可见性、单写入者串行访问是模拟前提；写前比较不是引擎CAS锁，不能防止其它写入者在最后读写间介入。UNKNOWN不能被包装成空账本。测试没有证明游戏保存截断时的原子恢复。

## LOCAL_SIMULATION_PASS — 本地模拟，不是实机

执行：PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/test_city_identity_registry.py。

覆盖：首次编号、重复编号、两城不同编号、重建模块、JSON序列化后新Lua VM恢复；写前异常、静默丢弃、写后异常、读回异常后恢复；共享table写入失败不污染原件；损坏/schema不符；写前变化、重入；引用复用/易主、空账本无初始化凭据；非测试文明、非MOCK调用拒绝。最终exit=0。

另运行test_city_fact_write_plan.py回归，exit=0。既有专业状态/投资算法本轮未修改。开发诊断状态READY/UNKNOWN/NOT_COMMITTED不替代项目验证等级。

## 后续最小存储探针边界（尚未部署，请勿测试）

建议单独版本先验证表存储：仅测试文明，独立DEV Property命名空间，两个合成记录包含编号、嵌套表和字符串key；写后读回→保存重载→再次读取/重复写入，面板显示完整性和写入次数。不会写专业/Potential、不会消耗单位、不会给真实城市假UID；因此可优先沿用旧存档，不需要为单纯序列化新开局。部署时才给正式两案步骤。

该探针通过只能证明表在实测条件下的保存行为；真实CityBuilt代际证明、重载前后绑定、征服/拆城复用及初始账本资格必须后续单独解决。它们目前属于USER_GAME_TEST_REQUIRED或尚待技术方案，而非PASS。OPEN-04既有设计问题仍保留，当前不需要用户追加决定。

本轮未修改Design、运行源码、UUID、游戏配置或截图，未启动游戏。用户需要决定：无新增。用户需要测试：无新增。Codex下一步：实现独立DEV表存储探针并先完成本地验证，再交付用户最小保存/读档测试。
