# B235 native review and B236 proposal

Evidence: **USER_GAME_TEST_PASS — scoped Engineering results**, with **USER_GAME_TEST_FAIL — same-turn Industry IV entry refresh** retained for the next batch. Review baseline: develop `324b326`; source/live B235.262 / modinfo262 from `fb7a547f9c44f2173057dfa0dc5ab227f46e75a9`, receipt `B235.262-fb7a547-playtest.json`. Read-only comparison confirms235/235 tracked Mod files match runtime; main remains `e901a22` / B069.96. No implementation, deployment, configuration edit or game launch in this review.

The user accepts the observed Standardization increase/withdrawal and their ordinary-Wonder acceleration calculation. They did not independently measure the incremental12/14% construction arithmetic because of native floor, and accept reuse of the existing construction carrier. Retain B234's native baseline and B235's local projection evidence; do not relabel the unmeasured increment as a new controlled native comparison or demand a repeat just for completeness. [B235 local result](Specialization_B235_Engineering_Local.md) and prior frozen results are unchanged.

## Evidence retained

Original collector files remain ignored under `local/diagnostics/B205/`. B205 is the reused collector label, not the tested build. Build attribution uses the user submission and verified deployment provenance. The first session has183/183 contiguous records and ends GAME_EXITED; the second has48/48 contiguous records and fresh context instances at T20, ending INTERRUPTED at the collector. Neither summary reports an alert. Transport reconnect/partial-frame events in the first collector do not leave a gap in the retained scalar sequence; they are not gameplay failures.

| Original relative to collector root | Bytes | SHA256 |
|---|---:|---|
| session-20261018T055739Z-d853a2/records.log | 67146 | `9ab2cd1b1e424766c0b5251d2dfdd2b78cb4fa9ad19ad738af4704378e1aa75e` |
| session-20261018T055739Z-d853a2/events.jsonl | 4862 | `6017caa574c890ae551b24e426e7cab567e8ecdf61b16fdad0ca7ec654e41f3f` |
| session-20261018T055739Z-d853a2/summary.txt | 618 | `491c64f615f5071bed032a1fa80a3fa22eceec55762659fabf60e0cd1a48d875` |
| session-20261018T061202Z-0aeb1d/records.log | 14826 | `fb4489fc8446ca4cf770476dd92335f1a78f90f885b4db61b70c658c98d62303` |
| session-20261018T061202Z-0aeb1d/events.jsonl | 654 | `94470717c22ee114690181ffab0d949c3277e37db922643e695aa1fd933ea12e` |
| session-20261018T061202Z-0aeb1d/summary.txt | 420 | `37074fb5c23c90e4633104e6299e3a5ee787a925df9788cd6b7792bdaf47320f` |

