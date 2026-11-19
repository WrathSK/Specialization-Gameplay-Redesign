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

No runtime code, test, tool, active manifest projection or Runtime_Index review source consumes these eight files. Maintained v2 and Historical navigation now targets fixed originals. The now-history-only [D0032 inventory](#d0032-static-adaptation-artifacts-in-git-history) retains seven textual locators and the frozen Direct_Event_Listener_Audit retains its baseline statement that Events_Dirty was historical-only; retrieve original context from this table. Original content/hashes and accepted contracts are preserved. The four retired path entries leave Authority.historical_only, while the existing Design/Revisions classification remains; no current authority source is replaced.

## D0032 static adaptation artifacts in Git history

These two completed A0160/D0032 static artifacts capture B076.103 source, not the current runtime: 121 file rows with hashes/anchors/manifest roles, 56 Design hashes, 16 older-v2 hashes, and the original planning-gate validation. They contain no independent native test or external database archive. Current technical contracts, source review and test/native evidence retain their own existing owners. Exact originals, recorded old checks and historical limitations remain intact; retirement does not reinterpret the original READY FOR P0-A result as current implementation or native acceptance.

Original directory: `Specialization/Architecture/v2`. All 2 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `28e257c4598ff1169444a13d1482acef40c6991c`. Recover with `git show 28e257c4598ff1169444a13d1482acef40c6991c:Specialization/Architecture/v2/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [D0032_Runtime_Inventory.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/28e257c4598ff1169444a13d1482acef40c6991c/Specialization/Architecture/v2/D0032_Runtime_Inventory.json) | `03ad69688b0bdd807964f77c0920cb562a8e5079c2584bc05bab1f409f63d6ce` |
| [D0032_Validation.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/28e257c4598ff1169444a13d1482acef40c6991c/Specialization/Architecture/v2/D0032_Validation.md) | `90df33b0aad4b6ac5f38630cb3bb15ca50ce797a70a0f921bdc987a91ae8094f` |

No runtime code, test, tool, active-context projection or Runtime_Index.files review_source consumes either artifact. Runtime_Index.historical_inventory is a historical locator only: it now targets the exact published original, while every current per-file hash/provenance/review_source and source/runtime identity field remains byte-equivalent. Maintained Architecture/v2/History references use the same fixed originals; one frozen S0201-era Status validation link retains its historical path and resolves through this table. D0032 adaptation, archaeology, implementation and spike contracts remain in HEAD, and raw evidence/backups are untouched.

## Original presentation carrier export in Git history

This completed PAC-I001/B076 database export groups 1,894 unique building definitions into 50 families (1,886 internal, four institutional candidates and four unclear mappings). It is a static loaded-configuration classification, not a current carrier registry, restore/withdrawal input, native effect test or permission to expose technical buildings. The accepted presentation-only institution principles remain in the maintained Model, current Architecture/Design and actual implementation. Original IDs, source/Mod commits, definition-list fingerprint and classification uncertainty remain exactly preserved in the published JSON.

Original directory: `Specialization/Architecture/v2`. All 1 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `1b086700da44a3cf5d8557ac339425a26f80b6ef`. Recover with `git show 1b086700da44a3cf5d8557ac339425a26f80b6ef:Specialization/Architecture/v2/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Presentation_Carrier_Inventory.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/1b086700da44a3cf5d8557ac339425a26f80b6ef/Specialization/Architecture/v2/Presentation_Carrier_Inventory.json) | `93187ff20ea6f54aeb71c0ffd4d541dbcd1c5b498fdd2760c16d88df7ab59004` |

No runtime, test, tool, active-context projection or current Runtime_Index review source consumes the export. The presentation Model and v2 index now link the fixed original. The Model explicitly limits its original NOT_STARTED header and inventory counts to the PAC/B076 checkpoint, while all PRES-001–007 rules and existing tables remain unchanged. No current per-file review evidence, source/runtime identity, native evidence, SQL definition or raw database archive is replaced or removed.

## Superseded early experiment steps in Git history

These six step sheets/placeholders are the old Governor/specialist and adjacency/route probes, B004/B006 route-test instructions, the initial four-target Crew experiment and its deferred-case wrapper. They do not supply independent current native acceptance. Their repeated result headers point to separately preserved user reports. The old NOT_IMPLEMENTED state and ordinary-building/district Crew targets are obsolete: current Industry Design permits only legal owned in-progress Wonders. Original expected outcomes, old skip/failure conditions and historical setup remain intact at the fixed source; they are not revived as current testing requirements.

