# 设计演变与来源记录

当前玩法从[Design阅读导航](../../Design/README.md)进入；正式规则仍由[当前Spec](../../Design/Specialization_v0.1_Design_Spec.md)及[Content](../../Design/Content/README.md)承担。本文不另立设计权威，不派发实现任务。

旧审阅、候选、阶段状态与修订只描述其形成时的结论，不代表今天的完整Gameplay规则。已被现行正式来源引用的接受决定仍可作为依据，不能因归档就丢失；技术调查的STATIC／未确认范围也不升级为实机证明。当前版本与取代关系查[Design ChangeLog](../../Design/Design_ChangeLog.md)。

## 审阅与边界来源

这些记录的玩法结论已进入对应正式内容及阅读版；审阅中的技术依据、未决事项和当时的验证范围保留原意。本次只移动路径、重定向必要的相对链接，没有改写规则正文。

| 记录 | 用途与后续解释入口 |
|---|---|
| [Research_D0026_Review.md](Reviews/Research_D0026_Review.md) | 科研初次冻结与旧效果取代；当前读Research_D0040及科研阅读版 |
| [Industry_D0027_Review.md](Reviews/Industry_D0027_Review.md) | 工业冻结及仍需保留的暂行合同；后续容量关闭见Industry_D0032 |
| [Culture_D0028_Review.md](Reviews/Culture_D0028_Review.md) | 文化初次冻结、Shared普通建筑与技术限制；部分边界随后由D0029取代 |
| [Culture_D0029_Review.md](Reviews/Culture_D0029_Review.md) | 文化归属、完整文明并集与外交资格接受记录；原Owner见闻归属由D0040取代 |
| [Research_D0030_Review.md](Reviews/Research_D0030_Review.md) | 学以致用改用D及不应机械统一其它consumer的理由 |
| [Boundary_D0031_Review.md](Reviews/Boundary_D0031_Review.md) | 学术传统身份暂停、施工队有限库存与文化展示要求；容量及展示方向后由D0032关闭 |
| [Commerce_D0032_Review.md](Reviews/Commerce_D0032_Review.md) | 商业冻结、旧规则取代、未决合同及静态技术证据 |
| [Long_Term_State_D0040_Review.md](Reviews/Long_Term_State_D0040_Review.md) | 用户确认的A–D城市／文明历史、信誉与合同生命周期；取代项、未讨论边界及当前测试复用 |
| [Commerce_D0039_Review.md](Reviews/Commerce_D0039_Review.md) | 用户确认的v0.1公式/首版Balance/指定Legacy收口与精确剩余边界；公式基线保留，生命周期现行增量见Commerce_D0040 |
| [Military_D0033_Review.md](Reviews/Military_D0033_Review.md) | 军事主体冻结与训练快照等边界；综合训练深度后由D0034恢复 |
| [Military_D0034_Review.md](Reviews/Military_D0034_Review.md) | 综合训练广度／深度的接受与未决转换公式 |
| [Shared_D0035_Review.md](Reviews/Shared_D0035_Review.md) | Absolute D语义、consumer确认与独立Catalog待办 |
| [Harbor_D0037_Review.md](Reviews/Harbor_D0037_Review.md) | 港口双线新基线、旧规则取代与军事两处改名；机制与候选命名/未决分开 |

## 文化展示记录

- [D0031调查与候选](Records/Culture_Era_Presentation_D0031.md)：保留当时未批准的选项比较和静态接口边界，不重新成为待批准任务。
- [D0032 Hybrid D批准](Records/Culture_Era_Presentation_D0032.md)：**仍是现行展示接受来源**，Authority继续指向它；当前[文化阅读版](../../Design/Culture.md)已呈现其玩家规则。路径归档不降低成熟度，不表示已实施。

以上两份展示记录保持原字节，彼此相对链接仍有效。正文中的`Content/Culture_D0029.json`按原Design目录语境理解，实际正式文件见[Culture_D0029](../../Design/Content/Culture_D0029.json)。

## 原位保留的冻结材料

| 原位材料 | 保留原因 |
|---|---|
| [Commerce候选审阅](../../Design/Commerce_Freeze_Candidate_Review.md) | D0032接受记录明确要求此前候选不变；原文相对链接指向Content，已由Commerce_D0032取代的候选不参与当前玩法 |
| [Military候选审阅](../../Design/Military_Freeze_Candidate_Review.md)与[原始用户记录](../../Design/Military_Freeze_Candidate_User_Record.md) | D0033明确保留原件；二者互链，候选还依赖Content、Spec、ChangeLog、Workflow与D0008；原始用户文本不重写 |
| [完整Spec修订D0001—D0034](../../Design/Revisions/) | 保持34份冻结原文字节及目录整体；冻结军事候选仍直接链接D0008，既有Historical架构快照仍直接链接D0001。拆散迁移或兼容空壳不在本轮增加 |

部分旧Spec快照本来就保留了原Design目录基准的相对链接；本轮没有修写这些冻结正文。追溯时可通过[Content](../../Design/Content/README.md)、上述审阅表和原位Revisions目录查找相应版本，不把原始路径字符串当作当前任务读取指令。

当前Spec保留在Design根目录以维持既有selector和冻结引用。ChangeLog继续是Workflow acceptance入口，并被冻结军事候选直接引用，也保留原路径。没有另建Canonical层或重构Content。
