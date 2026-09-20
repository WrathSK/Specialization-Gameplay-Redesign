# P0-E1 — 城市身份保存门禁：具体计划

Status: 用户已授权实施；B088.115只读交付LOCAL_SIMULATION_PASS，原生连续性门禁待核验，见[实施合同](P0_E1_Identity_Evidence.md)。以下保留原计划范围。原计划状态：PLANNED_NOT_AUTHORIZED。P0-D3与U1前置原型用户验收已完成；U1布局/文字及完整Presentation后置。当前B087.114/modinfo114，源码8dc6118。只规划，不实施/部署。
Authority: A0161与D0032目标架构、当前Design D0035及四专业authority。Shared D的语义/Lv2更新不改变本批身份保存门禁；Military不纳入v0.1。

## 1. 为什么下一步是E1

总计划D1→D2→D3后为E1城市身份门禁→E2进度保存适配→F学术传统，不存在已定义的D4。学术传统需要“同一座城”、持久年龄和暂停/续算；Culture Dialogue/见闻及未来合同还有不同ownership政策。先证明城市连续性，不通过UI/carrier/当前位置猜历史。

本批只建立可验证的身份/保存候选合同与只读迁移预演。**不正式迁移专业账本，不增加收益，不启用学术传统，不恢复旧继承writer。** E2正式接管及F能力仍单独授权。

## 2. 已核对现状与受保护边界

- BindingProbe使用SPC_DEV_BINDING_B013_TOKEN＋每player账本；uid形如DEV-B013-P…、记录锚定owner/cityID/坐标，DEV counter上限32。只能在原验证范围使用，不是已证明跨owner永久cityKey。本批不顺手移除上限或改first-city绑定流程。
- CityJournalProbe/CityFlowProbe/InvestmentAction/EffectiveFacts构成当前专业与投资凭据读取链，原记录、Start、writer保留。
- Gameplay明确InheritanceIsolation=true；CityInheritance/InheritanceShadow旧实现有Property写和projection能力，不能直接重新Start当新方案。
- CityInheritanceRead已有按需只读前后快照，可复用观察字段，坐标只定位，不作为永久ID；只存本次加载watch，不能宣称跨load身份验证已完成。
- P0-C/D1/D2/D3、Network及U1仍用当前已验证事实，不接入未确认的新cityKey授权。

## 3. 窄范围交付

### A. 身份证据与小型schema

明确cityRef（当前owner/id/x/y及本次对象证据）、cityKey（候选永久身份）与generation（夷平后同地新城不得复用）的区别。记录native转移事件参数、旧新引用、哪些City/Game Properties保留、读档行为；不能只根据事件名称假定参数可靠。

拟定独立身份记录schema/version、引用映射、已消失/待确认/冲突状态及History/mode最小合同。History只记录有证据的历史最大/转换，缺失不伪造；REALLOCATING只保留独立类型，不产生该Gameplay状态。cityKey只在证据完整时提出映射；冲突/部分数据标HELD（不允许迁移），未知标UNKNOWN，确认不同城市拒绝合并。

### B. 只读迁移预演

读取现有binding/journal/flow/investment/template记录，输出：可映射、不完整、冲突、无证据，以及依据。预演前后现有Property/凭据逐值相同；不重锚owner、不修补、不删除、不发收益。缺失历史不以“新记录空账本”掩盖。

旧开发档按实际状态分类：完整自建城可预演；部分写/锚点冲突HELD；无可证明连续性的征服/夷平历史不自动认领。可要求未来使用新测试档，但不能本轮决定所有旧档永久不兼容。

### C. 按需短诊断与原生门禁

主报告只给选定城市、当前引用、连续性结论、可迁移状态及一行原因；详细页才展示旧新锚点/哪些记录保留。不打印整份账本、隐藏合同内容或全世界城市列表。

优先复用已有只读观察路径。新观察器若需要，独立接收明确事件并保存固定上限的少量观察；不每帧扫描。load一次必要初始化、事件定域、按需读取；丢事件/乱序进入待确认，不能靠位置猜测接续。

