# Architecture Reconstruction — investigation workspace

Investigation / Non-authoritative / No design decision implied

Status: Stable — reviewed investigation checkpoint, 2026-10-28. Stable means evidence ready for review, not architecture approval or native acceptance.
Maintainer: Primary. Baseline: develop 19d4669d11df945afcda9d73329dfb984fe8c694; runtime B393.420, D0058 / A0183 / S0850. Tracked tree was clean on entry; publication adds only the eight new investigation Markdown files. Runtime source and existing documents remain byte-identical to this baseline.

## Purpose and authority

This package provides two corresponding views: actual transitional implementation (As-Is) and the expected architecture after the already approved refactor (To-Be). The latter is useful before implementation finishes; it cannot invent undecided responsibilities. All reports and Mermaid diagrams are investigation evidence, not Architecture Authority. Approved Architecture Markdown prevails. Record any conflict for owner review; do not choose a preferred interpretation or implement directly from a drawing. Approval state and implementation state remain separate.

Only new delivery Markdown in this topic is writable. No source/configuration, existing documentation, history, formal Architecture/Design, Status, governance, authority entry or Context Lock is changed. No new formal Architecture Workspace, document migration, refactor, runtime probe, test or deployment is part of this task. Mermaid is the primary diagram source; no draw.io duplicate is maintained.

## Reading navigation

| Reader question | Report |
|---|---|
| How does the current code fit together? | [As-Is overview](As_Is.md) — start here |
| What should the accepted refactor produce? | [To-Be expected architecture](To_Be.md) — approved requirements and current gaps |
| What happens after a particular trigger? | [Event chain atlas](Event_Chains.md) — E01–E10 |
| Who owns each fact, cache, history and applied result? | [Shared state matrix](Shared_State.md) — F01–F13 |
| Where are collection scans, turn work and deferred recovery? | [Scan inventory](Scan_Inventory.md) — S01–S33 |
| What differs, and what is still unknown? | [Consistency and questions](Comparison_and_Questions.md) — C01–C12, Q01–Q08 |
| Where is a particular Lua file in this map? | [Module index](Module_Index.md) — M01–M14, 218 packaged Lua files |
| Which direct native listeners have distinct duties or overlap shared notifications? | [Direct Event Listener Audit](Direct_Event_Listener_Audit.md) — supplementary four-profession audit at `abcc2b0`; classifications and source evidence |

Read As-Is and To-Be first; open only the event/state/scan details relevant to the question. Group IDs are investigation navigation labels, not proposed runtime services or a new authority registry. To-Be local T01–T24 labels are distinct from Workflow T01–T08 validation gates.

## Coverage and explicit limits

| Area | Completed | Boundary |
|---|---|---|
| Package and modules | 218/218 packaged Lua mapped; ordered startup and four-profession representative paths | File inventory is not full-body/function-path audit; 17 files marked targeted in the module subtask, other reports trace additional named paths independently |
| Events | Startup/load, founding, first qualification, acquisition/loss/recapture, facts, projects/Crew, route transport and turn/recovery | Native availability and event arrival/reentry order remain unproved |
| State | Permanent Store, effective facts/D, invalidation generations, network/Great Works, histories, deferred and derived recovery, carriers/UI | No universal currentness claim; production cold Commerce/Culture attribution remains incomplete |
| Scans | 33 sites/groups distinguish targeted, initialization, turn, recovery, request-only and retired branches | Not every loop in every diagnostic/UI/SQL file; no runtime frequency or performance attribution |
| Target | Approved U1/A0183 responsibilities, four professions, UI/startup/retirement and outstanding integration | No new architecture or automatically adopted Advisor recommendation |
| Consistency | Source-backed comparison, stale completion prose, incomplete applied-value display/cold attribution, native unknowns | Existing documents remain untouched; concerns are not automatic repair authorization |

Evidence: STATIC_CONFIRMED source/document reconstruction only. Previous B393 scoped user testing is cited as recorded evidence, not rerun or expanded. No tests, game, profiler or new listeners were executed.

## Comparison guide

Use the same subjects across the two views. As-Is groups M01–M14 describe actual code families, not a recommendation to preserve their boundaries. To-Be T01–T24 reconstruct accepted responsibilities; its E01–E10 counterpart table matches the actual event atlas. F01–F13 explain state ownership; S01–S33 show work scopes; C01–C12 compare implementation and documents. These labels are local navigation only, not new governance or validation-gate IDs.

Three important current-to-target differences are documented without fixing them: production Commerce/Culture cold attribution is not integrated merely because its adapter exists; applied-value institution display still has candidate arithmetic; retirement must preserve load-bearing cleanup/read/receipt duties before file removal. Other apparent overlap is recorded as a question, not assumed waste or architectural error. The detailed comparison retains approval-versus-implementation and code-versus-native evidence boundaries.

## Document validation and publication

- Fixed source HEAD and the 218-file package/index mapping were rechecked after resume. No tracked input changed during investigation.
- Three delegated authors completed bounded cross-review. Primary corrected the NetworkBoost retired-consumer description, disabled/no-op binding qualifications, approved-versus-proposed recovery wording and normative-conflict decision owner.
- All781 local file links, source line ranges and intra-package section anchors were checked. A resolving line anchor proves location, not the full semantic truth of its claim; substantive conclusions use the cited function/contract and bounded cross-review.
- All14 Mermaid diagrams render to valid SVG with Mermaid10.9.3 in an existing temporary headless Chrome instance, offline after the public renderer library loaded. Two literal-semicolon sequence-label errors were corrected. No browser/package was installed and no user profile was used. This verifies that renderer, not every future client renderer or all visual layout preferences.
- Context integrity passes341 runtime files and1277 guarded inputs without any authority/hash updates. No gameplay test suite, runtime probe, engine launch, deployment, optimization or repair was performed.
- Publication uses the existing Primary reviewed-Stable checkpoint and staged privacy/secret gate. Exact new report paths only; no raw game files, logs, binary outputs, generated full Closure, formal Architecture edits or default-context registration.

The earlier local save checkpoint was retained through laptop closure and resumed without restarting the investigation. This reviewed checkpoint is preserved by its Git publication; ignored drafts alone were not described as permanent backup. Source history at19d4669 remains the reproduction basis for this report's code anchors.

## Read Ledger

Stage A: root/project/investigation guidance; project and Architecture navigation; Workflow R9, language, checkpoint and reading rules; Authority metadata, Status CURRENT, P0-H routing; user prompt and final diagram-governance clarification. Stage B: modinfo and Gameplay/UI composition, actual calls/registrations/state access for shared infrastructure and the four current professions; accepted formal Architecture/U1/recovery references. No external Mod/HD scan, historical archive sweep, private disk search or live game inspection. Detailed ledgers remain in each report.

User decision: review the As-Is/To-Be views and any genuine conflict at the owner's pace; no new rule is required for publication. User testing: no additional immediate request; existing acceptance table remains user-owned. Primary next: deliver this reviewed investigation checkpoint and stop. Further architecture design, governance migration or runtime changes are separate authorized work.

## Supplementary direct-listener checkpoint — 2026-10-30

[Direct Event Listener Audit](Direct_Event_Listener_Audit.md) records the subsequent user-requested read-only listener review at develop `abcc2b0` / B396.423 metadata. It rechecks current registration/activation paths, parameters, shared-notification overlap, enumeration and recovery duties. The original B393 baseline, coverage and validation statements above remain historical statements about that earlier checkpoint; this addition does not refresh or supersede those reports. The audit remains non-authoritative and does not approve listener deletion or a centralized-push redesign.
