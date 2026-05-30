# Harness Architecture

This document is the implementation map for the Auto Research Harness described
in `docs/AUTO_RESEARCH_HARNESS.md`. It should be read after the conceptual
operating model in `docs/HARNESS_OPERATING_MODEL.md` and before modifying
pipeline contracts, harness tooling, or validation rules.

The goal of this document is to keep two layers separate:

- the abstract research architecture, which explains why the system is shaped
  this way
- the concrete repo implementation, which shows which files, commands, tests,
  and reports currently realize that architecture

For visuals, use `docs/HARNESS_SYSTEM_MAP.md`. For a deliverable-first exhibit,
use `docs/HARNESS_SHOWCASE.md`. For a command-level run, use
`docs/HARNESS_RUN_WALKTHROUGH.md`. For the bounded self-improvement control
loop, use `docs/HARNESS_IMPROVEMENT_LOOP.md`. For closure evidence, use
`docs/HARNESS_READINESS.md` and `docs/HARNESS_READINESS_AUDIT.md`. External
patterns are tracked in `docs/PATTERN_REGISTER.md`; canonical terms are tracked
in `docs/PROJECT_LANGUAGE.md`.

## Architectural Thesis

The repository is an Auto Research Harness: a system that lets agents and
humans convert open-ended research or project goals into durable, diagnosable,
and improvable execution records.

The architecture is not a general workflow service. It is intentionally
file-first and workspace-local. Its primary contribution is to place semantic
model work inside a protocol, ledger, evidence, and learning structure.

```text
research intent
-> capability selection
-> workflow protocol
-> execution ledger
-> evidence loop
-> improvement loop
-> reusable learning
```

## Abstract And Concrete Layers

| Abstract layer | Question it answers | Current repo surface |
|---|---|---|
| Research intent | What knowledge product or project outcome is being pursued? | user prompt, `GOAL.md`, README workflow descriptions |
| Capability Surface | Which semantic capabilities can do the work? | `.codex/skills/`, `SKILLS_STANDARD.md`, `SKILL_INDEX.md`, skill references, skill scripts |
| Workflow Protocol | What method constrains this class of work? | `pipelines/*.pipeline.md`, `templates/UNITS.*.csv`, `docs/PIPELINE_TAXONOMY.md` |
| Execution Ledger | Where does run state live outside chat memory? | `workspaces/<name>/`, `PIPELINE.lock.md`, `UNITS.csv`, `STATUS.md`, `CHECKPOINTS.md`, `DECISIONS.md`, `output/*` |
| Evidence Loop | How is run health diagnosed and compared? | `pipeline.py doctor`, `pipeline.py audit`, `pipeline.py audit-diff`, quality gates, manifests, JSON sidecars |
| Improvement Loop | How do final-deliverable defects repair earlier artifacts and contracts? | `docs/HARNESS_IMPROVEMENT_LOOP.md`, audit diffs, schema docs, validation tests, skill and pipeline edits |
| Learning Layer | How do repeated lessons become reusable assets? | `docs/PROJECT_LANGUAGE.md`, `docs/adr/`, `docs/PATTERN_REGISTER.md`, `docs/HARNESS_ROADMAP.md`, validation tests |

The abstract layer should drive future naming and explanation. The concrete
layer should drive implementation, validation, and tests. A new feature is
architecture-aligned only when it strengthens both.

## Layer Contracts

### Capability Surface

Authoritative files:

- `.codex/skills/<skill>/SKILL.md`
- `SKILLS_STANDARD.md`
- `SKILL_INDEX.md`

Skills own semantic judgment: what to read, what to produce, what evidence is
acceptable, what failure modes matter, and what guardrails prevent weak
reader-facing artifacts. Skill scripts may support deterministic scaffolding,
validation, compilation, extraction, or transformation, but they should not hide
domain judgment that belongs in the skill contract.

### Workflow Protocol

Authoritative files:

- `pipelines/*.pipeline.md`
- `templates/UNITS.*.csv`
- `templates/pipeline.schema.md`
- `templates/units.schema.md`

Pipelines describe the method for a class of work. They define routing hints,
stage order, target artifacts, quality contracts, required capabilities, and
human checkpoints. Unit templates make the protocol executable by binding
skills to inputs, outputs, dependencies, owners, checkpoints, and acceptance
criteria.

### Execution Ledger

Authoritative files in each run workspace:

