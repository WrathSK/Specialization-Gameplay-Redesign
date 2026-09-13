# B043：原单位面板操作与友好拒绝提示
Document Owner: Codex
Build: B043 / modinfo56
Architecture: A0097
Status: S0101
Design: D0011 synced with implementation limitations

新UI Context将自有ActionGroup通过ChangeParent挂到/InGame/UnitPanel/StandardActionsStack，不替换原版/HD文件或原生按钮。HD UI/Custom/CityButton_ResourceClassification.lua:65–72有跨Context ChangeParent到原城市按钮栈先例；原UnitPanel.xml的StandardActionsStack及UnitPanel.lua图标设置提供静态证据。
移民用ICON_UNITOPERATION_FOUND_CITY，施工队用ICON_UNITOPERATION_BUILD_IMPROVEMENT。各有中文用途提示，明确投资不建城、施工消耗单位/丢弃超额。准备后显示第二个同图标“确认”按钮；后端公开只读preview元数据，confirm附PlanToken并核对，移动/过回合隐藏旧确认，真正效果仍Gameplay重新验证。其它单位隐藏自有组，不改其按钮。
诊断窗口旧prepare/confirm隐藏但保留代码，DEV spawn/读取保留。执行结果保留在诊断窗口，可用于单位消失后查看；普通拒绝UI显示中文+稳定reason，完整Lua路径只写日志。用户截图正常MOVE_TO_LEGAL_TARGET，不是异常执行。
引擎未知错误保留HELD停止提示，不翻译成成功或普通拒绝。地图/投资/生产力机制不改。

本地test_unit_panel_actions.py通过实际UI挂接mock、两种图标、prepare/confirm元数据、其它单位隐藏及原Crew/投资回归。live DB已有Crew定义，旧测试插入会重复；本次内存fixture存在则只校验既有行，不改live数据库。Lua/XML/manifest56校验通过；真实面板布局与加载路径尚需实机。
新原面板入口若未找到，诊断显示UNIT_PANEL_STACK_NOT_FOUND，不偷偷把按钮留在原独立窗口算作完成。

D0011：按用户明确答复登记五档工业Lv1全开放、双侧速度缩放；冻存D0010并记录新hash。当前只有250DEV单位，五项目尚未实现。HD已有CityProjectCompleted回调先例，下一步按已确定规则接项目完成生成；游戏速度乘数与整数成本/转移精度必须同时验证，不能擅自只缩放成本。
备份DevelopmentBackups/Specialization-before-B043-unit-panel。UUID/配置未改，未启动游戏。
