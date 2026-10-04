# Specialization agent map

遵守[根AGENTS](../AGENTS.md)。用户是最终语义权威；Design写入与决策边界统一见[W0005](Workflow/README.md#w0005--authority-and-repository-knowledge)，任务读取与验证见W0001/W0004。一个活动写入任务；不要覆盖其它未审查修改。

## 读取与证据

- [项目导航](README.md)定位Design、Architecture、Status与Validation；当前任务以Status CURRENT块及Authority指向的manifest为准。只读相关合同，不从旧DEV注释/历史报告推断当前完成度。
- D/A修订、accepted hash及sync按现有流程维护；sync不等于已实现或实机通过。Historical、既有Backups、冻结结果不就地改写；纠正使用新记录并由Status引用。
- 用户审核计划后才实施；玩法歧义用`DESIGN_DECISION_REQUIRED`，不因API限制或实现便利静默换规则。README/AGENTS/路径规则变更须用户授权。

## 用户交付与诊断

使用独立、简明的中文用户摘要，说明结果、游戏影响、阻塞及下一步；技术细节按需提供。技术限制若要求改Design，解释原因和替代方案的玩法差异，交用户决定。

证据首次出现时说明：STATIC_CONFIRMED=代码/数据库证据；LOCAL_SIMULATION_PASS=本地模拟；USER_GAME_TEST_PASS/FAIL=用户实机已测场景；USER_GAME_TEST_REQUIRED=待实机；BLOCKED=需技术突破或用户决定。不扩大未测范围，不把外部建议当验收。

最终交付明确“用户需要决定”“用户需要测试”“Codex下一步”；无则写无，到批次边界停止。

日常验收／使用报告优先让用户直接判断：先以简明中文显示本次对象与结果、必要的预期／实际对照、需处理的异常和下一动作，省略无关模块信息、重复警告及原始ID／reference／nil清单。原生接口未定、残留或归属冲突等排障需要时，保留完整技术报告，按当前问题选择简报、明细或简报后附明细；不禁止复杂报告，也不要求每份报告都展开。保留UNKNOWN、残留效果、实验污染等重要信息，区分预期值、载体配置、原生实测；不能为简洁隐藏失败或扩大PASS。若可读报告已足够支持用户判断，不默认要求截图；确需原生证据时仍可使用截图。后续涉及报告的修改沿用此原则，不另开全局UI重构。面板无需固定9按钮，约15以内一般可接受；隐藏暂不用入口并保留可复用代码，优先报告阅读空间，不据此扩张UI范围。

## 截图归档（持续授权）

当前develop根目录`ScreenShots/`为截图投递入口，整目录由Git忽略，保持默认文件名；旧外部工作区收件箱已迁出。逐张读取、批次明确后移动原图至develop根目录`local/legacy-workspace/Specialization/Status/Validation/Evidence/<Batch>/`，核对移动前后SHA256并记录manifest/结果关联。收件箱目录不移动，不留重复副本；同名冲突不覆盖，未读/不明文件留下。归档原件冻结，不擅自删除或压缩；无需逐次请求归档授权。

## 保留的技术与测试约束

- 开发机制可以Cheat Panel验证；正常操作、保存读档与真实收益优先。身份冲突停止、重复不发放、不覆盖成果、不凭空补历史仍是必要保护。自然/Cheat、同回合/跨回合证据分开；极端组合可登记支持边界，不强迫每次先解决全部组合，也不扩大PASS或改变Design。
- [后台商路来源决定](Reports/Technical/Specialization_Network_Background_Source_Decision.md)已接受无需玩家打开窗口的BTS/原版UI当前路线读取；不要重新以“必须纯Gameplay全集”阻塞。仍需验证本Mod桥接的初始化、重载、撤销与重建；来源许可不是实机PASS。
- 截图与旧证据按[历史路径映射](Reports/Proposals/Legacy_Workspace_Relocation.md)定位；DB、日志及备份保持原位，外部路径按实际配置解析，不假定它们已打包进仓库。