- `PIPELINE.lock.md`
- `GOAL.md`
- `UNITS.csv`
- `STATUS.md`
- `CHECKPOINTS.md`
- `DECISIONS.md`
- `output/QUALITY_GATE.md`
- `output/RUN_ERRORS.md`
- `output/CONTRACT_REPORT.md`
- `output/DOCTOR_REPORT.md`
- `output/DOCTOR_REPORT.json`
- `output/RUN_AUDIT.md`
- `output/RUN_AUDIT.json`
- `output/unit_logs/*.manifest.json`

The workspace is not scratch space. It is the durable state record for one
research or project run. A future agent should be able to resume from this
ledger without reconstructing hidden context from the conversation.

### Evidence Loop

Authoritative files:

- `tooling/harness.py`
- `tooling/harness_contracts.py`
- `tooling/executor.py`
- `tooling/quality_gate.py`
- `scripts/pipeline.py`
- `scripts/validate_repo.py`
- `scripts/audit_skills.py`
- `scripts/generate_skill_graph.py`
- `scripts/readiness_audit.py`
- `tests/test_harness_smoke.py`
- `tests/test_harness_validation.py`
- `tests/test_pipeline_harness_doctor.py`
- `.github/workflows/harness.yml`
- `pyproject.toml`

The evidence loop supplies deterministic observation and comparison:

- `pipeline.py init` creates a workspace and locks a workflow protocol.
- `pipeline.py run-one` and `pipeline.py run` execute runnable units.
- `pipeline.py doctor` diagnoses a workspace without mutating it by default.
- `pipeline.py doctor --write` writes `output/DOCTOR_REPORT.md` and
  `output/DOCTOR_REPORT.json`.
- `pipeline.py audit --write` writes `output/RUN_AUDIT.md` and
  `output/RUN_AUDIT.json`.
- `pipeline.py audit-diff --write` compares two `RUN_AUDIT.json` payloads and
  writes `RUN_AUDIT_DIFF.md` plus `RUN_AUDIT_DIFF.json` beside the later
  payload.
- `validate_repo.py` protects pipeline contracts, docs entrypoints, schema
  references, ADR format, pattern-register metadata, and terminology alignment.
- `audit_skills.py` reports skill hygiene findings with stable JSON output,
  review categories, and next actions.
- `generate_skill_graph.py` regenerates dependency diagrams from skill IO and
  pipeline templates.
- `readiness_audit.py` checks closure evidence surfaces without claiming the
  long-running goal is complete.

### Improvement Loop

Authoritative files:

- `docs/HARNESS_IMPROVEMENT_LOOP.md`
- `docs/HARNESS_SHOWCASE.md`
- `docs/HARNESS_RUN_WALKTHROUGH.md`
- `docs/RUN_AUDIT_SCHEMA.md`
- `docs/RUN_AUDIT_DIFF_SCHEMA.md`
- `docs/SHOWCASE_AUDIT_SCHEMA.md`
- `tests/test_harness_validation.py`

The improvement loop is the project-specific answer to self-improvement. It
does not give the model permission to rewrite the repo invisibly. It requires
each improvement to pass through an inspectable chain:

```text
final defect -> intermediate artifact diagnosis -> repair surface -> validation evidence -> reusable asset
```

The repair surface should be as local as possible:

- skill wording or references when semantic judgment is underspecified
- pipeline stage or unit template when workflow shape is underspecified
- schema docs or validators when tools need stable fields
- doctor, run audit, or audit diff when diagnosis is missing
- ADR, project language, or roadmap when the lesson affects future work

This makes self-improvement a maintainer-friendly harness behavior rather than
an opaque autonomous loop.

Schema references:

- `docs/SKILL_AUDIT_SCHEMA.md`
- `docs/DOCTOR_REPORT_SCHEMA.md`
- `docs/RUN_AUDIT_SCHEMA.md`
- `docs/RUN_AUDIT_DIFF_SCHEMA.md`
- `docs/SHOWCASE_AUDIT_SCHEMA.md`

### Learning Layer

Authoritative files:

- `docs/AUTO_RESEARCH_HARNESS.md`
- `docs/HARNESS_OPERATING_MODEL.md`
- `docs/HARNESS_SYSTEM_MAP.md`
- `docs/HARNESS_IMPROVEMENT_LOOP.md`
- `docs/PROJECT_LANGUAGE.md`
- `docs/PIPELINE_TAXONOMY.md`
- `docs/HARNESS_ROADMAP.md`
- `docs/HARNESS_READINESS.md`
- `docs/HARNESS_READINESS_AUDIT.md`
- `docs/PATTERN_REGISTER.md`
- `docs/adr/`
- `workspaces/harness-upgrade/GOAL_STATUS.md`

