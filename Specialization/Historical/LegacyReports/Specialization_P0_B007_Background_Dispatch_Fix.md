# B007：后台路线调度修复与B6-1重试

> 最新用户结果：B007新三路线存档B6-1/B6-2已通过，不重复。删除城市变体仅旧缓存失效，完整重建未通过；原删除商人未执行。以[最新结果](Specialization_P0_B007_User_Result.md)为准，下文测试安排保留历史。

## CURRENT AUTHORITATIVE STATE

运行P0-B-007 / modinfo14。独立后台UI影子诊断，未接入正式RouteState或任何收益。纯Gameplay权威全集来源仍BLOCKED。

## 用户证据 / USER_GAME_TEST_FAIL

ScreenshotInbox中2026-09-11 12.13.23 PM截图：B006 Background routes为UNKNOWN，原因LoadScreenClose，无可用快照。说明后台context与加载监听已运行，后续延迟采样没有完成。没有显示getter错误，不能断言路线读取API失败；空context的SetUpdate未运行是待核对的调度解释。

12.13.26 PM截图是已有Gameplay探针：仍4条计数/4名商人/4个任务，端点参数nil。没有改变之前的确认范围，无需重测。

## STATIC_CONFIRMED

旧实现load只mark dirty，后续依赖ContextPtr:SetUpdate。B007改为LoadScreenClose和两个回合边界直接dispatch；Events.SystemUpdateUI处理dirty及Gameplay信号，避免仅依赖空context逐帧回调。官方Base/Assets/UI/TradeOverview.lua的SystemUpdateUI注册提供静态UI先例，不证明本context实际调度已通过。

按钮仍只读缓存，不采样、不打开贸易界面。增加刷新次数、系统通知次数、Context更新次数。错误清除可用快照并显示UNKNOWN。原Context定时刷新保留为备用；10秒兜底只在Context更新实际运行时成立，独立回合全量刷新不依赖该计时器。

## LOCAL_SIMULATION_PASS

- test_background_routes.py：不调用Context更新，LoadScreenClose直接生成完整集合；重复dirty通过SystemUpdateUI（无dt）合并刷新，系统通知1、Context更新0。原去重/撤销/异常隔离/关闭与缓存重建回归通过。
- test_specialization_p0.py：Lua/XML/manifest与窄探针、面板只读等回归通过。

这些是mock与静态检查，未启动游戏。SystemUpdateUI实机触发、后台getter结果与生命周期撤销仍需用户证据。

## USER_GAME_TEST_REQUIRED：只重试B6-1

1. 手动退出到主菜单，再加载原来的四商路Test存档；无需新局或改变路线。
2. 不打开BTS/原生贸易界面，也不点Read routes (UI)。进入地图后打开P0，确认标题P0-B-007，再点Background routes。
3. 保留一张截图到ScreenshotInbox，默认文件名即可。重点是状态、刷新次数/系统通知/Context更新、错误行与路线数。

PASS：COMPLETE_UI_SHADOW，4条现有路线及正确方向，刷新次数至少1；不需要打开贸易界面或新建商路。Gameplay对照PENDING须单独保留，不当作MATCH通过。

FAIL：持续UNKNOWN、错误、数量/方向错误或只有打开其它读取入口才恢复。若首次UNKNOWN，约1秒后仅再点Background routes查看一次；仍失败就停止，保留两次截图。不要求过回合补成功。

标题旧版表示包未重新加载，不能用于判断B007机制。Context更新0本身不判失败，只要其它调度已产出完整快照。

B6-2/B6-3暂停，先确认本项。无需再截图Route state (Game)，无需剪贴板或手抄ID。暂不索取不存在的Lua.log；如果标题仍旧/脚本未加载，可回传现有Modding.log。
