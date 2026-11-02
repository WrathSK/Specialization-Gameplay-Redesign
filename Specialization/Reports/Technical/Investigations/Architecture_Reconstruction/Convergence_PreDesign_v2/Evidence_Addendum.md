# Evidence Addendum — v2 decisions and targeted rechecks

Investigation / Non-authoritative / No implementation authorization

Status: Stable | Maintainer: Primary

2026-11-02. Source baseline: `0c9c60ec8e6a769461cfaaa801ffbb3f07a25804` (develop); D0058 / A0183 / S0866. Recorded runtime B399.426 from `4915170`; deployment not reverified here.


[Overview](Executive_Overview_v2.md) · [Gap matrix](Gap_Matrix_v2.md) · [Decisions](Decision_Register_v2.md)

## 1. Baseline and decision provenance

- v1 source baseline: `920b4ed2a8da5dd394b95fe03f96c81dc2a8a069`.
- v2 source/read baseline: `0c9c60ec8e6a769461cfaaa801ffbb3f07a25804`, develop and origin/develop matched; tracked tree clean on entry.
- The entire intervening commit adds only six v1 Markdown reports (671 lines). `Mod/`, `DevelopmentTests/`, `tools/`, formal Design/Architecture, Status and Workflow are unchanged. Therefore a changed classification in v2 is a decision or closer evidence reading, not a runtime fix.
- Authority metadata remains D0058/A0183/S0866; record says B399.426 from `4915170`, stable/main B307.334. This audit did not run live package verification, inspect a new save, or promote/deploy.
- **H2**, owner-supplied `Architecture_Convergence_v2_Handoff.md`, SHA256 `bcc5ac837102e7bd3b56af2ac22c35b7f600359704b1d82626e73feea19927f6`. This identifies the reviewed user input, not a permanent backup or independent Architecture source. Its relevant decisions are recorded in the Decision Register; the attached file is not copied into formal authority.
- Read all six v1 materials through Primary and three scoped delegated reviews. Old files remain unchanged; no v1 hashes/context entries are silently advanced.

Current formal Design `SAFE-004` still contains the older lawful-baseline allowance; A0183:21/640 reflects that history. H2 DEC06C changes the target away from treating irrecoverable corruption as a routine comprehensive recovery program. This requires explicit later formal synchronization, not code silently interpreting a report over Markdown, and not asking the owner to reapprove C.

## 2. New/current source rechecks

All source locators refer to the baseline above. `Mod/` and `DevelopmentTests/` paths are repository-relative. Formal/report paths are under `Specialization/`. E1–E11 are v2 addendum IDs; the older appendix's E01–E27 keep their own scope.

