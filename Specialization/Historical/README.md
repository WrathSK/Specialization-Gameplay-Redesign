# 冻结历史

既有冻结原件保持原字节；本次归档Design审阅只调整必要相对链接，规则正文不变，展示原件保持原字节。其中“最新/待测/多源未定”只是当时记录，不是当前权威。
当前玩法见[Design](../Design/README.md)，技术结构见[Architecture](../Architecture/README.md)，验证与暂停队列见[Status](../Status/Specialization_P0_Status.md)。少量新增的跳转文件仅维持旧相对链接，不复制证据正文。

设计审阅与文化展示来源见[设计历史导航](Design/README.md)；其中仍有效的接受依据与已被取代的候选分别标明。

## 原位保留的历史与证据

历史不要求全部物理迁入本目录。Architecture与Reports入口已将旧阶段派工与现行合同分开；冻结文件的相对链接、路径映射及review provenance仍有用途时保留原路径。

- [早期文件结构提案](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/8fbc08ad97b503ad500ed3009e3c1f7867b90cd0/Specialization/Reports/Proposals/Specialization_File_Structure_Proposal.md)含用户补充及迁移报告/路径映射引用；原件在固定Git历史中保留，接受与迁移依据仍可精确取回。
- [初次Design草案审阅](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/860fe6359ef98699dc75ab7dc5cdb84fb11d8207/Specialization/Reports/Proposals/Specialization_D0001_Draft_Review.md)保存最初来源缺口和候选审阅语境，原件从固定Git历史取回；当前规则与未决项以现行Design和Status为准。
- [早期架构调查计划](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/98131a7a6dec32c50cdfb1ac39d8f95af42f19f3/Specialization/Architecture/Architecture_v2_Plan.md)与v2原始调查地图已转为固定Git历史，保留合同形成语境；后续批次已取代旧进度，现行导航见[分类索引](../Architecture/v2/README.md)。

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

## Early README and AGENTS snapshots in Git history

The 13 early README and 13 AGENTS snapshots are available in the [original snapshots directory](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/1c0b97fdd62ead58e1580c6b274614f6e0d02280/Specialization/Historical/DocumentSnapshots) at commit `1c0b97fdd62ead58e1580c6b274614f6e0d02280`. All 26 files were retrieved from GitHub and matched by SHA256.

