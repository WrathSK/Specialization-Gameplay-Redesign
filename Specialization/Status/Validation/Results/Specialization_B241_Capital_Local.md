# B241 local result — Capital Investment

Date: 2026-10-18. Source basis: develop `695ae6f`. Build: B241.268/modinfo268. User explicitly authorizes the existing COM-B implementation and confirms permanent-institution establishment as the same-S tie-break; all other rules are retained. D0056 records that narrow clarification. **LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** Deployment is recorded separately after an actual guarded switch.

## Current implementation

One ordinary **资本投资** production-list action opens one shared panel with 科研／文化／工业 domains and **确认稳健投资／确认风险投资**. Opening/choosing a domain does not enqueue, debit or roll. It shows the current Treasury,25% principal, local D, current ACTIVE S with a named source or explicit no source, C,10-turn maturity, safe total/net, venture probability/success/failure/expected total and expected net. Negative expected net remains selectable. Existing contracts remain readable when current signing qualification declines.

Confirmed contracts lock mode, source/Owner references, P/D/S/C/R, probability, outcome and maturity. Three slots per city implement one unsettled contract per implemented non-Commerce domain; there is no nationwide cap. Ordinary ACTIVE/Identity/route changes do not reprice. Source Commerce city or locked S-city Owner change terminates without refund/failure/protection adjustment. Each city's owner-scoped hidden n is shared across venture domains, updated once after confirmed debit/activation, retained for original-owner return and cleared on actual Commerce Identity exit. No random outcome is exposed to normal UI/logs before settlement.

## State ownership and failure boundary

| State | Owner / lifetime |
|---|---|
| Contracts and n | Optional `capitalKnown/capital` extension in the existing per-city Store record; pure validation/calculation in CapitalInvestmentModel; at most3 current/latest domain records plus a scalar sequence and owner-count map |
| Institution establishment | Existing first-district time proves level1; each new confirmed Settler investment records the new permanent level's actual turn. Existing proven first-P4 Research/Reputation receipts can supply that time. No Governor/load-observation timestamps or guessed backfill |
| Ownership continuity | Existing matched Store loss increments `ownerChanges`; signed references detect loss even after a later return. Source contracts terminate in the same loss record write |
| Money | Actual native Treasury remains authoritative; Store keeps per-contract intent/calling/final receipts. These are not automatically atomic with the Treasury |
| Quotes / UI | Gameplay-owned replaceable current views; private confirmation input is revalidated. The UI never owns the formula, n, random result or settlement |
| Access marker | One exact internal building without yield, read/written only on actual availability changes; exact loss cleanup registered |

S selection consumes the existing verified center/recipient source projection through `CurrentCapitalSources`. It is neither Commercialization's direct-pair pool nor a transitive connected component or national maximum. Current proof/reference checks happen before source choice. Highest current ACTIVE wins; ties use earliest establishment of that corresponding permanent institution, then stable City ID/key. A unique highest source does not require an irrelevant tie-break. If an old record lacks reliable higher-level dates in a real tie, only that domain's quote is held with `CAPITAL_ATTAINMENT_HISTORY_UNKNOWN`; no history is fabricated. This optional extension is not a save migration project.

Native debit/credit first persists CALLING, makes one native call, reads balance back and then persists ACTIVE/SETTLED. New capital reads reject reentrant optimistic Store candidates. A thrown setter may already have written: cold load uses the saved final receipt if present; unresolved CALLING becomes HELD and never guesses from a later Treasury balance or repeats the action. Empty pre-call debit intent can be safely abandoned without a money call. Failure isolation retains other city records; no general Store/framework rewrite or new registry was introduced.

Treasury uses `GetTreasury():GetGoldBalance()` and `ChangeGoldBalance(amount)`, matching the read-only HD source surface (Workshop2465378070, `Gameplay/HD_Common.lua:72–76`, `Gameplay/Projects.lua` RNG usage). No standalone fractional-native probe was run. The writer requests unrounded formula values and accepts only matching immediate readback (absolute numerical tolerance0.000001); it never silently floors, compensates or retries a native mismatch. Fractional retention/engine quantization remains part of the one native test. The UI shows six fractional places; logs retain before/after/requested values.

