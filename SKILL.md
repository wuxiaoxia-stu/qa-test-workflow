---
name: qa-test-workflow
description: End-to-end QA workflow for requirements review, test-point analysis, professional test-case generation, test-case review, coverage review, and release-gate QA. Use this skill whenever the user asks to analyze or review a PRD, user story, acceptance criteria, API/UI specification, generate or supplement test cases, audit existing test cases, or prepare QA deliverables for release, even when they do not name this skill.
---

# QA Test Workflow

Use this single workflow skill for requirement analysis, test-case generation, and test-case review. Preserve facts, assumptions, gaps, and candidate coverage as separate evidence classes so a draft never silently becomes an acceptance criterion.

## Input

Accept requirement documents, PRD, user stories, acceptance criteria, API/UI specifications, existing test cases, technical notes, release scope, defect history, dependencies, and constraints. Jira links and IDs are metadata only unless the user explicitly requests Jira traceability.

## Mode Routing

Select one mode before producing content.

1. An explicitly named mode wins: `requirements-review`, `test-case-generation`, or `test-case-review`.
2. When the user explicitly invokes `qa-test-workflow` without naming a mode or another action, defaults to `test-case-generation`. Run the full workflow and return the final test cases to the user.
3. Requests to generate, design, create, or supplement test cases use `test-case-generation` and run the full workflow.
4. Requests to review, audit, or check existing test cases use `test-case-review`.
5. Requests to analyze or review requirements, test points, ambiguity, or testability use `requirements-review`.
6. When both requirements and existing cases are supplied without a clear action, ask one question to distinguish generation from review, unless rule 2 applies.

## requirements-review

1. Read `references/requirements-analysis/requirements-analysis.md` before writing the analysis.
2. Read `references/requirements-analysis/output-formats.md` only when the user requests Excel, CSV, JSON, Word, or XMind output.
3. Use matching files in `templates/requirements-analysis/` and helpers in `scripts/requirements-analysis/` when a conversion is needed.
4. Return the required six sections in order: Requirement Understanding; Gaps and Ambiguities; Risk Assessment; Testability Impact; Questions to Resolve; Recommended Next Steps.
5. Mark assumptions, unresolved decisions, and missing materials explicitly. Do not invent endpoints, fields, policies, environments, or root causes.

## test-case-review

1. Read `references/test-case-review/test-case-review.md` before reviewing cases.
2. Use `scripts/test-case-review/` to parse the exact supplied document when needed. Its default prompt is already wired to this package.
3. Cross-check available requirements, analysis, technical notes, release scope, risks, and existing cases. State which sources are unavailable.
4. Return: verdict; Blocker/Critical findings or explicit none; Major/Minor findings; missing high-risk scenarios; fix priority and retest order; residual risks.
5. Every finding needs severity, evidence, business impact, and recommended action. Do not elevate style-only issues above Minor unless they make a case unexecutable.

## test-case-generation

1. Read `references/test-case-generation.md`, `references/requirements-analysis/requirements-analysis.md`, and `references/test-case-review/test-case-review.md`.
2. Build a complete source inventory and run `requirements-review` as the first internal phase. Treat later user messages that add, correct, or number a requirement as source evidence: reopen the analysis and append the item before drafting or revising cases.
3. After the analysis exists and before drafting detailed cases, build the test-point model described in `references/test-case-generation.md`. Run `python scripts/test-case-generation/generate_test_points_xmind.py <测试点模型.json> --output <需求名称>_测试点.xmind`. This XMind file is a companion artifact for `test-case-generation` only; it does not replace or change the detailed test-case artifact or add default outputs to the other modes.
4. Produce a draft only after the analysis and test-point companion exist. Map confirmed cases to the deepest documented requirement; map gap-derived candidates to a visible gap and named industry baseline.
5. Create the required coverage matrix, then run `test-case-review` against the exact draft.
6. Record a disposition for every review finding. Apply only findings supported by source facts, confirmed analysis facts, or an applicable industry baseline; retain unsupported findings as gaps or residual risks.
7. When a requirement states distinct data populations, permissions, or scopes, preserve each stated behavior as an independent trace target. For example, a cleanup that names main and child records needs separate cleanup coverage; a role configuration and its runtime visibility scope need separate coverage. Missing mappings or fixtures block execution, not the documented capability's coverage.
8. Re-run the coverage matrix and `test-case-review` against the revised artifact. Before delivery, reconcile every current source-inventory row, including late supplements and all numbered parent/child requirements, to a confirmed/conditional case or a visible gap. Deliver only the revised final cases, the analysis report, the `<需求名称>_测试点.xmind` companion artifact, and the final review report unless the user asks for a draft comparison.

## Output Rules

- Use Simplified Chinese by default; preserve API names, configuration keys, IDs, and documented literal messages.
- Default generated test cases to an Excel workbook. Use `spreadsheets:Spreadsheets` for workbook authoring and visual verification. Use Markdown, CSV, JSON, Word, or XMind only when explicitly requested.
- The format rule above still governs the detailed test-case artifact. The test-point XMind is generated in addition and does not change any existing test-case format or explicit format request.
- Keep confirmed requirement cases, conditional cases blocked by missing data, and gap-derived candidate cases separate in traceability and coverage totals.
- A candidate case must be labelled `Pending Confirmation`, trace to a visible gap, name its applicable industry baseline, and state the pending product decision. It cannot satisfy confirmed acceptance coverage or a release gate.
- Treat an incomplete requirement as a usable first draft with explicit gaps; do not fabricate product behavior to make it look complete.

## Delivery Check

Before delivery, confirm that every independent source item is classified, every documented acceptance criterion has confirmed or conditional coverage, all review findings have a disposition, and the final review covers the exact revised artifact.
