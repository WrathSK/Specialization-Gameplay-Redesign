# B013 本地交付结果

Document Owner: Codex
Build: P0-B-013 / modinfo20
Architecture: A0014

## 用户摘要

新城DEV绑定探针已部署。加载后新建测试城市自动预留编号、写城市token、确认总账；旧城/加载只读，不补造历史。部分失败保留现场，不自动修复。需要用户执行[两案](../Cases/B013_New_City_Binding.md)，没有新增实机PASS。

## STATIC_CONFIRMED（静态证据，不等于实机）

BindingProbe.lua由Gameplay include且登记modinfo。玩家门控、加载阶段、城市owner/id/坐标核对；只监听CityBuilt，不监听区域事件产生绑定。读取命令BINDING_READ复用既有选城窄请求，不写Property；UI仅新增Read binding按钮。UUID保持df9efdad-dd48-40a7-b868-87f0617bc16d。

Game命名空间SPC_DEV_BINDING_B013_P<playerID>存schema/owner/counter/records；城市SPC_DEV_BINDING_B013_TOKEN存DEV-B013-P<player>-<serial>字符串。总账先RESERVED→城市token→总账CONFIRMED；每次Game写前比较与写后读回，city写后读回。32座上限用于控制DEV数据量，编号不回收；不输出production UID或专业/Potential。

重复CityBuilt仅在双方已确认且引用一致时不写；缺一侧/冲突/未知拒绝。模块单玩家busy避免重入。缺总账时扫描该玩家现有城token，存在残留则拒绝bootstrap；这是DEV启动保护，不证明正式账本丢失可以可靠区分首次安装（若所有痕迹均已丢失仍不可判定）。CityBuilt在征服/特殊Mod路径的语义未全面验证，不对正式身份作承诺。

加载后遍历测试玩家城市自动只读审计，日志和选城面板重新从Property读；不从缓存伪造匹配。读档/读取不完成RESERVED，也不补缺失token。本批只验证正常写入及恢复，城市性质未知时不改变OPEN-04。

## LOCAL_SIMULATION_PASS（本地模拟，不等于Civ VI实机）

最终通过六组：test_binding_probe.py、test_specialization_p0.py、test_storage_probe.py、test_completion_probe.py、test_specialization_identity.py、test_background_routes.py。执行环境为既有PYTHONPATH=/tmp/city-gpp-test-runtime及python3/lupa，各exit=0。

新增测试覆盖：加载期建城忽略、旧城不写、新城双方匹配、两城token不同、重复原生事件不写、context重建审计0写入、城市写失败保留RESERVED且不自动重试、引用复用拒绝、Game写失败不写城市、setter写后抛错读回一致、文明/事件坐标门控、残留城市token而总账丢失拒绝创建。

没有模拟完整游戏序列化/崩溃或多人；读回成功不是崩溃原子性。区域完成及专业状态离线模块未接入运行。

## 文件与备份

新增运行BindingProbe.lua；修改Gameplay.lua、Probe.lua、P0Panel.lua/xml、modinfo。新增test_binding_probe.py；更新test_specialization_p0.py加载新模块，test_storage_probe.py的隔离Gameplay夹具增加空BindingProbe以保持原测试范围。更新Architecture/Status/README/AGENTS及本两份案例/结果。

原运行包完整备份DevelopmentBackups/SpecializationP0-B012-before-B013-binding；四份文档保存在Historical/DocumentSnapshots/*_before_B013.md。Design、游戏配置、截图归档未修改。没有启动Civilization VI；等待用户结果。
