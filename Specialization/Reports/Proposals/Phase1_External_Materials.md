# Phase 1 external materials and path interpretation

Document Owner: Codex

Repository root R contains canonical Mod, documents and tests. The legacy workspace W is an external location configured by `local/config.json:legacy_workspace`; it is not this repository's parent. The existing W/AGENTS.md is untouched. Old W docs/source are retained for rollback, not continuing parallel editing. Future agents must open R and follow R/AGENTS.md.

## Deliberately local-only

- `W/Specialization/Status/Validation/Evidence/`: bulk PNGs and original screenshot manifests, unchanged. Markdown links into Evidence in preserved results/history resolve conceptually here, not to bundled evidence.
- `W/Specialization/ScreenShots/`: existing user screenshot inbox, unchanged; do not create/move the inbox merely for migration.
- `W/DevelopmentBackups/`: frozen backups; only seven named source fixtures are copied into R/DevelopmentTests/Fixtures.
- `W/DevelopmentReports/`: legacy redirects and mixed unrelated GPP material, not copied.
- Game cache/database, logs, saves, original/HD/Workshop source/assets: external dependencies, never bundled. Raw result .log files and large Handoff_Integrity.json also remain external.

## Preserved historical path semantics

Accepted Design, historical snapshots and validation result originals retain bytes and historical/hash meaning. Absolute `/Users/...` strings in those preserved documents are historical provenance, not executable current paths. Technical reports may also describe historical commands; only current root README/AGENTS, Architecture/Status and DevelopmentTests/README define active paths/commands. Future agents must not execute a historical command without adapting it explicitly.

`Phase1_Link_Audit.json` classifies every local Markdown link: bundled, omitted local evidence, legacy/external or unresolved historical. An unresolved historical link is not newly proven evidence; no stub is fabricated. Root README, AGENTS, active Architecture/Status and technical index links are checked separately. Historical source routing is superseded, not rewritten in original records.

All small Results JSON are preserved provenance only, not authoritative gameplay state. Phase1_Path_Map.json describes the previous document migration, not the current repository boundary.