本批默认**不写新的持久cityKey或identity marker**。若静态/只读实机不能证明跨load/owner连续性，不把门禁强行判PASS：报告缺哪项证据，再提出隔离、显式启用、只写新测试命名空间的最小技术实验供审阅。不得为实验改原专业账本、恢复旧继承模块或自动采用猜测identity。这样E1可以交付本地预演，但整体跨owner门禁未通过时E2仍关闭。

## 4. 实施顺序 / 预计文件

1. 完整读取Binding/Journal/Flow/Investment与隔离继承模块，列精确Property keys、引用和写入点；只读查native/HD事件先例。
2. 纯identity evidence resolver与migration preview模型（可新小文件，不建通用事务框架）；只读诊断接现有Gameplay dispatch/P0Panel，优先复用空闲按钮。
3. 实际旧记录fixture与事件模型测试，保护所有旧writer/收益；如需native观察，给一个独立测试档的短流程。
4. 形成E1证据与支持矩阵后停止；commit/push实现不等于E1全部实机通过。

可能涉及：只读新模型/诊断文件，Gameplay启动及只读dispatch、P0Panel/Localization、modinfo、tests。Binding/Journal/Flow旧writer默认零改动；如出现无法避免的语义变更，先报告而非混入E1。无carrier/收益SQL/Design变更，无UI润色。

## 5. 本地验收矩阵

| 情况 | 预期 |
|---|---|
| 原owner/id/位置/token及账本一致 | 唯一匹配，预演不写 |
| 改名 | 不因城市名生成新身份 |
| 易主/夺回证据完整 | 同一候选cityKey、currentRef更新；不转移能力/永久成果所有权 |
| 仅坐标相同、ID复用、夷平再建 | 不能沿用旧身份；无充分证据保持UNKNOWN/拒绝 |
| 缺token/缺ledger/冲突/重复token/部分投资凭据 | HELD，无自动repair或补历史 |
| 重复、乱序、load同回合事件 | 不创建多份身份/历史，不重复应用 |
| 冷读档没有上一session内存 | 只用实际持久证据，缺失明确UNKNOWN |
| Current/History/REALLOCATING | History不启用旧能力；REALLOCATING不冒充NONE；本批仅schema/model |
| 10000无关通知 | 无新增完整扫描、request、Building/Property写；观察缓冲有上限 |
| 前序回归 | A/B/C/D3及Network输出、旧投资凭据不变；无旧继承Start |

所有正常fixture不得隐藏module errors。STATIC与LOCAL_SIMULATION不是native连续性PASS。

## 6. 最小未来用户测试

只在确实需要native证据时安排**一个独立测试存档、一座已有专业城**：记录→用现有可控方式转移给另一owner→记录→夺回→记录→另存并重新加载→记录。诊断直接显示对照结论，用户不手算ID；不要求重跑科研收益测试，也不要求长局自然征服。

先检查当前Cheat/UI是否有可控转移方式；没有则报告并设计最小替代观察，不让用户盲等AI。夷平重建优先本地fixture；仅native标识仍有歧义时再提一次独立补测，不把它强塞默认流程。跨owner过程中旧能力是否继续可用不作为E1目标，本批不修其Gameplay继承。

## 7. 退出、回滚、下一步

E1完成需：只读预演/原记录不变通过、冲突可解释、至少所需native城市连续性证据可复核、schema与支持边界清楚；旧first-completion/投资writer及隔离状态仍保持。若native证据不足，标TECHNICAL_INVESTIGATION_REQUIRED，不进入E2。

无新的Gameplay设计决定阻塞开始E1只读实施。各专业征服Legacy仍后置，城市识别不等于授权继承收益。回滚以B087完整包和独立测试存档为界，本批不改存档schema；任何追加持久实验必须另列其保存兼容边界。

之后顺序：E1门禁通过→单独审阅/授权E2进度保存→F学术传统。计划阶段未部署；实施后按W0003保护门禁另记部署。E1原生门禁未通过前不进入E2。