Exact original repository paths are listed below. All 6 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `341165c5613e931d722f46d7c9284394491bef95`. Recover with `git show 341165c5613e931d722f46d7c9284394491bef95:<original-path>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Specialization/Historical/LegacyReports/Specialization_P0_Batch_A004.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/341165c5613e931d722f46d7c9284394491bef95/Specialization/Historical/LegacyReports/Specialization_P0_Batch_A004.md) | `3f1d19ea9b98d1888d7bf1306f5993cfe9e766540f56b7a7436daddd884c18e8` |
| [Specialization/Historical/LegacyReports/Specialization_P0_Batch_B001.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/341165c5613e931d722f46d7c9284394491bef95/Specialization/Historical/LegacyReports/Specialization_P0_Batch_B001.md) | `bd138f5abaad46c5221a83005b360a8ac1107b252b6a84e210c37369a3d6c99b` |
| [Specialization/Historical/LegacyReports/Specialization_P0_Batch_B004.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/341165c5613e931d722f46d7c9284394491bef95/Specialization/Historical/LegacyReports/Specialization_P0_Batch_B004.md) | `a080c395273a1210b56858dc1bf00ce36de4c4615073104c594edee23622139e` |
| [Specialization/Historical/LegacyReports/Specialization_P0_Batch_B006.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/341165c5613e931d722f46d7c9284394491bef95/Specialization/Historical/LegacyReports/Specialization_P0_Batch_B006.md) | `c1f1a3655b51a9ad1a6fa50e49653accd1703a7a87adcdba26321f6e26c47354` |
| [Specialization/Historical/LegacyReports/Specialization_P0_Deferred_Cases.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/341165c5613e931d722f46d7c9284394491bef95/Specialization/Historical/LegacyReports/Specialization_P0_Deferred_Cases.md) | `7a8c8e902ab29218592ccd38a70bf3b17de05b237ced21019f2dbb9d0a94bcb1` |
| [Specialization/Status/Validation/Cases/Deferred_Mechanics.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/341165c5613e931d722f46d7c9284394491bef95/Specialization/Status/Validation/Cases/Deferred_Mechanics.md) | `3f853d6f5189e143c2f21a591f414b96b1f11d3d1517bee89c518c51ed3a4827` |

No current code, test, tool, task manifest, active context or Runtime_Index review source consumes these six files. Deferred_Mechanics was an unreferenced placeholder and leaves with its old target; no new redirect is created. The frozen B006_Background_Routes report retains one bare Batch_B006 filename as a historical locator; consult this table. The original B005/B007/B008/B009 user result files, early failure reports, current Crew Design, modern scoped acceptance and native proof-gap records remain available. No previously unobserved boundary is marked passed.

## Superseded unit-action experiment cases in Git history

These four early case sheets describe free DEV injection, old map markers, a free 250-point Crew and fractional Quick-speed precision workflows at B039–B046. They are procedure inputs, not original user results. Current Industry rules restrict Crew to legal owned in-progress Wonders and use the accepted integer/floor/base-capacity policy; the old expected167.5/five initial costs do not become current criteria. Original instructions and failure/uncertainty conditions remain intact at the fixed source. Their retirement does not certify other game speeds, stacking combinations or native attribution.

Original directory: `Specialization/Status/Validation/Cases`. All 4 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `276598e86448a2c1f7b12ec43880e7395c2ec380`. Recover with `git show 276598e86448a2c1f7b12ec43880e7395c2ec380:Specialization/Status/Validation/Cases/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [B039_Construction_Injection.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/276598e86448a2c1f7b12ec43880e7395c2ec380/Specialization/Status/Validation/Cases/B039_Construction_Injection.md) | `365c0ca8392f30fc2d1de520dc16e5f7c0fc39ad257ce3a6b589e2d2fdcbdb1c` |
| [B041_Target_Markers.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/276598e86448a2c1f7b12ec43880e7395c2ec380/Specialization/Status/Validation/Cases/B041_Target_Markers.md) | `acd4c8211ad3de8bd761326f85ffb7a25e826e96dd1c9ea31ee6006eafdac73a` |
| [B042_Crew_And_Investment.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/276598e86448a2c1f7b12ec43880e7395c2ec380/Specialization/Status/Validation/Cases/B042_Crew_And_Investment.md) | `f7dc6aa66174da5d449dc6ffc5fd8d3535ee3b88b90122d5f4b743ddde326f35` |
| [B046_Crew_Precision.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/276598e86448a2c1f7b12ec43880e7395c2ec380/Specialization/Status/Validation/Cases/B046_Crew_Precision.md) | `7085b34d95d50f05dbc74c314ca1c0b1fcdc5bce364a733543052c17d8fa455f` |

