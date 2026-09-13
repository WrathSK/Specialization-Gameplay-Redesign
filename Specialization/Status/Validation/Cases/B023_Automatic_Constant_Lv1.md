# B023：常数型Lv1自动应用

Document Owner: Codex
Build: P0-B-023 / modinfo30
Verification: USER_GAME_TEST_REQUIRED

## 准备

本次新增Culture/Commerce建筑定义，建议新建Scotland (Specialization Test)测试局，保持HD和Cheat Panel。可用有完整B023数据库定义的旧局；若面板出现B023_DATABASE_MISSING才需新局，不清理Property。用Cheat准备三座城市，分别让第一个完成专业区域为普通学院、剧院广场、商业中心；完成提供专家岗位的建筑，分别安排1名对应专家。无需总督，不需要升级Potential。

保留的Read city flow用于检查记录；若首都UNTRACKED，另外建城，不把旧城现有区域当首次完成。没有ON/OFF按钮，Read auto Lv1只读，不能触发添加收益。

## 三个最小案例

1. Research：新城完成普通学院后，不打开P0面板也应自动应用。安排专家，先观察原生岗位提示应有3食物/3生产力，再Read auto Lv1：expected=RESEARCH、carrier=RESEARCH、workers=1。无需先点Read来启用。拍岗位图，面板结果可文字回报。
2. Culture与Commerce：另两城分别完成剧院广场、商业中心及岗位建筑，各安排1名专家。原生岗位应额外3食物/3生产力，原有文化/金币保留。Read显示各自expected与唯一同名carrier；不应获得其它专业carrier。各拍一图。此案是同一种自动机制的两个数据映射，不要求重复完整开关实验。
3. 保存上述局、回主菜单、读档。不点任何启用操作，查看各城岗位仍有加成；选一城Read auto Lv1并截图，changes this load=0（同次加载所有城市汇总，无其它城市新专业化/载体补齐时）。重复Read不改变数字。

约4张截图即可，按时间投递ScreenShots；其余检查可文字确认。PASS：自动且仅匹配专业生效、原生实际岗位有加成、读取不负责启用、重载不重复添加。FAIL：必须读面板才生效、错专业/重复产出、零专家固定补贴、读档丢失或ERROR。失败保留完整面板与岗位提示，说明区域类型/完成手段/出错步骤，附Lua.log、Database.log；不依赖剪贴板。

范围：本批仅标准三类区域、当前有效DEV记录的测试文明。替代区域、全体enabled资格、征服继承、高级等级和Industry不是本次验收；仍是逐步开发，非完整v0.1。网络没有启用，B010继续延后。
