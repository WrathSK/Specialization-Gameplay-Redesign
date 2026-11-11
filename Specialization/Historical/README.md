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

## Early README and AGENTS snapshots in Git history

The 13 early README and 13 AGENTS snapshots are available in the [original snapshots directory](https://github.com/WrathSK/Specialization-Gameplay-Redesign/tree/1c0b97fdd62ead58e1580c6b274614f6e0d02280/Specialization/Historical/DocumentSnapshots) at commit `1c0b97fdd62ead58e1580c6b274614f6e0d02280`. All 26 files were retrieved from GitHub and matched by SHA256.

The retained `Phase1_before_README.md` refers to the pre-migration navigation. Follow its earlier README citation to [the original file](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/1c0b97fdd62ead58e1580c6b274614f6e0d02280/Specialization/Historical/DocumentSnapshots/README_before_fresh_agent_handoff.md). The [Phase 1 copy manifest](../Reports/Proposals/Phase1_Copy_Manifest.json) retains the original migration inventory.

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
