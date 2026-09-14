# B064 独立影子账本验证

Document Owner: Codex
Design: D0025

本批在InheritanceShadow.lua中建立SPC_INHERITANCE_SHADOW_V1 Game Property；schema/revision/records/watch/events/sequence。records以旧有效binding token为备份键，完整深拷贝TOKEN/FLOW/JOURNAL/INVEST/TEMPLATES及其pending字段；这不是最终全球UID分配器。相同token不允许换Owner/CityID覆盖；未知/缺失binding不导入。当前City账本仍权威，影子不恢复、不付费、不改变ACTIVE。

BindingProbe、CityFlowProbe、CityJournalProbe、InvestmentAction、Standardization的已有写后校验点增加隔离通知。shadow失败被捕获并报告，不改变既有事务阶段/消耗流程；投资INTENT/CONSUMED_CONFIRMED/完成各自保存，不冒充已结算。正式权威迁移前仍需处理写失败恢复和原子边界。本批不声称跨City/Game双写为原子事务。

加载一次对启用玩家合法城市读取；每条相关生命周期事件核对已注册位置，仅记录原参数及当前端点，不由位置认定继承。事件日志最多24条持久，面板末6条；无关参数和空闲/回合无循环扫描。重载没有旧City也能由已保存watch读取Game备份；原址新token另建记录，不复制旧投资。旧Owner/ID仍历史，不盲改。

D0025时代对话仅修改DialogueModel的25倍公式及Dialogue.sql14组生成式100+25*(D-1)，手动TEST25/50/100数值不变。冻结D0024，Current Spec/ChangeLog/Architecture sync更新。用户免新实机，不冒充实测25%。

验证：DevelopmentTests/test_b064_shadow.py实际执行新模块+前批回归。Game存储深拷贝模拟、重复无写、City Property消失、加载重建、事件上限/无关无写、pending阶段、错误捕获、新token不串账。模型D9=200%，数据库每个Era的14项C/T factor严格检查。新增Fixtures/B064ShadowHooks.json作为五个精确通知点差异白名单，旧效果测试不删除；test_b059_dialogue.py只调整25%期望。

限制：实际Game保存数据和事件参数顺序待用户；尚未实现跨Owner正式继承、tombstone/新永久UID、Claim。此次观察日志筛选未知参数形状可能漏事件，若hook可用但无日志不能据此断言引擎不发事件。无后台高频扫描、未启动游戏、未提交Git。

部署核对：B064.90/modinfo90，110文件，源与运行包SHA256均c82c35de9881632fd2556c016a54d09bd57403e15295ae71bc2acbbccd74122b；旧包完整保存在外部SpecializationDeploymentBackups/.SpecializationP0-backup-f0tll826。git diff --check通过；D0024冻结hash与此前一致，D0025 hash为81dc772c1038718e567496cfdb165167e6090fae2b7b472b7301435d766d994b。
