# B226 — Culture Insight network and exact Eureka retirement

**LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** User authorized N3 implementation, exact old Culture Eureka retirement, retention of Research, and guarded deployment. Source B226.253 / modinfo253. B225 native tests are deferred into this single combined gate; they are not marked PASS.

## Accepted behavior and implementation

Each supported Culture ACTIVE IV source derives the civilizations for which its own reliable city history contains PEOPLE+WORKS+PLACES, excluding its current owner's civilization. Connected receivers union these independently complete sets. Two cities' partial categories never form a complete civilization. Receiver benefit is +1 Culture × union size per actually working specialist matching that receiver's single Identity; receiver ACTIVE is not an extra requirement. Received payload is not written into city history or re-exported. Existing direct source→center, center reception, capital self-connection and one-hop distribution remain unchanged.

`CultureNetwork.lua` owns32 exact internal district specialist carriers (four current identities × eight bits). `Building_CitizenYieldChanges` is the existing native per-worker primitive, already used for ResearchApply Culture. It adds no slots, flat city yield, GPP or permanent worker count. The current first qualified district is verified; unexpected multiple identity districts HOLD rather than select an arbitrary one. Presence, location and pillage are preflighted before mutation; obsolete effects are removed before current ones are added and read back. Pre-write UNKNOWN retains only an already confirmed same-reference projection; actual partial-write failure is reported and owned partial effects are cleaned when readable.

The eight-bit encoding covers0–255 and validates the loaded civilization catalog (101 definitions in the configured DB inspected for this batch). It is an explicit implementation coverage bound, not a new gameplay cap; out-of-range/unknown definitions fail visibly without clamping. Each source's existing Store record bound remains unchanged, and multi-source unions are not capped at64.

| State / input | Owner and lifecycle |
|---|---|
| Permanent Insight/category records | Existing CityProgressionStore; unchanged schema and first-success receipts. |
| Current topology | Existing NetworkBridge; additive CurrentCultureBatch returns copies, with no new capture or public-bucket dependency. |
| Source eligibility/history sets | Re-read and memoized once per synchronous consumer batch, discarded after it; current owner and ACTIVE IV independently rechecked. |
| Receiver effects | Sole CultureNetwork writer; exact source/receiver references, owned carriers and current district. No received history. |
| Pending updates | Bounded per-supported-player dirty city set, drained by existing GameCoreEventPublishComplete. Busy notifications survive; no timer. |
| Return / loss | Store Return only marks until new facts commit; confirmed exit removes exact effects. UNKNOWN does not turn into an empty source. |
| Actual workers | Native engine scales the district coefficient. Worker-only changes need no duplicate fact/ledger collection; report reads current workers on demand. |

A successful task independently calls SourceChanged after its reliable history write, even if the route signature did not change. Bridge publication notifies the new consumer. Source/receiver qualification, owner, relevant district and load paths re-evaluate affected projections; changed source scope selects its current/prior dependants. The existing one-way NetworkIsolation now includes all six owned writers. No frame scan, new timer, global AI history, new save field, task scheduler change or GC adjustment is added.

The existing **文化见闻** report now appends selected-city network complete-civilization count, matching workers and expected raw added Culture; the existing collector receives bounded `N1_INSIGHT kind=NETWORK` output. This is configured/expected output, not automatic native arithmetic certification. Other Culture modules and the Expedition cap/source/travel rules are unchanged.

## Exact old Culture retirement; Research retained

563 cleanup identities remain: B055 levels1–4 × recipients1–129 =516; B058 amounts1–45; B057 test amounts2/4. All1,126 native/HD attachments for these Culture buildings are removed from SQL generation/definitions. Normal NetworkBoost and its hidden TEST paths generate Research only. Initialization, confirmed exit and diagnostic isolation retain the finite old Culture cleanup catalogs. No prefix removal or global HD property reset occurs.

All Research SQL lines in the three affected SQL files are byte-identical to the B225 baseline, including1,126 native/HD attachment rows. Actual old/new Research formula, quantization, normal/Test/AUTO results were compared. Shared route topology and Research source/receiver semantics remain unchanged. The two small generator changes prevent regeneration from reviving the old Culture attachments; generated Lua catalogs are unchanged. Deployment tools are untouched.

