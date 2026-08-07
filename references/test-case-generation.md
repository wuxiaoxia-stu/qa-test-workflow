---
name: qa-test-workflow-generation
description: Internal generation rules for qa-test-workflow.
---

# QA Test Case Generator

Generate professional QA test cases from documented requirements. The goal is to behave like a senior QA engineer: extract facts first, flag unclear requirements, then produce atomic and verifiable test cases that can be imported into Jira-style test management tools.

This skill is adapted from the GitHub Gist `PramodDutta/Testcase.md` and converted into a Codex-compatible skill.

## Workflow

Follow these steps in order.

1. Read the source material supplied by the user:
   - PRD, feature spec, user story, acceptance criteria, API spec, UI spec, or attached document.
   - Treat Jira tickets, Jira IDs, and Jira links as optional metadata. Do not read, request, infer, or use Jira requirement content unless the user explicitly asks for Jira traceability.
   - Build a source inventory before analysis. Record every heading, numbered item, table row, figure, screenshot annotation, menu tree, and role/permission label that states or qualifies behavior. For browser-based documents, inspect the full page and all embedded images before concluding that the source has no additional requirements.
   - Preserve the source location for each inventory item. A numbered child requirement such as `2.1` or `3` is independently traceable even when the top-level requirement describes a related feature.
   - When the user supplies a later numbered supplement or correction, treat it as new source material rather than a note on the previous output. Reopen the source inventory, requirements analysis, hierarchy, coverage matrix, and final review before delivery.

2. Mandatory pre-generation requirements analysis:
   - Always complete this package's `requirements-review` phase after reading the source material and before generating test cases, even when the user asks only for final test cases or supplies a short requirement. A user-supplied analysis is additional input; it does not remove this gate.
   - Pass the original requirements plus any supplied business context, release scope, dependencies, constraints, technical notes, known issues, and existing analysis to `references/requirements-analysis/requirements-analysis.md`.
   - Create a requirements analysis artifact in the required order: Requirement Understanding; Gaps and Ambiguities; Risk Assessment; Testability Impact; Questions to Resolve; Recommended Next Steps.
   - Treat the original source and the analysis artifact as separate evidence. Documented or explicitly confirmed facts become confirmed requirement cases. A testability-impacting gap may additionally become a clearly labeled gap-derived candidate case only when its expected result is grounded in an applicable industry baseline source; it never becomes a confirmed product requirement.
   - Do not start hierarchy mapping, case drafting, or coverage accounting until the requirements analysis artifact exists. When the requested output format is case-only, keep the full artifact in the working context and surface its documented gaps and candidate-case mapping in the format's designated gap location.

3. Build the requirement hierarchy before extracting testable facts:
   - Use the source inventory as the completeness gate: every inventory item must be classified as a confirmed behavior, a conditional confirmed behavior, a gap, or non-requirement context. Do not omit an item because another top-level requirement looks similar.
   - Treat a figure, screenshot, menu tree, or permission matrix as requirement evidence when it visibly adds page names, access-control items, data scope, or acceptance behavior to the surrounding text. Record the figure location in the hierarchy instead of silently treating it as decoration.
   - When the source uses separate verbs such as add, rename, split, remove, regress, authorize, or clean, retain separate direct behaviors. Do not collapse them into a single page-exists case.
   - Parse heading levels, numbering, indentation, page/tab labels, and explicit parent-child wording. Preserve the source wording and source location.
   - Classify only supported nodes as `L1` large requirement/epic, `L2` module/page/tab/sub-requirement, or `L3` leaf behavior/acceptance criterion. Do not invent requirement IDs.
   - For every leaf behavior, record its explicit requirement ID when provided, direct requirement node, full ancestor path, source location, and covered behavior.
   - Assign each test case to the deepest node that explicitly states the behavior. Keep ancestor nodes for traceability; do not flatten a child requirement into its top-level parent.
   - Keep confirmed hierarchy coverage and gap-derived candidate coverage separate. Do not add a candidate case ID to an L1/L2/L3 row's `Covered Test Case IDs`, create a `Gap` hierarchy level, or synthesize an L2/L3 node from a gap. Put candidate IDs only in the `Candidate Case Mapping`, using the documented ancestor path as context when one exists.
   - If the parent-child relationship is unclear, flag the hierarchy as a requirement gap before generating cases instead of silently assigning the behavior to the nearest top-level requirement.

