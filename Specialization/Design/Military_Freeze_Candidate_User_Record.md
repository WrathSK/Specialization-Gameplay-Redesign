# Military redesign — user decision record

Role: candidate source evidence; NOT canonical revision, runtime specification or implementation authorization.
Date: 2026-09-20. User-provided text below is preserved verbatim.
Original attachment SHA256: `4b2af6c48333d1356039d34f63b14822db972e80d0839b55d87f4d8accc6e82c`.
Review: [Military Freeze Candidate](Military_Freeze_Candidate_Review.md).

---

这是 Civilization VI / Harmony in Diversity 的 Specialization Gameplay Redesign 项目。

本轮任务是：

# MILITARY REDESIGN — FREEZE CANDIDATE SYNCHRONIZATION & DESIGN REVIEW

请按照当前 W0001 Workflow 和 Authority Index 工作。

目标不是 Implementation。

目标是把 Design Chat 已经完成的新 Military redesign：
1. 与当前 D0032 Design Authority、Shared规则和历史 Military 设计核对；
2. 整理为新的 Military Freeze Candidate；
3. 区分：
   - 已确认设计；
   - Naming placeholder；
   - Balance待定；
   - Technical Investigation；
   - Legacy / Ownership待定；
4. 只提出真正阻塞 DESIGN_FROZEN 的 Gameplay边界问题。

本轮：

- 不修改 Gameplay / UI / SQL / runtime；
- 不部署；
- 不开始新的P0 implementation batch；
- 不擅自填写Balance数值；
- 不因为技术实现未知而修改Gameplay设计；
- 不重新设计Military；
- 不重新打开已经明确关闭的Red Team争议；
- 不修改Research / Industry / Culture / Commerce玩法；
- 如果需要建立新的Design revision，先完成审查并确认没有Blocking Design Decision后再按现有Design revision流程处理。

==================================================
A. Authority / Historical Boundary
==================================================

当前正式Authority仍以项目现有Authority Index为准。

历史文件（尤其D0008及其它旧Military设计）：

> 仅作为Historical Reference。

不能覆盖本轮用户确认的新Military设计。

旧D0008中值得保留并重新采用的部分包括：

- Veteran Mentorship旧公式；
- Veteran Insight旧公式及其Balance结论。

其它旧Military能力，尤其旧Mobilization Network：

> 不因历史存在而自动保留。

新设计优先。

==================================================
B. Military Specialization Philosophy
==================================================

Military specialization不是：

> 城市只能建设军营、只能做军事。

本项目对Specialization的定义是：

> 即使城市发展全面，它仍然拥有明确的制度重心，
> 并能够以该专业独特的方式利用城市其它发展成果。

Military的核心意义目前可以概括为：

> 把城市和文明已有的社会资源、组织能力、经验与人才，
> 更有效地集中转化为军事力量。

Military并不等于侵略。

它可以用于：

- 主动扩张；
- 突破和平发展空间不足；
- 防御危险邻居；
- 战前准备；
- 通过Asset Restructuring进行紧急军事化。

不要求Military在和平时期额外产生Science/Culture/Gold等经济Yield来“回本”。

军事准备本身可以具有机会成本。

==================================================
C. Institution Structure / Naming
==================================================

Military仍采用Shared 0/1/2/3结构：

Lv1：
0个Military专属named ability。

Lv2：
1个Shared-template ability。

Lv3：
2个Military专属能力。

Lv4：
3个Military专属能力。

该结构目前是自然形成的，但不要把0/1/2/3解释成不可违反的runtime schema。

当前机构名称：

### Lv1 — 武备社
状态：
> PLACEHOLDER / NAMING_REVIEW_REQUIRED

暂时使用，不视为最终LOCK。

### Lv2 — 武官所
状态：
> PLACEHOLDER / NAMING_REVIEW_REQUIRED

暂时使用，不视为最终LOCK。

### Lv3 — 演武场
状态：
> LOCKED

### Lv4 — 讲武堂
状态：
> LOCKED

不要重新命名已LOCK项目。

==================================================
D. Military Lv1 — Shared Base Support
==================================================

Military Lv1不增加额外Military专属能力。

工作Military Specialist继续采用Shared基础支持：

> +3 Food
> +3 Production

全等级保持该基础支持。

不要恢复旧版Military III专家升级。

==================================================
E. Military Lv2 — 行伍制度
==================================================

