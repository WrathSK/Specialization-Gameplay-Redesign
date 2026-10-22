"""Check only staged publication inputs. No source, index or history writes."""
from pathlib import Path
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 50 * 1024 * 1024
POLICY_FILES = ("tools/check_publication.py", ".githooks/pre-commit", ".gitleaks.toml")


class Incomplete(Exception):
    pass


def git(*args, optional=False):
    result = subprocess.run(["git", *args], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=30)
    if result.returncode and not optional:
        raise Incomplete("Git read failed; no PASS issued")
    return result


def decoded(text):
    for _ in range(5):
        new = html.unescape(urllib.parse.unquote(text)).replace("\\/", "/")
        new = re.sub(r"\\u002[fF]", "/", new)
        new = re.sub(r"\\u005[cC]", "\\\\", new)
        if new == text:
            break
        text = new
    return text


PRIVATE_PATH = re.compile(
    r"/(?:Users|home)/[^/\s<>`'\"{}$]+/"
    r"|[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s<>`'\"{}$]+"
    r"|/(?:private/)?var/folders/[^\s<>`'\"]+"
    r"|/" r"Volumes/[^\s<>`'\"]+"
    r"|file:" r"//[^\s<>`'\")]+", re.I)
DEVICE_ID = re.compile(
    r"(?:crashReporterKey|bootSessionUUID|sleepWakeUUID|anonymousUUID)"
    r"[\"']?\s*[:=]\s*[\"']?[a-f0-9][a-f0-9-]{15,}", re.I)
JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")


def prohibited(path):
    p = path.lower()
    parts = p.split("/")
    name = parts[-1]
    if any(x in parts[:-1] for x in ("local", "screenshots", "developmentbackups")):
        return True
    if p.startswith("specialization/status/validation/evidence/"):
        return True
    if name == "local.config.json" or name == ".env" or name.startswith(".env."):
        return name not in (".env.example", ".env.template")
    return bool(re.search(r"\.(?:log|ips|crash|civ6save|sqlite(?:3)?(?:-.*)?|db(?:-.*)?|pem|p12|pfx|key)$", name)
                or re.match(r"(?:firaxislive.*|crash[-_0-9].*)\.txt$", name))


def private_reasons(line):
    value = decoded(line)
    return [label for label, pattern in (("personal-path", PRIVATE_PATH),
                                        ("device-identifier", DEVICE_ID)) if pattern.search(value)]


def label(path, number):
    # Never echo suspicious names or terminal control characters.
    if private_reasons(path) or JWT.search(path) or any(ord(c) < 32 for c in path):
        return "staged file #" + str(number)
    return json.dumps(path, ensure_ascii=True)


def additions(path):
    patch = git("diff", "--cached", "--no-ext-diff", "--no-textconv", "--no-color",
                "--no-renames", "--unified=0", "--", path).stdout.decode("utf-8")
    line_number = None
    for line in patch.splitlines():
        match = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if match:
            line_number = int(match[1])
        elif line_number is not None:
            if line.startswith("+"):
                yield line_number, line[1:]
                line_number += 1
            elif line.startswith(" "):
                line_number += 1


def blob(oid):
    size = int(git("cat-file", "-s", oid).stdout)
    if size > MAX_FILE_BYTES:
        raise Incomplete("Staged blob exceeds 10 MiB review limit")
    return git("cat-file", "blob", oid).stdout


