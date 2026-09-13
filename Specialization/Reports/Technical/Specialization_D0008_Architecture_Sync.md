# D0008架构同步与范围评估

Document Owner: Codex
Architecture Revision: A0047
Design Spec Synced Through: D0008
Design Spec SHA256: 3dca4434a468f81a8e203a7a19d8c87dff5b24170d0667f50283ed2a23bd761c
Sync Status: SYNCED_WITH_LIMITATIONS
Evidence: STATIC_CONFIRMED（文本/hash核对，不是引擎实现通过）

已比较D0007冻结原文与当前Spec、ChangeLog；D0008未删Rule ID，新增HARB-006至009与DIP-MISSION-004至014。NET-RC-004的跨系统说明变更不修改Research/Culture本身公式。以下为HOW/范围索引，具体WHAT只引用Spec，不建立第二份数值权威。

| 设计入口 | 当前成熟度及架构处理 |
|---|---|
| SCOPE-001/002/003 | v0.1范围不扩展。以下Harbor/Military/Diplomatic Missions均Future，无需暂停或重启现有P0 |
| HARB-005至009、MIL-013 | ACCEPTED DIRECTION：海军II–IV默认平移已登记，不再把默认训练位置整体列为未决；合法Harbor/本城City Center、排除Canal。商业/GPP不覆盖，Naval资格/特殊建筑互动/动员仍独立TBD；未来复用经验路径仍待API研究 |
| MIL-004、NET-RC-004 | PROVISIONAL共享全国动员pool及阈值模型，最高有效ACTIVE和recipient去重；不能继续把多源归属/位置整体写作空白，也不能移植为Research/Culture或海军正式结算。未来需独立进度账本、合法单位/编制资格、生成位置与无位保留进度。tie-break与未定资格保留，不现在实现 |
| DIP-MISSION-001至003 | 接受任务框架，一域多任务、无需逐一和平镜像；成功不保证secondary reward。未来任务结果和奖励roll分离，XP/Era Score与奖励触发不可混为同一成功标记 |
| DIP-MISSION-004至007 | 公共外交奖励仍PROVISIONAL；商业三任务和剧院三任务分别建类型，不统一flat yield；Campus Eureka是概率且fallback默认不启用；Import Fair时效/次数等不提前补参数 |
| DIP-MISSION-008 | 只修正目标盟友那一份移民压力，不更改Community基础公式/成熟度，不扩大到全球贡献 |
| DIP-MISSION-009 | Infrastructure Coordination仅PREFERRED DESIGN CANDIDATE，跨owner辐射技术待审；Civilian Conversion仅THEME CANDIDATE ONLY。没有技术调查或默认fallback |
| DIP-MISSION-010至014 | 航天Eureka、持续海贸、军演递减XP、朝圣合格belief yield、外交/政府骨架分别隔离；Space自动联网不改、不给飞天生产加成；军演函数/朝圣白名单/系数与奖励范围按Spec保持暂定或TBD |
| OPEN-10/11/13、文末交互说明 | 旧整体未定描述由D0008分项成熟度替代；其它OPEN和Current v0.1规则不补定 |

Architecture旧D0002等段落及冻结报告为当时研究，不倒写。当前Future应以本索引和D0008为准。没有将接受整份文档理解成候选全部定稿。无源代码/API可行性验证、无军事/海军/外交功能开发；当前B020证据等级不变。
