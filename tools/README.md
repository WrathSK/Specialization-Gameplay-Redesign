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

## Develop publication gate

[check_publication.py](check_publication.py) is the single manual/pre-commit entry for staged publication safety:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_publication.py
```

Requires Python 3 and `gitleaks` on PATH (validated with 8.30.1). No Python packages, game files or external database are required. This gate does not run gameplay tests, install software, change the index, commit, push or deploy.

The gate runs only on `develop`; main, other branches and detached HEAD report NOT_APPLICABLE, not a scan PASS. It reads the Git index, not working-tree content. All changed regular UTF-8 files receive a full staged-blob credential scan with the default gitleaks rules plus four exact game-property-value exceptions in [.gitleaks.toml](../.gitleaks.toml). New files receive full privacy checks; existing files receive added-line privacy checks, so unrelated edits do not require scrubbing historical paths. Inline gitleaks allow comments, repository ignore files and environment config overrides cannot silently disable the scan. Policy/checker/hook working copies must match their staged versions. Index or HEAD changes during scanning invalidate the result.

The supplemental check detects personal home/install paths, local file URIs, encoded path forms and selected device-identifier values; JWT-shaped values are checked throughout each staged file. Raw evidence directories, private config, logs, saves, database/key/crash file types, symlinks and submodules are blocked even after force-add. Binary/non-UTF-8 content, a blob over 10 MiB, a batch over 50 MiB, missing dependencies or scanner failure require separate review and return NOT_RUN; they never silently pass. Whole history, ignored directories, screenshot pixels and raw local evidence are not scanned. This is pattern-based protection, not proof that all private information is absent.

Output contains repository-relative file/line/rule identifiers, never matching values or raw scanner diagnostics. Temporary staged copies and redacted scanner results use a private temporary directory and are removed on normal/error exit. No persistent scan ledger is created. Existing signatures, frozen evidence and Git history are not rewritten.

Exit 0: PASS, or an explicitly labelled NOT_APPLICABLE (non-develop / no staged content). Exit 1: BLOCKED findings. Exit 2: NOT_RUN/incomplete. On develop with staged content, Primary must obtain PASS before committing; investigate a failure without clearing, unstaging or rewriting another role's work. No blanket frozen-record or namespace exception is provided. Any exceptional publication needs a separately reviewed narrow change, not an automatic bypass.

### Local hook installation and removal

The tracked [.githooks/pre-commit](../.githooks/pre-commit) calls the same checker. Hook configuration is local and is **not** installed merely by cloning the repository. Before installation, verify the develop worktree and inspect both effective `core.hooksPath` and the common Git hooks directory. If another hook/configuration exists, stop and coordinate; never overwrite it.

After explicit authorization, from develop:

```sh
git config --local core.hooksPath "$(git rev-parse --show-toplevel)/.githooks"
```

Main and develop share this repository-local setting. The hook checks the active branch before invoking Python, so it does nothing in main or any non-develop checkout; no main files, global Git config or worktreeConfig mechanism are changed. The absolute installation path stays in local Git configuration, never in tracked documentation. If the checkout moves, reinstall deliberately after checking the setting. To remove this installation, first confirm the configured value still identifies this hook, then use `git config --local --unset core.hooksPath`.

A local hook can be bypassed or uninstalled; it is not role enforcement, a remote push gate or GitHub protection. Explicit staging, human evidence/privacy review, user authority and deployment gates still apply. Primary must run the manual entry if hook execution is uncertain. Report publication still follows [W0005](../Specialization/Workflow/README.md#advisory-and-investigation-local-checkpoints); a scan PASS accepts neither the report's conclusions nor implementation.

Targeted validation (temporary Git repositories, synthetic inputs, real gitleaks; no existing gameplay tests):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 DevelopmentTests/test_publication_gate.py
```
