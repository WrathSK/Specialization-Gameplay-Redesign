# Culture D0028 — Freeze Review

Document Owner: Codex
Design Authority: User
Document State: ACCEPTED
Freeze Status: DESIGN_FROZEN_BODY_NETWORK_MERGE_DEFERRED
Implementation / Balance Validation: PENDING

## 权威入口与范围

[Culture](Content/Culture_D0028.json)、[Shared](Content/Shared_D0028.json)、[Research D0028增量](Content/Research_D0028.json)为各自canonical内容。[D0027冻结Spec](Revisions/Specialization_Design_Spec_D0027.md)保留旧设计；Research_D0026、Industry_D0027字节不改。用户此次明确授权Research输入改动，不能用原“不得修改Research”的阶段要求否定新指令。

## 已确认边界

- 被掠夺普通建筑默认不存在于当前效果中，不贡献、不接受；免费取得按建筑性质处理，城墙可计，宫殿/奇观/机构/内部对象排除。永久Industry模板是显式历史例外，不遗忘。
- 同领域多个区域取最高单区域完善度。普通Tier逐栋相加再封顶，缺Tier不补。
- Dialogue按启动时代记成功次数，完成时采X；X=0也耗成功次数。中断须重新连续完整生产回合，ACTIVE不足只暂停收益不清记录。
- 单位绑定训练城；来源降级可继续任务及获记录；固定成功，完成后保留单位继续考察；2T按速度floor。
- 来源城市级唯一性暂定CUL-REVIEW-01；城邦/自由城排除暂定02；原Owner分区保存且新Owner不可用暂定03。
- 当前实际控制首都；目标巨作消失/首都迁移/易主/文明灭亡导致取消，无收益不耗成功次数，保留单位。战争不禁部署/任务，中途宣战参考间谍的原生处理，不擅加取消或风险。
- 圣地映射大预言家；不实现额外转信仰机制，不声称超额转换已验证。
- 新Culture Network替代Eureka；多源合并04明确后置。接收本专业实际工作专家，不复制见闻，不递归自传。Research网络待重设计但当前公式不动。
- Dialogue只倍率原生收益，不放大意义延展追加收益；未知Mod作品自动排除。

## 静态调查与技术标记

2026-09-16只读本机Cache/DebugGameplay.sqlite：合格七类210定义均有EraType；非文物创作者关联完整且与作品时代无差异，文物使用自身时代。不是任意Mod保证。现有DialogueModel非文物读creator时代，新合同要求作品自身历史时代。已查城市巨作yield/Tourism modifier和地区GPP类型，不证明all-native隔离或0.1精度。

本机加载Spy Cost=80只是当时数据库值，设计复制当前Spy成本，不硬编码80。Projects定义未见固定完整回合字段，低成本不等价。间谍Chooser/Support未明确暴露宣战转移的引擎处理，保持TECHNICAL_INVESTIGATION_REQUIRED，不将缺少UI分支当引擎行为证据。

普通建筑无法仅凭InternalOnly或HD Tier确定；宫殿非InternalOnly，市中心很多真实基础设施为Tier0。后续适配须明确分类，未知类型不扩大目录。0.1GPP、原生收益限定、Spy非敌对/无容量、owner记录与时代项目时序均待技术验证。

## 文案自审与例子

4机构与6能力数量0/1/2/3；仅本专业结构，不强加全局。项目/单位/Mission/见闻均有独立说明及动态字段，具体值不硬编码到动态本地化。

Dialogue示例X4增加20百分点，再X2增加10，累计原始30（实际受待定cap）；不是25%*(X-1)，作品移走不带走历史奖励。Aesthetic随当前X变，不按作品件数乘建筑收益。Meaning D3→1.5份Gold→4.5，不预先floor。GPP D10×38×0.1=38基础点，正常吃百分比。Research D总和12现在封顶10；主持5栋仍逐栋，新增Science不反馈完善度。

## 后续与边界

Schema/Civilopedia共享定义从Shared读取一次。后续Architecture适配要保护av2-runtime-b076.103，不新增轮询/全城重复扫描。本轮只Design，不改Architecture已实现状态、源码、Mod版本、运行包或main；不部署、不启动游戏。多源Network后置绝不伪标为已解决。
