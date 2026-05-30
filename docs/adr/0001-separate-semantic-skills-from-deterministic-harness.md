# ADR 0001: Separate Semantic Skills From The Deterministic Harness

- Status: accepted
- Date: 2026-05-28

## Context

The repository contains two kinds of work:

- semantic research work, such as planning a survey, writing evidence packs,
  judging citations, or shaping tutorial modules
- deterministic support work, such as initializing a workspace, validating
  pipeline contracts, executing skill scripts, diagnosing a stuck run, and
  recording output manifests

Before the harness layer was named explicitly, these responsibilities were
visible but not fully narrated as an architecture. The repo now includes
`tooling/harness.py`, `pipeline.py doctor`, unit output manifests, stale
`DOING` recovery, `pyproject.toml`, harness tests, and local checks. That makes the
split concrete enough to record as an architectural decision.

## Decision

Keep semantic work in skills and repeatable orchestration/checking in the
deterministic harness.

Skills should own:

- domain judgment
- reader-facing policy
- input/output expectations
- acceptance criteria
- guardrails and anti-patterns
- selective reference loading

The harness should own:

- workspace initialization and pipeline locking
- unit dependency/status mechanics
- scripted unit execution
- run logs and output manifests
- stale-state recovery
- workspace diagnosis
- contract validation
- generated graph freshness checks
- local smoke and validation checks

## Consequences

This keeps the project usable by both humans and agents. A maintainer can inspect
a skill to understand the semantic job, and inspect the harness to understand
repeatable execution behavior.

It also creates a clean upgrade path. When a failure is judgment-heavy, improve
the skill, references, or pipeline contract. When a failure is repeatable and
mechanical, improve validation, doctor output, recovery behavior, tests, or
manifests.

The tradeoff is that every new feature needs routing discipline. If a script
starts embedding hidden domain defaults, it belongs back in a skill reference or
asset. If a skill repeats mechanical validation language, it may belong in the
harness.

## Related Files

- `SKILLS_STANDARD.md`
- `.codex/skills/`
- `pipelines/`
- `templates/UNITS.*.csv`
- `tooling/harness.py`
- `tooling/executor.py`
- `scripts/pipeline.py`
- `scripts/validate_repo.py`
