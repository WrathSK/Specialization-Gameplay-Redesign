# B399 — action-button contract, Treasury exclusion and pre-U5 coverage

2026-11-01. Primary, read-only investigation at `d786ffd`, following the fifth playtest and the user's clarified A/B behavior. Live remains B399.426 / `4915170`; D0058/A0183 unchanged. No runtime, test implementation, formal Architecture/Design, game configuration, external Mod or deployment change. Native acceptance remains scenario-specific.

## 1. User-confirmed action contract and PT019

The same contract applies to both liquidation and configuration:

| State / input | Required UI behavior |
|---|---|
| Unprepared | A remains visible and provides the operation's informational tooltip. B is absent. |
| First A click | Prepare a plan; keep A and its information; show confirmation B immediately to A's left. |
| Further A clicks while that plan is prepared | Inert; do not confirm or replace the prepared plan. |
| B click | Confirm the matching current plan through the existing eligibility/reference/readback/irreversible-operation guards. |

The user's observed behavior is a real reported defect: B does nothing while a second A click appears to confirm. Do not redefine this as the intended two-click-A interaction or treat a successful liquidation as correct button behavior.

[RestructuringUI.lua](../../../../Mod/RestructuringUI.lua),38–47,declares distinct callbacks: tag −247/A calls PREPARE; tag −248/B calls CONFIRM with `v.prepared`. A has **no prepared-state inert guard**. [Restructuring.lua](../../../../Mod/Restructuring.lua),203–225,only prepares on PREPARE; irreversible liquidation/configuration requires CONFIRM plus the matching plan. A source-level callback swap is therefore not established as the fix. [UnitPanelActions.lua](../../../../Mod/UI/UnitPanelActions.lua),154 and212–222,already provides the separate investment/Crew example of inert Prepare and fixed right-A/left-B controls; it is a reference,not authorization to redesign unrelated controls.

Read-only native-source review: installed HD `UI/Replacement/DL_UnitPanel.lua` includes the native panel,retains its AddActionToTable,and for these custom icons delegates AddActionButton to the original renderer (1015–1088). Native Base UnitPanel.lua203–223/271–317 registers each action's CallbackFunc separately. The two custom rows reuse an icon but have distinct tags/callbacks. Same icon alone does not prove callback replacement.

A Lua5.1 local replay executes the actual RestructuringUI plus the native AddActionToTable/AddActionButton function bodies with only Civ type annotations stripped. Engine controls/selection/request delivery are explicit doubles. Results: initial A→REST_PREPARE; prepared B→REST_CONFIRM with the current plan; prepared A→REST_PREPARE again. Thus the missing A inert guard is **STATIC_CONFIRMED / locally reproduced**; the reported visual A-confirm/B-inert mapping is **not reproduced by this helper-level model**. Hitboxes/layout/instance reuse/asynchronous receipt timing remain unverified. The fifth trace lacks per-click action identity. Repair must preserve stable A/B positions and confirm-only plan handling,and verify the actual clickable controls;do not claim root cause or successful repair from this replay. No new native test is requested before such a repair.

## 2. 41/52 Gold: bounded exclusion, not another blocking investigation

User disposition: first exclude duplicate Commercialization/Mod payment; finding the ultimate external/native origin is a **nonblocking side task and may be dropped**. No additional broad probes,foreign-Mod changes or deliberate playtest are introduced.

The fifth archive's exact END→STARTED pairs are sorted by TRAIN sequence,not append order:

| Session / interval | Applied Commerce at END→STARTED | Extra balance change | Physical log lines |
|---|---:|---:|---|
| A1,58→59 |27→27|41|A867→937|
| A1,60→61 |52→54|41|A1232→1311|
| A1,61→62 |58→55|41|A1495→1556|
| A1,62→63 |0→0|41|A1635→1676|
| A2,63→64 |60→56|52|A2118→2179|
| B,63→64 /64→65 /65→66 |0→0 throughout|41 each|B186→241;298→344;357→393|
| C,67→68 through71→72 |0→0 throughout|41 each|C171→207;274→317;361→395;406→460;474→567|

The earlier fourth-playtest archive also records52when Commerce was43/46/47,not52. Values are neither a second copy of the configured Commercialization sum nor dependent on its active state. In particular,the repeated0→0 intervals refute duplicate active Commercialization as the explanation.

Source/loaded-definition checks:

- All Mod Lua sources have only two direct ChangeGoldBalance call sites: [CapitalInvestment.lua](../../../../Mod/CapitalInvestment.lua),76,and [DevelopmentInvestment.lua](../../../../Mod/DevelopmentInvestment.lua),327. Capital calls are guarded and logged;Development only debits the quoted positive cost. The fifth archive has exactly three contract debits at58T,three credits at68T and four Development debits. None explains the repeated41/52before LOCAL_BEGIN;the68Tcredits occur later and reconcile independently.
- Commercialization never directly pays the Treasury. [Commerce.sql](../../../../Mod/Data/Commerce.sql),1–11,defines31binary **city base Gold** carriers. Commerce creates/removes only the required bit buildings;[Commerce.lua](../../../../Mod/Commerce.lua),455–484,observes actual carrier totals. Captured expected/carrier sums agree,including0while inactive.
- The configured DebugGameplay.sqlite was opened with `mode=ro` and query-only. All31loaded Commerce bits have exactly one BuildingModifiers link,the declared base-city-yield modifier and their exact bit amounts;mapping mismatch count=0. No SPC-owned building modifier uses a Gold/Treasury one-shot-grant modifier. Other loaded SPC Gold effects are passive city-yield percentage,Great Work Gold,or specialist citizen-yield rows,not another per-turn Lua payment. Source examples: [ResearchApply.sql](../../../../Mod/Data/ResearchApply.sql),32–46,and the existing Culture Meaning yield carrier definitions. These effects participate in normal native yield accounting;their existence is not a second Gold-balance mutation.
- At59T,the distinct ordinary income is197.6015625=364.6015625−167;at68T it is96.55859375=290.55859375−194. The41is present before LOCAL_BEGIN;normal net income and the three Capital credits are separate later observations. The earlier review's exact screenshot reconciliation remains valid.

