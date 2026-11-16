# Unattributable District Events — Narrow Recovery Proposal

**State:** A SELECTED by Owner on2026-11-05 for existing-PU07 source investigation/local repair/composition only. B NOT APPROVED;no further B schema design now. Remaining text preserves the reviewed options,not new Design/Architecture or persistence authority.

**Code baseline:** develop `1b6a69b14f0cbc5911411aa2288ee237ebd74bbe`, B408.435, D0059/A0184/S0884. Production code, tests, formal rules and deployment remain unchanged by this document.

## 1. Recommendation and decision

Finish source attribution before adding persistence. B408 already protects fixed Claim candidates from unrelated district callbacks. The remaining question concerns a city whose profession must still be chosen by its first valid completed district, when a potentially relevant event cannot be attributed reliably.

**Recommended: approve A, with B retained as a conditional design candidate.** First evaluate the existing independent city-source paths within PU07. Add a recovery receipt only if a concrete remaining failure requires evidence to survive a load, and only after its historical-proof and bounded-recovery contract is reviewable. Do not make a speculative persistence subsystem a new prerequisite for every later slice.

The previous checkpoint suggested saved evidence as a possible solution; it did **not** establish that extra persistence is necessary or sufficient. Recording an event cannot manufacture its source city, prove it was complete at delivery, or reconstruct a missing first-completion order.

| Choice | What it permits after approval | What it does not permit |
|---|---|---|
| **A — Source-first, recommended** | Continue scoped source attribution and local composition tests under the existing PU07 contract. Retain strict UNKNOWN protection if evidence is insufficient; report the exact remainder. | No new saved fields, changed first-selection rule, automatic deployment or required game session. |
| **B — Conditional saved-evidence extension** | If explicitly selected, refine the minimal receipt contract in section 4 for separate approval before wiring it. | This draft alone does not authorize save-format changes, guessed history or a generic recovery framework. |
| **C — Defer the remainder** | Keep B408's safe subset and the remaining strict guard; Owner may direct independent approved work to resume. | Do not mark PU07/its dependent gate closed or describe broad automatic recovery as implemented. |

There is no request to reapprove the overall convergence program. A real new native limitation, persistence boundary or gameplay interpretation still returns to the Owner; ordinary implementation details do not.

## 2. Evidence and unchanged rules

