# 开发指南 / Development guide

日常开发在[develop](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/develop)进行；[main](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/main)保存获准的测试源码。两者使用独立工作树，外部游戏目录仅为部署目标。

1. 从[根约定](../AGENTS.md)、[项目约定](AGENTS.md)和[项目导航](README.md)开始，按Authority与Status进行任务范围内阅读。
2. 修改须符合用户授权；仅提交本批文件，完成适当验证和发布检查。原始证据、机器配置与未批准素材留在本地忽略目录。
3. 整批推广默认通过develop → main PR，采用保留祖先关系的普通合并；范围有限的稳定修复仍按既有hotfix流程处理。
4. main上的合并及记录完成后，通过Git正常回流develop；不要在两个分支分别重造相同记录。冲突须检查，不以整棵树强制覆盖。
5. 两个README保持共同入口；测试与开发用途分别由独立说明文件承载。版本和部署身份由Status与部署凭据维护。
6. 必须隔离候选时才使用临时发布分支；合并并核实其提交已包含在main后清理。长期保留main/develop，删除远程分支仍遵循明确授权边界。

详细流程见[Playtest Workflow](Architecture/Playtest_Workflow.md)。PR、合并、部署各自遵守用户授权；文档整理不会自动部署或启动游戏。

Use develop for ongoing work and main for approved playtest source. Shared entry documents link to audience-specific guides. Promote through a reviewed merge PR, then carry main-only records back through Git instead of duplicating them.
