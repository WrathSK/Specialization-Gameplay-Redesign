# Test Batch B006：独立后台读取（最多3项）

> 最新用户结果：B007新三路线存档B6-1/B6-2已通过，不重复。删除城市变体仅旧缓存失效，完整重建未通过；原删除商人未执行。以[最新结果](Specialization_P0_B007_User_Result.md)为准，下文测试安排保留历史。

> 历史版本B006：B6-1用户截图停在UNKNOWN / LoadScreenClose。当前运行包为B007；仅按[调度修复与单项重试](Specialization_P0_B007_Background_Dispatch_Fix.md)重试B6-1，B6-2/B6-3暂停。下文保留原计划；10秒兜底依赖Context更新回调，尚未实机证明。

USER_GAME_TEST_REQUIRED。运行版本P0-B-006 / modinfo13。没有正式网络/收益，所有结果标UI_SHADOW_ONLY。按钮Background routes是新增的只读查看入口，Route state (Game)是原Gameplay任务探针；本批主要用前者。

## B6-1：加载后后台自动读取

1. 由你手动重新加载已有四商路的Test存档，使脚本更新到B006；不新开局、不新增商路。
2. 进入地图前不打开原生/BTS贸易界面、Read routes (UI)或P0窗口。正常进入地图后打开Specialization P0→**Background routes**。无需选城市。
3. 截图一次：应为COMPLETE_UI_SHADOW、当前商路4条，显示四行城市名方向与商人ID。触发原因应为自动初始化/load/Gameplay就绪等，而不是按钮。

PASS：后台已生成完整四条记录，查看按钮仅显示；原路线应是Edinburgh→Stirling、Stirling→Aberdeen、Aberdeen→Edinburgh、Aberdeen→Stirling（以仍包含这四条的存档为前提）。Gameplay对照通常MATCH，首次尚未就绪时可能PENDING；PENDING不是完整对照通过。

FAIL/停止：没有后台记录、UNKNOWN/错误、少路线/错误端点、只有使用旧Read routes (UI)才出现。请截图，不为补成功去点旧读取按钮。若第一次恰好显示UNKNOWN且原因是dirty，约1秒后仅再次查看一次，记录两次状态；持续失败就停止。

## B6-2：同样存档再次读档，无需开贸易窗口

1. 在B6-1正常的前提下，不改路线，保存到测试副本，退出主菜单再加载。
2. 重复“先进入地图，后看Background routes已有缓存”，截图。

PASS：4条与相同端点自动重新出现；不需要新建路线、过回合、打开BTS或旧Read routes。generation/seq是当前context内序号，不要求比上次大。此测试是新增后台UI来源的恢复，和已通过的Gameplay任务读档是不同层。

FAIL：UNKNOWN、端点丢失、旧缓存冒充（版本/本次采样不存在）、需要额外操作路线才恢复。失败即停，不做B6-3。

## B6-3：删除一名在运行商路的商人（仅方便执行时）

1. 保留B6-2的四路线测试存档作为回退；在此分支关闭P0窗口。
2. 若现有Cheat Panel能直接删除一个指定单位，删除**一名正在执行上述路线的商人**，不删除城市、不创建新路线、不同时删除多个单位。若没有方便的删除入口，跳过并告诉我，不要求为此宣战或等待几十回合。
3. 不打开BTS或Read routes (UI)。完成删除后查看Background routes缓存。若仍显示4条，约10秒后再查看一次，以便核对独立fallback；不要点击任何刷新按钮。

PASS（本项仅UI shadow撤销）：当前完整数量4→3；最近变化+0/-1，已移除行对应所删商人，其它三条仍在。请保留“触发原因”，区分事件刷新与TIMER_FALLBACK；如果只靠fallback移除，记录为fallback通过，事件路径仍待确认。Gameplay可能PENDING，因为其旧样本已dirty；不用为强求MATCH继续过回合。

FAIL：fallback之后仍4条、删错/多删记录、UNKNOWN持续不恢复。回传截图即可；失败后不要继续删商人。该测试不等于战争、取消、自然结束和征服场景也通过。

## 回传

最多每项一张截图，默认文件名放DevelopmentReports/ScreenshotInbox即可；按时间对应B6-1/B6-2/B6-3，说明是否跳过第三项。无需上传、重命名、剪贴板或手抄内部ID。

若失败，多保留第一张错误状态和一次后续查看的状态。没有后台记录/标题仍旧时可保留本机Modding.log；Lua.log仅在实际存在时提供，不为此修改游戏日志设置。完成后停止，等分析，不继续其它专业机制测试。
