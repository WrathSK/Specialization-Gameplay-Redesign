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

## Third architecture candidate and audit trail in Git history

The [nine v3 reports](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/fb7be65b664b78f2c692cdc9d661511f37823b2e/Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/Convergence_PreDesign_v3) and [24 follow-up reports](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/fb7be65b664b78f2c692cdc9d661511f37823b2e/Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/Convergence_PreDesign_v3_Final) share commit `fb7be65b664b78f2c692cdc9d661511f37823b2e`. Read both groups at this snapshot to follow the original links between the candidate, review and dispositions. All 33 originals were retrieved from GitHub and matched by SHA256. See [Architecture](../Architecture/Specialization_v0.1_Architecture.md#current-authoritative-state) for accepted technical rules and [Status](../Status/Specialization_P0_Status.md#current-authoritative-state) for the current work and evidence boundary.

From the repository root, use `git show fb7be65b664b78f2c692cdc9d661511f37823b2e:<original-path>`. Prepend `Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/` to the path in the table. Compare the output of `shasum -a 256` with the recorded value.

<details>
<summary>Original paths and SHA256 for the 33 reports</summary>

| Path under Architecture_Reconstruction | SHA256 |
|---|---|
| `Convergence_PreDesign_v3/Decision_Closure_Register.md` | `99561e047bd14828a37515871a7bf1805be553a57dea602b879826539c763a1f` |
| `Convergence_PreDesign_v3/Executive_Architecture_Map.md` | `584755e93374a914e4433415ed8055fcb5f096651ca4bf6da990a45f24ece6af` |
| `Convergence_PreDesign_v3/External_Audit_Package.md` | `1ae03f6544a66cb8eefde67225944f382e5e93646c56a055bb752f73a0b0d5e8` |
| `Convergence_PreDesign_v3/Fact_Subscription_Contract.md` | `d008244a278b238f809b9a354a852e7ddfb5db00718f0234ee1c6402bbe1814b` |
| `Convergence_PreDesign_v3/Formal_Authority_Sync_Delta.md` | `6db0ee25ae884caac7caa703cc897785a8c47b9d50c13ce25b48b4c53a3c4bbc` |
| `Convergence_PreDesign_v3/Gap_Matrix_v3.md` | `a6cf940a971ac047826f0f922a868ddb45d2440a71c685e3c7b704a9dc87dffe` |
| `Convergence_PreDesign_v3/Option_B_Final_Candidate_Plan.md` | `1da3b3005be845f50a0223baa2951b4462f3bcbf858dc1104c049e4cb117d3ea` |
| `Convergence_PreDesign_v3/Owner_Gate_Stop_Report.md` | `6ca50406cd2fd26b65113720e30d170dbf073b0d44c26add3a21f9c0218d00ec` |
| `Convergence_PreDesign_v3/Pre_U5_Final_Candidate.md` | `702e87a15397438731c51f7efaec1f6e16379a0d40d7c1dd7adac55b1fa03cda` |
| `Convergence_PreDesign_v3_Final/Architecture_Convergence_Integrated_Roadmap_DRAFT.md` | `df98c918ff812cb628b0e4fa96c5eaa0cbed9725f742882a85da061edb60e447` |
| `Convergence_PreDesign_v3_Final/Decision_Closure_Register.md` | `0e813b495a27ee220a8ac0794ad5e9e84eae923964d2a0d699ffdae6c6b1e83b` |
| `Convergence_PreDesign_v3_Final/Executive_Architecture_Map.md` | `8f025cf8852f2bd44a1f79479b6a758264d314112c5a174764e59cec2975aec7` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/Audit_Finding_Disposition.md` | `4a962f9a0c628879a308bd700b0cf57eb4aa904e0fe00f29c2775f19f7cc59b3` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/Claude_Targeted_Reaudit_Package.md` | `170456b4d421ecfaae2886b32b23ee9fe69aeee8df9ccf8801d0f99e0e00bb9b` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/Completion_Wake_Responsibility.md` | `e100c9bd963724ea0511a650890cea01ef8f0f21d89dd4db69efb368e5dc43b3` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/D1_Branch_Disposition.md` | `304efe04e0c528364210e0087aaa73278da7489999430b79099ad26e7624a0a3` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/Decision_Closure_Revised.md` | `8c9729df8080e2546c8b5e557438128902df87bae58deead2326179c6886432e` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/Evidence_Debt_Coverage.md` | `23a3bb17079f8a28029e8f42f7385bced6f0a5e0a6a5c4e1947c122dfb284028` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/Formal_Authority_Sync_Delta.md` | `44b14b080e180b730359428b619e69987d0f42506a727c965a615db56a2d44b4` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/NET_Cold_Load_Contract.md` | `156803440239181bf0924bd472999fff62cc43a1b62eb515468c1b9b8ebf8334` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/Owner_Gate_Remaining_Decisions.md` | `3e6b4ce048f884e853d8a10689611220143d4c233887d8f9670344dcea603347` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/Owner_Handoff_20261104.md` | `be655cc5e99ee97ba77e51749809152cd24b164f69c4f580f70d1ff2f788b04b` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/P3_Production_Dependency_Inventory.md` | `919bb434f25f51c6f6028bb883e4be54ad2175c8aac0f3ef1a5f7f2b9f67804f` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/PU_Option_B_Revised_Plan.md` | `3fd08fad7b157d761a585462cd5d34b5b31c51a6a86378c1644bb2a5a94a4eff` |
| `Convergence_PreDesign_v3_Final/External_Audit_Disposition/README.md` | `4a0dab50df590de28e111e2728723424a7ab47537c9e545cb3a6a560e3eba266` |
| `Convergence_PreDesign_v3_Final/External_Audit_Package.md` | `40f4b46a4c0d6e542740baf25f52c8014bf3552bca18619b79824f372b43b9f0` |
| `Convergence_PreDesign_v3_Final/Fact_Subscription_Contract.md` | `8b7bd3665129fcf3f6e7eafc7678c81416ea0e5570cf6a1b8bd75840d3523b2d` |
| `Convergence_PreDesign_v3_Final/Formal_Authority_Sync_Delta.md` | `0d7cd0411d695772a92d75d75c6cfd69ce67b7a54e0f5ab1c38b81d2636ec4d7` |
| `Convergence_PreDesign_v3_Final/Gap_Matrix_v3.md` | `a1331bb13783abf2006bb8cabac7398b1292e307c2daeb2c5c03dee197aba4d8` |
| `Convergence_PreDesign_v3_Final/Option_B_Final_Candidate_Plan.md` | `7518591d01ab8f18614e7b94f437127b77fd3eb2b889f6331c79ef42e0b8d0c4` |
| `Convergence_PreDesign_v3_Final/Owner_Gate_Stop_Report.md` | `f55df0e68115787c52e68da67cb91f05193cef3ff3d4ec07798194e66d9d45f1` |
| `Convergence_PreDesign_v3_Final/Pre_U5_Final_Candidate.md` | `98cbb7c87c3567cb25a76d33aa7c7fa937d2928bdbe4d45cba185fcae638eb8e` |
| `Convergence_PreDesign_v3_Final/README.md` | `af5d009127d8355cede1548d440ad86dd062ddd03d0ec0232c843df0a28f6daa` |

</details>
