# B015新城记录提交 — 本地结果

Document Owner: Codex
Build: P0-B-015 / modinfo22
Design: D0005
Verification: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS
Game Verification: USER_GAME_TEST_REQUIRED

STATIC_CONFIRMED为Lua/XML/加载引用静态证据；LOCAL_SIMULATION_PASS为本地合成引擎通过，均不等于游戏通过。正式收益和专业状态消费未启用。

## 实際变化

新增运行CityJournalProbe.lua，使用 `SPC_DEV_CITY_JOURNAL_B015` 单个City Property存放schema/kind、B013 token、owner/cityID/位置、建城回合、health/revision、DEV specialization/potential与first记录。其为DEV候选事实，不是已验证永久UID，也不被正式CityRoleFacts/网络层消费。

BindingProbe仅在真实新建绑定成功后调用shared.OnFreshCityBinding；重复建城或加载不调用。B015初始化最后注册回调，因此不依赖两个独立CityBuilt监听器之间的顺序。它使用已实测方向的玩家GetDistricts():Members()过滤该城市，要求完整扫描、有已完成市中心、无已完成四族区域、两个监听器就绪；失败不建立资格。512扫描上限到达即明确失败，不把截断当完整。映射使用GameInfo/DistrictReplaces，不以RequiresPopulation单独分类。

完成事件核对对象/owner/type/IsComplete及绑定后，首次有效通知保存候选专业/Potential1；后续通知不覆盖。复制旧表后拟写，写前比较、写后完整读回；setter抛错但读回正确视为已写。写入失败或重入停止本玩家当前会话后续提交，能安全读取原表时尝试保存GAP；GAP持久保留且后续不能改专业。身份冲突不覆盖，不自动转移owner。

加载自动只读审计，Read city journal经Gameplay窄请求与token ACK；选城与测试文明门控沿用现有路径。旧城没有B015表时显示UNTRACKED_NO_WRITE，不导入B014记录。新按钮独立保留原按钮。

## 七组本地验证

命令前缀 `PYTHONPATH=/tmp/city-gpp-test-runtime python3 DevelopmentTests/`。最终执行均exit=0：

- test_city_journal_probe.py：实际BindingProbe→CityJournalProbe回调；正常新城/首次专业/重复通知与读档；旧绑定不补写；扫描失败/已有专业/无市中心拒绝；写后抛错读回；写失败停止/无法保存GAP明确提示；GAP重载阻止；重入停止；owner变化保留原记录；加载及文明门控。
- test_specialization_p0.py：Lua/XML与实际新按钮→Gameplay→ACK只读通路；原探针回归。新增UI断言后重跑一次通过。
- test_specialization_identity.py：独立文明SQL/展示资源/manifest检查；SQLite隔离模拟，不新增文明选择实机PASS。
- test_binding_probe.py：B013旧逻辑与失败/重复边界回归。
- test_completion_record_probe.py：B014观察表回归。
- test_storage_probe.py：DEV表存储与Gameplay请求回归；测试隔离stub更新。
- test_background_routes.py：后台商路影子回归，无权威升级。

## 限制与D0005

GAP标记自身若也无法写入，仅能保证当前会话停止；不承诺进程崩溃/重载后能检测该未持久化失败。Mod停用期间的完成历史缺口不能由版本号证明不存在。B015不提供上述全生命周期或多人原子性保证，不能作为正式专业初始化验收。

征服后必须保留事实是D0005已定设计。本批仅遇owner/绑定冲突停止并保留原始表，不执行正式继承；跨owner/cityID同城证据仍待技术实现，不能以此停止行为作为最终征服玩法。此表未实现Settler投资/模板内容，也不声称验证它们的继承。

当前真实写入与离线CityCompletionJournal没有直接复用：后者依赖MOCK_ONLY身份/队列契约；本探针独立测试真实建城扫描、直接回调和单表写后读回，禁止将MOCK凭据传进游戏。待实机通过后再将已验证接口适配到正式记录层。

## 保护与下一步

备份：DevelopmentBackups/SpecializationP0-B014-before-B015-journal，含运行原件、既有改动文件与Design hash清单。Design与UUID保持，未改Civ6配置，未启动游戏。仅新增运行脚本、修改BindingProbe/Gameplay/Probe/modinfo/UI加载与三个相关测试；当前A0021/S0023。

下一步只等待用户[B015三案](../Cases/B015_City_Journal.md)，不重复已通过批次，不执行B010。
