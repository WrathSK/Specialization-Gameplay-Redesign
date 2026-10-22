# B152.179 — P0-L2B基线入口受阻

Evidence: USER_GAME_TEST_BLOCKED_ENTRY；STATIC_CONFIRMED。四态Culture追加/旧Dialogue倍率比较 **NOT_TESTED**，不能判Floor失败、原生接口不支持或正式意义延展失败。
Baseline: develop `223503ec`；runtime source `85c77b4`，B152.179 / modinfo179。D0039/Culture D0038规则及原38 Meaning＋26 K LOCAL结果保持原证据范围。本轮只记录截图、定域源码核对和停止点，不实施修复。

## 截图直接证据

2026-10-03收到一图，已逐张查看并原样移入Git忽略目录 `local/legacy-workspace/Specialization/Status/Validation/Evidence/B152_P0L2B_Entry_Blocked_20261003/`。manifest记录原名、大小、SHA256与本结果；移动前后1/1 MATCH，无原图进Git。

T62，EDINBURGH (TEST)选中，按钮显示文化4级；报告版本P0-B-152.179、ACK，阶段“①基线：追加0／旧对话0%”。每件配置+0科研/+0金币/+0文化；**旧对话为未确认，并非已实测0%**。报告依次显示：

- `ME_DIALOGUE_SAMPLE_PENDING`；
- 操作未完成 `[ADVANCE]`，`CultureMeaningProbe.lua:61`转抛 `ME_DIALOGUE_UNCONFIRMED: missing current projection`；
- `ME_UI_CONFIGURATION_PENDING`，不记录成功基线。

没有有效的原生基线、W/D完整输出或C10/C11/C01差值。文化4级标签不单独证明ACTIVE4；ACK只证明回复，并非操作成功。图中阶段已设BASELINE，不能说失败已自动退回OFF或旧系统已恢复；新片段配置0也不能证明旧对话已成功撤销。本轮不要求追加截图或继续四态。

## 已确认的源码与测试缺口

1. [Dialogue Hold/Audit](../../../../Mod/Dialogue.lua)（34–43、58–92）先绑定override，调用Audit后立即验证`last`。Audit遇ready/busy/玩家门禁可早退；调用方没有确认本次更新实际执行。外层取城市/遍历等步骤也没有统一异常收尾。**不允许用无条件清busy绕过真实重入。**
2. 第42行的断言同时检查p存在、无错误、`meaning`及`applied`。`missing current projection`也可来自存在但仍为普通旧投影/百分比不匹配的p，不能据字符串断言p必为nil。第97行同样把多种未确认状态合并为`ME_DIALOGUE_SAMPLE_PENDING`。正常Audit缺馆藏会留下`DIALOGUE_COLLECTION_PENDING`；本图没有证明具体busy、样本或epoch值。
3. [实际采样入口](../../../../Mod/Gameplay.lua)（219–230）先`GreatWorkFacts.Receive`；[事实通知](../../../../Mod/GreatWorkFacts.lua)（165）同步OnConfirmed，由[Meaning回调](../../../../Mod/CultureMeaningProbe.lua)（238–242）触发Audit；之后才`Dialogue.Receive`。因此新事实与旧对话样本可能暂时不同步。Dialogue成功接收后没有显式Meaning重新确认，当前确认也未绑定同包Seq/Generation。**这是STATIC顺序风险，不是截图唯一根因已证实。**
4. [当前测试fixture](../../../../DevelopmentTests/test_culture_meaning_probe.py)（81–93）mock Summary并直接预装`dialogue.samples`；真实操作请求测试覆盖Meaning按钮，而非完整`DIALOGUE_SAMPLE→Facts回调→Meaning→Dialogue`链。未覆盖Hold遇busy、旧非Meaning投影、外层异常收尾或两份样本成对确认。原LOCAL PASS不改写为当时已查过这些路径。
5. [UI拒绝采基线](../../../../Mod/UI/BoostGreatWorkRead.lua)（103–107）是正确的未知保护，本次不放宽为0，也不吞掉失败。B150漏ImportFiles的旧故障不能直接套用；本次已到达Meaning/Dialogue实际函数。

**结论：** 确定失败为“Dialogue当前Meaning投影无法确认”；busy早退、旧投影/采样时序是需定域验证的候选。未取得引擎内部时序，不宣布其中任一已被原生证实。

## 建议的最小修复范围 — 尚未授权

- Dialogue Hold明确区分未执行/执行失败/投影不匹配，并保证自身Audit异常收尾；当前事实、精确owned载体及健康检查保持。
- 检查实际采样入口，只有本次新事实及Dialogue各自可靠接受后，才定域通知当前fixture重算；不能把同包确认改成全城扫描、无限重试或默认成功。
- 补真实采样入口、busy/旧投影、冷启动及跨turn的少量定向回归；按W0004相关L2/L3，不跑旧全回归/长测。实现的具体时序须在授权修复时核对，不在证据批次先改逻辑。
- 诊断优先显示当前失败原因/阶段，完整路径/trace仅详情；未知不记录基线。无需改D0038 Floor公式、资格规则、SQL收益或GC。

修复并安全部署后，先让同城C00正常确认，再续既定最小四态测试；本轮不要求重试。精确recipient接口仍是独立TECHNICAL_INVESTIGATION_REQUIRED，不因入口修复宣称解决。完整L2/全局cutover、L3/M/N/U2未授权。

## 运行包与停止点

source/live仍B152.179；已有W0003 receipt `B152.179-85c77b4-playtest.json`的DEVELOP_ACTIVE/182 MATCH仅按既有记录引用，本轮没有重新核验外部包。没有游戏启动/关闭、部署、Mod/Design/GC/永久状态/main变更，没有运行玩法测试或模拟。

用户已中止本次测试；下一建议是上述定域入口/同步修复，**等待单独修复授权**。本次不会推进实验、自动修复或开启下一能力；未知实验退出状态不写成已恢复AUTO。原[S0391 LOCAL检查点](Specialization_B152_P0L2B_Gates_Local.md)与B151整数证据保留。