| ID | Source / function / lines | Current fact and inference boundary |
|---|---|---|
| E1 Governor | Mod/Probe.lua:320–346; Mod/Data/GovernorProbe.sql:2–56; Mod/Data/TestAmerica.sql:19–20; Mod/EffectiveFacts.lua:114–121/210–218/232–239; Mod/NativeFacts.lua:59–64; Mod/RuntimeWork.lua:459–468; Mod/Gameplay.lua:837–848 | Six properties are native modifier-owned. Conditional nil is validfalse, CONTROL must1, hierarchy/read/ref errors UNKNOWN. No governor normally KNOWN ceiling1; Potential<=1 need not read gate. Immediate invalidation usually precedes publish-drained consumers, not proof deep reads run inside event. Independent modifier timing inconsistency is only an inference. Actual normal UNKNOWN rate/root unestablished |
| E2 Duty/registration | Mod/FactChanges.lua:105–114/164–173/182–203; Mod/FactConsumerBindings.lua:11–18/19–46/52–122; Mod/RuntimeWork.lua:59–76/226–231/265–290; Mod/GreatWorkFacts.lua:196–244; Mod/NetworkBridge.lua:133–144; Mod/RuntimeComposition.lua:46–70; Mod/Gameplay.lua:1029–1036 | Attempts≠takeover; existing owner pending patterns reusable. Bridge watermark-before-Emit error exists. Startup guards cover named current Register APIs, not any new declaration API. Phase0 infrastructure order and sealed drain are real dependencies |
| E3 Ability inputs | Mod/ResearchSupport.lua:9–18; Mod/IndustrySupport.lua:24–33; Mod/Lv2Housing.lua:20–40; Mod/Lv2GPP.lua:43–65; Mod/ResearchApply.lua:26–50/72–75; Mod/ResearchCross.lua:4/46–74; Mod/ResearchCrossSample.lua:20–52; Mod/ResearchInfrastructure.lua:31–54; Mod/ResearchChair.lua:34–47; Mod/ResearchTraditionEffects.lua:105–134; Mod/Commerce.lua:123–165/183–206/240–279/323–356 | ResearchCross has **no D input**, despite a D-caused wake declaration. ResearchApply worker count is used in plan totals, carrier coefficient per[y]. Housing uses tier presence, not weighted numeric D. Commerce worker-UNKNOWN zero branch remains; strict current vs output hold differs from retained-input recomputation |
| E3 continued | Mod/CultureAestheticModel.lua:5–34; Mod/CultureMeaningModel.lua:41–65; Mod/CultureInspirationModel.lua:6–17; Mod/DialogueEffects.lua:100–144; Mod/CultureInsightsTourism.lua:8–21/64–75; Mod/CultureNetwork.lua:110–173; Mod/StandardizationEffects.lua:157–207; Mod/IndustryWonderEffects.lua:50–74; Mod/DevelopmentInvestment.lua:197–225 | Culture GW count/era/category and building set/qualification are distinct cells. Dialogue passive uses current GW Summary, completion a fresh detached sample. Culture receiver identity not localACTIVE. Standardization combined D1 freeze and Development strict signing remain separate |
| E4 History/errors | Mod/StoreSubrecords.lua:100–201; Mod/StoreLifecycleRecovery.lua:14–63; Mod/CityProgressionStore.lua:340/404–438/736–778/823–825/1061–1169/1175–1179/1237–1248/1255–1278/1306–1349/1413–1428/1563–1592/1977–1985/2102–2140; Mod/IndustryHistory.lua:48–61/180–210; Mod/EngineeringStudyProjects.lua:129/147–150 | Real isolated/deterministic/deferred recovery exists; CHECK_FAILED not proof permanence. constructed resolves native object before profession relevance; missing target can hold unassigned records. Exit requires matched **foreign** loss.target; already-returned endpoint may block old cleanup. Return waits all exits. Strict completeE matches DEC07; presentN does not repair historicalE |
| E5 Claim | Mod/ClaimProjects.lua:111–139/144–186; Mod/Data/ClaimProjects.sql:4/7/10/13; Mod/CityProgressionStore.lua:872–897; DevelopmentTests/test_b124_claim.py:59–60 | Ordinary project cost1,000,000; internal complete1T path and intentional authenticated direct native completion coexist. Current callback takes first3 fields; unique frozen candidate/ref/receipt still required. Missing timer is not a defect under DEC08 |
| E6 Crew | Mod/UI/CrewProjectUI.lua:14–35; Mod/CrewProjects.lua:265–294; DevelopmentTests/test_refactor_s7d6_proof.py:23–50; Status/Validation/Results/Refactor_S7d6_Crew_Proof_Gap.md | Getter is player-wide GetNumProjectsAdvanced; per-project last receipt and exactly prior+1 remain. Frozen actual-owner counterexample produces0not2 when both callbacks see2. Conditional stale-old-A ambiguity does not prove native engine allows that history; no per-city ordinal verified |
| E7 UI | Mod/RestructuringUI.lua:38–47; Mod/Restructuring.lua:203–225; Mod/UI/UnitPanelActions.lua:154/212–222; Mod/UI/LevelBannerModel.lua:5–11; Mod/UI/InstitutionOverview.lua:25–36; Mod/Gameplay.lua:249–281; Mod/InstitutionPresentation.lua:59–101; Mod/ResearchTraditionEffects.lua:68–84 | Missing prepared-A inert guard distinct from unknown native hitbox/async mapping. Banner unknown suppresses; institutions retain same-ref structure with unknown state. Candidate age/L math not proof applied effect. UI projection cannot authorize a transaction |
| E8 Capital cross-use | Mod/Commerce.lua:24–31/148–155; Mod/CapitalInvestment.lua:137–184/343–345; Mod/CapitalInvestmentModel.lua:135–148; Design/Content/Commerce_D0058.json:263/281/292; Architecture/v2/Commerce_Preparation.md:200 | Passive unknown Reputation→effective0/READY; TransactionCurrent doesn't test reputationKnown; Capital locksR0 through common quote, prepare/confirm compares same fallback. Venture refund usesR; STABLE return doesn't. ACTIVEIII known qualificationR0 differs from ACTIVEIV unknown neededR. Static reach, no native occurrence asserted |
| E9 Baseline/coverage | Status/Specialization_P0_Status.md:1–27; Workflow/Authority.json; Status/Validation/Results/Specialization_B399_Network_Project_Coverage_Reconciliation.md:1–49; Status/Validation/Results/Specialization_B399_Button_Treasury_U5_Review.md | Scope/evidence unchanged. Mainline route/contract/ordinary four-profession acceptance retained; U5 not started; no uncontrolled trader death/plunder/city removal or repeated Claim core campaign |
| E10 Network hold/recovery | Architecture/Specialization_v0.1_Architecture.md:16–23/138–148; Design/Network.md:45–59; Mod/NetworkSender.lua:19–78; Mod/NetworkBridge.lua:20–23/620–660; Mod/NetworkInput.lua:72–105; Mod/NetworkRecoveryStore.lua:15–45 | NET1/2 repairs preserved; D1 pending output freeze and D2 source-retained contribution are narrower than generic stale reads. Cold Commerce/Culture consumer wiring still absent; adapter existence not integration |
| E11 Retirement/work | Reports/Proposals/Audit_Followup_Priorities.md:488–512; Reports/Advisory/Refactor_Program/Refactor_Program_Plan.md:297–330; Mod/Gameplay.lua:862/874–876/906–930/995–1012; Mod/UI/ProjectTurnRead.lua; Mod/UI/TimedProjectSelection.lua; Mod/UI/TimedProjectDisplay.lua; Mod/Dialogue.lua:38–61/298–327; Mod/UI/DialogueRefresh.lua:26–46/55–81/110–122/147; tools/deploy.py:50–53; tools/temporary_playtest.py:37–94 | Original S9/S10 responsibilities remain, mixed with already completed mechanisms. Probe/legacy names not deletion proof. Whole-catalog/city sampling source shape not CPU/RAM result. Two deploy paths have different removal review despite hash/rollback protection |

