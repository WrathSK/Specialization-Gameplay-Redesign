# Specialization P0 Status — B010

## CURRENT AUTHORITATIVE STATE

2026-09-11。运行包P0-B-010 / modinfo 17，仅独立测试文明+诊断。当前目标：可靠的Gameplay Trade Route State。**尚未发现已确认的权威全集provider，不能宣称正式状态层已完成。** 本轮完成可替换provider的离线状态层与NetworkState来源原型，已有自动单位operation探针；B006新增独立后台UI shadow读取与Gameplay数量/ID对照，无正式收益。

当前规则与状态以Architecture本文、B007_User_Result实机记录、B008_User_Result实机记录、B009_User_Result实机记录及B009_Shadow_State实现报告为准；旧版本报告已归入历史。用户负责实机，助手没有启动或操作游戏。

B005最新用户两图：自动采样与存读档后的4名商人任务列表通过，但所有X0/Y0/X1/Y1为nil。端点参数候选未通过，完整路线来源仍BLOCKED。不重跑B4-1/B4-2。详见Specialization_P0_B005_User_Result.md。

## CONFIRMED

| 项目 | 状态 | 范围 |
|---|---|---|
| 独立测试文明 | USER_GAME_TEST_PASS | 用户A1选择开局确认；本地独立ID与资源引用另有静态检查 |
| City Property | USER_GAME_TEST_PASS | marker读写与重新加载后保持，未再Mark |
| 总督 | USER_GAME_TEST_PASS | 新局present/established、2/3/4阈值随升级、调离原城撤销 |
| 区域/专家 | USER_GAME_TEST_PASS | 类型、存在、完整建造、实际工作人数 |
| UI相邻 | USER_GAME_TEST_PASS | 基础与政策翻倍后相邻区分；不是原生复制算法验收 |
| UI商路 | USER_GAME_TEST_PASS | 端点、三条时读档、第四条加入后同城两条分页 |
| Gameplay任务计数/枚举/读档 | USER_GAME_TEST_PASS | 两次自动采样均4条计数、4名商人、4个匹配任务，同样ID；不包括端点 |
| B007后台UI初始化/读档 | USER_GAME_TEST_PASS | 新存档三条路线，两次COMPLETE_UI_SHADOW、Gameplay数量/ID MATCH；并非Gameplay权威端点 |
| B009后台新增/标准缓存 | USER_GAME_TEST_PASS | 两图3→4、+1/-0；新增Stirling→Edinburgh，旧三条保留；标准count=4、rev 1→2 |
| B008城市删除完整重建 | USER_GAME_TEST_PASS | 后台3→1、+0/-2，保留Aberdeen→Stirling；publish-complete采样；Gameplay对照PENDING |
| B007城市删除缓存失效 | USER_GAME_TEST_PASS | CityRemovedFromMap后旧snapshot清除；不包括重新生成完整集合 |
| Gameplay商路事件 | USER_GAME_TEST_PASS | 新建路线端点捕获；事件历史读档丢失，不能代表现有路线 |
| 数据库/资源/原生Requirement | STATIC_CONFIRMED | 隔离SQLite/资源引用/源码，不扩大为所有Mod组合兼容 |
| 本轮源码研究 | STATIC_CONFIRMED | Pirates Gameplay计数/潜在合法性API；HD Temp_Interface实际是UI；引擎内存在operation读取符号，不能证明其实际返回语义 |

历史USER_GAME_TEST_FAIL（B008已修复本次删城场景）：B007的B6-3-CITY（Cheat Panel删除城市）停在UNKNOWN / CityRemovedFromMap；旧缓存正确失效，但刷新次数仍2，未生成剩余当前集合。系统通知/Context更新均0。不是原B6-3删除商人案例。详见B007_User_Result。

历史B006的B6-1停在UNKNOWN / LoadScreenClose；B007直接加载刷新已由本次B6-1/B6-2用户实机确认通过。

此前USER_GAME_TEST_FAIL：B005当前四个operation端点参数均nil（两次截图），未获取起终点。B004的GetUnitType错误已由GetType修复并经本次用户测试通过；不能将端点缺失归因于旧错误。

历史USER_GAME_TEST_FAIL：Gameplay city:GetTrade、城市/玩家GetAssignedGovernor缺失；旧宽泛采样曾卡住、剪贴板交付未成功。已用窄探针/原生门控/截图及日志处理，不恢复宽泛对象扫描。

## LOCAL_SIMULATION_PASS

B010选中城市只读角色事实：test_city_role_facts.py验证首都候选、专业/潜力缺失不猜测、总督条件上限与矛盾保护；test_specialization_p0.py、test_background_routes.py回归通过。

