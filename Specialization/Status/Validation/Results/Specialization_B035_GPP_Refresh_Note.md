# B035 GPP刷新延迟：用户接受备注

Document Owner: Codex
Disposition: ACCEPTED_OBSERVED_DELAY / NO_FIX / NO_ADDITIONAL_TEST

用户明确回报：同回合移出一名专家，carrier可由4立即变成2，但原生界面和报告的全国GPP均保持18；过回合后二者更新为12。目前用户未找到玩家操作回合中可触发实际GPP读数更新的方式。

这是已观察到的刷新行为；不能据此定位为纯UI缓存或断言底层实际结算延迟。报告读数与UI保持同步。不得将carrier立即变化等同于GPP立即变化。用户明确无需修复/改进/补测，B035 PASS保留，不作为后续开发阻塞。与住房情况类似，但不假定住房的同回合刷新操作也适用于GPP。