4. Extract only documented facts:
   - Feature description and scope.
   - Explicit regression requirements such as "keep existing flow working" or "regression normal". Create confirmed regression cases using the published baseline as the oracle; do not discard them merely because the source does not enumerate every field or message.
   - Explicit permission, data-migration, cleanup, or configuration requirements. Missing configuration values or complete mappings limit the test data and can block execution, but do not erase the documented capability from coverage.
   - When a cleanup names multiple data populations, preserve each named population as an independent direct behavior. When a role requirement states both configuration and a visibility limit, cover the configuration and the runtime data scope separately; do not collapse them into a generic list-exists case.
   - Category words such as "other", "etc.", "all", "only", "except", "new", or "independent". These change the coverage partition and must be represented in the analysis.
   - Acceptance criteria.
   - Business rules and calculations.
   - Field validations, constraints, ranges, formats, and required/optional behavior.
   - Technical dependencies, APIs, integrations, async jobs, or third-party systems.
   - Explicit edge cases.
   - UI/UX behavior and visible messages.
   - Error handling behavior.

5. Identify gaps and add controlled candidate coverage:
   - Distinguish an incomplete explicit requirement from an absent requirement. When the source states the behavior but omits an enum, timing, mapping, or exact fixture, create a confirmed conditional case that asserts only the stated behavior and lists the missing item as a blocking precondition or gap reference. Use a gap-derived candidate only when the behavior itself is absent from the source and an industry baseline supplies the proposed behavior.
   - A missing role matrix must not replace source-stated permission configuration or data-filtering cases with a single generic security candidate. Cover the stated permission behavior as confirmed conditional cases; reserve the candidate for unstated access semantics such as exact denial responses.
   - A missing cleanup mapping must not remove source-stated cleanup, isolation, or role-scope cases. Keep their expected results bounded by the published cleanup baseline and flag the unavailable mapping as a blocking prerequisite.
   - Do not invent missing product requirements. A gap-derived candidate case is a test proposal, not an acceptance criterion, requirement ID, or release approval.
   - Create a visible gap record for every ambiguous, conflicting, or testability-impacting item, including ownership, page/tab scope, parent-child relationships, business rules, validations, error handling, data changes, permissions, integrations, and observable outcome.
   - For each material gap, create one or more gap-derived candidate test cases when an applicable industry baseline source supports an observable expected result. Use a named, publicly identifiable source such as an applicable standard, RFC, OWASP or NIST publication, official platform policy, API contract, or regulatory rule; include the source version and control/section when available.
   - Do not create a candidate case when no applicable baseline can support an observable result. Keep that item as a gap warning and a question to resolve; do not substitute an invented user flow, exact threshold, message, status code, business calculation, retention period, or product policy.
   - Keep candidate cases separate from confirmed requirement cases. A candidate may use the nearest documented module and ancestor path for context, but its direct trace target is the numbered gap record, not an invented L3 behavior or requirement ID.
   - If a scenario cannot be validated from the available requirements or an applicable baseline, add a gap warning before the table.

Use this gap format:

```markdown
> Gap Identified: Insufficient information in the supplied requirements to validate [specific scenario]. Recommend clarification from PO/BA.
```

