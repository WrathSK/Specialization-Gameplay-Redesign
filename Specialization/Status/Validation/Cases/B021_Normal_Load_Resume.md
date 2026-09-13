# B021：正常读档后继续完成学院

Document Owner: Codex
Build: B021/modinfo28
Verification: USER_GAME_TEST_REQUIRED

一组测试，三张关键截图。使用现有测试文明局：优先用已经拥有B020记录但还没有完成首个专业区域的存档；若没有，则在B021加载后新建一城。已经RESEARCH/1的城市不能验证“读档后第一次锁定”。不要清空任何Property。

1. 选测试城，放置学院但不完成，点Read city flow (B021)。应DONE、rev3、NONE/0、stopped=false。正常保存、退出主菜单重载。
2. 选同城并Read：应RESUMED_NORMAL、DONE、rev3、NONE/0、本次加载写入0、stopped=false。截图1。
3. 用Cheat Panel“完成当前城市项目”完成学院，Read：应RESUMED_NORMAL、DONE、rev6、RESEARCH/1、本次加载写入3、stopped=false。再点Read应不变。截图2。
4. 再次保存退出重载并Read：应RESUMED_NORMAL、DONE、rev6、RESEARCH/1、写入0、stopped=false。截图3。

PASS：恢复本身不写永久记录；读档后的首次完成只提交一次；第二次读档保持。FAIL：LOAD_HELD、stopped=true、错误/无响应、数据丢失或数量不同；先停并回传截图和最后操作，保留Lua.log的[SPC][B021]和[B015][JOURNAL]相关内容。无需做丢写、毁城等故障实验。

默认截图名投递Specialization/ScreenShots即可。B020已有完成记录也支持普通重载，但不代替本批未专业化城测试。本批没有正式产出变化。
