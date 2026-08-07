# QA Test Workflow Open-Source Release Design

## Goal

Make `qa-test-workflow` understandable, installable, and safely reusable by external contributors without changing its three-mode QA workflow or moving bundled runtime resources.

## Scope

- Add a root README with installation, usage, modes, repository layout, and local verification instructions.
- License the repository under MIT.
- Add contribution and security-reporting guidance appropriate for a prompt-and-script skill repository.
- Extend `.gitignore` only for generated archives, test caches, and local environment files.
- Keep `SKILL.md`, `references/`, `scripts/`, `templates/`, `examples/`, `evals/`, and `tests/` in their existing locations because the skill resolves these relative paths.

## Non-Goals

- Do not add CI, issue templates, release automation, or a changelog in this release.
- Do not rename, relocate, or rewrite the existing skill behavior.
- Do not package generated `.skill` archives into Git.

## File Responsibilities

| File | Responsibility |
| --- | --- |
| `README.md` | Public entry point: purpose, installation, modes, layout, and verification. |
| `LICENSE` | MIT license terms. |
| `CONTRIBUTING.md` | Small-scope change, test, and pull-request expectations. |
| `SECURITY.md` | Private-channel guidance for sensitive reports; no public issue disclosure before a fix is available. |
| `.gitignore` | Excludes regenerated artifacts and local-only files. |

## Validation

1. Run package tests with the bundled Python runtime.
2. Compile all bundled scripts to catch syntax errors.
3. Inspect the tracked file set and `git diff --check` for accidental artifacts and whitespace errors.
4. Commit the open-source documentation separately from behavioral changes, then push only after explicit approval.