B009后续离线拓扑衔接：新增DeriveShadow入口，B009标准路线+显式MOCK角色，输出READY_SHADOW_PROVENANCE_ONLY；多类型全载荷、城市去重、多源来源保留、断源/中心身份/ACTIVE/模板变化与UNKNOWN隔离通过。test_shadow_network_state.py与原test_trade_route_state.py通过，未改运行包。详见Shadow_Network_Integration。

B009新增标准UI shadow缓存：schema/标量复制、revision幂等、3→1撤销、同数量换端点、输入/返回修改隔离、UNKNOWN清空、reset；test_shadow_route_state.py、test_background_routes.py、test_specialization_p0.py、test_trade_route_state.py均通过。

B008新增事件发布/播放完成批次刷新与最多3次尝试：无SystemUpdateUI/Context回调、过渡端点错误后恢复、重复边界不重扫、持续错误次数上限及新信号恢复均通过。test_background_routes.py、test_specialization_p0.py、test_trade_route_probe.py通过。

B007本地回归已通过：不调用Context更新时，LoadScreenClose立即采样；重复dirty由不带dt的SystemUpdateUI合并刷新。test_background_routes.py与test_specialization_p0.py均通过。

已有test_background_routes.py：独立无控件context的init/load/dirty/fallback，去重/撤销/端点异常/计数一致性、错误清空、过期Gameplay对照、shutdown及重新加载覆盖伪造缓存。P0按钮只读后台缓存已加入test_specialization_p0.py，三个相关回归脚本通过。

- test_specialization_p0.py：Lua/XML、既有UI/Game请求、身份限制、专家/总督、相邻、商路方向分页、错误路径；B004模块接入检查。
- test_specialization_identity.py：隔离数据库执行，旧记录不覆盖；部分hash/icon环境为fixture。
- test_specialization_network.py：sqrt、独立k、ACTIVE、城市去重、有限值与数据库TEXT存储。
- test_trade_route_state.py：空→1→多路线；同起点/同终点/同城对不同商人；重复刷新、重复dirty；仅移除A；端点易主/毁灭/无效；战争；load从MOCK全集恢复并覆盖错误缓存；未知/部分/UI/事件源拒绝；身份冲突；中心身份/ACTIVE变化；多网络来源、免费资格撤销仍保留其它资格；不计算多源L或收益。
- test_trade_route_probe.py：无UI的初始化/读档/回合自动采样、dirty合并、商人移除、闲置与缺失getter、只针对测试玩家。测试是mock；实际CountOutgoingRoutes与任务枚举现已用户确认，端点参数nil另记候选失败。

## USER_GAME_TEST_REQUIRED

当前B010仅核对选中首都/非首都的ROLE行，见B010_City_Role_Facts。无需重做总督升级/专家/路线测试；此前离线拓扑衔接无实机需求。

B9-1已USER_GAME_TEST_PASS：3→4、+1/-0、标准缓存rev 1→2，见B009_User_Result。B009模块装载及新增更新已确认，本批结束，不追加重复测试。

B008的B6-3-CITY已USER_GAME_TEST_PASS：3→1、+0/-2，publish-complete完成当前全集重建；见B008_User_Result。本批结束，不再重复。

B4-1/B4-2已经返回，不重复。B007的B6-1/B6-2已通过，不重复。B008城市删除完整重建已通过；原B6-3商人删除未执行，无需用户寻找新的cheat工具。真实自然结束/取消/掠夺/战争/征服/夷平生命周期仍未实测。

面板unknownOperations=0只表示任务类型已知，四个端点参数nil仍缺失。正式起终点恢复不能因为计数4/4就标PASS。

## B009 当前shadow候选

独立BackgroundRoutes.xml/lua自动读取，不打开任何窗口；Background routes按钮只看缓存。状态COMPLETE_UI_SHADOW/UNKNOWN与Gameplay MATCH/PENDING/MISMATCH分开，不修改GAMEPLAY_CURRENT准入。B007改为load/回合事件直接刷新，SystemUpdateUI处理dirty；SetUpdate仅作备用，10秒计时兜底仅在其实际被调用时成立。新增刷新/系统通知/Context更新计数。详情B007_Background_Dispatch_Fix报告。正式权威来源仍BLOCKED。影子路径初始化/读档已通过；B007城市删除后dirty未消费已由B008发布完成路径修复，并通过本次用户实机测试。三图两种更新计数均0，不再将SystemUpdateUI或10秒计时作为本场景已可用的兜底。B008新增GameCore事件发布/播放完成刷新，失败跨边界最多3次尝试；发布完成刷新已USER_GAME_TEST_PASS，失败重试分支仍仅LOCAL_SIMULATION_PASS；不改变来源权威性。

