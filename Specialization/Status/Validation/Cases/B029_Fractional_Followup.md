# B029新局后续：半点与重复保持

Document Owner: Codex
Status: USER_GAME_TEST_REQUIRED

直接沿用刚通过的新局首都，保持B029，不改专家/建筑/政策、不结束回合。不要用先前无效的旧档。

1. 从OFF状态点Carrier +1 / +1.5两次（到configured=1.5），点Read source totals，记住delta；再点同一个Carrier按钮一次并重新读取。截图一次，文字说明重复前后是否一致。
2. Carrier OFF，重新读取，截图一次。

PASS：第一步三项delta=1.5且重复不增长；OFF后均为0。相同新局无其它变化时总值应为5科技、2.796875文化、7.5生产，OFF回到3.5/1.296875/6。若基础已变化，以探针当次baseline计算的delta为准，不手抄ID。

若只增1，说明半点未体现，不能静默取整；若出现其它倍率/截断先回传实际数字。FAIL：重复累加、OFF残留或UNKNOWN。面板Getter是本测试比较依据，原生UI可能尚未刷新；保留截图即可，不要求过回合强制刷新。结束务必OFF。此项不证明任意小数精度/商业IV全机制。
