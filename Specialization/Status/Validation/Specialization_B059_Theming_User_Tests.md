# B059 — Oxford两著作主题化最小对照

Document Owner: Codex
Runtime: P0-B-059.83 unchanged
Status: STATIC_CONFIRMED setup / USER_GAME_TEST_REQUIRED native relationship

本机只读DebugGameplay数据库Building_GreatWorks：BUILDING_OXFORD_UNIVERSITY，GREATWORKSLOT_WRITING，NumSlots2；ThemingUniquePerson1，ThemingSameObjectType1，ThemingSameEras0；ThemingYieldMultiplier100、ThemingTourismMultiplier100，NonUniquePersonYield/Tourism0。原版Base/Assets/UI/GreatWorksOverview.lua:267、330、581使用IsBuildingThemedCorrectly；现有报告复用同一API。以上只证明配置/接口，不证明实际主题化及结算。

## 操作：同存档、原Culture ACTIVE4城市

1. 若原城可建牛津大学，用Cheat完成（不修改Mod/建筑规则）；把当前《变形记》和《紫式部日记》移进两个著作槽。保持其它作品/建筑/政策/总督/专家不变。不同作者、同类著作符合数据库条件；两个creator时代仍D2。以原生巨作UI和报告主题化建筑>=1、未知0为准。若无法建造或主题化未成立，只回传一张当前报告/原因，停止，不要求另开局或凑作品。
2. Dialogue OFF → Record GW baseline，截图1。必须在建造/移动完成后重新记录，不比较此前无Oxford基线。
3. TEST100 → Read Great Works，截图2（若主题化小计尚未刷新可过一回合再读，保持收藏不变）。完成后AUTO。无需再测25/50，100避免小数干扰。

## 记录/解释

读作品总C/T及“其中作品C/T”主题化小计；基线对照行若未出现也不妨碍两图人工计算。主题化状态必须两图相同。若城市里只有这座合格主题化建筑，主题化小计可隔离原有其它作品；含Relic/Product的其它主题化建筑保持不变但需说明。

两作品基础合计5。若主题化为100%，单独C基线候选10（其它modifier可能改变实测）。时代对话100%若先得+5再吃主题翻倍，差值候选+10；若主题与本项同层加算或独立追加，差值候选+5。旅游业也比较额外+5或+10，而非把包含全部既有倍率的旅游总数直接乘2。这是用于区分的候选，不预设引擎必须哪一种；不同/零差值则继续查作用域或刷新。

PASS分别登记：主题化原生判定成立；固定主题化收藏时本项实际收益响应；倍率关系与读数吻合。用户D0022已接受正常原生关系，无论自然加算或倍乘均不为旧设计重建补偿系统。其它作品类别/最终对外累计旅游不由本case覆盖。
