#!/usr/bin/env python3
"""Keep every generated file in the repo in step with its source.

    python3 scripts/sync.py           # write everything
    python3 scripts/sync.py --check   # change nothing, exit 1 if anything is stale

Why generated copies exist: each skill must be self-contained. A skill gets
installed on its own (zip upload to claude.ai or ChatGPT, `npx skills add`,
copying one folder into `~/.claude/skills`), and the Agent Skills spec says file
references resolve from the skill's own root. So the shared knowledge lives once
in `shared/` and is copied into every skill.

What this script owns:

1. `shared/references/*.md`  -> `skills/*/references/`
2. `shared/scripts/wa_lint.py` -> `skills/*/scripts/wa_lint.py`
3. `shared/snippets/core-rules.md` -> between the BEGIN/END markers in every SKILL.md
4. The version in `.claude-plugin/plugin.json` -> every other manifest and every
   SKILL.md `metadata.version`
5. `.claude/skills/<name>` symlinks -> `skills/<name>` (Claude Code clone-and-open)
6. `.codex-marketplace/whatsapp-skills/` -> the Codex/ChatGPT plugin package

Standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared"
SKILLS = ROOT / "skills"
PLUGIN = "whatsapp-skills"
CODEX_PACKAGE = ROOT / ".codex-marketplace" / PLUGIN

BEGIN = "<!-- BEGIN shared:core-rules -->"
END = "<!-- END shared:core-rules -->"
MD_HEADER = "<!-- GENERATED from shared/references/{name} by scripts/sync.py. Edit the source, not this copy. -->\n"
PY_HEADER = "# GENERATED from shared/scripts/wa_lint.py by scripts/sync.py. Edit the source, not this copy.\n"

#: What goes into the Codex package. Evals, tests and maintainer scripts stay out.
CODEX_PATHS = [".codex-plugin", "skills", "assets", "docs", "media/demo/demo.gif",
               "README.md", "CONTRIBUTING.md", "CHANGELOG.md", "LICENSE"]
CODEX_IGNORE = shutil.ignore_patterns("evals", "__pycache__", "*.pyc", ".DS_Store")


def skill_dirs() -> List[Path]:
    return sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())


def version() -> str:
    return json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]


# ---------------------------------------------------------------- expected ---


def expected_files() -> Dict[Path, str]:
    """Every generated text file and the content it must have."""
    out: Dict[Path, str] = {}
    refs = sorted((SHARED / "references").glob("*.md"))
    lint_src = (SHARED / "scripts" / "wa_lint.py").read_text(encoding="utf-8")
    shebang, rest = lint_src.split("\n", 1)
    lint_copy = shebang + "\n" + PY_HEADER + rest
    snippet = (SHARED / "snippets" / "core-rules.md").read_text(encoding="utf-8").strip()
    ver = version()

    for skill in skill_dirs():
        for ref in refs:
            out[skill / "references" / ref.name] = MD_HEADER.format(name=ref.name) + ref.read_text(encoding="utf-8")
        out[skill / "scripts" / "wa_lint.py"] = lint_copy

        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        if BEGIN not in text or END not in text:
            raise SystemExit(f"{skill.name}/SKILL.md is missing the {BEGIN} / {END} markers")
        before, tail = text.split(BEGIN, 1)
        _, after = tail.split(END, 1)
        text = f"{before}{BEGIN}\n{snippet}\n{END}{after}"
        text = re.sub(r'(?m)^(\s+version:\s*)"[^"]*"', rf'\g<1>"{ver}"', text, count=1)
        out[skill / "SKILL.md"] = text

    for rel in (".codex-plugin/plugin.json",):
        path = ROOT / rel
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = ver
        out[path] = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    path = ROOT / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for plugin in data["plugins"]:
        plugin["version"] = ver
    data.setdefault("metadata", {})["version"] = ver
    out[path] = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    return out


# ------------------------------------------------------------------- write ---


def write_files(files: Dict[Path, str]) -> List[str]:
    changed = []
    for path, content in files.items():
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current != content:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            if path.suffix == ".py":
                path.chmod(0o755)
            changed.append(str(path.relative_to(ROOT)))
    return changed


def sync_symlinks(check: bool) -> List[str]:
    problems = []
    mirror = ROOT / ".claude" / "skills"
    wanted = {s.name for s in skill_dirs()}
    if not check:
        mirror.mkdir(parents=True, exist_ok=True)
    existing = {p.name for p in mirror.iterdir()} if mirror.is_dir() else set()
    for name in sorted(wanted):
        link = mirror / name
        target = Path("..") / ".." / "skills" / name
        ok = link.is_symlink() and Path(os.readlink(link)) == target
        if not ok:
            problems.append(f".claude/skills/{name} (symlink)")
            if not check:
                if link.is_symlink() or link.exists():
                    link.unlink() if link.is_symlink() or link.is_file() else shutil.rmtree(link)
                link.symlink_to(target, target_is_directory=True)
    for name in sorted(existing - wanted):
        problems.append(f".claude/skills/{name} (stale)")
        if not check:
            link = mirror / name
            link.unlink() if link.is_symlink() or link.is_file() else shutil.rmtree(link)
    return problems


def _build_codex(into: Path) -> None:
    for rel in CODEX_PATHS:
        src = ROOT / rel
        dest = into / rel
        if src.is_dir():
            shutil.copytree(src, dest, ignore=CODEX_IGNORE)
        elif src.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)


def _tree(base: Path) -> Dict[str, bytes]:
    if not base.is_dir():
        return {}
    return {
        str(p.relative_to(base)): p.read_bytes()
        for p in sorted(base.rglob("*"))
        if p.is_file()
    }


def sync_codex(check: bool) -> List[str]:
    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / PLUGIN
        _build_codex(fresh)
        want, have = _tree(fresh), _tree(CODEX_PACKAGE)
        diff = sorted(k for k in set(want) | set(have) if want.get(k) != have.get(k))
        if diff and not check:
            if CODEX_PACKAGE.exists():
                shutil.rmtree(CODEX_PACKAGE)
            shutil.copytree(fresh, CODEX_PACKAGE)
    return [f".codex-marketplace/{PLUGIN}/{d}" for d in diff]


# -------------------------------------------------------------------- main ---


def stale_files(files: Dict[Path, str]) -> List[str]:
    return [
        str(path.relative_to(ROOT))
        for path, content in files.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != content
    ]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--check", action="store_true", help="report stale files and exit 1, change nothing")
    args = parser.parse_args(argv)

    files = expected_files()
    if args.check:
        problems = stale_files(files) + sync_symlinks(check=True)
        # The Codex package copies skills, so compare it after the skills are known-good.
        problems += sync_codex(check=True)
        if problems:
            print("Out of sync (run: python3 scripts/sync.py):")
            for p in problems:
                print(f"  {p}")
            return 1
        print(f"In sync: {len(skill_dirs())} skills, version {version()}.")
        return 0

    changed = write_files(files)
    changed += sync_symlinks(check=False)
    changed += sync_codex(check=False)
    if changed:
        print(f"Updated {len(changed)} path(s):")
        for c in changed[:40]:
            print(f"  {c}")
        if len(changed) > 40:
            print(f"  … and {len(changed) - 40} more")
    else:
        print("Nothing to do, already in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
