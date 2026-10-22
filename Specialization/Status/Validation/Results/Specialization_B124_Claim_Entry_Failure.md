# B124.151 — Claim入口失败与城邦取得范围缺口

2026-09-29，三图逐张读取，原图移入外部 `Specialization/Status/Validation/Evidence/B124_Claim_Entry_Failure_20260929/`，manifest记录原文件名及SHA256，3/3移动前后一致。不是全部Claim流程验收。

## 实际观察

1. `Screenshot 2026-09-28 at 9.48.50 PM.png`：B124.151，尼德罗斯0/262147，取得已确认、冻结商业、Potential0/ACTIVE0/投资0、已登记5。生产列表四个认领均灰，包括应可用的商业；报告无Claim模块预期“认领：…”行。用户确认该城先征服获得商业候选，之后建工业验证不会扩候选。候选保留符合规则；正式入口 **USER_GAME_TEST_FAIL**。图没有hover禁用原因，无法从图确定marker未挂、初始化未完成、事件回调未到或其它生产资格的精确根因。
2. `Screenshot 2026-09-29 at 4.01.00 AM.png`：日内瓦，征服消息；E2明确 `ACQUISITION_AI_MAJOR_REQUIRED`、登记尚未确认。用户说明原Owner为城邦。代码CityProgressionStore.admit要求old:IsMajor()==true，直接解释该拒绝；不是已得到空LegacySet，不得走空集first-completion代替。
3. `Screenshot 2026-09-29 at 4.01.32 AM.png`：同城专业报告 `FOUNDATION_EVIDENCE_PENDING`，EffectiveFacts/CityFlow读取堆栈外露。属于尚未登记后的下游读取失败；应简明呈现，不要求用户抄堆栈。

## 范围与依据

B110实现合同及其本地测试明确限原AI major，并拒绝nonmajor；本次城邦超出已经验证/实现的路径。Design PROG-006针对原Owner未建立专业的征服城市，并无Major-only排除；Culture人文考察的城邦排除与城市征服无关。不能将实现门槛说成正式Gameplay禁止城邦。补齐城邦来源验证仍需明确实施授权，不给城邦AI启用专业能力。

本地B124测试PASS保留为模拟证据，不能替代实际入口失败；测试中的mock事件与marker操作并未证明引擎入口就绪。当前可用日志未取得本次Lua异常，不能声称已定位首个模块启动错误。

## 建议下一窄修复（未实施）

- 先定位Claim模块启动/Load就绪/访问marker回读链，给当前城输出简短入口状态与确切错误；恢复合法商业入口，不修改冻结候选，不改生产收益或计时规则。
- 将征服城邦作为现有PROG-006合同下的缺失来源路径单独验证：仍要求真实转移证据、未有专业历史、当前本地玩家；不把Free City/交易或不明Owner一并放开，不新增cityKey/AI专业化。
- 专业报告对未登记取得显示原因，避免长堆栈；保留失败保护。

PT013暂停；未测试启动/完成/保存，不标PASS。无需重复当前失败流程。保留认领前及征服日内瓦前存档供修复后使用。本轮仅证据/状态记录，无runtime修改、部署或游戏启动。等待修复授权。