Ability Name：

> 行伍制度

状态：
> LOCKED

沿用Shared Lv2结构。

### Housing

ACTIVE ≥ 2时：

- 合格专业区域本体提供住房；
- 实际存在的合格普通建筑Tier分别提供住房；
- 使用Shared已经确定的Tier existence规则；
- 不使用District Completeness加权值代替Housing规则。

### Great General Points

每名实际工作的Military Specialist：

> +2 Base Great General Points

强调：

> Base GPP。

它代表稳定职业军事共同体开始持续产生杰出军事人才。

不要增加其它Military Lv2效果。

==================================================
F. Military Lv3 Ability A — 综合训练
==================================================

Ability Name：

> 综合训练

状态：
> LOCKED

核心：

高级Military城市能够把城市其它社会领域已经形成的基础知识、组织能力与制度成果纳入军事训练。

只读取五个领域：

1. Research / Campus
2. Culture / Theater
3. Industry / Industrial Zone
4. Commerce / Commercial Hub
5. Religion / Holy Site

明确不加入：

- Harbor；
- Diplomatic Quarter；
- Government Plaza；
- Preserve；
- Entertainment；
- Neighborhood；
- 其它目前没有直接故事关联的区域。

### Qualification

每个领域必须：

> 至少实际存在一个合格T1普通建筑。

不是：
- 只有区域本体即可；
- District Completeness达到某个高门槛；
- T2/T3/T4完整建设。

每个合格领域：

> 本城新训练的合格军事单位永久获得 +1 Combat Strength。

因此：

> 0–5个合格领域
> → +0～+5 Combat Strength。

理论+5要求：

- Encampment；
- Campus；
- Theater；
- Industrial；
- Commercial；
- Holy Site；

共6个区域，因此至少需要16人口区域位；
五个外部领域还需要实际T1建筑。

### Design Intent

这不是要求Military city必须成为“五色水桶城”。

+5是理论极限，不是能力开机条件。

例如：

> Research + Industry + Commerce满足资格
> → 新兵 +3 CS

完全是有效Military city。

核心Trade-off：

> 投入Population / District Slot / Production建设其它领域
> → 训练更高质量军队

vs

> 放弃部分长期城市发展
> → 直接把资源用于更多军队。

### Asset Restructuring

成熟非Military城市通过Asset Restructuring转为Military后：

> 可以利用自己已有的T1基础设施获得综合训练收益。

这是明确接受的预期玩法，不是Exploit。

因为Asset Restructuring已有：

- Potential P → P−1；
- REALLOCATING至少5个完整回合；
- 非Food产出−75%；
- Food Surplus−75%；
- 原专业ACTIVE能力退出；
- 新Military city没有既有Military Tradition。

不要重新打开“成熟Research城转Military所以白嫖”的争议。

==================================================
G. 综合训练 — Permanent Unit Provenance
==================================================

综合训练属于：

> Unit creation / training时锁定的永久训练来源。

城市以后失去某个T1建筑：

> 已经训练完成的单位不失去该CS。

城市以后转专业：

> 已经训练完成的单位不失去该CS。

具体哪些Unit Acquisition路径属于“本城新训练”：

- Production；
- Purchase；
- Faith purchase；
- free unit；
- levy；
- duplication；
- capture；

如果当前Design Authority没有统一定义，请：

> DESIGN_BOUNDARY_REVIEW_REQUIRED

不要擅自推导。

其中哪些只是技术识别问题，哪些会改变Gameplay，请区分。

==================================================
H. Corps / Army Formation Inheritance
==================================================

综合训练等“永久出生训练Buff”在Formation合并时：

> 不相加。

当前Design方向：

> 同一个Ability来源，在组成Formation时取组成单位中的最高值。

例如：

A：
> 综合训练 +4

B：
> 综合训练 +5

C：
> 综合训练 +1

Formation结果：

> 综合训练 = max(4,5,1) = +5

而不是：

> +10
或
> 平均后下降。

不同Ability来源仍分别结算。

例如：

> 综合训练 +4
> +
> 军略传承相关出生CS +1
> =
> 总计 +5

不要把不同来源的CS全部压成一个max。

### Design Intent

接受以下Emergent Strategy：

> 高级Military city生产精锐骨干部队；
> 普通城市生产普通兵员；
> Corps / Army吸收普通兵员后，
> 保留精锐骨干的训练标准。

