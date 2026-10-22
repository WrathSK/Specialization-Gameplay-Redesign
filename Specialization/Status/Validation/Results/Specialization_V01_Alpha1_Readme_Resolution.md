# Alpha.1 晋升：分支文档冲突处理与前次记录更正

日期：2026-10-21。用户授权保留main/develop不同README，并处理已定位的文档冲突。范围为晋升候选准备，不合并main、不部署、不创建版本标签。

## 更正

此前[晋升记录](Specialization_V01_Alpha1_Promotion.md)中“main是候选祖先”的判断错误，以本记录为准。共同祖先为e3651f9；main有bae6f66、08f1486、0896d59、e901a22四个独立文档提交。前次未正确检查祖先命令退出状态，不能将其视为通过。GitHub PR #1的mergeable_state=dirty是真实内容冲突，不是服务状态延迟。

只读三方预演定位四个冲突文件：根README.md、Specialization/README.md、根AGENTS.md和Specialization/AGENTS.md。main在共同祖先之后仅修改这四个文件；运行源码没有双侧冲突。

## 已批准的解决方式

使用promotion/v0.1.0-alpha.1作为临时晋升候选分支，以当前develop与main为双亲构造已解决冲突的合并提交，保留双方历史。它只承载本次晋升，不是另一条长期开发线。main和develop工作区不切换、不重置；主开发仍在原develop进行。

- 根README保留main中英文公开介绍，只将分支身份/版本说明调整为B268.295 alpha.1候选，并明确合并、标签及运行状态以晋升/部署记录为准。项目介绍正文、截图与视觉改版留待用户实机后另行授权。
- Specialization/README保留main的配套资料导航与develop跨分支导航，更新B268.295、D0057和待批准状态。
- 两份AGENTS采用现行develop约定。对照main独立改动，其有效的旧指南历史化、迁移映射、截图归档位置和源码/部署边界已被现行约定覆盖，不恢复旧版G0009或过时任务约束。
- develop两份README字节不变。候选分支相对develop仅两份README及对应Context_Lock散列不同；Mod目录树完全相同。
- GitHub不支持修改现有PR的head分支，因此创建替代PR，关联成功后关闭#1并标明替代关系，保留原PR讨论记录。

## 验证及后续边界

新增/修改文本经原发布检查器检查；候选使用隔离索引检查精确待提交文本，不改checker或长期规则。候选树的引用散列、Mod树和分支README差异单独核对。原运行包及既有243+28项测试结果不变，文档冲突解决不要求重复玩法测试。最终可合并状态以替代PR的GitHub实时结果核对。

原main和live临时部署不变。用户审阅批准合并后，仍先结束绑定旧main的临时部署，再执行晋升与稳定部署。未来晋升同样显式保留分支README，不设置会静默忽略冲突的全局合并策略。

User decision：审阅替代PR后批准后续合并/部署步骤。
User testing：本次无需新增实机。
Primary next：核对候选和替代PR，停止于审阅边界。
