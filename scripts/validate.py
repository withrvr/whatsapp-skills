#!/usr/bin/env python3
"""Validate every skill against the Agent Skills spec and this repo's conventions.

    python3 scripts/validate.py            # all skills
    python3 scripts/validate.py skills/whatsapp-status

Spec rules (https://agentskills.io/specification, mirrored from the reference
validator `skills-ref`):
  - SKILL.md with YAML frontmatter; only name, description, license,
    compatibility, metadata, allowed-tools
  - name: 1-64 chars, lowercase letters/digits/hyphens, no leading, trailing or
    double hyphen, equal to the directory name
  - description: 1-1024 chars; compatibility <= 500 chars; metadata string->string
  - body under 500 lines; file references resolve from the skill root

Repo conventions (stricter, so the bundle stays coherent):
  - name starts with `whatsapp-`; description <= 600 chars, no em dashes,
    includes a "Not for" sentence that points at sibling skills
  - every sibling skill a SKILL.md mentions exists
  - every file in references/ and scripts/ is mentioned by SKILL.md (no orphans)
  - metadata.version equals the plugin version
  - the shared core-rules block is present

Requires PyYAML (pip install -r requirements-dev.txt).
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List

try:
    import yaml
except ImportError:  # pragma: no cover
    print("PyYAML is required: pip install -r requirements-dev.txt", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
ALLOWED = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
SIBLING = re.compile(r"\bwhatsapp-[a-z]+(?:-[a-z]+)*\b")
NOT_SIBLINGS = {"whatsapp-skills", "whatsapp-formatting"}
MAX_DESCRIPTION_REPO = 600
MAX_BODY_LINES = 500
MAX_BODY_TOKENS = 5000  # spec recommendation, estimated as chars / 4


def plugin_version() -> str:
    return json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]


def all_skill_names() -> List[str]:
    return sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))


def parse(skill_md: Path):
    text = skill_md.read_text(encoding="utf-8")
    m = FRONTMATTER.match(text)
    if not m:
        return None, text, "SKILL.md has no YAML frontmatter block (--- ... ---) at the top"
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc:
        return None, text, f"frontmatter does not parse: {str(exc).splitlines()[0]}"
    if not isinstance(data, dict):
        return None, text, "frontmatter is not a mapping"
    return data, text[m.end():], None


def validate_spec(skill_dir: Path) -> List[str]:
    """Rules from the Agent Skills specification."""
    errors: List[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["missing SKILL.md"]
    data, body, problem = parse(skill_md)
    if problem:
        return [problem]

    extra = set(data) - ALLOWED
    if extra:
        errors.append(f"unexpected frontmatter fields: {', '.join(sorted(extra))}")

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("'name' must be a non-empty string")
    else:
        name = unicodedata.normalize("NFKC", name.strip())
        if len(name) > 64:
            errors.append(f"name is {len(name)} chars, max 64")
        if name != name.lower():
            errors.append("name must be lowercase")
        if name.startswith("-") or name.endswith("-"):
            errors.append("name can't start or end with a hyphen")
        if "--" in name:
            errors.append("name can't contain consecutive hyphens")
        if not all(c.isalnum() or c == "-" for c in name):
            errors.append("name may only contain letters, digits and hyphens")
        if name != skill_dir.name:
            errors.append(f"name '{name}' must match the directory name '{skill_dir.name}'")

    desc = data.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append("'description' must be a non-empty string")
    elif len(desc) > 1024:
        errors.append(f"description is {len(desc)} chars, max 1024")

    if "compatibility" in data:
        comp = data["compatibility"]
        if not isinstance(comp, str) or not 1 <= len(comp) <= 500:
            errors.append("compatibility must be a 1-500 char string")
    if "metadata" in data:
        meta = data["metadata"]
        if not isinstance(meta, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in meta.items()):
            errors.append("metadata must map strings to strings (quote numbers like version: \"1.0.0\")")
    for key in ("license", "allowed-tools"):
        if key in data and not isinstance(data[key], str):
            errors.append(f"{key} must be a string")

    lines = body.count("\n") + 1
    if lines > MAX_BODY_LINES:
        errors.append(f"SKILL.md body is {lines} lines, keep it under {MAX_BODY_LINES}")

    for ref in sorted(set(re.findall(r"`((?:references|scripts|assets)/[\w./-]+)", body))):
        path = ref.split(" ")[0]
        if not (skill_dir / path).exists():
            errors.append(f"SKILL.md references {path}, which doesn't exist")
    return errors


def validate_conventions(skill_dir: Path) -> List[str]:
    """This repo's own rules, on top of the spec."""
    errors: List[str] = []
    data, body, problem = parse(skill_dir / "SKILL.md")
    if problem:
        return []  # already reported by the spec check
    name, desc = data.get("name", ""), data.get("description", "")
    full = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    if not str(name).startswith("whatsapp-"):
        errors.append("skill names start with 'whatsapp-'")
    if isinstance(desc, str):
        if len(desc) > MAX_DESCRIPTION_REPO:
            errors.append(f"description is {len(desc)} chars, repo limit {MAX_DESCRIPTION_REPO}")
        if "—" in desc or "–" in desc:
            errors.append("no em or en dashes in description")
        if "Not for" not in desc:
            errors.append("description needs a 'Not for ... (use whatsapp-...)' sentence")
    if len(body) / 4 > MAX_BODY_TOKENS:
        errors.append(f"SKILL.md body is ~{int(len(body) / 4)} tokens, keep it under {MAX_BODY_TOKENS}")

    meta = data.get("metadata") or {}
    if meta.get("version") != plugin_version():
        errors.append(f"metadata.version {meta.get('version')!r} != plugin version {plugin_version()!r} (run scripts/sync.py)")
    if meta.get("author") != "withrvr":
        errors.append("metadata.author should be 'withrvr'")
    if data.get("license") != "MIT":
        errors.append("license should be 'MIT'")
    if "<!-- BEGIN shared:core-rules -->" not in full or "<!-- END shared:core-rules -->" not in full:
        errors.append("missing the shared core-rules markers")

    known = set(all_skill_names())
    for mentioned in sorted(set(SIBLING.findall(full)) - NOT_SIBLINGS):
        if mentioned not in known:
            errors.append(f"mentions '{mentioned}', which is not a skill in this repo")
    if isinstance(desc, str):
        for mentioned in set(SIBLING.findall(desc)) - NOT_SIBLINGS - {name}:
            if mentioned not in known:
                errors.append(f"description points at '{mentioned}', which doesn't exist")

    for sub in ("references", "scripts"):
        folder = skill_dir / sub
        if folder.is_dir():
            for f in sorted(folder.iterdir()):
                if f.is_file() and f"{sub}/{f.name}" not in full:
                    errors.append(f"{sub}/{f.name} is never mentioned in SKILL.md (orphan file)")
    if not (skill_dir / "references" / "examples.md").is_file():
        errors.append("every skill ships references/examples.md")
    if not (skill_dir / "evals" / "evals.json").is_file():
        errors.append("every skill ships evals/evals.json")
    return errors


def validate_all(paths: List[Path] = None) -> Dict[str, List[str]]:
    dirs = paths or sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))
    return {d.name: validate_spec(d) + validate_conventions(d) for d in dirs}


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    paths = [Path(a).resolve() for a in args] if args else None
    results = validate_all(paths)
    bad = 0
    for name, errs in results.items():
        if errs:
            bad += 1
            print(f"✗ {name}")
            for e in errs:
                print(f"    {e}")
        else:
            print(f"✓ {name}")
    print(f"\n{len(results) - bad}/{len(results)} skills valid.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
