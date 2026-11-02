#!/usr/bin/env python3
"""Build one upload-ready zip per skill, plus one zip with all of them.

    python3 scripts/build_zips.py            # -> dist/
    python3 scripts/build_zips.py --out /tmp/zips

Each zip holds a single top-level folder named after the skill, with SKILL.md
inside it: the layout claude.ai (Settings → Capabilities → Skills → Upload) and
other skill-upload screens expect. Evals are left out; they're for maintainers.

Zips are deterministic (fixed timestamps, sorted entries), so rebuilding
unchanged skills gives byte-identical files. Standard library only.
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"evals", "__pycache__"}
SKIP_FILES = {".DS_Store"}
EPOCH = (2026, 1, 1, 0, 0, 0)


def skill_files(skill: Path):
    for path in sorted(skill.rglob("*")):
        rel = path.relative_to(skill)
        if path.is_dir() or path.name in SKIP_FILES or SKIP_DIRS & set(rel.parts) or path.suffix == ".pyc":
            continue
        yield path, rel


def add(zf: zipfile.ZipFile, path: Path, arcname: str) -> None:
    info = zipfile.ZipInfo(arcname, date_time=EPOCH)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o755 if path.suffix == ".py" else 0o644) << 16
    zf.writestr(info, path.read_bytes())


def build(out: Path) -> list:
    out.mkdir(parents=True, exist_ok=True)
    skills = sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))
    built = []
    with zipfile.ZipFile(out / "whatsapp-skills-all.zip", "w") as bundle:
        for skill in skills:
            target = out / f"{skill.name}.zip"
            with zipfile.ZipFile(target, "w") as zf:
                for path, rel in skill_files(skill):
                    add(zf, path, f"{skill.name}/{rel.as_posix()}")
                    add(bundle, path, f"{skill.name}/{rel.as_posix()}")
            built.append(target)
    built.append(out / "whatsapp-skills-all.zip")
    return built


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build upload-ready skill zips.")
    parser.add_argument("--out", type=Path, default=ROOT / "dist", help="output folder (default: dist/)")
    args = parser.parse_args(argv)
    for path in build(args.out):
        print(f"{path.stat().st_size / 1024:6.1f} KB  {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
