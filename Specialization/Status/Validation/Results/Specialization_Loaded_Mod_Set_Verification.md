# Latest loaded mod set verification

Document Owner: Codex
Evidence: read-only native log/database/XML inspection; no game operations

Latest native Modding.log now records a111-entry Enabled Mods block at2736922.864, followed by785 Applying Component lines, Gameplay DLL initialization and Stage: Unserializing Game State. This supports a latest actual load context, beyond the earlier112-entry default configuration. The only set difference versus2736637.864 is removal of cb324efd-0491-48d5-bb49-8d5b66ba9a0e (Switch Civilization). Includes official DLC/modes:111 is not a third-party count or proof every mode executes.

All111 UUIDs uniquely map through current read-only Mods.sqlite to scanned modinfo paths.72 absolute manifests were read and their XML UUID matched;39 database paths are relative official-content paths and were not independently resolved/read. Thus distinguish111 database mappings from72 on-disk XML checks. Specialization maps to live modinfo99. Identified names include HD modules, BTS, More Lenses, BRS and both named overflow-fix packages. Co-presence does not prove conflicting active code, and component registration/application does not prove successful execution of every Lua callback.

This latest load is after the monitored PID33157 interval. It cannot retroactively prove that earlier process used the same set or identify the selected save filename. No save parsed. For current environment investigation no full screenshot list is needed; if user changed configuration between sessions, retain that uncertainty. No request to disable mods or alter the long-play save.

External archive W/Specialization/Status/Validation/Evidence/EnabledMods-20260914-2035 contains copied Modding.log, its SHA256 manifest and Loaded-mods.tsv with per-entry UUID/name/database version/XML status/path/hash. Original live log/database not modified. Outer W/Logs/Modding.log is stale2023 and excluded. Review is not memory-cause attribution. Source/runtime/main unchanged.
