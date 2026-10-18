# B227 — Collector field-order repair and native follow-up

Scope: user authorized the collector fix and review of the latest Advisor report and submitted session. No runtime, Design, timer, deployment or gameplay repair. Runtime remains B227.254. This record supplements, rather than rewrites, the earlier B227 local/deployment evidence.

## Collector repair — LOCAL_SIMULATION_PASS

The diagnostic emitter places evaluationOrigin/signalOrigin before stage. Both readers incorrectly required stage immediately after seq. Activity records were therefore silently omitted. The collector now delegates to the fixed reader parser: exact B205 TRAIN prefix and numeric sequence remain required, with exactly one uppercase stage field anywhere in the record. The 4096-byte limit, rejection of multiline records, batch boundary and existing output allowlists remain. No new live query, polling, timer or gameplay command.

59 offline reader/collector tests PASS, including reordered snapshot/live records, deduplication, stage counts, wrong batch/sequence, missing/duplicate/invalid stage, multiline and oversize rejection. No live socket opened. Previously discarded records are not reconstructed; raw logs remain unchanged. The corrected scripts take effect on the next manual collector start; no mod deployment is needed.

## Native evidence

Ignored local collector sessions (not published raw):
- `session-20261018T002643Z-a4b85c/records.log`: SHA256 `45cc62ca1b5d3961d0e40a3dde62c60a59bde056ce75fbe10c09e710282fc3f6`.
- `session-20261018T003805Z-bc5531/records.log`: SHA256 `5105c9ed8483f8e40ddb037abf147a99c8f27ed0d54737a2d1fe2be06ff93fd6`.

- First session: two pre-request native SLEEP denials, including a newly trained/arrived team. Each unwinds to ARRIVED with no timer or award. Event delivery is working; native eligibility remains unresolved.
- New session: T75 seq8/12 and14/18 show rejected starts with clean ARRIVED return. Redispatch seq19 replaces native unit3342342 with3407878 on arrival; the latter has native Skip/Sleep ALLOWED. Another dispatch seq26 replaces it with3473414. T79 seq32/35/37 proves TASK_PREPARING → ARMED → ASLEEP/TASK_RUNNING, task due81. T81 seq41 confirms RELEASED → ARRIVED with ownership/pending cleared. Insight reports list Khmer WORKS effective=true; user confirms successful collection after returning to Khmer.
- At task release the selected-unit signature shows AWAKE with Skip/Sleep DENIED and WAKE ALLOWED. This is a concrete inconsistent-looking native action signature to investigate, not proof of the engine's internal cause.
- User reports redispatch restores normal operation. A persistent global lock is no longer the leading explanation. Successful redispatch changes both native unit identity and time/context, so it does not alone establish which clears the fault. No deliberate redispatch workaround or forced wake is introduced.

## Advisor review and bounded network investigation

Reviewed Stable `Reports/Advisory/Expedition_Task_Lifecycle/External_Civ6_Project_Research.md` and the related lifecycle review. Their external global-lock example is a candidate from another project, not a diagnosis of this session. Event-first scheduling is consistent with current evidence; FinishMoves remains an unverified alternative for this Spy-class unit, not implementation permission. No external project code was executed or copied.

Culture Network: user reports the P0 waiting message and absent expected bonus. `Mod/CultureNetwork.lua` Describe returns that same message for absent records, changed reference, city/global/player errors or failed worker reads. Audit retains errors in errors/error/playerError; the waiting branch emits no NETWORK diagnostic. Therefore this log cannot identify topology absence as the cause. Successful Insight history is distinct from a verified current network projection. The current source also requires all PEOPLE/WORKS/PLACES for a foreign civilization before it contributes; incomplete history would normally produce a confirmed zero, not this generic waiting message.

Direct read path: CultureNetwork.network → NetworkBridge.CurrentCultureBatch → private currentView; BackgroundRoutes → NetworkSender → NetworkBridge supplies the route input. BackgroundRoutes is event-driven, not a hidden frame scheduler. No evidence justifies changing that scheduling or bypassing UNKNOWN protection.

Next proposed scope (not implemented): expose the existing bounded network error/input status in the waiting report and collector; investigate the task's post-release/arrival native action state and WAKE gate against the native UI shape. Use existing evidence first, no blind repeated native test. Gameplay repair requires separate approval. Culture Network yield/withdrawal remains unaccepted; B227 has scoped startup/completion/release success alongside recurring eligibility failure, not overall PASS.
