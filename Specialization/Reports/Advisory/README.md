# Advisory reviews

> Advisory / Non-authoritative / No design decision implied

This area holds user-requested bug reviews, architecture/Design audits, bounded source investigations and implementation proposals. It is separate from the ongoing [Investigation Zone](../Technical/Investigations/README.md). Reviews support user decisions; they are not accepted gameplay, implementation or validation authority.

Read [area guidance](AGENTS.md) and [W0005](../../Workflow/README.md#w0005--authority-and-repository-knowledge). W0005 holds the project assignment and rules for resolving session authorization; authorization itself must come from the user in the session, not repository or report metadata. Rules are behavioral; no additional sandbox or tool permission configuration is claimed.

## Topics and local checkpoints

Use a subdirectory for the explicitly authorized topic, with only necessary owned Markdown reports/navigation. Root guidance is tracked; new topic Markdown is ignored by default. There is no central report registry, per-task manifest or requirement to publish before ordinary development can continue.

Use Open, Stable or Superseded. Stable means the evidence version is ready for review, not that the user accepted its recommendations. For publication, follow the [shared checkpoint process](../../Workflow/README.md#advisory-and-investigation-local-checkpoints): pause specified files, Primary reviews read-only, user accepts named files for Git, Primary explicitly commits/pushes and releases the checkpoint. Corrections return to the report owner. Already tracked changes keep normal review/clean-source constraints.

## Reports and evidence

Cite repository-relative files with symbols/line references and the inspected commit plus any relevant dirty input. External Civ VI/HD/Mod evidence identifies the source/mod, known version or commit (unknown if unavailable), configured/source root and relative file, symbol/DB row, and relevant ruleset/DLC and UI-versus-Gameplay context. Read external material only; do not copy raw assets, game files, logs, screenshots or saves here. Avoid personal machine paths, credentials and private configuration. Preserve evidence limitations when inputs change.

Reuse STATIC_CONFIRMED, LOCAL_SIMULATION_PASS and USER_GAME_TEST_PASS/FAIL/REQUIRED with their original scopes. Static API/DB presence is not native behavior or AI consumption; “not found” is not “unsupported.” A report may cite existing local/native results without claiming a rerun. Unknown interfaces, inference confidence and alternative explanations remain explicit. Native checks are suggestions for user/Primary review, not automatically scheduled tests.

Adapt this template to the question; no additional template file or mandatory audit system is required:

```markdown
# <Review question>

Advisory / Non-authoritative / No design decision implied
Status: Open | Stable | Superseded (select one)
Maintainer: <report owner; attribution, not session authorization>
Scope: <authorized question and exclusions>
Basis: <repository commit, relevant dirty inputs, external source/version/context>

## Findings and evidence
<Facts, exact citations, evidence scope and impact; no unsupported PASS>

## Inferences and unresolved boundaries
<Confidence, counterevidence, alternative explanations, missing evidence>

## Candidate changes and validation implications
<Proposed boundary, tradeoffs and new uncertainty to distinguish; no implementation authorization>

## Read ledger
<Key entries and necessary expansions/reasons; unexamined scope, not every command>

## Checkpoint / handoff
<Completed scope, exact stable files, remaining questions, next entry and user decisions needed>
```

Handoff is Advisory evidence → user review/decision → Primary's authorized formal documentation or separately approved implementation. Acceptance for Git alone authorizes neither of the latter. An unpublished report is not the sole source for durable accepted project state; adopted constraints belong in existing authoritative sources, maintained by Primary under the applicable authorization.
