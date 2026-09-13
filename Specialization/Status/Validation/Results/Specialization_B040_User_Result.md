# B040：用户通过及单图复核
Document Owner: Codex
State: USER_GAME_TEST_PASS
Build: B040 / modinfo52

用户明确“行为都正常”，作为原三案人工通过记录；没有把所有案子写成截图验证。
唯一截图：B040.52，UNIT_BUILDER #2031630，plot1909 (59,25)，city LOC_CITY_NAME_WASHINGTON #262147。
Investment candidate: SETTLER_REQUIRED | RESEARCH P1 target=(59,25)。
Construction candidate: NOT VERIFIED AT THIS PLOT | BUILDING_STONEHENGE。
用户说明工人不在当前奇观地基上，故此结果为正常拒绝，不是接口异常；工人不能投资同样正常。
NOT VERIFIED同时涵盖“不是目标地基”和“缺少可核对的HD地基记录”，不能根据此提示独自区分二者。本图借用户场景说明确认前者；不据此宣称系统已能从错位处定位奇观目标。
入口显示修正、其它位置案按用户口头通过关闭，无需重测。截图原名移动至Evidence/B040并核对SHA256。
真实Crew、劳动力、单位消费、高亮均尚未通过此批验证。
