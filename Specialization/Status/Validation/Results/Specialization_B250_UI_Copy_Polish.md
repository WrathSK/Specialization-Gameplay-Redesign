# B250.277 — approved Chinese UI copy integration

Editorial review: 2026-10-18; implementation checkpoint: 2026-10-19. Basis: develop `c388fad`, B249.276 source `ad34b1f`, D0057 / A0176 / S0669. The user approved adopting the Gemini copy and then supplied the corrected attachment, requesting a descriptive rename and archive. This batch changes presentation strings only, plus build/current-review metadata. Gameplay, Design Authority, Architecture, formal tests, configuration, GC, main and frozen evidence remain unchanged.

## Scope and adoption

All203 handoff IDs resolve to the current source: **104 changed,99 KEEP**, with no missing or additional ID. The12 mapped source files still matched the editorial snapshot `1710c7e`, so no intervening text was overwritten. All16 institution names remain unchanged. Research/Culture/Industry institution help is polished; the four Commerce institution flavor descriptions remain KEEP, as the proposal requests. Its F4 question is not permission to invent a fuller mechanism description.

The7 F1–F3 factual replacements supersede their earlier COPY_ONLY variants in the same proposal:

- Culture Insights' local Tourism and Culture Network projections are implemented; retain the actual [B224](Specialization_B224_Native_Review.md) and [B232](Specialization_B232_Native_Review.md) acceptance scopes.
- Dialogue uses the accepted earned **Tourism-only** fallback. Remove the obsolete “records only” sentence, without promising amplification of Meaning or all native yields. See [B177](Specialization_B177_Dialogue_Cumulative_Native_Result.md).
- The normal Expedition has rewarded mission categories and the current destination interface. Remove prototype-only “no reward”/capital-only claims from the mapped normal strings. This does not close the held activity/release bugs or alter their scheduling.

| Source | Changed editorial entries |
|---|---:|
| `Mod/InstitutionPresentation.lua` | 8 |
| `Mod/Text/TestText.sql` | 26 |
| `Mod/Text/ExpeditionGate.sql` | 12 |
| `Mod/Text/Commerce.sql` | 28 |
| `Mod/Text/DevelopmentInvestment.sql` | 11 |
| `Mod/Text/Restructuring.sql` | 7 |
| `Mod/Text/ClaimProjects.sql` | 4 |
| `Mod/Text/DialogueProjects.sql` | 1 |
| `Mod/Text/EngineeringStudy.sql` | 1 |
| `Mod/UI/CityPotential.lua` | 1 |
| `Mod/UI/UnitPanelActions.lua` | 4 |
| `Mod/UI/DialogueProjectUI.lua` | 1 |

`Mod/Probe.lua` and `Mod/SpecializationP0.modinfo` change only build identification: B250.277 / modinfo277. No UI layout, control, event, timer, calculation, writer, saved field or API behavior changes.

## Integration safeguards

Eight entries receive narrowly documented wording corrections to preserve existing semantics, without changing the accepted style:

| IDs | Preservation |
|---|---|
| C-I3-HELP; C-DIALOGUE-02 | Success quota belongs to the **start game era**; each covered work era adds **5 percentage points**, not a new multiplicative5% bonus. |
| I-I4-HELP; I-STUDY-02 | E is civilization Wonder-era history/knowledge, not a scan of only currently existing Wonders. |
| S-BADGE | Potential is established investment level, not an immutable ceiling that restructuring can never reduce. |
| S-ACTION-02 | An uncertain HELD/PENDING/RESERVED investment result is not a cancellable preview. No instruction to cancel/retry is added. |
| M-CAPITAL-SAFETY-03 | Entering the deduction step is distinguished from proof that a debit completed. |
| C-PHASE-06 | HELD means state requires checking; it does not necessarily prove an active mission was interrupted. |

Names, formula coefficients, eligibility, Floor order, ownership/history distinctions and remaining implementation limits are retained. In particular, no Research network promise, Government/Diplomacy Meaning output, or precise District purchase discount is added. The `_250` identifier still displays the accepted260 base construction value.

## Local validation

**STATIC_CONFIRMED / LOCAL_SIMULATION_PASS within this text-only scope:**

-203/203 mappings checked against the effective source;99 KEEP entries unchanged. Runtime placeholders, icon/control tags and existing dynamic-value slots preserved. Editorial slot markers do not enter Lua.
- Executed all8 declared `UpdateText` scripts in load order in an in-memory localization database:1102 effective rows;90 intended Chinese rows changed, no added/deleted key. Existing SELECT-based Chinese fallbacks also propagate26 of those entries to `en_US`. No explicit `en_US` record or fallback SQL was edited, and no English translation was introduced; all other locale rows remain unchanged.
- All5 touched Lua files compile in Lua5.1. Removing only string-literal contents leaves byte-identical code and comments versus the baseline. Actual Lua rendering checks match all16 institution names/help strings and assembled investment/badge tooltips, including all three held-investment reason branches.
- The modinfo graph/file list is unchanged apart from version/description;265 runtime files remain present, uniquely listed where required.
-6 existing selected display methods PASS: ACTIVE/UNKNOWN retention, same-city identity refresh, selected-city/owner isolation, layout/static separation, Industry levels, and historical/current institution coexistence. No assertion was edited. The old full Culture display method hard-codes the retired “not implemented” help sentence; it was not selected as a current text oracle.
- Required context/hash, diff, navigation and staged-publication checks are completed at the commit checkpoint. Only named reviewed paths are rehashed; no blanket refresh.

These are local/source checks, not native layout or gameplay PASS. The user will observe wording, wrapping and tooltip readability during the planned v0.1 playtest. No new save/load sequence, yield test, game launch or separate test session is requested.

## Original editorial archive

The initial Desktop handoff was read only; it was not copied, renamed or edited. It contains203 unfilled proposal fields and is not the Gemini result.

The corrected download was moved, without rewriting its bytes, to ignored `local/editorial/2026-10-18/Specialization_v0.1_UI_Copy_Polish_Gemini.md`. Original filename: `gemini-code-1792389725812.md`. Size73,803 bytes; SHA256 `6a4177a320679eba98c5517cb9f49504e56afa494ed5d30afbe7efc7320433f5`. Pre/post move equality verified. The archive stays local; integrated source and this review are versioned. No screenshot, log, save or other external draft is included.

## Deployment and continuation

Local implementation is complete. At this source checkpoint the recorded live package remains B249.276, receipt `B249.276-ad34b1f-playtest.json`. B250 deployment requires the existing W0003 clean-source, process-exit and receipt/hash transaction; it is not inferred from committing source.

All [S0669 scheduling decisions](../../../Reports/Proposals/Audit_Followup_Priorities.md#v01-playtest-scheduling-checkpoint) remain: REALLOCATING cold-load and Standardization/Development addition belong inside the v0.1 playtest; the explicitly held features/audit work remain high priority afterward. Finish this copy/archive checkpoint and stop; no further gameplay batch is authorized.
