> HISTORICAL NOTES / superseded：此文件保留当时证据与测试步骤；当前规则、通过范围和待测任务以 Specialization_v0.1_Architecture.md / Specialization_P0_Status.md 为准，不执行其中已过期的测试要求。

## 用户确认补录：头衔阈值与迁走撤销

用户明确说明此前已验证：Established title thresholds 2/3/4随总督升级正确显示1或nil；总督移走后显示0/0/0。不要求截图，不读取图片。

USER_GAME_TEST_PASS：本城头衔阈值随升级响应；总督移走后本城三项阈值全部撤销为0。nil与0都可作为未激活原始表现；仅值1视为本探针已激活，不把Lua truthiness用于判定（Lua中0为真）。不再安排同样的升级/原城阈值撤销测试。

合并已有结果：新局control加载、无总督、派遣后present、未建立/已建立的established，以及区域/专家读取均已用户确认通过。P0总督基础条件验证可作为下一阶段依据。当前未实现正式专业Active计算或网络效果；不将这些探针通过外推成整个v0.1通过。此消息未另外提供目的城市迁移途中Req门槛表现、旧存档新增Modifier回填或多人验证，保留这些边界，不阻止后续独立P0工作。

本轮仅更新状态与实现约定，无代码改动，无图片读取，无游戏操作。


以下测试安排为此前历史；与本补录重复的项目不再执行。

# A007新局用户结果：存在与建立条件通过

用户明确回报：新存档control=1、其他=nil；通过cheat panel获取一个总督头衔并派遣后present正确显示，established=nil；建立后established=1。

USER_GAME_TEST_PASS（限定子项）：新局无条件control加载、无总督初始值、派遣后存在条件、未建立时established未激活、建立后established激活。未要求截图才能记录，用户明确测试回报即为证据。获取头衔通过cheat panel，未据此推定任意免费晋升的计数语义。

旧存档control缺失而同版本新局正常，支持新增trait效果未回填旧存档的解释。记录为旧存档增量兼容问题，不归因原生总督条件失效；未经存档内部实例分析，不声称完全查明引擎装载原因。后续总督测试以这个A007新局存档为准，保留旧存档，不实现强制Attach或伪造control。

仍为USER_GAME_TEST_REQUIRED：在新局中核对1→2头衔门槛、迁移后的原城撤销及目标城建立前阻断、Req4；完整城市专业Active机制尚未实现。此前旧局Req2/3随升级响应证据保留，不外推全部语义。区域与专家读取通过状态保持。

下一小批仅两项，已有条件就做，不必再新建：
1. 当前已建立且仅任命的总督，Read governor记录control/present/established和Req2/3/4；给同一总督一个普通晋升后重新Read。预期control/present/established保持1，Req2从nil/0到1，Req3/4不激活。前后各截图。若作弊工具直接添加晋升而非仅提供可用头衔，请注明；优先用正常晋升按钮。
2. 若已有第二座己方城市，将该总督迁过去：读取原城，present/established/Req2/3/4应撤销为nil/0；读取目标城，到任途中present=1、established及Req2/3/4未激活；建立后established=1、Req2=1。两个城市control始终1。缺少第二城则暂不做，不为此重开局。

PASS按各子项记录；有错误或数值不符则截图并停止该项。截图仍使用ScreenshotInbox默认文件名。不需要重测存在/建立的基础过程或专家。本轮只更新文档，不修改运行代码/SQL、不启动游戏。
