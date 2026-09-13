# 新城有序事件流与历史检查：本地组合

Document Owner: Codex
Architecture Revision: A0043
Design Reference: D0007 / PROG-005 / ELIG（未改）
Runtime: B019 / modinfo26（未改）
Verification: LOCAL_SIMULATION_PASS

## 实现与结果

新增DevelopmentTests/CityEventFlow.lua，只在MOCK_ONLY中使用。与CityPropertyBridge、统一表、Gate、恢复模型实际组合；没有引擎事件注册，没有覆盖shared.OnFreshCityBinding。

新城处理次序固定为既有legacy处理→核对处理结果和新城证据→打开城市连接→提交/对账。legacy返回nil不当作成功；必须有TRACKING结果以及已观察新建、绑定有效、扫描完整、市中心完成、无已完成v0.1区域的证据。现阶段inspectFresh/inspectComplete为注入fixture，真实检查adapter尚未接入。

LOADING期间不派发。已知通道的新城重复通知保留legacy调用，不再次写新表。每个有效完成通知单独按交付先后提交，不按区域类型或回合排序；后来完成的其它专业区域不覆盖锁定。旧城/新实例未追踪城市的完成通知不创建记录。监听就绪只能从LOADING进入一次，Close后不重开。

异常、重入、资格失效、旧处理健康异常、不完整扫描及提交不确定后暂停当前整个候选流，不跳过失败后用较晚事件锁专业；不回滚或清除既有成果。保守暂停是实验故障隔离，不是正式全帝国玩法规则，实际部署需要按owner管理流及资格事件。

新测试与七组提交/存储回归共八脚本exit0，覆盖加载通知忽略、legacy/核对/open顺序、两城独立、剧院先交付锁文化后学院不覆盖、重复通知、无追踪旧城、内部失败未抛异常、扫描不完整、重入/资格丢失、非法完成与写入失败后暂停。最终输出见DevelopmentBackups/Specialization-before-city-event-flow/test_result.json。

LOCAL_SIMULATION_PASS只说明本地模拟通过，不等于Civ VI实机通过。真实B015未改；mock旧处理不是B015引擎执行的替代证据。模拟中区域族使用State约定THEATER_SQUARE，实际引擎区类型转换仍需真实adapter核对。

## 历史完整性边界

模型只能发现已交付通知在验证或处理时失败，不能发现引擎/其它Mod根本没有交付的事件，也不能将本地serial解释为引擎历史连续编号。暂停标志是实例内的；本模块没有持久GAP或跨加载观察凭据。

为避免伪造历史，新的流不恢复旧channels；已有DONE也不授权处理加载后旧城的首次专业完成。正常保存重载的成果保持已由B019支持，但历史连续性是独立问题。本模型不是永久禁止旧城继续发展的设计修改，而是尚未部署的技术候选边界；正式适配必须补充持久观察状态/安全恢复，不能静默接受玩法变化。

资格检查先于legacy与城市访问。许可失效后的当前流保持暂停，不删除永久数据。此流程不提供跨owner身份，B013 token仍不是正式永久UID。

## 下一项

下一轮优先把上述检查映射到现有B013/B015真实返回值，并确定有序挂接方式（保留旧回调、检查旧处理吞错结果、不能自行覆盖槽位）。准备限定DEV接入时必须明确同次加载新城实验范围；跨加载继续处理的历史凭据尚需实现，不能宣称正式完成。当前没有新运行包、没有用户测试，B019不重复，B010继续延后。未启用专业收益。
