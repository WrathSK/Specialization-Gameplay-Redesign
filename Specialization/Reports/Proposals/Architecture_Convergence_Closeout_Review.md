# 架构收敛结项审阅稿

整理日期为 2026-11-17。本文件汇总当前实现与证据，供 Owner 结项审阅。正式规则沿用 [Architecture A0185](../../Architecture/Specialization_v0.1_Architecture.md) 和现行 Design。实际进度由 [Status](../../Status/Specialization_P0_Status.md#current-authoritative-state) 维护。

## 负责人摘要

本轮已经完成共享事实、变化通知、网络收益、独立行动与项目、HD／官方环境适配，以及旧实验模块的生产职责移交。B527 是这轮工程迁移的集成候选，最新 HD 巨作更新和冷读档已有实机记录。

当前可以审阅是否按已批准范围结束这一轮工程迁移。原版文化网络正向收益留待正常游玩时观察；B527 较早冷读档还缺首个本地回合的清理完成记录。两项继续保留各自证据状态。正式架构中的几段实现说明仍需按下表作事实性同步。

## 固定审阅基线

| 对象 | 已核对的定位 |
|---|---|
| 正式规范 | Architecture A0185、Design D0060，四个现行专业内容 D0059 |
| 候选运行代码 | B527.554，源码提交 `5cf9b48463cc5f875ebab562cc89c9cedb9d0bcb` |
| 当前安装来源 | `1495cbd1a32d2877df5aab8ecedcacbd733f35d9`，与上述候选的 Mod 字节一致 |
| 本稿所汇总的证据检查点 | `e85b0aca98cb8d037d530a38d5849c2a37e5758a`，Status S1091 |
| 当前运行包 | 314 个文件，SHA256 `fc7bca2fd8799ca17f453ed1e9123aa64286f941712230ebcd82f39a31447a26` |
| 稳定对照与恢复 | main B489.516，运行源码 `ce497054ed0ba440a03c5a7a66dfafc0d5721c3d`，337 个文件；临时部署回执确认其恢复包一致 |

后续文档提交继承这组代码基线。审阅前用 `git diff --exit-code 5cf9b484 HEAD -- Mod` 确认运行源码关系。部署身份以现行回执为准。

## 已完成的主干工作

| 实际职责 | 已落地的结果与主要实现 | 证据入口 |
|---|---|---|
| 环境装配与共享城市事实 | 官方与 HD 分别提供定义输入，共享目录解析有效升级链、Tier 与 D；当前城市基础从 Store 进入 EffectiveFacts。对应 Environment SQL、OrdinaryBuildingCatalog、NativeFacts、CurrentSpecializationFacts。 | [环境与 Tier](../../Status/Specialization_P0_Status.md#effective-building-tier-and-shared-depth-connected-locally--s0910)、[当前城市入口](../../Status/Specialization_P0_Status.md#read-current-city-foundations-directly-from-the-store--s1073)（O1／O5a） |
| 事实变化与责任交付 | FactChanges、FactConsumerBindings 和 RuntimeWork 交付有范围的任务，由各能力独立接管和确认；写入屏障、同回合再次变化和部分失败各有验证。 | [交付组合验证](../../Status/Specialization_P0_Status.md#effect-delivery-verified-and-synchronous-transition-policy-isolated--s0926)（O2） |
| 网络与实际收益 | 商业化、文化网络、工业标准化各自读取可靠事实并维护自身效果；被动收益保留、可靠失效撤除、严格交易证明和部分写入结果分别处理。 | [网络能力接管](../../Status/Specialization_P0_Status.md#passive-network-effects-independently-take-their-existing-audit-scopes--s0924)、[集成比较](../../Status/Specialization_P0_Status.md#prepare-the-two-profile-integration-candidate-for-native-acceptance--s1037)（O3） |
| 永久历史、项目和行动 | Store 保存历史与收据。认领、时代对话、工程研习复用技术计时机制，各自保留资格和奖励；投资、施工队、重组保持独立的不可逆操作凭据。 | [HD 行动验收](../../Status/Specialization_P0_Status.md#focused-b413-native-evidence-reviewed--s0902)、[两环境集成验收](../../Status/Specialization_P0_Status.md#b489-two-profile-native-acceptance-complete--s1047)（O4） |
| 启动、退出与恢复 | RuntimeComposition 管理启动和普通订阅，必要退出责任预先登记；最新旧巨作清理使用现有 Gameplay 加载／回合边界。 | [启动隔离](../../Status/Specialization_P0_Status.md#ordinary-effect-listeners-attach-after-initialization--s0930)、[最新清理移交](../../Status/Specialization_P0_Status.md#move-old-boost-startup-cleanup-to-gameplay-boundaries--s1088)（O5b） |
| UI 接入与呈现 | 官方和 HD 采用各自原生 UI 基底。机构、生产项目和单位行动通过既有接口读取实际状态。新版双语文案已接入。 | [原版生产交互](../../Status/Specialization_P0_Status.md#official-production-interaction-verified-on-b443--s0949)、[新版文案](../../Status/Specialization_P0_Status.md#complete-reviewed-bilingual-catalogue-integration--s1070)（O6） |
| 旧实现退出 | 工业旧载体由 StandardizationEffects 清理；其他旧实验清理由实际责任模块或 LegacyCleanup 承接。旧城市外壳、旧 Dialogue 和 Boost UI 等在真实缺文件组合与回滚验证后退出。仍有职责的 SQL／历史定义继续保留。 | [工业清理移交](../../Status/Specialization_P0_Status.md#move-retired-industrial-carrier-cleanup-to-standardization--s1072)、[最终候选](../../Status/Specialization_P0_Status.md#pin-the-retirement-candidate-for-native-integration--s1089)（O7） |
| 集成与范围验收 | B489 已完成记录范围内的 HD／官方联合验收。B527 继承适用部分，另核对新启动边界与巨作更新。 | [既有联合验收](../../Status/Specialization_P0_Status.md#b489-two-profile-native-acceptance-complete--s1047)、[B527 实机结果](../../Status/Specialization_P0_Status.md#b527-hd-great-work-and-cold-load-evidence-reviewed--s1091)（O8） |

各项结论限于对应记录的代码、环境和场景。表中“已落地”表示职责已经接入生产路径，实机覆盖按下表判断。

## 验收证据与尚缺记录

| 对象 | 当前可确认的范围 |
|---|---|
| HD／官方既有功能 | B489 两套实际加载清单、科研／文化实际收益、商业化、合同与冷恢复已有定域验收。普通行动和工业能力按各自早期验收继承。 |
| B527 HD 巨作 | Owner 验证 ACTIVE I 无风雅熏陶；ACTIVE IV 后市中心／剧院贡献为 1／2；同一时代作品不叠加；外城新增中世纪作品不影响首都，移入后变为 2／4。 |
| B527 HD 冷读档 | 实际 94 个加载目标与固定 HD 基线一致。冷上下文 seq54 收到加载事件，首个本地回合 T2 seq183 确认 B055_GW 及相关控制项 READY。 |
| 较早 B527 冷读档 | 记录加载完成，但采集停在 T1，缺少首个本地回合的清理完成样本；该组对应的原生加载清单未保留。继续标为未观测。 |
| 原版文化网络正向收益 | HD 早期已验证接通和冷读后的正向收益。当前两个环境使用同一 Gameplay 模块与效果 SQL，原版其他网络能力已有覆盖。原版这一能力的正向组合仍待观察。 |

原版文化网络采用正常游玩／平衡测试中的机会观察安排。届时可以同时保留实际加载清单和冷读后的首个本地回合记录。两项的待观察状态继续保留在当前信息中。

B527 原始材料位于忽略目录 `local/legacy-workspace/Specialization/Status/Validation/Evidence/B527_Readiness_GreatWork_20261117/manifest.json`，SHA256 `65c30333af5863963276aed3ad9a37e45af96b4c1f09ce129dbeeacb348b1239`。三个采集会话、19 份原始文件和部署回执的定位由该 manifest 提供。本批巨作收益来自 Owner 观察。采集中的断帧和诊断上限仍按原记录保留。

## 结项后继续保留的事项

| 事项 | 保留方式与推进条件 |
|---|---|
| 回合开始的商路核对及既有兜底 | Owner 已明确保留。若以后取得可靠自然事件替代证据，再定域审阅是否收窄入口。[保留决定](../../Status/Specialization_P0_Status.md#keep-the-turn-boundary-network-checks-pending-a-natural-replacement--s1029) |
| 原版文化网络与本轮冷读记录缺口 | 按上节在后续原版游玩中补观察。全环境原生验收继续保留这项精确限制。 |
| 施工队特殊计数顺序、迟到回调和认领异常来源 | 两城同级同回合在已测计数路径下通过。其他路径沿用唯一凭据保护；真实异常发生时留证调查。[已测范围](../../Status/Specialization_P0_Status.md#focused-b413-native-evidence-reviewed--s0902) |
| 人文考察团边境位移 | 独立的实机问题，沿用现有观察与异常调查安排。 |
| 历史测试夹具与版本差异 | 旧归属、住房／GPP和训练替身中的非通过项保留各自基线及断言。影响到相关路径时再核对。本轮没有执行全历史测试，已有数目不能相加为当前缺陷总数。[最近覆盖说明](../../Status/Specialization_P0_Status.md#restore-current-presentation-regression-coverage--s1071) |
| 新双语文案排版 | 源码与本地呈现检查已有记录，真实语言下的布局可在后续 UI 查看时观察。 |
| 支持范围 | 当前构建新档与同构建读档。未来专业、城市易主新玩法和额外环境支持按原有授权边界推进。 |

## 已有工作量与退役对照

| 对照 | 来源与可解释的结果 |
|---|---|
| B489 → B527 包文件 | 337 → 314，其中移出 25 个旧路径、加入 2 个本地化 XML；Lua 文件为 208 → 186。表示包内职责退出规模。 |
| 共享事实的局部组合 | S1037 记录的三 writer 模型中，锚点采样由 3 次变为 1 次，城市索引读取由 4 次变为 2 次，效果一致。 |
| 普通网络待确认 | 既有本地组合记录了被动效果 owner 的零 Audit／零写入，以及相同证明返回后的有界唤醒。 |
| 最新候选静态检查 | S1089 已记录 186 份 Lua 5.1 编译、31 份 XML 家族解析、619 个 File 引用和 10 个 LuaReplace 引用。 |

这些是源文件、局部工作量及静态结果。全局帧率、长局内存改善和原生耗时仍需各自测量。

## 正式实现说明的最小同步候选

以下均对应 [架构总说明](../../Architecture/Specialization_v0.1_Architecture.md) 中的当前实现描述。正式语义和保存合同沿用现行已接受规则。

| 所在段落 | 旧描述与拟同步内容 | 对照依据 |
|---|---|---|
| “运行入口与职责”中的当前专业事实 | 将正常路径写为 Store.Base → EffectiveFacts → CurrentSpecializationFacts；旧 CityFlow 分支按实际隔离测试用途说明。 | [EffectiveFacts](../../../Mod/EffectiveFacts.lua)、[S1073](../../Status/Specialization_P0_Status.md#read-current-city-foundations-directly-from-the-store--s1073) |
| “事实、保存与当前资格” | 将旧 Binding／Completion／Journal／Flow 外壳仍在运行树的描述，更新为当前 Store 入口及已完成的外壳退役；保留严格身份和永久历史要求。 | [城市外壳退出](../../Status/Specialization_P0_Status.md#retire-the-detached-city-registration-files--s1079) |
| “运行入口与职责”中的巨作事实 | 标明 DialogueRefresh 的现行样本传输和 GreatWorkFacts 接收；时代对话奖励仍由现行独立 owner 负责。 | [传输移交](../../Status/Specialization_P0_Status.md#transfer-dialogue-work-receipts-and-exact-old-withdrawal--s1087) |
| “收益应用与玩家呈现” | 将 B234 旧 CopyYields／StandardizationDiscount Lua 清理外观，更新为 StandardizationEffects 自有撤除；其他旧实验由 LegacyCleanup 等既定 owner 承担。 | [S1072](../../Status/Specialization_P0_Status.md#move-retired-industrial-carrier-cleanup-to-standardization--s1072)、[LegacyCleanup](../../../Mod/LegacyCleanup.lua) |
| UI 结构说明中的早期原型 | 补充官方／HD 基底与当前机构、生产、单位适配入口，引用各自实现和验收范围。 | [基底选择](../../Status/Specialization_P0_Status.md#official-and-hd-ui-bases-selected-separately--s0929)、[当前呈现回归](../../Status/Specialization_P0_Status.md#restore-current-presentation-regression-coverage--s1071) |

本轮先形成上述精确候选。架构规范的正式同步随后按现行修订流程处理。

## 审阅顺序与结项条件

1. 先核对本稿中的实现范围、证据边界和保留项是否符合已批准的收敛目标。
2. 代码复核按职责展开。主干迁移证据沿表中各阶段入口读取；稳定基线后的运行包变化使用 `git diff ce497054 5cf9b484 -- Mod`，重点核对当前 Store、StandardizationEffects、LegacyCleanup、GreatWorkFacts 与 Gameplay 启动职责。
3. 明确原版未观测部分在本轮工程结项和后续全环境验收中的归属。继续记录其真实状态。
4. 审阅认可后，完成上节正式实现说明的事实同步，按已接受范围记录工程结项。main 晋升与稳定部署按发布流程另行处理。

如需交给外部审阅者，由 Owner 转交本稿及对应固定提交。复核重点为实际职责是否全部接管、已移除路径是否仍有有效依赖、证据继承是否成立，以及保留项有无遗漏。本轮未执行新的外部审计。

本轮准备工作已复核现行 Context Lock、当前部署包哈希、四份 S1089 定域工件及 S1091 原始证据 manifest。功能测试沿用原执行记录，本轮没有重跑。完整机器工件保留在原本地忽略目录，源码与执行入口提供重跑依据。
