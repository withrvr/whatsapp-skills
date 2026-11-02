#!/usr/bin/env python3
"""Every pull request into main ships a new version.

    python3 scripts/check_version.py --base origin/main

Passes when the version in `.claude-plugin/plugin.json` is higher (semver) than
the version on the base branch, and CHANGELOG.md has a `## X.Y.Z` entry for it.
Passes too when the base has no plugin.json yet (the very first release).

Merging the PR then publishes that version: the release workflow tags `vX.Y.Z`
and attaches the skill zips. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ".claude-plugin/plugin.json"


def parse(version: str) -> Tuple[int, int, int]:
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version.strip())
    if not m:
        raise ValueError(f"not a semver X.Y.Z version: {version!r}")
    return tuple(int(x) for x in m.groups())  # type: ignore[return-value]


def base_version(base: str) -> Optional[str]:
    try:
        raw = subprocess.run(["git", "show", f"{base}:{MANIFEST}"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None
    return json.loads(raw)["version"]


def check(head: str, base: Optional[str], changelog: str) -> list:
    problems = []
    try:
        new = parse(head)
    except ValueError as exc:
        return [str(exc)]
    if base is not None and new <= parse(base):
        problems.append(f"version {head} must be higher than main's {base}: bump it in {MANIFEST}, "
                        f"then run python3 scripts/sync.py")
    if not re.search(rf"^## {re.escape(head)}\b", changelog, re.M):
        problems.append(f"CHANGELOG.md has no '## {head}' entry")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check that this branch ships a new version.")
    parser.add_argument("--base", default="origin/main", help="git ref of the target branch (default origin/main)")
    args = parser.parse_args(argv)
    head = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))["version"]
    base = base_version(args.base)
    problems = check(head, base, (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
    if problems:
        for p in problems:
            print(f"✗ {p}")
        return 1
    print(f"✓ ships version {head} (base: {base or 'no release yet'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