No runtime, test, tool, task manifest, active context or per-file Runtime_Index review source consumes these case sheets. B046_Project_Precision retains one historical relative case link; retrieve its original through this table. The technical precision investigation, actual game-result originals, current native evidence and still-unknown speed/precision limits remain. No new player test or retrospective PASS is introduced.

## Retired task navigation snapshots and delivered repair plans in Git history

These 27 pinned W0001 task manifests (B079–B233) and three delivered Store/shared-D/investment repair plans are completed process history, not the active task. Several originals still say AWAITING_USER or contain old next-step instructions; preserving those original words does not reopen a task or turn an unobserved edge into PASS. Current Authority/P0-H, accepted Design/Architecture and the independently retained native/local results own current rules, work and evidence. These declarative snapshots contain no raw game logs, saves or database archives. No current Runtime_Index per-file review_source depends on them.

Exact original repository paths are listed below. All 30 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `7da41bcea04a0c17283b71e26c7c37e4d14df372`. Recover with `git show 7da41bcea04a0c17283b71e26c7c37e4d14df372:<original-path>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Specialization/Workflow/Investment-Propagation.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/Investment-Propagation.json) | `dc2783bae2c863f3c1371011542078270aa54a4a8bb96f0a2ba8ad268536c4af` |
| [Specialization/Workflow/P0-B1.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-B1.json) | `0ab4f4cbcd6ccc10d214ccf413a929e2bab1540e9c49217b57b424877dbfe45e` |
| [Specialization/Workflow/P0-B2.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-B2.json) | `96fcfa98f7de3137df6f418071aa62904d873fd9c4bcaffe72805f6e9503e6f3` |
| [Specialization/Workflow/P0-C.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-C.json) | `6ab50d871f768d5bc1eb5f3746d5fc04c58a92997083c7ea49233eca591bfd82` |
| [Specialization/Workflow/P0-D1.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-D1.json) | `e4884985fb64e3b4c9379748921b49901d7ee93b8ff08d83fdd2e07a89ad5ae1` |
| [Specialization/Workflow/P0-D2.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-D2.json) | `f5cbf71bbb0f92c6001543d032c5df781be307eb98b866e92afc85c444ad6c60` |
| [Specialization/Workflow/P0-D3.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-D3.json) | `0ecf597e8ab1fe5ed7a2601fda8e5eb0d3cdd63b22c9cc33cc2af159ff7fddd3` |
| [Specialization/Workflow/P0-E1.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-E1.json) | `c3eeefb822356defa9fc1efabd7bedebabb686247c4266c600bdf5d25e0b2d75` |
| [Specialization/Workflow/P0-E2.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-E2.json) | `1e7b54d36ae9e71f9b60e0d9644c4775d7bf9ece87d6b22f084f548bcc5ed486` |
| [Specialization/Workflow/P0-F1.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-F1.json) | `800e7ac89236df4dc15ef9ea4794a9e156c2ae91d1002c3a03090e5cf02edd86` |
| [Specialization/Workflow/P0-F2.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-F2.json) | `a245915f40bd094902dd24726b5f9ffdd1c705153e34d2964cdc67ddaa540611` |
| [Specialization/Workflow/P0-GH1.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-GH1.json) | `56633c47751cba8d0d20b1bc2d0e87cbd983399f2c43e77839843e37cc904dac` |
| [Specialization/Workflow/P0-K.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-K.json) | `ad7953a98aee21d16a92fd834c5104b739e1ba54cd980a0a81ed8875f7f1c42c` |
| [Specialization/Workflow/P0-L1.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-L1.json) | `48a49ae81d7b66cec6518d7a16989ac914b13f678939aac714b7585e38ae4527` |
| [Specialization/Workflow/P0-L2A.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-L2A.json) | `2672ad4f884394d991f66d81b1ff1155e1c965b305cf777682e21ffd7163cfc1` |
| [Specialization/Workflow/P0-L2B.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-L2B.json) | `926c796045cd9e6687fff4580b0bdd9796361e609581942c66fed47ed28a7475` |
| [Specialization/Workflow/P0-L2C.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-L2C.json) | `40aa6c8fddb51053f3c2aaa2b997fda70a53c4f1d61f78cd74372f938a50103b` |
| [Specialization/Workflow/P0-L3.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-L3.json) | `381e7db68176645911b8226a2171910f0a44f9615c5b23a986ea0c0e1af3a105` |
| [Specialization/Workflow/P0-L3A.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-L3A.json) | `834d63c12efe1e6ed4dc7235dea2ed1496edcbd4e68765147567ce58823a37a5` |
| [Specialization/Workflow/P0-M1.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-M1.json) | `fa81dfdc4aef46cb4c08772bee10e4fd3eb72d6d73584d993501c81972957767` |
| [Specialization/Workflow/P0-M2.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-M2.json) | `1b4803f24dfda2999999004b5cf8eccbf127f99dbf5618e5bf5e2a5a3ca4a97d` |
| [Specialization/Workflow/P0-M3.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-M3.json) | `af55ffe8fbc363740f7d7577bd37cb71c7235e6407d8594733c6a4e1d9f871f8` |
| [Specialization/Workflow/P0-N1.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-N1.json) | `46615756cd579e380ff420ab94d0983e1d10ae5af3b5c827322c5f838b05118d` |
| [Specialization/Workflow/P0-Panel-Cleanup.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-Panel-Cleanup.json) | `ba13ce7196445f13d8c274a23f113ff4dfea4c5771b4cf42e79b95eec1462545` |
| [Specialization/Workflow/P0-U1.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/P0-U1.json) | `1d49b6c02c504d52809cf821efe0b989d94c4dbdaaa183dd748495befb6b5a8b` |
| [Specialization/Workflow/Shared-D-Facts.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/Shared-D-Facts.json) | `83d049663b05c39da143625e69e005f4646e31f3bca7ec249bcf6ae22cd24ca8` |
| [Specialization/Workflow/Store-Write-Repair.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Workflow/Store-Write-Repair.json) | `00bf4ab7b86f318d14784d1c8f5df8345cc8e1a5f89ff332099c9966265d5fa9` |
| [Specialization/Reports/Proposals/Store_Write_Repair_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Reports/Proposals/Store_Write_Repair_Plan.md) | `4082e5a14dfd1ae7ac42cc69f440916048632640690396782cb3abf57cddc935` |
| [Specialization/Reports/Proposals/Shared_D_Fact_Read_Repair_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Reports/Proposals/Shared_D_Fact_Read_Repair_Plan.md) | `d89a1982800794846590d4534ff327152b3d6cfb23a7ec8e39a3753d619d738f` |
| [Specialization/Reports/Proposals/Investment_Update_Propagation_Repair_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/7da41bcea04a0c17283b71e26c7c37e4d14df372/Specialization/Reports/Proposals/Investment_Update_Propagation_Repair_Plan.md) | `8aea25e0cdd51f5a69662919dbd8ad08514cf8ff5ec6cfe7e480a46bdd83ba13` |

The current helper now exposes P0-H only and retains its schema, selector, version, branch, hash/file-set and review-source checks. Old task commands were already rejected as stale by those checks; they are not revived or silently redirected. To reproduce an old command, use the helper and manifest from the same frozen historical baseline, with that baseline's recorded external prerequisites. The generic helper tests use the current P0-H fixture instead of retired P0-E2, with assertions unchanged. Maintained v2/Workflow hyperlinks target exact originals. Frozen Dry_Run.md, P0-B2_Revalidation.md, the B169/B170/B174 local results, prior Status entries and P15/P12b/independent and Advisor audit records retain their old task filenames/links; this table supplies replacement locators, not a claim that every old relative link still resolves. The actual result files, scoped native acceptance, current remaining attribution/Expedition limits and raw archives remain directly available.

## Previous active-task manifest history in Git

The active P0-H file is kept as the current task entry, not a cumulative process archive. Its previous complete version contains 232 result entries and 168 validation notes (5,932 lines / 309,080 bytes), including completed architecture-convergence and subsequent cleanup work and obsolete stage dependencies. Those entries remain byte-exact in the published source below; no raw logs, native results, local artifacts or historical commits are removed. Current Authority/Status, accepted rules and the retained original evidence keep their responsibilities.

| Complete prior file (fixed published source) | SHA256 | Retrieval |
|---|---|---|
| [P0-H.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/4db9e56aa7b0776b84d2d29a3db75ca414a6bba7/Specialization/Workflow/P0-H.json) | `7a3eb1ccc7b22f379c3acaa6bccbde0d3afceecea18090eefd1394e46c40de08` | `git show 4db9e56aa7b0776b84d2d29a3db75ca414a6bba7:Specialization/Workflow/P0-H.json` |

The original was independently retrieved from GitHub and matched by bytes, Git blob and SHA256. Historical key names and their prior source/receipt/artifact locators remain available in that version. Current helper/schema and tests do not consume those old result keys; current reading uses the compact task context and explicit Status/evidence pointers. This does not promote local artifacts to permanent backups or change any native PASS/unknown scope.

## Delivered navigation and queue-repair preparation in Git history

The original W0001 B1 dry-run, B2 task revalidation, Phase1 external-location note and B398/B399 queue-repair proposal are completed process inputs. Their then-current environment/task pointers, pending approvals, planned tests and proposed modules no longer describe present work. The queued-project proposal also records historical Owner restrictions and fifth-playtest observations; these remain verbatim in the fixed original. Current Shared Design/Architecture, Status/Backlog and original native/local result files retain present rules and evidence. No native observation is deleted or upgraded.

Exact original repository paths are listed below. All 4 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `45643d575bb5df49e8847d58c3b9e1cbd8fc9951`. Recover with `git show 45643d575bb5df49e8847d58c3b9e1cbd8fc9951:<original-path>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Specialization/Workflow/Dry_Run.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/45643d575bb5df49e8847d58c3b9e1cbd8fc9951/Specialization/Workflow/Dry_Run.md) | `85c53f42735405bf0dd51c3ff93897142ef5cf9fe6d167652e3633da31dadb2d` |
| [Specialization/Workflow/P0-B2_Revalidation.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/45643d575bb5df49e8847d58c3b9e1cbd8fc9951/Specialization/Workflow/P0-B2_Revalidation.md) | `ce6b64d2439e5d5c26866d5cbe666bfb399f1b2eff54c981ea828ff928a8b3dc` |
| [Specialization/Reports/Proposals/Phase1_External_Materials.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/45643d575bb5df49e8847d58c3b9e1cbd8fc9951/Specialization/Reports/Proposals/Phase1_External_Materials.md) | `8b8ce81bf5f45921044b81f9d2ff3c6bb4f93c21920ccde209fd5733bc301b24` |
| [Specialization/Reports/Proposals/Timed_Project_Queue_Recovery_and_Remaining_Playtest.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/45643d575bb5df49e8847d58c3b9e1cbd8fc9951/Specialization/Reports/Proposals/Timed_Project_Queue_Recovery_and_Remaining_Playtest.md) | `af05c7d35c1cb835ef2a3c4b1743f585c95d19cdddf3cf05da1c61e2413ac86b` |

