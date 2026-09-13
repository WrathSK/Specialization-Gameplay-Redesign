# B013/B015实际新城接口：本地挂接验证

Document Owner: Codex
Architecture Revision: A0044
Design Reference: D0007（未改）
Runtime: B019 / modinfo26（未改）
Verification: LOCAL_SIMULATION_PASS

新增DevelopmentTests/NativeFreshHookCandidate.lua，捕获原shared.OnFreshCityBinding作为legacy，保留一次调用，然后检查本次执行结果；只允许MOCK_ONLY，尚未登记运行包。重复安装拒绝。新观察者失败不回滚既有B015成果，也不阻止未来正常legacy调用；新观察者自身按player保持暂停。重入不递归执行旧处理。其它脚本之后覆盖整个槽位仍无法由未被调用的wrapper自动检测，真实安装顺序须受控。

## 检查依据

不是仅检查已有TRACKING表，而是核对本次legacy前后写入次数恰好+1、最近动作FOUNDATION_SAVED、未halted、加载阶段与两监听器注册，再核对当前绑定、城市/owner/坐标、初始化revision0/NONE/0/无first及建城回合。证据里的完整扫描与已观察新城来自已审查B015本次成功路径，不是新API返回；只适用于此版实现。未来改变B015逻辑必须重新核对适配。

因此B015内部吞掉扫描/写入错误仍能被拒绝；旧表即使TRACKING也不能当新事件证明。实际B013会过滤重复CityBuilt，加载不触发新绑定回调。公开诊断字段是DEV耦合，未作为长期正式API。

CityEventFlow新增AfterLegacy入口，接已核对证据而不再执行legacy；原Fresh入口保留。测试直接运行当前BindingProbe.lua和CityJournalProbe.lua，完整保留原有journal回归场景，再检查一次证据、读档/重复/旧表拒绝、扫描失败、丢写、写后异常、观察者失败与重复安装。最后实际回调→证据→AfterLegacy→CityPropertyBridge→统一表/Gate完整组合，新表DONE且B015只写一次。没有将mock测试当游戏执行。

八脚本exit0，输出与备份在DevelopmentBackups/Specialization-before-native-fresh-hook。修改仅离线CityEventFlow，新增候选/测试/报告；运行、Design与其余既有Tests保持。

## 边界与下一项

LOCAL_SIMULATION_PASS为本地组合通过，不新增游戏PASS。本模块只核对新城回调，未完整挂接原生完成事件、正式资格许可或跨加载持久历史；不能将同次回调证据延伸到未来所有通知。B013仍是DEV绑定，不是跨owner永久UID。

下一项可准备限定DEV集成：安装顺序明确为B013/B015启动后、load前；旧回调结果核对后再分发。实际完成通知须同样经过对象与区域族检查；加载后已有城保持只读直到历史凭据安全恢复。此限制只属于尚未部署的实验，不改变Design中城市应继续发展的规则，不据此启用正式专业收益。当前无需新实机测试或重复B019，B010延后。
