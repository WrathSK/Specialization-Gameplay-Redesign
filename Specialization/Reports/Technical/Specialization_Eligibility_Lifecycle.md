# 资格失效与重新授权：离线入口

Document Owner: Codex
Design Reference: D0007 / ELIG-001..006
Architecture Reference: A0031
Scope: MOCK_ONLY / NOT_DEPLOYED

## 本轮结果

新增DevelopmentTests/EligibilityLifecycle.lua及test_eligibility_lifecycle.py。LOCAL_SIMULATION_PASS表示本地模拟通过，不等于实机通过。与实际CurrentPlayerRoster候选组合测试，旧模块不改、运行B017不改、无新实机批次。

入口将资格读取结果转换为短期处理许可，未连接任何城市写入或收益。New要求MOCK_ONLY。Refresh开始即清除旧授权，只在显式AFTER_LOAD_CLOSE阶段、完整名单和一致资格结果后建立新许可；名单读取失败、格式矛盾、未知/未启用/不在当前名单均不产生该玩家许可。每次重新读取，不信任上次成功值。

Acquire产生本实例登记的许可对象；Check核对对象来源、当前代次、玩家及当前资格。外部修改对象字段、伪造对象、跨玩家、跨实例、旧刷新许可均不能冒用。Invalidate立即阻止旧许可继续通过。外部读取期间若再次失效或内层刷新完成，外层旧刷新不能覆盖新状态；校验结束前再次核对代次。

## 检查覆盖

- 初始未就绪无许可；读取成功后仅enabled玩家取得许可。
- 先前许可在刷新开始即失效；失败不能沿用旧成功结果。
- UNKNOWN、DISABLED、名单移除均无许可；恢复后可重新获取，旧许可继续失效。
- 读取回调触发失效、内层新刷新时旧刷新不提交。
- 新实例不承认旧对象；多enabled玩家互不冒用；名单资格冲突拒绝。

## 明确边界

这是入口许可模型，不是独立授权安全沙箱，不验证任意第三方恶意Lua。生产接入时必须在操作/提交边界重新Check，不能只在排队前检查一次；Check后外部状态变化也需要实际事件及时Invalidate。未注册真实事件，不能声称当前游戏已经能及时撤销许可。

没有读写永久城市事实接口，授权失效不能清除专业/Potential/模板；当前名单不在不代表从未参与。没有实际Modifier撤销、事务回滚、已在执行中的回调中断或正式Network缓存失效实现。进入机制的许可不能替代这些工作。

阶段AFTER_LOAD_CLOSE是调用方证据契约，不是本模块自行发现引擎就绪。真实GetAliveIDs返回及初始化/恢复时机仍待合并运行验证；54–61身份不猜测。没有改变Design，也不重开AI/征服规则。

## 下一步

将名单、资格读取和本许可模型组合为最小只读Gameplay运行对照，记录名单与可运行玩家；正式效果保持关闭。后续实机应验证新增名单/运行许可，而不重复旧界面或固定槽位截图。当前尚未发新测试。

修改前文档与保护hash见DevelopmentBackups/Specialization-before-eligibility-lifecycle；原有Design/Runtime/Tests逐文件hash保持。无游戏配置/UUID变更，未启动游戏。当前任务与证据入口：[Status](../../Status/Specialization_P0_Status.md)。