Read-only HD2.2 source evidence: `HD/UI/Loaders/ToolTipLoader_TCP.lua`76–95 reads aggregate Tech/Civic properties; `HD/UpdateDataBase/DL_Wonders.sql`598–610 and `HD/UpdateDataBase/DL_GreatPeople.sql`169–173 own unrelated Tech boost contributions. HD is a configured external source label. Removing only this Mod's attachments/carriers preserves those contributions; no external source was edited.

## Audit-triggered boundary review

Relevant [follow-up priorities](../../../Reports/Proposals/Audit_Followup_Priorities.md) were rechecked. AF-14's general partial-topology policy is not adopted: the new consumer requires an AVAILABLE verified complete topology, holds same-reference projections on UNKNOWN, and withdraws on confirmed loss. It consumes copied current metadata/projections rather than extending published mutable-input alias dependence. P13a-Q04's128-route/16KB transport bounds remain explicit and unchanged; this batch adds no routes or wire rows. No general network/save/event framework refactor is bundled.

## Verification

**670 targeted tests PASS**, including26 B226 tests,617 related task/current-facts/Store/collector/helper cases retained from B225, and27 directly adjacent Insight report/Tourism tests. The combined643-case run and the adjacent27-case run each pass. Existing Python3.14.8 / Lupa2.8 lua55 reused. Actual Lua consumers/Bridge/NetworkBoost run with engine-shaped fixtures; disposable SQLite verifies SQL structure/attachments. No external DB writes, gameplay-wide regression, stress campaign or claimed native CPU/memory reduction.

New cases cover independent3/3, same-civ dedup, union beyond64, current-owner filtering, no recursion, direct center/capital self reception, source downgrade/restore and route loss, receiver ACTIVE0 and four identities/NONE, native worker scaling, no-topology-change task result, once-per-source history reads, scoped receiver updates, location/pillage repair, late UNKNOWN HOLD, failed write/readback, cold initialization, delayed Return, exact exit, all563 old IDs, unchanged Research normal/TEST output, generator reproduction, package imports and six-module isolation. An actual task/Gate completion test confirms notification only after the history write.

Independent read-only reviews found two defects in the initial draft: a never-contributing low source could defeat UNKNOWN HOLD, and pre-write unreadability could enter mutation cleanup. Separate contributing-source tracking and preflight-before-mutation now cover both counterexamples. Reviewers found no remaining blocker within these bounded paths. Three historical package-only pins193/199/200 remain excluded/not rewritten; old gameplay assertions were not weakened.

## One combined B225+B226 native session

Start the existing manual collector. Use the supported test campaign. Choose Culture ACTIVE IV source S, a receiver R with a specialization and working matching specialists, and a valid domestic connection: S→capital R is sufficient when R is the capital; otherwise use S→trade center→R. If S itself is the capital, use its native self-connection and a capital→R distribution route.

1. Use **文化见闻** to find an already complete foreign civilization or one missing a category. Prefer filling that category with **休眠 → 派遣到新城市 → 任务 → 开始任务**, then completion. Check idle controls on arrival and that **任务** can still open afterward, with completed rows disabled individually. For 艺文采撷, replace/move the original work while leaving another eligible one only if convenient; otherwise defer that subcase rather than manufacture a long setup.
2. Select R and open **文化见闻**. The appended network summary gives complete civilization count N, actual matching workers W and raw expected additional Culture N×W. Verify the corresponding district specialists' native Culture. Existing city percentage modifiers may affect the city total. Do not infer native yield solely from our configured report.
3. In active S, sell the last eligible Great Work; without ending the turn, verify current work eras / 风雅熏陶 clear, then restore a work. Historical completed Insights and R's network contribution should remain: network uses history, not current holdings.
4. Move S's Governor away so S falls below ACTIVE IV. Verify its network contribution disappears from R; other still-qualified sources remain. This is the decisive withdrawal check. No extra re-enable or saved-active/cold-load ritual is required.

Collector logs are primary evidence; screenshot only a visible disagreement. Stop on a task or yield failure and submit that session, without repeated blind attempts. If no complete civilization or legal mission target exists, report that specific missing prerequisite and defer only the network native gate; do not mark it PASS. Prior city Tourism/Floor/isolation acceptance is inherited, not a new test requirement.

## Delivery and stop point

Local implementation complete; live remains last verified B225.252 until the guarded B226 deployment record is filled. User decision: none. User testing: the single combined session above. Primary next: review that evidence. Reattachment, era UI, site movement, additional professions, new network formulas and unrelated audit repairs remain outside this batch.