No Mod, test/tool, active context or current Runtime_Index per-file review_source consumes these four files. The v2 B2 review and project README background links now target fixed originals; the current legacy mapping remains local. The old Architecture portable-source note now points to that existing current mapping. Frozen B398/B399 results and historical Status/Backlog retain their original queue-plan/review filenames, anchors and period-specific claims; use this table for exact retrieval, not an assertion that all historical relative links still resolve. Earlier historical-index mentions of Dry_Run.md and P0-B2_Revalidation.md now refer to these fixed originals. The B1 proxy measurement is an old text-read experiment, not an actual token/CPU/native performance result. Old free-action/pending ownership/Crew restrictions do not replace accepted later results.

## Delivered early ability and presentation plans in Git history

These seven completed plans cover the original Lv2 Housing/GPP cutover, Research Infrastructure, Interdisciplinary Research, Applied Learning, Academic Chair, the first city-identity investigation and the institution presentation prototype. The retained implementation and native records cover their delivered scopes. The fixed plans preserve earlier qualification assumptions, proposed precision gates, candidate UI scope and exact limitations. Current Design/Architecture and Status govern any later work. The deferred Great Works era-coverage UI plan remains in the current tree.

Original directory: `Specialization/Architecture/v2`. All 7 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `6cfefeffc9a22fc8edd1ebfcbbca1065f9a46b71`. Recover with `git show 6cfefeffc9a22fc8edd1ebfcbbca1065f9a46b71:Specialization/Architecture/v2/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [P0_B2_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/6cfefeffc9a22fc8edd1ebfcbbca1065f9a46b71/Specialization/Architecture/v2/P0_B2_Plan.md) | `48c2f1915bae0aa71402652e6d093357078b39af1e90255d94c1835244f113cf` |
| [P0_C_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/6cfefeffc9a22fc8edd1ebfcbbca1065f9a46b71/Specialization/Architecture/v2/P0_C_Plan.md) | `632d56ef4827d3c4be9d8edc56683f751f9c4225d5908041293e837164941aa3` |
| [P0_D1_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/6cfefeffc9a22fc8edd1ebfcbbca1065f9a46b71/Specialization/Architecture/v2/P0_D1_Plan.md) | `8e0eade15be491a2c157b4e4f43e493bc2559e4039e31a0709120753da95d324` |
| [P0_D2_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/6cfefeffc9a22fc8edd1ebfcbbca1065f9a46b71/Specialization/Architecture/v2/P0_D2_Plan.md) | `ec46e4ce28acdd8991d2e14963ed090a3d8aa2442eaeb374153aad4e98ca64a1` |
| [P0_D3_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/6cfefeffc9a22fc8edd1ebfcbbca1065f9a46b71/Specialization/Architecture/v2/P0_D3_Plan.md) | `359a7cdb800b584097309b01ee68844caeab99b27df1868fa8489c857dd7f25f` |
| [P0_E1_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/6cfefeffc9a22fc8edd1ebfcbbca1065f9a46b71/Specialization/Architecture/v2/P0_E1_Plan.md) | `57366fd549921a017f3fec8524d695eeb749590d8bc9bd30215779d706f684e0` |
| [P0_U1_Plan.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/6cfefeffc9a22fc8edd1ebfcbbca1065f9a46b71/Specialization/Architecture/v2/P0_U1_Plan.md) | `3a6b8fe16aa9e4ef3a6e62ed0524723713e620875e37027ab21c64809fb5019c` |

The retained D0032 migration plan and v2 navigation link to the exact versions below. The original Research Infrastructure primitive-gate report and older Status entries retain period-specific references to the plan filenames; this table supplies their targets. B080/B081/B084–B088/B094 result and evidence files, current module provenance, the native precision evidence and accepted presentation contracts remain directly available.

## Early research candidates and probe procedures in Git history

The fixed originals cover the pre-D0015 HD Standardization catalog (167 rows, 17 excluded virtual candidates and 16 district replacements), the early ledger proposal, the D0013 remaining-work review, the early GW-002 BASE-adjacency proposal, the initial agent handoff, and the B010–B021 instructions for the original city, save and eligibility probes. The retained Design D0060 and Engine Reference explain effective-chain Tier and the present template inputs. The B052–B054 and GW primitive reports retain actual technical observations. The manual probes describe retired interfaces and their original environment.

Exact original repository paths are listed below. All 18 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `30f53c2f818574b424c6886e8da0c0976671e417`. Recover with `git show 30f53c2f818574b424c6886e8da0c0976671e417:<original-path>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [Specialization/Reports/Technical/Specialization_Standardization_Catalog_Candidate.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Reports/Technical/Specialization_Standardization_Catalog_Candidate.md) | `b309d72229b0f0ba2c138be8b5acdae5210e9c283a0ad3be1d454cfed70bce7f` |
| [Specialization/Reports/Technical/Specialization_Standardization_Catalog_Candidate.json](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Reports/Technical/Specialization_Standardization_Catalog_Candidate.json) | `aa3fed3cc936b5665b973f34ca67b7f46b5632838b8d6a6bb576b768e836d62e` |
| [Specialization/Reports/Technical/Specialization_Standardization_Storage_Research.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Reports/Technical/Specialization_Standardization_Storage_Research.md) | `bcb6dfc66edb8a0aac4887f1946c70e18cedcd0d55132016544131d2d45f3f1f` |
| [Specialization/Reports/Technical/Specialization_v01_Remaining_Work_Review.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Reports/Technical/Specialization_v01_Remaining_Work_Review.md) | `946afcdedde3b677205ec0695a1e4deca54755ff87ba6b91c88a70fe58c95dd5` |
| [Specialization/Reports/Technical/Specialization_GW002_Implementation_Preparation.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Reports/Technical/Specialization_GW002_Implementation_Preparation.md) | `972d12352d8dcfe03029903a01d0b95c81567cf13f148ca53187a9ea6634484e` |
| [Specialization/Reports/Technical/Specialization_Fresh_Agent_Handoff_Audit.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Reports/Technical/Specialization_Fresh_Agent_Handoff_Audit.md) | `a54dae910767b2e63b7b4d8ead7b9a91e2871530e74f899fd6d06633485918cc` |
| [Specialization/Status/Validation/Cases/B010_Deferred.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B010_Deferred.md) | `53330175f81e33cf857aea4a49b5d2fa41aa1a12cefdd888f22807aa85b576db` |
| [Specialization/Status/Validation/Cases/B011_Completion_Events.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B011_Completion_Events.md) | `14a7170bb860f5cdc15ebcf7c1f718914ffaea7ff4d43a832267aa427215105d` |
| [Specialization/Status/Validation/Cases/B012_Table_Storage.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B012_Table_Storage.md) | `46979f2102b3febef3d29ce20af522d1b0dad1fae202fb56596e1b75b61a6142` |
| [Specialization/Status/Validation/Cases/B013_New_City_Binding.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B013_New_City_Binding.md) | `9600c452f5a0c92aed1bb3a89c56dae607629d4ec0f77b3372d79df9fbd84354` |
| [Specialization/Status/Validation/Cases/B014_Completion_Record.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B014_Completion_Record.md) | `47c0ebd977e8ad664932eed81797c8f2fa4a078c8bf247fd1e7ad890ac56d56b` |
| [Specialization/Status/Validation/Cases/B015_City_Journal.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B015_City_Journal.md) | `e717e40c9e5d3c2e33844563ff24872558ea90c59821a704ab10ce6ed93e9667` |
| [Specialization/Status/Validation/Cases/B016_Eligibility.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B016_Eligibility.md) | `1af36ff9d4e523c415b343d994c32c2e2f6a9d7e304fb9de7538c91ddbaf010c` |
| [Specialization/Status/Validation/Cases/B017_Unknown_Slots.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B017_Unknown_Slots.md) | `54ba2dfdbb68019d2457fcc5918ffebc300aa3a348f33d85289fd0a36ae0f6be` |
| [Specialization/Status/Validation/Cases/B018_Runtime_Eligibility.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B018_Runtime_Eligibility.md) | `4296d7314c012d2d5a1e00b9c208fa7731b0190d3217e65f05965f8d774710a1` |
| [Specialization/Status/Validation/Cases/B019_Envelope_Recovery.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B019_Envelope_Recovery.md) | `30761e7ddb08ee1749891012e6d7a4f8e7e8b1d2b59ea1a907b98545e6a74fb4` |
| [Specialization/Status/Validation/Cases/B020_City_Flow.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B020_City_Flow.md) | `d3749e858887bcd13d53ffb5a627941488bd2e4f6b774570241f78dfee9eb2f5` |
| [Specialization/Status/Validation/Cases/B021_Normal_Load_Resume.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/30f53c2f818574b424c6886e8da0c0976671e417/Specialization/Status/Validation/Cases/B021_Normal_Load_Resume.md) | `bd98de4ded66b1372a2c6a1fca7ce0e6846a27101de707e8349ecffa26ea2915` |