All three submitted screenshots were viewed, then moved byte-for-byte from `ScreenShots/` to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B235/`; its local manifest records the association. Originals are not committed or publicly embedded.

| Screenshot | Bytes | SHA256 |
|---|---:|---|
| 1: Screenshot 2026-10-17 at 11.07.53 PM.png | 12777572 | `c0e9875164b06bf9eba73c070c7c0f4e621854cce0cc20e8c0a04e2f79777a8d` |
| 2: Screenshot 2026-10-17 at 11.08.04 PM.png | 12492304 | `f3814780d09ffbac3c9d3959ef09dd90ff02cb8e73d3b7a839d3d43395b90864` |
| 3: Screenshot 2026-10-17 at 11.10.52 PM.png | 9878887 | `01ce13f4025724245631663c60bb23d02095d268b9332ceb938fdab6a003fa18` |

## Observed results

| Check | Evidence | Conclusion / limit |
|---|---|---|
| First study | First session seq52 ACTIVE at T13/L0/E1, due14; seq61 CALLING, seq64 T14/L1/E1 | One full-turn completion increases L exactly once; then EST_KNOWLEDGE_REACHED |
| Second study | seq179 ACTIVE at T19/L1/E2, due20; seq180 CALLING, seq181 T20/L2/E2 | Second completed study adds one layer; no extra layer beyond current E |
| Enhanced projection | seq66/68 Standardization12 VERIFIED; seq81/82 zero after source withdrawal; seq156/158 restore12; screenshot3 shows14% construction/4% building purchase | Observed update/withdrawal/recovery accepted; this withdrawal reaches no eligible source, not an isolated III10/0 fallback measurement |
| Saved L and cold restore | First collector GAME_EXITED; fresh session seq4 history COMPLETE/revision6, seq25 L2/E2; seq39/40 Standardization14 VERIFIED; seq31 Wonder ACTIVE4 with era9 | Saved L and current derived effects recover; initial network wait resolves in seq46 AVAILABLE at1/1 proof |
| Gold purchase | Three native production purchase lists and the table below | Observed native price quotes fit the requested0/2/4% discounts and5-Gold downward rounding; no actual debit was captured |
| Megaproject Engineering | User explicitly checked actual acceleration; first-session seq60/154 and restart seq31 confirm current ACTIVE4/era9 projection | USER_GAME_TEST_PASS for the user's tested ordinary-Wonder case; scalar records alone do not reconstruct production inputs or every era gap |
| IV entry delay | User reports new Industry IV investment leaves Study and Macro unavailable until next turn, also visible in P0 | Confirmed user-game defect; merge the scoped repair into B236, not a new standalone test |

The native trace contains no cancelled ACTIVE study attempt: L1 persists through qualification loss, then a fresh L1→2 attempt succeeds, but that does not independently prove interruption of an unfinished attempt. Cancellation/III fallback retain the existing targeted local evidence; no additional native session requested. Legal Faith purchase was not shown; target-specific District purchase remains the prior isolated technical gap. The final construction-report row points at a normal product project and reports expected0, which is consistent with Standardization's target scope, not a lost14% building/District enhancement. All observed network waits resolve; no new blocking failure was found in the reviewed records.

## Gold quote calculation

Screenshot1 is the user's0% reference in **Mecca**; screenshots2–3 are2%/4% in **Edinburgh**. This is not a controlled same-city before/after test. Across the common listed buildings, all affected values fit:

`quoted Gold = 5 × floor(reference price × (1 − discount) / 5)`

| Visible building(s) | 0% reference | 2% quote | 4% quote |
|---|---:|---:|---:|
| 法表 |200|195|190|
| 粮仓 / 磨坊 / 测量仪 |240|235|230|
| 水力作坊 / 风车 |400|390|380|
| 建造工坊 / 手工工场 |800|780|765|
| 工厂 / 电子厂 / 化工厂 |1600|1565|1535|
| 燃煤发电厂 |2000|1960|1920|
| 燃油发电厂 |2200|2155|2110|
| 核电站 / 互联网公司 / 物流中心 |2400|2350|2300|
| 会展中心 |600|600|600|
| 警署 |880|880|880|

Examples:800×0.98=784→780;800×0.96=768→765.1600×0.98=1568→1565;1600×0.96=1536→1535. The effective percentage inferred from the displayed integer can therefore exceed2%/4% slightly. This empirical quote fit is not a claim about every internal modifier ordering. No rounding compensation is proposed. Gray/unavailable entries corroborate quotes, not purchasing rights.

The unchanged Exhibition/Police entries belong to separate template groups in [StandardizationCatalog](../../../../Mod/StandardizationCatalog.lua), rather than CENTER_BASIC. Their unchanged price is not evidence that the other matched-template discount failed; the screenshots do not independently prove those two groups' holder inventories.

## IV-entry repair boundary and next batch

[Gameplay](../../../../Mod/Gameplay.lua) already calls `EngineeringStudy.Refresh` and `IndustryWonderEffects.Refresh` after a proved COMMITTED investment, for both normal Settler and DEV entry routes. [InvestmentAction](../../../../Mod/InvestmentAction.lua) returns the city ID and final receipt; [EffectiveFacts](../../../../Mod/EffectiveFacts.lua) derives ACTIVE from committed investment and Governor properties. Study/Wonder also have existing event/load readiness paths. It would be incorrect to call the missing update a proven absent hook or to patch it with a timer.

The exact failed native ordering is not in the retained scalar log. The next batch must first reproduce the real post-investment route with authoritative facts arriving before/after the notification, then correct only the affected dirty/publication/recovery ordering. Keep the proved receipt requirement, UNKNOWN and same-turn changes; no broad scan, forced effects, repeated commands or P0 prerequisite. Add only bounded existing-trace fields if needed to make a remaining failure actionable.

The [B236 proposal](../../../Architecture/v2/Industry_Preparation.md#b236-proposal--construction-teams-and-industry-iv-entry) combines that repair with IND-4: Crew formation/source capacity and Engineering Practice, Wonder-only fixed injection and required protection. New cost/grant/source binding must be established before release; if a native gate requires changing accepted gameplay, stop that subpath for the user's decision. Culture HOLD and District-purchase investigation stay separate.

## Review checks

Reference/schema/selector integrity and context-helper self-test PASS (235 runtime files,731 locked documents);404 scoped Markdown links/anchors resolve. Archive SHA256 matches all3 originals. Diff review is limited to6 documentation/metadata paths; all unrelated locked hashes, Mod, Design, tests and prior results remain unchanged. CURRENT stays7 lines,1049 bytes versus1151 before. No gameplay regression was rerun; the staged publication gate applies before commit.

User decision: approve or revise B236; no new Design decision requested by this review.
User testing: no extra B235-only session; IV-entry check joins the future Crew session.
Primary next: documentation/context/publication checks and commit/push, then stop. B236 implementation/deployment requires approval.
