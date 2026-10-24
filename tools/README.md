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

### Develop switch sequence (W0003, as used B205–B212)

The tool only switches stable→develop. Each new develop build is therefore two guarded steps, with no game launch in between:

1. **Game-exit check.** Match only the game executable: `pgrep -f 'Civ6.app/Contents'`. A broader pattern such as `Sid Meier` also matches the Claude/agent process, whose arguments contain the Civ VI directory, and falsely reports the game as running.
2. **Restore stable.** Run `restore` with the **previous** develop receipt (`SpecializationDeploymentBackups/<Bxxx.vvv>-<sha7>-playtest.json`), passing `--expected-source <receipt stable_hash> --expected-runtime <receipt develop_hash>`. Run check-only first; the hashes must equal the receipt.
3. **Activate develop.** Run `activate` with a **new** receipt named `<Bnew.vnew>-<sha7>-playtest.json` on clean committed develop, passing `--expected-source <check-only source_hash> --expected-runtime <stable_hash>`.
4. **Verify.** Run `deploy.py --config <main checkout local/config.json>` (read-only). It must report `identical: true` and 219 files, with no `.specialization-deploy-pending.json`. Then record the version, source commit, receipt and MATCH in Status, Authority, Runtime_Index and the result.

The config lives in the main checkout's ignored `local/config.json` (the develop worktree has none). Under zsh, unquoted variables do not word-split: pass hashes literally, or drive loops from Python.

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

## Fixed Expedition diagnostic read (B205)

[read_expedition_trace.py](read_expedition_trace.py) is a read-only FireTuner client for the current diagnostic batch:
- `probe` reads turn/context availability.
- `trace` reads only the bounded B205 scalar ring.
- `record` takes one ring snapshot, then passively keeps exact `[SPC][B205][TRAIN]` prints for a bounded window.

It does not enable Tuner, launch the game, select arbitrary Lua/context/host or run GC. The exact advertised GameCore_Tuner context is required, and output is bounded. Errors are NOT_VERIFIED, never successful collection. The Mac `GameCore_Tuner` context has no `rawget`, so the command uses ordinary table reads and reports a native `ERR` reply instead of masking it as a timeout (`8963218`).

[collect_expedition_trace.py](collect_expedition_trace.py) is the unattended session collector (S0549):
- It waits for localhost:4318.
- It repeats the fixed `record` capture, by default with a 30 s window, reconnecting across loads.
- It deduplicates records and writes `local/diagnostics/B205/session-*/` (`records.log`, `events.jsonl`, `summary.txt`).
- It flags population changes per city and native/definition cost mismatches.
- It stops after the game has been gone for `--idle-exit` seconds (default 30), on Ctrl-C/SIGTERM, or at a 12-hour cap.
- During an in-game reload the Tuner socket **refuses** connections for about 2–3 minutes, which looks the same as a game exit. For multi-load sessions use `--idle-exit 300` and stop with Ctrl-C; the summary is still written.
- B212: it also records the Expedition Gate's `[SPC][B191][N1_*]` prints (dispatch, task, completion, cancellation, return) as `gate` lines.
- It sends no gameplay command and changes no configuration.

B267 collection contract: meaningful TRAIN records no longer stop after a per-role lifetime quota. Repeated state/quote/failure reports are change-only by city/target/domain; temporal requests and receipts remain individual records. Each role retains a 512-record-per-turn runaway breaker with `TRACE_THROTTLED`, while optional Unit/Event native sampling has its independent 96-sample bound. The scalar ring holds 256 entries; the fixed reader accepts 256 snapshot entries (262 protocol rows), 2 MiB snapshot bytes, and up to 8,192 passive TRAIN rows / 16 MiB / 16,384 frames per window. Safety-limit failures and ring-overwrite gaps are explicit; disconnected output beyond the ring cannot be recovered. The separate `UI.DataError` fallback retains its 128-call safety limit and is not the complete collection channel.

The collector saves META counters and alerts for suppression/errors, native-sampling exhaustion, fallback-channel stop, missing readiness/load samples and capture/ring gaps. Readiness means initialization gates, not successful effect reconciliation. Commerce turn records compare configured base Gold and current carrier bits; they do not prove net Treasury accrual. Carrier health observes the fixed 35 ResearchSupport/Lv2GPP types and never repairs them. First-session new-game/load delivery remains a native check.

Tuner policy (user decision, 2026-10-16): during development `EnableTuner` stays 1 and the user toggles it from the terminal with the game closed. `AppOptions.txt` uses CRLF line endings, so a sed pattern must include `\r`. Primary does not restore it after sessions. From repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/collect_expedition_trace.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/read_expedition_trace.py probe
```

Native fixed-query transport was observed once; automatic disk logging, passive streaming and B205 trace retrieval are distinct unverified surfaces. Retain output only in ignored local evidence; do not publish raw engine logs/configuration. [Scope and evidence](../Specialization/Status/Validation/Results/Specialization_B205_Expedition_Reload_Diagnostics_Local.md). Offline checks: `python3 DevelopmentTests/test_expedition_trace_reader.py` (needs Lupa) and `python3 DevelopmentTests/test_expedition_trace_collector.py`. Neither opens a live socket.

## B271 bounded turn observations

A/B record treasury timing and existing callback/audit counts automatically during the first six observed local turns after load. C is separately off by default: right-click the existing 专业化诊断 entry to toggle for this load. It observes two contexts, at most400 events per side/window, in batches of12; no new timer/frame listener. Run the existing collector during2–3 turns. New TRAIN rows enter records.log; summary.txt reports balance observations/network confirmation order, callback counts, missing points and capped/incomplete event windows. A first observed balance difference is an interval observation, not attribution to engine accrual. Existing ring/protocol/reader limits remain unchanged. See [B271 evidence and limitations](../Specialization/Status/Validation/Results/Specialization_B271_Turn_Timing_Carrier_Pillage.md). This documentation does not authorize deployment.
