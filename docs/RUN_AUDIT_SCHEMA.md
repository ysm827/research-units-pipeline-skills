# Run Audit Schema

This document defines the current `run-audit.v1` JSON contract written by:

```bash
python scripts/pipeline.py audit --workspace workspaces/<name> --write
```

The human report is `output/RUN_AUDIT.md`. The machine-readable sidecar is
`output/RUN_AUDIT.json`.

## Ownership

- Producer: `tooling.harness.build_run_audit_payload`
- Writer: `tooling.harness.write_run_audit_json`
- Compatibility check: `tooling.harness.validate_run_audit_payload`
- Architecture decision: `docs/adr/0002-keep-run-audit-as-markdown-plus-json.md`

The schema is intentionally lightweight and repo-local. It is not a general
workflow standard and does not claim semantic artifact quality.

## Top-Level Fields

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Must be `run-audit.v1`. |
| `generated_at` | string | Local ISO-like timestamp for the audit payload. |
| `workspace` | string | Absolute workspace path used for the audit. |
| `repo` | string | Absolute repo root path used for the audit. |
| `pipeline_lock` | string | Compact summary from `PIPELINE.lock.md`, or empty when unavailable. |
| `pipeline` | string | Resolved pipeline name, or empty when the locked spec cannot be resolved. |
| `current_checkpoint` | string | Current checkpoint parsed from `STATUS.md`, or `unknown`. |
| `run_ledger_files` | object | Presence map for core workspace ledger files. |
| `unit_status` | object | Counts by unit status from `UNITS.csv`. |
| `target_artifacts` | list | Presence records for pipeline target artifacts. |
| `unit_output_manifests` | object | Summary and records from `output/unit_logs/*.manifest.json`. |
| `harness_issues` | list | Typed harness issues found during the audit. |
| `remediation_summary` | object | Counts by remediation category. |
| `recent_reports` | list | Compact previews of recent harness report artifacts. |
| `verdict` | string | `PASS` when there are no error-level harness issues; otherwise `ATTENTION`. |
| `exit_code` | integer | Command-style exit code: `0` for pass, `2` for attention. |

## Run Ledger Files

`run_ledger_files` is an object with boolean values for these keys:

- `PIPELINE.lock.md`
- `GOAL.md`
- `UNITS.csv`
- `STATUS.md`
- `CHECKPOINTS.md`
- `DECISIONS.md`

These files make a workspace inspectable without relying on chat history.

## Target Artifacts

Each `target_artifacts` item is an object:

| Field | Type | Meaning |
|---|---|---|
| `path` | string | Workspace-relative target artifact path. |
| `exists` | boolean | Whether the artifact exists at audit time. |

Missing target artifacts are also represented as `missing_target_artifact`
harness issues.

## Unit Output Manifests

`unit_output_manifests` is an object:

| Field | Type | Meaning |
|---|---|---|
| `count` | integer | Number of manifest files discovered. |
| `by_status` | object | Counts by manifest status. |
| `latest` | object | Compact summary of the last manifest after path sort, or empty. |
| `records` | list | Compact manifest summaries. |

Each manifest summary may contain:

- `path`
- `unit_id`
- `skill`
- `status`
- `exit_code`
- `generated_at`
- `outputs`

The `outputs` field is copied from the unit manifest summary and should be
treated as producer-owned metadata.

## Harness Issues

Each `harness_issues` item is an object:

| Field | Type | Meaning |
|---|---|---|
| `level` | string | Issue severity, usually `ERROR` or `WARN`. |
| `code` | string | Stable issue code such as `missing_units` or `missing_target_artifact`. |
| `message` | string | Human-readable issue detail. |
| `remediation_category` | string | Stable repair class. |
| `next_action` | string | Concrete repair hint. |

`remediation_summary` counts the issue list by `remediation_category`.

## Recent Reports

Each `recent_reports` item is an object:

| Field | Type | Meaning |
|---|---|---|
| `path` | string | Workspace-relative report path. |
| `preview` | string | First non-empty content line. |

Current report sources are `output/RUN_ERRORS.md`, `output/QUALITY_GATE.md`,
and `output/CONTRACT_REPORT.md`.

## Compatibility Rule

Future tooling should consume `output/RUN_AUDIT.json` and check it with
`validate_run_audit_payload` before relying on the payload.
To compare two audits, use `python scripts/pipeline.py audit-diff` and consume
`RUN_AUDIT_DIFF.json` through `validate_run_audit_diff_payload`; do not infer
regression state by scraping two Markdown reports.

Breaking changes to `run-audit.v1` should be handled by one of these paths:

- preserve backward compatibility in readers
- introduce a new schema version
- update ADR 0002 and this reference with a migration note

Do not scrape `RUN_AUDIT.md` for machine behavior unless the JSON sidecar is
unavailable and the tool explicitly accepts that weaker contract.
