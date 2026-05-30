# Harness Roadmap

This roadmap translates the current architecture documents into staged,
checkable engineering work. It is intentionally grounded in existing files:
skills, pipeline contracts, unit templates, workspaces, manifests, doctor
reports, validation scripts, tests, README files, and ADRs.
The conceptual source for the current story is
`docs/AUTO_RESEARCH_HARNESS.md`, `docs/HARNESS_OPERATING_MODEL.md`, and
`docs/HARNESS_IMPROVEMENT_LOOP.md`.

## Roadmap Principles

1. Keep the harness file-first and workspace-local until there is a proven need
   for an external runtime.
2. Prefer validation, doctor output, and tests over prose-only architecture.
3. Promote repeated run pain into reusable assets: glossary terms, ADRs,
   validation rules, templates, skill improvements, or pipeline contract
   changes.
4. Keep semantic judgment in skills and deterministic repeatability in the
   developer harness.
5. Use representative pipelines for broad changes: `arxiv-survey-latex`,
   `evidence-review`, `idea-brainstorm`, and `source-tutorial`.
6. Treat final-deliverable defects as evidence for improving intermediate
   artifacts, not as a reason to rewrite the final artifact blindly.

## External Patterns To Keep

The canonical source for adopted, partial, and deferred external patterns is
`docs/PATTERN_REGISTER.md`. This roadmap keeps only the patterns that currently
drive staged work.

| Pattern | Why it helps | Current repo mapping | Next use |
|---|---|---|---|
| Durable execution, as practiced by Temporal | Long-running work should resume from persisted state rather than chat memory | `UNITS.csv`, stale `DOING` recovery, `STATUS.md`, `pipeline.py doctor` | Make recovery issues easier to classify and repair |
| Explicit dependencies and outputs, as practiced by DVC pipelines | Artifact contracts should be inspectable rather than implied | unit `inputs`, `outputs`, `depends_on`, target artifacts, unit manifests, `RUN_AUDIT_DIFF.json` | Use audit diffs before considering a heavier regression ledger |
| Capability cataloging, as practiced by Backstage | Users pick capabilities, not file trees | `docs/PIPELINE_TAXONOMY.md` | Keep maturity and ownership visible as workflows evolve |
| Semantic conventions, as practiced by OpenTelemetry | Stable names reduce drift across tools, docs, and reports | `docs/PROJECT_LANGUAGE.md` | Reuse canonical terms in doctor output and validation messages |
| Docs-as-contract | Important architecture entrypoints should fail validation when they drift | README link checks in `scripts/validate_repo.py` | Extend validation only where drift is concrete and cheap to detect |

Sources:

- https://docs.temporal.io/
- https://dvc.org/doc
- https://backstage.io/docs/features/software-catalog/
- https://opentelemetry.io/docs/specs/semconv/

## What Not To Adopt Yet

| Deferred pattern | Reason to defer | Trigger to revisit |
|---|---|---|
| External workflow runtime | Current workflows are file-first and do not need a service dependency | Multiple concurrent runs require scheduling, retries, or remote workers |
| Database-backed run store | Workspace files already act as the run ledger | Queries across many historical workspaces become painful |
| Full benchmark dashboard | No stable corpus of comparable runs exists yet | At least three representative completed workspaces are available |
| Automatic repair planner | The repo first needs typed issue categories and clear repair surfaces | Doctor reports consistently identify the same repair classes |
| Executable thesis pipeline | `graduate-paper` has no unit template or machine-readable pipeline contract yet | A decision is made to promote it from guided framework to executable pipeline |

## Milestones

### M1: Legible Harness Baseline

Status: in progress.

Goal: make the Auto Research Harness architecture understandable and hard to
drift.

Tracked artifacts:

- `docs/HARNESS_ARCHITECTURE.md`
- `docs/AUTO_RESEARCH_HARNESS.md`
- `docs/HARNESS_OPERATING_MODEL.md`
- `docs/HARNESS_SHOWCASE.md`
- `docs/HARNESS_IMPROVEMENT_LOOP.md`
- `docs/PIPELINE_TAXONOMY.md`
- `docs/PROJECT_LANGUAGE.md`
- `docs/HARNESS_ROADMAP.md`
- `docs/HARNESS_READINESS.md`
- `docs/HARNESS_READINESS_AUDIT.md`
- `docs/SHOWCASE_AUDIT_SCHEMA.md`
- `docs/adr/0001-separate-semantic-skills-from-deterministic-harness.md`
- ADR index drift validation in `scripts/validate_repo.py`
- README project reference links
- `scripts/validate_repo.py` docs-entrypoint checks
- `scripts/readiness_audit.py` evidence-surface checks
- `scripts/showcase_audit.py` portable exhibit checks
- `tooling/harness_contracts.py` shared docs/readiness/local-check contract
  constants including `HARNESS_LOCAL_CHECKS`

Acceptance:

- Strict repo validation fails when core harness docs or README entrypoint
  links drift.
- New contributors can find the operating model before dropping into
  file-level commands.
- New contributors can inspect a final deliverable first and trace it back
  through protocol, artifacts, and evidence.
