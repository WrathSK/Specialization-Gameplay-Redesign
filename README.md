# Specialization Gameplay Redesign

A Civilization VI / Harmony in Diversity mod for city specialization and domestic trade networks. Current v0.1 implementation scope is Research, Culture, Commerce and Industry; other profession designs are future records.

Start with [AGENTS](AGENTS.md) and the [project map](Specialization/README.md). Gameplay Design is user-authoritative; decision boundaries are in [Workflow guidance](Specialization/Workflow/README.md#w0005--authority-and-repository-knowledge).

- **Design:** [accepted Spec](Specialization/Design/Specialization_v0.1_Design_Spec.md), [content authority map](Specialization/Design/Content/README.md), [ChangeLog](Specialization/Design/Design_ChangeLog.md).
- **Architecture:** [current contracts and implementation links](Specialization/Architecture/v2/README.md).
- **Progress and evidence:** [Status current block](Specialization/Status/Specialization_P0_Status.md), [validation results](Specialization/Status/Validation/Results/).
- **Agent entry:** [W0001](Specialization/Workflow/README.md), [Authority index](Specialization/Workflow/Authority.json); follow the current task manifest, not a remembered conversation.
- **Canonical source:** [Mod](Mod/). main is the last promoted trusted source; develop contains current work, including pending user validation, in its separate worktree. The external Civ VI runtime is a deployment copy, not an editing location.
- **Testing / deployment:** [test instructions](DevelopmentTests/README.md), [tools](tools/README.md), [Playtest Workflow](Specialization/Architecture/Playtest_Workflow.md). Current versions and live-package state are recorded in Status/Authority; no game launch by default.
- **Local setup / external evidence:** copy [configuration example](local.config.example.json) to ignored `local/config.json`; keep credentials out. [External materials](Specialization/Reports/Proposals/Phase1_External_Materials.md) records evidence/backup locations that remain outside Git.