6. Design confirmed cases and eligible gap-derived candidate cases:
   - For an explicit category partition, create positive coverage for named categories, exclusion coverage for named categories that belong elsewhere, and an aggregate disjointness/completeness check when the source requires a split without loss. For an open category such as "other self-operated channels", include a conditional case using one business-confirmed representative; if no representative is available, keep the case and mark its data prerequisite as the associated gap.
   - For explicitly required regression flows, create a case per named flow and relevant changed page. Expected results may compare with the release baseline when the requirement does not define a product-specific value.
   - For explicitly required permissions, configurations, migrations, or cleanups, cover the stated configuration, filtering/scope, direct access surfaces, and lifecycle or rerun behavior only where each behavior is source-stated. Mark missing product decisions as blocking gaps rather than deleting the coverage row.
   - Positive scenarios: when happy paths or acceptance criteria are described.
   - Negative scenarios: when invalid input, error handling, or rejection rules are specified.
   - Boundary value: when min/max limits, ranges, lengths, or thresholds are defined.
   - Field validation: when required fields, formats, uniqueness, data types, or constraints are defined.
   - Error handling: when errors, fallback behavior, retries, or messages are documented.
   - Integration: when APIs, external systems, queues, events, or dependencies are mentioned.
   - Security: when auth, authorization, privacy, data protection, or permission rules are specified.
   - Performance: when response time, load, concurrency, timeout, or throughput criteria are specified.
   - Gap-derived candidate cases: when a documented capability has a material functional, security, data-integrity, interoperability, accessibility, or reliability gap and a named industry baseline supplies an appropriate observable expectation.
   - For every candidate case, write the expected-result cell as `Candidate Expected Result (Industry Baseline, Pending Confirmation): [observable result]. Basis: [source, version, section/control]. Pending product decision: [specific missing rule].`
   - Do not use a candidate baseline to invent product-specific wording, values, timing, roles, error codes, user journeys, pricing, or business semantics. Mark the candidate as `Pending Confirmation` until PO/BA or the requirement owner explicitly adopts, replaces, or rejects it.

7. Before final output, check coverage:
   - Add a Source Coverage Matrix that lists every source-inventory item, its direct requirement path, its status (`Covered`, `Conditional - blocked by gap`, `Gap only`, or `Non-requirement context`), and its covering case IDs. A document with an uncovered numbered section, table requirement, or figure-based permission item cannot be treated as complete.
   - Count `Conditional - blocked by gap` cases separately from gap-derived candidates. Conditional cases remain confirmed requirement coverage because their behavior is explicit; candidates do not.
   - Test-case count is not a coverage metric. A compact case set is acceptable only when the matrix shows that no independent behavior, category exclusion, required regression flow, permission capability, or data-cleanup capability was collapsed or omitted.
   - Every documented acceptance criterion should map to at least one test case.
   - Every material gap should map either to at least one gap-derived candidate case with a stated baseline source or to a gap warning that explains why no valid baseline exists.
   - Each behavior should appear once unless a different layer or input class justifies another case.
   - Verify every case maps to the deepest applicable requirement node and retains its full ancestor path.
   - Count confirmed requirement coverage and gap-derived candidate coverage separately. Candidate cases do not satisfy confirmed acceptance-criterion coverage and cannot be used as the sole release gate.
   - List unmapped, ambiguous, incorrectly flattened, or baseline-unsuitable acceptance criteria as gaps.

8. Mandatory post-generation review gate:
   - Require the reviewer to reconcile the generated workbook against the Source Coverage Matrix, including all numbered sections and figure-derived behavior. The reviewer must flag any source item that was silently converted into a gap, candidate, or high-level combined case without explicit traceability.
   - Treat the generated cases as a draft until review findings have been processed. A test-case generation task is incomplete until the draft has been reviewed. Always complete this package's `test-case-review` phase after the coverage check, even when the user asks only for case generation and does not explicitly request a review.
   - Pass the generated artifact, the original requirements, the requirements analysis artifact, and any supplied technical notes, scope, risk, dependency, or defect-history context to the reviewer. The reviewer must cross-check cases against both the source requirement hierarchy and the analysis artifact's risks, gaps, testability impacts, and unanswered questions.
   - Require the reviewer to validate each gap-derived candidate case's gap trace, industry-baseline source, source applicability, observable expected result, pending-product decision, separate coverage count, and `Pending Confirmation` label. The reviewer must flag any candidate that presents a baseline as a confirmed product requirement.
   - Follow `references/test-case-review/test-case-review.md` and its required output order. The review must include a Pass/Conditional Pass/Fail verdict; explicit Blocker/Critical findings or an explicit none; Major/Minor findings; positive, negative, and boundary coverage gaps; traceability and step/expectation quality; missing high-risk scenarios; business impact; fix priority and retest/regression order; and residual risks.
   - Review the exact generated draft. For Excel, review the workbook or use the review skill's existing parser/helper when needed; for Markdown or mind-map output, review the exact generated content.

