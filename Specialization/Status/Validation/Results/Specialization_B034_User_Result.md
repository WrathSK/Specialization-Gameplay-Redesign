# B034用户结果：住房开启、逐层增加与撤销后的显示延迟

Document Owner: Codex
Build: P0-B-034 / modinfo42
Design: D0010（SHARED-001继承原规则）
Result: USER_GAME_TEST_PASS（用户已实机验证，限下述观察范围）
Known Limitation: 同回合撤销后城市面板住房可能暂未刷新；用户明确接受，不阻塞后续开发

## 证据与测试变体

用户用已有Research/Potential2城市测试：起初无总督、ACTIVE1、住房6；派遣前总督已2级，建立后触发ACTIVE2。不是B034原案例的投资1→2触发，但同样验证ACTIVE门控。初始住房6及总督准备为用户口头证据；五张图按文件名时间顺序逐张读取。

| 图/时间 | 回合 | ACTIVE | expected / carrier | tiers | changes / refreshes | 城市面板人口/住房 |
|---|---|---|---|---|---|---|
| 1 / 09:46:09 | 5 | 2 | +1 / +1 | NONE | 5 / 47 | 2/7 |
| 2 / 09:46:29 | 5 | 2 | +2 / +2 | 1 | 6 / 48 | 2/8 |
| 3 / 09:46:41 | 5 | 2 | +3 / +3 | 1,2 | 7 / 49 | 2/9 |
| 4 / 09:46:55 | 5 | 1 | +0 / +0 | NONE | 10 / 51 | 2/9（旧显示） |
| 5 / 09:47:06 | 6 | 1 | +0 / +0 | NONE | 10 / 69 | 2/6 |

五图均为city=65536 / STIRLING (TEST)，面板B034；图2、3为用户说明同回合购买一级、二级建筑，读数逐层正确；截图本身不显示具体建筑名称，不额外推定购买种类。没有ERROR文字。

用户额外口头观察：Cheat增加人口也没有立即更新城市面板，随后开始生产移民触发人口显示更新，住房同时恢复6。此附加操作没有独立截图，不伪造时序/数值采样。

## 判定

- USER_GAME_TEST_PASS：本城总督门控开启住房，两个已建层级各追加一份，ACTIVE回1后载体全部撤销，下一回合城市住房回到基准6；用户接受观察到的显示延迟。
- 关键区别：carrier是逐项HasBuilding读到的载体数量，不是城市实际总住房Getter。图4证明载体已为0；图4→5 changes保持10，回合刷新没有再次移除载体。因此不能把回合后的9→6解释为Lua到下一回合才开始撤销。
- 同回合城市面板立即更新没有通过，保留已知限制。用户接受该延迟不等于已证明所有内部住房计算即时更新。
- 本次未回报保存重载、重复读取、不相关专业族、所有HD建筑层级、Lv1岗位保持或其它总督附加住房组合；不扩大实机PASS，也不因此追加补测。本批按已观察范围关闭，无新用户测试。

## 代码机制检查：STATIC_CONFIRMED

STATIC_CONFIRMED只表示源码证据，不等于实机根因证明。

1. 运行Lv2Housing.lua:44–49使用RemoveBuilding后HasBuilding复核，确认后才增加changes；Describe:76–92仅读取，既不调用Audit也不调用城市GetHousing。与图4已移除、图5无额外移除吻合。
2. 本机原版Base/Assets/UI/Panels/CityPanel.lua:484 Refresh先调用GetCityData再ViewMain；:317通过data.Housing更新住房标签。CityProductionChanged/Updated/Completed、CityWorkerChanged等路径会RefreshIfMatch；LocalPlayerTurnBegin也注册刷新。所检查的原版注册列表没有直接订阅GovernorAssigned/Established/Changed，也没有订阅本Mod内部载体移除通知。
3. HD UI/Replacement/DL_CityPanel.lua:4–15包含Expansion1或基础CityPanel，:100–101调用BASE_Refresh；HD CitySupport.lua:571从pCityGrowth:GetHousing读取Housing。DL.modinfo含此面板替换配置。这支持“等待其它城市事件刷新”的解释，但未枚举本局所有UI Mod或记录实际事件顺序，不能声称精确根因已完全定位。
4. 用户开始生产移民后更新，与生产事件会刷新城市资料的代码路径一致。不因而声称需要改变人口或生产才能真正撤销住房，也不将原版是否存在其它同回合住房下降场景作为结论。

本轮不加全局UI强制刷新、不模拟生产/人口变化、不修改游戏数值。未来若顺手改进界面，可优先发送只读刷新通知；若要区分UI缓存与引擎住房缓存，应在同一时点采样原生GetHousing，当前不要求用户额外测试。

## 归档与保护

五张原图已移动到[Evidence/B034](../Evidence/B034/)，原文件名保留，移动前后SHA256逐项相同，见[manifest](../Evidence/B034/manifest.json)。截图收件箱未移动。

运行源码、Design、Tests不改；无新模拟或测试执行，不启动游戏。变更前文档及保护hash见DevelopmentBackups/Specialization-before-B034-result。Architecture A0079 / Status S0081记录本结果；下一项共同Lv2基础GPP，住房刷新延迟不作为前置阻塞。