The learning layer exists so repeated experience does not remain trapped in
individual runs. Repo-level decisions belong in ADRs. Canonical terms belong in
the project language. Adopted and deferred external patterns belong in the
pattern register and roadmap. Completion claims belong in readiness evidence.

## Workflow-Harness Coupling

The project combines workflows and harness constraints through a control loop:

1. The user describes the desired knowledge product.
2. The operator or routing hint selects one of the current workflow protocols:
   `arxiv-survey`, `arxiv-survey-latex`, `research-brief`, `paper-review`,
   `evidence-review`, `idea-brainstorm`, `source-tutorial`, or
   `graduate-paper`.
3. Executable workflows materialize into `PIPELINE.lock.md` and `UNITS.csv`.
4. Skills produce artifacts under the execution ledger.
5. The evidence loop diagnoses, audits, and compares the state of the run.
6. The improvement loop traces weak final deliverables back to intermediate
   artifact, skill, workflow-protocol, model-capability, or harness-fallback
   gaps.
7. Repeated failures are promoted into skills, pipeline contracts, validation
   rules, schema docs, ADRs, glossary entries, or roadmap changes.

`graduate-paper` is intentionally not described as an executable pipeline yet.
It is a guided thesis workflow framework until it has a machine-readable
frontmatter contract and a unit template.

## Deliverable-First Demonstration

New readers should be able to start from a final product and trace backward
through the harness. The tracked exemplars under `example/` provide that path.

The compact `research-brief` fixture shows a briefing lineage:

```text
output/SNAPSHOT.md
-> outline/outline.yml
-> outline/taxonomy.yml
-> papers/core_set.csv
-> output/DELIVERABLE_SELFLOOP_TODO.md
-> output/CONTRACT_REPORT.md
```

The richer `source-tutorial` fixture shows a delivery lineage:

```text
output/TUTORIAL_EXCERPT.md
-> output/TUTORIAL_SPEC_EXCERPT.md
-> outline/module_plan.yml
-> sources/manifest.summary.yml
-> evidence/TUTORIAL_SELFLOOP.md
-> evidence/DELIVERY_EVIDENCE.md
-> evidence/CONTRACT_REPORT.md
-> evidence/RUN_AUDIT_SUMMARY.md
```

These exemplars are documentation fixtures. Live generated runs still belong
under `workspaces/<name>/` and should be inspected with `pipeline.py doctor`,
`pipeline.py audit`, and `pipeline.py audit-diff`.

## Known Fragility And Mitigation

| Fragile point | Current mitigation | Next strengthening move |
|---|---|---|
| A reader may see many files before seeing the final product | README now points to the operating model; this doc points to a deliverable-first exemplar | Add more completed exemplar runs only after they are representative and auditable |
| Initialized workspaces can look successful before final artifacts exist | `pipeline.py audit` reports missing target artifacts and returns `ATTENTION` | Keep target-artifact coverage visible in run audits and audit diffs |
| Semantic quality is hard to prove mechanically | Skills and quality gates own judgment-heavy checks; audits state their limits | Add representative semantic evaluation fixtures before building a benchmark dashboard |
| Terminology can drift as docs evolve | `docs/PROJECT_LANGUAGE.md` and validation checks protect core terms | Promote repeated terminology drift into stricter validation only when cheap to detect |
| External architecture ideas can become slogans | `docs/PATTERN_REGISTER.md` maps patterns to repo files and adoption status | Add ADRs before adopting heavier runtimes, stores, or dashboards |

## External Patterns Adopted

The maintained register of adopted, partial, and deferred patterns lives in
`docs/PATTERN_REGISTER.md`.

- Temporal durable execution motivates persisted run state and recovery.
- DVC pipeline discipline motivates explicit inputs, outputs, and target
  artifacts.
- LangGraph persistence motivates inspectable agent state across turns and
  checkpoints.
- Prefect workflow/task separation motivates the split between workflow
  protocol and skill behavior.
- MADR-style ADRs motivate compact decision records protected by validation.
- OpenTelemetry semantic conventions motivate stable project language.

The repo borrows the discipline behind these systems, not their full runtime
stacks.

## Extension Policy

New mechanisms should follow this standard:

1. Name the harness layer being deepened.
2. Map the change to existing repo surfaces before adding new ones.
3. Add or update validation when drift would be cheap to detect.
4. Add an ADR when the decision affects long-term structure or compatibility.
5. Keep live run outputs under `workspaces/<name>/`.
6. Keep curated examples under `example/` and label them as fixtures.
7. Avoid claiming semantic benchmark quality until representative completed
   runs and evaluation criteria exist.
