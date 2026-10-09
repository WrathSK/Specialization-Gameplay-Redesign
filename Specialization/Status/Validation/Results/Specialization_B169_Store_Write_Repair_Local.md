# B169.196 — Store保存层定域修复本地检查点

Date: 2026-10-08 / America/Vancouver
Evidence: **STATIC_CONFIRMED / LOCAL_SIMULATION_PASS**；**NOT_DEPLOYED / USER_GAME_TEST_REQUIRED_AFTER_DEPLOYMENT**。
Source: `943f26c46a9667e06800235c7db2ff2fb5f20f8c`；modinfo196。外部运行仍登记B168.195，本轮未读取或修改运行包、存档或游戏配置。

## 本次完成与边界

用户接受[原计划](../../../Reports/Proposals/Store_Write_Repair_Plan.md)，只处理IA-P06a-F01普通写跨record成本、相邻F02坏引用隔离和必要的失败占用。用户补充的普通写异常读回边界已纳入实际Store；不重新开启其它审计项。

[Store](../../../../Mod/CityProgressionStore.lua)保留完整validator、manager旧snapshot比较、Game旧值比较、写锁、setter/readback和成功后副本。有效引用按字段存在性取`loss.target → current → origin`；false／错误shape不能回退。仅可靠不变引用的普通写跳过唯一性全表检查；恢复、新登记、有效引用变更仍检查。未新增save字段、schema、cityKey或全量反向索引。

