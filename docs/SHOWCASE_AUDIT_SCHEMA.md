# Showcase Audit Schema

This document defines the current `harness-showcase-audit.v1` JSON contract
written by:

```bash
python scripts/showcase_audit.py --format json
```

The CI gate uses the same producer in strict mode:

```bash
python scripts/showcase_audit.py --strict
```

## Ownership

- Producer: `scripts.showcase_audit.build_showcase_audit`
- Text/JSON renderer: `scripts.showcase_audit.render_markdown` and
  `scripts.showcase_audit.render_json`
- Compatibility check:
  `scripts.showcase_audit.validate_showcase_audit_payload`
- CI gate: `python scripts/showcase_audit.py --strict`
- Architecture decision:
  `docs/adr/0006-keep-showcase-audit-as-repo-local-json-contract.md`

The schema describes portable showcase fixture health. It does not rerun live
retrieval, compile LaTeX, execute units, or judge semantic research quality.

## Top-Level Fields

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Must be `harness-showcase-audit.v1`. |
| `repo` | string | Absolute repository path inspected by the audit. |
| `verdict` | string | `PASS` when all checks pass; otherwise `ATTENTION`. |
| `showcase_doc` | string | Repo-relative showcase document path. |
| `checks` | list | Ordered check records. |
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
- `research_brief_fixture`
- `source_tutorial_fixture`

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
