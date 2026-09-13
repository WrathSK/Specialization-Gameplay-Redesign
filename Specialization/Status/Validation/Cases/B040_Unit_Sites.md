# B040：单位入口与地块读取（三个小案）
Document Owner: Codex
State: USER_GAME_TEST_REQUIRED
Build: B040 / modinfo51

沿用现有存档，回主菜单重新加载，P0顶部版本B040。不要求新局、不需要新施工队。
选中己方移民/工人，屏幕右上P0按钮下出现 Unit sites (read only)。不必打开P0面板。点击显示独立报告；移动/改选单位后旧报告会关闭，重新点击读取。读数均不消耗单位、不加生产力、不投资。

1. 移民：选Potential<4的已有专业城市，把移民移到其已完成专业区域上，点击读取，Investment candidate应为SITE OK；移至相邻同城己方普通地块再读，应为MOVE_TO_TARGET_PLOT。若该城队列不合法，Construction行无目标是正常的；只看Investment行。
2. 工人：选当前正在建一个普通区域建筑的城市，将工人放到该建筑所属区域上，Construction candidate应SITE OK (location only)。改用一个在建区域地基再读，也应SITE OK。工人Investment行SETTLER_REQUIRED正常；无需实际施工或重复B039注入测试。
3. 奇观：在当前正在建造的奇观地基上放工人并读取，Construction candidate应SITE OK；将队列改成其它目标（不完成奇观）再读，不能把旧奇观当有效当前施工点。若报告NOT VERIFIED，请保存报告；可能是HD未建成奇观位置记录缺失，不能当作已通过。

PASS：按钮随工人/移民出现，正确识别各自位置与当前目标，离开后拒绝；生产和单位都未被改变。不同动作行分别判断，不要求每张报告两行同时OK。
正常口述即可，异常提供对应报告截图和当前目标/单位所在格；ERROR或10秒无响应附Lua.log。不点击旧P0的Inject或投资按钮执行这些位置测试。
这不是新地块规则正式生效，也不是施工队单位生成/消费测试。
