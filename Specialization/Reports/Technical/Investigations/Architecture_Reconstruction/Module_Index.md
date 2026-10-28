# Module Index

Investigation / Non-authoritative / No design decision implied

Status: Stable
Owner: Architecture Modules investigation subtask; writes pause for Primary review.
Basis: develop `19d4669d11df945afcda9d73329dfb984fe8c694`；B393.420 / D0058 / A0183 / S0850。

This is a complete static inventory of **218 packaged Lua files**, matching the on-disk `Mod/**/*.lua` set. Entries are deduplicated from the modinfo `Files` section. Inventory is not a function-level audit. Groups are report navigation identifiers, not a new Architecture, migration plan or authoritative ownership ruling. SQL is M14.

## Evidence depth and activation legend

- **T**: targeted startup, call, read or write excerpts were traced; this is still not an exhaustive file/path review.
- **I**: packaging, literal include and entry symbol inventory only; no claim of ability correctness, execution reachability or complete save recovery.
- **GP**: referenced by an explicit composition registration in `Gameplay.lua` (include/definition or Start); a failed prerequisite may skip it.
- **UI**: same-stem Lua for a modinfo AddUserInterfaces XML, or a ReplaceUIScript entry; declared engine loading root, not verified in-game.
- **IN**: statically reachable from GP/UI roots through literal includes, including conditional/retired branches; not proof of execution.
- **PKG**: packaged but not reached in the literal include graph; dynamic callers are not ruled out.
- **R**: explicit retired startup option/flag; retained library, reader or cleanup functions do not establish an active production effect writer.

## Group directory

| ID | Logical family | Lua files |
|---|---|---:|
| M01 | Startup and shared tools | 6 |
| M02 | Identity, permanent Store, restructuring and lifecycle | 19 |
| M03 | Facts, invalidation and native sampling | 12 |
| M04 | Network bridge and recovery evidence | 10 |
| M05 | Shared levels and carrier effects | 16 |
| M06 | Research | 14 |
| M07 | Culture, Great Works and Dialogue | 24 |
| M08 | Commerce, Capital and Development | 18 |
| M09 | Industry, Standardization and Engineering | 11 |
| M10 | Timed projects, crew and unit actions | 25 |
| M11 | Culture expedition and spy | 19 |
| M12 | General UI presentation and readers | 12 |
| M13 | Diagnostics, experiments and audit | 32 |
| M14 | Declarative SQL | 0 |

## Complete packaged Lua mapping

Each source link points to the file first line; GP evidence additionally links the actual `composition.Run` line. At most two function declaration symbols are extracted per file; an empty cell means none extracted, not absence of interfaces.

