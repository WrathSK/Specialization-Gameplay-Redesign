> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

# P0-A-004：Governor / Specialist（3项小测试）

全部状态USER_GAME_TEST_REQUIRED。A1、A2已通过，不重复。由用户启动/操作游戏；本地开发者不启动或等待游戏。

## 共用准备与记录

下次启动游戏加载原测试文明存档即可；如当前游戏仍开着，需由你退出并重新启动一次以加载新Lua。面板标题应为P0-A-004。保持与A2相同的Mod组合；不要新开局，已有进度不足可继续该局，或先做具备条件的项目。缺少前置就回报“暂未具备条件”，不是FAIL。

选中己方测试文明城市，点 **Read governor** 或 **Read specialists**，随后 **Show / Copy**。屏幕显示ACK和多行数字即能截图，不要求剪贴板工作。不点Mark，不需要抄ID。每次状态改变后必须重新点对应Read再Show；只点Show不会刷新。

界面：assigned=是否分配；established=是否建立；base=已拥有的基础晋升数；extra=已拥有非基础晋升数；owned=两者合计；titleCandidate=任命1+extra（候选值，非历史支出）；Engine Req2/3/4是现有原生条件写出的原始属性，nil或0暂视为未激活候选，1为激活候选。没有ACK、ERROR或PENDING均不是成功。

## A3a — 只增加一个头衔

前置：一座城市有已建立的普通总督，当前仅任命、没有额外晋升；另有1个可用头衔。尽量选无免费晋升的普通总督。暂不具备时先做A4，或把现有总督界面截图回传以调整测试。

1. 选该城，Read governor → Show / Copy，截图 `A3a-before`（连同总督晋升界面截图，证明当前已拥有技能）。预期established=true、titleCandidate=1、Req2未激活。
2. 在总督界面为同一总督购买一个普通晋升，不迁移、不换政策、不结束回合；回到同城重新Read governor → Show / Copy，截图 `A3a-after`。
3. 预期extra增加1、owned增加1、titleCandidate从1到2；established仍true；Req2从nil/0到1；Req3/4保持nil/0。

PASS：所有变化如上。候选计数不符或Req2不符为FAIL（这也可能揭示设计语义与引擎计数不同，不自行接受变化）。若数字只是暂未刷新，可关面板重开再Read一次；保留两次截图。只有过回合才变化应明确记录延迟，不能按即时刷新PASS。

## A3b — 只比较建立前后（复用A3a总督）

前置：两座己方城市，该总督有恰好2个titleCandidate，目标城没有其他总督。总督已经拥有更多头衔也可测试，但注明实际数值，不预期Req3/4均为0。

1. 把该总督迁移到目标城。选原城Read governor → Show，截图：assigned=false、Req2应撤销为nil/0。
2. 选目标城，在到任途中Read governor → Show，截图 `A3b-arriving`：assigned=true、established=false；即便titleCandidate=2，Req2也应nil/0。
3. 不增加晋升、不要再迁移，正常推进至总督界面显示已建立。选同一目标城Read governor → Show，截图 `A3b-established`。
4. 预期只有established从false到true，titleCandidate不变，Req2从nil/0到1（有更多头衔时对应Req3/4也应激活）。

PASS：原城撤销，目标城建立前不激活、建立后激活，候选头衔不变。FAIL：API返回异常、途中已激活、建立后未激活、原城残留或候选计数自行变化。过程中城池易主/总督被移除等改变前提时重设该项，不把混合变量结果作为依据。

## A4 — 专家人数0/1变化（与Governor测试独立）

前置：己方城市至少一个已完成专业区域及提供专家槽的建筑，有空余可调配人口。优先Campus/Theater/Industrial Zone/Commercial Hub；本城专业区域不超过6个。没专家槽不能用区域已建成代替。人口锁定和现有工作分配可截图留底，以便测试后恢复。

1. 城市“管理市民”，找到该专业区域的专家分配；选一个有可用槽的区域。Read specialists → Show / Copy，截图 `A4-before`，记该行workers=N及complete=true。
2. 只向该区域多分配1名市民（从普通地块调入，不改变建筑/人口/政策，不结束回合），重新Read specialists → Show，截图 `A4-plus1`；预期同一行workers=N+1。
3. 移出刚才这1名专家，重新读取，截图 `A4-restored`；预期同一行恢复N。最好同时截到市民分配界面，证明不是新增专家容量。

PASS：同一区域workers严格N→N+1→N，complete始终true，与实际分配人数一致。FAIL：数值不变、跟着容量而非在岗人数变化、ERROR/PENDING或卡住。显示NO_SPECIALTY_DISTRICT表示前置不足，不算通过。

## 任何异常

如果卡住立即停止该项，不重复点击；回传最后操作和能获得的画面。若仍响应，Show / Copy会显示最后阶段/ERROR，可截图。保存可获得的Lua.log、Database.log、Modding.log、GameCore.log（下次启动前）；当前目录为工作目录下Firaxis Games/Sid Meier's Civilization VI/Logs。没有Lua.log不必为日志重跑。

每项回传前后截图及PASS/FAIL/未具备条件即可，不用人工计算复杂数据。通用RAW_API_ONLY和USER_GAME_TEST_REQUIRED字样是探针固定声明，不会自行随测试变成PASS。本批结束后先回传，不继续Adjacency/Trade。
