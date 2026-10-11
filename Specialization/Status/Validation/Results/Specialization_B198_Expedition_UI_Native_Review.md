# B198 — native UI feedback and requested refinements

Evidence: five user-submitted screenshots, sorted by capture time on 2026-10-11, plus the user's written feedback. Build under review: **B198.225 / modinfo225**. [Local implementation basis](Specialization_B198_Expedition_Native_Layout_Local.md). Original images are archived outside Git at `local/legacy-workspace/Specialization/Status/Validation/Evidence/B198/2026-10-11/`; original names/bytes and SHA256 were verified during the move, with a local manifest.

## Observed scope

| Image | Evidence role | Observation |
|---|---|---|
| 1 | Ordinary Spy UI reference | Native city selection and adjacent mission list; selected-city header supplies the selection cue. |
| 2 | B198 relocation screen, T88 | Adapted city list/banner/drawer render; automatic city choice, gold outline and redundant travel preview remain. |
| 3 | B198 task screen, T88 | Expedition is shown at Alexandria; the no-reward two-turn task is automatically selected. |
| 4 | B198 after Start, T88 | Panel remains open, Start is disabled and selection-check wording appears. User reports the task started; missing close feedback caused uncertainty. |
| 5 | Ordinary Spy UI reference | Native mission list and confirmation presentation, not proof of an Expedition task outcome. |

**Scoped native presentation acceptance:** the user positively accepts the overall B198 direction and requests specific refinements. The task-start panel remaining open is a confirmed UI defect. The screenshots reach the destination task screen; they do not independently prove exact raw source/name/capacity continuity, ordinary-Spy recruitment during this session, task completion, END or cold loading. Unchanged earlier lifecycle evidence remains inherited within its recorded scope; B197's failed evidence is not rewritten.

## Authorized follow-up

No automatic city/task selection on opening; no selected-city gold outline; right-hand relocation drawer previews the implemented task rather than repeating travel duration; close after correlated accepted task start. Replace generic district icons with display-only mission locations: city center, positively readable eligible Great Work hosts and completed Wonders, using each Wonder's icon when available.

Foreign collection visibility/completeness is still a native boundary. Missing location data must remain visibly incomplete, not an empty-complete inventory or dispatch veto. This request does not authorize formal mission rewards, N2/N3, target-rule expansion, persistence or changes to capacity/binding/task semantics. The separate [B199 implementation](Specialization_B199_Expedition_Selection_Locations_Local.md) records local checks and the minimal delta test.
