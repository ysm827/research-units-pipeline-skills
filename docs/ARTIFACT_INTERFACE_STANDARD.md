# Artifact Interface Standard

This document defines the repo standard for intermediate artifacts. It turns
the self-improvement idea in `docs/HARNESS_IMPROVEMENT_LOOP.md` into a concrete
interface rule: an artifact is not a leftover file if a later person, model,
script, validator, or run can depend on it.

The standard is intentionally grounded in current repo surfaces:
`pipelines/*.pipeline.md`, `templates/UNITS.*.csv`, `workspaces/<name>/`,
`DOCTOR_REPORT.md/json`, `RUN_AUDIT.md/json`, `RUN_AUDIT_DIFF.md/json`, unit
manifests, schema docs, and showcase fixtures.

`scripts/validate_repo.py` protects this document as a repo-level contract. It
checks the required sections, interface fields, format vocabulary, and current
repo mapping rows so the standard does not silently drift into prose-only
guidance.

## Interface Thesis

The harness improves only when intermediate state is readable, traceable,
locatable, and repair-oriented.

Readable means two different things:

- Human-readable: a compact report that helps a user, reviewer, or maintainer
  understand context, evidence, status, and next action.
- Machine-readable: a stable CSV, TSV, YAML, or versioned JSON surface that a
  model, script, validator, or future comparison tool can consume without
  scraping prose.

Every durable artifact should declare which side it serves. Important
artifacts may serve both sides through paired Markdown and structured sidecars.

## Required Interface Fields

When adding or changing a durable harness artifact, define these fields in the
pipeline, schema doc, README section, or skill contract that owns it:

| Field | Meaning |
|---|---|
| `artifact_path` | Where the artifact lives relative to a workspace or repo root |
| `producer` | Skill, command, script, or human checkpoint that writes it |
| `consumer` | Later unit, reviewer, validator, model, script, or docs page that reads it |
| `format` | Markdown, CSV, TSV, YAML, JSON, PDF, TeX, SVG, or directory |
| `human_view` | What a person should understand from opening it |
| `machine_view` | What a tool or future agent can read deterministically |
| `trace_keys` | Stable ids, paths, hashes, unit ids, schema names, or checkpoint names |
| `repair_surface` | Skill, pipeline, unit template, schema, validator, ADR, or glossary term to change when it fails |
| `validation` | Test, local check, quality gate, doctor issue, run audit, audit diff, or manual checkpoint |
| `visibility` | Public/tracked, workspace-local, ignored/private, or curated fixture |

Not every artifact needs a new schema file. It does need enough declared shape
that a future maintainer can tell whether it is a user deliverable, a run
ledger entry, a diagnostic report, or a reusable learning asset.

## Format Selection

| Need | Preferred format | Current repo examples | Notes |
|---|---|---|---|
| Reader-facing explanation | Markdown | `STATUS.md`, `CHECKPOINTS.md`, `DOCTOR_REPORT.md`, `RUN_AUDIT.md` | Keep compact, status-oriented, and easy to quote in handoff |
| Tabular unit or evidence state | CSV or TSV | `UNITS.csv`, `templates/UNITS.*.csv`, `papers/core_set.csv` | Prefer CSV/TSV when rows and columns are the product |
| Structured protocol or outline | YAML | pipeline frontmatter, outline fixtures, source manifests | Use when humans edit structure and tools need predictable keys |
| Stable tool payload | Versioned JSON | `DOCTOR_REPORT.json`, `RUN_AUDIT.json`, `RUN_AUDIT_DIFF.json`, unit manifests | Pair with schema docs and compatibility checks before downstream reliance |
| Visual lineage or generated figure | SVG or image | `docs/assets/harness-showcase-lineage.svg` | Keep source intent inspectable in docs |
| Compiled knowledge product | PDF, TeX, Markdown | `latex/main.pdf`, `latex/main.tex`, final reports | Treat as final deliverable plus lineage, not as the only evidence surface |
| Declarative graph or contract language | Defer until a consumer exists | none today | Do not introduce a GCL-style language unless a script, validator, or agent policy consumes it |

