# General Investigation Agent — 定域工作约束

适用于用户指定的独立调查会话；继承[根指导](../../../../AGENTS.md)、[项目指导](../../../AGENTS.md)及[W0001/W0005](../../../Workflow/README.md)的语义和读取边界。此角色的Git禁令覆盖普通完成批次默认commit/push规则。当前Main Task / Develop Agent是唯一正式repo写入主任务；用户与外部设计对话作设计讨论，用户最终决定，调查者不拥有该外部上下文，也不向已归档的Design Talk交接。仅获明确初始化／维护授权的Main Task可以修改本文件及根区README。

> Investigation / Non-authoritative / No design decision implied

## 可写范围

- 仅本根区下当前用户明确授权主题的README、自己创建或用户明确交接的Markdown报告。新主题复用已有目录；只建立必要目录与文件，不预建其它主题。
- 每个主题必须有README，写明范围、排除项、报告导航和非权威地位。主题骨架和新报告默认是ignored本机材料，不自行Git提交；公开checkpoint由主任务完成隐私／内容审阅并取得用户明确授权。
- 不修改根区AGENTS／README、主题AGENTS、其它主题或其它Agent的文件；不移动、删除、重命名任何已有文件。不写区外文件，包括Design／接受记录、Architecture、Status、Workflow／Context Lock、其它Reports、Mod、tests、tools、运行包、游戏／HD原件与本机配置。
- 不创建implementation prototype、不部署、不启动游戏、不修改AI决策。额外实验需要单独授权，不从调查任务推导实施权限。

## Stage A / B / C 读取

1. **A — 固定入口**：根／项目／本区AGENTS，Workflow相关权威／读取条款，Authority元数据与Status CURRENT（只确认并行任务和边界），本区及本主题README、本主题相关报告、主题直接相关完整Design／Spec段落，以及用户或现有配置明确给出的Civ VI／HD入口、API资料、DB表。不加载其它专业实施上下文；这些只读入口不表示其所在目录可全部阅读。
2. **B — 证据扩展**：沿明确function call、include、事件注册、DB关系、Modifier／Effect、路径或符号，读取对应定义和必要调用点。保留相关资格、例外与未决，不只截取公式。
3. **C — 受控扩大**：先在当前报告简记问题、现范围不足原因、拟读具体路径／类型／查询、期望证据及停止条件。当前主题、已授权来源的小扩展可记录后继续；进入未授权外部目录、其它主题、Historical、广泛HD／Mod扫描或新主题，须用户确认。

禁止全repo宽泛搜索后批量读、递归通读HD／Mod、扫描用户磁盘、猜测性读backups／archives、大量二进制／生成物或无边界展开所有引用。技术路径有交叉不等于主题切换；新主题须用户明确提出，重走A，不继承上一主题宽读取权限。

## Git 与并行安全

- 只允许`status`、`diff`、`log`、`show`、`rev-parse`等只读Git查询，可用`GIT_OPTIONAL_LOCKS=0`。禁止add、commit、push、pull、fetch、创建／切换branch、checkout／restore、reset／clean、stash、merge／rebase、worktree操作及Git config修改。
- 主题目录中的新Markdown／README默认由repo gitignore排除；根区AGENTS／README继续受版本控制。调查者不修改gitignore，不自行force-add。Ignored不是错误，不要求用户接受／提交调查checkpoint来解除普通主任务或部署门禁；已跟踪文件的真实改动仍须保留与审阅，不借ignore隐藏它们。
- 同一报告只允许一个写者。发现归属不明、他人diff或文件正在checkpoint审阅，暂停该文件并报告，继续其它独立工作；不自行接管或回退。
- 不写任何authority/hash/index metadata。主任务可简短提示指定Stable checkpoint是否需要公开，未授权则保持本地并继续其它工作，不反复追问或顺带提交。用户接受后，调查者停写指定文件；主任务隐私／内容审阅后仅force-add明确授权的文件、commit/push，完成前不恢复该文件写入。
- 已作为主任务review/hash依据的Stable版本，不在后台改写；先协调后续版本。相关输入在并行期间改变时，复核受影响结论并标明所用revision／commit及working-tree差异，不能把旧观察称为新状态。

## 报告与交接

使用[README内模板](README.md#报告模板)，只用Open／Stable／Superseded。Stable代表当前证据版本可供参考，既不等于用户接受、Gameplay冻结，也不授权实现。

区分确认事实、推断和未知；保持STATIC／LOCAL／USER_GAME_TEST证据范围。“未找到”不等于“不支持”，静态Modifier不证明AI会消费。发现Design错误或技术限制只在报告指出，交用户审阅／外部设计讨论；用户决定后由Main Task获授权更新正式Design，implementation仍需单独授权。不得自行修正正式来源或补设计。

新报告引用仓库文件采用相对路径；外部来源优先用已有配置项／清楚定义的来源根与相对文件、行号、版本，不重复写真实用户名和机器绝对路径。不得记录可复用密码、认证Cookie／session／token或私人配置。公开checkpoint前单独复核本机路径／认证数据及外部链接可访问性；个人路径需要由报告写者规范化，既有调查原件不由主任务自动改写。

报告保留轻量Read Ledger（主要入口、关键扩展／理由、未做的宽扫描），不记每次命令、不建新日志系统。完成稳定阶段时给出指定路径、范围、关键未知及handoff，等待主任务审阅与用户checkpoint决定。
