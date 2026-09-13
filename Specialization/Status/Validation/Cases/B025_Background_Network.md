# B025：后台商路接入、分发与撤销

Document Owner: Codex
Build: P0-B-025 / modinfo32
Verification: USER_GAME_TEST_REQUIRED

本次没有新SQL定义，可沿用B024测试存档，先保存测试副本并回主菜单重新加载B025。全程无需打开贸易路线总览、BTS窗口或P0 Background routes按钮；建立路线所需的商人选择目的地操作照常允许。Read network (Game)只显示结果，不触发商路采样。

角色范围：当前有效DEV Lv1专业（已有Read city flow记录），不用升级Potential。准备科研城S、文化城C、商业专业城H、普通己方接收城D；D可用现有城市，不要求有专业。H必须是商业专业城市，不是只造了商业中心的其它专业城。用Cheat提供商人/容量。若只方便科研源，可先测S/H/D两条路线并明确回报仅Research；Culture组合不凭空判PASS。

## 1. 接入与分发

建立S→H、C→H、H→D三条有效国内商路（方向不能反）。选H，Read network (Game)：READY_BACKGROUND_UI、center=YES、connected应包含RESEARCH及CULTURE来源。选D，同按钮应显示Research/Culture的selectedReceives=YES。两张图即可，不再测试端点分页。N为全玩家去重接收城市数，有其它路线时不机械要求N=1；本案看D是否同时收到两类。

PASS：不打开贸易总览也能得到READY；H有两个直接来源，D经同一分发路线接收两类。面板只有网络诊断，不应增加实际城市收益或触发Boost。

若NO_BACKGROUND_BATCH、LOAD_NOT_READY、STALE_SIGNAL_OR_TURN、PARTIAL_BATCH、ENDPOINT或其它UNKNOWN，保留完整面板，不通过打开Background routes掩盖初始化问题。可给正常一个游戏更新机会后再读，不要求等许多回合。

## 2. 保存读档

保存、回主菜单、重载，不打开贸易总览；直接选D读取。应再次READY，Research/Culture接收保持，路线数量与之前相同。seq是传递序号，不是持久路线数，允许重置，不要求人工比ID。拍一张图。

## 3. 单个来源撤销

在测试副本中取消/结束C→H（若能方便完成）；如果Cheat无法删除商人，允许用删除文化源C城市的变体验证，务必注明“删城变体”，不据此宣称正常到期或掠夺已通过。保留S→H与H→D，且确保C是H唯一Culture来源、D没有其它Culture接收依据。

选D读取：Research仍YES、Culture变NO；READY显示当前重建结果，不能永远留在旧YES。拍一张图。若只是瞬时UNKNOWN，可再读一次；若持续UNKNOWN，回传完整错误。不要对正式游玩存档执行删城。

失败回传：完整Read network面板、具体步骤、来源/中心/接收城名称；Lua.log如有、Database.log仅数据库错误时。截图按顺序投递ScreenShots即可。首批约4张图，不重发B010，也不重测已通过的商路端点/分页。

未包含：正常到期、掠夺、多人/AI覆盖、超过128条路线、等级升级、正式Network Strength/收益。这里只验证新的后台→Gameplay链路与Lv1诊断拓扑。