- **STATIC_CONFIRMED:** [PROG-001/005](../../Design/Specialization_v0.1_Design_Spec.md#L97) chooses the first **valid completed** district notification, not placement, type priority or a load snapshot. Validity includes city identity, district type, completion and historical eligibility. Fixed Legacy Claim candidates follow a separate path.
- **STATIC_CONFIRMED:** the [construction callback](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/1b6a69b14f0cbc5911411aa2288ee237ebd74bbe/Mod/CityProgressionStore.lua#L2143) uses the known owner/type/x/y prefix,with no independently qualified cityID argument;four bound parameters do not prove exact native arity. Its [completion proof](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/1b6a69b14f0cbc5911411aa2288ee237ebd74bbe/Mod/CityProgressionStore.lua#L2018) additionally validates the live district, city, type, owner, completion and reference. The callback name alone does not replace those checks.
- **LOCAL_SIMULATION_PASS, limited:** B408's [tests](../../../DevelopmentTests/test_pu07a_completion_scope.py) and [S0884 evidence](../../Status/Specialization_P0_Status.md#pu07a-evidence-and-limits--s0884) cover 51 selected methods, including 24 new methods. A missing qualifying target no longer poisons two fixed Claim sets. With two potentially affected FIRST_COMPLETION roots, the conservative hold still occurs; that test explicitly characterizes an **OPEN** remainder, not a repair PASS.
- **STATIC_CONFIRMED candidate sources:** existing [RuntimeWork](../../../Mod/RuntimeWork.lua#L451) consumes owner/districtID/cityID for district events. In pinned HD Gameplay, `PolicyOnDistrictConstructed` uses `Map.GetPlot(x,y)` and `Cities.GetPlotPurchaseCity(plot)`. This establishes a same-context usage precedent, not a guarantee of attribution during the missing-reference condition. A plot's current city cannot silently substitute for the event's original district/city identity.
- **NOT ESTABLISHED:** that a completely unattributable qualifying completion occurs in supported normal macOS play, its frequency, or an independent witness that always recovers it. Synthetic nil/throw tests prove the source branch's consequences, not native incidence.

The [accepted PU07 row](https://github.com/WrathSK/Specialization-Gameplay-Redesign/blob/fb7be65b664b78f2c692cdc9d661511f37823b2e/Specialization/Reports/Technical/Investigations/Architecture_Reconstruction/Convergence_PreDesign_v3_Final/Architecture_Convergence_Integrated_Roadmap_DRAFT.md?plain=1#L118) requires scope repair without invented first history or new persistent authority. The [defensive-engineering rule](../../Architecture/Specialization_v0.1_Architecture.md#L185) requires evidence before additional fallback/recovery machinery. These are the reasons for this decision boundary, not new restrictions invented by the proposal.

## 3. A — Complete the existing source route first

1. Filter reliable non-v0.1, known incomplete and otherwise definitively irrelevant observations before they can affect first history. An unreadable value is not a confirmed negative. Keep B408's fixed-candidate exclusion and generic admission-failure protection.
2. Evaluate the existing plot-to-city Gameplay usage and independently delivered city/district identifiers. Select a source only after checking its actual context, signature and meaning. Prefer a direct same-callback read; introduce no cross-context assumption or generic event bus.
3. Treat any alternative city as an attribution candidate until its owner, full city reference, district location/type/identity, completion state and admission epoch agree. If it requires a district collection, read only the independently located city, with complete bounded validation; do not scan all players/cities to find a convenient match. Disagreement is UNKNOWN.
4. A separate progress notification may identify a source, but is not automatically a completion witness or proof that it preceded another event. Any retained scalar correlation must have an explicit size, epoch, matching and disposal rule; no native-object retention or presumed registration order.
5. If these facts provide the full original proof, keep the existing first-selection commit. If they identify only the city, scope the failure to that city; do not grant or backdate a first completion. If they cannot identify a city, retain the explicit conservative remainder and report it.

**Local acceptance:** actual Store + Claim, missing primary lookup with reliable independent source, disagreement, incomplete district, wrong owner/reference/epoch, unrelated cities, replacement families, duplicate/reentrant callbacks, early admission, same-turn competing completions and load boundaries. Preserve generic foundation failure and existing errors; prove no normal-path scan/retry growth. Do not weaken first-proof assertions to make the alternate source usable.

**Native gate:** only if a specific supported-context question remains unanswerable locally, propose a small separately approved read-only observation of ordinary district placement/completion and source agreement. No forced pillage, uncontrolled AI event, full-campaign replay or game launch by Primary. A normal successful getter is not proof of recovery when all getters fail. No probe is authorized or enabled by this draft.

**A closes only what it proves.** Do not infer that it solves cross-load loss, or that every defensive all-unreadable branch must first receive an elaborate recovery subsystem. Whether a demonstrated residual is a release/support limitation remains an explicit disposition; this proposal does not silently close the existing gate.

## 4. B — Minimal receipt candidate, if evidence justifies persistence

### Purpose and ownership

Keep enough evidence about an actually delivered, unresolved district observation to avoid losing its order across a supported same-build load. **CityProgressionStore remains the sole owner of first identity, eligibility and the recovery record.** No new general service, second identity ledger, shared transaction credential or per-profession recovery implementation.

An unattributable event cannot honestly be placed inside an arbitrary city's record. If a separate Store-owned saved journal is necessary, its key/version and the relationship to indexed city records require formal approval. This is the proposed extension beyond the current contract.

### Minimal data, not snapshots

| Saved item | Purpose / restriction |
|---|---|
| Version and monotonic observation sequence | Preserve actual delivery order across loads. Sequence is not a native completion ID or evidence that completion happened. |
| Original scalar owner/type/x/y and delivery turn | Preserve exactly what was received; unknown fields remain explicitly unknown. No native objects or formatted reports. |
| Family/completion observations and provenance | Separate known relevant, known incomplete, and UNKNOWN. A recorded callback is not automatically `CONFIRMED_COMPLETE`. |
| Original identity/epoch evidence, when available | City token/reference, owner-change/admission witness and district identity only if reliably observed. Never fill gaps from a later city's current identity. |
| Candidate scope at that observation | Only then-eligible unresolved first-history records and pending admissions. Share one bounded cohort description; do not copy whole city records into every receipt. Exclude already specialized and fixed Claim histories. |
| Resolution / commit witness | Tie an exact resolved observation to the one confirmed Store first-selection write. No Boolean “processed” without the matching record/reference. |

Original unresolved scope must survive relevant loss/removal/reuse boundaries without interpreting a new city at the same coordinates as the old source. This proposal adds no ownership gameplay or cross-owner recovery entitlement.

### Resolution and ordering

1. Read back the receipt before using it to replace an existing protection. Failed or unconfirmed persistence retains strict protection; no caller proceeds on assumed success.
2. While an earlier observation could still be a city's first, preserve the later relevant notifications instead of selecting the later one immediately. This includes later **known-source** observations; saving only the original unknown row would still lose first-order information.
3. Recover only on a verified related source/availability event or the existing normal initialization boundary. No timer, every-turn all-city check, arbitrary-event retry or idle Publish polling. Callback/source correlation must be established first; if no reliable recovery trigger exists, B is not ready to implement.
4. Attribution and completion are separate. A later `IsComplete=true` cannot prove that an unreadable earlier placement was already complete. Nor can present coordinates or a current district list establish an old owner/epoch. Require delivery-time proof or an independently valid witness of the same historical notification; otherwise remain UNKNOWN.
5. Before committing, exclude every earlier observation that could affect the same first-history choice, or prove which valid observation is first. Then use the original Store validation/CAS/readback and identity publication. Save bytes alone never grant Potential or authorize an investment.
6. Confirm the city-record commit before retiring the receipt. A failure between journal and city-record writes must be idempotent: no second identity grant, guessed receipt acknowledgement or replay of native operations. Define both write-failure directions before wiring.
7. Keep ambiguous duplicates as observations unless identity/epoch/completion evidence proves equivalence. Matching owner/type/x/y/turn alone is not a unique completion receipt. After settlement, delete only the resolved recovery material; preserve the permanent city first/investment history.

### Bounds, failure and saves

B is a **gated candidate**, not a ready-to-code schema. Before its implementation approval, record exact numeric caps, serialization size, cohort membership representation, CAS/write ordering and the verified recovery trigger in the same scoped plan. Reuse the existing eight-observation per-foundation bound where applicable; it is **not** evidence that eight global unresolved events suffice.

- Bound unresolved observations, pending cohorts, and per-city later-first candidates separately. Retain the earliest necessary evidence; do not truncate or evict it to make room. Overflow must fail closed visibly within the affected uncertainty scope, never choose a later first or claim successful recovery. An overflow with lost proof is not an automatic-recovery PASS.
- No whole-root/history/report copies. An unknown source may initially implicate N eligible first-history cities: cohort intake can therefore be O(N), not “constant cost.” Measure serialization/copying and later-candidate retention; sharing a cohort avoids multiplying its copies by every receipt.
- No receipt/extra save write on an ordinary fully proved event outside a recovery episode. Same-value/duplicate notification handling must not create idle writes or unbounded diagnostics. If that cannot be demonstrated, revise or reject B.
- Missing, malformed, unknown-version or partially written recovery data never means “no prior event.” Keep it isolated and preserve parent identity guards. No manual player selection or technical reset is proposed.
- Scope is new campaigns and same-build saves after an approved format change. No cross-build migration promise. B408's old `completionError` string contains no original event witness; do not automatically clear or reinterpret it. Source rollback is not a save-history rollback.
- If source/completion/order evidence was never available, a receipt cannot guarantee eventual recovery. Continued uncertainty remains a diagnosed safety limitation, not the finished normal workflow. If automatic recovery requires evidence the engine cannot provide, return that precise limit rather than inventing another state machine.

## 5. Proof and stopping gates

| Stage | Evidence needed before declaring success |
|---|---|
| Source choice | Primary code/context evidence and actual Store composition, with disagreement/UNKNOWN cases. Community or HD use alone is not native failure-time acceptance. |
| Justification for B | A concrete supported-path evidence-loss case across loading; identify precisely which reliable information disappears and how the saved receipt enables deterministic recovery. A synthetic nil branch alone is insufficient justification for mandatory new persistence. |
| Receipt model | Earliest-unknown → later-valid cases in same and different cities; duplicate ambiguity; pending-before-admission; city/owner/reference reuse; capacity and work bounds; malformed/partial data. No production write yet. |
| Store composition | Receipt-write and city-write failures in both orders, reload between writes, reentry, exact once-only first choice, unchanged investment/other profession records, normal/idle zero extra work, restricted Lua51 and package/context checks. No weakened assertions. |
| Native delta, if needed | Minimum approved same-build save/load or source-availability question; separate native acceptance from local simulations. No complete U5 rerun by default. |

Do not close PU07/advance its dependent Claim gate solely because a journal exists. Preserve the independently OPEN Crew/native and other convergence gates; no whole-repository audit is requested.

## 6. Requested disposition

**Suggested Owner response:** “Proceed with A within the approved PU07 scope; B remains unapproved until its need, recoverable historical proof and exact bounds are demonstrated. Return only a genuine source/save/semantic decision.”

If the Owner instead wants B's exact contract developed now, that authorizes only the scoped candidate design; formal Architecture/save synchronization and production wiring follow explicit approval of that contract. It does not approve a new gameplay fallback for permanently unknown first history.

Owner disposition: A selected on2026-11-05;B remains unapproved and its save structure is not being refined. A code/local outcome and concrete native limits are recorded in [S0886](../../Status/Specialization_P0_Status.md#pu07-source-a-evidence-and-limits--s0886),not new authority in this proposal. User decision:none for that delivery. User testing:none now. Primary next:stop after its verified develop publication;no probe/deployment/other work package.

## Evidence locators

Internal links above refer to the fixed B408 source baseline. Existing [recovery-persistence approval](Refactor_Recovery_Persistence_Proposal.md) covers network source contributions and skipped lifecycle duties, not this new first-completion journal; its approval does not transfer automatically.

External source root **ENV-20261104**, HDv2.2 / Workshop2465378070 / Gameplay, as resolved by the existing [Engine Reference index](../Technical/Engine_Reference.md#source-index-and-raw-locations): `Policies.lua:72–86`, `PolicyOnDistrictConstructed`, SHA256 `42cf2a0df96806223a9f1d641b65254a4844be9f07463322fab2665f97e6404f`; `Misc.lua:584–599`, `UncompletedWonderRecord`, SHA256 `f4c78ba81f4d102b9ae1f196d6f0d24eebc2a821b3e3457cd50faa6de0daea7b`. The latter handles a Wonder queue/property and reinforces why a similarly named notification is not, by itself, a v0.1 completed-specialization proof. No HD code is copied, and no new native incidence or platform guarantee is claimed.
