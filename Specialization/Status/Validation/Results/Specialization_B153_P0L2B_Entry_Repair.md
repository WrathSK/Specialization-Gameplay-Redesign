# B153.180 — 意义延展单城验证入口修复

Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；USER_GAME_TEST_REQUIRED。用户授权修复B152中止的入口/成对采样；不授权正式六yield/all-city cutover或L3/M/N/U2。D0039 / Culture D0038逐领域Floor、K0.5、资格与现有收益定义均未改变。

## 问题与修复边界

[B152原生中止](Specialization_B152_P0L2B_Entry_Blocked.md)仅证明C00对话投影未确认；没有原生四态差值，也没有引擎内部busy/iterator证据。本批本地可重现丢失iterator state/control、异常留下更新锁、忙碌时读取旧投影以及事实先通知/Dialogue后落地的风险；不将其中任一写成截图唯一原生根因。

- [Dialogue](../../../../Mod/Dialogue.lua)：Init/Audit拥有自己的锁并保证异常收尾；BUSY不能清他人的锁或确认旧last。完整遍历保留原生iterator/state/control；目标缺失清除该目标旧投影，返回本次是否执行及原因。逐城规则、0/100实验及精确owned载体保持。
- [旧巨作相邻](../../../../Mod/GreatWorkAdjacency.lua)：它是Dialogue.Receive末尾的直接同步依赖，也会丢iterator三值并阻断返回。仅修Audit三值与异常锁收尾，保留Init/目录/计算/事件/正常旧效果；没有全局关闭writer。
- [实际采样入口](../../../../Mod/Gameplay.lua)：Facts和Dialogue各自验证、独立接收；两端本次均明确接受后才记录一份当前pair receipt，再通知当前单城Meaning。ACK仍只表示处理，不代表成功；拒收/重复不通知，不增加重试队列。
- [Meaning Probe](../../../../Mod/CultureMeaningProbe.lua)：取消它在Facts尚未配对时的提前回调，其它原有Facts消费者保留。Hold/Read必须匹配accepted-pair的Seq/Generation/Turn/FactsEpoch/FactsInput、目标reference、当前KNOWN事实和本次投影stamp，并确认实际载体/健康。一端落后时的重复包不能冒充新确认。
- 未配对期间只保留已持有实验的配置并标未确认，不采基线、不把UNKNOWN当0；配对后按当前事实确认。相同有效配置零写，避免新Seq对100%实验反复撤回重加。报告首屏显示错误码与短原因，无源码路径堆叠；未增加本地化key或按钮。

## 更新范围与临时状态

当前fixture明确动作/同回合事实变化/正常回合与现有load/loss路径继续；post-pair只访问该fixture，未添加全城Meaning扫描、per-frame/hover请求或独立GC。原有收藏接收与普通旧writer范围不扩大。

Dialogue只保留每支持玩家一份最新pair header；sample继续使用原有当前集合。generation/epoch/input/turn/reference失效使旧凭据不可确认，transfer/return清pair；没有历史队列、Property、永久账本或saved实验重放。加载仍默认OFF、精确清理已登记实验载体，未修改E2 authority。

## 本地验证

- 53项Meaning定向测试PASS（原38保留，增加真实入口/异常边界）；26项K事实/producer/legacy隔离回归PASS。
- 实际Gameplay request +真实Facts/Dialogue/GWA，无预装样本：冷C00、事实回调不提前用旧Dialogue、同内容新Seq/无changed恢复、跨turn、Generation/Epoch/Input拒收、重复包、ACK一端领先/旧pair反例、两城市隔离、native iterator三值。
- BUSY/普通或旧Meaning投影不假确认；外层GetCities/Members/FindID/GetID/Count异常锁收尾与Init重入；UNKNOWN/精确撤销/加载/配置健康和原四态断言保留。受控100%同内容新Seq零写；busy后新接受样本恢复仍只属于模拟证据。
- 复用已有Lupa2.8/lua55，外部Gameplay数据库只读并复制到内存；未安装依赖、修改外部DB或跑历史full/stress。
- 五个改动Lua语法、modinfo180/182文件集合、当前selector/hash/链接及diff检查通过。SQL/模型/原生UI读取、GC策略、Design、main、永久状态未改。

LOCAL不能证明原生迭代器形状、真实UI时序或Culture倍率正确。B151整数证据及B152冻结LOCAL/失败结果保持各自原范围。

## 一个最小续测

冷启动已有测试存档，选原同一Culture ACTIVE4城市；支持的非主题馆藏，至少有正整数Culture追加来源（以当前D报告为准，例如政府/外交领域D3）。作品/位置/D/其它修正保持固定，不开旧手工Dialogue实验。

1. 左键“意义延展验证”准备C00，右键等UI读数刷新。应为追加0、旧对话0%，无未确认错误；若入口仍错误就停止并只提供该报告。
2. 左键C10、右键读取；再左键C11、右键读取；再左键C01、右键读取。一次末阶段报告即可提供四态记录。
3. 核对 `C10−C00` 与 `C11−C01` 都应等于报告每件理论Culture追加×合格W。旧对话native-only差值继续按既定门禁核对，不能从carrier配置宣布通过。
4. 最后左键结束，确认OFF及旧效果正常恢复。任一阶段未知或两次追加差值不同就停止，不继续新能力、不要求旧小数或长测。

## 部署与停止点

B153.180 / modinfo180 canonical source完成；实际部署需本轮clean commit/push、可靠退出核对及W0003精确receipt/staging/equality。部署前live仍按既有B152 receipt，不从HEAD推断。部署结果在成功事务后补充。

精确recipient原语仍TECHNICAL_INVESTIGATION_REQUIRED；本批只修可逆验证入口，不宣布完整意义延展实施或实机PASS。用户需要新Design决定：无。Codex到此停止，等待上述最小续测。
