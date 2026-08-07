from pathlib import Path
import unittest


REQUIRED_FILES = (
    "SKILL.md",
    "references/test-case-generation.md",
    "references/requirements-analysis/requirements-analysis.md",
    "references/test-case-review/test-case-review.md",
    "scripts/requirements-analysis/parse_formats.py",
    "scripts/test-case-review/run_review.py",
    "evals/eval.yaml",
)


class SkillPackageTest(unittest.TestCase):
    def test_skill_is_self_contained_and_declares_all_modes(self):
        root = Path(__file__).resolve().parents[1]
        skill = (root / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("name: qa-test-workflow", skill)
        self.assertIn("requirements-review", skill)
        self.assertIn("test-case-generation", skill)
        self.assertIn("test-case-review", skill)
        self.assertNotIn("invoke `requirements-analysis`", skill)
        self.assertNotIn("invoke `test-case-reviewer-plus`", skill)

        for relative_path in REQUIRED_FILES:
            self.assertTrue((root / relative_path).is_file(), relative_path)

    def test_generation_reference_uses_internal_phases(self):
        root = Path(__file__).resolve().parents[1]
        generation = (root / "references/test-case-generation.md").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("invoke `requirements-analysis`", generation)
        self.assertNotIn("invoke `test-case-reviewer-plus`", generation)
