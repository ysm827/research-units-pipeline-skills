# Skill Audit Schema

This document defines the current `skill-audit-report.v1` JSON contract
written by:

```bash
python scripts/audit_skills.py --format json
```

The same producer can emit a focused report with:

```bash
python scripts/audit_skills.py --format json --review-category template_placeholder --limit 20
```

## Ownership

- Producer: `scripts.audit_skills.build_report_payload`
- Text/JSON renderer: `scripts.audit_skills.render_report`
- Compatibility check: `scripts.audit_skills.validate_skill_audit_payload`
- Local blocking check: `python scripts/audit_skills.py --fail-on WARN`
- Architecture decision:
  `docs/adr/0004-keep-skill-audit-as-repo-local-json-before-sarif.md`

The schema describes static skill hygiene findings. It does not judge semantic
output quality and does not mutate skill files.

This contract borrows the useful discipline of static-analysis interchange
formats such as SARIF: stable result records, machine-readable locations, rule
ids, severities, and summary metadata. It is not a SARIF document. SARIF export
is deferred until a concrete external consumer, such as GitHub code scanning,
needs it.

## Top-Level Fields

| Field | Type | Meaning |
|---|---|---|
| `schema` | string | Must be `skill-audit-report.v1`. |
| `summary` | object | Scan counts, grouped counts, and filter metadata. |
| `findings` | list | Displayed finding records after optional filtering and limiting. |

## Summary

`summary` is an object:

| Field | Type | Meaning |
|---|---|---|
| `skills_scanned` | integer | Number of skill directories scanned. |
| `files_scanned` | integer | Number of text files scanned. |
| `findings` | integer | Number of findings after review-category filtering. |
| `displayed_findings` | integer | Number of finding records included in `findings`. |
| `by_severity` | object | Counts by `ERROR`, `WARN`, or `INFO`. |
| `by_rule` | object | Counts by audit rule id. |
| `by_review_category` | object | Counts by review category. |
| `filters` | object | Active filters such as `review_category`, `limit`, or `summary_only`. |

`displayed_findings` can be smaller than `findings` when `--limit` or
`--summary-only` is used.

## Finding Records

Each `findings` item is an object:

| Field | Type | Meaning |
|---|---|---|
| `severity` | string | `ERROR`, `WARN`, or `INFO`. |
| `rule_id` | string | Stable audit rule id. |
| `skill` | string | Skill package name. |
| `path` | string | Repo-relative file path. |
| `line` | integer | 1-based line number. |
| `message` | string | Human-readable finding. |
| `excerpt` | string | Compact source-line excerpt. |
| `review_category` | string | Triage class such as `template_placeholder`. |
| `next_action` | string | Suggested maintenance action. |

## Filters

Current filter metadata can include:

| Field | Type | Meaning |
|---|---|---|
| `review_category` | list | Review categories requested through `--review-category`. |
| `limit` | integer | Maximum displayed finding records requested through `--limit`. |
| `summary_only` | boolean | Whether finding details were intentionally omitted. |

Filtering is applied before `--fail-on`. The local blocking check should keep
using the unfiltered WARN-level command so blocking skill regressions remain
visible.

## Compatibility Rule

Future tooling should consume the JSON output from
`python scripts/audit_skills.py --format json` and check it with
`validate_skill_audit_payload` before relying on the payload.

Breaking changes to `skill-audit-report.v1` should be handled by one of these
paths:

- preserve backward compatibility in readers
- introduce a new schema version
- update this reference, the schema metadata in
  `tooling/harness_contracts.py`, and ADR 0004 or a superseding ADR

Do not scrape the text skill audit report for machine behavior unless the JSON
output is unavailable and the tool explicitly accepts that weaker contract.
