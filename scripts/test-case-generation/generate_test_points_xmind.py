#!/usr/bin/env python3
import argparse
import itertools
import json
from pathlib import Path
import sys
import zipfile


REQUIRED_POINT_FIELDS = (
    "id",
    "priority",
    "status",
    "source_id",
    "title",
    "expected_result",
)
VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}
VALID_STATUSES = {"Confirmed", "Conditional", "Pending Confirmation"}


class InputValidationError(ValueError):
    pass


def _has_text(value):
    return isinstance(value, str) and bool(value.strip())


def validate(data):
    if not isinstance(data, dict) or not _has_text(data.get("title")):
        raise InputValidationError("root title is required")

    modules = data.get("modules")
    if not isinstance(modules, list):
        modules = []
    points = []
    for module in modules:
        if not isinstance(module, dict) or not _has_text(module.get("title")):
            raise InputValidationError("module title is required")
        dimensions = module.get("dimensions")
        if not isinstance(dimensions, list):
            continue
        for dimension in dimensions:
            if not isinstance(dimension, dict) or not _has_text(dimension.get("title")):
                raise InputValidationError("dimension title is required")
            test_points = dimension.get("test_points")
            if isinstance(test_points, list):
                points.extend(test_points)

    if not points:
        raise InputValidationError("at least one test point is required")

    seen_ids = set()
    for point in points:
        if not isinstance(point, dict):
            raise InputValidationError("test point field is required: id")
        for field in REQUIRED_POINT_FIELDS:
            if not _has_text(point.get(field)):
                raise InputValidationError(f"test point field is required: {field}")
        if point["priority"] not in VALID_PRIORITIES:
            raise InputValidationError(f"invalid priority: {point['priority']}")
        if point["status"] not in VALID_STATUSES:
            raise InputValidationError(f"invalid status: {point['status']}")
        if point["id"] in seen_ids:
            raise InputValidationError(f"duplicate test point id: {point['id']}")
        seen_ids.add(point["id"])


def _topic(title, topic_ids):
    return {"id": f"topic-{next(topic_ids)}", "class": "topic", "title": title}


def build_content(data):
    topic_ids = itertools.count(1)
    root_topic = _topic(data["title"], topic_ids)
    root_topic["structureClass"] = "org.xmind.ui.logic.right"
    module_topics = []
    for module in data["modules"]:
        module_topic = _topic(module["title"], topic_ids)
        dimension_topics = []
        for dimension in module["dimensions"]:
            dimension_topic = _topic(dimension["title"], topic_ids)
            point_topics = []
            for point in dimension["test_points"]:
                point_topics.append(
                    _topic(
                        f"{point['id']} [{point['priority']} | {point['status']} | "
                        f"{point['source_id']}] {point['title']} | "
                        f"预期结果: {point['expected_result']}",
                        topic_ids,
                    )
                )
            dimension_topic["children"] = {"attached": point_topics}
            dimension_topics.append(dimension_topic)
        module_topic["children"] = {"attached": dimension_topics}
        module_topics.append(module_topic)
    root_topic["children"] = {"attached": module_topics}
    return [
        {
            "id": "sheet-1",
            "class": "sheet",
            "title": f"{data['title']} 测试点",
            "rootTopic": root_topic,
        }
    ]


def write_xmind(data, output_path):
    content = json.dumps(build_content(data), ensure_ascii=False)
    metadata = json.dumps(
        {"creator": {"name": "qa-test-workflow", "version": "1.0"}, "activeSheetId": "sheet-1"},
        ensure_ascii=False,
    )
    manifest = json.dumps({"file-entries": {"content.json": {}, "metadata.json": {}}})
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("content.json", content.encode("utf-8"))
        archive.writestr("metadata.json", metadata.encode("utf-8"))
        archive.writestr("manifest.json", manifest.encode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Generate an XMind test-points map from JSON")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        validate(data)
        write_xmind(data, args.output)
    except (OSError, json.JSONDecodeError, InputValidationError) as error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
