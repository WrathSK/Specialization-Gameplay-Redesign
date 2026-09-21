# Deployment (explicit opt-in)

`Mod/` is the sole editable source. The tool reads `local/config.json:runtime_dir`; use the template at repository root. Do not edit the deployed package or deploy while the game or another editor is modifying it. This tool does not start/stop the game.

Default **read-only** check:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/deploy.py
```

The report prints aggregate source/runtime hashes and equality/count; consume this summary, inspect individual files only on mismatch. If identical, no deployment is necessary. Only after deployment authorization and review:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/deploy.py --apply --authorize-stable-update --expected-source <reviewed-source-hash> --expected-runtime <reviewed-runtime-hash>
```

The target must be an existing `SpecializationP0` directory with the project UUID. Source/target cannot overlap, symlinks are rejected, and runtime-only files cause refusal (no automatic deletion). Hash mismatch rejects unreviewed changes. This means removing a runtime file is a separately reviewed maintenance task, not a generic sync command.

Staging and retained `.SpecializationP0-backup-*` packages live in `SpecializationDeploymentBackups` outside the scanned Mods directory. The staged copy is verified before replacing the whole target. Handled swap errors restore the old directory. Other Mod manifests are read only to reject duplicate UUIDs; unrelated Mods are never modified or deleted.

## Interruption boundary

Two directory renames are not one crash-atomic operation. A process/machine crash between them can leave the target temporarily absent, **not silently mixed**. `.specialization-deploy-pending.json` records stage/backup/target and expected hashes before the first rename; further attempts refuse. Inspect these named paths and verify package hashes; with user authorization restore the recorded backup if the target is absent, or choose the verified completed deployment. Never blindly rerun, delete the backup, or clear the marker. If rollback itself fails, the exception and marker remain for inspection. Filesystem/power-loss durability is not guaranteed by local simulation.

W0004 v2: Git/GitHub replace ordinary canonical-source backup trees and pre-edit snapshots. Do not create extra manual backups on top of this transaction. Tool-generated rollback packages remain retained: the temporary restore path requires its recorded stable backup, so bounded retention is not yet implemented. Historical backups are untouched. Keep deployment records concise (version, source commit, result/equality, receipt reference, abnormal recovery); no duplicate full hash/path inventory.

Stable-only gate: apply requires explicit user-approved current-playtest update and clean committed main. Develop/detached apply is rejected even with the authorization flag. Default check is read-only. Temporary develop game tests require a separately approved recovery/switch procedure; never bypass the gate. See ../Specialization/Architecture/Playtest_Workflow.md.

## Authorized temporary playtest

`temporary_playtest.py activate|restore` is a separate, check-only-by-default entry. It requires explicit hashes/config/stable-root/receipt; `--apply --authorize-temporary-switch --confirmed-game-exited` is only used after user authorizes that switch. Never call from normal builds/tests. See Architecture/Playtest_Workflow.md W0002. Ordinary deploy.py remains stable/main only.

## External runtime monitor (no deployment)

[Optional macOS monitor](external_monitor/README.md) runs only when the user starts it. Independent bounded process-resource logs; no Mod/package dependency, no game launch/injection. Current game is not auto-attached by setup.
