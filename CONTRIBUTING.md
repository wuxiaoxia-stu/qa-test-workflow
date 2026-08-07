# Contributing

## Scope

Keep pull requests focused. Explain the user-visible change, list affected workflow modes, and avoid unrelated resource moves or formatting rewrites.

When a change affects QA guidance, preserve the package's evidence classes:

- Confirmed requirements remain distinct from conditional cases blocked by missing data.
- Gap-derived candidates remain labelled `Pending Confirmation` and cannot satisfy an acceptance or release gate.
- Review findings retain evidence, severity, business impact, recommended action, and disposition.

## Tests and Evaluations

Update `tests/` for structural or routing changes. Update or add an `evals/cases/*.yaml` scenario when the generated QA behavior changes.

Run the following commands from the repository root before opening a pull request:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python -m compileall -q scripts
```

Do not commit generated `.skill` archives, Python caches, local environment files, customer data, access tokens, or production requirement artifacts.

## Pull Requests

Describe the source evidence and expected behavior for each workflow change. Include the verification output and identify any residual risk or intentionally unresolved product decision.
