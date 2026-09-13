# B030：一组精度/激活区分测试

Document Owner: Codex
State: USER_GAME_TEST_REQUIRED

目的：不是重测B029的0.5；把第二槽改成含整数部分的1.5，以区分槽位激活和小数丢失。

1. 安装当前版本后新建Scotland (Specialization Test)测试局，建首都并选中；面板应为P0-B-030。无需区域、专家或商路。旧档不作为本案证据，因为其Modifier实例可能保留旧值。
2. 同一回合点击Carrier OFF，然后Carrier +1 / +2.5一次，再Read source totals。应configured=1，S/C/P delta均1。截图①。若不是1即停止加档，OFF并回传。
3. 再点击Carrier +1 / +2.5一次，再Read source totals，应configured=2.5。截图②。不要过回合或改变人口、政策、建筑等状态。
4. 点击Carrier OFF，再Read source totals；应configured=0、三项delta=0。正常只需口头确认恢复；异常则截图③。无需重复点击或存读档重测。

第二步（累计2.5档）结果判据：delta三项2.5=本场景小数PASS；2=第二槽生效但小数FAIL；1=第二槽无可观察增益，原因待查；其它或不一致=待诊断。OFF delta0=撤销PASS，否则FAIL。configured仅配置，不是实测。

回传两张截图及OFF是否归零即可。异常保留存档；若有ERROR截全错误文字，保留该次Database.log/Modding.log/Lua.log（若生成），不要求寻找不存在的日志。无需手抄城市ID或计算总数。截图投递ScreenShots，Codex复核后归档。
