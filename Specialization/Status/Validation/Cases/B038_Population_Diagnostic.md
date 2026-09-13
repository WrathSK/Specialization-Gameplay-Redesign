# B038 科研最小诊断（modinfo49）

Document Owner: Codex
State: USER_GAME_TEST_REQUIRED

只用原科研城、原存档，回主菜单重载modinfo49。保持Population4、ACTIVE3、政策/建筑不变。文化暂不测，商业不重测。

1. 调出全部专家，点Read auto Lv1，截报告。新增段会显示live workers、expected、carrier、last audit workers和native city total。若workers0但carrier非0，到此即可先回传，不必做后面步骤。
2. 若零专家时expected=carrier=0，解锁一个其它岗位让系统自动安排1名专家，不点专家锁，读报告截图。
3. 点专家锁定，确认仍1名，再读报告截图。无需多次重复锁/解锁或测试更多组合。

最多三张报告，不用手算18.1。需明确前后是否换了有科技产出的地块、人口或倍率变化。若城市UI与报告native total不同，口述UI值即可。

分流判据：workers与last audit不符、expected与carrier不符→应用/触发问题；二者一致但城市增量不对→继续查原生作用与基准构成；不能只凭carrier相等判收益PASS。若零专家仍有2载体可额外口述过回合是否撤销，但不要求为此扩展测试。GPP不在本批。
