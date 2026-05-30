# Project Language

This glossary defines canonical language for the repository. It should be used
when editing README files, pipeline docs, skill docs, validation messages, and
harness reports.

The glossary borrows the discipline of semantic conventions: terms should be
stable enough that humans and tools can rely on them. This is similar in spirit
to OpenTelemetry semantic conventions, but scoped to this repo.

Source: https://opentelemetry.io/docs/specs/semconv/

## Canonical Terms

### Auto Research Harness

The project-level identity for this repository.

Use Auto Research Harness when explaining the system as a whole: model-driven
research work constrained by workflow protocols, execution ledgers, evidence
loops, and reusable project knowledge. Do not use it to claim that the repo is
a fully autonomous planner or external workflow runtime.

### Operating model

The conceptual system shape in `docs/HARNESS_OPERATING_MODEL.md`.

Use operating model when explaining why skills, workflow protocols, execution
ledgers, evidence loops, and learning assets belong together. Do not use it as
a synonym for implementation details or CLI commands.

### Capability surface

The bottom layer of the operating model: reusable semantic capabilities and
their local support material.

Current surface: `.codex/skills/`, `SKILLS_STANDARD.md`, `SKILL_INDEX.md`,
skill references, assets, and deterministic skill scripts.

### Skill

A reusable semantic execution unit under `.codex/skills/<skill>/`.

Use `skill` for the unit that owns judgment, acceptance criteria, guardrails,
and selective reference loading. Do not call a skill a function or script.

### Skill script

An optional deterministic helper under `.codex/skills/<skill>/scripts/`.

Use `skill script` only for repeatable support work such as scaffolding,
validation, compilation, extraction, or deterministic transformation. If a
script embeds hidden domain judgment, move that judgment into `SKILL.md`,
`references/`, or `assets/`.

### Pipeline

A workflow contract under `pipelines/`.

Use `pipeline` for the workflow-level contract: stages, routing hints, target
artifacts, quality contract, required skills, and checkpoint shape.

### Workflow protocol

The protocol-level view of a pipeline: the constrained task shape that defines
stages, target artifacts, checkpoints, success criteria, and required
capabilities.

Use workflow protocol when discussing architecture and story. Use pipeline when
referring to the concrete files under `pipelines/`.

### Executable pipeline

A pipeline with frontmatter contract, unit template, target artifacts, and
validation support. Current executable pipelines are the `*.pipeline.md` files.

Do not describe `graduate-paper` as executable until it has a unit template and
machine-readable frontmatter contract.

### Pipeline family

A group of pipelines that serve the same product intent. Current families are
Survey, Review, Ideation, Tutorial, and Thesis.

### Pipeline taxonomy

The catalog of pipeline families and maturity levels in
`docs/PIPELINE_TAXONOMY.md`.

Use the taxonomy to describe current workflow capabilities. Do not use it to
announce a future pipeline before the corresponding contract, documentation, or
research-stage marker exists.

### Taxonomy drift

A mismatch between `docs/PIPELINE_TAXONOMY.md` and the current pipeline
contracts or unit templates.

Current validation checks executable pipeline names, contract paths, unit
template paths, and the `graduate-paper` research-stage marker.

### Harness

The deterministic support layer around skills and pipelines.

The harness owns repeatability: workspace initialization, unit execution,
status transitions, recovery, manifests, doctor reports, validation, audits,
and local smoke checks.

### Implementation surface

A concrete file, command, test, report, or schema that realizes an abstract
harness construct.

Use implementation surface when connecting architecture language to current
repo files. Avoid using implementation details as the top-level story when the
audience first needs the abstract layer.

### Developer harness

The repo-local code and scripts that implement harness behavior:
`tooling/harness.py`, `tooling/executor.py`, `scripts/pipeline.py`,
`scripts/validate_repo.py`, `scripts/audit_skills.py`,
`scripts/generate_skill_graph.py`, tests, `pyproject.toml`, and local harness
checks.

