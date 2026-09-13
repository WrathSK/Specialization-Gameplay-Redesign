# B021：正常保存路径恢复处理

Document Owner: Codex
Architecture Revision: A0048
Build: B021/modinfo28
Verification: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED

## 用户授权与支持范围

用户已明确当前以Cheat Panel机制测试为主，极端错误边界不作为所有机制前置，但保留必要保护。本轮据此实现正常保存恢复，不以不可证明的“任意丢写后恢复”阻塞正常路径。没有修改Design或声称解决此前反例。

沿用SPC_DEV_CITY_FLOW_B020键与记录格式，兼容已保存的B020数据。LoadScreenClose后：有记录且绑定/owner/坐标正确、stage为DONE、B015健康未halted并与facts整表一致、监听器就绪，才在内存恢复active。未专业化城额外检查市中心完整、区域枚举成功且无已完成专业区域；放置未完成允许。该扫描只排除可见冲突，不证明所有历史。恢复不写Property，不从缺记录旧城创建专业事实。

界面模式RESUMED_NORMAL。已锁专业后后续完成不覆盖；未专业化城市读档后可接收首个真实完成并三阶段提交。PENDING、GAP、不一致、已完成区域与NONE冲突、绑定错误仍暂停玩家B021处理，已经临时恢复的token撤销。无盲重试或覆盖修复。完整丢写后两表恰好相同且历史痕迹消失的旧反例依然在支持范围外，不能称为USER_GAME_TEST_PASS。

## 验证

test_city_flow_resume执行实际B013/B015/hook/B021：放置未完成→加载恢复→首次完成→重复/再次加载，缺记录不采纳，PENDING/两表冲突/GAP/扫描或绑定异常拒绝。另四组原生回调/桥接回归，共五脚本exit0；运行Lua编译及XML/manifest引用/UUID通过。LOCAL_SIMULATION_PASS仅本地模拟。

B020原test_city_flow_probe及test_load_history_ambiguity包含旧LOAD_READ_ONLY预期，冻结保留历史范围，本轮不把它们称为现版本通过的回归；B021由新测试覆盖恢复规则，旧极端反例未被修复。无新增实机结论，[一组用户测试](../../Status/Validation/Cases/B021_Normal_Load_Resume.md)待回报。

## 文件与后续

修改CityFlowProbe.lua、Probe版本、面板文字与modinfo版本；新增测试/报告/案例。B015与B013、Design、SQL、其它已有Tests不变。备份/结果DevelopmentBackups/Specialization-before-B021。未启动游戏。

下一项接入可通过专家人数变化直接核对的Lv1真实收益，不再追加多轮极端恢复模型。通用资格/征服等完整产品边界保持待办；本批为测试文明DEV路径，不代表正式系统全部完成。