The pre-migration `Phase1_before_README.md` is now [history-only](#phase-1-before-navigation-snapshots-in-git-history). Follow its earlier README citation to [the original file](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/1c0b97fdd62ead58e1580c6b274614f6e0d02280/Specialization/Historical/DocumentSnapshots/README_before_fresh_agent_handoff.md). The [Phase 1 copy manifest](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/8fbc08ad97b503ad500ed3009e3c1f7867b90cd0/Specialization/Reports/Proposals/Phase1_Copy_Manifest.json) retains the original migration inventory.

From the repository root, use `git show 1c0b97fdd62ead58e1580c6b274614f6e0d02280:<original-path>`. Prepend `Specialization/Historical/DocumentSnapshots/` to the filename and compare `shasum -a 256` against the table.

<details>
<summary>Original filenames and SHA256 for the 26 snapshots</summary>

| Original filename | SHA256 |
|---|---|
| `AGENTS_before_A0009.md` | `dd2ad3bf2b2417cb16633b19ae927b80d25066b1b2bfdbc51f32ece6665b0c1c` |
| `AGENTS_before_A0010.md` | `e7c1d974cbf14d0f3246119790f4bf8ec6d40714a0abd573288bed0dcb8cc270` |
| `AGENTS_before_B011_user_review_20260911.md` | `db63a76fd7198f61d4e0608dfd6ddb3756ca8060ba6103da7c68bce64a411bde` |
| `AGENTS_before_B012.md` | `66a579a89ffde1330429bf9f20f64b1a9b71adde6745e57bb62303ae429b301d` |
| `AGENTS_before_B012_user_review.md` | `f4b515d706161a31f333e9befae2ba6f574c52142e4b82835c27c548bb584c0e` |
| `AGENTS_before_B013.md` | `120b18240245991049c6b31ed49df1123dc3fb0c7096790615e8450b4cb2985f` |
| `AGENTS_before_B013_user_review.md` | `507d18740b05ccca44c1b11c5b8771cc94368a66330180a57370807db70da7a6` |
| `AGENTS_before_B014.md` | `1de5e5562adf732ee36c6ac63138655ce2f978eb7b98b4b308fb6bed039eacec` |
| `AGENTS_before_B014_user_review.md` | `62a1d661f6301321a8944c550b27bcb01d63da612d9735f295114bcd0a72866c` |
| `AGENTS_before_B015_user_review.md` | `b2a194276b04293aa321caddbf4679ce0ec126f3b0fa097d4188cd68a26e4d66` |
| `AGENTS_before_archive_binding.md` | `b61d2f29af4ca6d3bc0c32329ee78ae674ec4caea0b1150688e4636a2aac32cf` |
| `AGENTS_before_completion_history_review.md` | `8cdf6da4438c01907ea8950c8171198442608437a158171b938e568cc3e13ef4` |
| `AGENTS_before_fresh_agent_handoff.md` | `70c06bba9221c1724df146b9d5cb9acebafe58f2868394ebb1705a0aef88ff68` |
| `README_before_A0009.md` | `fd684903276b9e6adf21bcdac62369ea9c00cc1fa9a0ad043b41f35c902ed615` |
| `README_before_A0010.md` | `3e026e5da1879f8631fb44093235e41e2606312d3e220fd54a419af2fc6b4867` |
| `README_before_B011_user_review_20260911.md` | `336b427263174de683bf507f9e497dec90bce2b540e6510f0e5ea4943cf16d04` |
| `README_before_B012.md` | `8a85fc2df0e36186dc98f5dd6b0899bde862e456342b964d072c6ad77a1965c9` |
| `README_before_B012_user_review.md` | `3f81ba1a185af26b1f4e2106ffe55ca7088ae06973fabf711196dda4ecd261b6` |
| `README_before_B013.md` | `e49b97b797b0dda85b07776b2fcd952ffda6ee0bb52275eb77e1478d530f3428` |
| `README_before_B013_user_review.md` | `15da7f5cabb03b8893056a507c3017ff0bdbb0a62992ccf156deb35ecd8e662d` |
| `README_before_B014.md` | `45848d114c438cd384c6a213b18417958e466dc340fe137e1106e236c7a21c0b` |
| `README_before_B014_user_review.md` | `b542a009307ff9fc470979690142413b582c1fd82e8aff7ba7bb33d33a294912` |
| `README_before_B015_user_review.md` | `858f14040785bfc9795c1603cfc569312888837f0faacccf2493ccc7cc1396ee` |
| `README_before_archive_binding.md` | `a068c8f8e1fdeb14a3eb880f0e631d53b1e2a3d2d58f9ce9e99be94dc072cdde` |
| `README_before_completion_history_review.md` | `58c1c783964e26570256796171310558e3c40dd5d1793ec29a8cf74dc82ca99e` |
| `README_before_fresh_agent_handoff.md` | `1266642548d1b8f0d9e20016b1377e6c7228bbb2aeecd7284e0b3b449ad7560f` |

</details>

## Early Status, Architecture and technical index snapshots in Git history

The [snapshot directory](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/ca540456ff1d0610281085ba6026b21f636933e9/Specialization/Historical/DocumentSnapshots) at `ca540456ff1d0610281085ba6026b21f636933e9` preserves the 49 originals listed below. Read the earlier status, architecture and technical index files at this same commit to keep their relative references together. All 49 originals matched the published bytes by SHA256. The four Phase 1 snapshots retain their tracked paths.

From the repository root, use `git show ca540456ff1d0610281085ba6026b21f636933e9:<original-path>`. Prepend `Specialization/Historical/DocumentSnapshots/` to the filename and compare `shasum -a 256` with the table.

<details>
<summary>Original filenames and SHA256 for the 49 snapshots</summary>

| Original filename | SHA256 |
|---|---|
| `README_technical_before_A0009.md` | `deb3f2b838e14f98e599b6ad4be73909dfb86d53b62735a149e644f3560146d0` |
| `README_technical_before_A0010.md` | `7a5c6f602f7d7449499a186bbc94e55e571ed3003a37934901e6ba5f70fd2ec2` |
| `Specialization_P0_Status_S0003_before_D0001_sync.md` | `85f3e08f8e1174d7c540b02b2ab86133d835b4a9e95a322b300b2586886d1d78` |
| `Specialization_P0_Status_S0004_before_multisource.md` | `6ed23f2313251b81e9045b5610c9e69920ae95ad48849927d3e2b3cd19a81512` |
| `Specialization_P0_Status_S0005_before_route_audit.md` | `b4e6ae00ad333a6b5a2429de4f5390cc477a5b464e97dfb27bc68c00ccea19f4` |
| `Specialization_P0_Status_S0006_before_city_state.md` | `66410db39a7f6c05aab4faa51796815b53073d1ceb47d5bfd80094e90c0b78e6` |
| `Specialization_P0_Status_S0007_before_completion_adapter.md` | `a687c39f4a1eafbc1ba91c1ca69bc409f0e13369305b7d76d4efe726bfd18136` |
| `Specialization_P0_Status_S0008_before_B011.md` | `c3c8e52e1fd407880f0e411b3c08ef4efa3b6986cbb8bc2bd107f5d86fc75ab2` |
| `Specialization_P0_Status_S0112_before_B051_failure.md` | `91ae1763b55204bf5a264cf073d4d186bd4eec99cb88d2b4fde0de47408d8c8e` |
| `Specialization_P0_Status_before_A0009.md` | `97e2a7fc848558ade121285addc310521f10992a16403bbf73b5d10e283740e9` |
| `Specialization_P0_Status_before_A0010.md` | `b0e9342030630b2cbe2c1f169b3b796d72d61c84b8318999d9a78801703502b6` |
| `Specialization_P0_Status_before_B011_user_review_20260911.md` | `dcf1931daaa8ef5e9c3ca87fde35b109c20d283b3d6ae2cb6647dc459e279dd9` |
| `Specialization_P0_Status_before_B012.md` | `4878924b09caf7bdaacaead6efec40e93bf86354c9649bff90e7d415c3d8e7c9` |
| `Specialization_P0_Status_before_B012_user_review.md` | `08ea147056850c42e5b6e1d560d7560f2bb3e62b564078d81ec70771ee6a2ccd` |
| `Specialization_P0_Status_before_B013.md` | `afb6a073396a356130560450be195f49a620b64213a1b3a20d39cf7349e0c4a6` |
| `Specialization_P0_Status_before_B013_user_review.md` | `dcb0e67e3edaf5eceaff39b06341395a779cdd7197455b097d3e6d7813d92cbf` |
| `Specialization_P0_Status_before_B014.md` | `40a1ff81d3f3378d50778a62088fef1cf22a9bc3e5fefe168602388d8adb6dac` |
| `Specialization_P0_Status_before_B014_user_review.md` | `f39e069930ebfe0da31eaa02705d50039740ac730d9271afcaee5e5183bc9caf` |
| `Specialization_P0_Status_before_B015_user_review.md` | `1dfac502659d9ca6ff167f1daf7a09ddcf546e06bae8d1947e79280c5f94f851` |
| `Specialization_P0_Status_before_B069.md` | `1e85254d313d39d582a90ec69ab08bbb4737865d68b563ee19b217313086d2a8` |
| `Specialization_P0_Status_before_archive_binding.md` | `8d3b097030e6a17d45de25f36126a92421a6c4d1620082140e6ab11bb4257ddd` |
| `Specialization_P0_Status_before_completion_history_review.md` | `6226b5087481c5d80a66830b51eab5fdb71a2b3e85b508c64e7d81f16bd0d72a` |
| `Specialization_P0_Status_before_fresh_agent_handoff.md` | `ac84b76962de163c5c33c137b6c572a3a737a55a59cd21361176aea072be2b73` |
| `Specialization_P0_Status_before_phase1_B010.md` | `c1f846d5211290455da9b1cbf656332b21fda6105d15c8632bebc5732707c3e0` |
| `Specialization_P0_Status_through_B003.md` | `b51328d9b3ba04977c7b1a858539925d45ecb4f68aa19935af60fd64287c5144` |
| `Specialization_v0.1_Architecture_A0001_before_D0001_sync.md` | `e15cc943f480225bedba39051ad09c331f660c8411c286723105238147190820` |
| `Specialization_v0.1_Architecture_A0002_before_multisource.md` | `d082a190fadd8e86c0221a90b87b4c72dcad78bcb1f8a9d9a26e62c2d98d8581` |
| `Specialization_v0.1_Architecture_A0003_before_route_audit.md` | `d85de5cd22a2834eff5022d60c63060b0f266c73bfa614d106fe77214f18482a` |
| `Specialization_v0.1_Architecture_A0004_before_city_state.md` | `568e9dd6bcd38a8d0b74950f06f76e8e9a1e561e098cb96a7dbfeb524e863deb` |
| `Specialization_v0.1_Architecture_A0005_before_completion_adapter.md` | `42916e75b5cb28b2a06d5a1b14e49503049c8bbdf3f4b2d2d43c842b576c4d74` |
| `Specialization_v0.1_Architecture_A0006_before_B011.md` | `bb9fff7d248a78340f4d1228639b758bbe42ca30ffa7042988a209d2d949d6ac` |
| `Specialization_v0.1_Architecture_before_A0009.md` | `eebe546950ae6abaed805ff878ced45141b4e16c5c97724c0ed42d95819f69e0` |
| `Specialization_v0.1_Architecture_before_A0010.md` | `4c586284ca0ec69079a88b6d324f825670d162c26f0d587005a72ac7ff19374b` |
| `Specialization_v0.1_Architecture_before_B011_user_review_20260911.md` | `b6bfbf6b4a477a57a677588d337e8ae7068bb60967da983ff3c6eeb5e04eaa0f` |
| `Specialization_v0.1_Architecture_before_B012.md` | `b76dac0d21bb5f2d01dc2850c7c50e1e4d9e7a115929d44ccc546b73caf45643` |
| `Specialization_v0.1_Architecture_before_B012_user_review.md` | `dde40c2d0b200d9f3f5a1fd46ba9f9803d0a17722419d2094fa1a399ae75c709` |
| `Specialization_v0.1_Architecture_before_B013.md` | `9eeb61d449e4e4b7527f96fbbf2f23fa0e95c9b59c6766ccaa53ea8e7815a986` |
| `Specialization_v0.1_Architecture_before_B013_user_review.md` | `42ae34a5e83561236f57ea82271a277d7a355fc41b4752c28622fc6707a19417` |
| `Specialization_v0.1_Architecture_before_B014.md` | `e3fe6a7edbe36fe56fc9efbc6a858d2a4747eda524eed2fb377623dcea1f840b` |
| `Specialization_v0.1_Architecture_before_B014_user_review.md` | `c7d50e53997ce4e21f9f18725f644f502141fdc5c1d5f788b3d3353f920d828f` |
| `Specialization_v0.1_Architecture_before_B015_user_review.md` | `cbf9f1f9215abc92956ce98b7b311c4a79ea570297f039e3e8f112a5635435d8` |
| `Specialization_v0.1_Architecture_before_B069.md` | `6c2a6f30b2682ffc7e4fc8336b95a1ac0d11d19e953364bedb8faa801256d0fe` |
| `Specialization_v0.1_Architecture_before_archive_binding.md` | `d1e5873403583dd6ac7254d5e34089b7633f0c5f77dfcf83b72484be2d288551` |
| `Specialization_v0.1_Architecture_before_completion_history_review.md` | `15e198a451f81b887f21d040476d390ba80f3433dcac8c1d67966fae832ab87d` |
| `Specialization_v0.1_Architecture_before_fresh_agent_handoff.md` | `ff58a8fa5e9daf46fcd0994eb30222f5b6af03dfce077af98db1ddc5687c195f` |
| `Specialization_v0.1_Architecture_before_phase1_B010.md` | `a43517577b3cef5ac249efbf99a257d500518f2cec2fea2d3f0cae6b9cbc8a8a` |
| `Specialization_v0.1_Architecture_through_B003.md` | `6f7566c8da739cf8ac5effac532036d8a8895d7ecbb2bc97f3c8e14ea883813f` |
| `Technical_Index_before_completion_history_review.md` | `e8dfda9f28dbf4be2f8b39bfe4c12276b80647d03109f48ee7ab12c31a0328d2` |
| `Technical_Index_before_fresh_agent_handoff.md` | `4b58fd9b9e089c26841c39f882ada95579300c6d93fc90cfaf8d11802409f178` |

</details>

## Completed localization review and B527 audit handoff in Git history

The three B489 localization review documents completed their delivery role. Adopted copy is maintained in the actual `Mod/Text/` SQL/XML and UI localization sources; S1070 records the acceptance and remaining historical-fixture/native-layout limits. This retirement does not claim that every proposed diagnostic/legacy rendering was adopted. Design still governs gameplay meaning. The B527 closeout handoff likewise completed its delivery role: the Stable independent audit is retained in its original report, the Owner-approved closeout record and A0187/Status carry current responsibilities and limits. None of these four files is a runtime, test, generator, deployment or recovery input.

All four originals were independently retrieved from GitHub at published commit `a4b340b984af01774bc15bfcec8951ceb2b5b14a` and matched byte-for-byte before retirement. This is Git-history preservation, not a new local archive. Read one from the repository root with `git show a4b340b984af01774bc15bfcec8951ceb2b5b14a:<original-path>`.

| Original repository path | SHA256 | Fixed GitHub source |
|---|---|---|
| `Specialization/Reports/Proposals/Chinese_Localization_Draft.md` | `c4629aa6a2830ac101f68b584270f9d7c0075530e0775ef706a485adfa8a982f` | [Original](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/a4b340b984af01774bc15bfcec8951ceb2b5b14a/Specialization/Reports/Proposals/Chinese_Localization_Draft.md) |
| `Specialization/Reports/Proposals/English_Localization_Draft.md` | `932d2e13ed1fe5e40a1ffaec968dec54687a2ab9963043b2a8c6283763bedad2` | [Original](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/a4b340b984af01774bc15bfcec8951ceb2b5b14a/Specialization/Reports/Proposals/English_Localization_Draft.md) |
| `Specialization/Reports/Proposals/English_Localization_Sample.md` | `861b70eabf798ad87163a6e629228d97b6f0e7595c3405d24a4667201fb29a46` | [Original](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/a4b340b984af01774bc15bfcec8951ceb2b5b14a/Specialization/Reports/Proposals/English_Localization_Sample.md) |
| `Specialization/Reports/Proposals/Architecture_Convergence_Closeout_Audit_Handoff.md` | `fbc462cd9389ee0fb36b433517df6889df4265e23fd4f8f6d214d065224d0616` | [Original](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/a4b340b984af01774bc15bfcec8951ceb2b5b14a/Specialization/Reports/Proposals/Architecture_Convergence_Closeout_Audit_Handoff.md) |

**Known historical locators:** the old S1094 Status paragraph retains one relative Markdown link to the now-retired handoff. Its original P0-H result and the Stable audit's Requested-by line also retain the old textual path. These are historical references, not live inputs; use this table's fixed source instead. Their original bodies/hashes are preserved, and this cleanup does not claim every historical relative link resolves in HEAD. The inter-draft links leave the current tree together with the drafts. No current authority or default context points to the retired files.

## Phase 1 before-navigation snapshots in Git history

The four snapshots were initially retained pending their dependency/relative-link review. That review is now complete: no current code, test, tool, authority, manifest or runtime index consumes them. Their old reading instructions, B051/S0116 state and A0111 implementation descriptions are superseded by the current AGENTS/Workflow, Status and Architecture; the accepted Design, original validation reports and migration path mapping remain in place. Their unique historical prose is preserved in Git rather than copied into a new archive. Intrinsic pre-migration relative paths retain their historical meaning and are not advertised as working current links.

All four files were retrieved independently from GitHub at published commit `a4b340b984af01774bc15bfcec8951ceb2b5b14a` and matched by bytes/SHA256. Recover with `git show a4b340b984af01774bc15bfcec8951ceb2b5b14a:<original-path>`.

| Original repository path | SHA256 | Fixed GitHub source |
|---|---|---|
| `Specialization/Historical/DocumentSnapshots/Phase1_before_README.md` | `4a6f981d7eb78bb5a1916666fc4718c1a9c896620a5759c8520b79ffc9aa5363` | [Original](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/a4b340b984af01774bc15bfcec8951ceb2b5b14a/Specialization/Historical/DocumentSnapshots/Phase1_before_README.md) |
| `Specialization/Historical/DocumentSnapshots/Phase1_before_AGENTS.md` | `653317344bad81b8ecfd23108da0b96b49f8b76e0e343112e4ebf42bcaf4ee1b` | [Original](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/a4b340b984af01774bc15bfcec8951ceb2b5b14a/Specialization/Historical/DocumentSnapshots/Phase1_before_AGENTS.md) |
| `Specialization/Historical/DocumentSnapshots/Phase1_before_Specialization_P0_Status.md` | `30b709a95f01b1ecb3eff29762376aedb142e381d30824914986f0f18b0567ae` | [Original](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/a4b340b984af01774bc15bfcec8951ceb2b5b14a/Specialization/Historical/DocumentSnapshots/Phase1_before_Specialization_P0_Status.md) |
| `Specialization/Historical/DocumentSnapshots/Phase1_before_Specialization_v0.1_Architecture.md` | `87f2a8ec37c84b4994f9723e55b49094bb2bb2f47bdfce836bf649836978c1a9` | [Original](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/a4b340b984af01774bc15bfcec8951ceb2b5b14a/Specialization/Historical/DocumentSnapshots/Phase1_before_Specialization_v0.1_Architecture.md) |

<a id="proposed-next-family-early-local-refactor-results--owner-approval-required"></a>

## Early local refactor results in Git history

**Retired from HEAD under the Owner-approved document lifecycle delegation (2026-11-18).** This completed family follows the S1097 cleanup; its original proposal and decision boundary remain historical in S1098. The reports describe completed S4/S5 local implementation checkpoints; they contain no original user-game logs, screenshots, saves or independent native acceptance. Current rules/results are maintained by Architecture/Status and the versioned test sources. Original assertions, failure descriptions, commands and source versions remain recoverable from the unchanged report blobs.

**Exact retired scope:** the 15 reports below under `Specialization/Status/Validation/Results/`, totalling 404 lines / 72,123 bytes. Each was fetched independently from GitHub at published commit `e42caca061db9b50c3b3c869e1fe2fd1666220c1` and matched against HEAD and the local Git blob. Recover with `git show e42caca061db9b50c3b3c869e1fe2fd1666220c1:<original-path>`. These are original preserved bytes, not reconstructed reports.

| Original report (fixed source) | Lines | Bytes | SHA256 |
|---|---:|---:|---|
| [Specialization_B274_Refactor_S4a.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B274_Refactor_S4a.md) | 32 | 5283 | `6c91e2543d77f965957fe6dfd98b38461fb7fb43024446601359c075b1980c03` |
| [Specialization_B275_Refactor_S4b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B275_Refactor_S4b.md) | 37 | 6972 | `cb30f07c3e1229043f4f1c87c087e21869821e17502339c275bb3a0be6c594fd` |
| [Specialization_B277_Refactor_S5a1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B277_Refactor_S5a1.md) | 29 | 4500 | `27bc6a1e4cf9bc1e59132257965a03ec90b200b6a429b55eebafb1c126505ad2` |
| [Specialization_B279_Refactor_S5_History.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B279_Refactor_S5_History.md) | 27 | 5460 | `4ab5a9fe5de63fa97b690be4c1c88f65fab929686a9f04dbce2728c296ced6fb` |
| [Specialization_B280_Refactor_S5a.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B280_Refactor_S5a.md) | 27 | 5981 | `47924c7d6da2961e4c1102525f76cbbd65df872356cc82cebaf2e6f9723d72be` |
| [Specialization_B281_Refactor_S5b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B281_Refactor_S5b.md) | 25 | 4948 | `c5ba70256f60ec50c5db065757eca1f2d44ba1ba42e5d012b1e5e59b7f8c85ac` |
| [Specialization_B282_Refactor_S5c1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B282_Refactor_S5c1.md) | 25 | 4758 | `71e9922ae480bbe81b51ff30d93e4a84ee286586bbbd328bc2434c7f68060ca0` |
| [Specialization_B284_Refactor_S5d1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B284_Refactor_S5d1.md) | 21 | 3360 | `f745b30bc672402700b37c788af59d3c794de63492489dbf2ab68ec7d11eaa8a` |
| [Specialization_B286_Refactor_S5d3.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B286_Refactor_S5d3.md) | 25 | 4481 | `5497a718d4117b16dcac7b8b5995a32ffaec75dba476ae136d9beac7d2d2f19b` |
| [Specialization_B288_Refactor_S5d4b1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B288_Refactor_S5d4b1.md) | 25 | 6139 | `c290c0e1ee3a6f378170b5360508fc44d3efa90ca635ebadd50ebe8007d08b9e` |
| [Specialization_B289_Refactor_S5d4b2.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B289_Refactor_S5d4b2.md) | 31 | 5074 | `84c61dbf797678b79d52fc7ddabfff0682c6911f56a432da43892ba5dbdd70a3` |
| [Specialization_B290_Refactor_S5d4c1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B290_Refactor_S5d4c1.md) | 25 | 4067 | `06391eb4d6e0f120798ee8d805dcabeae69f49361d65f2f67f1b199a4819a4de` |
| [Specialization_B291_Refactor_S5d4c2.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B291_Refactor_S5d4c2.md) | 25 | 3793 | `d5556caf3e1face1e0448527695e980986be2e5fa3b82fdf1027d9541793e820` |
| [Specialization_B292_Refactor_S5d4c3.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B292_Refactor_S5d4c3.md) | 25 | 3866 | `5296e4041134ca5f4dc667e194e0d92ea9cec5596cf21f198d0197ccc6866a63` |
| [Specialization_B293_Refactor_S5d4c4.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B293_Refactor_S5d4c4.md) | 25 | 3441 | `0915fac290ed264bb39fa81bb57a703877de0e3a85718d125e0e026038c34ff4` |

**Deliberately retained in HEAD:** B273 S3 is still the Runtime_Index review source for `Mod/UI/TimedProjectSelection.lua`; B278 S5a2a is the review source for `Mod/LevelBannerState.lua`. B283, B285 and B287 retain directly useful event-namespace corrections, external signature evidence, pillage-owner/repair semantics and bounded native-log interpretation. They are not included merely to reach a file-count target.

**Dependency handling:** no runtime, test, tool, default-context or Runtime_Index input depends on these 15 reports. The follow-up plan now links their exact published versions; the seven Closure-history textual report locators use this recovery table. Only these 15 obsolete Context Lock entries are removed. Test sources, Closure originals/index, five retained reports, current rules and raw native evidence remain. The former proposal anchor is retained above for historical S1098 links. This is a document retirement, not a new validation or native-acceptance claim.

## Completed S5 and S6 local results in Git history

These 17 completed local-stage reports describe the former projection-health migration, transfer groundwork and shared-fact optimizations. They no longer drive current work; current Architecture, Status and versioned tests own present rules and results. Their local measurements, original failure examples and commands remain historical evidence at the fixed source, without creating new native acceptance or preserving obsolete next-step instructions as current tasks.

Original directory: `Specialization/Status/Validation/Results/`. All 17 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `e42caca061db9b50c3b3c869e1fe2fd1666220c1`. Recover with `git show e42caca061db9b50c3b3c869e1fe2fd1666220c1:Specialization/Status/Validation/Results/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Specialization_B294_Refactor_S5d4c5.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B294_Refactor_S5d4c5.md) | `15d206aa3bd2fd9e95cc5793352fd3961342785182b370567d107c5a827f8922` |
| [Specialization_B295_Refactor_S5d4c6.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B295_Refactor_S5d4c6.md) | `6e3f4581eccfb020b8c4c71ef461586cf96f1a7f44f1bf0594372ba674d7246b` |
| [Specialization_B296_Refactor_S5d4c7.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B296_Refactor_S5d4c7.md) | `4109ba982a8f2cdfd3d9f7a1e5e38fd73f52425f4370ebc044b9cc20f2850dbd` |
| [Specialization_B297_Refactor_S5d4c8.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B297_Refactor_S5d4c8.md) | `4a1f383a72941546f69710cf0110a18fd0f1c72fdfb9d7a053b892712f53baf0` |
| [Specialization_B298_Refactor_S5d4c9.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B298_Refactor_S5d4c9.md) | `e4b0dd6a40f512ca0fecc5af6fdad495bb94e950cd53fe5b3ea37ecff3ab28be` |
| [Specialization_B299_Refactor_S5d4c10.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B299_Refactor_S5d4c10.md) | `d78d47403d5b624a78bf6be5e78dff6452e0ebd188d1380d9bfc9fd2c34190c2` |
| [Specialization_B300_Refactor_S5d4c11.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B300_Refactor_S5d4c11.md) | `d3937230e1ff1df310b75c27e585f4555f5e3a0c486c076c43dc6b45a8f07c14` |
| [Specialization_B301_Refactor_S5d4d1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B301_Refactor_S5d4d1.md) | `792da6f8ae295fcf669d20e52aa9aeb76b416e6483daa815eb2094a2cdbf78f5` |
| [Specialization_B302_Refactor_S5d4d2.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B302_Refactor_S5d4d2.md) | `06b5df65b47d18da0c42c8d749b8282fda1aa4b3144342cbea9ded4b0ca9a816` |
| [Specialization_B303_Refactor_S6a.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B303_Refactor_S6a.md) | `098b32c6444d13fd3892ac49d1e09b78f00f879bab8c8a5a2d3880fcf4954ef2` |
| [Specialization_B304_Refactor_S6b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B304_Refactor_S6b.md) | `e895901a808547eaa41e26659e3d8f2c3c3cfba63f41cea43b8de8fa54aea358` |
| [Specialization_B305_Refactor_S6c.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B305_Refactor_S6c.md) | `0b6ea81850ecf3f8749ec934f7f57fb5234c872223f69a01e1d600309ca69c50` |
| [Specialization_B309_Refactor_S6e.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B309_Refactor_S6e.md) | `4d16614a4a65172fb8e79a9faebe6b5c376418dff073e47a382d2094a4149064` |
| [Specialization_B310_Refactor_S6f.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B310_Refactor_S6f.md) | `3be0783d68c47b500f53bd2b2cfaa990e7052645d2314c84feed4f4dd9d861d0` |
| [Specialization_B311_Refactor_S6g.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B311_Refactor_S6g.md) | `17f346ff1e849408eb0fad5461e329c29a86f2f1f9fc3a099f052f5f167b1321` |
| [Specialization_B312_Refactor_S6h.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B312_Refactor_S6h.md) | `0c200e2a85c5f5b22f234a986fc1ded68c3299d9e6fcefb61542094b4c99eba7` |
| [Specialization_B314_Refactor_S6j.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B314_Refactor_S6j.md) | `ca2285c8d3277f12798066aa7f9d4413305353b217ef958074526d14d4c2e386` |

No retired report is an input to production code, tests, tools, active context or Runtime_Index. The old follow-up schedule now targets exact published originals. B306 S6d and B313 S6i remain in HEAD because ReverseDependencies and InvestmentAction still use them as review provenance. All current proof, UNKNOWN/exit rules, original test assertions and raw native evidence are preserved.

## Completed S7 to S9 local results in Git history

These 58 completed pre-U5 implementation checkpoints have only local/static result status and no independent native acceptance. They describe superseded intermediate kernels, Store migration, UI transport, probes and recovery prototypes. Their original assertions, failed attempts, measurements, source/environment identities and then-open limits remain preserved at the exact historical source. Current Architecture/Status, actual versioned tests and subsequent accepted evidence own present rules and unresolved responsibilities; retirement neither closes an unknown nor revives these obsolete next-stage instructions.

Original directory: `Specialization/Status/Validation/Results/`. All 58 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `e42caca061db9b50c3b3c869e1fe2fd1666220c1`. Recover with `git show e42caca061db9b50c3b3c869e1fe2fd1666220c1:Specialization/Status/Validation/Results/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Specialization_B315_Refactor_S7a1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B315_Refactor_S7a1.md) | `b9b876b82fb0c52ec997a7b5907132df01c40f5582354d8703d04e2c8cb885a5` |
| [Specialization_B316_Refactor_S7a2.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B316_Refactor_S7a2.md) | `eba8e34b55d0ab52e60ab94102c8fee52f0cf4de33c3d6ca85b1bd83fa2a26df` |
| [Specialization_B317_Refactor_S7a3.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B317_Refactor_S7a3.md) | `98b5ec9b3be7671ed7569440c0aeeb2c7cee57240b5b242f331698bd492e6535` |
| [Specialization_B318_Refactor_S7a4.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B318_Refactor_S7a4.md) | `bc9af59624bf837e305d704a74e380e8c092887a10e4b496aea8f0e527319696` |
| [Specialization_B319_Refactor_S7a5.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B319_Refactor_S7a5.md) | `003babd54d68fb60a38c41abba10e98896cef8e8071da14bc3c57667a023b0db` |
| [Specialization_B324_Refactor_S7d1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B324_Refactor_S7d1.md) | `db21897aa133b4ea8ceb54efbfbc7381ad79ad78b085580224e3168448bd8d77` |
| [Specialization_B325_Refactor_S7d2.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B325_Refactor_S7d2.md) | `772e6142bfdd5a40340852d0d245faf74b2a92632a0b163ea7b70418e4d9e79f` |
| [Specialization_B326_Refactor_S7d3a.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B326_Refactor_S7d3a.md) | `7f662098d3fc1977159776c77f368dd82ae91f47f59d82157fdb890af2ab3dc0` |
| [Specialization_B327_Refactor_S7d3b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B327_Refactor_S7d3b.md) | `6eeb26b19af9b765e83f3f2109b33c5c49f2879388b4d3d99b32ab145ac226b8` |
| [Specialization_B332_Refactor_S8a.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B332_Refactor_S8a.md) | `cf981ddab2d77873c9da129fcca528b753255e5b0ac95b6f751065ea8999dfc6` |
| [Specialization_B333_Refactor_S8b1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B333_Refactor_S8b1.md) | `92365df3b39f22c7eab1774e29aba83a6654d632475d29b78832335d5bef57b4` |
| [Specialization_B334_Refactor_S8c1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B334_Refactor_S8c1.md) | `94c449d55101c5ec58889efa387469b49fb9e1f05eda0e6b6c1997de52f2cbbd` |
| [Specialization_B335_Refactor_S8c2.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B335_Refactor_S8c2.md) | `858a598acd37ee5d6e6447756f0e75c6899bb963e2a2de4ab965b13267e29fdc` |
| [Specialization_B336_Refactor_S8c3.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B336_Refactor_S8c3.md) | `bd16ce6617359314fa0a96f5f4c2eb23bef217f542c905478d9265690aa751a7` |
| [Specialization_B337_Refactor_S8c4.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B337_Refactor_S8c4.md) | `86ed80f0961171cbff6572b0c099cedf3dce1d6380e945757b37d9a2b7b4d5f8` |
| [Specialization_B338_Refactor_S8c5a.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B338_Refactor_S8c5a.md) | `a97245a6bd25ad76addf07cbd715173717cd70b3787396c191e5f72f3ba42352` |
| [Specialization_B340_Refactor_S8c5c.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B340_Refactor_S8c5c.md) | `055e35d0c7cc59aebdd24493d1e86b7ff68018fc55159d3e506cf0b0207dfff5` |
| [Specialization_B341_Refactor_S8b2.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B341_Refactor_S8b2.md) | `8004445610528e6df0e6c6021d463b64c6c7df38ea9e973af82e4cb55db743ec` |
| [Specialization_B342_Refactor_S8b3.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B342_Refactor_S8b3.md) | `55c3dbe2820aacd7a749044dd2ffd387cc3f3ff95f22802e5b7bf637817795b7` |
| [Specialization_B343_Refactor_S8b4.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B343_Refactor_S8b4.md) | `6024da8fd49570bbfb263d4594d856311620ac60ec08456e2f7ff9cab19ef1e8` |
| [Specialization_B344_Refactor_S8b5.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B344_Refactor_S8b5.md) | `ea9ce240af0746f628fb7b386b27de3c094ba03abfe2252d0362cc7cfbc42c5f` |
| [Specialization_B345_Refactor_S8b6.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B345_Refactor_S8b6.md) | `17b726120eefd9ba84ddfacfa024c51e2cbc406e942a5eeb32b29c3b664faa60` |
| [Specialization_B346_Refactor_S8b7a.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B346_Refactor_S8b7a.md) | `62f26362f22b74a7a20355eedfb9421f81ad11f2f858da65cbac49e26f2f02ab` |
| [Specialization_B347_Refactor_S8b7b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B347_Refactor_S8b7b.md) | `4f1c7549c8c8f5dfaff8ed6f66261b82e270794965ee118714a0c867983a9b93` |
| [Specialization_B349_Refactor_S9a1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B349_Refactor_S9a1.md) | `d0c6700f96fc4d9241896c3cae80d90ff3852d81e3f718ab48b75be7a6dc43a8` |
| [Specialization_B350_Refactor_S8b9.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B350_Refactor_S8b9.md) | `765b4628a84aae5e0bc0a87a0eca0fd12c65a5516ba0ebcff55ca2451bd2af58` |
| [Specialization_B351_Refactor_S8b10.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B351_Refactor_S8b10.md) | `f6b8db8e5a1b9318a7e41ceca259a9696a0b97940fb887eaa22473fd6092f243` |
| [Specialization_B354_Refactor_S9b2.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B354_Refactor_S9b2.md) | `e44070ca1677dd4d437ad7adc083f718d137c9650fc6044f7c330d6b7cbfa61a` |
| [Specialization_B356_Refactor_S9c1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B356_Refactor_S9c1.md) | `a7da0b414e39886e2ec7d94d548143c7a0b323fc1b9c0ec1c00a6e5c3a8b1c3b` |
| [Specialization_B357_Refactor_S9c2.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B357_Refactor_S9c2.md) | `ce9e3a37af2ca48701474596e6f18633a6e3426ed3bafd0dd9b9fc227942a44b` |
| [Specialization_B358_Refactor_S9c3.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B358_Refactor_S9c3.md) | `aeab5eaefed75337b5fe810196ed2f7b434eb3e2e2016175ad1d9b8c12b2e5b3` |
| [Specialization_B359_Refactor_S9c4a.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B359_Refactor_S9c4a.md) | `12bb5e04dbb10164c4a79f765fafbc8d4c106983611e7ff46bb03d83beb82203` |
| [Specialization_B360_Refactor_S9c4b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B360_Refactor_S9c4b.md) | `91085192dd1f64665b6923ab7a585ade148a4912cdca778617fe21e31f668c72` |
| [Specialization_B361_Refactor_S9c5a.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B361_Refactor_S9c5a.md) | `30fb3a3e813abd254d5dcc1a6dbaf8ba5e5c02a6496ed4d4edc9fab1d342dc8e` |
| [Specialization_B362_Refactor_S9c5b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B362_Refactor_S9c5b.md) | `ebddca2d6c2f29daa755a5b14b64e64dafbc28830200e7115d0cc7f0bd78ee74` |
| [Specialization_B364_Refactor_S9c6b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B364_Refactor_S9c6b.md) | `15c79ad1a634968934e2f7893526518aea55691d95d7131c31341dbff905ec12` |
| [Specialization_B365_Refactor_S9a3a.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B365_Refactor_S9a3a.md) | `344613641c9885e6fe65ae9ba89af539882c060ac600231677490fc5f63a0b01` |
| [Specialization_B366_Refactor_S9a3b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B366_Refactor_S9a3b.md) | `b192b6f48ec94b33bc955e54e5f0d30da99e1fce4058937952a77586451cb38b` |
| [Specialization_B367_Refactor_S9a3c.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B367_Refactor_S9a3c.md) | `960e35eda38a1e929622c19e304646be159266df8635e39972d923707cc9f9b4` |
| [Specialization_B368_Refactor_S9a3d.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B368_Refactor_S9a3d.md) | `6f3139c879829079075b933388d7601f82e9b21219d1894e91ec28d9ef943c50` |
| [Specialization_B369_Refactor_S9a3e.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B369_Refactor_S9a3e.md) | `12bcfcbf976db413047aee5f2ff0cd242786d56568aeae6d9dc356a8fc4fa06e` |
| [Specialization_B370_Refactor_S9d1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B370_Refactor_S9d1.md) | `0ee0057bd27c69ee55d55db9b93e202f65b623863827cf7654ff6e44306e0154` |
| [Specialization_B371_Refactor_S9d1b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B371_Refactor_S9d1b.md) | `cedb871fe7cadbffc0b563ee9989afe53d9e1aa8d80b98c12ae6c8f763027268` |
| [Specialization_B372_Refactor_S9e1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B372_Refactor_S9e1.md) | `90000974a1e95b092e3154298f493102ac77fb2455f3b27fe83e5fb3cb4a09e4` |
| [Specialization_B375_Refactor_S9e3.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B375_Refactor_S9e3.md) | `fe4255c03e47edb4351f8b4eda695592fcfa9a93dd08f44580463d63be1b6178` |
| [Specialization_B376_Refactor_S9e3b.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B376_Refactor_S9e3b.md) | `dd2a680e1ef34b7b0381dd48d60d6f6c90e0adfc8cd1d5ca7d457674d189beb4` |
| [Specialization_B377_Refactor_S9e4.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B377_Refactor_S9e4.md) | `f1f11e1fefa30c65f37dcd1b21e65d9c7cee7c1dbf8df1e66d5d92bd971db2c2` |
| [Specialization_B378_Refactor_S9e5.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B378_Refactor_S9e5.md) | `c6c62f0d9c8f29c2be903ed6179777f83aaec6298167e2ce99dbdedefb8860aa` |
| [Specialization_B379_Refactor_S9e6.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B379_Refactor_S9e6.md) | `1a4a8808882c4acc42f4977a3b2d82f79f10ed595974e48feb9910a9b17a4b3d` |
| [Specialization_B381_Refactor_S9e8.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B381_Refactor_S9e8.md) | `e4223c484f445af220876c68105552f33f8cc05b48bf78e727a12840687e8f04` |
| [Specialization_B383_Refactor_S9e10.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B383_Refactor_S9e10.md) | `bf771fb627fb8c915089fcabf6420435a28637543e05db195a863c06734f2513` |
| [Specialization_B384_Refactor_S9f1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B384_Refactor_S9f1.md) | `fcf0ddfead6273dd03281d8081e9ad940b06e214351eba0958ac90c8f5dbdbcc` |
| [Specialization_B386_Refactor_S9f3.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B386_Refactor_S9f3.md) | `ae4df8d2566dc3e016012075a4602c15152541a1fc8f7d65f5868e12ccb1dc9f` |
| [Specialization_B387_Refactor_S9f4.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B387_Refactor_S9f4.md) | `9c0e19fa21c9f105d84a3b3100f53568ac609a9d8d0d42d9c90b6e392bfc6a0b` |
| [Specialization_B388_Refactor_S9g1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B388_Refactor_S9g1.md) | `961a921a24f76d21ddece7883ea1ba72529afb71256e2638d9eb5f294728ad83` |
| [Specialization_B389_Refactor_S9g2.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B389_Refactor_S9g2.md) | `7415a1057c3c404233ba2d6daeecae74ee36cd111a0ee5452ebd5f3e03c3acfc` |
| [Specialization_B390_Refactor_S9g3.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B390_Refactor_S9g3.md) | `bd98c18356c7dfa36bc9e911e51927ae1618986794c90b757d2462719e4c6bd1` |
| [Specialization_B391_Refactor_S9g4.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/e42caca061db9b50c3b3c869e1fe2fd1666220c1/Specialization/Status/Validation/Results/Specialization_B391_Refactor_S9g4.md) | `c89919da1f42027fded35d570e11387d9b2e6c9a8659a8b479e8c3ef50b9cde0` |