### Local harness check

A repo-local command listed in `HARNESS_LOCAL_CHECKS` inside
`tooling/harness_contracts.py` and referenced by the readiness evidence.

Use local harness check for commands that maintainers should run when a
contract regresses or before a release. Current checks include WARN-level skill
audit and portable showcase audit. Do not add a check until it is fast,
deterministic, and backed by local validation or tests.

### Workspace

The directory for one run, normally under `workspaces/<name>/`.

A workspace is a run ledger. It should contain the selected pipeline, goal,
unit table, status, decisions, generated artifacts, quality reports, errors,
and unit logs.

### Execution ledger

The operating-model name for workspace state as a durable run record.

Use execution ledger when emphasizing resume, audit, handoff, and recovery.
Use workspace when referring to the concrete directory under `workspaces/`.

### Artifact

A file or directory produced or consumed by a unit or stage.

Use `artifact` for durable files that later work can inspect. Avoid using it
for transient chat context.

### Artifact interface

The declared contract around a durable artifact: path, producer, consumer,
format, human-readable view, machine-readable view, trace keys, repair surface,
validation, and visibility.

Use artifact interface when an intermediate artifact is expected to support
handoff, tool consumption, audit, comparison, or future repair. Do not use it
for temporary scratch content that no later person or tool consumes.

### Artifact interface standard

The repo-level standard in `docs/ARTIFACT_INTERFACE_STANDARD.md`.

Use the standard before adding a new report, table, sidecar, artifact pack, or
structured output family. It is the bridge between the improvement loop and
concrete file formats: Markdown for people, CSV/TSV/YAML/JSON for tools, and
paired surfaces when both readers matter.

### Artifact contract

The declared set of required artifacts for a pipeline, stage, or unit.

At pipeline level, this appears in `target_artifacts` and stage `produces`. At
unit level, this appears in `UNITS.csv` `inputs`, `outputs`, and `acceptance`.

### Unit

One row in `UNITS.csv`.

A unit binds a skill to concrete inputs, outputs, acceptance criteria,
dependencies, owner, checkpoint, and status.

### Unit template

A `templates/UNITS.*.csv` file used to materialize `UNITS.csv` in a workspace.

### Checkpoint

A named stage boundary such as `C0`, `C1`, or `C2`.

Use `checkpoint` for durable workflow progress, not for a casual note.

### Human checkpoint

A checkpoint that requires human approval recorded in `DECISIONS.md`.

Human checkpoints are first-class harness state. They should not live only in a
chat transcript.

### Decision

A durable record in `DECISIONS.md` or an ADR.

Use `DECISIONS.md` for per-run approvals and choices. Use ADRs for
repo-level architecture decisions.

### ADR

An architecture decision record under `docs/adr/`.

Use ADRs for decisions that affect project structure, contracts, validation, or
long-term maintenance. Current accepted ADRs are indexed in `docs/adr/README.md`.
Strict repo validation checks that ADR files and the index do not drift. It
also checks the minimal ADR contract: status, date, context, decision,
consequences, and related files.

### Roadmap

The staged repo-level upgrade track in `docs/HARNESS_ROADMAP.md`.

Use the roadmap for adopted, deferred, and next harness work. Do not use it as
a substitute for validation, tests, ADRs, or concrete file changes.

### Pattern register

The external architecture pattern ledger in `docs/PATTERN_REGISTER.md`.

Use the pattern register to map mature project ideas back to current repo
files. Do not use it to claim that this repo has adopted an external runtime
or benchmark system unless a matching local mechanism exists.

Strict repo validation checks the pattern register's required sections,
reference codebase rows, status vocabulary, and adoption rules so external
learning does not drift into an ungrounded slogan.

### Readiness

The completion evidence ledger in `docs/HARNESS_READINESS.md`.

Use readiness to map goal requirements to current evidence, validation
surfaces, and remaining risks. Do not treat readiness as proof of completion
unless the final closure gate has been run against the current worktree.

