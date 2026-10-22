# Discount idle：城市规模放大与请求计数边界

Document Owner: Codex
Scope: B072.99只读源码调查；不修改Gameplay/部署。

## 用户问题与实机证据

单城/双城增长速度可以提供线索。上一批截图显示：无城约0.057GB/min；包含建城过程的单城区间约0.088；双城纯静置约0.216。后两者表观比约2.46，但单城区间无刚建城基线，且网络尚未握手，双城已VERIFIED并推进18回合，因此不能用此比值证明城市翻倍导致内存翻倍，也不能拟合RAM复杂度。单次有限窗口还不能区分泄漏与缓存/分配器暂留。

## STATIC_CONFIRMED：代码证据，不是实机因果证明

StandardizationDiscount.lua: Audit绑定GameCoreEventPublishComplete；入口counter在ready/busy保护之前。另有Governor/Turn、EnsureReady、Receive调用来源，counter没有按来源拆分。因此约59次/秒不能直接宣称59FPS或已经证明全部来自同一listener。

每次成功Audit第一轮遍历C座TestPlayer城市，每城candidate调用RecipientSources。
NetworkBridge.currentView先Refresh，再读取缓存。
Refresh→NetworkInput.Capture遍历该玩家全部C座城市，并调用EffectiveFacts.Read，重新构建输入与签名；相同签名的抑制发生在这些读取之后。
Audit第二轮再逐城reconcile。

在一个玩家、全部输入可读取、无工业来源额外读取、无其它并行counter贡献的简化条件下：
- query次数：C；
- EffectiveFacts读取：C²；
- city_scan计数：C²+2C（两次Discount循环加C次全国输入采集）；
- 完整derive可以为0，不代表上述工作为0。

|城市C|每Audit事实读取|city_scan|
|---|---:|---:|
|1|1|3|
|2|4|8|
|4|16|24|
|8|64|80|

双城实机窗口：18602 Audit×4=74408 facts；×8=148816 city_scan；×2=37204 query/cache_hit，逐项精确吻合。是静态调用结构与运行计数的交叉证据。地区扫描另有74408增量，不把它机械加入通用公式；区域数、身份读取路径、其它未计Audit模块可影响它。工业来源存在时还会额外读取来源事实和模板。

## 临时分配与持续占用不能等同

Capture反复建立cities/parts/ids/refs及字符串签名；EffectiveFacts/CityFlow读取、校验Property表并clone；Discount每轮建立targets/info/parts等，即使最后signature相同也已发生分配。这是分配压力的静态证据。正常可回收的临时对象也有这些行为；是否有对象被留存、原生绑定分配未释放或分配器暂留，现有材料不能确定。此前另一PID的MALLOC_TINY增长不能直接映射到本次Lua对象。

## 重要计数边界纠正

net_send只在NetworkSender增加，net_receive只在NetworkBridge增加。它们不是全Mod RequestPlayerOperation总计；send_inflight/peak同样仅代表该NetworkSender。
UI/DiscountEligibility.lua自身存在DISCOUNT_INIT、DISCOUNT_ELIGIBILITY发送，未增加这些counter。
未ready时每次refresh可请求初始化；已ready时signature不同或接收seq未追上就发送新seq，没有NetworkSender式单flight保护。SystemUpdateUI在未initialized时调用safe，publish/playback也调用safe。
这是一个待运行证据验证的重发风险，不能据截图宣布实际发生；也不能再以network send=0排除全部请求风暴。Gameplay对应Receive会在接受新seq时调用两次Audit，故触发来源仍需隔离确认。

## 下一步最小调查/实验提案（未实施）

优先分开检验：A 高频入口导致的重复全国事实读取；B 折扣请求未ACK时的重复发送。
若授权诊断build，可先以固定计数区分Audit调用来源及折扣INIT/ELIGIBILITY send/receive，不逐事件日志、不改收益；随后同一双城存档、同配置分别做单变量路径对照。不能同时关闭多个消费者或直接把HD列为根因。用户当前不需重做单城双城测试。

当前仅文档；无源码/配置/运行包改动，无游戏进程附加。关联：../../Status/Validation/Results/Specialization_Idle_City_Comparison_20260914.md。
