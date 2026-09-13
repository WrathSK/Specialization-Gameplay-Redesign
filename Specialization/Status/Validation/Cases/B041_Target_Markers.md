# B041：合法目标地图标记（三小案）
Document Owner: Codex
State: USER_GAME_TEST_REQUIRED
Build: B041 / modinfo53

回主菜单重载原存档，不需新局。无消费、无产出变更。标记是独立小标签，不是伟人整格染色；只显示当前可见地块。不表示本回合能走到。无须再验证B040脚下读数。

1. 选中移民：已有Potential1–3且可继续投资的专业区域应自动出现INVEST标签；Potential4城市不出现。单位不用站到目标上。只需观察已有测试城，无需新建。可打开Unit sites看标记数量/unknown cities。
2. 工人施工预览：选工人，打开Unit sites，点Builder targets ON / OFF (test)，关闭报告观察地图。正在建建筑的所属区域、在建区域、当前奇观地基应出现BUILD TEST。切换某城当前队列至单位/项目，等待最多约6秒，旧施工标记应消失。只用已有目标，不重做注入。
3. 清除/兼容：取消选择或选择其它单位，标记消失；若已有伟人，顺便确认其原高亮仍正常，不要求额外造伟人。再选移民标记重现，原建城水源提示/移动正常。关闭Builder preview后选工人不再显示我们标记。

PASS：目标与当前状态一致；模式切换后旧标记清除，未遮挡单位操作、未干扰原提示。
异常：提供地图+Unit sites底部TargetStatus截图。unknown cities>0不表示没有目标，是对应城市未成功确认，Lua.log可显示TARGET_UNKNOWN城市ID/原因。若没有Lua.log，先回传截图，不反复重开局。
本批仅确认目标枚举与地图标签；正式地块限制、施工队单位、消费未启用。
