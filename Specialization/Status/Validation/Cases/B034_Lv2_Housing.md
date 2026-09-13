# B034：共同Lv2住房（三步，单城）

Document Owner: Codex
Build: P0-B-034 / modinfo42
State: USER_GAME_TEST_REQUIRED（需要用户游戏内验证，尚未通过）

## 准备

退出至主菜单后加载更新版本的现有测试存档，确认面板B034与`Read Lv2 housing`按钮。优先用现有Research城市：Potential1、学院完成、尚未建图书馆；若没有这样的城市，可以在当前局用Cheat新建一座，不要求重新开局。安排已拥有至少2个头衔、且没有自身住房加成的总督，等建立。此时Potential1所以ACTIVE仍1。

先不要投资或造建筑；记录城市住房面板的**住房总量H**（不是人口或剩余住房）。`Read Lv2 housing`应expected=+0、carrier=+0。若旧档报B034_DATABASE_MISSING或TIER_DATABASE_MISSING，停止并回传文字/截图，不反复点击；不能把旧档定义缺失当机制通过。

本轮按钮是只读，观察住房变化时先看城市UI，再读报告，避免混淆自动应用与按钮触发。无需抄城市ID。若现有城已建图书馆，报告中的额外量会相应增加；可回传现有建筑/数值，由Codex核对，不必为完全相同布置重开局。

## B034-1：投资打开住房

沿用已通过的Prepare/Confirm投资方式，移民使本城Potential1→2；总督保持原位与原等级，不改其它状态。

PASS：实际住房H→H+1（仅学院，无建筑）；Read progression显示Potential2/ACTIVE2，Read Lv2 housing为expected=+1、carrier=+1。再读一次住房不增加。

FAIL：没有+1、增加不止+1、重复读取累加、expected与carrier不一致、ERROR。若过一回合才更新，请说明，不能算即时通过。

## B034-2：建筑增加一层

在同城用Cheat完成图书馆；保留相同总督。当前本机HD图书馆自身Housing=0，因此住房应再增1。

PASS：住房H+1→H+2；报告expected=+2、carrier=+2、tiers=1。原Lv1专家支持保持。重复读数不累加。

FAIL：没有增加、增加超过预期、内部标记被计入建筑层级、读报告后才生效。若用了其它建筑，请说明名称，其自身住房可能不同。

## B034-3：读档与撤销

保持上一步状态保存并重新加载。先查看住房仍H+2，读报告expected/carrier均+2；不应需要点击按钮开启。

然后将总督调走，保持城市建筑不变。

PASS：Potential仍2，ACTIVE回1；住房回H；expected/carrier均+0，原Lv1专家3F3P仍保留。若总督自带住房或其它城市状态变动，则先回传原始数值，不能直接套H判据。

FAIL：加载丢效果/累加，调走保留Lv2住房，投资Potential丢失，或Lv1一起消失。仅回合后修复也请单独注明。

## 回传

人工说明三步是否PASS，附三个关键阶段报告即可（第一步开启、第二步建筑、第三步撤销）；住房基准/各阶段总数可口头提供，读档保持也可口头确认。不需要每次点击截图。

失败请保留：对应Read Lv2 housing报告、Read progression、城市住房明细，以及游戏Lua.log；数据库缺失/SQL错误再附Database.log与Modding.log。记录操作后立即还是过回合才更新。截图仍投递Specialization/ScreenShots，读取后按已批准规则归档。
