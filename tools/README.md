# Deployment (explicit opt-in)

`Mod/` is the sole editable source. The tool reads `local/config.json:runtime_dir`; use the template at repository root. Do not edit the deployed package or deploy while the game or another editor is modifying it. This tool does not start/stop the game.

Default **read-only** check:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/deploy.py
```

The report prints complete source/runtime tree hashes. If identical, no deployment is necessary. Only after deployment authorization and review:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/deploy.py --apply --expected-source <reviewed-source-hash> --expected-runtime <reviewed-runtime-hash>
```

The target must be an existing `SpecializationP0` directory with the project UUID. Source/target cannot overlap, symlinks are rejected, and runtime-only files cause refusal (no automatic deletion). Hash mismatch rejects unreviewed changes. This means removing a runtime file is a separately reviewed maintenance task, not a generic sync command.

A new sibling staging directory is fully copied and checked before replacement. The old whole target is renamed to a uniquely named `.SpecializationP0-backup-*` directory and retained; the staged directory takes its place. Handled errors restore the old whole directory. No other Mod is read, scanned, edited or deleted.

## Interruption boundary

Two directory renames are not one crash-atomic operation. A process/machine crash between them can leave the target temporarily absent, **not silently mixed**. `.specialization-deploy-pending.json` records stage/backup/target and expected hashes before the first rename; further attempts refuse. Inspect these named paths and verify package hashes; with user authorization restore the recorded backup if the target is absent, or choose the verified completed deployment. Never blindly rerun, delete the backup, or clear the marker. If rollback itself fails, the exception and marker remain for inspection. Filesystem/power-loss durability is not guaranteed by local simulation.

The migration tested this tool on temporary packages with an injected swap failure. The actual game runtime was checked only and not replaced. Backups are never automatically cleaned. Phase 1 performs no Git operation.
