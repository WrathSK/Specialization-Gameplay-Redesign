# Specialization Gameplay Redesign

Document Owner: Codex

This independent directory is the project boundary. `Mod/` is the sole canonical editable gameplay source; the external Civ VI `Mods/SpecializationP0` directory is a deployed copy. Workspace access does not imply ownership. Phase 1 creates files only: no Git initialization, remote, authentication, commit or push is authorized.

Start with [AGENTS](AGENTS.md), [project entry](Specialization/README.md), [accepted Design](Specialization/Design/Specialization_v0.1_Design_Spec.md), [Status](Specialization/Status/Specialization_P0_Status.md), and [Architecture](Specialization/Architecture/Specialization_v0.1_Architecture.md).

- Runtime source: **P0-B-051.67 / modinfo 67**, UUID unchanged.
- Accepted design: **D0014**, exact bytes preserved.
- [Tests](DevelopmentTests/README.md): current regression uses seven included fixtures; SQL checks still require a read-only external game database.
- [Deployment](tools/README.md): check first; apply only with explicit authorization and reviewed source/runtime hashes. Phase 1 does not redeploy the live runtime.
- [Local evidence and historical paths](Specialization/Reports/Proposals/Phase1_External_Materials.md): screenshots, backups, logs and machine inventories remain outside the repository. Historical links are not silently rewritten.
- Machine configuration: copy `local.config.example.json` to ignored `local/config.json` and fill your paths. No credentials belong in either file.

No game launch is permitted. B051.67's existing game-test status remains pending; migration does not validate gameplay.