这目前视为Feature，不自动视为Exploit。

Technical Investigation需确认：

- Civ VI Formation merge主体；
- Unit Ability inheritance；
- Upgrade persistence；
- 是否能可靠实现per-ability max。

不要因为技术未知而修改Design。

==================================================
I. Military Lv3 Ability B — 后勤编制
==================================================

Ability Name：

> 后勤编制

状态：
> LOCKED

Design核心：

Military III解锁一个专属Logistics Support unit line。

该单位与一个Combat Unit形成：

> 1:1 Escort / Formation

以后：

> 该Combat Unit的每回合Strategic Resource Maintenance被取消；
> 转而由Logistics unit承担额外Gold Maintenance。

### Hard Boundaries

后勤编制：

不改变：
- 训练单位的一次性Strategic Resource cost；
- 购买单位的一次性Strategic Resource cost；
- Upgrade的一次性Strategic Resource cost。

所以：

> 没有对应资源时仍不能凭空建立该单位。

后勤只解决：

> ongoing maintenance。

### Progression

后勤单位随着需要新Strategic Resource maintenance的军事单位出现逐步解锁升级版本。

高级版本：

> 可以承担本等级及此前等级Strategic Resource的maintenance替换。

具体：

- unit line；
- unlock tech/civic；
- resource coverage；

根据当前HD实际军事单位表之后确定。

### Gold Cost

Gold maintenance尚未确定。

Balance目标：

> 不同历史阶段的后勤扩编，
> 对当时玩家经济造成大致类似的相对压力。

当前仅有非常宽的设计预期：

> 早期约10级别Gold/T；
> 后期可能上升至数百乃至约1000 Gold/T量级。

这不是锁定数字。

不要写入正式Balance值。

### Uranium / Endgame Resources

尚未决定：

> Uranium等特殊终局资源是否允许后勤替代。

登记：

> DESIGN / BALANCE REVIEW REQUIRED

不要擅自包含或排除。

==================================================
J. 后勤编制 — Presentation / Technical Branch
==================================================

当前Design preference：

> 实体Support Unit。

原因：

- 后勤编制在地图上真实存在；
- 有明确的Production成本；
- 1:1军队组织关系可见；
- Support死亡具有战场意义；
- RP强于后台名单。

但保留fallback：

> UI / Unit Ability Logistics Contract。

如果Technical Spike证明实体Escort：

- link不稳定；
- embark问题严重；
- ZOC/formation频繁断开；
- save/load不可靠；
- resource maintenance动态切换不可控；
- AI无法合理处理；
- 性能成本明显过高；

可以再审Presentation。

不要在Technical Investigation前把fallback升级为Design replacement。

重点调查：

- Link / Unlink；
- Create / Destroy；
- Support death；
- Upgrade；
- Embark；
- Formation；
- resource tick；
- save/load；
- AI；
- event-driven feasibility。

==================================================
K. Military Lv4 Ability A — 战阵传授
==================================================

Ability Name：

> 战阵传授

状态：
> LOCKED

沿用旧D0008 Veteran Mentorship主体及旧公式。

核心：

当一个合格新兵发生真实Combat时：

> 检查附近符合资格的友军老兵。

Mentor必须：

- Promotion数量高于当前单位；
- 属于相同军事大类 / Promotion Class。

根据双方Promotion差：

> 获得旧公式定义的Mentorship Bonus XP。

### Design Intent

正常新老混编战线应自然获得基础收益。

允许：

> 极致军事玩家通过走位提高Mentorship覆盖。

这不是自动Design问题。

但不能要求极致微操才能获得正常价值。

同Promotion Class限制用于：

> 防止一个高机动满级单位成为所有兵种的万能教练。

请核对D0008旧公式、资格、range和边界，
不要凭记忆重写。

如果新“同Promotion Class”边界与D0008不同，
以本轮新Design为准。

==================================================
L. Military Lv4 Ability B — 沙场领悟
==================================================

Ability Name：

> 沙场领悟

状态：
> LOCKED

沿用D0008 Veteran Insight主体及旧公式。

核心：

高Promotion单位发生真实Combat时：

> 根据自己已经掌握的Promotions，
> 获得额外Insight XP。

哲学：

> 已有知识越丰富，
> 越能从新的实践中看到过去无法理解的东西。

### Balance Evidence

旧公式此前已经严格计算：