| File / fixed source evidence | Group | Depth | Declared activation | Extracted symbols (not complete API) |
|---|---|---|---|---|
| [BindingProbe.lua](../../../../../Mod/BindingProbe.lua#L1) | M13 | I | GP ([Run:849](../../../../../Mod/Gameplay.lua#L849)) | `SPCBindingProbe.Start`, `key` |
| [BoostConfig.lua](../../../../../Mod/BoostConfig.lua#L1) | M05 | I | IN |  |
| [BoostIntegerConfig.lua](../../../../../Mod/BoostIntegerConfig.lua#L1) | M05 | I | IN |  |
| [CapitalInvestment.lua](../../../../../Mod/CapitalInvestment.lua#L1) | M08 | I | GP ([Run:976](../../../../../Mod/Gameplay.lua#L976)) | `SPCCapitalInvestment.Start`, `emit` |
| [CapitalInvestmentDiagnostics.lua](../../../../../Mod/CapitalInvestmentDiagnostics.lua#L1) | M08 | I | IN | `field`, `finite` |
| [CapitalInvestmentModel.lua](../../../../../Mod/CapitalInvestmentModel.lua#L1) | M08 | I | IN | `copy`, `M.Same` |
| [CarrierHealthTrace.lua](../../../../../Mod/CarrierHealthTrace.lua#L1) | M13 | I | GP ([Run:883](../../../../../Mod/Gameplay.lua#L883)) | `SPCCarrierHealthTrace.Start`, `read` |
| [CarrierSet.lua](../../../../../Mod/CarrierSet.lua#L1) | M05 | I | IN | `SPCCarrierSet.Registry`, `registry.Owns` |
| [CityFlowProbe.lua](../../../../../Mod/CityFlowProbe.lua#L1) | M03 | I | GP ([Run:861](../../../../../Mod/Gameplay.lua#L861)) | `SPCCityFlowProbe.Start`, `clone` |
| [CityIdentityExperiment.lua](../../../../../Mod/CityIdentityExperiment.lua#L1) | M02 | I | GP ([Run:989](../../../../../Mod/Gameplay.lua#L989)) | `SPCCityIdentityExperiment.Shadow`, `held` |
| [CityIdentityMapping.lua](../../../../../Mod/CityIdentityMapping.lua#L1) | M02 | I | GP ([Run:989](../../../../../Mod/Gameplay.lua#L989)) | `SPCCityIdentityMapping.Start`, `same` |
| [CityIdentityRead.lua](../../../../../Mod/CityIdentityRead.lua#L1) | M02 | I | GP ([Run:820](../../../../../Mod/Gameplay.lua#L820)) | `int`, `M.Copy` |
| [CityInheritance.lua](../../../../../Mod/CityInheritance.lua#L1) | M02 | I | PKG | `SPCCityInheritance.Start`, `cp` |
| [CityInheritanceRead.lua](../../../../../Mod/CityInheritanceRead.lua#L1) | M02 | I | PKG | `SPCCityInheritanceRead.Start`, `copy` |
| [CityJournalProbe.lua](../../../../../Mod/CityJournalProbe.lua#L1) | M13 | I | GP ([Run:853](../../../../../Mod/Gameplay.lua#L853)) | `SPCCityJournalProbe.Start`, `bucket` |
| [CityProgressionStore.lua](../../../../../Mod/CityProgressionStore.lua#L1) | M02 | T | GP ([Run:838](../../../../../Mod/Gameplay.lua#L838)) | `publishFact`, `CreateProgressionRecord` |
| [CityReference.lua](../../../../../Mod/CityReference.lua#L1) | M02 | I | IN | `integer`, `native` |
| [CitySequenceProbe.lua](../../../../../Mod/CitySequenceProbe.lua#L1) | M13 | I | GP ([Run:822](../../../../../Mod/Gameplay.lua#L822)) | `SPCCitySequenceProbe.Start`, `number` |
| [ClaimProjects.lua](../../../../../Mod/ClaimProjects.lua#L1) | M10 | I | GP ([Run:962](../../../../../Mod/Gameplay.lua#L962)) | `SPCClaimProjects.Start`, `d.IsBusy` |
| [Commerce.lua](../../../../../Mod/Commerce.lua#L1) | M08 | T | GP ([Run:972](../../../../../Mod/Gameplay.lua#L972)) | `M.Start`, `key` |
| [CommerceCalculation.lua](../../../../../Mod/CommerceCalculation.lua#L1) | M08 | I | IN | `finite`, `M.Layout` |
| [CommerceConvergence.lua](../../../../../Mod/CommerceConvergence.lua#L1) | M08 | T | GP / R ([Run:949](../../../../../Mod/Gameplay.lua#L949)) | `SPCCommerceConvergence.Start`, `d.Withdraw` |
| [CommerceModel.lua](../../../../../Mod/CommerceModel.lua#L1) | M08 | I | IN | `copy`, `int` |
| [CompletionProbe.lua](../../../../../Mod/CompletionProbe.lua#L1) | M13 | I | GP ([Run:816](../../../../../Mod/Gameplay.lua#L816)) | `SPCCompletionProbe.Start`, `scalar` |
| [CompletionRecordProbe.lua](../../../../../Mod/CompletionRecordProbe.lua#L1) | M13 | I | GP ([Run:851](../../../../../Mod/Gameplay.lua#L851)) | `SPCCompletionRecordProbe.Start`, `bucket` |
| [ConstructionProbe.lua](../../../../../Mod/ConstructionProbe.lua#L1) | M13 | I | GP ([Run:893](../../../../../Mod/Gameplay.lua#L893)) | `SPCConstructionProbe.Start`, `key` |
| [CopyYields.lua](../../../../../Mod/CopyYields.lua#L1) | M05 | I | GP / R ([Run:919](../../../../../Mod/Gameplay.lua#L919)) | `SPCCopyYields.Plan`, `SPCCopyYields.Start` |
| [CrewModel.lua](../../../../../Mod/CrewModel.lua#L1) | M10 | I | IN | `M.Copy`, `M.Same` |
| [CrewPrecision.lua](../../../../../Mod/CrewPrecision.lua#L1) | M10 | I | GP ([Run:905](../../../../../Mod/Gameplay.lua#L905)) | `SPCCrewPrecision.Start`, `before` |
| [CrewProjects.lua](../../../../../Mod/CrewProjects.lua#L1) | M10 | I | GP ([Run:901](../../../../../Mod/Gameplay.lua#L901)) | `SPCCrewProjects.Start`, `key` |
| [CultureAesthetic.lua](../../../../../Mod/CultureAesthetic.lua#L1) | M07 | I | GP ([Run:937](../../../../../Mod/Gameplay.lua#L937)) | `same`, `M.Start` |
| [CultureAestheticModel.lua](../../../../../Mod/CultureAestheticModel.lua#L1) | M07 | I | IN | `integer`, `M.Plan` |
| [CultureInsightsTourism.lua](../../../../../Mod/CultureInsightsTourism.lua#L1) | M07 | I | GP ([Run:1003](../../../../../Mod/Gameplay.lua#L1003)) | `M.Plan`, `M.Start` |
| [CultureInspiration.lua](../../../../../Mod/CultureInspiration.lua#L1) | M07 | I | GP ([Run:947](../../../../../Mod/Gameplay.lua#L947)) | `SPCCultureInspiration.Start`, `d.IsOwnedCarrier` |
| [CultureInspirationModel.lua](../../../../../Mod/CultureInspirationModel.lua#L1) | M07 | I | IN | `integer`, `M.Plan` |
| [CultureInspirationProbe.lua](../../../../../Mod/CultureInspirationProbe.lua#L1) | M07 | I | GP / R ([Run:945](../../../../../Mod/Gameplay.lua#L945)) | `SPCCultureInspirationProbe.Start`, `tr` |
| [CultureMeaning.lua](../../../../../Mod/CultureMeaning.lua#L1) | M07 | I | GP ([Run:943](../../../../../Mod/Gameplay.lua#L943)) | `SPCCultureMeaning.Start`, `d.IsOwnedCarrier` |
| [CultureMeaningModel.lua](../../../../../Mod/CultureMeaningModel.lua#L1) | M07 | I | IN | `M.RecipientCoverage`, `integer` |
| [CultureMeaningProbe.lua](../../../../../Mod/CultureMeaningProbe.lua#L1) | M07 | I | PKG | `SPCCultureMeaningProbe.Start`, `d.IsOwnedCarrier` |
| [CultureNetwork.lua](../../../../../Mod/CultureNetwork.lua#L1) | M07 | T | GP ([Run:1005](../../../../../Mod/Gameplay.lua#L1005)) | `name`, `int` |
| [CurrentSpecializationFacts.lua](../../../../../Mod/CurrentSpecializationFacts.lua#L1) | M03 | I | GP ([Run:871](../../../../../Mod/Gameplay.lua#L871)) | `SPCCurrentSpecializationFacts.Read`, `SPCCurrentSpecializationFacts.Inspect` |
| [DevelopmentInvestment.lua](../../../../../Mod/DevelopmentInvestment.lua#L1) | M08 | I | GP ([Run:978](../../../../../Mod/Gameplay.lua#L978)) | `SPCDevelopmentInvestment.Start`, `emit` |
| [DevelopmentInvestmentCatalog.lua](../../../../../Mod/DevelopmentInvestmentCatalog.lua#L1) | M08 | I | IN | `SPCDevelopmentInvestmentCatalog.Build` |
| [DevelopmentInvestmentModel.lua](../../../../../Mod/DevelopmentInvestmentModel.lua#L1) | M08 | I | IN | `int`, `ref` |
| [DevelopmentInvestmentTargets.lua](../../../../../Mod/DevelopmentInvestmentTargets.lua#L1) | M08 | I | IN | `M.Candidates`, `M.Options` |
| [DiagnosticLog.lua](../../../../../Mod/DiagnosticLog.lua#L1) | M13 | I | IN | `SPCDiagnosticLog.For` |
| [Dialogue.lua](../../../../../Mod/Dialogue.lua#L1) | M07 | I | GP / R ([Run:939](../../../../../Mod/Gameplay.lua#L939)) | `SPCDialogue.Start`, `set` |
| [DialogueEffects.lua](../../../../../Mod/DialogueEffects.lua#L1) | M07 | I | GP ([Run:985](../../../../../Mod/Gameplay.lua#L985)) | `SPCDialogueEffects.Start`, `d.IsOwnedCarrier` |
| [DialogueModel.lua](../../../../../Mod/DialogueModel.lua#L1) | M07 | I | IN | `SPCDialogueModel.Plan`, `SPCDialogueModel.Collect` |
| [DialogueProjectModel.lua](../../../../../Mod/DialogueProjectModel.lua#L1) | M07 | I | IN | `copy`, `integer` |
| [DialogueProjects.lua](../../../../../Mod/DialogueProjects.lua#L1) | M07 | I | GP ([Run:980](../../../../../Mod/Gameplay.lua#L980)) | `SPCDialogueProjects.Start`, `key` |
| [DistrictCompleteness.lua](../../../../../Mod/DistrictCompleteness.lua#L1) | M03 | I | GP ([Run:871](../../../../../Mod/Gameplay.lua#L871)) | `clone`, `same` |
| [DistrictPrecisionProbe.lua](../../../../../Mod/DistrictPrecisionProbe.lua#L1) | M13 | I | PKG | `M.Error`, `M.Start` |
| [DistrictPrecisionRead.lua](../../../../../Mod/DistrictPrecisionRead.lua#L1) | M13 | I | PKG | `number`, `SPCDistrictPrecisionRead.Render` |
| [EffectiveFacts.lua](../../../../../Mod/EffectiveFacts.lua#L1) | M03 | I | GP ([Run:863](../../../../../Mod/Gameplay.lua#L863)) | `SPCEffectiveFacts.Start`, `clone` |
| [EligibilityProbe.lua](../../../../../Mod/EligibilityProbe.lua#L1) | M13 | I | GP ([Run:855](../../../../../Mod/Gameplay.lua#L855)) | `SPCEligibilityProbe.Start`, `read` |
| [EngineeringStudyModel.lua](../../../../../Mod/EngineeringStudyModel.lua#L1) | M09 | I | IN | `copy`, `int` |
| [EngineeringStudyProjects.lua](../../../../../Mod/EngineeringStudyProjects.lua#L1) | M09 | I | GP ([Run:966](../../../../../Mod/Gameplay.lua#L966)) | `SPCEngineeringStudyProjects.Start`, `key` |
| [EnvelopeProbe.lua](../../../../../Mod/EnvelopeProbe.lua#L1) | M13 | I | GP ([Run:859](../../../../../Mod/Gameplay.lua#L859)) | `equal`, `M.Expected` |
| [EventTimingDiagnostics.lua](../../../../../Mod/EventTimingDiagnostics.lua#L1) | M13 | I | IN | `safeRead`, `state` |
| [ExpeditionEntry.lua](../../../../../Mod/ExpeditionEntry.lua#L1) | M11 | I | IN | `SPCExpeditionEntry.Select`, `integer` |
| [ExpeditionGate.lua](../../../../../Mod/ExpeditionGate.lua#L1) | M11 | I | PKG | `SPCExpeditionGate.Start`, `int` |
| [ExpeditionGateRead.lua](../../../../../Mod/ExpeditionGateRead.lua#L1) | M11 | I | PKG | `integer`, `call` |
| [ExpeditionMovementProbe.lua](../../../../../Mod/ExpeditionMovementProbe.lua#L1) | M11 | I | PKG | `SPCExpeditionMovementProbe.Start`, `integer` |
| [ExpeditionSpyGate.lua](../../../../../Mod/ExpeditionSpyGate.lua#L1) | M11 | I | GP ([Run:1007](../../../../../Mod/Gameplay.lua#L1007)) | `SPCExpeditionSpyGate.Start`, `unitCapacityChanged` |
| [ExpeditionSpyRead.lua](../../../../../Mod/ExpeditionSpyRead.lua#L1) | M11 | I | IN | `integer`, `call` |
| [ExpeditionSpyStore.lua](../../../../../Mod/ExpeditionSpyStore.lua#L1) | M11 | I | GP ([Run:1007](../../../../../Mod/Gameplay.lua#L1007)) | `integer`, `plain` |
| [ExpeditionSpyUI.lua](../../../../../Mod/ExpeditionSpyUI.lua#L1) | M11 | I | IN | `M.IsTeam`, `M.ByID` |
| [ExpeditionTraining.lua](../../../../../Mod/ExpeditionTraining.lua#L1) | M11 | I | GP ([Run:1009](../../../../../Mod/Gameplay.lua#L1009)) | `SPCExpeditionTraining.Start`, `observe` |
| [ExpeditionTrainingDiagnostics.lua](../../../../../Mod/ExpeditionTrainingDiagnostics.lua#L1) | M11 | I | IN | `scalar`, `M.Failure` |
| [FactChanges.lua](../../../../../Mod/FactChanges.lua#L1) | M03 | I | IN | `token`, `integer` |
| [FactConsumerBindings.lua](../../../../../Mod/FactConsumerBindings.lua#L1) | M03 | T | GP ([Run:1016](../../../../../Mod/Gameplay.lua#L1016)) | `SPCFactConsumerBindings.New`, `target` |
| [FreshBindingHook.lua](../../../../../Mod/FreshBindingHook.lua#L1) | M03 | I | GP ([Run:861](../../../../../Mod/Gameplay.lua#L861)) | `M.Install`, `verify` |
| [GPPReadout.lua](../../../../../Mod/GPPReadout.lua#L1) | M05 | I | IN | `SPCGPPReadout.Render` |
| [Gameplay.lua](../../../../../Mod/Gameplay.lua#L1) | M01 | T | IN | `stage`, `refreshInvestmentSupport` |
| [GreatWorkAdjacency.lua](../../../../../Mod/GreatWorkAdjacency.lua#L1) | M07 | I | GP / R ([Run:941](../../../../../Mod/Gameplay.lua#L941)) | `SPCGWAdjacency.Start`, `key` |
| [GreatWorkAdjacencyModel.lua](../../../../../Mod/GreatWorkAdjacencyModel.lua#L1) | M07 | I | IN | `M.Parts`, `M.Collect` |
| [GreatWorkCatalog.lua](../../../../../Mod/GreatWorkCatalog.lua#L1) | M07 | I | IN | `C.Resolve`, `C.Build` |
| [GreatWorkFacts.lua](../../../../../Mod/GreatWorkFacts.lua#L1) | M07 | I | GP ([Run:935](../../../../../Mod/Gameplay.lua#L935)) | `F.Hex`, `F.Unhex` |
| [GreatWorkProbe.lua](../../../../../Mod/GreatWorkProbe.lua#L1) | M07 | I | GP ([Run:933](../../../../../Mod/Gameplay.lua#L933)) | `SPCGreatWorkProbe.Start`, `set` |
| [HalfYieldProbe.lua](../../../../../Mod/HalfYieldProbe.lua#L1) | M13 | T | GP / R ([Run:917](../../../../../Mod/Gameplay.lua#L917)) | `SPCHalfYieldProbe.Plan`, `SPCHalfYieldProbe.Start` |
| [IdentityEqual.lua](../../../../../Mod/IdentityEqual.lua#L1) | M01 | I | IN | `SPCIdentityEqual.Same` |
| [IndustryHistory.lua](../../../../../Mod/IndustryHistory.lua#L1) | M09 | I | GP ([Run:921](../../../../../Mod/Gameplay.lua#L921)) | `SPCIndustryHistory.Start`, `int` |
| [IndustrySupport.lua](../../../../../Mod/IndustrySupport.lua#L1) | M09 | I | GP ([Run:887](../../../../../Mod/Gameplay.lua#L887)) | `SPCIndustrySupport.Start`, `key` |
| [IndustryWonderEffects.lua](../../../../../Mod/IndustryWonderEffects.lua#L1) | M09 | I | GP ([Run:968](../../../../../Mod/Gameplay.lua#L968)) | `SPCIndustryWonderEffects.Start`, `key` |
| [InheritanceShadow.lua](../../../../../Mod/InheritanceShadow.lua#L1) | M02 | I | PKG | `SPCInheritanceShadow.Start`, `cp` |
| [InspirationReadout.lua](../../../../../Mod/InspirationReadout.lua#L1) | M06 | I | IN | `tr`, `finite` |
| [InstitutionPresentation.lua](../../../../../Mod/InstitutionPresentation.lua#L1) | M13 | I | IN | `M.GetRows`, `M.Signature` |
| [InvestmentAction.lua](../../../../../Mod/InvestmentAction.lua#L1) | M13 | I | GP ([Run:873](../../../../../Mod/Gameplay.lua#L873)) | `SPCInvestmentAction.Start`, `cp` |
| [LegacyCleanup.lua](../../../../../Mod/LegacyCleanup.lua#L1) | M02 | I | IN | `SPCLegacyCleanup.Start`, `text` |
| [LegacyCleanupCatalog.lua](../../../../../Mod/LegacyCleanupCatalog.lua#L1) | M02 | I | IN | `C.Keys`, `C.Group` |
| [LevelBannerState.lua](../../../../../Mod/LevelBannerState.lua#L1) | M13 | I | GP ([Run:1013](../../../../../Mod/Gameplay.lua#L1013)) | `SPCLevelBannerState.Start`, `key` |
| [Lv2GPP.lua](../../../../../Mod/Lv2GPP.lua#L1) | M05 | I | GP ([Run:881](../../../../../Mod/Gameplay.lua#L881)) | `SPCLv2GPP.Start`, `int` |
| [Lv2Housing.lua](../../../../../Mod/Lv2Housing.lua#L1) | M05 | I | GP ([Run:879](../../../../../Mod/Gameplay.lua#L879)) | `SPCLv2Housing.Start`, `validate` |
| [Lv3Effects.lua](../../../../../Mod/Lv3Effects.lua#L1) | M05 | I | GP ([Run:891](../../../../../Mod/Gameplay.lua#L891)) | `SPCLv3Effects.Start`, `readFacts` |
| [Lv3Support.lua](../../../../../Mod/Lv3Support.lua#L1) | M05 | I | GP ([Run:889](../../../../../Mod/Gameplay.lua#L889)) | `historicalStart`, `readFacts` |
| [Lv4CopyRead.lua](../../../../../Mod/Lv4CopyRead.lua#L1) | M05 | I | IN | `notice`, `SPCLv4CopyRead.Metadata` |
| [Lv4Percent.lua](../../../../../Mod/Lv4Percent.lua#L1) | M05 | I | GP ([Run:907](../../../../../Mod/Gameplay.lua#L907)) | `SPCLv4Percent.Start`, `d.WithdrawCulture` |
| [NativeFacts.lua](../../../../../Mod/NativeFacts.lua#L1) | M03 | I | GP ([Run:867](../../../../../Mod/Gameplay.lua#L867)) | `SPCNativeFacts.New`, `enabled` |
| [NetworkBoost.lua](../../../../../Mod/NetworkBoost.lua#L1) | M04 | I | GP / R ([Run:931](../../../../../Mod/Gameplay.lua#L931)) | `SPCNetworkBoost.Quantize`, `SPCNetworkBoost.Start` |
| [NetworkBridge.lua](../../../../../Mod/NetworkBridge.lua#L1) | M04 | T | GP ([Run:885](../../../../../Mod/Gameplay.lua#L885)) | `SPCNetworkBridge.Start`, `d.RegisterConsumer` |
| [NetworkInput.lua](../../../../../Mod/NetworkInput.lua#L1) | M04 | I | IN | `atom`, `N.Reference` |
| [NetworkIsolation.lua](../../../../../Mod/NetworkIsolation.lua#L1) | M04 | I | GP ([Run:999](../../../../../Mod/Gameplay.lua#L999)) | `SPCNetworkIsolation.Start`, `short` |
| [NetworkRecoveryCell.lua](../../../../../Mod/NetworkRecoveryCell.lua#L1) | M04 | I | PKG | `same`, `reason` |
| [NetworkRecoveryModel.lua](../../../../../Mod/NetworkRecoveryModel.lua#L1) | M04 | I | PKG | `integer`, `fields` |
| [NetworkRecoveryStore.lua](../../../../../Mod/NetworkRecoveryStore.lua#L1) | M04 | T | PKG | `M.Key`, `M.Open` |
| [NetworkSender.lua](../../../../../Mod/NetworkSender.lua#L1) | M04 | T | IN | `SPCNetworkSender.New`, `stop` |
| [OrdinaryBuildingCatalog.lua](../../../../../Mod/OrdinaryBuildingCatalog.lua#L1) | M03 | I | GP ([Run:871](../../../../../Mod/Gameplay.lua#L871)) | `flag`, `M.Build` |
| [OverflowStorageProbe.lua](../../../../../Mod/OverflowStorageProbe.lua#L1) | M13 | I | GP ([Run:993](../../../../../Mod/Gameplay.lua#L993)) | `SPCOverflowStorageProbe.Start`, `key` |
| [PerformanceCounters.lua](../../../../../Mod/PerformanceCounters.lua#L1) | M13 | I | IN | `M.New`, `M.Count` |
| [PlayerActionReplies.lua](../../../../../Mod/PlayerActionReplies.lua#L1) | M13 | I | GP ([Run:903](../../../../../Mod/Gameplay.lua#L903)) | `SPCPlayerActionReplies.New`, `integer` |
| [Probe.lua](../../../../../Mod/Probe.lua#L1) | M01 | I | IN | `P.CrewBase`, `P.CrewAmount` |
| [ProjectTurnObservation.lua](../../../../../Mod/ProjectTurnObservation.lua#L1) | M10 | I | GP ([Run:995](../../../../../Mod/Gameplay.lua#L995)) | `SPCProjectTurnObservation.Start`, `publish` |
| [PropertyCell.lua](../../../../../Mod/PropertyCell.lua#L1) | M02 | I | IN | `SPCPropertyCell.WriteReadback`, `SPCPropertyCell.NonnegativeFinite` |
| [PurchaseProbe.lua](../../../../../Mod/PurchaseProbe.lua#L1) | M13 | I | GP ([Run:925](../../../../../Mod/Gameplay.lua#L925)) | `SPCPurchaseProbe.Start`, `row` |
| [PurchaseProbeRead.lua](../../../../../Mod/PurchaseProbeRead.lua#L1) | M13 | I | IN | `SPCPurchaseProbeRead.Render` |
| [QualificationProbe.lua](../../../../../Mod/QualificationProbe.lua#L1) | M13 | I | GP ([Run:857](../../../../../Mod/Gameplay.lua#L857)) | `M.New`, `C.Read` |
| [ReadinessSummary.lua](../../../../../Mod/ReadinessSummary.lua#L1) | M13 | I | IN | `SPCReadinessSummary.Start`, `d.Register` |
| [ResearchApply.lua](../../../../../Mod/ResearchApply.lua#L1) | M06 | I | GP ([Run:913](../../../../../Mod/Gameplay.lua#L913)) | `name`, `M.Start` |
| [ResearchApplyModel.lua](../../../../../Mod/ResearchApplyModel.lua#L1) | M06 | I | IN | `M.Plan` |
| [ResearchChair.lua](../../../../../Mod/ResearchChair.lua#L1) | M06 | T | GP ([Run:915](../../../../../Mod/Gameplay.lua#L915)) | `name`, `explain` |
| [ResearchChairModel.lua](../../../../../Mod/ResearchChairModel.lua#L1) | M06 | T | IN | `M.Plan` |
| [ResearchCross.lua](../../../../../Mod/ResearchCross.lua#L1) | M06 | I | GP ([Run:911](../../../../../Mod/Gameplay.lua#L911)) | `name`, `M.Start` |
| [ResearchCrossModel.lua](../../../../../Mod/ResearchCrossModel.lua#L1) | M06 | I | IN | `M.Domain`, `M.Plan` |
| [ResearchCrossSample.lua](../../../../../Mod/ResearchCrossSample.lua#L1) | M06 | I | IN | `S.Replacements`, `S.Receive` |
| [ResearchInfrastructure.lua](../../../../../Mod/ResearchInfrastructure.lua#L1) | M06 | I | GP ([Run:909](../../../../../Mod/Gameplay.lua#L909)) | `name`, `integer` |
| [ResearchInfrastructureShadow.lua](../../../../../Mod/ResearchInfrastructureShadow.lua#L1) | M06 | I | GP ([Run:871](../../../../../Mod/Gameplay.lua#L871)) | `M.WithWorkers`, `read` |
| [ResearchSupport.lua](../../../../../Mod/ResearchSupport.lua#L1) | M06 | I | GP ([Run:877](../../../../../Mod/Gameplay.lua#L877)) | `SPCResearchSupport.Start`, `validate` |
| [ResearchTradition.lua](../../../../../Mod/ResearchTradition.lua#L1) | M06 | I | GP ([Run:865](../../../../../Mod/Gameplay.lua#L865)) | `integer`, `M.Validate` |
| [ResearchTraditionEffects.lua](../../../../../Mod/ResearchTraditionEffects.lua#L1) | M06 | I | GP ([Run:869](../../../../../Mod/Gameplay.lua#L869)) | `name`, `M.Start` |
| [Restructuring.lua](../../../../../Mod/Restructuring.lua#L1) | M02 | I | GP ([Run:1011](../../../../../Mod/Gameplay.lua#L1011)) | `SPCRestructuring.Start`, `key` |
| [RestructuringModel.lua](../../../../../Mod/RestructuringModel.lua#L1) | M02 | I | IN | `M.Copy`, `M.Same` |
| [RestructuringUI.lua](../../../../../Mod/RestructuringUI.lua#L1) | M02 | I | IN | `M.IsTeam`, `M.Request` |
| [ReverseDependencies.lua](../../../../../Mod/ReverseDependencies.lua#L1) | M03 | I | IN | `SPCReverseDependencies.New`, `id` |
| [RuntimeAuditCore.lua](../../../../../Mod/RuntimeAuditCore.lua#L1) | M13 | I | IN | `cell`, `M.FileSink` |
| [RuntimeComposition.lua](../../../../../Mod/RuntimeComposition.lua#L1) | M01 | T | IN | `M.Native`, `failed` |
| [RuntimeWork.lua](../../../../../Mod/RuntimeWork.lua#L1) | M03 | T | GP ([Run:875](../../../../../Mod/Gameplay.lua#L875)) | `SPCRuntimeWork.New`, `b.Facts` |
| [SafeCallbacks.lua](../../../../../Mod/SafeCallbacks.lua#L1) | M01 | I | IN | `M.Call`, `M.Notify` |
| [SampleLifecycle.lua](../../../../../Mod/SampleLifecycle.lua#L1) | M03 | I | IN | `count`, `integer` |
| [ShadowRouteState.lua](../../../../../Mod/ShadowRouteState.lua#L1) | M04 | I | IN | `integer`, `copy` |
| [SourceYieldProbe.lua](../../../../../Mod/SourceYieldProbe.lua#L1) | M13 | I | IN | `SPCSourceYieldProbe.Read` |
| [SpecialistSupport.lua](../../../../../Mod/SpecialistSupport.lua#L1) | M05 | I | IN | `S.Retire`, `find` |
| [Standardization.lua](../../../../../Mod/Standardization.lua#L1) | M09 | I | GP ([Run:923](../../../../../Mod/Gameplay.lua#L923)) | `SPCStandardization.Start`, `clone` |
| [StandardizationCatalog.lua](../../../../../Mod/StandardizationCatalog.lua#L1) | M09 | I | GP ([Run:923](../../../../../Mod/Gameplay.lua#L923)) | `SPCStandardizationCatalog.Build` |
| [StandardizationDiscount.lua](../../../../../Mod/StandardizationDiscount.lua#L1) | M09 | I | GP / R ([Run:927](../../../../../Mod/Gameplay.lua#L927)) | `SPCStandardizationDiscount.Start`, `d.Withdraw` |
| [StandardizationEffects.lua](../../../../../Mod/StandardizationEffects.lua#L1) | M09 | T | GP ([Run:929](../../../../../Mod/Gameplay.lua#L929)) | `SPCStandardizationEffects.Start`, `replaceDependencies` |
| [StorageProbe.lua](../../../../../Mod/StorageProbe.lua#L1) | M13 | I | GP ([Run:818](../../../../../Mod/Gameplay.lua#L818)) | `SPCStorageProbe.Start`, `expected` |
| [StoreDeferredLifecycle.lua](../../../../../Mod/StoreDeferredLifecycle.lua#L1) | M02 | I | IN | `int`, `plain` |
| [StoreLifecycleRecovery.lua](../../../../../Mod/StoreLifecycleRecovery.lua#L1) | M02 | I | IN | `integer`, `M.Plan` |
| [StoreSubrecords.lua](../../../../../Mod/StoreSubrecords.lua#L1) | M02 | I | IN | `fields`, `S.Keys` |
| [TimedProductionProbe.lua](../../../../../Mod/TimedProductionProbe.lua#L1) | M13 | I | GP ([Run:991](../../../../../Mod/Gameplay.lua#L991)) | `SPCTimedProductionProbe.Start`, `empty` |
| [TimedProject.lua](../../../../../Mod/TimedProject.lua#L1) | M10 | I | GP ([Run:997](../../../../../Mod/Gameplay.lua#L997)) | `SPCTimedProject.Start`, `key` |
| [TimedProjectModel.lua](../../../../../Mod/TimedProjectModel.lua#L1) | M10 | I | IN | `SPCTimedProjectModel.ClassifyQueue`, `SPCTimedProjectModel.Boundary` |
| [TimedProjectReaders.lua](../../../../../Mod/TimedProjectReaders.lua#L1) | M10 | I | GP ([Run:960](../../../../../Mod/Gameplay.lua#L960)) | `SPCTimedProjectReaders.New`, `current` |
| [TimedProjects.lua](../../../../../Mod/TimedProjects.lua#L1) | M10 | I | IN | `SPCTimedProjects.Queue`, `SPCTimedProjects.WorkSet` |
| [Tombstones.lua](../../../../../Mod/Tombstones.lua#L1) | M02 | I | IN | `add`, `SPCTombstones.Names` |
| [TradeRouteProbe.lua](../../../../../Mod/TradeRouteProbe.lua#L1) | M13 | I | GP ([Run:814](../../../../../Mod/Gameplay.lua#L814)) | `SPCTradeRouteProbe.Start`, `scalar` |
| [TurnLedger.lua](../../../../../Mod/TurnLedger.lua#L1) | M05 | I | IN | `SPCTurnLedger.Advance` |
| [UI/BackgroundRoutes.lua](../../../../../Mod/UI/BackgroundRoutes.lua#L1) | M04 | T | UI | `integer`, `need` |
| [UI/BoostGreatWorkRead.lua](../../../../../Mod/UI/BoostGreatWorkRead.lua#L1) | M07 | I | IN | `snapshot`, `SPCBoostGreatWorkRead.Boost` |
| [UI/BoostRefresh.lua](../../../../../Mod/UI/BoostRefresh.lua#L1) | M05 | I | UI | `refresh` |
| [UI/CapitalInvestmentPanel.lua](../../../../../Mod/UI/CapitalInvestmentPanel.lua#L1) | M08 | I | UI | `L`, `number` |
| [UI/CapitalInvestmentUI.lua](../../../../../Mod/UI/CapitalInvestmentUI.lua#L1) | M08 | I | IN | `M.Backend`, `M.Reference` |
| [UI/CityBannerManager_SPC_Levels.lua](../../../../../Mod/UI/CityBannerManager_SPC_Levels.lua#L1) | M12 | I | PKG | `attach`, `CityBanner:UpdateName` |
| [UI/CityBannerManager_SPC_TimedProject.lua](../../../../../Mod/UI/CityBannerManager_SPC_TimedProject.lua#L1) | M12 | I | PKG | `CityBanner:UpdateProduction` |
| [UI/CityIdentityEvidence.lua](../../../../../Mod/UI/CityIdentityEvidence.lua#L1) | M02 | I | IN | `SPCCityIdentityEvidence.New`, `scalar` |
| [UI/CityPotential.lua](../../../../../Mod/UI/CityPotential.lua#L1) | M12 | I | UI | `signal`, `clearPending` |
| [UI/ClaimIconOverlay.lua](../../../../../Mod/UI/ClaimIconOverlay.lua#L1) | M12 | I | IN | `SPCClaimIconOverlay.New`, `apply` |
| [UI/ClaimProjectUI.lua](../../../../../Mod/UI/ClaimProjectUI.lua#L1) | M10 | I | IN | `M.IsProject`, `M.Current` |
| [UI/CommercePanel.lua](../../../../../Mod/UI/CommercePanel.lua#L1) | M08 | I | UI | `L`, `number` |
| [UI/CommerceUI.lua](../../../../../Mod/UI/CommerceUI.lua#L1) | M08 | T | IN | `M.Backend`, `M.Available` |
| [UI/CopyYieldRefresh.lua](../../../../../Mod/UI/CopyYieldRefresh.lua#L1) | M05 | I | PKG | `stopNetwork`, `networkBlocked` |
| [UI/CrewProjectOrder.lua](../../../../../Mod/UI/CrewProjectOrder.lua#L1) | M10 | I | UI | `PopulateGenericItemData`, `CreateQueueInstance` |
| [UI/CrewProjectUI.lua](../../../../../Mod/UI/CrewProjectUI.lua#L1) | M10 | I | IN | `SPCCrewProjectUI.New`, `localCity` |
| [UI/DevelopmentInvestmentPanel.lua](../../../../../Mod/UI/DevelopmentInvestmentPanel.lua#L1) | M08 | I | UI | `L`, `num` |
| [UI/DevelopmentInvestmentRead.lua](../../../../../Mod/UI/DevelopmentInvestmentRead.lua#L1) | M08 | I | IN | `SPCDevelopmentInvestmentRead.New`, `definitions` |
| [UI/DevelopmentInvestmentUI.lua](../../../../../Mod/UI/DevelopmentInvestmentUI.lua#L1) | M08 | I | IN | `M.Backend`, `M.Reference` |
| [UI/DialogueProjectUI.lua](../../../../../Mod/UI/DialogueProjectUI.lua#L1) | M07 | I | IN | `M.Current`, `M.Preview` |
| [UI/DialogueRefresh.lua](../../../../../Mod/UI/DialogueRefresh.lua#L1) | M07 | I | UI | `validOwner`, `foreign` |
| [UI/DiscountEligibility.lua](../../../../../Mod/UI/DiscountEligibility.lua#L1) | M12 | I | PKG | `count`, `reset` |
| [UI/EngineeringStudyUI.lua](../../../../../Mod/UI/EngineeringStudyUI.lua#L1) | M09 | I | IN | `M.Current`, `M.Text` |
| [UI/ExpeditionGateWindow.lua](../../../../../Mod/UI/ExpeditionGateWindow.lua#L1) | M11 | I | PKG | `L`, `setReport` |
| [UI/ExpeditionMovementProbe.lua](../../../../../Mod/UI/ExpeditionMovementProbe.lua#L1) | M11 | I | PKG | `L`, `show` |
| [UI/ExpeditionSpyActivity.lua](../../../../../Mod/UI/ExpeditionSpyActivity.lua#L1) | M11 | I | UI | `detail`, `view` |
| [UI/ExpeditionSpyChooser.lua](../../../../../Mod/UI/ExpeditionSpyChooser.lua#L1) | M11 | I | UI | `redirect`, `Open` |
| [UI/ExpeditionSpyPopup.lua](../../../../../Mod/UI/ExpeditionSpyPopup.lua#L1) | M11 | I | UI | `redirect`, `OnShowMissionBriefing` |
| [UI/ExpeditionSpyUnitPanel.lua](../../../../../Mod/UI/ExpeditionSpyUnitPanel.lua#L1) | M11 | I | UI | `OnPromptToDeleteUnit`, `OnDeleteUnit` |
| [UI/ExpeditionSpyWindow.lua](../../../../../Mod/UI/ExpeditionSpyWindow.lua#L1) | M11 | I | UI | `noAction`, `clearRows` |
| [UI/ExpeditionTrainingName.lua](../../../../../Mod/UI/ExpeditionTrainingName.lua#L1) | M11 | I | UI | `detail`, `view` |
| [UI/ExpeditionTrainingUI.lua](../../../../../Mod/UI/ExpeditionTrainingUI.lua#L1) | M11 | I | IN | `SPCExpeditionTrainingUI.New`, `observe` |
| [UI/GPPRefresh.lua](../../../../../Mod/UI/GPPRefresh.lua#L1) | M05 | I | UI | `observe`, `source` |
| [UI/GreatWorkBasis.lua](../../../../../Mod/UI/GreatWorkBasis.lua#L1) | M07 | I | PKG | `number`, `SPCGreatWorkBasis.Plan` |
| [UI/IndustryRefresh.lua](../../../../../Mod/UI/IndustryRefresh.lua#L1) | M09 | I | UI | `refresh`, `safe` |
| [UI/InstitutionOverview.lua](../../../../../Mod/UI/InstitutionOverview.lua#L1) | M12 | I | UI | `currentPacket`, `eligible` |
| [UI/Institutions.lua](../../../../../Mod/UI/Institutions.lua#L1) | M12 | I | UI | `top`, `size` |
| [UI/LevelBannerModel.lua](../../../../../Mod/UI/LevelBannerModel.lua#L1) | M12 | I | IN | `M.View` |
| [UI/LevelBanners.lua](../../../../../Mod/UI/LevelBanners.lua#L1) | M12 | I | UI | `destroy`, `color` |
| [UI/OverflowStorageRead.lua](../../../../../Mod/UI/OverflowStorageRead.lua#L1) | M12 | I | IN | `SPCOverflowStorageRead.New`, `shortError` |
| [UI/P0Panel.lua](../../../../../Mod/UI/P0Panel.lua#L1) | M12 | I | UI | `status`, `overflowPulse` |
| [UI/ProjectTurnRead.lua](../../../../../Mod/UI/ProjectTurnRead.lua#L1) | M10 | I | IN | `SPCProjectTurnRead.New`, `api.Read` |
| [UI/ResearchCrossRefresh.lua](../../../../../Mod/UI/ResearchCrossRefresh.lua#L1) | M06 | I | UI | `refresh`, `safe` |
| [UI/RuntimeAudit.lua](../../../../../Mod/UI/RuntimeAudit.lua#L1) | M13 | I | UI | `now`, `count` |
| [UI/SafeAdapters.lua](../../../../../Mod/UI/SafeAdapters.lua#L1) | M01 | I | IN | `SPCSafeAdapters.New`, `declaration` |
| [UI/TimedProjectCityPanel.lua](../../../../../Mod/UI/TimedProjectCityPanel.lua#L1) | M10 | I | UI | `ViewMain` |
| [UI/TimedProjectDisplay.lua](../../../../../Mod/UI/TimedProjectDisplay.lua#L1) | M10 | I | IN | `SPCTimedProjectDisplay.IsCurrent`, `SPCTimedProjectDisplay.Text` |
| [UI/TimedProjectRead.lua](../../../../../Mod/UI/TimedProjectRead.lua#L1) | M10 | I | IN | `SPCTimedProjectRead.New`, `state` |
| [UI/TimedProjectSelection.lua](../../../../../Mod/UI/TimedProjectSelection.lua#L1) | M10 | I | IN | `SPCTimedProjectSelection.New`, `publish` |
| [UI/TimedProjectSelectionClient.lua](../../../../../Mod/UI/TimedProjectSelectionClient.lua#L1) | M10 | I | IN | `SPCTimedProjectSelectionClient.New`, `message` |
| [UI/TimedTurnProbe.lua](../../../../../Mod/UI/TimedTurnProbe.lua#L1) | M13 | I | UI | `gameplay`, `request` |
| [UI/UnitPanelActions.lua](../../../../../Mod/UI/UnitPanelActions.lua#L1) | M12 | I | UI | `signal`, `clearView` |
| [UI/UnitSites.lua](../../../../../Mod/UI/UnitSites.lua#L1) | M10 | I | UI | `selected`, `refresh` |
| [UI/UnitTargetMarkers.lua](../../../../../Mod/UI/UnitTargetMarkers.lua#L1) | M10 | I | UI | `signal`, `discardPending` |
| [UnitActionSitePolicy.lua](../../../../../Mod/UnitActionSitePolicy.lua#L1) | M10 | I | GP ([Run:895](../../../../../Mod/Gameplay.lua#L895)) | `SPCUnitActionSitePolicy.Check`, `integer` |
| [UnitActions.lua](../../../../../Mod/UnitActions.lua#L1) | M10 | I | GP ([Run:899](../../../../../Mod/Gameplay.lua#L899)) | `SPCUnitActions.Start`, `unit` |
| [UnitSiteFacts.lua](../../../../../Mod/UnitSiteFacts.lua#L1) | M10 | I | IN | `M.Districts`, `take` |
| [UnitSiteProbe.lua](../../../../../Mod/UnitSiteProbe.lua#L1) | M10 | I | GP ([Run:895](../../../../../Mod/Gameplay.lua#L895)) | `SPCUnitSiteProbe.Start`, `data.Read` |
| [UnitTargets.lua](../../../../../Mod/UnitTargets.lua#L1) | M10 | I | GP ([Run:897](../../../../../Mod/Gameplay.lua#L897)) | `SPCUnitTargets.Start`, `collect` |
| [YieldCarrierProbe.lua](../../../../../Mod/YieldCarrierProbe.lua#L1) | M13 | I | IN | `plotFor`, `read` |

## SQL and non-Lua resource boundary

M14 covers modinfo UpdateDatabase, UpdateText, UpdateIcons/Colors and FrontEnd configuration SQL. ArtDefs, textures and XML are not Lua modules. Gameplay definitions, project availability, internal carriers, icons/text and test civilization configuration load through distinct action types; a Data file is not automatically an active Gameplay writer. Examples: [ResearchChair definitions](../../../../../Mod/Data/ResearchChair.sql#L2), [in-game declarations](../../../../../Mod/SpecializationP0.modinfo#L10), [database action](../../../../../Mod/SpecializationP0.modinfo#L408).

## Precision and unknowns

218/218 measures packaged-file coverage; T means targeted excerpt tracing only. The static include graph does not resolve external base-game/HD libraries, dynamic include strings, engine startup success, runtime replacement conflicts or condition values. Some files cross families, including expedition/unit actions and profession UI/Gameplay owners. Each file receives one navigation group; dependencies require the As-Is evidence.

## Read Ledger / Handoff

Read modinfo and literal include/function declarations of all packaged Lua for the authorized inventory; followed direct Gameplay.Run, FactConsumerBindings, Store, NetworkSender and ResearchChair calls into targeted functions. No external Mod, HD, Historical, save or log scans; no tests/deployment. Stable means this static evidence version is ready for review. User decision: none. User testing: none requested. Primary next: review both module reports, citations and coverage under the existing checkpoint process.
