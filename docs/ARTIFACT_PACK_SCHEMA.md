# Artifact Pack Schema

This document defines the current `artifact-pack.v1` JSON contract written by:

```bash
python scripts/pipeline.py pack --workspace workspaces/<name> --write
```

The human report is `output/ARTIFACT_PACK.md`. The machine-readable sidecar is
`output/ARTIFACT_PACK.json`.

For reader-facing fixtures or handoff notes, the same command can also write a
portable excerpt:

```bash
python scripts/pipeline.py pack --workspace workspaces/<name> --write-excerpt
```

This creates `output/ARTIFACT_PACK_EXCERPT.md` and
`output/ARTIFACT_PACK_EXCERPT.tsv` with workspace-relative paths only.

## Ownership

- Producer: `tooling.harness.build_artifact_pack_payload`
- Writer: `tooling.harness.write_artifact_pack_json`
- Excerpt writers: `tooling.harness.write_artifact_pack_excerpt_markdown` and
  `tooling.harness.write_artifact_pack_excerpt_tsv`
- Compatibility check: `tooling.harness.validate_artifact_pack_payload`
- Architecture decision: `docs/adr/0008-keep-artifact-pack-as-manifest-before-archive.md`

The schema is intentionally a manifest, not an archive. It records what a
workspace currently contains, where reviewable evidence lives, and whether the
source harness reports still require attention. It does not copy files,
compress outputs, publish a bundle, or judge semantic quality.

## Top-Level Fields

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Must be `artifact-pack.v1`. |
| `generated_at` | string | Local ISO-like timestamp for the manifest. |
| `workspace` | string | Absolute workspace path used for the manifest. |
| `repo` | string | Absolute repo root path used for the manifest. |
| `pipeline` | string | Resolved pipeline name, or empty when the locked spec cannot be resolved. |
| `artifact_interface_standard` | string | Current artifact interface standard reference. |
| `source_reports` | object | Compact verdicts for doctor, run-audit, improvement-report evidence, and run-state handoff when available. |
| `artifacts` | list | Indexed workspace artifacts grouped by review role. |
| `summary` | object | Present/missing counts for the whole pack and each category. |
| `verdict` | string | `PASS` when source reports pass; otherwise `ATTENTION`. |
| `exit_code` | integer | Command-style exit code: `0` for pass, `2` for attention. |

## Source Reports

`source_reports` is an object keyed by report name. Current keys are:

- `doctor`
- `run_audit`
- `improvement_report`

Each source report record contains:

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Source payload schema name. |
| `verdict` | string | Source report verdict. |
| `exit_code` | integer | Source report exit code. |

The `run_audit` source report may also contain `run_state`, copied from
`run-audit.v1`. This lets artifact-pack consumers route on the run phase and
artifact coverage without opening `output/RUN_AUDIT.json` first. The copied
state keeps the same conservative meaning as the run audit: it summarizes
harness evidence and does not judge semantic quality.

## Artifact Records

Each `artifacts` item is an object with these stable fields:

| Field | Type | Meaning |
|---|---|---|
| `category` | string | Review role: `target_artifact`, `unit_output`, `run_ledger`, `harness_report`, or `unit_manifest`. |
| `path` | string | Workspace-relative artifact path. |
| `exists` | boolean | Whether the artifact exists at manifest time. |

When a path exists, the record may also include:

| Field | Type | Meaning |
|---|---|---|
| `type` | string | `file` or `directory`. |
| `size` | integer | File size in bytes. |
| `sha256` | string | File digest for stable comparison. |
| `file_count` | integer | Number of files inside a directory artifact. |

## Summary

`summary` contains:

| Field | Type | Meaning |
|---|---|---|
| `total` | integer | Number of indexed artifact records. |
| `present` | integer | Indexed artifacts that exist. |
| `missing` | integer | Indexed artifacts that do not exist. |
| `by_category` | object | Per-category `{total, present, missing}` counters. |

## Compatibility Rule

Future tooling should consume `output/ARTIFACT_PACK.json` and check it with
`validate_artifact_pack_payload` before relying on the fields.

Breaking changes to `artifact-pack.v1` should be handled by one of these paths:

- preserve backward compatibility in readers
- introduce a new schema version
- update ADR 0008 and this reference with a migration note

Do not treat the artifact pack as a packaging runtime yet. It is the
deliverable-first manifest that lets a reviewer or future model start from
final outputs, then trace backward through run ledgers, harness reports, and
unit manifests.

The excerpt files are a derived presentation surface, not a new schema. They
exist to reduce manual drift in tracked fixtures and handoff notes. Consumers
that need compatibility guarantees should read `output/ARTIFACT_PACK.json`.