**Disposition:** the captured intervals exclude duplicate Commercialization carrier application and duplicate SPC Lua Treasury calls as the cause. No evidence supports another SPC payment. This does not establish a complete native/foreign-Mod transaction ledger or prove the ultimate origin. Engine/HD yield-accounting interactions are not globally certified absent. PT017 is **nonblocking**,with origin UNKNOWN;do not reopen a large root-cause investigation or demand a new save just to name the source.

## 3. What remains before final U5

The original [B391 checklist](Specialization_B391_Develop_Playtest_Checklist.md) explicitly describes an **intermediate develop test**,not the final S11/U5 candidate. Its original requirements must be reconciled with later user acceptance and deferrals;do not copy all eight rows back into a new mandatory checklist. The [fifth review](Specialization_B399_Fifth_Playtest_20261101.md),[Industry review](Specialization_B397_Industry_Playtest_20261031.md),[Culture/Research review](Specialization_B395_Culture_Research_Playtest_20261029.md),current Status and accepted refactor schedule are the scoped basis.

| Category | Current disposition | Next responsibility |
|---|---|---|
| Four-profession ordinary abilities,activation/withdrawal and most numeric checks | Substantial user acceptance across the five runs;individual scopes remain in their result records. No full repeat requested. | Primary preserves the acceptance matrix;only changed paths get a later regression delta. |
| Commercialization,Capital maturity/pre-maturity reload,Development continuity,Reputation,REALLOCATING cold restore/manual configuration | Fifth-run mainline coverage now present. Standardization purchase max/withdrawal and the user's observed combined Development/Standardization progress are also retained. | No new standalone campaign. A final changed build may need one representative combined-effect check,not repetition of each domain. |
| PT019 action A/B | Intended interaction now explicit;missing A inert guard confirmed,full native mapping still open. | Primary investigates/repairs the actual UI boundary under approved implementation scope;then one short liquidation/configuration smoke. Not a re-test of every Restructuring rule. |
| Claim full-turn and interrupted/reloaded round | Recent consolidated records do not establish its independent full-round/reload closure. Dialogue/Study cannot prove Claim's independent outcome rules. | Reconcile existing evidence first;only if absent,cover one round during the eventual final smoke. “No located receipt” is not a claim the user never tried Claim. |
| Crew multi-city same-tier completion | Not covered by the single-source Industry test. Current CrewProjects still uses player-wide completion count and last-per-project receipt;the proof/attribution boundary remains open. | Primary resolves/supports the engineering boundary before asking the user to exercise it. A final supported two-city completion is a native gate;repeated user attempts cannot substitute for unique attribution. |
| Crew use after cold load / once-only consumption | Ordinary750spend,slot release and applicable modifiers are accepted. The reviewed summary does not independently close the specific after-load/use/no-replay scenario. | Reuse existing evidence if it proves this;otherwise one convenient final-candidate use/reload check. Do not repeat all Crew tiers or purchase types. |
| Final package loading,diagnostic exit and performance | Current testing is still on the diagnostic/intermediate B399 package. No final clean-candidate footprint/heap attribution or final readiness closure is claimed. | Primary completes engineering/local gates;final candidate gets ordinary load/turn/idle/memory smoke with existing collector. Advisor analyzes attributable growth;do not equate raw whole-game growth with SPC cost. |

### Engineering work is not missing player testing

Before a genuine final U5 candidate,the original accepted S9/S10 work must still close. This does not move the separately chosen post-U5 Option B migration into the pre-U5 scope. In current source,NetworkRecoveryStore/Cell exist but have no automatic Commerce/Culture consumers;the accepted per-source cold-recovery integration is not completed by an ordinary successful reload. The original exact duties in Binding/CityFlow/Construction,CultureInspiration,timing/display and other legacy modules must move before retirement. Required cleanup/save/SQL references remain. The deployment tool still needs the approved audited file-removal/rollback path before retired files are removed. No source is deleted or schema altered by this review.

These are Primary implementation/local-composition responsibilities,including fault/UNKNOWN recovery,not tasks to ask the player to fabricate unreadable facts,corrupt saved records or randomly expose retirement defects. Final U5 follows their integration and tested package boundary. Existing ability-test outcomes remain useful;only materially changed paths require a new focused check.

### Explicitly outside mandatory current testing

- Multi-item Dialogue/Study queue counting: user-deferred,nonblocking;current sole-item restart has accepted scope.
- PT01741/52origin: nonblocking after the exclusions above.
- HD automatic-versus-locked specialist GPP: do not demand repetitive Commerce/Industry verification.
- Pillage/flood: opportunistic long-play observation only;never require forced/random pillage as an exit task.
- Undecided ownership/loss/return gameplay and parked Police eligibility: separate user/design scope,not invented U5failure conditions.
- Expedition feature/ejection repair: separately tracked PT018,not silently imported into the accepted refactor program. The user's ordinary three-task/reload successes remain accepted;the border-displacement defect is not erased.
- Venture failure/protection,Reputation cap and other unexercised extremes remain honest coverage limits;no forced RNG fishing or repeated whole-profession campaign is added here.

User decision:none needed for this investigation;A/Bcontract and nonblocking Treasury disposition are recorded. User testing:none requested now;the table separates eventual minimal native checks from prior engineering obligations. Primary next:publish scoped documentation and stop;do not implement,deploy or promote main from this investigation.