9. Apply review findings before final delivery:
   - After the review is complete, create a disposition for every finding. Apply each finding supported by the original requirements, confirmed facts in the requirements analysis artifact, or an applicable industry-baseline source by modifying the relevant case. Keep unsupported findings as documented gaps or residual risks instead of inventing behavior.
   - Rerun the coverage check after the revisions, then complete the `test-case-review` phase once more against the exact revised final artifact, original requirements, and requirements analysis artifact. The final review must confirm the revised cases, not only the original draft.
   - The externally delivered test-case artifact must be the revised final version. Do not label or deliver the initial draft as final. Deliver the revised final test cases together with the final review report; provide the initial draft only when the user explicitly requests a before/after comparison.

## Requirements Analysis Handoff

Use the requirements analysis artifact as the handoff contract between analysis, generation, review, and revision:

| Analysis output | Required downstream use |
|---|---|
| Confirmed scope and explicit behavior | Confirmed requirement hierarchy, case traceability, and executable expected results |
| Gaps, ambiguities, assumptions, and unresolved questions | Gap warnings and either gap-derived candidate cases with an applicable industry baseline or residual risks explaining why no valid baseline exists |
| Risk assessment and testability impact | Case priority, coverage focus, and reviewer high-risk-scenario checks |
| Dependencies and impacts | Integration coverage only when the original requirement documents the behavior |

The required execution order is: `requirements-review` -> draft test cases -> `test-case-review` -> revised test cases -> final `test-case-review` -> final test cases.

## Gap-Derived Candidate Cases

Use this contract for every case created from an identified requirement gap:

| Required item | Rule |
|---|---|
| Classification | Mark as `Gap-derived candidate` and `Pending Confirmation`; do not call it a confirmed requirement case. |
| Traceability | Reference the visible numbered gap record and retain the documented module and ancestor path when available. Do not invent a requirement ID or L3 behavior. |
| Industry baseline source | Name the applicable source and, where available, its version plus control, section, or contract clause. A vague claim that something is "industry common" is not sufficient. |
| Candidate expected result | State one observable pass/fail result, label it `Candidate Expected Result (Industry Baseline, Pending Confirmation)`, and name the exact product decision still awaiting confirmation. |
| Scope | Do not use the baseline to infer business-specific values, content, rules, permissions, flows, or timing. |
| Release use | Keep it out of confirmed-requirement coverage and the default smoke/release gate until the owner confirms it. |

Add a `Candidate Case Mapping` beside the gap list with: gap number, candidate case ID, documented module/path, industry baseline source, candidate expected result, and pending product decision. Reuse the gap number already visible in the analysis artifact; it is not a requirement ID.

## Test Case Rules

Each test case should be:

- Atomic: validate exactly one behavior.
- Traceable: map a confirmed case to the deepest applicable acceptance criterion or leaf requirement; map a gap-derived candidate case to its visible gap record and named industry baseline. Retain the full parent path for context. Add a Jira ID only when the user explicitly requests Jira traceability.
- Verifiable: expected result has observable pass/fail criteria. Candidate cases must use the required candidate-expected-result label and source instead of presenting the result as product-confirmed.
- Precise: avoid vague wording like "works properly" or "error is shown".
- Data-backed: include concrete test data when the requirement defines or implies usable values.
- Reproducible: include clear preconditions and ordered steps.

## Requirement Hierarchy Rules

Use the following mapping for every requirement-driven test case:

| Level | Meaning | Example |
|---|---|---|
| L1 | Large requirement, epic, or overall change scope | `大需求1` |
| L2 | Module, page, tab, or child requirement | `新增「银联订单」页签` |
| L3 | Atomic behavior or acceptance criterion | `删除「收款主体」筛选项和列表显示` |