- New contributors can understand how final-deliverable defects should repair
  intermediate artifacts, skills, workflow protocols, validators, or ADRs.
- New contributors can run `scripts/showcase_audit.py --strict` to confirm
  that the tracked examples contain real deliverables, evidence reports,
  protocol links, and the visual lineage asset.
- Future tools can consume `harness-showcase-audit.v1` through
  `docs/SHOWCASE_AUDIT_SCHEMA.md` instead of scraping Markdown.
- The same showcase audit is listed as a local harness check so exhibit
  regressions are treated as harness regressions, not only documentation drift.
- Strict repo validation warns when the external pattern register loses its
  required sections, adopted/partial/deferred status vocabulary, reference
  codebase table, or adoption rules.
- Strict repo validation warns when an ADR file is missing from
  `docs/adr/README.md`, or when the index links a missing ADR file.
- Strict repo validation also checks each ADR's minimal format contract:
  status, date, context, decision, consequences, and related files.
- New contributors can tell the difference between a skill, a pipeline, a
  workspace, and the developer harness without reading chat history.
- A resumed goal can run `scripts/readiness_audit.py` to find missing closure
  evidence surfaces before attempting final verification commands.
- `graduate-paper` remains accurately described as research-stage until its
  executable contract exists.

### M2: Diagnosable Workspace Recovery

Status: in progress.

Goal: make workspace failures easier to classify and repair without executing
more units.

Candidate changes:

- Keep typed remediation categories on `tooling/harness.py` doctor issues.
- Keep default doctor inspection read-only.
- Add tests for missing workspace files, invalid statuses, missing
  dependencies, dependency cycles, and missing DONE outputs.
- Keep `pipeline.py doctor --write` as the explicit opt-in path for writing
  the same diagnosis to `output/DOCTOR_REPORT.md` and
  `output/DOCTOR_REPORT.json`; default doctor remains console-only.
- Keep `tooling.harness.validate_doctor_payload` as the compatibility check
  for the `doctor-report.v1` shape before adding repair automation.
- Keep `docs/DOCTOR_REPORT_SCHEMA.md` aligned with that compatibility check so
  recovery tooling does not need to reverse-engineer Markdown.
- Keep schema validation helpers shared inside `tooling/harness.py` so future
  workspace JSON sidecars do not duplicate type-checking logic.
- Keep schema reference metadata validation in `scripts/validate_repo.py` so
  the schema name, JSON path, producer, validator, and ADR link stay visible.

Acceptance:

- A stuck workspace report names the issue code, severity, affected unit or
  artifact, typed remediation category, and concrete next action.
- The same report can be persisted as `output/DOCTOR_REPORT.md` when a durable
  handoff artifact is useful, with `output/DOCTOR_REPORT.json` as the
  machine-readable sidecar.
- Existing doctor tests still pass for all initialized executable pipelines.
- The doctor remains safe to run before and after interrupted execution.

### M3: Run-Level Audit And Regression Memory

Status: in progress.

Goal: make results auditable across a whole run, not only per unit.

Candidate changes:

- Keep the run summary format pointed at `PIPELINE.lock.md`, `UNITS.csv`,
  `STATUS.md`, `DECISIONS.md`, quality reports, errors, and unit manifests.
- Keep `pipeline.py audit --write` as the lightweight Markdown run ledger at
  `output/RUN_AUDIT.md`, with `output/RUN_AUDIT.json` as the machine-readable
  sidecar for future comparison tooling. This split is recorded in
  `docs/adr/0002-keep-run-audit-as-markdown-plus-json.md`.
- Keep `tooling.harness.validate_run_audit_payload` as the compatibility check
  for the `run-audit.v1` shape before adding comparison tooling.
- Keep `docs/RUN_AUDIT_SCHEMA.md` aligned with that compatibility check so
  future consumers do not need to reverse-engineer the payload from tests.
- Reuse the same schema validation helpers that power doctor-report checks.
- Keep schema reference metadata validation in `scripts/validate_repo.py` so
  the schema name, JSON path, producer, validator, and ADR link stay visible.
- Keep `pipeline.py audit-diff` as the first repo-local comparison surface for
  two `RUN_AUDIT.json` payloads, writing `RUN_AUDIT_DIFF.md` and
  `RUN_AUDIT_DIFF.json` without mutating workspaces.
- Keep `docs/RUN_AUDIT_DIFF_SCHEMA.md` aligned with
  `validate_run_audit_diff_payload` so future comparison consumers do not need
  to scrape Markdown.
- Compare expected target artifacts against generated outputs after a run.
- Keep broader trend dashboards deferred until representative completed
  workspaces exist.

Acceptance:

- A completed workspace can answer: which pipeline ran, which units completed,
  which artifacts were produced, which checks passed, and which decisions were
  made.
- Regression comparison is possible without replaying the whole workflow.
- Tests fail if the `run-audit.v1` payload loses required fields or key
  container types.
- The `run-audit.v1` field contract is documented for future tooling.
- Tests fail if the `run-audit-diff.v1` payload loses required fields or key
  container types.
- The `run-audit-diff.v1` field contract is documented for future tooling.

