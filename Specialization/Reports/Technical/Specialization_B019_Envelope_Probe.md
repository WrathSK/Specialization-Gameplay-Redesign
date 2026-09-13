# B019：合成单表阶段探针

Document Owner: Codex
Architecture Revision: A0040
Build: P0-B-019 / modinfo26
Verification: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

## 实际接入

新增唯一运行目录EnvelopeProbe.lua，由Gameplay include/start，modinfo ImportFiles/Files登记；面板复用现有空位增加Read envelope和Next envelope stage。通过既有EXECUTE_SCRIPT请求路径，两个操作均不需要城市选择。UUID、SQL、文明定义和配置未改。

只允许测试文明玩家，写入唯一专用键SPC_DEV_ENVELOPE_B019_P<player>。六阶段为两笔固定合成操作，每笔原值/PENDING→目标/PENDING→目标/DONE，空记录为阶段0。DEV_B019不是实际城市ID。读取必须整表与七种合法固定快照之一完全一致，坏表不覆盖。每次Next携带UI观察到的ExpectedStage，过期请求不写；整表写前重读、一次setter、写后精确匹配。未确认写入停止本次实例。没有清空/迁移旧DEV表。

LoadScreenClose自动对当前名单中的测试玩家只读，记录autoStep；UI只显示结果。尚未获得load事件时拒绝Next。Read不修改Property。读档不自动恢复执行；BEFORE_PENDING经用户Next推进仅是显式合成实验，不为正式不确定资源事务制定重做规则。

## 与离线模型的关系和边界

采用既有统一表的before/target/PENDING/DONE结构与读回规则；测试将实际运行脚本产出的六张表交给PendingCityRecovery进行独立契约校验。运行探针是有限固定fixture，不部署MOCK_ONLY Gate/城市规划器，也不把合成身份当永久城市UID。此轮不构成正式提交器或通用资格接入。合成快照严格比较只能证明此固定数据范围，真实城市记录规模仍需后续适配。

STATIC_CONFIRMED只代表Lua语法、XML、文件加载引用及UUID检查。LOCAL_SIMULATION_PASS代表本地mock通过：实际Gameplay请求、面板无城派发、自动load、六阶段JSON新VM恢复、重复过期请求、非测试玩家拒绝、坏表/读失败/丢写/写后异常；再加既有六组提交/恢复测试，七脚本exit0。Lua模拟运行时不等于Civ VI引擎。

USER_GAME_TEST_REQUIRED：两案见[测试步骤](../../Status/Validation/Cases/B019_Envelope_Recovery.md)。自动load时机、Game Property正常保存重载和实际UI可读性仍由用户验收。没有新USER_GAME_TEST_PASS。正常重载不能证明进程崩溃原子性或读写之间存在锁。

## 文件及保护

新增EnvelopeProbe.lua、test_envelope_probe.py及本报告/案例；修改Gameplay.lua、Probe.lua、P0Panel.lua/xml、modinfo，更新Architecture/Status/入口版本和索引。备份与校验位于DevelopmentBackups/Specialization-before-B019，旧Design、Tests、SQL和其他运行文件不变。没有启动游戏。
