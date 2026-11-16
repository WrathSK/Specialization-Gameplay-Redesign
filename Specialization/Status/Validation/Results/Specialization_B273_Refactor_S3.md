# B273.300 — S3 composition isolation and readiness

State: S3_COMPLETE / S4_AUTHORIZED; source basis `28aae8b`. No deployment/main promotion/native PASS.

## Runtime Impact Contract

- Startup owner: explicit ordered Gameplay entries, typed OK/FAILED/SKIPPED_DEPENDENCY; actual startup prerequisites only. Includes and Starts stay in their original relative positions. A protected epilogue reports partial initialization honestly and seals diagnostic composition independently.
- Scope: synchronous per-entry facades for Events/GameEvents/LuaEvents register callbacks at the same native Add position and preserve identity/Remove/call semantics; no native namespace mutation. Failed-owner guards quarantine partial listeners even if Remove is absent. Only finite entry/event/function handles retained, no city/player objects; no timer, scan or new native read. Normal runtime handler exception behavior remains.
- Partial exports and explicit callback/decorator slots are restored on Start failure. Store exit/return and GreatWorkFacts consumer registration callbacks are owner-gated; failed exits cannot falsely ACK cleanup. No blind restart or native-write rollback. Dependencies skip rather than running an incomplete chain.
- Request and permanent-write observers: per-consumer protection in existing order; commit ACK independent of subsequent derived/observer errors. Store authority, persisted schema, native operations and formulas unchanged.
- Readiness: nine load-only writers use one idempotent latch. Actual Store WAITING blocks readiness; LoadScreenClose or first existing publish/turn after Store initialized triggers once. No repeated Audit once latched. Diagnostic self-registration cannot confer business readiness.
- UI: each constructor/Items/Sync/Before/Publish isolated; native project and unit rows restored after a failed mutating adapter. Rollback requires per-call copies of both lists for callable Items adapters (at most six current render adapters); none for absent/optional no-Items adapters. This is an explicit local UI allocation cost, not an allocation-neutral claim. Exact failed SPC selections fail closed; native selections continue. Context shutdown removes owned hooks and identity-matching readers only.
- Gates: unchanged S2 S3 target assertions, late-listener/consumer/exit quarantine, startup order/dependency/epilogue, observer sibling/commit proof, no-frame readiness, actual adapter restoration and shutdown. Keep inherited tests separate from Lua51 program closure. No gameplay changes; U5 native acceptance remains required.

## Results and evidence boundaries

**LOCAL_SIMULATION_PASS:** all four unchanged S2 target assertions now pass: investment post-commit ACK/sibling isolation, late Start survival/seal/failed-listener quarantine, native UI list survival and Store committed-identity survival after an observer exception.23 added S3 cases cover missing/throwing Remove, Add-then-throw, identity-preserving duplicate registration/removal, callable events and synchronous reentry, failed internal exit/return/GW callbacks, Store legacy-mode skip, actual Start order, independent failure scope, old Dialogue retirement, partial external view rollback, diagnostic registration failure, all nine actual readiness writers, no-frame WAITING/one-shot behavior, truthful skipped-writer diagnostics, missing/nil/throwing UI guards, exact Crew fallback, dynamic export cleanup/newer context, constructor rollback and shutdown/event isolation.

The full Lua5.1 program runner executes50 cases:41 passing properties,9 explicitly OPEN S4/S5/S6 counterexamples, no unexpected failure. [Executed closure](Specialization_B273_Refactor_S3_Closure.json) distinguishes actual complete modules, failed-partway execution, source fragments and isolated Start doubles. It does not claim that every production Start ran against the real engine.40 selected inherited unittest methods and the selected B270 real-positive-effect fixture bodies pass. Older backends remain as authored.

Three fixture setup assumptions initially failed after the authorized latch: two B270 cold fixtures had already delivered an initial Load before seeding their supposed cold state; the selected historical P0-C profile used a second Load to recover a changed reference. Current B270 cold setup now defers its first Load; the explicit current P0-C profile delivers the already supported relevant PlayerTurnActivated event instead. All assertions are unchanged; frozen `test_p0_c.py` and previous evidence remain byte-identical. No failure was hidden by relaxing an output/recovery assertion.

**STATIC_CONFIRMED:**192 runtime Lua files compile under Lua5.1;25 XML parse; modinfo300 lists314 package files exactly. Three new packaged helpers, no SQL/save schema/formula change.100 heuristic review alarms remain below the reviewed S2 baseline; this is not proof all old debt is fixed. Native/HD base OnShutdown linkage was read-only verified; external sources were not copied or modified.

**Runtime limits:** rollback copies are local to each callable UI Items adapter/render (up to six adapters over the native lists); absent/no-Items adapters do not copy. This cost is explicit, not an allocation-neutral or native-memory improvement claim. No timer/periodic scan/retry was added. Startup tracks finite static module/event/function registrations; it does not retain new native city/player objects or roll back native writes. Failed internal cleanup remains unconfirmed, never falsely ACKed. Sealed means composition finished; FAILED/SKIPPED and Store/business readiness remain separate.

Native callback delivery, UI context lifetime and final integration remain **USER_GAME_TEST_REQUIRED** at U5. No newly identified native fact blocks S4 continuation. Stable/live remain B271.298; no deployment, main action or game launch.

## Handoff

- **User decision:** none for routine continuation; accepted U1 and eight-era correction remain.
- **User testing:** none now; U5 final integration, earlier only a concrete blocking native fact. No new USER_GAME_TEST_PASS.
- **Primary next:** S4 diagnosed Great Work/Industry/GC/native scope and D1/D2 network hold/recovery; internal U2 checkpoint then separate approved A8 correction before S5. No automatic deployment.