- 不存在高级单位升级速度反超低级单位；
- 大多数情况下只减少约1次Combat；
- 没有情况减少2次Combat；
- 少数情况下甚至不能减少晋升所需Combat次数。

因此：

> 不要仅因为“Promotion → XP → Promotion”存在正反馈
> 就重新标记为Snowball Design Risk。

需要做的是：

> 核对当前HD XP环境是否改变旧模型输入。

若HD环境变化：

> BALANCE_REVALIDATION_REQUIRED

而不是自动重开Design。

==================================================
M. Military Lv4 Ability C — 军略传承
==================================================

Ability Name：

> 军略传承

状态：
> LOCKED

Great General原生拥有：

A.
> 保留单位，继续提供Aura。

B.
> Retire，消耗Great General并获得原生独特Retire能力。

Military IV新增：

C.
> Institutionalize / Legacy Action。

执行后：

- Great General永久消耗；
- 不触发原生Retire效果；
- 其军事知识永久沉淀在执行该行为的Military city；
- 提升该城市自己的Military Tradition。

Military Tradition是：

> Local Historical State。

不是全国共享。

### Design Intent

允许：

> 原生Retire效果较弱的Great General更倾向用于军略传承。

这不是自动问题。

该系统也承担：

> 为弱Retire GG提供另一种长期价值出口。

真正Trade-off尤其发生在：

> 当前GG投入恰好能够使Military Tradition升下一档

的时候。

此时玩家需要比较：

> 当前Aura
> vs
> 原生Retire
> vs
> Tradition升档。

不要重新加入：
> 不同时代GG要求

目前不采用该方向。

==================================================
N. Military Tradition — Discrete Tier Structure
==================================================

Military Tradition采用：

> 有限离散档位。

当前目标结构：

> 约6档。

具体GG数量门槛未定。

非常重要：

> 每个Tradition档位只强化一个维度。

三个强化维度：

1. 本城以后训练单位的初始Combat Strength；
2. 战阵传授产生的Mentorship XP；
3. 沙场领悟产生的Insight XP。

如果最终为6档：

> 每个维度全程只强化约2次。

目的：

> 避免每升一档同时强化三个效果，
> 导致低档正常、高档数值爆炸。

具体：

- 档位顺序；
- 每档GG需求；
- CS增量；
- Mentorship增量；
- Insight增量；

全部属于：

> BALANCE / DESIGN DETAIL REQUIRED

不要擅自填写。

### Local Identity

Military Tradition集中在一座历史Military city：

> 明确接受为Feature。

目标就是让：

> 百年Military IV
≠
> 新资产重组Military IV。

不要把“形成一座帝国军事名城”当成Design缺陷。

==================================================
O. Military Network — 统一动员
==================================================

Network Ability Name：

> 统一动员

状态：
> LOCKED

旧D0008：

> Mobilization Progress → 自动生成军事单位

正式作为Legacy候选退出。

不要默认保留。

新Network：

> Command Source + Mobilization Target + Network Participants。

==================================================
P. Command Source
==================================================

Network中存在一个当前有效：

> Command Source / 司令城。

Command Source必须：

- 是合格Military specialization city；
- 当前Active Production Item是一个合格军事单位。

它当前实际正在生产的：

> normalized Unit Type

定义：

> 当前Network Mobilization Target。

注意：

**只读取Current Active Production Item。**

不是：

> Production Queue里存在某单位即可。

所以不存在：

> 队列里挂Tank，
> 当前实际造Wonder，
> 仍然广播Tank Target。

Production目标切换事件：

> 立即改变或取消资格/Target。

不要重新提出该Queue Spoofing伪问题。

==================================================
Q. Command Authority
==================================================

司令权威按Military等级：

> Military IV > III > II > I。

规则：

### No current Command Source

第一个进入：

> 正在实际生产合格军事单位

状态的Military city：

> 成为Command Source。

### Higher Authority

当Military city发生相关Production Queue变化：

若：

> Candidate Military Level > Current Command Source Level

则：

> Candidate接管司令权。

### Equal Authority

若：

> Candidate Level = Current Command Source Level

则：

> 不夺权。

当前Command Source保持。

因此：

> 同级时先建立有效Command状态者优先。

### Current Command Source changes production

Command Source不变。

Target更新为：

> 新Current Active Production Item。

### Command Source invalidates

例如：

- 停止生产合格军事单位；
- 转专业；
- Military资格下降；
- 城市失去；
- 当前Target失效；

