"""The repo around the skills: manifests agree, generated files are fresh, docs
link to things that exist, and the install surfaces see the same 8 skills."""
from __future__ import annotations

import io
import json
import os
import re
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

from helpers import ROOT, SKILL_NAMES, load_module, sync

build_zips = load_module("build_zips", ROOT / "scripts" / "build_zips.py")

WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class Manifests(unittest.TestCase):
    def setUp(self):
        self.claude = load(".claude-plugin/plugin.json")
        self.market = load(".claude-plugin/marketplace.json")
        self.codex = load(".codex-plugin/plugin.json")
        self.agents = load(".agents/plugins/marketplace.json")

    def test_names_agree(self):
        self.assertEqual(self.claude["name"], "whatsapp-skills")
        self.assertEqual(self.market["plugins"][0]["name"], self.claude["name"])
        self.assertEqual(self.codex["name"], self.claude["name"])
        self.assertEqual(self.agents["plugins"][0]["name"], self.claude["name"])

    def test_versions_agree(self):
        v = self.claude["version"]
        self.assertRegex(v, r"^\d+\.\d+\.\d+$")
        self.assertEqual(self.market["plugins"][0]["version"], v)
        self.assertEqual(self.market["metadata"]["version"], v)
        self.assertEqual(self.codex["version"], v)

    def test_descriptions_agree_and_count_skills(self):
        desc = self.claude["description"]
        self.assertEqual(self.market["plugins"][0]["description"], desc)
        self.assertEqual(self.codex["description"], desc)
        self.assertTrue(desc.startswith(f"{len(SKILL_NAMES)} skills"), desc)
        self.assertIn(f"{len(SKILL_NAMES)} skills", self.codex["interface"]["longDescription"])

    def test_marketplace_points_at_repo_root(self):
        self.assertEqual(self.market["plugins"][0]["source"], "./")

    def test_codex_package_path_exists(self):
        path = ROOT / self.agents["plugins"][0]["source"]["path"]
        self.assertTrue((path / ".codex-plugin" / "plugin.json").is_file())
        self.assertEqual(sorted(p.name for p in (path / "skills").iterdir()), SKILL_NAMES)
        self.assertFalse(any((path / "skills").glob("*/evals")), "evals stay out of the package")

    def test_codex_icon_exists(self):
        self.assertTrue((ROOT / self.codex["interface"]["composerIcon"]).is_file())

    def test_every_json_parses(self):
        for path in ROOT.rglob("*.json"):
            if "evals-workspace" in path.parts or ".git" in path.parts:
                continue
            with self.subTest(path=str(path.relative_to(ROOT))):
                json.loads(path.read_text(encoding="utf-8"))


class Generated(unittest.TestCase):
    def test_everything_in_sync(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = sync.main(["--check"])
        self.assertEqual(code, 0, out.getvalue())

    def test_claude_mirror_symlinks(self):
        mirror = ROOT / ".claude" / "skills"
        self.assertEqual(sorted(p.name for p in mirror.iterdir()), SKILL_NAMES)
        for name in SKILL_NAMES:
            link = mirror / name
            self.assertTrue(link.is_symlink(), name)
            self.assertEqual(os.readlink(link), os.path.join("..", "..", "skills", name))
            self.assertTrue((link / "SKILL.md").is_file())

    def test_generated_files_say_so(self):
        for name in SKILL_NAMES:
            for ref in (ROOT / "shared" / "references").glob("*.md"):
                copy = ROOT / "skills" / name / "references" / ref.name
                self.assertTrue(copy.read_text(encoding="utf-8").startswith("<!-- GENERATED"), copy)


class Docs(unittest.TestCase):
    DOCS = ["README.md", "CONTRIBUTING.md", "AGENTS.md", "CHANGELOG.md", "docs/INSTALL.md",
            "docs/USAGE.md", "docs/SCENARIOS.md"]

    def test_readme_lists_every_skill(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in SKILL_NAMES:
            self.assertIn(f"`{name}`", readme)
        self.assertIn(f"{len(SKILL_NAMES)} open-source Agent Skills", readme)

    def test_relative_links_resolve(self):
        link = re.compile(r"\]\((?!https?://|mailto:|#)([^)#\s]+)(?:#[^)]*)?\)")
        for rel in self.DOCS:
            path = ROOT / rel
            text = re.sub(r"```.*?```|`[^`\n]*`", "", path.read_text(encoding="utf-8"), flags=re.S)
            for target in link.findall(text):
                with self.subTest(doc=rel, target=target):
                    self.assertTrue((path.parent / target).resolve().exists(), f"{rel} → {target}")

    def test_scenario_catalog(self):
        text = (ROOT / "docs" / "SCENARIOS.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| (\d+) \| .+? \| `(whatsapp-[a-z-]+)` \|", text, re.M)
        numbers = [int(n) for n, _ in rows]
        self.assertGreaterEqual(len(rows), 100)
        self.assertEqual(numbers, list(range(1, len(rows) + 1)), "rows numbered 1..N without gaps")
        used = {skill for _, skill in rows}
        self.assertEqual(used, set(SKILL_NAMES), "every skill appears, and only real skills")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"{len(rows)} everyday scenarios", readme)

    def test_changelog_has_current_version(self):
        version = load(".claude-plugin/plugin.json")["version"]
        self.assertIn(f"## {version} ", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_no_mentions_of_other_bundles(self):
        banned = re.compile(r"sergebulaev|\blinkedin-skills\b|\bx-skills\b|\bpublora\b|\bapify\b", re.I)
        for path in ROOT.rglob("*"):
            if not path.is_file() or {".git", "evals-workspace", "dist", "tests"} & set(path.parts):
                continue
            if path.suffix not in {".md", ".json", ".py", ".yml", ".svg", ".txt", ""}:
                continue
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIsNone(banned.search(path.read_text(encoding="utf-8", errors="ignore")))

    def test_no_markdown_bold_in_whatsapp_text_blocks_anywhere(self):
        """Any ```text block in any doc is a WhatsApp message and must not leak Markdown bold."""
        block = re.compile(r"^```text\n(.*?)\n```", re.S | re.M)
        for path in list(ROOT.glob("docs/*.md")) + [ROOT / "README.md"] + list((ROOT / "skills").glob("*/SKILL.md")):
            for body in block.findall(path.read_text(encoding="utf-8")):
                self.assertNotRegex(body, r"\*\*\S", f"{path.name}: {body[:60]}")


class Zips(unittest.TestCase):
    def test_zips_have_one_top_folder_with_skill_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            with redirect_stdout(io.StringIO()):
                built = build_zips.build(Path(tmp))
            names = {p.name for p in built}
            self.assertEqual(names, {f"{n}.zip" for n in SKILL_NAMES} | {"whatsapp-skills-all.zip"})
            for name in SKILL_NAMES:
                with zipfile.ZipFile(Path(tmp) / f"{name}.zip") as zf:
                    entries = zf.namelist()
                    self.assertIn(f"{name}/SKILL.md", entries)
                    self.assertIn(f"{name}/scripts/wa_lint.py", entries)
                    self.assertEqual({e.split("/")[0] for e in entries}, {name})
                    self.assertFalse(any("/evals/" in e for e in entries))

    def test_zips_are_deterministic(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            with redirect_stdout(io.StringIO()):
                build_zips.build(Path(a))
                build_zips.build(Path(b))
            for name in SKILL_NAMES:
                self.assertEqual((Path(a) / f"{name}.zip").read_bytes(), (Path(b) / f"{name}.zip").read_bytes())


if __name__ == "__main__":
    unittest.main()
