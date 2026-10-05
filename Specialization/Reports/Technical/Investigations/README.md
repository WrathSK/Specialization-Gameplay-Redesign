# General Investigation Zone / 通用调查区

这里供一个长期复用的独立调查会话，在同一develop worktree中研究用户明确指定的Civilization VI／Harmony in Diversity技术问题。调查回答“暴露了什么接口、证据是什么、还不知道什么”，不产生Gameplay决定，也不代替实现任务。

> **Investigation / Non-authoritative / No design decision implied**

用户是最终语义权威。这里与现有Design、Architecture、Status、Validation职责分离；不构成第二套Authority、Workflow、调度或memory系统。操作约束见[本区AGENTS](AGENTS.md)、[项目并行例外](../../../AGENTS.md#并行-investigation-窄例外)、[W0001/W0005](../../../Workflow/README.md)。这是文档工作协议，不是额外的操作系统沙箱。

## 主题目录与当前导航

当前没有主题目录；本次初始化不启动具体调查。

新主题必须由用户明确提出。先复用现有同主题目录；不存在时选择稳定、清楚的名字，只建本次所需README和Markdown报告，不预建空主题。主题README记录范围、排除项、报告导航及非权威声明；根区导航由主任务维护，调查者只维护本主题导航。

推荐先由主任务创建或审阅最小主题骨架，普通commit/push形成tracked baseline，再长期调查。用户明确允许调查者先创建时，文件可暂留untracked；这不授予Git写权限。一个新主题不需要新branch、worktree、manifest、Workflow编号或锁文件。

## 并行文件与Git边界

调查会话只能写自己当前授权主题的Markdown；主任务继续维护用户授权的正式文档与实现。双方可以按任务需要读取产物，不互相修改专属文件。目录中的规则不能由调查者改写来扩大权限。

Investigations保持Git可跟踪，不加gitignore。调查者仅做只读Git查询，不add/commit/push/pull/fetch、不切分支、不stash、不修改配置。主任务仅显式stage本批文件，禁止整树add或commit-a；其它调查改动可以保持dirty/untracked。

主任务需要引用调查报告时，先核对证据范围；Stable报告不会自动成为Design、Architecture合同或全部任务的默认读取项。hash/index登记由主任务按实际review依赖处理，不因文件进入Git就全量加入context；已有审阅依据发生变化仍须复核，不能盲目rehash或绕过失败。

## 读取范围

- **Stage A**：固定入口和当前主题直接材料；Authority／Status只读当前边界，不读整份历史。技术来源使用用户／现有配置明确给出的入口。
- **Stage B**：有明确调用、注册、表关系、Modifier／Effect、路径或符号时，跟进对应定义及必要调用点。
- **Stage C**：小范围扩展先记录问题、理由、具体查询、证据目标及停止条件。跨主题、历史、未授权外部目录、广泛HD／Mod扫描或新研究主题，先取得用户确认。

完整约束见[AGENTS](AGENTS.md#stage-a--b--c-读取)。Read Ledger只记录关键入口与扩展，不逐命令记账。主题切换必须显式授权并重走Stage A；不得继承上个主题的宽读取范围。

## 报告状态与checkpoint

| 状态 | 含义 |
|---|---|
| Open | 正在调查，结论可能变化 |
| Stable | 当前证据版本已稳定，可供讨论引用；不表示用户接受或设计冻结 |
| Superseded | 已被后续指定报告／版本取代，保留追溯链接 |

长调查可以分段形成Stable checkpoint，不必等待整个主题结束：

1. 调查者标明报告路径、完成范围、未知项，停写本次指定文件。
2. 主任务只读审阅；有问题交回调查者修订，不直接接管文件。
3. 用户决定是否接受该指定checkpoint进入Git。
4. 主任务复核diff、归属及并行状态，仅显式stage被接受文件，commit/push；其它改动不随入。
5. 主任务确认checkpoint结束。后续修改已被引用／锁定的Stable版本先协调，不后台改写。

技术结果影响玩法时继续使用：**Investigation evidence → Design Talk discussion → User decision → Design Authority update → separately authorized Implementation**。用户接受调查checkpoint只是接受记录入库，不自动接受某种Gameplay方案。

## 报告模板

按实际问题删去不适用小节；不强制每主题相同文件数量，不另建模板文件。

```markdown
# <主题 / 问题>

Investigation / Non-authoritative / No design decision implied
Status: Open | Stable | Superseded（实际只选一个）
维护者: <调查会话或用户明确交接的维护者>
范围: <本次问题及明确排除项>
依据: <相关repo commit / Design revision / 外部来源版本；未提交输入差异如有>

## 已确认事实与证据
<文件／符号／DB表／API／公开资料链接，证据等级与适用边界>

## Read / Write / Listen surface
<接口、参数与已知限制；未知与未测单列>

## 推断、反证与未知
<推断依据与置信度、其它解释、不能推导的结论>

## 最小native验证建议
<只有本地证据不能回答的问题；建议不是实测PASS或实施授权>

## Read Ledger
<主要入口；关键扩展路径／理由；C扩展的证据目标与停止条件；未做的宽扫描>

## Handoff
<完成范围、关键限制、尚未解决问题、供用户决定的事项>
```

不要记录可复用的认证信息、私人配置或无关数据；不要将原始游戏、日志、截图、存档或运行包搬入本区。实机原件与公开资料各按现有证据约定保存／引用；没有取得原件不声称重新检查过。