All B011–B021 user results and corresponding local reports stay available. B010 remains an old deferred case with no recorded run in this instruction sheet. The original role-facts report, readback and load/failure evidence, datasets and raw archives retain their own scope. Prior Status, B012–B018 local results and B019–B021 technical reports preserve their old links; the table above supplies exact historical retrieval by path. The old two-file catalog can be opened from its pinned directory with original relative links. No active task, test, tool, mod or per-file Runtime_Index consumer requires the retired copies.

## Remaining early playtest procedures in Git history

These 25 source sheets describe manual playtest setups for B022–B051 experiments: specialist support and Great Person points, housing, early network and city totals, integer versus fractional effects, Settler/Crew controls and the old automatic copy abilities. Retained technical reports explain the actual primitives, measured outcomes and failures. The fixed sheets recover the original instructions, expected values and stop conditions. The current game uses the accepted four-profession rules and current interfaces.

Original directory: `Specialization/Status/Validation/Cases`. All 25 originals were independently retrieved from GitHub and matched by bytes, SHA256 and Git blob at published `c85c030b849e8278b14768d8e100071042e305ef`. Recover with `git show c85c030b849e8278b14768d8e100071042e305ef:Specialization/Status/Validation/Cases/<filename>`. Git history, test assertions and original failure details remain unchanged; local artifact hashes do not claim permanent raw-artifact preservation.