则触发：

> 单次有界重新选举。

重新选举时：

1. 只检查当前合格Military cities；
2. 优先最高Military Authority；
3. 同等级候选中，选择最早进入当前“合格Active Military Production”状态者；
4. 其当前Active Production Item成为新的Mobilization Target。

允许保存：

> stable eligibility sequence / event sequence

用于同级稳定tie-break。

不要每回合重新比较、重新选举。

==================================================
R. Network Participants / Response
==================================================

统一动员的响应城市：

> 不要求自身是Military specialization。

所有接入当前专业Network、且满足Network共同资格的城市：

如果其Current Active Production Item：

> 与Mobilization Target属于同一个normalized Unit Type

则：

> 获得该军事单位的Production效率加成。

因此可能出现：

Military IV：
> 作为司令城确定当前全国重点训练Tank。

Industry IV：
> 响应Tank动员，利用自己的高Production快速训练Tank。

Commerce / Research / ordinary city：
> 如果接入Network并主动训练Tank，
> 同样可以获得统一动员Production bonus。

这是预期设计。

### Military Identity Preservation

响应城市只获得：

> 统一训练/生产效率。

明确不获得Command Source的：

- 综合训练Combat Strength；
- Military Tradition；
- 战阵传授；
- 沙场领悟；
- 后勤编制资格；
- 其它local Military abilities。

所以：

> Military负责组织和确定训练方向；
> Industry等其它城市可以贡献生产能力；
> 但不会因此成为Military city。

==================================================
S. Mobilization Target
==================================================

当前倾向使用：

> normalized Unit Type / Unit Line

而不是：

> 整个Promotion Class。

原因：

“所有近战单位”过宽，
会让统一动员接近通用Military Production buff。

目标应该表达：

> 全国当前正在围绕一种具体军事需求进行统一训练。

但Unique Replacement必须考虑归一化。

例如：

> Unique Unit与其替代的标准Unit
是否属于同一Mobilization Target，

需要Design/Technical review。

请调查当前项目已有：

- unit normalization；
- replacement mapping；
- Promotion Class；
- Corps / Army unit type；

相关基础设施。

不要擅自决定未明确边界。

==================================================
T. Unified Mobilization — Intended Decision
==================================================

假设Command Source正在训练Tank。

其它Network城市可以：

A.
> 同样训练Tank
> → 获得统一动员Production bonus。

B.
> 训练Artillery / Aircraft /其它单位
> → 不获得该bonus，但维持军队兵种多样性。

C.
> 继续Building / District / Wonder / Project
> → 不获得bonus，但继续城市自身发展。

因此Network的核心Trade-off是：

> 统一生产计划提高动员效率

vs

> 分散生产保持兵种结构与城市发展自由。

不要把Network改成：

> Military city存在 → 全国所有军事单位Production +X%。

==================================================
U. Unified Mobilization — Event-driven Intent
==================================================

该设计刻意适合事件驱动。

预期：

Military Production Queue / Active Production变化：
> 检查Command Authority与Target。

Current Command Source Production变化：
> 更新Target或使Command失效。

普通Network participant Production变化：
> 只重新判断该城市是否匹配当前Target。

Command Source失效：
> 单次有界重新选举。

Network topology变化：
> 更新相关participant资格。

不要求：

> 每帧或每回合全帝国扫描。

请将：

> Gameplay Design

与：

> 最终可用事件/API

分开。

如果事件覆盖不完整：

> TECHNICAL_INVESTIGATION_REQUIRED

而不是修改Design。

==================================================
V. Unified Mobilization — Queue Spoofing Clarification
==================================================

此前外部Review多次提出：

> “司令城把Tank留在Queue中，
> 实际生产Wonder，
> 仍然给全国Tank bonus。”

该批评基于错误理解。

本Design读取：

> Current Active Production Item。

不是：

> Queue contains Unit。

因此：

Tank → Wonder

发生Active Production变化时：

> Tank Target立即退出/改变。

不存在：

> 当前实际生产Wonder同时继续广播Tank

的合法状态。

如果玩家：

> 一直保持Tank为Current Active Production，
> 但故意不完成它，

那么该城市的Production也确实持续投入/占用在Tank生产上，
并没有免费把同一Production用于其它项目。

因此目前：

> 不增加Cooldown；
> 不增加“必须X回合内完成”；
> 不增加取消生产惩罚。

