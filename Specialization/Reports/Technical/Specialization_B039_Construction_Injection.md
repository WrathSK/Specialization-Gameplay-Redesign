# B039 施工队前置：当前目标生产力注入DEV探针

Document Owner: Codex
Build: P0-B-039 / modinfo50
Design: D0010 CREW-001..004（不改规则）

## 已调查路径

HD Gameplay/HD_Common.lua:307–355 CityAddProgressPercentage识别当前Building/District/Unit/Project，通过Utils读取成本/进度，再amount=min(amount,cost-progress)，最后city:GetBuildQueue():AddProgress(amount)。函数使用math.floor是百分比计算规则，不能机械迁移为我们的固定Crew设计。

HD UI/Additions/HD_Utils.lua:7–40实现GetCityCurrentBuildQueueCost/GetCityCurrentBuildQueueProgress，调用GetBuildingCost/Progress、GetDistrictCost/Progress等。Gameplay经ExposedMembers.DLHD.Utils调用这些现有只读UI辅助函数；不可宣称纯Gameplay所有getter均可用。B039按该既有HD方式调用，缺接口明确拒绝，无静默猜测成本。Great Engineer的MODIFIER_SINGLE_CITY_GRANT_PRODUCTION_IN_CITY另见HD DL_GreatPeople.sql（Joseph Paxton、Amount680、KeepOverflow0），但针对Wonder的目标约束/引擎行为仍需研究，不据此认定District通用。

## 本轮部署范围

DEV调试操作，不是正式施工队：任意己方测试文明城市可预览Building/District/Wonder当前队列，点Inject 250 (DEV)免费注入最多250，无需/不消耗单位，不生成项目或Crew。不写专业/投资/网络数据。不用于正常平衡游玩。

ConstructionProbe.Prepare只读当前目标并保留本会话预览（城市、turn、目标、成本、已投入、min(250,remaining)）；每次预览取消同城旧预览。Apply在消费预览后再次读真实队列，拒绝类型/成本/进度/回合/owner变化；只调用一次AddProgress(min)，超额不传引擎、不递归。异常后不自动重试，重复Inject必须重新Preview。空队列/单位/项目拒绝，当前完成目标拒绝。读后目标类型一致性检查防止helper读期间目标变化。

调用后读取当前队列成本/进度，显示是原目标还是后续目标。这个报告不是完成/零overflow证明：原生Modifier倍率、HD钩子、完成事件、队列内部延迟/既有后项进度都需实机。报告Next progress非0时不能在未知前值下直接归为overflow；测试要求下一项预先0进度。实际AddProgress参数非整数时不自行floor，行为仍待证据。

Preview/Inject取代当前可见住房/总督诊断按钮，旧控件和回调仍隐藏保留；9任务按钮不增加。四类Lv3收益及此前科研/文化UI延迟均未改。

## 验证

STATIC_CONFIRMED：本机HD先例/辅助函数/KeepOverflow0；所有Lua语法、manifest50、文件路径、9任务按钮。LOCAL_SIMULATION_PASS：真实ConstructionProbe预览零注入、Building/District/Wonder单次cap、模拟超额不进下项、重复操作、空/非法目标、旧进度/回合/归属拒绝、调用不确定后不重试。test_construction_probe.py。模拟不能证明引擎生产Modifier和overflow。

USER_GAME_TEST_REQUIRED：仅B039四个目标/溢出小案。尚未实现固定五项目→五单位、移动/消耗、项目完成授予或持久重复保护。CREW-004速度缩放和档位时点仍TBD，当前只用标准速度固定250 probe，不自行增加门槛或定正式速度规则。后续项目/单位接入前再处理必要决定。
