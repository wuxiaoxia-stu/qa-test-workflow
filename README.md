# QA Test Workflow

[简体中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`qa-test-workflow` is a single Codex skill for end-to-end QA work: requirements review, test-case generation, and test-case review. It keeps documented facts, unresolved gaps, and industry-baseline candidates visibly separate so generated cases remain traceable and reviewable.

Generated QA artifacts default to Simplified Chinese. API names, configuration keys, IDs, and literal messages remain unchanged.

## Capabilities

| Mode | Use it for | Main deliverable |
| --- | --- | --- |
| `requirements-review` | Reviewing a PRD, story, acceptance criteria, API/UI specification, or testability | Requirement understanding, gaps, risks, testability impact, questions, and next steps |
| `test-case-generation` | Creating or supplementing cases from requirements | Traceable cases, test-point XMind companion, coverage matrix, requirements analysis, and final case review |
| `test-case-review` | Auditing an existing case set before execution or release | Severity-ranked findings, missing high-risk coverage, retest order, and residual risks |

The skill selects a mode automatically. State a mode explicitly when the request contains both requirements and existing test cases but you want a specific outcome.

## Install in Codex

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

## Install in Other Agents

This repository follows the Agent Skills layout: install the entire `qa-test-workflow` directory, not only `SKILL.md`. The `references/`, `scripts/`, `templates/`, `examples/`, and `evals/` directories are part of the package.

Clone the repository once, then copy its root directory to the target skills directory for your agent:

```bash
git clone https://github.com/wuxiaoxia-stu/qa-test-workflow.git
```

| Agent | Personal installation | Project installation | Notes |
| --- | --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/qa-test-workflow/` | `.claude/skills/qa-test-workflow/` | Use personal scope across projects, or commit the project scope for a team. |
| [Cursor](https://cursor.com/docs/context/skills) | `~/.cursor/skills/qa-test-workflow/` | `.cursor/skills/qa-test-workflow/` | Cursor also recognizes the compatible `.agents/skills/` layout. |
| [Trae](https://forum.trae.cn/t/topic/19464) | `~/.trae-cn/skills/qa-test-workflow/` for the China edition | `.trae/skills/qa-test-workflow/` | Use the project path when a Trae edition exposes a different personal directory. |

### File-Based Installation

On macOS or Linux, replace `<skills-parent>` with one of the table's parent directories, such as `~/.claude/skills` or `.cursor/skills`:

```bash
mkdir -p <skills-parent>
cp -R qa-test-workflow <skills-parent>/
```

On Windows PowerShell, use the target parent directory for the chosen agent:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force .\qa-test-workflow "$env:USERPROFILE\.claude\skills\"
```

For a project-scoped installation, run the equivalent commands from the project root and use `.claude/skills`, `.cursor/skills`, or `.trae/skills` as `<skills-parent>`. Open a new agent session after installation.

### Tencent WorkBuddy

Tencent WorkBuddy imports skills through its UI rather than a fixed file-system directory. Open **Skills** > **Add Skill** > **Import Local Skill Package**, then import the downloaded local package for this repository. Follow the import dialog if your client version requests a directory or an archive. Review `SKILL.md` and bundled scripts before granting an imported skill permissions.

## Use

Provide the requirement materials, cases, and intended action. The skill accepts PRDs, user stories, acceptance criteria, API/UI specifications, technical notes, release scope, defect history, and existing test cases.

```text
Review this PRD for testability and list the release-blocking gaps.

Generate Excel test cases for this API change, including requirements analysis and a final case review.

Audit these existing checkout test cases against the supplied acceptance criteria.
```

For generation, the workflow first builds a source inventory and requirements analysis, exports a test-point XMind companion, then reviews the case draft before delivering the revised final cases. The XMind file supplements rather than replaces the requested detailed-case format. Confirmed requirements, data-blocked conditional cases, and gap-derived candidates remain separate. A candidate never counts as confirmed acceptance coverage.

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
