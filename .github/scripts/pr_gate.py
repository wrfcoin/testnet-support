#!/usr/bin/env python3
"""Cheap repo-wide checks run by pr-gate.yml on every PR and push to main.

1. Markdown: valid UTF-8, non-empty, balanced code fences.
2. Internal relative links/images in Markdown resolve to files or directories
   (external URLs, mailto:, and pure #anchors are ignored).
3. No tracked file over 5 MB.
4. Syntax: .py (compile), .json (json.load), .yml/.yaml (yaml.safe_load), .sh (bash -n).

Stdlib only, except PyYAML for YAML (installed by the workflow).
Usage: pr_gate.py [repo_root]
"""
import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

MAX_BYTES = 5 * 1024 * 1024
LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^)]*[\"'])?\s*\)")
REF_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s+.*)?$")
SKIP_TARGET = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//|#)")


def tracked(root):
    out = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"], check=True, capture_output=True
    ).stdout
    return [p for p in out.decode().split("\0") if p]


def check_markdown(root, rel, errors):
    path = root / rel
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        errors.append(f"{rel}: not valid UTF-8 ({e})")
        return
    if not text.strip():
        errors.append(f"{rel}: empty markdown file")
        return
    fence = None
    targets = []
    for n, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if m:
            marker = m.group(1)
            if fence is None:
                fence = marker[0] * 3
            elif marker[0] == fence[0]:
                fence = None
            continue
        if fence is not None:
            continue
        # strip inline code spans so `[x](y)` examples are not treated as links
        stripped = re.sub(r"`[^`]*`", "", line)
        for t in LINK.findall(stripped):
            targets.append((n, t))
        d = REF_DEF.match(stripped)
        if d:
            targets.append((n, d.group(1)))
    if fence is not None:
        errors.append(f"{rel}: unclosed code fence")
    for n, target in targets:
        if SKIP_TARGET.match(target):
            continue
        ref = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not ref:
            continue
        dest = (root / ref.lstrip("/")) if ref.startswith("/") else (path.parent / ref)
        try:
            dest.resolve().relative_to(root.resolve())
        except ValueError:
            errors.append(f"{rel}:{n}: link escapes the repo: {target}")
            continue
        if not dest.exists():
            errors.append(f"{rel}:{n}: broken relative link: {target}")


def check_syntax(root, rel, errors):
    path = root / rel
    suffix = path.suffix.lower()
    try:
        if suffix == ".py":
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        elif suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        elif suffix in (".yml", ".yaml"):
            import yaml

            list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
        elif suffix == ".sh":
            r = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
            if r.returncode:
                errors.append(f"{rel}: bash -n: {r.stderr.strip()}")
    except Exception as e:  # noqa: BLE001 - report any parser failure as a finding
        errors.append(f"{rel}: syntax error: {e}")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors, counts = [], {"md": 0, "syntax": 0, "files": 0}
    for rel in tracked(root):
        path = root / rel
        if not path.is_file():  # symlink to dir, submodule
            continue
        counts["files"] += 1
        if path.stat().st_size > MAX_BYTES:
            errors.append(f"{rel}: {path.stat().st_size} bytes exceeds the 5 MB limit")
        if rel.lower().endswith(".md"):
            counts["md"] += 1
            check_markdown(root, rel, errors)
        if path.suffix.lower() in (".py", ".json", ".yml", ".yaml", ".sh"):
            counts["syntax"] += 1
            check_syntax(root, rel, errors)
    print(
        f"checked {counts['files']} files: {counts['md']} markdown, "
        f"{counts['syntax']} syntax-checked"
    )
    for e in errors:
        print(f"::error::{e}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