| Original report (fixed published source) | SHA256 |
|---|---|
| [B022_Research_Lv1_Yields.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B022_Research_Lv1_Yields.md) | `312d2e433e1a6ae3d8bc79d9138842105137b23f3a43b8cf51f91e41cdfd2427` |
| [B023_Automatic_Constant_Lv1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B023_Automatic_Constant_Lv1.md) | `7c4a8fd4f778f2707e6873f9cd657fe85718d6c2e216bf8fcb6429cc185adef6` |
| [B025_Background_Network.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B025_Background_Network.md) | `cfcebad3c1ac8ea551702fb4c18f579e1efcd596980ae69c47ca87c80ef8bb18` |
| [B027_Direct_Reception.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B027_Direct_Reception.md) | `15d3f0d34dd10c546918c5cf15b3908754645d29d47fa301555dc406ce4edf29` |
| [B028_Source_Totals.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B028_Source_Totals.md) | `99d0ebf020d81095064e2a12806ca734fd8955127b0ccdf6dc3f59ef44b4143e` |
| [B029_Fixed_Yield_Carrier.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B029_Fixed_Yield_Carrier.md) | `2a94ef4af004f78f52d1c2ea7fb2be327a96934ef6f64960e4204136d7ce27e7` |
| [B029_Fractional_Followup.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B029_Fractional_Followup.md) | `4726645542a090a25fd0ab541a024f7dac2db78826a775749ff2b1b579e71083` |
| [B029_New_Game_Control.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B029_New_Game_Control.md) | `29ea73dced41a04840b9bd28ddcf9417138338ed0199f81c888a1af9bf2393fe` |
| [B038_Lv3_Remaining.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B038_Lv3_Remaining.md) | `9bfabbcd4573180654363194cc841ce6fdb0d792d198384a2e4215ab459e3288` |
| [B038_Population_Diagnostic.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B038_Population_Diagnostic.md) | `b766dd5abf95f47c058713a8de4342229ab6ccaff34b8bf3464e705ed7bd4d24` |
| [B040_Unit_Sites.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B040_Unit_Sites.md) | `05c07a66764c47e046e84ac2ba40ad059f12c431dcfa8544873fa2efa29a6450` |
| [B043_Unit_Panel.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B043_Unit_Panel.md) | `e58a5af95ed951ac25d3f6143bfe10fda8725bbeacc269f104bb1b115fb1aef1` |
| [B044_Crew_Projects.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B044_Crew_Projects.md) | `0e83a8add92701a93abef9fc53cf5a652914cc69a8cc42af289e955fd1413a7b` |
| [B048_Lv4_Percent.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B048_Lv4_Percent.md) | `b4bfdad848794824fb2edb7b2d641019a1d1c01600f9470c10b95d2012ae5440` |
| [B049_Lv4_Copy_Basis.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B049_Lv4_Copy_Basis.md) | `e213d7612f0238bd0aa4a55d51359cdc90fec44a5dc583899a4180365087d30f` |
| [B050_Half_Yield.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B050_Half_Yield.md) | `389ba7c55dde7731ac0bab0805f787c0a22e55a402fe7eb4c336198042473d5f` |
| [B051_Automatic_Copy_Yields.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B051_Automatic_Copy_Yields.md) | `c3d2df285af7d2cfa3f8c0538bfd0ac194cde66111b9516e883cd02483ec4a80` |
| [B030_Precision_Control.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B030_Precision_Control.md) | `6856f4064824328f60b429865eb6c43c3309018599b2039cbf56c1a7773d8f21` |
| [B031_Network_Withdrawal.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B031_Network_Withdrawal.md) | `83c158798638a63b097c69a18ef093e1bdecf27aa16e54733d9a7385977d87cf` |
| [B033_Settler_Investment.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B033_Settler_Investment.md) | `fbec65ca3ea577ec6a8f30a121a0bc26bb54a06ef147708bcadd8da5180f5d3a` |
| [B034_Lv2_Housing.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B034_Lv2_Housing.md) | `1c16e6adeb017d80cdfe9cc01e2ca40333ee681be60a2cd86d075cd78aaa6745` |
| [B035_Four_Family_GPP.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B035_Four_Family_GPP.md) | `ab996a3e3847510f85362c2319ec89b0460d767b6b946233f5b3869c528b09af` |
| [B035_Lv2_GPP.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B035_Lv2_GPP.md) | `fad4bdde8b48af47f3db737fc84c330a20872fdeea503941ce85bb7edc6a600a` |
| [B036_Industry_Lv1.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B036_Industry_Lv1.md) | `66c0067def4aa0cd63d2c9ba1a53f4d323e9d25071e884bf893440fa0ddca839` |
| [B037_Lv3_Support.md](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/c85c030b849e8278b14768d8e100071042e305ef/Specialization/Status/Validation/Cases/B037_Lv3_Support.md) | `9d88da74cca434ee39da13a12e665082e890dba554291e855a2a1d04f660b113` |

The only remaining references are in dated technical/local or native evidence and one Advisory roadmap. Their original references still identify the files listed here. The B034 new-files list and the B035 case checksum remain frozen; the B035 checksum independently matches the historical original below. The older first-pass eligibility, construction capacity and native rate assumptions retain their original scope. This closes retirement of the procedure-only Cases directory on develop while preserving Results, technical evidence, local fixtures, playtest backlog and current evidence routes.
