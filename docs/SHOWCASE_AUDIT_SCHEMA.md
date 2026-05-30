# Showcase Audit Schema

This document defines the current `harness-showcase-audit.v1` JSON contract
written by:

```bash
python scripts/showcase_audit.py --format json
```

The local showcase check uses the same producer in strict mode:

```bash
python scripts/showcase_audit.py --strict
```

## Ownership

- Producer: `scripts.showcase_audit.build_showcase_audit`
- Text/JSON renderer: `scripts.showcase_audit.render_markdown` and
  `scripts.showcase_audit.render_json`
- Compatibility check:
  `scripts.showcase_audit.validate_showcase_audit_payload`
- Local blocking check: `python scripts/showcase_audit.py --strict`
- Architecture decision:
  `docs/adr/0006-keep-showcase-audit-as-repo-local-json-contract.md`

The schema describes portable showcase fixture health. It does not rerun live
retrieval, compile LaTeX, execute units, or judge semantic research quality.
The producer first checks that fixture group definitions, required markers,
deliverables, and tracked fixture paths remain internally synchronized.
For tracked `ARTIFACT_PACK_EXCERPT.tsv` files, the producer validates the
canonical `category	path	exists	role` header, row width, non-empty category,
path, and role cells, boolean `true` / `false` values for `exists`, and row
consistency with the paired Markdown excerpt table. It also checks tracked
fixture files for absolute local paths such as `/Users/...`, `/home/...`,
`/tmp/...`, Windows user paths, and `file://...` URIs so portable examples do
not accidentally depend on a maintainer's private workspace.

## Top-Level Fields

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Must be `harness-showcase-audit.v1`. |
| `repo` | string | Absolute repository path inspected by the audit. |
| `verdict` | string | `PASS` when all checks pass; otherwise `ATTENTION`. |
| `showcase_doc` | string | Repo-relative showcase document path. |
| `checks` | list | Ordered check records. |
| `scorecard` | list | Optional ordered fixture coverage records emitted by the current producer. |
| `note` | string | Boundary note describing what the audit does not prove. |

## Check Records

Each `checks` item is an object:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable check id such as `showcase_doc` or `source_tutorial_fixture`. |
| `status` | string | `PASS` or `WARN`. |
| `evidence` | string | Human-readable evidence for the check. |
| `next_action` | string | Suggested maintenance action. |

Current check ids:

- `showcase_doc`
- `lineage_assets`
- `pipeline_protocols`
- `fixture_contracts`
- `research_brief_fixture`
- `source_tutorial_fixture`

## Scorecard Records

The current producer emits `scorecard` as an additive field. Consumers that do
not need fixture coverage can ignore it, but consumers that do read it should
validate each item before using the counts.

Each `scorecard` item is an object:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Fixture id matching a fixture check id. |
| `label` | string | Reader-facing fixture label. |
| `status` | string | `PASS` when all tracked files and required markers are present; otherwise `WARN`. |
| `tracked_files` | integer | Number of fixture files expected by the showcase contract. |
| `present_files` | integer | Number of expected fixture files currently present. |
| `required_markers` | integer | Number of required evidence markers checked inside fixture files. |
| `present_markers` | integer | Number of required markers currently present. |
| `evidence_surface` | string | Compact human-readable coverage summary. |

The scorecard is deliberately conservative. It is a coverage summary for the
portable exhibit, not a semantic benchmark, reader-quality score, or proof that
live retrieval and compilation still work.

## Compatibility Rule

Future tooling should consume the JSON output from
`python scripts/showcase_audit.py --format json` and check it with
`validate_showcase_audit_payload` before relying on the payload.

Breaking changes to `harness-showcase-audit.v1` should be handled by one of
these paths:

- preserve backward compatibility in readers
- introduce a new schema version
- update this reference, the schema metadata in
  `tooling/harness_contracts.py`, and ADR 0006 or a superseding ADR

Do not scrape the Markdown showcase audit report for machine behavior unless
the JSON output is unavailable and the tool explicitly accepts that weaker
contract.
