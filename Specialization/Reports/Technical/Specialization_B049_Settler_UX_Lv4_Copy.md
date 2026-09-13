# B049：移民投资UX与Lv4复制计算准备

Document Owner: Codex
Build: P0-B-049 / modinfo62
Design: D0012 unchanged (RES-004 / IND-004 / IND-NET-003 / TERMS-002)

## 本轮结果与边界

B048百分比按用户“B048 pass”登记通过。移民UX已实现；Research/Industry的50%只完成只读计算与多源选择，没有新收益发放。不是完整Lv4，也不把计算报告当成效果实现。没有更改设计、投资事务、Crew事务或任何SQL。

## 移民UX

两个行动共用固定90宽容器，Prepare offset46、Confirm offset0，每按钮宽44。未准备即预留确认空间；准备后左侧显示确认、原位置显示预览。Crew位置规则不变。移民使用结构化后台View，复用InvestmentAction的facts/settler/anchor/ledger比较，只能撤销临时plan，无永久写入。UnitActions.Run以及InvestmentAction.Prepare至文件末尾与本轮前备份逐字相同。

| 状态 | 文案 |
|---|---|
| 非法位置 | 投资专业化；将移民移动至本城的专业区域，即可投资城市专业化。 |
| 合法未准备 | 投资专业化；消耗1名移民，使本城专业潜力永久提高1级。换行当前潜力：X级 → Y级；点击后可预览投资结果并进行确认。 |
| 已到4级 | 投资专业化；专业潜力已达到4级，无法继续投资。 |
| Prepared | 投资预览；当前专业、当前潜力、投资后潜力、消耗1名移民，空行后高级专业能力仍需满足对应的总督条件。 |
| Confirm | 确认投资；消耗此移民，使本城专业潜力永久提高至Y级。此操作无法撤销。 |

重复点击预览不发请求。坐标、回合、Owner、专业锚点、Potential、账本及完成状态失效时撤销临时预览；确认时原有结算还会重新验证。读取失败隐藏Confirm、不把失败当合法。后台约0.5秒刷新与Crew一致；同两次采样之间未观察到的移动往返不能声称被完整事件追踪。确认原逻辑保留，不许旧资格对新目标执行。原生动作栏实际像素仍需用户后续顺带观察，不派独立UX测试。

## Lv4实际产出复制调查

本机DebugGameplay只读查询：Building_YieldDistrictCopies只有BuildingType、OldYieldType、NewYieldType三列。Coal Plant为Production→Production，Grand Hotel为Culture→Culture；没有可填50%的比例字段。不能杜撰Amount参数。HD UI/Replacement/CitySupport.lua:644–647按district:GetYield读取区域产出，另用GetAdjacencyYield读取相邻。这支持读取候选，但并不能证明与引擎Building_YieldDistrictCopies在所有行业/跨yield情形完全等价。历史B002也明确保留此边界。

HD Gameplay/CityYield.lua的ChangeYield最终拼接YIELD_CREATOR名称并AttachModifierByID；不是通用小数解决方案。B030固定城市Modifier已出现小数缺失，不能重用并宣称50%支持。B038每人口小数是另一个Effect，直接借用会让固定复制额受人口影响；需先证明补偿与精度，未采用。没有恢复线性Boost、没有取整50%、没有使用城市总产出代替区域基数。

Lv4CopyRead提供：
- Gameplay验证当前城市专业/ACTIVE；NetworkBridge.RecipientSources复用现有本回合、signal、路线数、端点检查，再derive当前接收来源。
- Industry仅保留当前ACTIVE4来源及专业区域ID；UI读取这些精确区域的Production；计算一半并按实际金额max，非相加、非仅按等级选源。
- Research读取本城四类标准区域中非Campus已完成区域的六类yield，合计×0.5；标为标准区域小计。其它RequiresPopulation区域显式提示不完整，不冒充完整设计范围。
- 所有值保留Lua浮点，无floor/round。未知/缺失source不当0；网络未刷新显示原因。无Property写入、无载体、无自动收益，也不改变后台网络权威。
- 新Read Lv4 copy复用原Read specialists位置，后者Hidden保存；不增加面板按钮行数。读取须点击，因为此项是诊断；后续正式收益不允许依赖此按钮。

## 当前阻塞与下一步

IMPLEMENTATION_LIMITATION：固定50%收益的原生小数承载仍未证实，因此Research/Industry正式复制尚未接入。不是已证明无法实现，不需要用户现在选择改设计。下一步先确认候选区域基数，再独立研究可撤销的精确小数发放（含城市百分比影响），通过后方可启用收益。GW-001/003仍有时代曲线、类别、倍率设计待决，本轮不发起额外决定；Commerce IV之前暂停的小数研究不视为已解决。

## 验证

STATIC_CONFIRMED：定义/本机代码证据；不等于游戏运行通过。LOCAL_SIMULATION_PASS：test_b049_settler_copy.py执行真实UI、InvestmentAction、UnitActions、NetworkBridge、Lv4CopyRead；不是Civ VI实机。覆盖固定位置、连续两次点击、重复预览、Potential/Owner/地块/完工失效、cap、实际mock单单位消耗与账本提交、Crew旧回归、来源去重/过期拒绝、整数与半点、最高来源下降、缺失来源、六yield及Campus排除。全部Lua语法/XML/manifest可解析，新增Lua已ImportFiles并列Files。所有SQL、Crew/投资结算、D0012 hash保持。

USER_GAME_TEST_REQUIRED：仅新基数读取/多源输出预览，见B049小批次；移民UX后续顺带。不扩大用户B048 PASS范围。没有启动游戏。
