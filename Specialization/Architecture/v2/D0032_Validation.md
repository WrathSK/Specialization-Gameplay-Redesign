# D0032 Architecture Adaptation — 文档验证

Document Owner: Codex
Date: 2026-09-18
Architecture: A0160 / Status S0201
Evidence: STATIC_CONFIRMED only; no new runtime simulation or game test
Source baseline: `65170105c289bfcfc098ed3276cef795c6399a77`

## 本轮检查

- 全部121个Mod文件登记SHA256、manifest角色、源码函数/桥接/写入线索；索引的每条line/text逐项对照真实文件通过。矩阵按混合职责分类，不以Probe文件名判断只读，不把ImportFiles当启动。
- 当前Design目录57个文件（含本地Finder metadata）逐字节与开工前一致；所有Design JSON语法通过。发布的authority hash索引排除`.DS_Store`，保留56项项目文档。D0032没有修订，历史authority没有改写。
- 新Markdown相对文件链接通过；`git diff --check`通过；改动仅Architecture与Status。
- 重点人工合同核对：Research RES-005保留但新Network deferred；Industry模板union与建设/购买独立max；Culture每个source自身3/3后union、城市Dialogue与原Owner见闻分离；Commerce source-city pity、签约后断路不撤销旧合同；ordinary D与Housing tier-presence分离；REALLOCATING不等于NONE。
- 每个旧主动收益族都有计划退出批次；清理范围包含Buildings、trait条件、HD Property、项目原生授予和隐藏实验入口。没有执行任何清理。
- 技术spike逐项区分primitive静态证据和结算/时序待测；DebugGameplay当前没有SPC Buildings，不据此声称载体加载或实机通过。
- 本轮没有运行Gameplay回归或新事件模拟：源码未变，不重报A–D2历史LOCAL_SIMULATION_PASS为新Design PASS。未来P0-A及各批的本地/最小实机门禁已经列出。

## 隔离与hash

- develop Mod：121文件完全未变。排序文件hash字典摘要：`7894516cd4647c824e77580ac4eb1d46f8593ebe0fd0ff62501c447ecad206ca`。
- live：121文件与开工前相同，且与develop Mod逐文件相同；仍B076.103/modinfo103。未部署、未启动游戏、未改配置/其它Mod。
- main HEAD：`e3651f9b7c90110f3a8890a7b12ca299996b306b`，工作树clean；没有修改main。
- DevelopmentTests、tools及Design没有本批修改；新源码索引是文档证据，不是runtime或自动部署配置。
- Git发布：本地文件检查后只提交本批文档到develop，正常push origin/develop，最后核对HEAD与clean。最终commit/push结果由交付报告及Git历史给出，不在提交前伪造commit hash。

## Gate

**GATE B — READY FOR P0-A / None blocking P0-A.** 仅代表规划具备第一批实施条件，不是实施授权、不代表全部未来功能技术可行性已验证，也不关闭55GB内存事件的独立长期证据要求。