## 3. Corrected interpretation versus v1

| v1 concern/recommendation | v2 interpretation | Reason / remaining evidence |
|---|---|---|
| General fact-type retained use and “passive D” example | Ability/input/use matrix; ResearchCross D=N/A | Actual current input must govern; R1 clarifies existing adjacency retention without a formula change |
| Decide raw vs derived ACTIVE | Raw ceiling direction now approved; root/lifetime/opt-in remains | No routine UNKNOWN proof; no cache complexity justified just by a hypothetical error |
| Best-effort vs reliable coordinator | Reliable takeover direction now approved | Only minimum contract remains proposed; no best-effort vote repeated |
| Complete D7 legal-zero-baseline program | Superseded as target by C, root/error first | Preserve legitimate existing repair/deferred mechanisms; later formal sync not wholesale deletion |
| Lower-bound E alternative | Withdrawn; complete history required | DEC07A explicit |
| Claim missing timer risk | Direct authentic early completion justified | DEC08A intentional test/compatibility path; positive/cancel event distinction still evidence-first |
| Potential fourth canceled argument | Not established for Gameplay event | B396 main already distinguishes **CityProjectCompletedNarrative** bCanceled from CityProjectCompleted; do not transfer signatures |
| All remaining S9/S10 before U5 | Remaining obligations now in O3/O6/O7/etc after baseline | DEC11A; exact minimal preU5 worklist still not implementation approved |
| Benchmark/percent choice | No percentage or arbitrary CPU/RAM KPI question remains | DEC12A; preserve existing bounded-work checks and finite native acceptability observations |
| Late exit = only missing return wake | Actual foreign endpoint authorization can prevent late old cleanup after return | T4 must distinguish allowed window, bug and changed endpoint; event retention alone not enough |
| Passive unknown Reputation exception only | New G29 identifies an irreversible consumer of fallbackR0 | Need mode-dependent current input; no blanket Capital disable or new refund formula |