The project should prefer the simplest format that preserves the interface.
CSV beats a bespoke DSL for flat tables. Markdown plus JSON beats Markdown-only
when tools need stable fields. A richer graph or contract language is justified
only after repeated completed workspaces show that CSV/YAML/JSON are no longer
enough.

## Current Repo Mappings

| Artifact family | Interface role | Human-readable surface | Machine-readable surface | Primary repair surface |
|---|---|---|---|---|
| Workflow protocol | Reusable method for a class of work | `pipelines/*.pipeline.md` body | pipeline frontmatter, `templates/UNITS.*.csv` | pipeline contract, unit template, taxonomy |
| Execution ledger | Durable run state | `GOAL.md`, `STATUS.md`, `CHECKPOINTS.md`, `DECISIONS.md` | `UNITS.csv`, status columns, unit ids, manifests | unit status, checkpoint, decision record |
| Workspace diagnosis | Explain whether a run can continue | `output/DOCTOR_REPORT.md` | `output/DOCTOR_REPORT.json` (`doctor-report.v1`) | doctor issue category, harness validator, workspace contract |
| Run audit | Summarize whole-run evidence | `output/RUN_AUDIT.md` | `output/RUN_AUDIT.json` (`run-audit.v1`) | target artifact contract, manifests, audit validator |
| Audit comparison | Prove whether a repair improved evidence | `output/RUN_AUDIT_DIFF.md` | `output/RUN_AUDIT_DIFF.json` (`run-audit-diff.v1`) | audit-diff logic, schema doc, regression test |
| Improvement report | Map failed evidence to upstream repair surfaces | `output/IMPROVEMENT_REPORT.md` | `output/IMPROVEMENT_REPORT.json` (`improvement-report.v1`) | skill, pipeline, unit template, schema, validator, ADR, or glossary |
| Skill hygiene | Keep capability surface maintainable | console summary, audit docs | `skill-audit-report.v1` JSON output | skill doc, skill standard, audit rule |
| Showcase | Let readers inspect deliverables first | `docs/HARNESS_SHOWCASE.md`, example READMEs | `harness-showcase-audit.v1` JSON output | fixture, protocol link, showcase audit |
| Learning layer | Promote repeated lessons | ADRs, project language, roadmap, pattern register | validation metadata and link checks | ADR, glossary, roadmap, validate_repo |

## Repair Protocol

When a final deliverable or run artifact is weak, do not start by rewriting the
final prose. First locate the failed interface:

1. Identify the observed defect in the final deliverable, showcase fixture, or
   audit report.
2. Locate the upstream artifact that should have carried the missing evidence,
   decision, unit state, or constraint.
3. Classify the failed interface as human-readable, machine-readable, or both.
4. Repair the smallest owning surface: skill, pipeline, unit template, schema,
   validator, ADR, project language, or roadmap.
5. Prove the repair with a local check, test, doctor report, run audit,
   audit diff, or progress-log entry.

This keeps self-improvement bounded. The repo improves by repairing artifacts
and contracts, not by trusting hidden chat memory.

## Anti-Patterns

- A prose-only artifact is consumed by a script or future agent.
- A structured artifact is created but no producer, consumer, or schema name is
  documented.
- A final deliverable is rewritten without attributing the defect to an
  upstream artifact or contract.
- A custom format is introduced before CSV, TSV, YAML, or JSON has failed.
- A private workspace note is required to understand a public repo change.
- A generated sidecar is relied on by tools before compatibility checks exist.

## Extension Rule

Before adding a new artifact family, update at least one durable surface that
declares the interface: pipeline contract, unit template, schema reference,
README section, ADR, project language entry, or validation rule. If the
artifact becomes a project-wide convention, add it to this standard.
