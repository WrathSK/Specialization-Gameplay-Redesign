# B235 — Engineering Study, IV Standardization and older-Wonder production

Evidence: **LOCAL_SIMULATION_PASS / STATIC_CONFIRMED**. Source **B235.262 / modinfo262**. Native production, legal purchase prices and this new city-history transaction remain **USER_GAME_TEST_REQUIRED**. Source/live provenance is separate in the final checkpoint and [Status CURRENT](../../Specialization_P0_Status.md#current-authoritative-state).

## Authorized scope and preflight

The user authorized IND-3 under [the B235 plan](../../../Architecture/v2/Industry_Preparation.md#b235-proposal--engineering-study-and-wonder-production) and unchanged Industry/Shared D0045. B234's accepted III baseline and exact old-writer retirement are retained. No Crew/Engineering Practice, Culture HOLD, Research-network redesign, balance, GC or Design change.

The new persisted-asset audit triggers AF-01/12/13 and P06a/P07 were checked against the actual Store/Dialogue path. Store still owns the Game index and per-city records, structural validation, readback/failure boundary, reservations and exit/return. The new pure Engineering model owns only its business schema and transitions. A narrow read fence prevents the new Engineering reader from publishing candidate L inside a native Property setter callback. This is not a general Store repair or closure of the old audit findings.

Loaded DB evidence is read-only. `EFFECT_ADJUST_BUILDING_PURCHASE_COST` has BuildingType/Amount examples including `MESSIAH_PURCHASE_BUILDING_MONUMENT_DISCOUNT_MODIFIER`; existing B054 uses the city modifier. `EFFECT_ADJUST_WONDER_ERA_PRODUCTION` has StartEra/EndEra/IsWonder/Amount examples such as `CORVEE_ANCIENTCLASSICALWONDER`; the new building-owned city carrier uses COLLECTION_OWNER. These are interface/argument evidence, not new native acceptance.

**Known partial delivery:** the loaded DB exposes only `EFFECT_ADJUST_ALL_DISTRICTS_PURCHASE_COST`, with no established target-specific District purchase primitive. B235 does not install that broad substitute. District construction enhancement is implemented; District purchase enhancement remains BLOCKED_TECHNICAL. Building purchase uses the existing target-specific effect without adding permission. Both already-legal Gold/Faith channels still need scoped native evidence; an unavailable channel is not silently treated as tested.

## Implementation and ownership

| Surface | Implemented | Limits |
|---|---|---|
| Civilization knowledge E | `IndustryHistory.Credit` reads the existing bounded completion receipts; confirmed E changes notify study eligibility | No city display reconstruction, foreign completion collector, world scan or new E authority |
| City history L | Optional `engineeringKnown` + version1 `engineering` extension in the existing city record; serial, contiguous successful L receipts, one pending attempt and bounded latest outcome | Never-initialized differs from initialized-zero and damaged/missing established history; L is never reconstructed from E or carriers, nor clamped to current E |
| Full-turn study | Normal production **工程传统研习**; Industry ACTIVE IV and L<E; explicit selection + exact current sole project; end-turn proof then existing FinishProgress primitive and verified receipt commit | No Dialogue quota. Uncertain native completion/Store write is held, not replayed; a prematurely forced completion does not create full-turn evidence |
| Interruption | Production change, confirmed ACTIVE/identity loss or owner loss cancels only the pending round; requalification requires fresh selection/full turn | Completed L remains. UNKNOWN holds unresolved work without rewarding it. REALLOCATING is not yet an implemented state producer; its future Commerce transition must call this same identity-exit cancellation before continuing |
| Restore | Store restores reliable L/receipts and any ACTIVE attempt; pending CALLING without this session's armed proof becomes held | No automatic reward replay, old-save migration or independent save framework. Unsupported owners stay dormant; same-city supported return derives current output |
| Standardization | Existing single writer uses actual holders per template: III10/0, IV10+2L construction /2L building purchase; self and network sources take independent per-template MAX | Nonholders contribute nothing; remove old final value before adding replacement; UNKNOWN retains only applicable evidence. Exact old Discount/Copy retirement remains |
| Macro Engineering | `IndustryWonderEffects`: ACTIVE IV, own civilization era versus each Wonder's own era; gaps1/2/3+ yield10/20/30, current/future0 | Native ordinary-production modifier only; independent N/E/L. Existing fixed Crew AddProgress path unchanged; revised Crew integration remains its own future gate |
| Presentation/logs | Native Industrial Zone project icon, normal production list and existing1T display; left **工业历史 / 模板** reports L/E/Macro, right **工业标准化** reports exact current targets | Report never activates the system. Existing bounded scalar collector records ENGINEERING_STUDY, ENGINEERING_STUDY_REPORT and INDUSTRY_WONDER_EFFECT; diagnostic expected values are not proof of native yields |

The city transaction validates the same token/reference before and after writes. Confirmed-loss cleanup matches the current city geometry/owner even after a return changes native cityID, so it neither leaves the current view nor clears an unrelated reused ID. Duplicate completion cannot add another layer. Loss cancels the pending attempt before recording the transfer. An existing known record missing its Engineering component is held rather than reinitialized.

## Events, scaling and resource exits

Inputs are explicit queue selection, production change/completion, end/activation of the supported player's turn for active attempts, governor/current-fact publication, committed city changes, confirmed E changes, era changes, existing native publish/load and Store exit/return. Confirmed L writes actively notify Standardization's existing affected-source/receiver path. No new timers, frame callbacks, world-city fallback or GC changes. Era fallback reads one supported-player era and only marks cities on a changed era; existing error slots retry at an existing player-turn boundary.

Pending attempts are city-owned persistent transactions. Session `dirty`, active/armed/completion latches and UI click intent have one owner; they leave on completion, cancellation, loss, reference change, turn-expired click or context shutdown. The native carriers are derived, not persisted authority. Initialization reads supported cities only for the new Wonder writer; Store's existing confirmed-exit/load callbacks own foreign cleanup.

The loaded catalog has175 template targets and9 eras. SQL generates1575 IV final-value definitions plus27 Wonder-era definitions and1 access marker (1603 new internal Buildings). Only one current value per matching template is installed, with up to one applicable value per older Wonder era; definitions are not all instantiated per city. The available L catalog follows loaded eras, not an arbitrary five-layer cap. A missing definition holds that projection instead of changing saved L. Initial/load presence checks cover the owned definitions; subsequent writes touch changed values. This has a real bounded catalog/startup cost; local visits and idempotence do not establish native CPU/memory improvement.

## Local validation

| Actual-source suite | PASS |
|---|---:|
| B235 Engineering Study/Store, effects/SQL, production UI and package | 39 |
| B234 projection/support and current integration fixtures | 38 |
| Industry history / catalog | 25 /2 |
| Store write boundaries | 18 |
| Dialogue projects / current UI behavior | 21 /7 |
| B232 network revalidation | 18 |
| Selected investment propagation behaviors | 20 |
| **Total** | **188** |

New counterexamples cover full-turn two completions and L=E, L>E retention, confirmed E notification, interruption/restart, same-publish away/back, ACTIVE loss, identity exit, duplicate/premature completion, missing/throwing native completion, cold restored ACTIVE and CALLING, initialized-zero versus corruption, owner loss/recapture/changed cityID, reentrant reads and drop/third-value/throwing writes, other-city isolation, per-template actual-holder MAX, failed exact removal, no layer clamp, era change/UNKNOWN recovery, no foreign-city scan, and explicit UI start intent without panel dependence. SQL is applied only to an in-memory copy of the configured read-only DB, including repeatable cleanup of this batch's own definitions in that copy.

`test_investment_update_propagation...test_syntax_package_and_unchanged_contracts` still hardcodes historical modinfo201 and its changed-file set; B234 already excluded it. It is unchanged and not counted as PASS. Current package/syntax checks validate262 instead. B234 fixture adaptation adds an empty level table and an uninitialized Engineering reader; no old behavior assertion was weakened. This is scoped local evidence, not gameplay-wide/native/performance acceptance.

Additional checks PASS:12 changed/new Lua sources parse; modinfo262 references all235 actual runtime files;506 scoped Markdown links/anchors resolve; context check/self-test pass with235 runtime files and730 locked files;3 helper fixtures pass. The77 B235/B234 tests were rerun after the last diagnostic-only refinement. Diff whitespace passes; staged publication is gated before each commit. No full gameplay regression or long memory test was requested or run.

## One combined native session

Use the manually started existing collector and a campaign started with B235.262, per the current save-scope contract. Cheat setup is allowed; ordinary production is the measured output. Prepare one Industry ACTIVE IV source with E>=2 (two supported-player completed Wonders from different own eras), L0, and a known ordinary template; avoid a second stronger source when comparing values. A legal unbuilt building in its template group is enough for the price/construction check. Existing logs are primary evidence; take a price/progress breakdown only where native values are not captured.

1. Select **工程传统研习** from the normal production list, as the only project. Before and after one complete turn use **工业历史 / 模板**: L0→1. Right-click it for **工业标准化**: matching construction12%, building purchase2%. Compare the actual legal building price/progress with unchanged base and other modifiers; the report's expectation alone is insufficient.
2. Start a second study, then remove its ACTIVE IV qualification before the turn completes. L stays1; at ACTIVE III its own source returns10%/0%. Restore IV, select a fresh study and complete a full turn: L2, construction14%, building purchase4%. This distinguishes cancellation from pause/resume and exercises final-value replacement.
3. With workers/base production and other bonuses fixed, compare ordinary production of one Wonder behind the civilization's era while IV versus below IV. Expected additional percent is10/20/30 for gap1/2/3+. Preserve native rounding; no compensation. A single relevant gap is enough for the primitive; other gaps are locally checked.
4. Save and fully restart once after L2. Confirm L2 and current14%/4% projection remain. This checks the newly added authoritative history, not the unchanged probe default-OFF lifecycle. No extra enable/disable/re-enable ritual. If no legal Faith purchase is available, mark that channel untested without creating one artificially; District purchase is excluded by the stated technical gate.

## Source and deployment checkpoint

Local implementation complete; source B235.262/modinfo262. Deployment is not inferred from the edited source. Until the guarded switch is recorded, external runtime remains the verified B234.261 receipt. Native results remain pending. Main, accepted Design, GC, other profession implementations, frozen prior evidence and configuration are unchanged.