### M4: Pipeline Contract Maturity

Status: in progress.

Goal: make each workflow's maturity, input shape, output shape, checkpoints,
and success criteria explicit.

Candidate changes:

- Keep `docs/PIPELINE_TAXONOMY.md` synchronized with `pipelines/` and
  `templates/UNITS.*.csv`.
- Keep the current taxonomy drift validation focused on deterministic facts:
  executable pipeline names, contract paths, unit template paths, and the
  `graduate-paper` research-stage marker.
- Decide whether `graduate-paper` should remain a guided framework or become
  an executable pipeline.
- Add ADRs for non-obvious promotion or deferral decisions.

Acceptance:

- Every executable pipeline has current target artifacts, stage coverage,
  representative tests, and documentation.
- Non-executable workflows are clearly named as such and do not pretend to have
  unit-template coverage.
- Strict repo validation warns when executable pipeline metadata disappears
  from `docs/PIPELINE_TAXONOMY.md`.

### M5: Skill And Quality Gate Tightening

Status: in progress.

Goal: reduce drift between skill docs, skill scripts, unit templates, and
quality gates.

Candidate changes:

- Keep the current `audit_skills.py` WARN surface empty and locally checked with
  `python scripts/audit_skills.py --fail-on WARN`.
- Triage new `audit_skills.py` WARN findings as actionable skill hygiene
  regressions.
- Keep diagnostic/example ellipses out of WARN-level `reader_facing_ellipsis`
  results so audit output focuses on strings that can leak into generated
  artifacts.
- Keep skill audit findings grouped by fine-grained `review_category` with
  `next_action` guidance. INFO signals should separate syntax placeholders,
  reference examples, placeholder policy, asset palettes, anti-pattern
  guidance, and template slots before any category is promoted to WARN.
- Keep review-category filtering, detail limiting, and summary-only output in
  `audit_skills.py` so large INFO queues can be sampled before cleanup or
  severity promotion.
- Keep `docs/SKILL_AUDIT_SCHEMA.md` aligned with `skill-audit-report.v1` so
  future audit tooling does not need to reverse-engineer JSON output.
- Keep ADR 0004 visible as the decision that skill audit should remain
  repo-local JSON before any SARIF adapter is justified by an external
  consumer.
- Use canonical project language in high-frequency skill docs.
- Add quality gate tests for the most fragile artifact contracts.
- Document when a script is scaffolding versus semantic execution support.

Acceptance:

- The local WARN-level skill audit check fails on actionable findings while
  INFO-level findings remain review signals.
- Skill audit summaries expose review categories, not only raw rule counts.
- Skill audit users can inspect a single review category without reading the
  full report.
- Skill audit JSON consumers have a documented field contract and a
  compatibility check.

- Blocking skill issues remain near zero.
- High-frequency skills are easier to route, inspect, and test.
- Quality gate messages point to repair paths rather than only failure states.

### M6: Improvement Loop And Product Surfaces

Status: proposed.

Goal: make the self-improvement story operational without pretending the repo
is already a fully autonomous agent runtime.

Candidate changes:

- Add a run-level improvement suggestion report that maps final-deliverable
  defects to likely intermediate artifact, skill, pipeline, schema, validator,
  or ADR repairs.
- Add artifact pack export so a reader can inspect the final deliverable,
  intermediate reports, structured sidecars, decisions, and lineage together.
- Add a run scorecard for B-side or lab settings: deliverable coverage,
  evidence depth, unresolved issues, human checkpoints, and comparison deltas.
- Tighten high-frequency skill cards so natural-language routing can choose a
  workflow and capability with fewer tokens.
- Add natural-language checkpoint operations only after their effects can be
  represented as `DECISIONS.md`, unit status changes, or artifact edits.
- Keep auto research pilot mode bounded to initialized workspaces and guarded
  by doctor, run audit, and human checkpoints.

Acceptance:

- A weak final artifact can be traced to a specific upstream repair surface.
- The recommended repair target is local: skill, pipeline, unit template,
  schema, validator, ADR, or project language.
- Human-readable reports and machine-readable sidecars stay paired when both
  people and tools consume the artifact.
- Product-facing examples remain deliverable-first and auditable through
  `showcase_audit.py`.
- No autonomous policy loop is added before representative completed
  workspaces and evaluator surfaces exist.

## Current Iteration Track

The long-running upgrade goal is tracked in
`workspaces/harness-upgrade/GOAL_STATUS.md`. That workspace-local file records
iteration history, validation results, and next actions. This roadmap is the
tracked repo-level counterpart: it explains where those iterations should
compound.

`docs/HARNESS_READINESS.md` is the current evidence ledger for eventual closure:
it maps completion requirements to repo evidence, validation surfaces, and
remaining risks.

`docs/PATTERN_REGISTER.md` is the current pattern ledger for external learning:
it prevents future upgrades from importing large runtime stacks without first
mapping the underlying discipline to existing repo artifacts.
Strict repo validation protects the register's basic structure and required
reference-codebase/adoption-rule vocabulary.

At least ten substantive iterations are required before the goal can be
considered for completion.
