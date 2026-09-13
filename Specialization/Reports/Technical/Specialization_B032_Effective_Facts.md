# B032：游戏侧只读投资账本与统一有效事实

Document Owner: Codex
Build: P0-B-032 / modinfo40
Design: D0009 unchanged
Status: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS
Native integration: USER_GAME_TEST_REQUIRED（与下一批真实升级合并，不单独派发）

## 实际实现

新增运行EffectiveFacts.lua，在CityFlowProbe之后、ResearchSupport/NetworkBridge之前初始化。Read调用既有SupportFacts检查foundation/binding/journal一致，再读取城市Property SPC_DEV_INVESTMENT_LEDGER_V1。不存在账本时保持原Potential，不创建记录，不迁移旧存档。无专业城市返回Potential/ACTIVE0；有专业而无投资为1。投资账本格式对应离线桥：schema/anchor/revision/investments/pending；校验同城/首个区域、唯一单位凭据、最多3笔和revision=1+笔数。

仅从已完成凭据推导总Potential，不存第二份等级。pending只报告状态，不把未确认操作计入已完成投资；本轮无高级发放，后续高级提交需明确pending许可。高Potential用既有P.CityRoleFacts读取已验证的原生总督门槛，ACTIVE=min(Potential, ceiling)。未知总督条件不伪造ACTIVE，返回UNKNOWN_GOVERNOR；Lv1无需再次依赖总督control，避免旧档基础收益回归。

ResearchSupport和NetworkBridge都改读EffectiveFacts。Lv1能力仍依赖原正确区域和既有carrier；network不再用potential==1排除已升级来源，拓扑身份接受potential>=1。**本轮网络仍仅派生连接/接收资格，不使用ACTIVE进行强度或高级收益结算；未完成sourceLevels正式结算结构。**不能把不再排除高Potential称为Research/Culture强度已接入。

面板Read source totals位置改为Read progression，经新的PROGRESSION_READ请求显示Potential/ACTIVE、完成投资数、pending、账本是否存在。旧SOURCE_YIELDS入口保留，固定收益实验UI不恢复。模块只读，无SetProperty、投资按钮、Unit消耗或自动恢复操作；Property写适配和executor尚未注册，下一步仍要完成。

## 验证

新增test_effective_facts.py，执行实际运行模块：账本缺失零写、Potential4/ACTIVE4→1、未知门槛、重复单位/错误anchor/revision/pending及未专业校验；实际NetworkBridge全套D0009拓扑/断路回归通过，并额外验证Potential4来源保留；实际B024自动Lv1生命周期fixture经新reader验证新城/完成/加载/未准备玩家/错误carrier回归，并额外确认Potential4、ACTIVE1仍保留正确Lv1 carrier。所有原运行Lua语法、XML/manifest文件引用与UUID/version40检查通过。

模拟使用合成投资记录，不能当作实际移民投资或原生保存/读取通过；不提供写合成记录的用户按钮。未对游戏原生Property可见性或界面显示新增PASS。运行源码已改变，因此旧B024/B031 PASS仍为旧构建对应机制证据，本构建兼容性由本地回归支持，实机与下一批正常移民动作合并观察。

## 下一步

注册实际Property写入、同请求移民身份/位置校验及消耗确认，并安排最小升级1→2/重复/保存重载测试。必须确保未授权或失败不消耗单位，不把HD两请求直接照搬。跨owner永久身份和账本完全丢失仍保留边界；小数/Commerce IV、B010继续暂停。本轮用户无需操作，不重测总督原始接口。