只有Technical Investigation证明原生Production系统存在真实可套利行为时，
才重新打开。

==================================================
W. Unified Mobilization — Production Bonus
==================================================

具体Production bonus：

> UNRESOLVED BALANCE PARAMETER。

不要填写默认值。

需要之后比较：

- fixed bonus；
- Command Source Military Level scaling；
- participating city count scaling；
- diminishing return；
- speed scaling。

当前Design尚未决定。

不要自动让：

> Tradition

提高Network bonus。

Military Tradition目前保持：

> local historical asset。

==================================================
X. Military Design Interaction Summary
==================================================

当前Military体系可以理解为：

### Lv1
基础军事专业共同体。

### Lv2 — 行伍制度
职业军事共同体稳定形成：
> Housing + Base Great General Points。

### Lv3 — 演武场

**综合训练**
> 城市其它社会领域
> → 新兵质量。

**后勤编制**
> Production + Gold
> → 战略资源maintenance capacity
> → 可维持更大规模的高资源军队。

### Lv4 — 讲武堂

**战阵传授**
> 老兵已有知识
> → 新兵成长。

**沙场领悟**
> 自己已有知识
> → 从新实战中产生更深理解。

**军略传承**
> Great General个人军事知识
> → 城市长期Military Tradition。

### Network — 统一动员

> 高级Military Command Source确定当前训练目标；
> Network其它城市可以响应统一训练计划；
> → 提高扩军速度。

因此大致形成：

> Quality
> + Sustain / Scale
> + Experience Transfer
> + Veteran Learning
> + Institutional Memory
> + Coordinated Mobilization

==================================================
Y. Explicitly Closed / Do Not Reopen
==================================================

以下问题已经经过Design Chat + Red Team + Naming Review讨论。

除非发现新的、具体且可证明的冲突，
不要重新打开：

1. “Military城市发展多个其它区域违背Specialization”
   → CLOSED。

2. “成熟非Military城资产重组后利用旧基础设施是Exploit”
   → CLOSED；这是预期synergy。

3. “Mentorship和Insight都给XP，所以必须合并”
   → CLOSED。

4. “Insight存在正反馈，所以一定XP Snowball”
   → CLOSED；旧公式已有严格数学验证。

5. “弱Retire Great General更倾向军略传承，所以机制失败”
   → CLOSED；这是允许的价值出口。

6. “Tradition集中在一座Military city所以失败”
   → CLOSED；这是local identity feature。

7. “Formation max意味着精锐骨干+普通兵员，所以自动Exploit”
   → CLOSED；目前视为允许的Emergent Strategy。

8. “少量战略资源通过后勤支持更多资源单位等于复制资源”
   → CLOSED；这是能力目的。

9. “实体Support数量增加就等于地图格和移动操作翻倍”
   → CLOSED；Escort可同格，实际操作成本需Technical Spike验证。

10. “Command Source把单位留在Queue里、实际造其它项目仍广播Target”
    → CLOSED；设计只读取Current Active Production Item。

==================================================
Z. Naming Status
==================================================

当前Naming：

### Institution

Lv1：
> 武备社
> PLACEHOLDER / NAMING_REVIEW_REQUIRED

Lv2：
> 武官所
> PLACEHOLDER / NAMING_REVIEW_REQUIRED

Lv3：
> 演武场
> LOCKED

Lv4：
> 讲武堂
> LOCKED

### Abilities

Lv2：
> 行伍制度
> LOCKED

Lv3：
> 综合训练
> LOCKED

Lv3：
> 后勤编制
> LOCKED

Lv4：
> 战阵传授
> LOCKED

Lv4：
> 沙场领悟
> LOCKED

Lv4：
> 军略传承
> LOCKED

Network：
> 统一动员
> LOCKED

不要重新做Naming Pass。

==================================================
AA. Required Design Review
==================================================

请把本轮设计整理成：

> Military Freeze Candidate

并与当前Authority逐项核对。

重点检查：

### 1. 真正Blocking Gameplay Decisions

只提出：

> 如果不回答，就无法准确知道玩家规则是什么

的问题。

不要把：

- Balance数字；
- Technical API；
- Naming placeholder；
- UI布局；

冒充Blocking Design。

### 2. Balance Register

集中登记，但不填写未经批准数值：