## Trigger and work boundary

- Signing is an explicit native script request with stale-quote, duplicate, busy and same-domain guards; rejected occupancy consumes no RNG.
- Existing network/Commerce publications mark current quotes dirty; one publish callback coalesces those marks. Quote inputs reuse facts within the three-domain read, not full diagnostic construction.
- Existing player-turn/load events visit registered capital records for maturity/recovery. Only actual contracts inspect source references; no world/building/work/route scan is added.
- Transfer handling reconciles affected supported old/new Owners. No AI specialization, timer/frame polling, new GC, Development Investment or Restructuring implementation.

## Validation

**155 targeted tests PASS; 0 failures/errors/skips.** 46 B241 tests plus109 inherited Commerce/Store/UI/network/SQL checks. Actual Lua model, Store, service, UI adapters and existing NetworkBridge are exercised; native Treasury/control rendering are explicit doubles. The old Commerce UI fixture only loads the newly required Capital UI module; its assertions are unchanged.

Coverage: exact fractional-double debit and settlement; sequential25% remaining balance; safe and both venture outcomes; n shared/reset; current ACTIVE choice and permanent-level tie order; no-source minimums; real-tie unknown history; no local district requirement; stale quote/double/reentrant confirmation; isolated other city; Owner loss of either key city; normal gate/route decline;10-turn maturity; saved outcome and cold-VM recovery; pre-call/write/readback failures; native throw-before/after/ignore/rounding; final Store write failing before or after application; no replay/second debit/credit; known missing/corrupt state; source IDs copied without recursive forwarding; actual production interception and scalar UI request/ack.

All changed/direct Lua syntax, package/XML, current Design links/anchors, context selectors/hashes, diff and staged publication are checked separately before commit. Ordinary capital writes/settlement retain zero cross-record uniqueness visits in the actual Store fixture; this is a local access-count result, not native CPU/memory evidence. Frozen audits/results and old D0055 sources are unchanged. The new frozen D0055 Spec is byte-identical to its reviewed original.

## One minimal native session

Use an in-scope Standard-speed test campaign and one Commerce ACTIVE III+ city. Keep the existing manual collector running; it collects the new CAPITAL records without a new process or configuration. No P0 toggle or diagnostic prototype is needed.

1. **城市生产列表 → 资本投资**. Select 科研; inspect the shown current quote, then **确认稳健投资**. Check immediate debit and an executing contract. Opening this panel must leave the production queue unchanged.
2. Select 文化 or 工业, then **确认风险投资**. Its principal must use25% of the already reduced Treasury. Both contracts occupy separate domains. Leave the outcome hidden; do not force either random branch.
3. Save once during the term, fully exit and cold-load once. Open **资本投资** and confirm the same locked principal, terms and maturity. Continue to the quoted due turn (both contracts run in parallel).
4. Confirm each contract shows **已结算**, a risk result when relevant and its actual returned amount. Continue one more turn/check once to exclude a repeated payout. The logger's CAPITAL_MONEY before/after isolates settlement from normal per-turn income; no per-turn screenshot series or manual total-income reconstruction is requested.

This tests the new native Gold primitive and contract persistence/settlement once. If a money mismatch/HELD occurs, stop signing and return the log; do not repeatedly click, reroll, rebuild the same test or choose a rounding rule implicitly. Engine precision that requires changing the economic amount returns to the user. Existing B240 yields, other professions and old harness OFF/re-enable paths are inherited.

## Stop / delivery

User decision: institution tie-break confirmed; no further gameplay decision inferred. User testing: the single session above. Primary next: record actual deployment outcome, then stop for native evidence. Capital acceptance does not advance Development Investment or Restructuring. Main, Culture HOLD, external configuration and prior evidence stay unchanged.
