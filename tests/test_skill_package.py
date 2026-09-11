from pathlib import Path
import unittest


REQUIRED_FILES = (
    "SKILL.md",
    "references/test-case-generation.md",
    "references/requirements-analysis/requirements-analysis.md",
    "references/test-case-review/test-case-review.md",
    "scripts/test-case-generation/generate_test_points_xmind.py",
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
        self.assertNotIn(r"C:\Users", skill)
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

    def test_generation_adds_test_point_xmind_as_a_companion_artifact(self):
        root = Path(__file__).resolve().parents[1]
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        generation = (root / "references/test-case-generation.md").read_text(
            encoding="utf-8"
        )
        eval_case = (root / "evals/cases/generation-full-workflow.yaml").read_text(
            encoding="utf-8"
        )

        self.assertIn("generate_test_points_xmind.py", skill)
        self.assertIn("<需求名称>_测试点.xmind", skill)
        self.assertIn("companion artifact", skill)
        self.assertIn("## Test Point XMind Companion", generation)
        self.assertIn("Confirmed", generation)
        self.assertIn("Conditional", generation)
        self.assertIn("Pending Confirmation", generation)
        self.assertIn("does not replace", generation)
        self.assertIn(
            "Default generated test cases to an Excel workbook", skill
        )
        self.assertIn("expected_result", generation)
        self.assertIn("\u9884\u671f\u7ed3\u679c", skill)
        for existing_expectation in (
            "Requirement Understanding",
            "Source Coverage Matrix",
            "Review Conclusion",
            "final review",
        ):
            self.assertIn(existing_expectation, eval_case)
        self.assertIn('- "测试点"', eval_case)
        self.assertIn('- ".xmind"', eval_case)

    def test_late_requirement_supplements_and_separate_scope_are_preserved(self):
        root = Path(__file__).resolve().parents[1]
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        generation = (root / "references/test-case-generation.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Treat later user messages", skill)
        self.assertIn("distinct data populations", skill)
        self.assertIn("later numbered supplement", generation)
        self.assertIn("multiple data populations", generation)

    def test_nested_readmes_do_not_reference_migrated_skills(self):
        root = Path(__file__).resolve().parents[1]
        readmes = (
            root / "references/requirements-analysis/README.md",
            root / "references/test-case-review/README.md",
        )

        for readme in readmes:
            text = readme.read_text(encoding="utf-8")
            self.assertIn("qa-test-workflow", text)
            self.assertNotIn("@skill", text)
            self.assertNotIn("install-skills", text)

    def test_explicit_skill_invocation_defaults_to_test_case_generation(self):
        root = Path(__file__).resolve().parents[1]
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        explicit_invocation_eval = (
            root / "evals/cases/explicit-invocation-default-generation.yaml"
        )

        self.assertIn("explicitly invokes `qa-test-workflow`", skill)
        self.assertIn("defaults to `test-case-generation`", skill)
        self.assertTrue(explicit_invocation_eval.is_file())

    def test_feishu_group_intake_requires_exact_keyword_and_preserves_order(self):
        root = Path(__file__).resolve().parents[1]
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        eval_case = (root / "evals/cases/feishu-group-intake.yaml").read_text(
            encoding="utf-8"
        )

        self.assertIn("exact contiguous substring `\u98de\u4e66\u7fa4`", skill)
        self.assertIn("`\u98de\u4e66` alone", skill)
        self.assertIn("`Feishu group`", skill)
        self.assertIn("`Lark group`", skill)
        self.assertIn("\u98de\u4e66\u7fa4\u9700\u6c42\u6458\u8981", skill)
        self.assertLess(
            skill.index("\u98de\u4e66\u7fa4\u9700\u6c42\u6458\u8981"),
            skill.index("pass the summary and its evidence references"),
        )
        self.assertIn("\u4ece\u98de\u4e66\u7fa4", eval_case)
        self.assertIn("\u4e0d\u542b\u98de\u4e66\u7fa4", eval_case)
        self.assertIn("\u4ec5\u542b\u98de\u4e66\u6216\u82f1\u6587\u8fd1\u4f3c\u8bcd", eval_case)
