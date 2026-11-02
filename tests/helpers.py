"""Shared test helpers. Stdlib + PyYAML only."""
from __future__ import annotations

import datetime as dt
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))
SKILL_NAMES = [p.name for p in SKILLS]

#: The examples in references/examples.md were written for this date.
EXAMPLES_TODAY = dt.date(2026, 11, 2)

TEXT_BLOCK = re.compile(r"^(?P<fence>`{3,})text[ \t]*\n(?P<body>.*?)\n(?P=fence)[ \t]*$", re.S | re.M)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # dataclasses need the module registered
    spec.loader.exec_module(module)
    return module


wa_lint = load_module("wa_lint", ROOT / "shared" / "scripts" / "wa_lint.py")
sync = load_module("sync", ROOT / "scripts" / "sync.py")
validate = load_module("validate", ROOT / "scripts" / "validate.py")


def text_blocks(markdown: str):
    """Every ```text block: the copy-ready WhatsApp messages in a document."""
    return [m.group("body") for m in TEXT_BLOCK.finditer(markdown)]