[Architecture保存合同](../../../Architecture/Specialization_v0.1_Architecture.md#store普通写与故障占用b169)记录现行实现；原审计报告、原复现脚本、raw result和冻结结论均保持原样。F03、提交可见性Q01、return顺序Q02、Research跨Owner规则、GC、事件／缓存架构等未处理。

## 普通写成本与逐值对照

固定修复前source `cdd3ceb8b401c5cbe4d58cbbdbc7998b1edddeb7`，同一实际Store fixture、全部计龄城ACTIVE1。N=持久记录数；T=本次真正计龄写入数。访问计数为唯一性循环返回的record条数（含本城），初始化／注册／load不计入本次普通写窗口。

| N / T | 修复前唯一性访问 | B169唯一性访问 | 实际record写次数，前→后 | 完整记录逐值 |
|---|---:|---:|---:|---|
| 8 / 8 | 64 | 0 | 8→8 | MATCH |
| 20 / 20 | 400 | 0 | 20→20 | MATCH |
| 40 / 40 | 1600 | 0 | 40→40 | MATCH |
| 40 / 1 | 40 | 0 | 1→1 | MATCH |

对照比较每条完整record的确定性编码，包含年龄、revision、Identity、Potential相关记录、投资收据及绑定；计龄结果保持age1。同回合重复不新增写；同回合真实投资、模板增量、Claim timer变化可继续保存，控制城逐值不变。可靠保存重建后记录保持，未改变现有年龄模型对合法下一回合的结算。

**这不是原生CPU／内存改善证据。** worker遍历、完整校验、目标record复制和原生写入仍存在。B169目标读回经有界Copy以取得可靠证据，不能宣称分配总量下降或全部扫描归零。本批没有新增常驻计数器、调整GC或用户内存长测。

## 实际读回驱动的故障保护

以下均为本地实际Store注入，非已发生玩家存档事故：

| 证据／故障 | 实现结果与已测边界 |
|---|---|
| 普通写／引用变更，可靠读回原端点，包括业务字段第三值 | 目标worker hold，不晋升candidate；不扩大UNKNOWN；其它正常城投资／不变引用写继续，安全的新登记可继续 |
| setter抛错但已应用candidate，读回可靠候选端点 | 仍判写失败；保留候选占用，manager旧snapshot保持；不能把成功读到candidate当setter成功 |
| 普通写／引用变更读到第三端点、不可解析shape或getter／Copy失败 | 有限session UNKNOWN阻止无法证明安全的新登记／引用变更；不误放行；其它正常城不变引用写仍可继续 |
| 写前stale／读错 | 同样按实际端点分类；setter没有执行不代表实际占用仍然已知 |
| silent-drop／throw-before，可靠读回旧值 | 保留旧权威、目标hold，不额外占用一个未发生变更的候选端点 |
| 可靠nil与读取异常 | nil仅保留已有旧引用或初次index登记端点；读错为UNKNOWN，不混成缺record或首次初始化 |
| 初次record提交失败／City token写失败 | index／位置保留；不补造旧record，登记端点保持占用；可靠缺record跨load仍hold；未知拒绝结构写 |
| load current/loss/target为false／错误table／错误ID | 原件保持，目标hold；正常对照城仍可读写；UNKNOWN不按部分字段猜引用 |
| bad revision但引用可靠 | 目标hold但引用仍占用，不能因为worker未ready就放弃碰撞检查 |
| 真实load碰撞／坏index | 维持collection hold；load无写入 |
| candidate碰撞 | 拒绝目标写；旧Game记录保持，控制城正常 |
| 实际失城→夺回、Governor变化、重复通知 | 依现有身份／binding证据重算；无重复写，冲突夺回被拒绝；不引入新的恢复猜测 |

reservation只覆盖held／不完整登记token，每个token最多一个候选端点和UNKNOWN标志；正常已提交记录继续只用envelope。成功确认清除session条目，重新加载从实际可靠记录重建，不持久化失败candidate或自动重试。未知可能占用任意端点时，结构写保守拒绝；不承诺损坏存档下所有动作均能继续。

## 本地验证与可重跑入口

- [新定向runner](../../../../DevelopmentTests/test_store_write_boundaries.py)：**18个unittest方法、48个subTest PASS**。测试内定点注入唯一性计数与私有只读快照，生产无新测试API；故障用私有storage精准注入，正常写／失败hold／投资／计龄／模板／Claim timer／易主使用实际worker和consumer入口。
- 同一runner包含B127的3组、B128的11组原断言。这14组是两个方法内部的既有Lua分组，不虚算为48个subTest。仅排除B128已被B140取代的旧工业“首次认领仍缺模板历史”组，不宣称整个历史B128通过。
- [B140模板](../../../../DevelopmentTests/test_b140_templates.py)与[B143传统](../../../../DevelopmentTests/test_b143_tradition.py)完整定向入口PASS：初始化／union／历史保护、投资与收据、UNKNOWN、owner hold、冷加载、失败恢复；既有业务断言和文件未修改。
- `test_b142_templates.py`因未配置外部DB未执行（NOT_RUN_DEPENDENCY）；其目录SQL专项不是本批修改路径，不读取游戏目录补环境，也不把未运行写成PASS。
- 修改Lua语法、modinfo196 XML与B169.196标识一致；当前context/schema/selector及self-test PASS（186运行源文件／473锁定文件），helper定向3项PASS，变更Markdown的356个本地链接／锚点零失败，diff空白检查通过。没有运行全历史回归或stress，未启动游戏。

本地需Python与已安装`lupa.lua55`（通过现有环境提供，不写系统Python），保留上述Git基线对象。一般命令：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_store_write_boundaries.py
PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_b140_templates.py
PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_b143_tradition.py
python3 Specialization/Workflow/context.py check Store-Write-Repair
python3 Specialization/Workflow/context.py self-test Store-Write-Repair
```

当前批次[manifest](../../../Workflow/Store-Write-Repair.json)使用既有结构；helper只登记该名称的命令行选项，未改schema、选择器或验证策略。Context Lock仅更新本批已审变化；Runtime Index只更新Store与两个包标识文件，不追齐其它历史manifest。

## 后续一次最小实机流程

**当前无需测试：B169尚未部署。** 后续经有效部署授权及游戏退出／干净源码／receipt／恢复点门禁切换后，只做：

1. 读取现有从开局启用Mod的支持存档，查看两座城；尽量一座已有科研传统，记录Identity、Potential、投资／模板／年龄中的已有项。
2. 过一个正常玩家回合，并在一座城做一次本来合法的投资或其它现成永久记录写入。确认目标按规则变化、对照城无异常。
3. 保存独立副本，完全退出后冷加载一次，确认两城相关记录保持、能力正常。

这一次区分“修改后的写入及load检查是否被真实Property保存／恢复正确承接”；本地无法证明原生存档路径，因此保留该步骤。故障shape／未知占用反例全部留在本地，不增加用户实机步骤；无需重测所有易主、40城、Probe默认OFF或反复启用。B168 GPP待办独立，不由此替代或自动恢复。

## 停止点

本地实现与检查点完成，未部署、未promote、未修改Design语义或永久归属。保存schema未变；本地兼容对照不自动成为所有原生存档兼容保证。下一步仅处理本批后续安全部署／一次最小验收，等待用户安排；不自动推进其它审计修复或玩法批次。
