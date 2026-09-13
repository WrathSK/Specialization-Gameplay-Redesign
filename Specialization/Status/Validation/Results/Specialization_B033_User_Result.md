# B033 实际移民投资：三图与用户补充

Document Owner: Codex
Build: P0-B-033 / modinfo41
Evidence: ../Evidence/B033/manifest.json
Status: USER_GAME_TEST_PASS（下列观察范围）

## 截图

三张均RESEARCH、city65536。

| 时间 | 阶段 | 观察 |
|---|---|---|
| 09:15:23 | PREPARED，回合1 | Potential1→2预览，Settler589832；选中移民仍显示，尚未消耗 |
| 09:15:46 | INVESTED，回合1 | consumed1Settler；Potential2、ACTIVE1、KNOWN；investments1、pending=false、Ledger PRESENT |
| 09:19:44 | 重新读取，回合3 | Potential2、ACTIVE2、KNOWN；investments1、pending=false、Ledger PRESENT；专业RESEARCH保持 |

第三图为用户指定存读档后步骤；退出/加载过程本身依人工回报，不由截图时钟单独推断。ACTIVE2与第二图的1不同，结合用户另外操作总督的说明属合理变化，并非存档不一致。不能将本批扩展为Potential3/4投资上限实机通过。

## 用户明确口头证据

- 确认仅消耗一名移民，重复确认不重复升级或消耗，保存重载保持；原Lv1检查通过。
- 原城市没有既有商路，因此未测升级前后保留原商路身份。该项继续未验证，不列FAIL。
- 升级后新建立商路，网络身份正确：限定新路线接入，非原路线连续性证明。
- 任命/建立/升级/调离总督时ACTIVE能正确变化；1级总督仍ACTIVE1。总督精确各阶段截图未提供，按用户手动观察登记，不编造3/4级测试矩阵。支持Potential2场景动态门控，并非高级收益已生效。

三图同时确认Network details / Next及Read network (Game)两处英文标签显示正常，B031标签修复可在该语言/环境登记USER_GAME_TEST_PASS；不证明其它语言字体。

## 结论与后续

正常移民投资1→2、原生删除后确认、正常存读档和重复保护按观察范围USER_GAME_TEST_PASS。回调失败/单位ID重用/征服/跨owner/中断恢复只保留既有本地或未验证边界；网络旧路线保留未测，不因用户总体pass合并。没有发现本轮阻塞，无需补拍现有已过步骤。下一项适合共同Lv2住房/GPP实施研究，保持小数/Commerce IV后置。本轮仅登记结果及原图归档，运行/Design/Tests未改。
