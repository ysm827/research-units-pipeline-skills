# Doctor Report Schema

This document defines the current `doctor-report.v1` JSON contract written by:

```bash
python scripts/pipeline.py doctor --workspace workspaces/<name> --write
```

The human report is `output/DOCTOR_REPORT.md`. The machine-readable sidecar is
`output/DOCTOR_REPORT.json`.

## Ownership

- Producer: `tooling.harness.build_doctor_payload`
- Markdown renderer: `tooling.harness.render_doctor_report`
- JSON writer: `tooling.harness.write_doctor_json`
- Compatibility check: `tooling.harness.validate_doctor_payload`
- Architecture decision: `docs/adr/0003-keep-doctor-report-as-markdown-plus-json.md`

The schema describes workspace diagnosis state. It does not mutate a workspace
and does not claim that outputs are semantically correct.

## Top-Level Fields

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Must be `doctor-report.v1`. |
| `generated_at` | string | Local ISO-like timestamp for the diagnosis payload. |
| `workspace` | string | Absolute workspace path used for diagnosis. |
| `repo` | string | Absolute repo root path used for diagnosis. |
| `pipeline_lock` | string | Compact summary from `PIPELINE.lock.md`, or empty when unavailable. |
| `current_checkpoint` | string | Current checkpoint parsed from `STATUS.md`, or `unknown`. |
| `units_present` | boolean | Whether `UNITS.csv` exists. |
| `unit_status` | object | Counts by unit status from `UNITS.csv`; empty when units are missing. |
| `next_runnable` | object | Compact next-runnable unit record, or empty when no unit can run. |
| `harness_issues` | list | Typed workspace issues found during diagnosis. |
| `remediation_summary` | object | Counts by remediation category. |
| `recent_reports` | list | Compact previews of recent harness report artifacts. |
| `verdict` | string | `PASS` when there are no error-level harness issues; otherwise `ATTENTION`. |
| `exit_code` | integer | Command-style exit code: `0` for pass, `2` for attention. |

## Next Runnable

`next_runnable` is either empty or contains:

| Field | Type | Meaning |
|---|---|---|
| `unit_id` | string | Unit id from `UNITS.csv`. |
| `title` | string | Unit title, or `(untitled)`. |
| `skill` | string | Skill name, or `(no skill)`. |

## Harness Issues

Each `harness_issues` item is an object:

| Field | Type | Meaning |
|---|---|---|
| `level` | string | Issue severity, usually `ERROR` or `WARN`. |
| `code` | string | Stable issue code such as `missing_units` or `missing_done_output`. |
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

Future recovery or repair tooling should consume `output/DOCTOR_REPORT.json`
and check it with `validate_doctor_payload` before relying on the payload.

Breaking changes to `doctor-report.v1` should be handled by one of these paths:

- preserve backward compatibility in readers
- introduce a new schema version
- update ADR 0003 and this reference with a migration note

Do not scrape `DOCTOR_REPORT.md` for machine behavior unless the JSON sidecar
is unavailable and the tool explicitly accepts that weaker contract.
