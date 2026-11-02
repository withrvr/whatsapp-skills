"""Every skill meets the Agent Skills spec and the repo's conventions, and the
examples it teaches from obey its own rules."""
from __future__ import annotations

import json
import re
import unittest

from helpers import EXAMPLES_TODAY, ROOT, SKILL_NAMES, SKILLS, text_blocks, validate, wa_lint

CHECK_TYPES = {
    "starts_with_message", "message_count", "contains", "icontains", "contains_any", "not_contains",
    "regex", "not_regex", "response_regex", "response_not_regex", "max_chars", "min_chars",
    "max_emoji", "script", "lint_clean",
}


class Spec(unittest.TestCase):
    def test_there_are_skills(self):
        self.assertGreaterEqual(len(SKILLS), 8)

    def test_spec_rules(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertEqual(validate.validate_spec(skill), [])

    def test_repo_conventions(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                self.assertEqual(validate.validate_conventions(skill), [])

    def test_validator_catches_bad_names(self):
        """Guard the validator itself: a broken check would pass everything."""
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "Bad--Name"
            bad.mkdir()
            (bad / "SKILL.md").write_text("---\nname: Bad--Name\ndescription: x\nfoo: bar\n---\nbody\n")
            errors = " | ".join(validate.validate_spec(bad))
            self.assertIn("lowercase", errors)
            self.assertIn("consecutive hyphens", errors)
            self.assertIn("unexpected frontmatter fields: foo", errors)

    def test_descriptions_are_distinct_enough_to_route(self):
        """Each description names what it is NOT for, pointing at a real sibling."""
        for skill in SKILLS:
            data, _, _ = validate.parse(skill / "SKILL.md")
            with self.subTest(skill=skill.name):
                pointers = set(re.findall(r"whatsapp-[a-z-]+", data["description"])) - {skill.name}
                self.assertTrue(pointers, "description should point at a sibling skill")
                self.assertTrue(pointers <= set(SKILL_NAMES))


class Examples(unittest.TestCase):
    """The examples are what the model imitates. They must be flawless."""

    def test_examples_lint_clean(self):
        for skill in SKILLS:
            doc = (skill / "references" / "examples.md").read_text(encoding="utf-8")
            blocks = text_blocks(doc)
            with self.subTest(skill=skill.name):
                self.assertGreaterEqual(len(blocks), 4, "at least 4 worked examples")
            for i, block in enumerate(blocks, 1):
                kind = "status" if skill.name == "whatsapp-status" else "message"
                report = wa_lint.lint(block, kind=kind, today=EXAMPLES_TODAY)
                with self.subTest(skill=skill.name, block=i):
                    self.assertEqual([f"{f.code}: {f.message}" for f in report.errors], [])
                    self.assertEqual([f"{f.code}: {f.message}" for f in report.warnings], [],
                                     f"example {i} should be warning-free:\n{block}")

    def test_skill_md_examples_lint_clean(self):
        for skill in SKILLS:
            body = (skill / "SKILL.md").read_text(encoding="utf-8")
            for block in text_blocks(body):
                report = wa_lint.lint(block, today=EXAMPLES_TODAY)
                with self.subTest(skill=skill.name):
                    self.assertEqual(report.codes("error"), [], block)

    def test_status_examples_fit_one_glance(self):
        doc = (ROOT / "skills" / "whatsapp-status" / "references" / "examples.md").read_text(encoding="utf-8")
        for block in text_blocks(doc):
            self.assertLessEqual(len(block), 200, block)


class Evals(unittest.TestCase):
    def test_every_skill_has_evals_in_spec_format(self):
        for skill in SKILLS:
            data = json.loads((skill / "evals" / "evals.json").read_text(encoding="utf-8"))
            with self.subTest(skill=skill.name):
                self.assertEqual(data["skill_name"], skill.name)
                self.assertGreaterEqual(len(data["evals"]), 3)
                ids = [e["id"] for e in data["evals"]]
                names = [e["name"] for e in data["evals"]]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertEqual(len(names), len(set(names)))
            for e in data["evals"]:
                with self.subTest(skill=skill.name, eval=e.get("name")):
                    for key in ("id", "prompt", "expected_output", "assertions", "checks"):
                        self.assertIn(key, e)
                    self.assertTrue(all(isinstance(a, str) and a for a in e["assertions"]))
                    self.assertTrue(e["checks"])
                    for c in e["checks"]:
                        self.assertIn(c["type"], CHECK_TYPES)
                        if "pattern" in c:
                            re.compile(c["pattern"])

    def test_check_types_match_the_runner(self):
        runner = (ROOT / "scripts" / "run_evals.py").read_text(encoding="utf-8")
        for t in CHECK_TYPES:
            self.assertIn(f'"{t}"', runner, f"run_evals.py doesn't grade '{t}'")


if __name__ == "__main__":
    unittest.main()
