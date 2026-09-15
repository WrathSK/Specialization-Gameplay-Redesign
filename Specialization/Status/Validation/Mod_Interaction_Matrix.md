# Mod Interaction Matrix

Document Owner: Codex
Current runtime: B072.99 / modinfo99 (unchanged)
Purpose: smallest known reproducing set / largest known non-reproducing set within observed conditions, not global proof.
Dependencies and exact UUIDs: [audit](../../Reports/Technical/Specialization_Mod_Interaction_Dependencies.md).

## Sets (exact third-party membership via audited aliases)

- BASE = SPC + BTS + EMM.
- FULL11 = BASE + CORE + CIV + DIST + IND + PRODUCT + TYCOON + TITLE + AREA.
- H = BASE + CORE.
- U = CIV + DIST + TITLE + AREA (legal on H).
- E = PRODUCT + TYCOON + IND (legal on H; IND requires the first two).

CORE=Civ6 Plus; CIV=Civilizations & Leaders; DIST=District Expansion; IND=HD Industries & Corporations; PRODUCT=Monopoly++ Corporation and Product Adjustments; TYCOON=Monopoly++ Tycoons and Investors; TITLE=Mods Title Localization; AREA=Larger MODinUse Area; SPC=Specialization; BTS=Better Trade Screen; EMM=Enhanced Mod Manager.

## Observed matrix (unknowns retained)

|ID|Exact third-party set|Closure|Duration/time|Memory start→end|Observation|Crash|Notes|
|---|---|---|---|---|---|---|---|
|O0|BASE|Official SPC expansions retained; third-party closure complete|User's window, duration UNKNOWN|UNKNOWN|No sustained growth observed|Separate earlier construction-list crash; not equated with memory|User confirmed multiple checks; map/mode details not independently captured; not permanent PASS|
|O1|FULL11|Complete|Sep14 crash21:25:30; user idle4–5min|UNKNOWN|Slow growth reported|Yes, native pure-virtual abort|PID39989; exact50 entries/11third-party archived; no Switch Civilization|
|O2a|FULL11|Complete by user confirmation|21:32:19→21:38:35;376s;Turn1/0city|9.23→9.59GB|Growth observed|None in window|PID41293; Activity Monitor Memory; mode ON user confirmed|
|O2b|FULL11|Same|21:38:35→21:44:24;349s|9.59→10.10GB|Growth observed|None in window|Includes founding first city; not pure idle baseline|
|O2c|FULL11|Same|21:44:24→21:46:55;151s|10.10→11.87GB|Growth observed|None in window|Operations/Turn1→19/second city; not used as idle slope|
|O2d|FULL11|Same|21:46:55→21:52:12;317s;Turn19/2city|11.87→13.01GB|Growth observed|None in window|Discount18602, facts74408, city_scan148816; correlation not causation|
|T1|H|CORE requires only official expansions; BASE complete|PENDING 300s/0city|PENDING|USER_GAME_TEST_REQUIRED|PENDING|Only current assigned test|

Current largest known non-reproducing third-party set: BASE, under its reported observation window.
Current smallest known reproducing third-party set: FULL11, among tested documented configurations; not claimed irreducible. Protocol differences prevent precise rate comparison until controlled reversal. Original112 set stays frozen historical evidence and is not this investigation's BASE.

## Uniform protocol

Every trial is a NEW game, never an old save with different enabled mods. Keep same build, GS ruleset, official DLC/modes (Monopolies ON), map size/type/seeds where practical, game speed, human civilization/leader and AI roster where possible. Do not let added leaders silently change random AI selection. Retain current graphics/window/focus conditions. Fully exit/restart between configurations to avoid carrying the previous process allocation history; user performs all actions.

On first interactive Turn1: no founding, movement, end turn or Diagnostics. Record start timestamp/Memory, remain idle300seconds, record end timestamp/Memory and whether rise was approximately continuous. Keep capture timing after load consistent. External monitor already exists: reuse normal30s trends, preferably auto-snapshots OFF identically in all trials; no new setup needed if Activity Monitor endpoints are easier. Compare like metrics (Activity Monitor Memory vs same; monitor physical_footprint vs same), never RSS vs Memory. Report crashes separately; a crash-shortened window is not a clean negative.

Return only enabled group, start/end time, start/end Memory, observed trend/crash, monitor session if captured. No fixed GB/min PASS cutoff. If indistinguishable, mark INCONCLUSIVE; only then consider matched two-city300s windows. Never repeat full five-stage sequence per combination.

## Adaptive decision tree (not a request to run all)

Test0: BASE already observed negative; do not repeat now.
Test1: H only (four third-party Mods).
- Growth returns: Test2=BASE (remove CORE), Test3=H (restore CORE). Stop additions. Confirm reproducible ON/OFF/ON association; this identifies CORE-added closure interaction, not sole culprit or exact script.
- No growth: Test2=H+U (add CIV,DIST,TITLE,AREA together).
  - Growth: Test3=H (remove U); then restore H+U in a later confirmation before splitting U into {CIV,DIST} and {TITLE,AREA}.
  - No growth: Test3=H+E (replace U with economic closure). This is a sibling subset compared against H, not one-mod contrast against Test2.
    - Growth: next remove E→H, then restore E before subdividing. To distinguish IND from its dependencies, test H+PRODUCT+TYCOON before adding IND; both Monopoly++ may be split individually if the pair reproduces.
    - No growth: neither half alone reproduces; do not exonerate either. FULL11 retest checks cross-half interaction/reproducibility. If reproduced, minimize by legal removal with dependency closure and retain each negative/positive set.

At first candidate-positive stop adding components; remove the LAST added closure and re-enable under same protocol. Unknown/inconclusive is not negative. For group splitting keep closure consistent; never leave IND enabled while disabling either Monopoly++ dependency. Maximum3 upcoming conditional trials described; currently user only needs T1.

## Priority contract

No DISCOUNT_AUTO_AUDIT_OFF, trigger instrumentation, formal Discount optimization, Batch C/D or compatibility patches until smallest-known set investigation is reviewed. Existing C² issue retained as independent performance debt. Once candidate closure is confirmed compare Discount behavior in BASE vs candidate to find interaction boundary, not pre-assume Discount root cause. Crash and memory outcomes remain separate columns. No new test outcome fabricated.

## Follow-up 22:32–23:04 (supersedes pending assumption that T1 was run exactly)

[Results](Results/Specialization_Mod_Isolation_2232.md). Run1=BASE+CORE+TITLE+AREA,1city204s9.30→9.50GB;2city203s11.08→11.76GB. Smaller known growth-observed set now six Mods, not an irreducible set. Run2=noHD+Cheat,3city1121s9.30→9.69GB; user confirms both helpers retained; Cheat UUID not independently captured, no new largest non-repro declared. Same PID45352 both runs. No crash captured; independent monotonic time series absent. Initial four-Mod T1 remains untested. Prefer next controlled CORE-only toggle with helpers+Cheat fixed; user confirms main-menu-only switching; no addon expansion or Discount change.
