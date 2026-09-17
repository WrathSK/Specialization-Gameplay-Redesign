# Culture D0029 — Boundary Amendment Review

Document Owner: Codex
Design Authority: User
Document State: ACCEPTED
Freeze Status: DESIGN_FROZEN
Implementation / Balance Validation: PENDING

## 版本与权威

沿现有Dxxxx新修订惯例，不覆写D0028：[当前Culture](Content/Culture_D0029.json)，[旧Culture](Content/Culture_D0028.json)，[旧Review](Culture_D0028_Review.md)，[冻结D0028 Spec](Revisions/Specialization_Design_Spec_D0028.md)。本轮仅ownership/network merge/diplomatic eligibility；机构、能力、Mission、数值、duration及其它合同原样保留。

## 正式决定与marker

- CUL-REVIEW-01 CONFIRMED：original-owner + source-city scoped见闻与三类成功记录；不同来源城仍可有各自记录。
- CUL-REVIEW-02 CONFIRMED：已遇见、存活其它Major文明；City-State第一版明确排除，其文化交流列FUTURE_CANDIDATE/FUTURE_EXPANSION，不否定文化价值；Free Cities明确排除。不新增边境/使馆/联盟/任何国内外商路要求。
- CUL-REVIEW-03 CONFIRMED：observations原Owner记录不删除，新Owner不能使用，原Owner收回来源城后在正常条件下恢复；Dialogue累计倍率和City×START Game Era额度随城市转移，ACTIVE不足暂停效果，不因易主再获本时代次数。
- CUL-REVIEW-04 RESOLVED_CONFIRMED：每个有效来源先独立筛出3/3完整考察文明集合，再做接收端并集。不拼接跨source零散记录，不重复算同文明。receiver仅本专业工作专家，K_C=1，接收不赋见闻所有权、不再输出为自身payload。

战争允许部署、开始、继续与成功完成；宣战自身不取消任务。仍无失败率/捕获/死亡/外交惩罚。原生引擎若强制撤回则报告TECHNICAL_INVESTIGATION_REQUIRED / IMPLEMENTATION_LIMITATION，不反改Design。真正目标失效依旧取消、不给收益、不耗成功额度并保留单位。

## 文档级合同例子

A={日本,埃及,印度}、B={日本,中国,美国}→并集5；A/B都仅日本→1；三个source分别只有日本的People/Works/Places→空集0。
城市+45%且时代已用→易主仍+45%记录与已用；ACTIVE<III效果暂停、记录保留。见闻原Owner记录则不供新Owner使用，原Owner收回后按正常资格恢复。

这些例子验证设计表达，不是Gameplay实现测试，不宣称实机PASS。Research_D0028、Industry_D0027、Shared_D0028及旧Culture原文保持hash；不传播Culture的ownership/union到其它专业。

## 范围

本轮只Design文档。尚未解决的既有balance/技术适配保留；不启动Architecture adaptation，不改Mod、main或运行包，不部署/tag/promotion。
