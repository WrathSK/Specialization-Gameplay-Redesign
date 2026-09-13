# B042：真实施工队与共同单位动作（三小案）
Document Owner: Codex
State: USER_GAME_TEST_REQUIRED
Build: B042 / modinfo55

先回主菜单加载现有测试存档，确认Unit actions / sites窗口标题B042。本次新增单位SQL/美术；先沿用旧档。若明确显示CREW_DEFINITION_MISSING，才用测试文明新局，不先要求重开。
不需要开启工人测试模式，真正Crew自动显示BUILD目标。固定只有250档，DEV免费生成，不代表五档正式项目已完成。不会把普通工人转为Crew。

1. 生成/外观/移动：选一座己方城（市中心不要站移民/工人等平民），点Unit actions / sites打开窗口，再点Spawn Crew 250 (DEV free)。应生成“施工队250（测试）”，可见工人模型/图标，1劳动力，可正常移动。选它，不站当前建设目标时点Prepare，应拒绝且不消耗。普通工人不能使用新施工动作。若模型或1charge异常，先记录，不反复生成。
2. 真实施工：将Crew移动到一个当前合法建筑/区域/奇观地块，Prepare显示apply/waste，再Confirm；单位消失，当前目标只增加min(250,剩余)。优先用剩余不足250、下一项0的目标，一次兼验浪费且下一项0。无需重做三类注入。再点Confirm不得追加。正常保存读档后成果保持、不重新发放；可与第三案合并一次读档。
3. 移民新入口：选一座Potential<4的专业城，移民站其专业区域而非市中心，通过同一Prepare / Confirm unit action。应消耗一个移民、Potential+1，Identity不变，现有ACTIVE门控保持。可在移动到区域前先点Prepare观察拒绝。无需重测所有等级；旧P0市中心投资入口仍保留，不用于本案。

报告出现HELD / RESULT UNCERTAIN停止重试，回传报告和Lua.log（如果有）。此时可能已消耗单位但收益未确认；不要用再次点击猜测结果。
截图只需异常；正常可口述单位外观、劳动力、注入前后、投资+1及保存读档。新美术报错附Modding.log/Database.log及可用Lua.log。