### Doctor

The workspace diagnosis command: `python scripts/pipeline.py doctor --workspace
workspaces/<name>`.

The doctor should inspect state without mutating it by default. It reports
pipeline lock, current checkpoint, unit status counts, next runnable unit,
harness issues, typed remediation categories, next actions, and recent reports.
With `--write`, it persists the same diagnosis as `output/DOCTOR_REPORT.md`
and `output/DOCTOR_REPORT.json`. The Markdown/JSON split is an accepted
architecture decision.

### Doctor report schema

The `doctor-report.v1` field contract in `docs/DOCTOR_REPORT_SCHEMA.md`.

Use this schema reference when writing tools that consume
`output/DOCTOR_REPORT.json`. Use `validate_doctor_payload` to check payload
compatibility before relying on the fields.

### Improvement report

The workspace repair-map command:
`python scripts/pipeline.py improve --workspace workspaces/<name> --write`.

Use improvement report for the harness artifact that maps doctor/run-audit
evidence to an upstream interface, repair surface, recommended action, and
validation command. Do not describe it as an autonomous repair planner.

The human-readable report is `output/IMPROVEMENT_REPORT.md`; the
machine-readable sidecar is `output/IMPROVEMENT_REPORT.json`.

### Improvement report schema

The `improvement-report.v1` field contract in
`docs/IMPROVEMENT_REPORT_SCHEMA.md`.

Use this schema reference when writing tools that consume
`output/IMPROVEMENT_REPORT.json`. Use `validate_improvement_payload` to check
payload compatibility before relying on the fields.

### Remediation category

A stable repair class attached to a doctor issue.

Use remediation categories to group repeated workspace failures without making
the doctor mutate files. Current examples include `repair_units_contract`,
`repair_dependency_graph`, `repair_unit_status`, `repair_artifact_contract`,
`record_human_checkpoint`, and `restore_workspace_contract`.

### Quality gate

A deterministic check that decides whether a unit's outputs are good enough to
advance.

Quality gates should point to a concrete report and a repair path. They should
not silently rewrite semantic work.

### Audit

A broader review of skill, pipeline, or workspace health.

Examples include `audit_skills.py`, `pipeline-auditor`, and
`artifact-contract-auditor`.

### Audit signal

An audit finding that should point to a likely repair action rather than merely
matching text mechanically.

For skill audits, diagnostic examples and anti-pattern labels should not crowd
out warnings about strings that can leak into generated artifacts.

WARN-level skill audit findings are intended to be blocking for local release
checks. INFO-level
findings are review signals until they are promoted into a sharper rule.

### Review category

The triage class attached to a skill audit finding.

`scripts/audit_skills.py` emits `review_category` and `next_action` for each
finding so INFO-level signals can be grouped and reviewed without reading every
line item as a separate decision. Low-severity ellipsis findings should be
split by maintenance intent, such as `syntax_placeholder`,
`reference_example_phrase`, `placeholder_policy`, `asset_palette_reference`,
`anti_pattern_guidance`, and `template_placeholder`.

Use `audit_skills.py --review-category <name> --limit <N>` to inspect one
review queue, and `audit_skills.py --summary-only` when only grouped counts are
needed.

### Skill audit schema

The `skill-audit-report.v1` field contract in
`docs/SKILL_AUDIT_SCHEMA.md`.

Use this schema reference when writing tools that consume
`python scripts/audit_skills.py --format json`. Use
`validate_skill_audit_payload` to check payload compatibility before relying on
the fields. ADR 0004 records why this repo keeps `skill-audit-report.v1` as a
repo-local JSON contract before adding any SARIF adapter.

### Run audit

The workspace-level audit command:
`python scripts/pipeline.py audit --workspace workspaces/<name>`.

Use run audit to summarize one workspace's run ledger, unit status, target
artifact coverage, unit output manifests, recent harness reports, harness
issues, remediation summary, and audit verdict. With `--write`, it creates
`output/RUN_AUDIT.md` and its machine-readable sidecar
`output/RUN_AUDIT.json`. The Markdown/JSON split is an accepted architecture
decision.