For the supplied example, the direct ownership is `L2 > L3`, not `L1` alone:

```text
L1 大需求1
└── L2 新增「银联订单」页签
    ├── L3 前端删除「收款主体」字段筛选项及列表显示
    └── L3 该列表导出去除「收款主体」字段
```

- Use the L3 behavior as the direct trace target for a test case, use the L2 node as the module/page context, and retain L1 as the ancestor path.
- Do not promote a child page/tab requirement to the L1 requirement merely because the L1 heading appears first.
- When the source does not provide a requirement ID, write `N/A` or `未提供`; do not create `REQ-001`, `PRD-001`, or similar identifiers.
- If the output format has no dedicated hierarchy columns, keep the exact case columns unchanged. In Excel, add a `Requirement Hierarchy` mapping table to the `说明与缺口` worksheet; in Markdown/CSV, add a compact `Requirement Hierarchy` block immediately before the case table. Both mappings must include the level, source wording, direct parent, full path, source location, and covered test case IDs.
- Keep `需求编号` or `Requirement ID` limited to an explicit source identifier or `N/A`/`未提供`; do not put the hierarchy path into the identifier field.

## Jira Handling

- Ignore Jira requirement content, ticket links, and Jira IDs by default. Design cases only from the non-Jira source material supplied by the user.
- Do not create a requirement gap, request additional information, or block case generation because Jira information is unavailable.
- Include Jira information only when the user explicitly requests it. When using the default table format without an explicitly requested Jira ID, set the `Jira ID` cell to `N/A`.

- In the default Excel format, use `需求编号` for the explicit PRD or requirement reference. Add a separate `Jira ID` column only when the user explicitly requests Jira traceability or provides a Jira-compatible template.

## Output Format

### Default: Excel Workbook

Unless the user explicitly requests another presentation format, create and deliver an `.xlsx` workbook. Use the `spreadsheets:Spreadsheets` skill for workbook authoring, formatting, export, and visual verification.

The workbook must contain these four worksheets in this order:

1. `说明与缺口`: source URL and source files, requirement summary, documented gaps, `Candidate Case Mapping`, execution prerequisites, and smoke exit criteria.
2. `冒烟用例`: P0 primary flows and high-risk compatibility checks. Keep smoke cases separate from full regression cases.
3. `详细用例`: complete regression cases, separating confirmed requirement cases from explicitly labeled gap-derived candidate cases. Include positive, negative, boundary, integration, security, and performance cases only when supported by the requirements or by an applicable named industry baseline for a documented gap.
4. `覆盖统计`: formula-driven totals for smoke cases, detailed cases, priorities, test types, requirement gaps, confirmed requirement-clause coverage, and gap-derived candidate coverage.

The `冒烟用例` and `详细用例` worksheets must use these exact columns in this order:

| 测试用例 ID | 需求编号 | 模块/功能 | 测试用例标题 | 前置条件 | 测试步骤 | 测试数据 | 预期结果 | 优先级 | 测试类型 |
|---|---|---|---|---|---|---|---|---|---|

Workbook rules:

- In `说明与缺口`, add a `Source Requirement Inventory` before the hierarchy mapping. Include source location, exact behavior, classification, coverage status, blocking gap, and case IDs. Include figures and screenshots that contain requirement information.
- A confirmed case blocked only by unavailable fixtures, enums, mappings, or baseline data stays in `详细用例`. Put the gap ID and required prerequisite in its precondition; do not relabel it as a candidate or exclude it from confirmed coverage.
- Keep `测试步骤` as numbered steps inside the cell, with line breaks between steps.
- Use `需求编号` for the explicit PRD/requirement reference. Do not invent Jira IDs or relabel a requirement number as a Jira ID.
- Use Simplified Chinese for worksheet names and case content unless the user requests another language; preserve API names, event names, configuration keys, and exact documented messages.
- Add filters and freeze the header row on the two case worksheets.
- Add list validation for `优先级` (`严重`, `高`, `中`, `低`) and `测试类型` (`功能`, `负向`, `边界`, `集成`, `安全`, `性能`).
- Use formulas for `覆盖统计`; do not hardcode counts that can be calculated from the case sheets.
- Save the final workbook under `outputs/<unique_thread_id>/` and visually verify every worksheet before delivery.
- Keep gap warnings and the `Candidate Case Mapping` in `说明与缺口`. Add candidate rows to `详细用例` with a title beginning `验证[候选]`; set their requirement-reference cell to `N/A` unless the source supplied one, and keep their `Pending Confirmation` status, baseline source, and gap number in the mapping rather than adding columns to the fixed case table.
- Do not place a gap-derived candidate in `冒烟用例`, count it as confirmed coverage, or turn undocumented behavior into an unlabeled deterministic expected result.