No retired report is consumed by current runtime code, tests, tools, active context or Runtime_Index. Nineteen other S7–S9 reports remain because they are still actual Runtime_Index review sources. The old follow-up schedule and timed-project proposal now target exact published originals. One historical relative link in Specialization_B391_Develop_Deployment.md still names B391_Refactor_S9g4.md; use the fixed original in this table, without rewriting that frozen deployment result or claiming every old link resolves. The separate Refactor_S7d6_Crew_Proof_Gap.md, current Crew/Claim/Expedition boundaries, accepted rules and raw native evidence remain in HEAD.

## Prior audit scheduling and intake in Git history

The former Audit_Followup_Priorities record combines the B204/B249/B266 roadmap, B271-to-B391 implementation intake, initial defect dispositions, user decisions and Primary qualifications of Advisory proposals. It is a completed historical scheduling/publication record, not the current task queue. Current scheduling and authorization remain in Status/Authority; accepted rules and dependency-triggered review are in Design, Architecture and Workflow. Original Advisor source reports, U1 approval provenance, current unresolved boundaries and raw evidence remain. Retiring this old aggregate does not adopt rejected reconciliation proposals, declare every old finding solved, or change preserved user decisions.

Original directory: `Specialization/Reports/Proposals`. All 1 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `aa1aa7567c26076659cb3b6b9843780f1f753067`. Recover with `git show aa1aa7567c26076659cb3b6b9843780f1f753067:Specialization/Reports/Proposals/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Audit_Followup_Priorities.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/aa1aa7567c26076659cb3b6b9843780f1f753067/Specialization/Reports/Proposals/Audit_Followup_Priorities.md) | `9e99e426faf6b9e25ef6ac165471e2b6cd8f54b00e2282b01972b2f0681133aa` |

Five maintained navigation/preparation documents now link the immutable original (including original anchors); U1 and the recovery proposal also have explicit current-reading notes. Seven frozen documents retain historical relative locators: `Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/To_Be.md`; `Specialization/Status/Validation/Results/Specialization_B213_Expedition_Repair_Culture_UI.md`; `Specialization/Status/Validation/Results/Specialization_B226_Culture_Network.md`; `Specialization/Status/Validation/Results/Specialization_B250_UI_Copy_Polish.md`; `Specialization/Status/Validation/Results/Specialization_B267_Preplaytest_Diagnostics.md`; `Specialization/Status/Validation/Results/Specialization_V01_Alpha1_Promotion.md`; `Specialization/Status/Validation/Results/Specialization_V01_Playtest_Readiness_B266.md`. Use the fixed original above for those locators; their bodies and historical scope remain unchanged. No runtime, test, tool, active context or Runtime_Index uses the retired plan as a live input. This is not an all-history-link PASS.

## Completed early workspace migrations in Git history

These five completed 2026-09-11/12 organization and repository-migration artifacts no longer define the workspace. They include the original directory proposal, two delivery reports, the 539-entry copy inventory and the 35-move map. Their old role rules, not-yet-Git instructions, staged migration plans and counts are historical, superseded by current AGENTS/Workflow and the canonical repository. Original approval supplements, checks and path/hash mappings remain preserved in the fixed source; no migration or old test is replayed.

Original directory: `Specialization/Reports/Proposals`. All 5 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `8fbc08ad97b503ad500ed3009e3c1f7867b90cd0`. Recover with `git show 8fbc08ad97b503ad500ed3009e3c1f7867b90cd0:Specialization/Reports/Proposals/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Specialization_File_Structure_Proposal.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/8fbc08ad97b503ad500ed3009e3c1f7867b90cd0/Specialization/Reports/Proposals/Specialization_File_Structure_Proposal.md) | `43e33361051ad8590dca1a3f6a6bbd22c67619ddcbf9c12ef149ff76b0b4872d` |
| [Specialization_Repository_Phase1_Migration.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/8fbc08ad97b503ad500ed3009e3c1f7867b90cd0/Specialization/Reports/Proposals/Specialization_Repository_Phase1_Migration.md) | `c7e967b81365f0d6a717ed61f6402d8b657330d84638b7530670d2d77e8d12cf` |
| [Specialization_Phase1_Migration_Report.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/8fbc08ad97b503ad500ed3009e3c1f7867b90cd0/Specialization/Reports/Proposals/Specialization_Phase1_Migration_Report.md) | `fefca3584678179c5f790073bda09b5d5f395436629b6cfc4d9e996a7c24043e` |
| [Phase1_Copy_Manifest.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/8fbc08ad97b503ad500ed3009e3c1f7867b90cd0/Specialization/Reports/Proposals/Phase1_Copy_Manifest.json) | `db7b2294858747d5b8f905d8e02eb5d385d84c8ac6848daa223d44fac4ad319d` |
| [Phase1_Path_Map.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/8fbc08ad97b503ad500ed3009e3c1f7867b90cd0/Specialization/Reports/Proposals/Phase1_Path_Map.json) | `a3e948cfb5da97451da2f7ac49ffa2f1ab977c4d6a2d354da34bdae91c008ae0` |

