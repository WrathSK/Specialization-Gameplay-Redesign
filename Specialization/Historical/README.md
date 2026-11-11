# 冻结历史

既有冻结原件保持原字节；本次归档Design审阅只调整必要相对链接，规则正文不变，展示原件保持原字节。其中“最新/待测/多源未定”只是当时记录，不是当前权威。
当前玩法见[Design](../Design/README.md)，技术结构见[Architecture](../Architecture/README.md)，验证与暂停队列见[Status](../Status/Specialization_P0_Status.md)。少量新增的跳转文件仅维持旧相对链接，不复制证据正文。

设计审阅与文化展示来源见[设计历史导航](Design/README.md)；其中仍有效的接受依据与已被取代的候选分别标明。

## 原位保留的历史与证据

历史不要求全部物理迁入本目录。Architecture与Reports入口已将旧阶段派工与现行合同分开；冻结文件的相对链接、路径映射及review provenance仍有用途时保留原路径。

- [早期文件结构提案](../Reports/Proposals/Specialization_File_Structure_Proposal.md)含用户补充及迁移报告/路径映射引用，保留作为接受与迁移依据。
- [初次Design草案审阅](../Reports/Proposals/Specialization_D0001_Draft_Review.md)含来源缺口/候选状态，且旧冻结文档仍链接该路径；不是当前Design或待审批队列。
- [早期架构调查计划](../Architecture/Architecture_v2_Plan.md)与v2原始调查地图保留合同形成语境；后续批次已取代旧进度，现行导航见[分类索引](../Architecture/v2/README.md)。

当前正式合同、接受记录/反证、仍未决候选、已接受未来设计都不能仅按文件名或版本号归为废弃过程材料。不改写冻结原件，不以Git可恢复为理由删唯一证据。

## Phase 1 generated artifacts in Git history

Use the original paths at commit `240a89717aebc681408edfc01508b4fe00a4f04f` to consult the Phase 1 link classification and migration check output. Both originals were retrieved from GitHub and matched against their local SHA256.

| Original repository path | SHA256 | GitHub |
|---|---|---|
| `Specialization/Reports/Proposals/Phase1_Link_Audit.json` | `4c835a88a0feebd64b0923d75af6d50914038e080ef95c4bd9e164b85f112db5` | [Original](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/240a89717aebc681408edfc01508b4fe00a4f04f/Specialization/Reports/Proposals/Phase1_Link_Audit.json) |
| `Specialization/Reports/Proposals/Phase1_Migration_Validation.json` | `0033231b17214183e2f5a49cd57aab45bc40a17baf59c92ecfe5e01b2a50b9f3` | [Original](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/240a89717aebc681408edfc01508b4fe00a4f04f/Specialization/Reports/Proposals/Phase1_Migration_Validation.json) |

From the repository root, read either original with `git show 240a89717aebc681408edfc01508b4fe00a4f04f:<original-path>`. Substitute the full path from the table and pipe the output to `shasum -a 256` to verify it. The Phase 1 reports describe their original workspace and link resolution. Use the [legacy path mapping](../Reports/Proposals/Legacy_Workspace_Relocation.md) for current access to external evidence.