def run():
    root = Path(os.fsdecode(git("rev-parse", "--show-toplevel").stdout).strip())
    os.chdir(root)
    branch = git("symbolic-ref", "--quiet", "--short", "HEAD", optional=True)
    if branch.returncode or branch.stdout.strip() != b"develop":
        print("PUBLICATION_CHECK NOT_APPLICABLE: only develop is enabled")
        return 0
    before = git("ls-files", "--stage", "-z").stdout
    head = git("rev-parse", "--verify", "HEAD", optional=True).stdout
    entries = {}
    for row in before.split(b"\0"):
        if not row:
            continue
        meta, raw_path = row.split(b"\t", 1)
        mode, oid, stage = meta.split()
        if stage != b"0":
            raise Incomplete("Unmerged index; resolve it before publication review")
        entries[os.fsdecode(raw_path)] = (mode, oid.decode("ascii"))
    # Policy itself must be a reviewed staged version, not an unstaged substitute.
    for path in POLICY_FILES:
        if path not in entries or entries[path][0] not in (b"100644", b"100755"):
            raise Incomplete("Publication policy files must be regular staged/tracked files")
        if (root / path).is_symlink() or (root / path).read_bytes() != blob(entries[path][1]):
            raise Incomplete("Publication policy differs from index; review and stage it first")
    raw = git("diff", "--cached", "--raw", "-z", "--no-abbrev", "--no-renames",
              "--no-ext-diff", "--no-textconv").stdout.split(b"\0")
    changes = []
    for i in range(0, len(raw) - 1, 2):
        old_mode, new_mode, old_oid, new_oid, status = raw[i].split()
        path = os.fsdecode(raw[i + 1])
        if status == b"D":
            continue
        if status not in (b"A", b"M", b"T"):
            raise Incomplete("Unsupported index transition; no PASS issued")
        if entries.get(path) != (new_mode, new_oid.decode("ascii")):
            raise Incomplete("Index changed during collection")
        changes.append((path, new_mode, new_oid.decode("ascii"), status))
    if not changes:
        if git("ls-files", "--stage", "-z").stdout != before or git("rev-parse", "--verify", "HEAD", optional=True).stdout != head:
            raise Incomplete("Index or HEAD changed during collection")
        print("PUBLICATION_CHECK NOT_APPLICABLE: no staged content to scan")
        return 0
    scanner = shutil.which("gitleaks")
    if not scanner:
        raise Incomplete("gitleaks is missing; install it before committing develop")
    findings = []
    files = {}
    total = 0
    with tempfile.TemporaryDirectory(prefix="spc-publication-") as temp:
        tmp = Path(temp)
        scan = tmp / "inputs"
        scan.mkdir(mode=0o700)
        config = tmp / "policy.toml"
        config.write_bytes(blob(entries[".gitleaks.toml"][1]))
        config.chmod(0o600)
        ignore = tmp / "empty-ignore"
        ignore.write_text("")
        for n, (path, mode, oid, status) in enumerate(changes, 1):
            display = label(path, n)
            if prohibited(path) or private_reasons(path) or JWT.search(path):
                findings.append(display + ": prohibited publication path/type")
                continue
            if mode not in (b"100644", b"100755"):
                findings.append(display + ": symlink/submodule is not a scannable report/source file")
                continue
            content = blob(oid)
            total += len(content)
            if total > MAX_TOTAL_BYTES:
                raise Incomplete("Staged content exceeds 50 MiB review limit")
            if b"\0" in content:
                raise Incomplete("Binary staged content requires separate publication review")
            text = content.decode("utf-8")
            for line_number, line in (enumerate(text.splitlines(), 1) if status == b"A" else additions(path)):
                for reason in private_reasons(line):
                    findings.append(display + ":" + str(line_number) + ": " + reason)
            for line_number, line in enumerate(text.splitlines(), 1):
                if JWT.search(decoded(line)):
                    findings.append(display + ":" + str(line_number) + ": token-shaped value")
            # Opaque .txt names prevent path-based scanner exemptions and exposure of paths.
            name = str(n).zfill(6) + ".txt"
            files[name] = display
            target = scan / name
            target.write_bytes(content)
            target.chmod(0o600)
        result_path = tmp / "redacted.json"
        env = {k: v for k, v in os.environ.items() if not k.startswith("GITLEAKS_")}
        result = subprocess.run(
            [scanner, "dir", str(scan), "--config", str(config), "--redact=100",
             "--no-banner", "--no-color", "--ignore-gitleaks-allow",
             "--gitleaks-ignore-path", str(ignore), "--max-decode-depth", "5",
             "--timeout", "30", "--report-format", "json", "--report-path", str(result_path)],
            cwd=tmp, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45)
        if result.returncode not in (0, 1) or not result_path.is_file():
            raise Incomplete("gitleaks did not complete successfully; raw diagnostics suppressed")
        leaks = json.loads(result_path.read_text())
        if not isinstance(leaks, list) or (bool(leaks) != (result.returncode == 1)):
            raise Incomplete("gitleaks result is inconsistent; no PASS issued")
        for leak in leaks:
            filename = Path(leak["File"]).name
            if filename not in files or not isinstance(leak["StartLine"], int):
                raise Incomplete("Unrecognized scanner result; no PASS issued")
            # Do not print Match, Secret, Description, entropy or captured scanner output.
            rule = leak["RuleID"]
            if not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", rule):
                raise Incomplete("Invalid scanner rule identifier")
            findings.append(files[filename] + ":" + str(leak["StartLine"]) + ": credential rule " + rule)
    if git("ls-files", "--stage", "-z").stdout != before or git("rev-parse", "--verify", "HEAD", optional=True).stdout != head:
        raise Incomplete("Index or HEAD changed during scan; review and run again")
    if findings:
        print("PUBLICATION_CHECK BLOCKED")
        for finding in sorted(set(findings)):
            print("- " + finding)
        return 1
    print("PUBLICATION_CHECK PASS: " + str(len(changes)) + " staged files; secret scan and added-content privacy checks")
    return 0


def main():
    try:
        return run()
    except (Incomplete, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        # Exception details can contain source data or private temporary paths.
        detail = str(error) if isinstance(error, Incomplete) else "Check could not complete; raw diagnostics suppressed"
        print("PUBLICATION_CHECK NOT_RUN: " + detail)
        return 2


if __name__ == "__main__":
    sys.exit(main())
