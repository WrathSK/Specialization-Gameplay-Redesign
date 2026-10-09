# B173.200 — 馆藏消费者通知隔离与有限补发

Date: 2026-10-08。Source baseline: develop a12fdce / B172.199。用户已批准P13a-F04定域修复，并与巨作启迪合并验收。**LOCAL_SIMULATION_PASS；USER_GAME_TEST_REQUIRED**。实际live以Status/receipt为准；本地完成不代表部署。

## 已修复的范围

[原审计P13a-F04](../../../Reports/Audit/Specialization_Independent_Audit_Ledger.md#ia-p13a-f04--mediumgw多消费者通知依赖隐式单callback包装顺序)及[W04冻结反例](../../../Reports/Audit/Evidence/W04/callback_isolation_result.json)保持原样：先前单个OnConfirmed包装链，前置异常可阻止后续；同内容新seq不能补投。B172保护了新Inspiration，但旧AE→Meaning链仍存在。

- GreatWorkFacts以具名、启动期注册替代单callback；按注册顺序独立pcall，三个消费者不再调用前驱。不新建通用事件总线、持久订阅或动态发现框架。
- 每个消费者只保留当前城市的待通知条目（owner/reference/epoch/尝试边界），不保留旧馆藏/收益/事件历史。新有效采样只合并当前变化城市和该消费者失败项；相同内容的新seq能补投失败者，成功者不重复。无效、重复、foreign、旧epoch/input包不触发补投。
- 通知前核当前Owner/reference；可靠失效即裁剪，暂时读取失败保留待核对，不猜0。Reset/confirmed loss后的epoch边界清待通知；Shutdown丢弃订阅与待处理。消失城市的效果退出仍由既有Store/module-owned路径负责，不保留可重放到新城的旧ID tombstone。
- 同步新样本不递归调用消费者；合并后最多立即补一轮。补轮中再来的工作留待下一有效采集；普通异常不会原地重试。每帧pulse只沿旧producer协议，不因通知失败增加采集或传输重试。
- 消费者实收独立ID列表，诊断只返回副本；错误按消费者保留且长度有界。巨作事实报告仅异常时显示“馆藏通知待重试：能力名”，详细页可查原因；没有新面板/常驻诊断。
- Gameplay现有Meaning/Inspiration启动兜底不再在同包绕过待通知错误重试，并各自pcall；一个能力的异常不阻断旧Dialogue样本配对。该相邻路径是真实直接调用依赖，不是投资传播改造。

**证据边界：**采集ACK只证明相应处理/验证；通知函数正常返回不代表内部逐城writer成功或原生收益入账。模块已捕获的业务错误、BUSY、UNKNOWN、carrier回读/撤销继续由模块处理，本批没有把它们转成公共重试任务。永久Property/schema、三个公式/ACTIVE规则、SQL、采集器/UI producer、GC、其它专业不变。

## 实际修改与回归

运行源码：GreatWorkFacts、CultureAesthetic、CultureMeaning、CultureInspiration；Gameplay只改两项启动兜底的调用隔离；Probe/modinfo升B173.200。没有新增运行文件/载体。

定向入口：[test_great_work_notifications.py](../../../../DevelopmentTests/test_great_work_notifications.py)。复用实际Lua接收器、现行Gameplay请求、实际三个writer及现有K/Shared D fixture；外部DebugGameplay只读复制到内存。三个现行test文件只适配注册接口及对应异常反例，数值/退出断言保持。旧Probe/frozen audit原件不改；历史固定modinfo199断言未执行，由本批version200/完整package检查替代，不宣称全历史全绿。

**81方法 / 44 subTest PASS，0失败、0错误、0跳过**：21新通知/三消费者集成用例；B172现行23方法（旧package版本断言除外）；K原有26方法；Meaning5、Aesthetic6。覆盖：

- 首/中/末任一订阅者异常，其它两者继续；下一同内容有效seq仅重试失败者；重试用最新事实。
- 错包/旧包/foreign不补发；真实同回合变更与两城作品移动；UNKNOWN不激活/不清成0；重新出现的正确事实恢复。
- 双端Owner/ref变化、confirmed loss、Reset/Shutdown/会话替换；永久账本不写；其它城市错误不被成功者抹去。
- 同步重入不递归、至多一轮catch-up，持续失败待处理条目有界；启动兜底不能同包再次触发失败回调，不能阻断另一能力/旧样本配对。
- 实际三个文化收益投影、B172 E0–7/各门槛、先撤后加、失城/冷重建与原有回读失败保护保持；业务失败仍可见，通知成功不能掩盖它。

结构计数：三订阅者×三个变化城首次各投递一次；单订阅者失败后同内容新seq只增加它的一次投递；12次重复失败始终3个待处理城市，其它订阅者仍只执行1次。12次idle pulse不增加采集、发送或通知调用；一次同步新样本案例A执行2次、B执行1次、最大调用深度1。都是本地路径证据，**不换算原生CPU/内存改善**。

初次集成未配置外部DB，工具明确报缺依赖；随后复用main现有配置的只读路径完整执行，不安装依赖、不修改外部数据库。Lua/189文件package、318个活动文档链接/锚点及diff检查通过；context/schema/selectors/hash在具名review后同步检查。不跑全历史或大规模stress。

## 与巨作启迪一次验收

沿用[B172一次session](Specialization_B172_Inspiration_Automatic_Local.md#一次最小实机验收)，用B173包一次完成，不分别重复两批测试。

1. 正常Culture ACTIVE IV城，固定现有GPP来源，查看巨作启迪：当前E应配置3E%。如读数延迟，过回合看伟人界面/报告；全国读数不当作本城基数。
2. 移入一个不同合格时代：E+1、配置多3个百分点；同次观察风雅熏陶按时代更新、意义延展按作品件数更新。追加相同时代作品不再增加启迪倍率。报告足以说明时无需另截整套图。
3. 将合格作品临时移到非Culture ACTIVE IV城：E0配置撤销，按实际刷新时机看收益回落；搬回恢复当前事实。顺便看其它两项正常退出/恢复，不额外重做独立流程。

这不是额外的保存→手动OFF→退出→冷加载→再启用测试，也不要求人工制造Lua异常。已有未改persistence/owned withdrawal的实机证据继承，本地覆盖本批通知失效/重入。GPP百分比实际入账/叠加仍需用户当前观察，不能由通知测试替代。

## 保留边界与停止

P13a-F04的静态订阅/通知异常隔离/下一有效采样补投在本地完成；未声称统一处理所有业务失败或所有事件链。P13a-F02全建筑定义扫描、P13a-F03投资提交传播、P08机械writer公共化仍开放且不在本批。原独立审计证据不改写。

本批不改Design、main、GC或保存schema，不推进M/N/U2。按W0003既有门禁部署后停止，等待与巨作启迪合并的原生验收；游戏运行/退出不明时保留本地检查点，不替换运行包。
