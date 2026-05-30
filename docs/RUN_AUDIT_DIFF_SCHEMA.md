# Run Audit Diff Schema

This document defines the current `run-audit-diff.v1` JSON contract written by:

```bash
python scripts/pipeline.py audit-diff \
  --before workspaces/<name>/output/RUN_AUDIT.before.json \
  --after workspaces/<name>/output/RUN_AUDIT.json \
  --write
```

The human report is `RUN_AUDIT_DIFF.md`. The machine-readable sidecar is
`output/RUN_AUDIT_DIFF.json` when the `--after` payload is the usual
`output/RUN_AUDIT.json`. When `--write` is used, both files are written beside
the `--after` payload.

## Ownership

- Producer: `tooling.harness.build_run_audit_diff_payload`
- Writer: `tooling.harness.write_run_audit_diff_json`
- Compatibility check: `tooling.harness.validate_run_audit_diff_payload`
- Architecture decision: `docs/adr/0005-keep-run-audit-diff-as-json-backed-comparison.md`

The schema is intentionally lightweight and repo-local. It compares two
already-valid `run-audit.v1` payloads. It does not run units, mutate a
workspace, or judge semantic research quality.

## Top-Level Fields

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Must be `run-audit-diff.v1`. |
| `generated_at` | string | Local ISO-like timestamp for the diff payload. |
| `before_path` | string | Absolute path to the earlier `RUN_AUDIT.json`. |
| `after_path` | string | Absolute path to the later `RUN_AUDIT.json`. |
| `before_schema` | string | Schema value from the earlier payload. |
| `after_schema` | string | Schema value from the later payload. |
| `before_workspace` | string | Workspace value from the earlier payload. |
| `after_workspace` | string | Workspace value from the later payload. |
| `before_pipeline` | string | Pipeline value from the earlier payload. |
| `after_pipeline` | string | Pipeline value from the later payload. |
| `before_verdict` | string | Verdict from the earlier payload. |
| `after_verdict` | string | Verdict from the later payload. |
| `unit_status_delta` | object | After-minus-before unit status counts. |
| `target_artifact_changes` | list | Target artifact presence changes. |
| `manifest_counts` | object | Before, after, and delta for unit output manifests. |
| `harness_issue_counts` | object | Before, after, and delta for harness issues. |
| `comparison_issues` | list | Diff-level issues such as pipeline mismatch or newly missing target artifacts. |
| `verdict` | string | `PASS` when the after audit passes and the diff finds no comparison issues; otherwise `ATTENTION`. |
| `exit_code` | integer | Command-style exit code: `0` for pass, `2` for attention. |

## Unit Status Delta

`unit_status_delta` is an object whose keys are status names and whose values
are integer deltas. A positive value means the after payload has more units in
that status. A negative value means it has fewer.

Example:

```json
{
  "DONE": 1,
  "TODO": -1
}
```

## Target Artifact Changes

Each `target_artifact_changes` item is an object:

| Field | Type | Meaning |
|---|---|---|
| `path` | string | Workspace-relative target artifact path. |
| `before_exists` | boolean or null | Whether the artifact existed in the before payload; null means absent from the before contract. |
| `after_exists` | boolean or null | Whether the artifact exists in the after payload; null means absent from the after contract. |
| `change` | string | Change class such as `became_present`, `became_missing`, `added_present`, or `removed_present`. |

Unchanged artifacts are omitted from the diff payload to keep the report
compact.

## Count Deltas

`manifest_counts` and `harness_issue_counts` share the same shape:

| Field | Type | Meaning |
|---|---|---|
| `before` | integer | Count in the earlier audit. |
| `after` | integer | Count in the later audit. |
| `delta` | integer | `after - before`. |

## Compatibility Rule

Future tooling should call `validate_run_audit_payload` for each source
`RUN_AUDIT.json`, then call `validate_run_audit_diff_payload` before relying on
the diff payload.

Breaking changes to `run-audit-diff.v1` should be handled by one of these
paths:

- preserve backward compatibility in readers
- introduce a new schema version
- update ADR 0005 and this reference with a migration note

Do not infer regression state by scraping `RUN_AUDIT_DIFF.md` unless the JSON
sidecar is unavailable and the tool explicitly accepts that weaker contract.
