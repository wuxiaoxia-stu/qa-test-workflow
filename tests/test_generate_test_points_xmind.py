import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "test-case-generation" / "generate_test_points_xmind.py"
PARSER_DIR = ROOT / "scripts" / "requirements-analysis"
sys.path.insert(0, str(PARSER_DIR))
from parse_formats import parse_xmind


SAMPLE_INPUT = {
    "title": "权益订单拆分",
    "modules": [
        {
            "title": "订单拆分",
            "dimensions": [
                {
                    "title": "正常流程",
                    "test_points": [
                        {
                            "id": "TP-001",
                            "priority": "P0",
                            "status": "Confirmed",
                            "source_id": "REQ-1",
                            "title": "满足条件时生成拆分订单",
                            "expected_result": "系统生成拆分订单，订单状态和明细符合需求定义。",
                        }
                    ],
                }
            ],
        }
    ],
}


class GenerateTestPointsXMindTest(unittest.TestCase):
    def run_generator(self, input_data):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            input_path = temporary_path / "test-points.json"
            output_path = temporary_path / "test-points.xmind"
            input_path.write_text(json.dumps(input_data, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(GENERATOR), str(input_path), "--output", str(output_path)],
                capture_output=True,
                text=True,
            )
            return result, output_path.exists()

    def run_generator_with_raw_input(self, raw_input):
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            input_path = temporary_path / "test-points.json"
            output_path = temporary_path / "test-points.xmind"
            input_path.write_text(raw_input, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(GENERATOR), str(input_path), "--output", str(output_path)],
                capture_output=True,
                text=True,
            )
            return result, output_path.exists()

    def test_generates_parseable_xmind_with_expected_hierarchy(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            input_path = temporary_path / "test-points.json"
            output_path = temporary_path / "test-points.xmind"
            input_path.write_text(json.dumps(SAMPLE_INPUT, ensure_ascii=False), encoding="utf-8")

            # Act
            result = subprocess.run(
                [sys.executable, str(GENERATOR), str(input_path), "--output", str(output_path)],
                capture_output=True,
                text=True,
            )

            # Assert
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertTrue(output_path.is_file())
            with zipfile.ZipFile(output_path) as archive:
                self.assertEqual(set(archive.namelist()), {"content.json", "metadata.json", "manifest.json"})
                content = json.loads(archive.read("content.json"))
                self.assertEqual(
                    json.loads(archive.read("metadata.json")),
                    {"creator": {"name": "qa-test-workflow", "version": "1.0"}, "activeSheetId": "sheet-1"},
                )
                self.assertEqual(
                    json.loads(archive.read("manifest.json")),
                    {"file-entries": {"content.json": {}, "metadata.json": {}}},
                )

            sheet = content[0]
            self.assertEqual(sheet["id"], "sheet-1")
            self.assertEqual(sheet["class"], "sheet")
            self.assertEqual(sheet["title"], "权益订单拆分 测试点")
            self.assertEqual(sheet["rootTopic"]["structureClass"], "org.xmind.ui.logic.right")
            self.assertEqual(sheet["rootTopic"]["class"], "topic")
            self.assertEqual(sheet["rootTopic"]["children"]["attached"][0]["class"], "topic")
            self.assertEqual(
                sheet["rootTopic"]["children"]["attached"][0]["children"]["attached"][0]["class"],
                "topic",
            )
            self.assertEqual(
                sheet["rootTopic"]["children"]["attached"][0]["children"]["attached"][0]["children"]["attached"][0]["class"],
                "topic",
            )
            self.assertEqual(
                [sheet["rootTopic"]["id"], sheet["rootTopic"]["children"]["attached"][0]["id"], sheet["rootTopic"]["children"]["attached"][0]["children"]["attached"][0]["id"], sheet["rootTopic"]["children"]["attached"][0]["children"]["attached"][0]["children"]["attached"][0]["id"]],
                ["topic-1", "topic-2", "topic-3", "topic-4"],
            )
            self.assertEqual(
                parse_xmind(output_path)["topics"],
                [
                    "权益订单拆分 测试点",
                    "权益订单拆分",
                    "订单拆分",
                    "正常流程",
                    "TP-001 [P0 | Confirmed | REQ-1] 满足条件时生成拆分订单 | 预期结果: 系统生成拆分订单，订单状态和明细符合需求定义。",
                ],
            )

    def test_rejects_invalid_root_title_and_empty_test_points(self):
        cases = []
        missing_title = json.loads(json.dumps(SAMPLE_INPUT))
        del missing_title["title"]
        cases.append((missing_title, "root title is required"))

        blank_title = json.loads(json.dumps(SAMPLE_INPUT))
        blank_title["title"] = "  "
        cases.append((blank_title, "root title is required"))

        no_test_points = json.loads(json.dumps(SAMPLE_INPUT))
        no_test_points["modules"][0]["dimensions"][0]["test_points"] = []
        cases.append((no_test_points, "at least one test point is required"))

        for input_data, error_text in cases:
            with self.subTest(error_text=error_text):
                # Arrange / Act
                result, output_exists = self.run_generator(input_data)

                # Assert
                self.assertEqual(result.returncode, 2)
                self.assertIn(error_text, result.stderr)
                self.assertFalse(output_exists)

    def test_rejects_duplicate_id_missing_or_blank_required_fields_and_invalid_values(self):
        duplicate_id = json.loads(json.dumps(SAMPLE_INPUT))
        duplicate_id["modules"][0]["dimensions"][0]["test_points"].append(
            json.loads(json.dumps(duplicate_id["modules"][0]["dimensions"][0]["test_points"][0]))
        )
        cases = [(duplicate_id, "duplicate test point id: TP-001")]

        for field in ("id", "priority", "status", "source_id", "title", "expected_result"):
            missing_field = json.loads(json.dumps(SAMPLE_INPUT))
            del missing_field["modules"][0]["dimensions"][0]["test_points"][0][field]
            cases.append((missing_field, f"test point field is required: {field}"))

            blank_field = json.loads(json.dumps(SAMPLE_INPUT))
            blank_field["modules"][0]["dimensions"][0]["test_points"][0][field] = "  "
            cases.append((blank_field, f"test point field is required: {field}"))

        invalid_priority = json.loads(json.dumps(SAMPLE_INPUT))
        invalid_priority["modules"][0]["dimensions"][0]["test_points"][0]["priority"] = "P9"
        cases.append((invalid_priority, "invalid priority: P9"))

        invalid_status = json.loads(json.dumps(SAMPLE_INPUT))
        invalid_status["modules"][0]["dimensions"][0]["test_points"][0]["status"] = "Draft"
        cases.append((invalid_status, "invalid status: Draft"))

        for input_data, error_text in cases:
            with self.subTest(error_text=error_text):
                # Arrange / Act
                result, output_exists = self.run_generator(input_data)

                # Assert
                self.assertEqual(result.returncode, 2)
                self.assertIn(error_text, result.stderr)
                self.assertFalse(output_exists)

    def test_rejects_malformed_json_and_missing_hierarchy_titles(self):
        malformed_result, malformed_output_exists = self.run_generator_with_raw_input("{")
        self.assertEqual(malformed_result.returncode, 2)
        self.assertIn("Expecting property name", malformed_result.stderr)
        self.assertFalse(malformed_output_exists)

        cases = []
        missing_module_title = json.loads(json.dumps(SAMPLE_INPUT))
        del missing_module_title["modules"][0]["title"]
        cases.append((missing_module_title, "module title is required"))

        missing_dimension_title = json.loads(json.dumps(SAMPLE_INPUT))
        del missing_dimension_title["modules"][0]["dimensions"][0]["title"]
        cases.append((missing_dimension_title, "dimension title is required"))

        for input_data, error_text in cases:
            with self.subTest(error_text=error_text):
                result, output_exists = self.run_generator(input_data)
                self.assertEqual(result.returncode, 2)
                self.assertIn(error_text, result.stderr)
                self.assertFalse(output_exists)


if __name__ == "__main__":
    unittest.main()