### Evidence loop

The operating-model layer that decides whether a run is healthy enough to
continue, needs repair, or should promote a lesson back into the repo.

Current surfaces include quality gates, `pipeline.py doctor`,
`pipeline.py audit`, `pipeline.py audit-diff`, unit manifests, and JSON schema
sidecars.

### Improvement loop

The cross-layer control model in `docs/HARNESS_IMPROVEMENT_LOOP.md`.

Use improvement loop for the process that starts from a weak final deliverable,
traces the problem back to intermediate artifacts, workflow protocols, skill
contracts, model-capability limits, or harness fallback gaps, then promotes the
repair into a visible repo asset.

Do not use improvement loop to imply invisible self-modification. Evidence
should come from tests, validation, doctor reports, run audits, audit diffs,
schema docs, ADRs, or durable artifact changes.

### Intermediate artifact

A durable artifact that lets a later stage, human reviewer, or tool understand
how a final deliverable was produced.

Use intermediate artifact for reports, tables, sidecars, manifests, outlines,
evidence matrices, extraction forms, checkpoint records, and decisions that
carry state between units. Human-readable intermediate artifacts should be
compact reports. Machine-readable intermediate artifacts should prefer CSV,
TSV, YAML, or versioned JSON.

### Defect attribution

The act of mapping a final-deliverable problem to its most likely upstream
repair surface.

Use defect attribution before rewriting final prose. Common repair surfaces
are skills, pipeline stages, unit templates, artifact contracts, schema docs,
validators, doctor/audit checks, ADRs, and project language.

### Artifact pack

A future product-facing bundle that collects a final deliverable, important
intermediate reports, machine-readable sidecars, decisions, and lineage
evidence for review.

Use artifact pack for exported review material. Do not use it for the entire
workspace or for private developer-local goal logs.

### Run audit diff

The run comparison command:
`python scripts/pipeline.py audit-diff --before <RUN_AUDIT.json> --after <RUN_AUDIT.json>`.

Use run audit diff to compare two already-valid run audit payloads. It reports
unit status deltas, target artifact presence changes, unit output manifest
count changes, harness issue count changes, source verdict changes, and
diff-level comparison issues. With `--write`, it creates `RUN_AUDIT_DIFF.md`
and `RUN_AUDIT_DIFF.json` beside the later audit payload.

Do not use run audit diff to claim semantic quality. It compares harness and
artifact evidence that the underlying run audits already know how to observe.

### Readiness audit

The repo-level evidence-surface audit command:
`python scripts/readiness_audit.py --progress workspaces/harness-upgrade/GOAL_STATUS.md`.

It checks whether completion evidence surfaces are present and discoverable.
It does not run final verification commands and does not mark the long-running
goal complete.

### Harness contract

The shared repo-level list of harness entrypoints, README links, schema
references, local harness checks, current workflows, and readiness-audit
evidence paths.

The current implementation lives in `tooling/harness_contracts.py` and is used
by both `scripts/validate_repo.py` and `scripts/readiness_audit.py`.

### Run audit schema

The `run-audit.v1` field contract in `docs/RUN_AUDIT_SCHEMA.md`.

Use this schema reference when writing tools that consume `output/RUN_AUDIT.json`.
Use `validate_run_audit_payload` to check payload compatibility before relying
on the fields.

### Run audit diff schema

The `run-audit-diff.v1` field contract in
`docs/RUN_AUDIT_DIFF_SCHEMA.md`.

Use this schema reference when writing tools that consume
`RUN_AUDIT_DIFF.json`. Use `validate_run_audit_diff_payload` to check payload
compatibility before relying on the fields.

### Showcase audit schema

The `harness-showcase-audit.v1` field contract in
`docs/SHOWCASE_AUDIT_SCHEMA.md`.

