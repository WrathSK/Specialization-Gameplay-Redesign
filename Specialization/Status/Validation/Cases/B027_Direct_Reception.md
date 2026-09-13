# B027：D0009直接接收（一个测试）

Document Owner: Codex
Status: USER_GAME_TEST_REQUIRED（用户实际游戏验证前不能记PASS）

使用上一批最后的存档，不需要新局或建城。退出到主菜单后载入，确认面板P0-B-027，不打开贸易总览。

前置路线保持：科研首都→纽约、文化城→纽约、纽约→阿伯丁；若存档不是这组路线，请说明实际路线，不要照用下面N。

选纽约，点击Read network (Game)，截图一次。预期connected仍有科研与文化；RESEARCH N=3、CULTURE N=2，纽约两项selectedReceives均YES。相对于B026，新增的是首都的科研recipient和纽约的文化recipient；不是增加source或商路。

PASS：上述两类N/纽约接收均符合，且READY_BACKGROUND_UI。FAIL：仍为旧N=2/1、纽约文化NO，或报UNKNOWN/ERROR。失败只回传整张面板截图，保留当前存档；无需重复起终点分页、拆路线或开新局。商路不同则先核对拓扑，不据此判实现失败。

本测试不覆盖Commerce IV产出、断路撤销或高级ACTIVE；旧批次仍延后。