## 4. Exact project event evidence boundary

The current Gameplay listeners use `Events.CityProjectCompleted(playerID,cityID,projectID)`. Existing primary-source examples referenced by the frozen Crew proof report show first3 fields, not full emitted signature, cancellation delivery or duplicate guarantees.

B396 main `Reports/Advisory/Architecture_Engineering_Audit/Independent_Architecture_Audit_B396.md:419/639` explicitly attributes `bCanceled` to `CityProjectCompletedNarrative`, referring to native `ProjectBuiltPopup.lua`. Its companion DLA-07 shorthand is not stronger evidence. This audit reread the repository record, **did not re-open installed native source or run the callback**. No guessed fourth-argument filter or timer restriction is justified.

## 5. Existing evidence, not newly executed tests

| Existing source | Scope retained | Limit |
|---|---|---|
| test_b136_facts.py:145–208 | Injected known/invalid/unknown governor fixture cases | Not actual modifier timing or current native recovery proof |
| test_b124_claim.py:59–60 | Deliberate direct native-completion fixture | Authentic native event cancellation semantics not proved |
| test_refactor_s7d6_proof.py:23–50 and frozen Crew proof result | Actual-owner zero-grant counterexample + conditional ambiguity | Characterization PASS demonstrates a gap, not D5 multi-city PASS; native histories unknown |
| test_refactor_s9f4.py; test_store_write_boundaries.py; test_refactor_s8c5c.py | Existing exact deferred/CAS/business-transition coverage | Not a new all-error recovery PASS |
| Specialization_B397_Network_Proof_Transport.md | Recorded87-method real-module selection + explicit baseline failures | No fresh execution; ordinary native recovery later in B399, deliberate packet-loss origin still unknown |
| Specialization_B395_Culture_Research_Playtest_20261029.md; Specialization_B397_Industry_Playtest_20261031.md; Specialization_B399_Fifth_Playtest_20261101.md | Named previously accepted normal paths | Changed OptionB paths need delta regression, not automatically inherited blanket PASS |

Unprefixed test basenames above are under `DevelopmentTests/`; result basenames under `Specialization/Status/Validation/Results/`.

No gameplay test, current fixture run, failure injection, new log analysis, native game/DB experiment, benchmark or probe was executed this round. Existing tests and results are read as evidence and proposed future gates. No new LOCAL_SIMULATION_PASS or USER_GAME_TEST_PASS is claimed.

## 6. Read ledger and document QA

Read repository/root/topic guidance and W0005 scope/publication; Authority/Status current metadata; all six v1 reports; H2; named formal clauses and actual producer/consumer/Store/transaction/startup paths listed above. Three scoped read-only reviews returned facts/use, delivery/registration, and history/lifecycle/completion findings; Primary spot-checked high-impact branches. No broad HD/other-Mod/native binary scan, archive sweep or root-cause repair was performed.

The seven owned report files are the only permitted writes. v1 remains frozen; no formal Design/Architecture/Status/Authority/Context Lock update, test/config/source/runtime change, U5 start, OptionB execution, deployment or main promotion. Document QA passed: seven files,25 local report links and79 distinct source-anchor groups resolve, with cited line numbers in bounds. G01–G29, all60 F rows,14 DEC disposition rows,R1–R6 andT1–T8 are structurally complete/unique. Three scoped cross-reviews were incorporated: GPP worker permission does not auto-approve retained governor qualification; Aesthetic does not use tier magnitude; native evidence is conditional on the actual interface question rather than restricted to a fixed subset of tasks. Source baseline/H2 hash and existing tracked tree/index remained unchanged before explicit report staging. Mermaid dependency source received a node/edge review, not renderer execution. The standard staged privacy/credential check remains a separate publication gate. Source-anchor existence is not proof of every semantic claim.

User decision: R1–R6 remaining target detail review; not DEC reapproval. User testing: none now. Primary next: stop after the reviewed report checkpoint and await v3 authorization.
