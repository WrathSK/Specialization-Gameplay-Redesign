# B035 用户人工通过与投资上限补充

Document Owner: Codex
Build: P0-B-036 / modinfo45
Status: USER_GAME_TEST_PASS（用户明确人工确认，按以下范围）

## B035 GPP

用户说明测试数量较多未截图，“结果都正常”“B035pass”。按当前B035_Four_Family_GPP.md批次登记四类专家点数、文化三类、人数变化/总督撤销恢复/读档通过；此部分全部是用户人工回报，不伪称有GPP截图或逐步原始数值。

用户另明确验证：平伽拉本城+100%伟人点数、古典共和全国+15%、文艺赞助人政策卡均可影响点数。人工验算文艺赞助人25%和古典共和15%合为40%（额外百分比，非总倍率0.40）。这是本次组合观察证据，不证明所有Modifier collection、生效范围或所谓层级；不推出平伽拉与二者的三重叠加顺序，也不证明宜居度/其它收益百分比具体内部算法。用户明确不追加测试，仅记录。

## 专业进阶及Lv4上限

用户明确回报移民投资和总督等级可正常使专业达到4级；登记已测进阶状态通过，不等于未实现Lv3/4能力通过。

唯一截图11.11.44显示精简9按钮面板，标题SPC P0-B-036 | B035 GPP tests，报告B033 REJECTED: POTENTIAL_CAP_4及InvestmentAction.lua:48调用栈。截图证明Prepare拒绝显示，不单独证明Confirm结果。用户明确回报Confirm后移民未消耗、投资未升至5，作为补充实机PASS。

STATIC_CONFIRMED：InvestmentAction.Prepare先清空plans与InvestmentPreview，再检查potential<4；失败由pcall捕获返回REJECTED，发生在settler检查/计划创建之前。Confirm亦有有效预览与potential<4保护，消耗发生在其后。截图调用栈是预期assert拒绝的调试细节，不是未捕获崩溃。

UX待办：把POTENTIAL_CAP_4/PREPARE_FIRST等预期拒绝显示为简短提示，例如“已达投资上限Lv4，不能继续投资；移民未消耗”。调用栈留日志，未知错误仍保留诊断。本轮仅记录，不改运行代码，不要求补测。

## 证据与边界

原图见../Evidence/B035/manifest.json，按原名/SHA256归档。未提供GPP数字/截图不能捏造逐项测量表。未扩大到AI/多人、任意百分比组合、所有异常路径。B035无需追加测试；施工队及未实现的高级专业收益仍待开发。
