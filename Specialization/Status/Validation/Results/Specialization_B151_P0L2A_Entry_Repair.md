# B151.178 — L2A导入与请求入口修复

Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS；USER_GAME_TEST_REQUIRED。本轮用户明确授权B150入口最小修复；不授权L2B。
Baseline: develop 6af9ef6，原source/live B150.177 c66b053。[B150入口失败原件](Specialization_B150_P0L2A_Entry_Blocked.md)与[原探针范围/流程](Specialization_B150_P0L2A_Local.md)保持。

## 最小修改

| 文件 | 修改 |
|---|---|
| Mod/SpecializationP0.modinfo | 两个Meaning Lua加入现有SPCP0_Common ImportFiles；版本178。总Files仍精确182文件含modinfo，SQL/定义不变 |
| Mod/Gameplay.lua | 每次有效Meaning请求清掉旧View；CITY/MODULE/ADVANCE/VIEW/DESCRIBE阶段及240字节有界单行错误；操作失败与后续读取失败分别保留 |
| Mod/CultureMeaningProbe.lua | Describe允许复用本次View，入口只读一次；writer/模式/退出/事实与模型不变 |
| Mod/Probe.lua | P0-B-151.178版本标识 |
| DevelopmentTests/test_culture_meaning_probe.py | 导入名单约束、移除任一导入负例、执行完整实际request函数的正常与失败覆盖；未复制一个替代handler |

View在本次读取和描述都成功后才附当前token发布。Advance拒绝或配置UNKNOWN不会成为成功基线；临时view.error只影响这次报告，不修改probe状态。READ没有Advance或收益写入。没有新增请求、事件、轮询、GC、永久数据或诊断历史。

## 本地验证与边界

- 25项定向真实Lua55/SQL测试PASS：原18项模型/受控写入/互斥/UNKNOWN/loss/load加7项注册/实际请求测试。两个后续细化的入口测试重新定向通过。
- 注册负例在可丢弃XML中删除任一Import，保留总Files仍必须失败；真实fixture后续include受实际导入名单限制。**这是注册与模拟可见性证据，不是原生VFS实测。**
- 实际完整request函数验证prepare→READ→enable→end、每次只读一个View、READ零写、其它城与永久token保持；城市/模块/缺方法/异常/错误View/错误报告、混合Advance+View失败、新token、清旧读数、有界错误及配置未知均覆盖。
- 本机只读DB现已含B150定义。第一次执行因重复Types INSERT未启动测试；修正仅内存副本中精确10个probe载体/70个附件的重建，随后25项PASS。外部DB未写入，没有放宽SQL断言。
- 三个改动Lua语法、Python语法与XML/注册检查PASS。Context/selector/hash、相关活动链接与diff在提交前核对。
- 原B150的15项L1、26项K及分发结果按未变源码/合同保留，本轮不重新跑完整玩法/历史/stress；它们不证明曾漏掉的导入路径或原生精度。

已补确认的打包缺陷，不声称已排除本局所有引擎异常。B150具体启动失败行仍未取得；修复后若失败按具体阶段继续定域判断。

## 续测入口

使用未开启probe的存档副本冷启动，在同一Culture ACTIVE4且有已确认合格作品的城市，左键“意义延展验证”一次。应显示“基线：旧相邻暂停，测试收益关闭”、实际W/D、载体配置及原生基线；若报阶段/错误就停并回传该页。

基线成功后，继续[既定单城流程](Specialization_B150_P0L2A_Local.md#一个最小实机流程)：第二次左键启用、右键只读，原生0.5/1.5/4.5仍待测。不要因ImportFiles或挂载成功宣布精度通过，不自行Floor。不要求重做L1旅游、E2、旧长测。加载/失城等未实测边界仍保留。

本批修复完成后按W0003安全门禁部署，实际source commit、receipt与live只查[Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state)。设计、模型、SQL/收益目录、GC/永久成果、main不改；到L2A门禁停止，不进入L2B/L3/M/N/U2。