Use this schema reference when writing tools that consume
`python scripts/showcase_audit.py --format json`. Use
`validate_showcase_audit_payload` to check payload compatibility before
relying on the fields.

### Schema compatibility check

A lightweight validator in `tooling/harness.py` that checks a workspace JSON
sidecar's stable shape before future tooling relies on it.

Current checks include `validate_skill_audit_payload`,
`validate_doctor_payload`, `validate_run_audit_payload`, and
`validate_run_audit_diff_payload`. The showcase audit also exposes
`validate_showcase_audit_payload` because its JSON output is a repo-level
exhibit contract. Workspace JSON sidecars share common type-checking helpers
inside `tooling/harness.py`; skill audit JSON owns its check in
`scripts/audit_skills.py` because it is a repo-level static-audit command
rather than a workspace artifact.

Schema reference docs are also checked by `scripts/validate_repo.py` so the
schema name, output path or command, producer, and validator remain
discoverable.

### Manifest

A machine-readable record of generated outputs.

Current unit manifests live under `output/unit_logs/*.manifest.json` and record
unit id, skill, status, exit code, output paths, existence, file size, and
hashes.

### Recovery

The harness behavior that turns stale interrupted state into an inspectable
state.

Current example: stale `DOING` units are recovered to `BLOCKED` before the next
runner invocation.

### Self-loop

A workflow unit or skill that diagnoses a failure and routes a bounded repair
instead of letting weak artifacts pass downstream.

Examples include `evidence-selfloop`, `writer-selfloop`,
`argument-selfloop`, `tutorial-selfloop`, and `deliverable-selfloop`.

### Reroute

An explicit upstream return path when a later stage discovers that earlier
artifacts are insufficient.

Use `reroute` for planned workflow repair, not for ad hoc rewriting.

### Run ledger

The set of workspace files that make a run inspectable: `PIPELINE.lock.md`,
`GOAL.md`, `UNITS.csv`, `STATUS.md`, `CHECKPOINTS.md`, `DECISIONS.md`,
reports, logs, and manifests.

The compact workspace diagnosis artifacts are `output/DOCTOR_REPORT.md` for
people and `output/DOCTOR_REPORT.json` for future recovery tooling. The compact
run-level audit artifacts are `output/RUN_AUDIT.md` for people and
`output/RUN_AUDIT.json` for future comparison tooling.

### Showcase fixture

A tracked example under `example/` that demonstrates deliverable lineage for
readers.

Use showcase fixture for curated examples that are portable across clones. Do
not use it as a synonym for a live workspace under `workspaces/<name>/`.

### Showcase audit

The repo-level exhibit check:
`python scripts/showcase_audit.py --strict`.

Use showcase audit to verify that portable examples under `example/` still
contain reader-facing deliverables, protocol links, evidence reports, and the
visual lineage asset. Do not use it as a substitute for live retrieval,
compilation, run audit, or semantic quality review.

The same command is listed as a local harness check for exhibit regressions.

## Terms To Avoid Or Qualify

- Avoid `automation` when the work is really LLM-first semantic execution.
  Prefer `harness` or `pipeline` depending on scope.
- Avoid `script` as a synonym for `skill`.
- Avoid `workflow` when the file-level contract is specifically a `pipeline`.
- Avoid calling `graduate-paper` executable until the contract exists.
- Avoid saying a run is "complete" unless artifact contracts, unit statuses,
  and relevant quality gates support that claim.
- Avoid saying "checks prove quality"; local checks prove only the contracts
  they inspect.

## Current Naming Conventions

- Pipeline names are lowercase with hyphens.
- Skill names are lowercase with hyphens and match `.codex/skills/<skill>/`.
- Workspace outputs stay under `workspaces/<name>/`.
- Run-local logs and reports stay under `output/`.
- Architecture docs live under `docs/`.
- Repo-level architecture decisions live under `docs/adr/`.
- Staged harness roadmap lives in `docs/HARNESS_ROADMAP.md`.
