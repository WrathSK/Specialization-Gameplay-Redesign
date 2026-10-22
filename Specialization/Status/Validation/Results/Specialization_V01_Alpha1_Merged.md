# Alpha.1候选：main晋升与稳定部署完成

日期：2026-10-21。用户已审阅并授权合并PR #2。GitHub普通merge完成，提交852b04c9af9d69b41ea3bc9d4a791f61dcd94202，保留候选c31e06b的双方历史和main专用README。旧PR #1由#2替代并关闭。

main正式源码基线现为B268.295 / modinfo295，取代B069.96。develop继续保留自己的两份README。项目介绍的截图和全面改写仍待后续授权。

## 部署与恢复

确认游戏退出后，先通过B268.295-5091059-playtest.json将临时部署恢复旧stable，凭据进入STABLE_RESTORED；旧main及备份哈希一致。随后合并并同步独立main工作区，从干净已提交main部署B268.295。运行目录310/310文件与main一致，SHA256为9c5c1b64a8b4a10c39c2f9bc975c3a59a6ecee08c650e77ac1e5455b2747d6da。外部本地记录：B268.295-852b04c-stable-deployment.json。旧stable及移出的develop包保留，事务标记已清除。

运行字节与用户此前测试的B268一致；没有新玩法修改、游戏启动或配置改动。原243+28项检查和实机覆盖边界保持，截图仍只归档而未视觉验收。未创建版本标签或GitHub Release；v0.1.0-alpha.1仍为拟定名称，main晋升不代表最终v0.1冻结。

长期实机基线已明确，结束此前W0003临时develop自动切换阶段；后续运行包变化遵守显式批准与现有恢复检查。未来晋升保留分支各自README，不将候选README反向覆盖develop。

本记录更新Status/Authority/manifest/Runtime_Index指向实际main和live状态；原批次与晋升准备记录保留为历史，不反写其当时结论。[祖先关系更正](Specialization_V01_Alpha1_Readme_Resolution.md)仍有效。

User decision：版本标签与Release尚未执行。
User testing：继续约定综合实机，无须为本次仅源码晋升重复图标验收。
Primary next：等待反馈；不自动启动新开发或部署批次。
