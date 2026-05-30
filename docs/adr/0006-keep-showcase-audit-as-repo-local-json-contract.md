# ADR 0006: Keep Showcase Audit As Repo-Local JSON Contract

- Status: accepted
- Date: 2026-05-30

## Context

`scripts/showcase_audit.py` now checks the portable examples under `example/`
and is run by `.github/workflows/harness.yml`. That makes the showcase more
than prose: it is a protected exhibit gate for deliverable-first fixture
health.

The command already emits Markdown for humans and JSON for tools through
`python scripts/showcase_audit.py --format json`. Once a command is CI-backed
and machine-readable, future tooling should not infer its shape from examples
or scrape the Markdown report.

## Decision

Keep `harness-showcase-audit.v1` as a small repo-local JSON contract before
adding formal JSON Schema files or an external dashboard.

The contract is documented in `docs/SHOWCASE_AUDIT_SCHEMA.md` and checked by
`scripts.showcase_audit.validate_showcase_audit_payload`. The CI gate remains:

```bash
python scripts/showcase_audit.py --strict
```

The schema covers repository path, verdict, showcase document path, check
records, and the boundary note. It does not claim live workflow execution,
retrieval quality, LaTeX compilation, or semantic benchmark quality.

## Consequences

Future agents and lightweight tools can consume showcase audit JSON without
reverse-engineering Markdown. The exhibit gate stays file-first and cheap to
run, which matches the current harness architecture.

If the showcase grows into a benchmark dashboard or multi-run exhibit system,
that future work should build on this JSON contract or introduce a new schema
version. It should not silently change `harness-showcase-audit.v1`.

## Related Files

- `scripts/showcase_audit.py`
- `docs/SHOWCASE_AUDIT_SCHEMA.md`
- `docs/HARNESS_SHOWCASE.md`
- `docs/HARNESS_READINESS.md`
- `docs/HARNESS_ROADMAP.md`
- `tooling/harness_contracts.py`
- `.github/workflows/harness.yml`
