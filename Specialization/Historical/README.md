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

## Early architecture candidates in Git history

The [six v1 reports](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/9addf8d01dcbcb46d28e59ffa5625950f4540e57/Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/Convergence_PreDesign_v1) and [seven v2 reports](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/9addf8d01dcbcb46d28e59ffa5625950f4540e57/Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/Convergence_PreDesign_v2) remain readable at commit `9addf8d01dcbcb46d28e59ffa5625950f4540e57`. Use the pinned trees to follow the original relative links. The [accepted Architecture](../Architecture/Specialization_v0.1_Architecture.md#current-authoritative-state) governs current work.

From the repository root, use `git show 9addf8d01dcbcb46d28e59ffa5625950f4540e57:<original-path>`. Prepend `Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/` to the path in the table. Pipe the output to `shasum -a 256` to compare it with the verified original.

<details>
<summary>Original paths and SHA256 for the 13 reports</summary>

| Path under Architecture_Reconstruction | SHA256 |
|---|---|
| `Convergence_PreDesign_v1/Decision_Register.md` | `f1a51eca79bb8bec09bc89d2aa47c8a25da51bace5e322e8689eca95d1ba8b62` |
| `Convergence_PreDesign_v1/Evidence_Appendix.md` | `83ee9a8aac0f1cf7fc013954f83212a747407133aaf01dd62d9f9cd0cee9c07a` |
| `Convergence_PreDesign_v1/Executive_Overview.md` | `9db317a1fb885d556361638f640a790dabba9c37079c94c8b9b820a674c583bc` |
| `Convergence_PreDesign_v1/Extension_Readiness_Assessment.md` | `9d701a0dcf9c33fa46954aa36b0a4d46050aeed90f9a6dee3afa5762942c6f40` |
| `Convergence_PreDesign_v1/Gap_Matrix_v1.md` | `9595919cf1c27c7dc910d152ac922171b56880f9358208ed7a93a42ee0ba67ce` |
| `Convergence_PreDesign_v1/Migration_Impact_and_Dependencies.md` | `5511e0f96b1b93e46383fd44139e18c0d32d8c0dfb63dc0e3143bfd7ef8c80c3` |
| `Convergence_PreDesign_v2/Decision_Register_v2.md` | `a7953625cac57380d74d6358e80b5c0d4a0061a6cec49df09659ed81dd2b1872` |
| `Convergence_PreDesign_v2/Evidence_Addendum.md` | `bcc6cf4fec6cd0d6b8047f07443d18b70b100a9c2c58a39ce79621af936695cc` |
| `Convergence_PreDesign_v2/Executive_Overview_v2.md` | `667e298c8cd5d061f87b87ddd3241899b70d4c3e261cbb99f3b1b3530ddf17fe` |
| `Convergence_PreDesign_v2/Gap_Matrix_v2.md` | `3a04986f491a7e55cff3bbc74e9db31c6e49c4a53649d5e43b2d9db2a5fab65a` |
| `Convergence_PreDesign_v2/Option_B_Migration_Map_v2.md` | `e5f3c6091dafc5809a519f6fcaa695e7aa65c49a39ca3cd6408975cf5d4a9989` |
| `Convergence_PreDesign_v2/Per_Ability_Fact_Use_Matrix.md` | `de471d9075e462e5ae02547126661bcbe4dee1ca3d35781ae0d3b43e92f650bb` |
| `Convergence_PreDesign_v2/Pre_U5_Worklist.md` | `d25a58a4bce4c4bf1f650045e653d224c958f978d1e1ab6f3c80c0e40282684f` |

</details>
