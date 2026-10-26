# B391.418 — 用户批准的 develop 阶段测试部署

日期：2026-10-25；记录 S0847。用户明确授权部署并要求新档刻意触发场景清单。本次临时切换到当前已提交 develop；不是最终 U5，也没有 main 晋升。

- 部署源码：`b0be389631c35291b545238f3e252ae32c76bda4`，B391.418 / modinfo418。
- 运行包：`DEVELOP_ACTIVE`，340/340 文件与源码 SHA256 一致；总摘要 `983881621f35f399c3181122220799a6ea207bdd8cd44d533490b96e7bdaeed2`。
- 恢复点：B307.334 稳定包312/312与 main 的 Mod 摘要一致。main HEAD仍为`bc49dab5739e7819ceaf49228de7d47310c296d8`。
- 事务凭据：外部部署归档目录中的`B391.418-b0be389-playtest.json`；完整稳定备份位置和双向校验值在凭据内。无未完成事务。未启动游戏。
- 安全检查：提升权限的只读进程检查确认无`Civ6.app/Contents`游戏进程；两个工作树部署前干净；使用原有 temporary_playtest.py 的 check-only→activate 事务，没有绕过 main 专用部署门禁。稳定备份保留在 Mods 扫描范围外；恢复仍须用户批准并退出游戏。

## 证据与实际范围

`STATIC_CONFIRMED`：217份 Lua5.1重新编译、25份 XML重新解析、339项 modinfo 引用与实际资源集合完全相符，共340运行文件。部署前 Context/Runtime 校验通过。

`LOCAL_SIMULATION_PASS`：既有[S9g4结果](Specialization_B391_Refactor_S9g4.md)的75/75工件哈希与当前源码输入重新核对一致；没有宣称本次重跑75项。切换工具回归本次重新执行，授权、摘要、完整恢复（含 develop 独有文件退出）和失败回滚通过。命令：`PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_temporary_playtest.py`。

`USER_GAME_TEST_REQUIRED`：[阶段测试清单](Specialization_B391_Develop_Playtest_Checklist.md)。Cheat Panel机制检查与自然原生事件、跨回合及读档证据分别记录；没有实机 PASS。

## 尚未完成的范围

- S9仍在进行，S10尚未完成。NetworkRecovery Model/Cell/Store仍为无自动生产消费者的库；商业/文化网络的冷加载逐来源恢复尚未接入，不能把本次测试当作该问题已修复的验收。
- D7永久不可恢复判据/合法基线、实际已应用值/UI组合、U4闭包及最终扫描工作量比较仍需后续完成。
- 同级施工队多城同回合完成的唯一原生归属凭据仍开放；日常逐项测试先错开，不把它列为已支持的通过项。
- S10旧探针职责迁移/退出未完成，包括HalfYieldProbe；本次帧耗时和堆增长只能作为中间版本观测，不是重构最终性能结论。B271 A/B/C时序探针继续禁用，未重新启用。

User decision：本次一次临时部署已执行；后续部署、恢复和main晋升仍分别按授权执行。

User testing：使用B391新档执行清单，投递日志/必要截图；最终U5在剩余重构完成后安排。

Primary next：本批次边界等待用户阶段测试证据；保留已授权S9→S10的后续范围，不以本次部署宣告完成。