Current runtime, tests, tools, active context and Runtime_Index do not consume these five artifacts. Historical navigation now targets their exact published versions. Phase1_External_Materials.md and Legacy_Workspace_Relocation.md remain directly available: the latter owns current access to relocated screenshots/raw evidence. The old 35-move map and copy inventory can still be consulted at the fixed source without maintaining them as current routing. External backups, raw files and original missing-evidence boundaries are untouched.

## Superseded discussions and delivered review inputs in Git history

These four completed inputs are the early route-source alternatives, the original Closure-storage discussion, the never-applied U1 text patch and the delivered B412/B413 external-review handoff. The background-source decision, accepted evidence-storage rules and final U1 choices have their current owners in existing Reference/Workflow/Design/Architecture; the handoff records its completed return and deployment. Their former pending approvals, unresolved draft alternatives and obsolete deployment/test instructions are not current tasks. Originals remain intact at the fixed source, including limits, failure examples, decisions and review scope; no new rule or native acceptance follows from retirement.

Original directory: `Specialization/Reports/Proposals`. All 4 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `2d130d9e7e4f20dae6a9e00c88d62933486e0c8c`. Recover with `git show 2d130d9e7e4f20dae6a9e00c88d62933486e0c8c:Specialization/Reports/Proposals/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Specialization_Network_Connection_Distribution_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/2d130d9e7e4f20dae6a9e00c88d62933486e0c8c/Specialization/Reports/Proposals/Specialization_Network_Connection_Distribution_Plan.md) | `92f1519da8728d7ed2b6b8062e01ede3cab8371ce9cd91b55ce612c54f4ede3d` |
| [Refactor_Closure_Storage_Proposal.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/2d130d9e7e4f20dae6a9e00c88d62933486e0c8c/Specialization/Reports/Proposals/Refactor_Closure_Storage_Proposal.md) | `378e6303905cc55d10da7f1a103dce61a78bb9f9776b4c8f261b0c319c243305` |
| [Pre_U5_External_Review_Handoff.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/2d130d9e7e4f20dae6a9e00c88d62933486e0c8c/Specialization/Reports/Proposals/Pre_U5_External_Review_Handoff.md) | `88ff9c5bd79ead08b0ab034eecace0bdacb3b55231ee4c3c3c571d443a14f05d` |
| [Refactor_Program_U1_Text.patch](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/2d130d9e7e4f20dae6a9e00c88d62933486e0c8c/Specialization/Reports/Proposals/Refactor_Program_U1_Text.patch) | `363e97561fade38679a48d62e1c6364fb47a34d175b31f72e8f2393c58814c35` |

No runtime, test, tool, active-context or Runtime_Index consumes these four inputs. The accepted U1 record now links its original patch at the fixed commit. Historical relative references remain in Specialization_B023_Auto_Constant_Lv1.md, Refactor_Closure_Storage_2026-10-24.md and the two B412/B413 handoff links in the S0896/S0898 Status history; use this table for exact replacement locators. Their frozen bodies are unchanged and no all-history-link PASS is claimed. The current background-source decision, 31-Closure retrieval index, evidence rules, Crew proof-gap record and native evidence remain in HEAD.

## Superseded preparation and initial Design review in Git history

These three completed inputs are the pre-assembly environment proposal, the source-attribution options sheet and the first D0001 draft review. The current Tier definition and explicit Owner exceptions are already in Shared D0060; the earlier environment candidate is not a current Tier table or a renewed fifth-tier approval request. Claim source option A has its delivered S0886 outcome and evidence limits, while option B remains unapproved. The initial D0001 pending status, draft OPEN numbering and source gaps describe that first review, not current Design. Original decisions, candidate alternatives, evidence identities and limitations remain intact in Git; retirement does not close an unresolved engine boundary or approve a new fallback.

Original directory: `Specialization/Reports/Proposals`. All 3 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `860fe6359ef98699dc75ab7dc5cdb84fb11d8207`. Recover with `git show 860fe6359ef98699dc75ab7dc5cdb84fb11d8207:Specialization/Reports/Proposals/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Environment_Assembly_Readiness.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/860fe6359ef98699dc75ab7dc5cdb84fb11d8207/Specialization/Reports/Proposals/Environment_Assembly_Readiness.md) | `85b9c453ad7984c24ec37c526019d8ed179bbe81bfac10d16705aff618310092` |
| [Claim_Completion_Recovery_Proposal.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/860fe6359ef98699dc75ab7dc5cdb84fb11d8207/Specialization/Reports/Proposals/Claim_Completion_Recovery_Proposal.md) | `5f54a1cdd98d8d192829d6650987b1b556e475b5c5f7e756f841ed9c20279d39` |
| [Specialization_D0001_Draft_Review.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/860fe6359ef98699dc75ab7dc5cdb84fb11d8207/Specialization/Reports/Proposals/Specialization_D0001_Draft_Review.md) | `b5e0fa14d4a9b25b6d7f654e58e8c758807fb15a18e789a98bf9d545a6b17b6b` |

