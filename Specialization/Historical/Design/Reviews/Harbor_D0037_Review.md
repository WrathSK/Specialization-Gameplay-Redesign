# Harbor D0037 — accepted baseline and Military naming amendment

Date: 2026-10-02
Decision authority: User Harbor Design Talk Handoff, explicit request to establish new current baseline.
State: ACCEPTED FUTURE DESIGN; names / Balance / Technical / Legacy maturity retained.

## Authority and scope

Formal content: [Harbor D0037](../../../Design/Content/Harbor_D0037.json), [Military D0037](../../../Design/Content/Military_D0037.json), [current Spec](../../../Design/Specialization_v0.1_Design_Spec.md). Complete human reading: [Harbor](../../../Design/Harbor.md), [Military](../../../Design/Military.md). This is an acceptance/supersession record, not another gameplay authority or implementation plan.

User adopted 100% maritime commerce + 100% naval military and simultaneous sibling institutions at III/IV. Accepted systems: II crew Housing/Admiral points; III domestic marine-resource network and international market breadth; IV Base-only export, civilization-relative locked imports and permanent operating-time capacity; naval III training/logistics and IV mentorship/insight/local tradition. No extra Harbor Network or naval Commander City.

Military changes only 行伍制度→行伍编制 and 后勤编制→战地勤务. All D0034 Military gameplay contracts, parameters and other names remain unchanged. Harbor now explicitly mirrors those current mechanisms; Aerodrome does not automatically follow. Current v0.1 remains Research/Culture/Industry/Commerce only. No runtime, Architecture adaptation, prototype or deployment.

## Conflict and supersession audit

| Existing source at D0036 | New accepted treatment |
|---|---|
| HARB-001 full dual identity | Retained, now simultaneous commercial/naval institutions at III/IV |
| HARB-002 unspecified Merchant/Admiral and marine-improvement yields | New II explicitly has Housing/base Admiral GPP, amounts TBD. Unassigned old Merchant/improvement wording is not converted into an invented extra ability; residual scope remains unresolved |
| HARB-003 all own-city marine resources, not adjacent-only | Retained local resource Base adjacency scope; new port-link adds raw resources from other own qualified feeder ports. Existing ownership/improvement details remain open |
| HARB-004 Export, own-city higher Actual/local ratio | Superseded by Base-only connected-district input, add to each outgoing qualified maritime route then market multiplier. No own-city Actual exception |
| HARB-005 early Military mirror / Naval Mobilization | Current Military mirror expressly accepted; naval mobilization, Commander City and independent Harbor Network not adopted |
| HARB-006 II +15% normal combat XP | Retired; crew institutional Housing/GPP replaces it |
| HARB-007 III Insight, dynamic source specialists | Replaced by IV current Military Insight: permanent E_birth, current actual promotions |
| HARB-008 continuous garrison training | Retired; not added alongside new IV abilities |
| HARB-009 old mentorship | Current same-PromotionClass / permanent entitlement mirror, no unconstrained old class formula running in parallel |
| Military old ability names | Two user-authorized renames only; unchanged mechanics |
| Earlier “Harbor/Aerodrome not yet adapted” active reading note | Harbor now explicitly adapted by Design; Aerodrome still open |

The handoff calls old Export “HARB-003”; actual D0036 places Export at HARB-004, while HARB-003 is marine adjacency. Audit follows the actual rule content, not the inconsistent number. [D0036 snapshot](../../../Design/Revisions/Specialization_Design_Spec_D0036.md) retains exact pre-amendment bytes; no prior frozen records rewritten.

## Preserved maturity and boundaries

- 船政局 STRONG_FREEZE_CANDIDATE; five other institution names PLACEHOLDER. Ability names keep READY_TO_FREEZE (可冻结), STRONG_CANDIDATE or TENTATIVE; accepted mechanism does not silently lock a name.
- Remote +1 is a first balance-test preference, not final. K, export curve/yields, import effects, operating thresholds and naval pending values remain unset. C6 triangular milestones and median-ratio classifier are candidates only.
- Harbor numerical overrides remain TBD even where the mechanism mirrors Military. No automatic final Harbor 3F3P, Housing/GPP or breadth-CS values are inferred. Current Military own fixed values remain untouched.
- Trading relations preserve exact 0→1 lock / last 1→0 removal. No anti-reroll/era lock. Export cannot recursively consume its output or Harbor-derived yields. Market diversity remains linear, not automatically diminishing.
- Operating growth: ACTIVE IV + at least one domestic/international maritime route, +1 per eligible turn independent of route count. Loss ACTIVE IV pauses, does not reset; earned capacity survives Governor movement/temporary loss. Owner transfer/respecialization/destruction not generalized from this permission.
- Naval current formulas and birth-buff/formation contracts mirror current Military; training efficiency remains a city effect. No Naval III Insight, garrison ability, old +15%, automatic native XP cap8 or E<=4 transplanted.

Open before dependent future implementation: qualified Harbor/resource predicates; maritime topology/Canal; direction and civilization scope of relation counting; domestic hinterland direction; export eligible domains/self contribution/heterogeneous yield aggregation; exact classifier and supply effects; assets across owner/identity/destruction; naval unit/support mapping. These are exposed in formal content and reading text, not silently chosen by engineering. They do not block accepting this baseline or the unrelated four-profession v0.1 work.

Community appeal-D / Shared-D and Entertainment support / current Culture network boundaries remain unchanged. Aerodrome old mirror remains independent. Canal adjacency and Diplomatic maritime mission contracts remain their own future designs.

## Current task revalidation

B148 / P0-L1 native Tourism gate remains pending. The current Culture Spec section, Culture/Shared content, runtime, writer boundaries and L1 context selectors are unchanged. Only authority version metadata is synchronized; Harbor/Military are not added to the Culture implementation reading set. Culture preparation remains planning-only. This acceptance records no USER_GAME_TEST and requests no new native test.