B009标准状态层：ShadowRouteState.lua输出READY_UI_SHADOW、复制读取、完整替换、dirty失效与单独revision；后台只读导出ReadNormalizedRoutes。保留owner:cityID快照身份，不假造永久UID。未接运行中的NetworkState/正式Gameplay状态层，来源准入不放宽。离线NetworkState现有单独DeriveShadow入口，仅接受明确UI影子路线+MOCK角色，详见Shadow_Network_Integration。

B010只读角色事实通过既有Read governor显示：capital候选、未知专业/潜力/ACTIVE及总督条件上限。当前没有可信专业账本写入者，SPC_P0_FIRST_SPEC只作诊断，不能进入网络来源；详见B010_City_Role_Facts。

## BLOCKED / DESIGN DECISION REQUIRED

1. 真实Gameplay全集provider缺失：离线状态层不在modinfo里，不运行网络。不用UI自动桥接或历史日志冒充。
2. 单位任务读取与已测存读档场景通过；当前端点参数nil。完整端点访问、完成后清除、war/capture/raze等生命周期仍缺证据。
3. 多源Research/Culture权威L与Industry合并未定：只保留sourceUID/kind/ACTIVE/templateRevision及每recipient到source的资格，不采用max/average/sum/逐中心sqrt求和。
4. 永久City UID跨征服和重建未实现。当前prototype由resolver输入稳定UID；探针不写UID、不改存档。

## 文件变更

B010修改Probe.lua选城角色读取及版本、P0Panel.xml标题、manifest17；新增test_city_role_facts.py、B010_City_Role_Facts，更新Architecture/Status；B009运行包已备份。

本轮修改DevelopmentTests/NetworkState.lua，新增test_shadow_network_state.py与Shadow_Network_Integration报告，更新Architecture/Status；运行包仍B009。

本次新增B009_User_Result并同步Architecture/Status及B009测试报告结果指引。代码未改、版本仍B009，无需换包。

B009新增ShadowRouteState.lua、test_shadow_route_state.py及B009_Shadow_State报告；修改后台集成、版本/manifest16、test_background_routes.py、Architecture/Status。B008运行包已备份。

本次新增B008_User_Result并同步Architecture/Status、旧批次结果说明；运行代码未改，无需换包。

B008修改BackgroundRoutes.lua批次调度/计数、Probe.lua/P0Panel.xml/manifest版本15、test_background_routes.py；新增B008_Batch_Flush报告，更新Architecture/Status。B007运行包已备份。

本次用户结果核对：新增B007_User_Result，更新Architecture/Status与旧批次结果指引；运行代码未改，无需重新安装。

B007修改UI/BackgroundRoutes.lua调度与诊断、Probe.lua与P0Panel.xml版本、modinfo版本14、test_background_routes.py。更新Architecture/Status及B006报告/批次的历史说明，新增B007_Background_Dispatch_Fix。B006运行包已备份至DevelopmentBackups/SpecializationP0-P0-B-006。SQL与正式机制未改。

B006新增UI/BackgroundRoutes.xml/lua、test_background_routes.py；修改TradeRouteProbe.lua诊断数据与dirty revision、P0Panel.lua/xml只读入口、Probe.lua/manifest版本和后台context注册、test_specialization_p0.py。SQL未改；B005备份已保存。新报告B006_Background_Routes、Batch_B006；Architecture/Status同步。

以下为B004/B005已有实现：

运行：新增TradeRouteProbe.lua；修改Gameplay.lua、Probe.lua版本、UI/P0Panel.lua/xml、SpecializationP0.modinfo。新增按钮只看缓存；新增自动采样只输出诊断。数据库SQL未改。

离线：新增DevelopmentTests/TradeRouteState.lua、NetworkState.lua、test_trade_route_state.py、test_trade_route_probe.py；更新test_specialization_p0.py模块装载；NetworkStrength.lua注释明确未接入。

文档：重整Architecture/Status；新增B004_Trade_Route_State、Batch_B004；修正Network_Sqrt的旧版本/旧测试计划说明；旧报告加历史标识。原文件完整快照Historical/*_through_B003.md；运行包备份DevelopmentBackups/SpecializationP0-P0-B-003。

## HISTORICAL NOTES / superseded

旧Status完整保存Historical/Specialization_P0_Status_through_B003.md；旧Architecture保存同目录。旧线性、per-route、Commerce IV固定增加与多中心求和均无当前有效性。旧A001–A004/B003已通过却仍待测的描述不再出现在当前待测清单；B003显示本身没有用户独立验收，不伪造PASS。
