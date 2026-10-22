# B072.99：无城市 / 建城 / 双城静置对照

Document Owner: Codex
Evidence: 用户实机截图10张，逐张复核；同一PID 41293。
Build: P0-B-072.99 / modinfo99

## 结论与边界

用户确认沿用前次缩减Mod组合（见Specialization_Crash_20260914_212530.md的11个第三方项）；这是用户确认，不以安装目录推断启用。此次没有重新独立捕获加载清单。

无城市静置也有内存增长，因此本地城市扫描不是所有增长的必要条件。双城静置317秒，Activity Monitor Memory增加1.14GB，Discount检查增加18602，恰好对应74408次事实读取、148816次城市扫描、74408次区域扫描、37204次Network查询/缓存命中。完整derive、建筑写、Property写、send/receive全部无增量。重复工作已被运行时证据确认；内存因果与具体Mod归属仍UNKNOWN，不能宣布泄漏定位或修复。

STATIC_CONFIRMED指代码静态证据，不等于游戏验证：StandardizationDiscount.Audit在入口增加audit_standard，早于ready/busy判断；挂接GameCoreEventPublishComplete。NetworkBridge在共享缓存命中之前仍采集完整输入事实。故零城市的Audit计数不代表完成同数量昂贵城市处理；缓存命中也不代表无需扫描。此轮不修改实现。

## 五组时间线

时间为2026-09-14当地截图时间；内存保持Activity Monitor的Memory/GB口径，不改称RSS。数值显示有舍入。

|组|时间|阶段（用户描述）|Turn|Memory GB|线程|端口|
|---|---|---|---:|---:|---:|---:|
|1|21:32:19|进入新局，未建城|1|9.23|32|1501|
|2|21:38:35|无城市静置|1|9.59|32|1501|
|3|21:44:24|原地建城后静置，未过回合|1|10.10|33|1508|
|4|21:46:55|持续操作、推进回合并建立第二城|19|11.87|33|1508|
|5|21:52:12|双城静置|19|13.01|34|1493|

|区间|秒|Memory增量GB|约GB/min|解释|
|---|---:|---:|---:|---|
|1→2|376|0.36|0.057|无本地城市静置|
|2→3|349|0.51|0.088|含建城过程；缺少刚建成瞬间基线，不能作纯单城静置斜率|
|3→4|151|1.77|0.703|混合操作及18回合，不归因第二座城市|
|4→5|317|1.14|0.216|用户描述纯静置，可做同窗counter对照|

全窗1193秒，+3.78GB；所有截图routes=0，不能把这次问题归因于实际商路数量。

## 累计counter转录

使用面板current/total中的total跨Turn比较；不是把Turn1 current与Turn19 current相减。

|累计项|1|2|3|4|5|
|---|---:|---:|---:|---:|---:|
|audit_standard|1324|23823|44684|50847|69449|
|EffectiveFacts|0|0|57|29434|103842|
|city_scan|0|0|41213|180543|329359|
|district_scan|0|0|41150|55412|129820|
|building_check|0|0|4030|3181454|3181454|
|building_create/remove|0/0|0/0|0/0|0/0|0/0|
|property_write|0|0|7|14|14|
|net_send/receive|1/0|1/0|1/0|2/1|2/1|
|derive_requested|3|3|20587|29015|66219|
|derive_executed|0|0|0|3|3|
|cache_hit/miss|0/0|0/0|0/0|7248/3|44452/3|
|input_duplicate|0|0|0|7571|44775|
|send_inflight|547|23046|43906|44937|44937|
|send_timeout|0|0|0|1|1|
|route_scan|3|3|4|74|74|
|route_revalidate|2|2|5|131|131|
|unit_callback|0|0|4|6380|6380|
|audit_lv3|8|8|16|2160|2160|
|audit_boost|3|3|3|644|644|
|audit_commerce|1|1|4|740|740|
|audit_copy|7|7|13|1183|1183|

1→2：audit_standard与send_inflight均+22499（约59.84/s），facts/scans仍0。
4→5：audit_standard+18602（约58.68/s）；facts=4×、city_scan=8×、district_scan=4×、query/cache_hit=2×该增量。其它表列Audit无变化，route扫描/发送/建拆也无变化。完整Network共享计算仍有效，但输入读取与Discount入口重复调用未解决。

## 初始化等待不是队列长度

前三组inflight=1、peak=1，网络revision=0，发送1/接收0；后两组inflight=0、peak=1、revision=1，发送2/接收1。
NetworkSender对同回合未ACK的单个flight增加send_inflight后返回；跨回合才记timeout并清理。因此43906是跳过发送次数，不是43906个待发请求，也不能直接据此断言原生队列膨胀。截图说明Turn1长时间未完成握手；为何没有ACK仍UNKNOWN。第4组已跨回合、timeout累计1，只能说与该路径相容，不能仅凭截图恢复精确事件顺序。

## 后续调查顺序（未实施）

1. 定向检查Discount为何近60Hz进入，以及在输入未变时为何重复获取事实；保留真实更新语义。
2. 独立检查新局Turn1后台请求为何等待至推进回合，避免将抑制次数当队列。
3. 若获准实验，使用同配置控制单一检查路径做内存对照；不能同时改多模块或直接归咎HD。

此前另一PID的MALLOC_TINY增长属于独立证据，本组没有footprint分类，不能直接套用。FILE_API_UNAVAILABLE仍存在，不宣称自动日志可用。无需重复此五组测试。

## 原件与归档

外部W/Specialization/Status/Validation/Evidence/Idle-City-Comparison-20260914/；W为游戏application-support工作区。10张原图55734202字节，按原名冻结，manifest.json保存逐文件SHA256；移动前后全部一致。每组带(2)的是Activity Monitor，另一张为游戏counter。原图不进入Git。未更改源码/Design/运行包/配置，未启动或附加游戏。
