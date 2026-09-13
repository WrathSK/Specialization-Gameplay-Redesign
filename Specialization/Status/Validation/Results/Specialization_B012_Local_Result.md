# B012 本地交付结果

Document Owner: Codex
Build: P0-B-012 / modinfo19
Architecture: A0011

## 用户摘要

已部署两个专用表存储按钮，复用既有窄Gameplay请求，免选城/剪贴板。读取不写入，写入只在独立DEV键为空时进行，重复相同内容不写，异常/不匹配不覆盖。运行UUID保持，正式专业和收益未启用。需用户执行[两案](../Cases/B012_Table_Storage.md)。

## STATIC_CONFIRMED

仅静态证据，不等于游戏验证：StorageProbe在modinfo的ImportFiles与Files登记，由Gameplay include；版本B012/19；UUID df9efdad-dd48-40a7-b868-87f0617bc16d未变。唯一新增写入调用为Game:SetProperty(SPC_DEV_STORAGE_B012_P<playerID>,固定测试表)，玩家由P.IsTestPlayer门控。没有City:SetProperty、单位/生产/GPP/网络收益调用。读取发生在Gameplay，UI只发操作请求和显示带token ACK，不把UI快照作为存储权威。

两个合成记录检验字符串key、嵌套表、数值17/0/0.5/42、字符串UID和true/false。递归完整比较检查缺键/多键/类型；错误或不匹配不能重置。setter报错后仍尝试读回，MATCH只表示当时完整可见，不保证磁盘durability。attempts是本次Gameplay加载中的实际setter调用次数，读档重置；持久revision保持1，不以按钮计数作为永久事实。

## LOCAL_SIMULATION_PASS

本地模拟通过，不等于Civ VI实机：

- test_storage_probe.py：空读、首次写、重复不写、Context重建只读、已有不一致拒绝、写后异常读回、读失败无写、写前异常；面板无选城请求；执行真实Gameplay请求分支、ACK匹配和非测试玩家拒绝。
- test_specialization_p0.py：既有窄探针/marker/总督/专家/相邻/路线回归。
- test_specialization_identity.py：身份SQL与资源引用隔离检查。
- test_completion_probe.py：B011事件语义与UI分页保持；版本断言改用当前P.VERSION。
- test_background_routes.py：既有后台影子商路回归。

均使用PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/<脚本>，最终exit=0。首次存储测试缺少mock Events定义而失败，已补齐测试环境后重跑通过；不是游戏失败证据。未启动游戏或安装依赖。

## 文件与恢复范围

运行新增StorageProbe.lua，修改Gameplay.lua/Probe.lua/UI P0Panel.lua/xml和modinfo；新增test_storage_probe.py，更新两个既有测试的模块加载/版本断言。源码旧包完整保存DevelopmentBackups/SpecializationP0-B011-before-B012-storage；四份文档旧版另存Historical/DocumentSnapshots/*_before_B012.md。Design、配置、截图未编辑。

用户实机状态为USER_GAME_TEST_REQUIRED，无新增USER_GAME_TEST_PASS。这个探针未加载CityIdentityRegistry离线模块，不生成真实城市编号，也不执行离线专业事实写入计划。