### Explicit non-Excel formats

Use a Markdown table with these exact columns only when the user explicitly requests Markdown or CSV-compatible content. Keep the dedicated Mind Map Mode below for explicit mind-map requests.

| Test Case ID | Jira ID | Module/Feature | Test Case Title | Preconditions | Test Steps | Test Data | Expected Result | Priority | Test Type |

After the requirement-hierarchy block and before the case table, add a `Candidate Case Mapping` when any gap-derived candidate case exists. Keep the fixed case-table columns unchanged; candidate titles must begin `验证[候选]`, and their expected results must use the required candidate label and baseline source.
|---|---|---|---|---|---|---|---|---|---|

### Language

- Unless the user explicitly requests another language, write all test case content, test steps, expected results, test data descriptions, and gap warnings in Simplified Chinese.
- Keep column headers, test case IDs, API names, event names, configuration keys, and documented literal messages unchanged when format compatibility or traceability requires it. Preserve Jira IDs only when the user explicitly requests Jira traceability.

### Mind Map Mode

Use this mode when the user asks for a "思维导图", "脑图", "导图", or a hierarchical test-case format. Return a Markdown nested list that can be read directly or imported into a mind-map tool.

- Start with one root node containing the feature name. Include a Jira ID only when the user explicitly requests Jira traceability.
- Add a dedicated `需求缺口与候选用例` branch before the confirmed test-case branches when any requirement gaps exist. Place each gap-derived candidate case below its source gap with its baseline source and pending product decision.
- Group cases beneath meaningful module or risk branches. Do not create a branch for a behavior that is not supported by the supplied requirements.
- The only exception is a gap-derived candidate case that meets the `Gap-Derived Candidate Cases` contract; label it as pending confirmation rather than presenting it as a supported requirement behavior.
- Begin each test-case node with its test case ID, priority, test type, and title, for example: `TC_LOGIN_001 [严重 | 功能] 验证已激活用户使用有效凭证可以登录`.
- Under every test-case node, include the child nodes `前置条件`、`操作`、`测试数据`、`预期结果`。Keep each case atomic and preserve the same verifiable behavior as the table format.
- Preserve test case IDs, API names, event names, configuration keys, and exact documented messages. Preserve Jira metadata only when the user explicitly requests it. The hierarchy is a presentation change, not a loss of traceability.
- Use Simplified Chinese by default. Keep the tree concise enough to scan, but do not omit conditions or expected results needed to execute the case.

Use this structure:

```markdown
# [功能名称] - 思维导图测试用例

- [功能名称]
  - 需求缺口
    - [Gap 1]
  - [模块 A]
    - TC_<MODULE>_001 [严重 | 功能] 验证[行为]
      - 前置条件：[前置条件]
      - 操作：[按顺序列出步骤]
      - 测试数据：[具体数据]
      - 预期结果：[可观察结果]
```

Column guidance:

- `Test Case ID`: use `TC_<MODULE>_<NNN>`, for example `TC_LOGIN_001`.
- `Jira ID`: use an explicitly requested ticket ID; otherwise use `N/A`.
- `Module/Feature`: use the direct L2/L3 page, tab, module, or behavior context; do not use the L1 large requirement alone.
- `Test Case Title`: start with `验证`; gap-derived candidate titles start with `验证[候选]`.
- `Preconditions`: state required system/account/data state before execution.
- `Test Steps`: numbered steps using `1. 2. 3.` inside the cell.
- `Test Data`: concrete values, not generic placeholders like "valid input".
- `Expected Result`: observable result including exact message/status/state when documented. For a gap-derived candidate case, use `Candidate Expected Result (Industry Baseline, Pending Confirmation)` plus its named baseline source and pending product decision.
- `Priority`: `Critical`, `High`, `Medium`, or `Low`.
- `Test Type`: `Functional`, `Negative`, `Boundary`, `Integration`, `Security`, or `Performance`.

