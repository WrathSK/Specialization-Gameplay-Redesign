# D0002 → A0009 架构同步

Document Owner: Codex
Design Spec Synced Through: D0002
Accepted Spec SHA256: 22c5023528aa1d0380ca96e89a8551d55d73d87bcfad8bb4a21e5ef29f4efa32
Architecture Revision: A0009
Sync Status: SYNCED_WITH_LIMITATIONS

## 用户摘要

已核对D0001冻结原文与当前D0002，设计hash与ChangeLog一致。变化属于未来Military经验体系，当前v0.1专业成长与网络规则未改变。已将新规则的接口需求与待研究项同步到Architecture，未实现军事收益，不要求游戏测试。

## 差异与Rule适配

STATIC_CONFIRMED：此处只指文档差异、hash和规则对应关系经静态核对，不表示经验API或游戏运行通过。

| Rule | 架构处理 |
|---|---|
| SCOPE-001 / header | 当前设计权威更新至D0002；SCOPE-002当前v0.1范围不变 |
| MIL-001 / MIL-005 | 对应基础支持/GPP接口与正常Combat XP modifier；正常XP不通过独立加XP模拟。实际工作人数、训练来源追踪及正常经验叠加/上限保持需以后验证 |
| MIL-002 / MIL-007 | Insight与正常XP分开结算；以后需要战斗身份、单位实际Promotions（含合法合并继承）、相关城市实际工作专家、避免同场战斗重复奖励的凭据。不能由累计XP倒推P，不能自行添加硬上限 |
| MIL-006 | 不生成Academy虚拟专家，不改HD三级建筑路线 |
| MIL-008 | Future/OUT_OF_V0.1；ENT虚拟专家适用范围保持未决，不默纳入E |
| OPEN-10 | XP增幅/整条Insight曲线不再列为候选；仅保留Spec中尚未决定的Future事项 |

完整diff另核对：从第2节到Military前的正文完全一致；Harbor至OPEN-10前正文完全一致。其余变化为Military正文、OPEN-10及接受header/结语。D0001规则覆盖表继续作为未变Rule的同步证据，见[原同步报告](Specialization_D0001_Architecture_Sync.md)。本报告补充差异，不复制完整数值规则表。

## 技术限制与研究边界

Military依然未做完整API可行性研究。同步是登记设计对应的实现责任，不是承诺这些接口已可用。未来需验证：训练来源如何保留及城市资格变化怎样关联；战斗何时采样E/P；实际晋升读取与合并继承；正常XP与额外Insight的结算顺序；重复战斗事件和存档期间如何避免重复发奖。若细化需要新的玩法决定，届时交用户确认，不由实现代码默选。

正常8 XP cap是本次Accepted Spec要求保持的行为边界，本轮未独立验证各Mod组合下引擎实际结算。不得用额外XP伪造正常modifier、不得把额外Insight压回普通cap，也不提前实现Harbor/Aerodrome镜像。

用户需要决定：无新增；Future既有未决保留。
用户需要测试：无。
Codex下一步：继续当前v0.1城市事实接入准备，Future经验API研究延后。
