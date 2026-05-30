# Improvement Report Schema

This document defines the current `improvement-report.v1` JSON contract written
by:

```bash
python scripts/pipeline.py improve --workspace workspaces/<name> --write
```

The human report is `output/IMPROVEMENT_REPORT.md`. The machine-readable
sidecar is `output/IMPROVEMENT_REPORT.json`.

## Ownership

- Producer: `tooling.harness.build_improvement_payload`
- Writer: `tooling.harness.write_improvement_json`
- Compatibility check: `tooling.harness.validate_improvement_payload`
- Architecture decision: `docs/adr/0007-keep-improvement-report-as-a-local-repair-map.md`

The schema is intentionally lightweight and repo-local. It does not claim to
repair work automatically or judge semantic quality. It maps existing doctor
and run-audit evidence to likely upstream repair surfaces.

## Top-Level Fields

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Must be `improvement-report.v1`. |
| `generated_at` | string | Local ISO-like timestamp for the improvement payload. |
| `workspace` | string | Absolute workspace path used for the report. |
| `repo` | string | Absolute repo root path used for the report. |
| `pipeline` | string | Resolved pipeline name, or empty when the locked spec cannot be resolved. |
| `artifact_interface_standard` | string | Current artifact interface standard reference. |
| `source_reports` | object | Compact verdicts for doctor and run-audit evidence. |
| `suggestions` | list | Upstream repair suggestions derived from harness issues. |
| `verdict` | string | `PASS` when no repair suggestions were generated; otherwise `ATTENTION`. |
| `exit_code` | integer | Command-style exit code: `0` for pass, `2` for attention. |

## Source Reports

`source_reports` is an object keyed by report name. Current keys are:

- `doctor`
- `run_audit`

Each source report record contains:

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Source payload schema name. |
| `verdict` | string | Source report verdict. |
| `exit_code` | integer | Source report exit code. |

## Suggestions

Each `suggestions` item is an object:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable suggestion id within the report, such as `S001`. |
| `source_report` | string | Source evidence surface, currently `doctor` or `run_audit`. |
| `observed_problem` | string | Human-readable issue copied from the source evidence. |
| `evidence` | string | Compact issue severity and code. |
| `upstream_interface` | string | Artifact, ledger, checkpoint, dependency, or target-artifact interface likely at fault. |
| `repair_surface` | string | Local surface to change, usually a remediation category. |
| `recommended_action` | string | Concrete next repair action from the source issue. |
| `validation` | string | Local command that should be rerun after repair. |

## Compatibility Rule

Future tooling should consume `output/IMPROVEMENT_REPORT.json` and check it
with `validate_improvement_payload` before relying on the fields.

Breaking changes to `improvement-report.v1` should be handled by one of these
paths:

- preserve backward compatibility in readers
- introduce a new schema version
- update ADR 0007 and this reference with a migration note

Do not treat the improvement report as an autonomous repair planner. It is a
file-first repair map: source evidence -> upstream interface -> local repair
surface -> validation command.