- 综合训练：当前固定+1/领域、max5已经是Design；
- Tradition六档具体门槛；
- Tradition各档CS / Mentorship / Insight增量；
- 后勤Gold/T；
- 后勤各版本成本；
- 统一动员Production bonus；
- 若需要speed scaling，分别登记。

### 3. Technical Investigation Register

至少包括：

#### 综合训练
- T1 ordinary building qualification复用；
- unit acquisition path；
- permanent Unit Ability；
- Upgrade persistence；
- Corps / Army per-ability max inheritance。

#### 后勤编制
- 专属Support line；
- Escort API；
- Link/Unlink；
- Death；
- Upgrade；
- Embark；
- Formation；
- Strategic Resource maintenance；
- Gold maintenance；
- tick ordering；
- save/load；
- AI；
- performance；
- UI-contract fallback。

#### 战阵传授
- Combat event；
- nearby mentor；
- same Promotion Class；
- old D0008 formula integration。

#### 沙场领悟
- old D0008 formula；
- current HD XP environment revalidation。

#### 军略传承
- Great General third action；
- consume without native Retire；
- local persistent Tradition；
- tier transition；
- ownership / conquest；
- reallocation Legacy。

#### 统一动员
- Active Production event；
- Command authority；
- stable eligibility sequence；
- normalized Unit Type；
- Unique replacement；
- Corps / Army production；
- participant topology；
- dynamic Production modifier；
- no unnecessary polling。

### 4. Legacy Review

明确登记：

- Military Tradition转专业后如何保存/失效；
- 征服/易主后如何处理；
- 历史Military institution如何展示；
- 已训练单位永久Buff继续存在；
- 后勤单位在来源城市转专业后的资格；
- Command Source转专业立即失效；
- 旧D0008 Mobilization Network退出。

不要擅自套用Research / Industry / Culture / Commerce的Legacy规则。

==================================================
AB. District Completeness / Shared Architecture Note
==================================================

本轮Design Chat还发现一个Shared问题：

当前District Completeness使用：

> T1 / T2 / T3 / T4 = 1 / 2 / 3 / 4

但：

- 原版 / 纯HD很多区域只有T1–T3；
- 区域建筑扩展中只有部分区域拥有T4；
- 不同区域“满建设”的理论Completeness可能因此不同。

Military综合训练已经明确：

> 不依赖Completeness；
> 只读取T1普通建筑存在性。

所以该Shared问题：

> 不阻塞Military综合训练。

但请检查当前Architecture / Design中是否已经明确处理：

> 不同规则环境下T4不存在时，
> District Completeness的cap / normalization语义。

如果尚未处理：

> SHARED_DESIGN_REVIEW_REQUIRED

只登记，不在本轮擅自修改Shared规则。

==================================================
AC. Expected Output
==================================================

请输出：

A. Authority / historical sources used

B. Military canonical candidate table

C. Institution / ability naming status

D. Lv1 / Lv2 Shared rules

E. 综合训练完整规则

F. Permanent Unit / Formation inheritance

G. 后勤编制完整规则

H. 战阵传授

I. 沙场领悟

J. 军略传承 / Military Tradition

K. 统一动员 / Command Source / Network

L. Interaction with Asset Restructuring

M. Balance Register

N. Technical Investigation Register

O. Legacy Review Required

P. Shared District Completeness issue

Q. Blocking Design Decisions

R. Candidate Freeze Assessment:
- READY_TO_FREEZE
或
- NOT_READY_TO_FREEZE

如果NOT_READY：
只列真正blocking的问题。

S. Files changed

T. Git status / commit / push

U. 用户需要决定

V. 用户需要测试

W. Codex下一步

==================================================
AD. Stop Condition
==================================================

如果审查后：

> Blocking Design Decisions = None

则可以：

1. 按现有Design revision流程建立新的Design revision；
2. 将Military升级为DESIGN_FROZEN；
3. 更新必要的Design Spec / ChangeLog / Content导航；
4. 保留Naming placeholders、Balance、Technical、Legacy标记；
5. commit；
6. push develop；
7. STOP。

如果存在真正Blocking Gameplay Decision：

1. 建立Military Freeze Candidate；
2. 不擅自决定；
3. 不升级canonical Design；
4. commit/push候选审查文档；
5. 向用户提出最小必要问题；
6. STOP。

无论哪种情况：

> 不Implementation。
> 不修改runtime。
> 不部署。
> 不开始Architecture adaptation。 