No runtime, test, tool, active context or Runtime_Index consumes these three files. The Historical entry for the initial review now targets its exact original. The S0907 paragraph in Status and the historical s0907 P0-H proposal locator still name Environment_Assembly_Readiness.md; consult this table for the fixed original rather than rewriting that historical record. Current Shared Design, Engine Reference/source archives, S0886 attribution evidence and actual native acceptance remain available; no source DB, raw observation or accepted rule is deleted.

## Original Architecture v2 investigation in Git history

These eight B069/AV2-I001 documents are the original investigation plan, state/dependency/event maps, candidate findings, static validation and generated event/source indexes at e3651f9. They are historical source observations and proposed work, not current Architecture contracts or an outstanding implementation queue. The 298-row event list and 72-file hash index/56 source-excerpt blocks record source registration, not delivered native events or measured memory/CPU. Current Architecture, Runtime_Index and task-scoped source/evidence remain authoritative for their respective roles. The accepted Batch A–D2 technical contracts, Design and independent native evidence stay in HEAD; old risks are neither reopened nor declared solved by this retirement.

Exact original repository paths are listed below. All 8 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `98131a7a6dec32c50cdfb1ac39d8f95af42f19f3`. Recover with `git show 98131a7a6dec32c50cdfb1ac39d8f95af42f19f3:<original-path>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Specialization/Architecture/Architecture_v2_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/98131a7a6dec32c50cdfb1ac39d8f95af42f19f3/Specialization/Architecture/Architecture_v2_Plan.md) | `dc7f7df8b9ccee502b32c7cfc6ea37c5726dbde6e75df7e6ea3b4b5ca9a59366` |
| [Specialization/Architecture/v2/Source_Index.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/98131a7a6dec32c50cdfb1ac39d8f95af42f19f3/Specialization/Architecture/v2/Source_Index.md) | `62233a625206dbe7adf59ff63151979b0b9c6faedbaa11a66caa51b31bdbece8` |
| [Specialization/Architecture/v2/Event_Catalog.tsv](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/98131a7a6dec32c50cdfb1ac39d8f95af42f19f3/Specialization/Architecture/v2/Event_Catalog.tsv) | `3f585bbad8f6558434174e6f7cd14e7ea68c5b3ad12f8b9f6a98a8d01cbbd087` |
| [Specialization/Architecture/v2/State_Ownership_Save.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/98131a7a6dec32c50cdfb1ac39d8f95af42f19f3/Specialization/Architecture/v2/State_Ownership_Save.md) | `bc9501c135f3bdd85813453f03ff15025d3e1addcae7f0598f53342a68ef0314` |
| [Specialization/Architecture/v2/Events_Dirty.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/98131a7a6dec32c50cdfb1ac39d8f95af42f19f3/Specialization/Architecture/v2/Events_Dirty.md) | `2facd54c436e089e99aaf6d55246912d85abfea4f17ee1404cab5896c005e986` |
| [Specialization/Architecture/v2/Validation.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/98131a7a6dec32c50cdfb1ac39d8f95af42f19f3/Specialization/Architecture/v2/Validation.md) | `d34fc04ac92f9b2f18db4b297b4fc7107c8d8b95fdd9376575a39219d51a7e4f` |
| [Specialization/Architecture/v2/Findings_Batches.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/98131a7a6dec32c50cdfb1ac39d8f95af42f19f3/Specialization/Architecture/v2/Findings_Batches.md) | `c03b8d84d2b501562b3442ea2b337758a8a73668b499137fb49dba8fb5d0c26d` |
| [Specialization/Architecture/v2/Dependencies_Bridges.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/98131a7a6dec32c50cdfb1ac39d8f95af42f19f3/Specialization/Architecture/v2/Dependencies_Bridges.md) | `f74419ed4001c0174931d188e88eab015d948d314217f8a911688a59b7faa654` |

No runtime code, test, tool, active manifest projection or Runtime_Index review source consumes these eight files. Maintained v2 and Historical navigation now targets fixed originals. The D0032_Runtime_Inventory historical hash table retains seven textual locators and the frozen Direct_Event_Listener_Audit retains its baseline statement that Events_Dirty was historical-only; retrieve original context from this table. Original content/hashes and accepted contracts are preserved. The four retired path entries leave Authority.historical_only, while the existing Design/Revisions classification remains; no current authority source is replaced.
