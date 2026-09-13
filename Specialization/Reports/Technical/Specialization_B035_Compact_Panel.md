# B035测试准备与P0面板精简

Document Owner: Codex
Runtime: P0-B-036 / modinfo45（仅UI更新）

保留9个按钮：Read Lv2 GPP / Read progression / Read auto Lv1；Read Lv2 housing / Read governor / Read specialists；Prepare investment / Confirm investment / Read network (Game)。Open/Close保留。

旧按钮XML定义移入Hidden=1的LegacyProbeButtons容器，Lua回调、引擎请求与探针模块全部保留，后台机制不依赖可见按钮。之后需要时将指定控件移回Window并分配布局；不要直接显示整个历史容器，否则旧坐标会与当前布局重叠。完整改前文件另有DevelopmentBackups/Specialization-before-B035-compact-panel。

外框仍840×664；正文起点y62，第一行按钮顶y526，给正文464px垂直空间（实际字形边界仍待游戏渲染）。三行位于底部106/62/18。标题从P.VERSION生成，消除原B035静态标题错配。英文控件标签沿用既有兼容方案。

STATIC_CONFIRMED：XML ID唯一、9按钮可见且不越界、旧按钮在隐藏容器中、manifest45。LOCAL_SIMULATION_PASS：实际P0Panel.lua初始化，所有可见及隐藏控件回调成功绑定，动态标题正确。均不等于游戏内视觉通过；视觉可随B035一次确认，无另开测试。

GPP/住房/投资/工业/网络Gameplay与SQL未修改。Accepted D0010未修改。未启动游戏。

当前批次为B035_Four_Family_GPP.md：四类0→1，一城人数/撤销/重载，文化25%倍率。B035仍USER_GAME_TEST_REQUIRED；B036既有结果保留。
