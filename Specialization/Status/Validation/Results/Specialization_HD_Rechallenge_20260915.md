# HD Core重新加入：增长复现与独立崩溃记录

Document Owner: Codex
Evidence: 用户2026-09-15提交8图/崩溃报告；人工逐图复核。仅develop文档，未改源码/部署。

## 当前结论

重新加入CORE后增长复现：第二次完整窗口316秒9.13→9.37→9.58GB，约+0.0854GB/min。与前轮ON +0.39GB/307秒、OFF −0.01GB/315秒构成ON/OFF/ON关联。此为RUNTIME EVIDENCE，不是HD单独根因证明或内存修复PASS。第一场被崩溃截断，不计算其增长率。

组合按用户执行本轮协议记为SPC+BTS+EMM+TITLE+AREA+Cheat+CORE；本批没有新启用列表原件，不能声称重新从Mod数据库确认。地图种子/AI名单未独立确认。截图均B072.99，Turn1/0城市、Cheat可见。

## 时间线（Activity Monitor Memory，不等同RSS）

|场次|截图时间|距本场首图秒|PID|Memory GB|Threads|Ports|audit_standard|send_inflight|
|---|---|---:|---:|---:|---:|---:|---:|---:|
|第一次/截断|05:45:02|0|68667|9.15|32|1454|557|276|
|第二次|05:49:53|0|69145|9.13|32|1479|446|222|
|第二次|05:52:39|166|69145|9.37|33|1477|10058|10127|
|第二次|05:55:09|316|69145|9.58|33|1479|18788|19123|

用户称第一次在约2:30准备截图时崩溃；报告精确时间05:46:55.9968，即首图后约114秒。保留两种记录，不改写用户计时起点。没有第一次终点内存，不推算崩溃时RAM。

第二次audit增18342，约58.044/s；send_inflight增18901，是单个未完成请求的发送抑制次数，不是18901个排队请求。三张均inflight=1/peak=1。facts/city_scan/district_scan/building_check/create/remove/property_write为0；derive/executed=0，requested=3；network send/receive=1/0；revalidate=2/route_scan=3/same_snapshot=2；其它Audit Lv3/Boost/Commerce/Copy=8/3/1/7，busy_skip=492均不变。无unit callbacks，runtime log仍FILE_API_UNAVAILABLE。

城市C²扫描不解释这段零城窗口。无HD对照Audit也约58/s，入口频率本身不能区分内存结果。Network send/receive只覆盖该桥，不能推广为所有Mod所有请求为0。三个采样点递增，不声称逐秒严格单调。

## CRASH INCIDENT（与memory分开）

PID68667，2026-09-15 05:46:55.9968 -0700，EXC_CRASH(SIGABRT)，SIGNAL6，abort() called。Thread5 TBB(WinID7)：__pthread_kill→pthread_kill→abort→abort_message→__cxa_pure_virtual→Civ6 offset9223148→libtbb。

与此前2026-09-14 21:25:30 PID39989记录的pure-virtual/offset9223148特征一致。说明重复的原生崩溃签名，不证明相同触发条件、同一对象或与内存增长同根因。未见明确OOM终止依据；无符号游戏地址无法定位Lua/Mod。另一个未崩溃线程包含Metal/overlay绘制栈，不据此归因Steam overlay。第二场完成316秒窗口未见崩溃。

## 下一步：只做去掉SPC的对照

保持CORE、BTS、EMM、TITLE、AREA、Cheat，去掉SPC。完全退出再启动，新局Turn1/0城，同速度/地图设置/垄断模式/窗口焦点条件，0/2:30/5分钟Memory截图即可；不需要不存在的Specialization counters。

SPC测试领袖随Mod移除不可选，采用原版苏格兰/罗伯特作为最接近替代，明确这是无法保持相同的配置项（不把结果当严格同领袖单变量）。若不再增长，下一轮再让有/无SPC都用相同原版领袖确认，避免误把测试文明差异当全Mod交互。若仍增长，说明SPC在该新局条件下不是复现必要条件，但不能证明原55GB incident全部同源。先不要求这两个后续实验。

## 归档与边界

外部W/Specialization/Status/Validation/Evidence/HD-Rechallenge-20260915-0545/：8张PNG原名移动、Crash-report.txt从用户附件复制、manifest.json记录SHA256；9证据文件共55098383字节，逐份校验。W按外部路径合同解析。未将截图/崩溃全文加入Git，未读取新session日志冒充崩溃进程日志。当前没有归因结论，Discount优化/C/D保持暂停。
