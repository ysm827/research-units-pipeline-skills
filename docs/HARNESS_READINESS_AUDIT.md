# Harness Readiness Audit

This document defines the lightweight readiness-audit interface for the
long-running harness upgrade. It does not mark the goal complete. It checks
whether the evidence surfaces needed for a final closure audit are present and
discoverable.

## Command

```bash
python scripts/readiness_audit.py --progress workspaces/harness-upgrade/GOAL_STATUS.md
```

Use `--format json` when another tool needs to consume the result. Use
`--strict` when a missing evidence surface should return a non-zero exit code.

## What It Checks

The audit reports `harness-readiness-audit.v1` and checks:

- progress ledger existence, active goal state, and iteration count
- required harness docs and README links
- ADR set and ADR index presence
- pipeline taxonomy coverage for the current eight workflows
- executable pipeline contracts and unit templates
- harness CI gates listed in `HARNESS_CI_GATES`: WARN-level skill audit and
  portable showcase audit
- core validation, audit, pipeline, graph, readiness, showcase, and test
  surfaces

The contract lists used by this audit live in `tooling/harness_contracts.py`,
which is shared with `scripts/validate_repo.py` so README/docs/CI evidence
surfaces do not drift across two scripts. The same shared contract module also
defines the pattern-register metadata and schema reference docs that strict
repo validation protects.

## What It Does Not Check

The readiness audit does not run the final verification commands. It does not
run tests, strict repo validation, skill audit, compile checks, or workspace
doctor/audit commands. Those remain in `docs/HARNESS_READINESS.md` as the final
closure gate.

This split is intentional: the readiness audit is a fast evidence-surface check
for resumed work, while the final closure gate is the stronger proof step.

## Interpretation

- `PASS` means every evidence surface checked by the script exists.
- `ATTENTION` means at least one evidence surface is missing or stale.
- A passing readiness audit is not completion proof by itself.

The final closure decision still requires reading the current worktree,
running the commands named in `docs/HARNESS_READINESS.md`, and verifying every
explicit goal requirement against current evidence.
