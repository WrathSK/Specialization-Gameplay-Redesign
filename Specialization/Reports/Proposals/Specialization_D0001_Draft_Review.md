# D0001草案审阅说明

Owner: Codex
Design Authority: User
State: DRAFT_PENDING_USER_ACCEPTANCE

## 变更范围

修改Design Spec/ChangeLog、README/AGENTS、Status的职责与待办说明；Architecture保持字节不变，不执行A0002/sync/WHAT去重。Source/Tests/manifest、Historical、既有Backups及截图保持不变。新的迁移前文档快照另存DevelopmentBackups，不覆盖旧文件。

当前D0001是整个项目WHAT草案，不是只记录已实现能力；Rule ID已经分配用于审阅。ACCEPTED FUTURE DESIGN只表示用户此前已确认的未来范围/机制；整个D0001仍未接受，Community与+15%XP候选保持原状态。

## 来源核对

1. 完整读取当前README/AGENTS、Design两文件、Architecture A0001和Status S0001。WHAT取自A0001，不从旧报告恢复废弃设计。
2. 新用户附件73622cc1-3bb8-42d1-9bf6-4d5e59fbb43d提供职责变更、全部Future补充、无source时Strength=0及共同成长明确规则。
3. 只读搜索当前/历史文档、R1备份及最初两份用户附件，寻找Landscape/Religion/Government正文；仅找到列入未来范围、其它系统对它们的引用，没有找到完整Lv1–4/Network原文。Great Work的Landscape是作品类型，不可替代Landscape专业。
4. Military Lv1“common specialist support”、Lv2Housing/GPP只保留原骨架；除摘要明确的Lv3 5F5P、槽位和候选XP外，不自动把v0.1四专业数值扩展到未来专业。待用户明确继承范围。

## 从A0001迁入草案（不从Architecture删除）

独立测试文明；完成区域锁专业；Settler/Potential/总督ACTIVE；四专业完整Lv1–4；Shared Housing/GPP；Base与Actual游戏语义；网络方向、全载荷/去重/撤销/Commerce IV；Research/Culture sqrt与最高有效ACTIVE；Industry标准化/金币折扣；施工队五规格与浪费溢出；Great Work时代保值/基础相邻；已有Spaceport/Entertainment意图。

Spec不含API、Lua调用、Probe版本或P0通过流水。住房/GPP与表格用Rule ID引用，避免设计文档内多份数值表。

## 从本次Future摘要写入

Military四级骨架和Mobilization；Harbor完整海商/海军双线；Diplomatic三线、永久保护国、使者tier、Spy生存/能见度；九区域和平外交任务；Community临时资格/人口承载/自动迁移；三栋Local/Regional组合与虚拟专家排除规则；Aqueduct明确公式；Dam待定X；Canal十专业产出表/替代+6Gold意图；Hangar/Airport；Spaceport卫星后局部自动双向联网。

## 所有未决项

Spec OPEN-01至OPEN-18是当前完整草案审阅索引；不把其余Future细节简写成“framework established”。

- SOURCE_DETAIL_REQUIRED：Landscape、Religion、Government完整既有原文缺失；这是资料缺口，不证明用户从未设计过。
- PROVISIONAL：Community整体、首次Neighborhood资格/锁定、Lv1–4、槽位递减、Migration参数/权重/底线。
- BALANCE_CANDIDATE_NOT_ACCEPTED：+15% XP/军营工作专家；Military曲线/训练/带教/动员参数另TBD。
- 其它TBD/决策：继承/旧档/并发完成、首都本地接入、Boost精度、Industry合并、Great Work标准/类别/倍率、Crew速度/档位、Harbor出口模型和海军、外交多源/永久名额降级/Spy、联盟任务解锁奖励、娱乐范围公式/有效专家映射、Dam X、Canal叠加/归属/Community分支、Airport系数/叠加。

## 内部交互问题（没有擅自裁决）

1. “永久保护国”与ACTIVE下降后的较低名额如何同时成立：当前明确保护性质，但超额关系未定义，OPEN-12。
2. Community“取得资格”是否立即锁专业，以及与一般首次完成规则关系：PROVISIONAL，OPEN-14。
3. Local有效专家与“实际工作专家”定义必须逐能力对照；不准虚拟人数获得native支持/GPP，但哪些自制Science/XP等公式计入需明确，OPEN-15。
4. Research/Culture max不能自行推广Military/Community/Industry；各source-specific结算保留未决，不能假装共享同一L选择规则。
5. Harbor远端Base/相关相邻与本城较高Actual比例边界尚无精确公式，OPEN-11；不私自统一。

未发现本次Research/Culture max与A0001直接矛盾；无源归零是用户明确补足。未发现理由推翻已确认v0.1数值。上述问题是未定交互/资料缺口，不是技术失败导致的玩法改写。

## 检查与停点

仅做文档结构/Rule ID/必需内容/状态/链接检查与未改文件校验，不运行功能测试、不生成游戏PASS、不启动游戏。没有把draft hash写入Architecture，也没有登记正式同步。等待用户审核和明确接受D0001。
