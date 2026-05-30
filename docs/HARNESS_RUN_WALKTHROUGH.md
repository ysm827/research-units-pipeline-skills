# Harness Run Walkthrough

This walkthrough ties `docs/HARNESS_SYSTEM_MAP.md` to one concrete repo-local
run. It is intentionally narrow: it demonstrates how a user goal becomes a
pipeline lock, unit ledger, doctor report, and run audit. It does not claim that
the semantic research work is complete.

The observed run was executed in this checkout with `uv run python ...` because
the local shell does not expose `python` directly. The examples below use
`python` to match the repo docs; prefix commands with `uv run` if your local
environment needs it.

## Demo Workspace Boundary

The demo workspace is:

```text
workspaces/harness-demo-research-brief/
```

Workspace outputs belong under `workspaces/<name>/` and are ignored by git. This
demo is a local run ledger, not a tracked fixture and not a replacement for
tests.

## 1. Kick Off A Goal

Command:

```bash
python scripts/pipeline.py kickoff \
  --topic "Demo research brief on retrieval augmented generation evaluation" \
  --pipeline research-brief \
  --workspace workspaces/harness-demo-research-brief \
  --overwrite \
  --overwrite-units
```

Observed output:

```text
Workspace ready: /Users/renjunbin/Documents/codebase/try/research-units-pipeline-skills/workspaces/harness-demo-research-brief
Next: run `python scripts/pipeline.py run --workspace <ws>` (it will pause if a HUMAN approval is required)
```

This creates the workspace ledger:

```text
PIPELINE.lock.md
GOAL.md
UNITS.csv
STATUS.md
CHECKPOINTS.md
DECISIONS.md
queries.md
papers/
outline/
output/
citations/
```

The lock file records the selected contract:

```text
pipeline: pipelines/research-brief.pipeline.md
units_template: templates/UNITS.research-brief.csv
locked_at: 2026-05-30
```

The goal file records the run intent:

```text
# Goal

Demo research brief on retrieval augmented generation evaluation
```

## 2. Diagnose The Workspace

Command:

```bash
python scripts/pipeline.py doctor --workspace workspaces/harness-demo-research-brief --write
```

Observed result:

```text
doctor-report.v1
verdict: PASS
current checkpoint: C0
unit status: TODO 11
next runnable: U001 Initialize workspace and copy templates
harness issues: none
```

The command writes:

```text
output/DOCTOR_REPORT.md
output/DOCTOR_REPORT.json
```

The JSON sidecar is the machine-readable handoff. In this run it used schema
`doctor-report.v1` and verdict `PASS`.

## 3. Audit The Run Ledger

Command:

```bash
python scripts/pipeline.py audit --workspace workspaces/harness-demo-research-brief --write
```

When scripting this walkthrough, append `|| true` if you want the shell to keep
going after an expected `ATTENTION` verdict. The audit command returns non-zero
when the run ledger is not complete.

Observed result:

```text
run-audit.v1
pipeline: research-brief
current checkpoint: C0
unit status: TODO 11
verdict: ATTENTION
```

The command writes:

```text
output/RUN_AUDIT.md
output/RUN_AUDIT.json
```

The audit found the initialized ledger but refused to treat it as a completed
run because two target artifacts were still missing:

```text
output/DELIVERABLE_SELFLOOP_TODO.md
output/CONTRACT_REPORT.md
```

That failure mode is useful. It proves that the harness can distinguish
"workspace initialized" from "workflow completed".

## Layer Mapping

| System layer | Demo evidence |
|---|---|
| User goal | `GOAL.md` stores the requested research brief topic |
| Capability choice | `research-brief` was selected explicitly at kickoff |
| Pipeline contract | `PIPELINE.lock.md` points to `pipelines/research-brief.pipeline.md` |
| Unit graph | `UNITS.csv` is copied from `templates/UNITS.research-brief.csv` |
| Workspace ledger | `STATUS.md`, `CHECKPOINTS.md`, `DECISIONS.md`, `papers/`, `outline/`, and `output/` exist under the workspace |
| Developer harness | `pipeline.py doctor` writes `DOCTOR_REPORT.md` and `DOCTOR_REPORT.json` |
| Run audit | `pipeline.py audit` writes `RUN_AUDIT.md` and `RUN_AUDIT.json` |
| Machine contract | JSON sidecars use `doctor-report.v1` and `run-audit.v1` |
| Governance boundary | The audit returns `ATTENTION` until target artifacts are produced |

## What This Does Not Prove

This walkthrough does not prove retrieval quality, paper selection quality,
draft quality, or completed semantic execution. It proves the current harness
loop:

```text
goal -> pipeline lock -> unit ledger -> workspace diagnosis -> run audit
```

The next deeper demo would run semantic units, inspect unit output manifests,
and compare `RUN_AUDIT.json` before and after target artifacts are produced:

```bash
python scripts/pipeline.py audit-diff \
  --before workspaces/harness-demo-research-brief/output/RUN_AUDIT.before.json \
  --after workspaces/harness-demo-research-brief/output/RUN_AUDIT.json \
  --write
```

That comparison writes `RUN_AUDIT_DIFF.md` and `RUN_AUDIT_DIFF.json` beside
the after payload.
