# HD保留、Specialization关闭：零城窗口

Document Owner: Codex
Evidence: 用户完成指定对照后投递6图，2026-09-15逐张复核。

## 观察

|时间|elapsed seconds|Activity Monitor Memory GB|PID|Threads|Ports|
|---|---:|---:|---:|---:|---:|
|06:02:35|0|8.78|70353|31|1429|
|06:05:13|158|8.92|70353|32|1407|
|06:07:43|308|8.97|70353|32|1402|

308秒净增0.19GB，平均约0.0370GB/min。前158秒+0.14GB（0.0532GB/min），后150秒+0.05GB（0.0200GB/min）。三点递增但斜率减小，不等于逐秒单调、不足以证明持续泄漏或平台期。截图均Turn1、无城市，单位位置不变；Specialization诊断入口不在，Cheat可见，Robert肖像。配置按用户对照上下文：CORE+BTS+EMM+TITLE+AREA+Cheat，不含SPC；无新启用UUID列表，不将界面缺失单独当配置证明。原版Robert替代SPC测试领袖、地图不同、诊断面板是否打开不同，保留比较限制。没有SPC counters，不能填写为0。窗口未见崩溃，不是崩溃修复PASS。

## 与此前比较

SPC+CORE：307秒+0.39GB、重新加入后316秒+0.45GB；SPC无CORE：315秒−0.01GB；CORE无SPC：308秒+0.19GB。本轮表明没有SPC也可观察到短期净增长，不能宣称同一种持续异常已在无SPC复现，也不能凭斜率差认定SPC贡献了固定比例泄漏。ROOT CAUSE / sustained leak classification仍UNKNOWN。

下一步若继续验证，只延长相同无SPC组合零城静置观察5分钟，记录该窗口起止Memory/时间即可；若已退出无需为补齐这次窗口立刻重启。此步骤用于区分继续增长与逐渐稳定，不再重复刚完成的0/2:30/5分钟测试，不修改任何Mod。若稳定再考虑匹配原版领袖及相同面板状态的SPC开关对照；本轮不提前派发。

## 证据与范围

6图已按原名移入外部W/Specialization/Status/Validation/Evidence/HD-Without-SPC-20260915-0602/；manifest含SHA256，移动前后校验，共50062835字节。只更新develop文档；源码、main、运行包、Design和配置均不改，Discount优化继续暂停。