Priority logic:

- `Critical`: blocks core flow, causes data loss, bypasses security, or prevents release-critical behavior.
- `High`: validates major acceptance criteria or primary business flow.
- `Medium`: validates secondary rules, formatting, non-blocking validation, or alternate flows.
- `Low`: UI polish, copy, non-critical visual behavior, or low-impact checks.

## Guardrails

- Do not use an ambiguity in test data, acceptance detail, or configuration value as a reason to omit a behavior that is explicitly stated in the source. Preserve it as a conditional confirmed case and make the missing prerequisite visible.
- Do not stop source extraction at the first top-level requirement. Numbered child sections, tables, screenshots, permission trees, data-migration notes, and explicit regression statements must be inventoried and reconciled before delivery.
- Do not replace multiple source-stated capabilities with one generic "page exists", "mutual exclusion", or security candidate case. Keep direct traceability for each independent behavior.
- Do not write requirements disguised as test cases.
- If a requirement is ambiguous, flag it. Create a gap-derived candidate case only when it meets the `Gap-Derived Candidate Cases` contract; otherwise keep a conditional outcome as a question or residual risk, not a test case.
- Do not add security, performance, boundary, or integration cases as confirmed cases unless the source material gives enough basis. A candidate case in these categories requires a named applicable industry baseline and the required pending-confirmation label.
- Never label a gap-derived candidate result as `Expected Result`, `Requirement`, `Acceptance Criterion`, or `Pass` without its `Candidate Expected Result (Industry Baseline, Pending Confirmation)` qualifier.
- Do not let candidate coverage hide a missing confirmed acceptance criterion, satisfy a release gate, or replace clarification from the requirement owner.
- If the user asks for extra exploratory ideas beyond documented scope, separate them under `Exploratory Ideas` and clearly mark them as not requirement-traceable.
- Default to Simplified Chinese for test case output unless the user explicitly requests another language. Preserve field names where Jira/CSV compatibility requires it.

## Minimal Example

输入：

```text
AC1：已激活用户可使用已注册邮箱和正确密码登录。
AC2：密码错误时，显示“邮箱或密码错误”。
邮箱最大长度为 255 个字符。
```

输出：

| Test Case ID | Jira ID | Module/Feature | Test Case Title | Preconditions | Test Steps | Test Data | Expected Result | Priority | Test Type |
|---|---|---|---|---|---|---|---|---|---|
| TC_LOGIN_001 | N/A | 登录 | 验证已激活用户使用有效凭证可以登录 | 1. 用户账号已存在且状态为已激活。2. 用户位于登录页。 | 1. 输入已注册的邮箱。2. 输入正确密码。3. 点击登录。 | 邮箱：testuser@example.com；密码：Test@1234 | 用户认证成功并跳转至仪表盘。 | High | Functional |
| TC_LOGIN_002 | N/A | 登录 | 验证密码错误时展示配置的错误提示 | 1. 用户账号已存在且状态为已激活。2. 用户位于登录页。 | 1. 输入已注册的邮箱。2. 输入错误密码。3. 点击登录。 | 邮箱：testuser@example.com；密码：WrongPass!99 | 页面展示“邮箱或密码错误”，用户仍停留在登录页。 | High | Negative |
| TC_LOGIN_003 | N/A | 登录 | 验证邮箱字段限制最大长度 | 1. 用户位于登录页。 | 1. 输入长度超过 255 个字符的邮箱地址。2. 移出邮箱字段焦点或提交表单。 | 邮箱：256 个字符的邮箱值 | 系统阻止提交，或展示需求中定义的超出最大长度校验行为。 | Medium | Boundary |
