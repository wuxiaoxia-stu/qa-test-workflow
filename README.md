# QA Test Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`qa-test-workflow` is a single Codex skill for end-to-end QA work: requirements review, test-case generation, and test-case review. It keeps documented facts, unresolved gaps, and industry-baseline candidates visibly separate so generated cases remain traceable and reviewable.

Generated QA artifacts default to Simplified Chinese. API names, configuration keys, IDs, and literal messages remain unchanged.

## Capabilities

| Mode | Use it for | Main deliverable |
| --- | --- | --- |
| `requirements-review` | Reviewing a PRD, story, acceptance criteria, API/UI specification, or testability | Requirement understanding, gaps, risks, testability impact, questions, and next steps |
| `test-case-generation` | Creating or supplementing cases from requirements | Traceable cases, coverage matrix, requirements analysis, and final case review |
| `test-case-review` | Auditing an existing case set before execution or release | Severity-ranked findings, missing high-risk coverage, retest order, and residual risks |

The skill selects a mode automatically. State a mode explicitly when the request contains both requirements and existing test cases but you want a specific outcome.

## Install

Codex loads a personal skill when its directory contains `SKILL.md` under the Codex skills directory.

### macOS and Linux

```bash
git clone https://github.com/wuxiaoxia-stu/qa-test-workflow.git
mkdir -p ~/.codex/skills
cp -R qa-test-workflow ~/.codex/skills/
```

### Windows PowerShell

```powershell
git clone https://github.com/wuxiaoxia-stu/qa-test-workflow.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force .\qa-test-workflow "$env:USERPROFILE\.codex\skills\"
```

Start a new Codex task after installation so the skill list is refreshed.

## Use

Provide the requirement materials, cases, and intended action. The skill accepts PRDs, user stories, acceptance criteria, API/UI specifications, technical notes, release scope, defect history, and existing test cases.

```text
Review this PRD for testability and list the release-blocking gaps.

Generate Excel test cases for this API change, including requirements analysis and a final case review.

Audit these existing checkout test cases against the supplied acceptance criteria.
```

For generation, the workflow first builds a source inventory and requirements analysis, then reviews the case draft before delivering the revised final cases. Confirmed requirements, data-blocked conditional cases, and gap-derived candidates remain separate. A candidate never counts as confirmed acceptance coverage.

## Repository Layout

```text
SKILL.md                         Machine-facing workflow and mode routing
references/                      Detailed requirements, generation, and review guidance
scripts/                         Standard-library helpers for common artifact formats
templates/                       Output templates
examples/                        Review input and output samples
evals/                           Skill evaluation cases
tests/                           Package integrity regression tests
```

## Verify Locally

The bundled scripts use the Python standard library. From the repository root, run:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python -m compileall -q scripts
```

On Codex Desktop, replace `python` with the bundled Python runtime if your system Python is unavailable.

## Contributing and Security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Report sensitive findings through the private path in [SECURITY.md](SECURITY.md), not in a public issue.

## License

This project is licensed under the [MIT License](LICENSE).
