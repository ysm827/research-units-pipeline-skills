# Auto Research Harness Program

This document states the research program behind the repository. It uses a
more formal style than the README because its job is to explain why the
architecture is coherent before a reader learns the local file tree.

## Abstract

The project treats open-ended research and project work as a controlled
knowledge-production process. A model may supply semantic judgment, but the
project must supply the constraints that make that judgment repeatable,
inspectable, and improvable.

The central thesis is:

```text
Auto Research becomes reliable only when model actions are constrained by a
harness that protocolizes work, externalizes state, audits evidence, and
promotes repeated lessons into reusable project knowledge.
```

This repository implements that thesis as a file-first research/workflow
harness. It does not claim to be a fully autonomous research runtime. Instead,
it provides the minimum durable structure needed for agents and humans to run
research workflows without relying on chat memory.

## Problem Statement

Single prompts are flexible but fragile. They can produce good local results,
yet they rarely preserve enough state to support resumption, audit, or
cross-run learning.

Pure scripts are repeatable but too narrow for research. They can enforce a
mechanical sequence, yet they cannot by themselves judge literature scope,
argument quality, evidence gaps, novelty, or reader fit.

The project therefore adopts a hybrid architecture:

- semantic skills perform judgment-heavy work
- workflow protocols constrain the shape of that work
- execution ledgers persist run state and artifacts
- evidence loops diagnose and compare run health
- improvement loops trace final-deliverable defects back to intermediate
  artifacts and repair surfaces
- learning layers turn recurring experience into project-level memory

The harness is the part that makes the semantic system cumulative rather than
episodic.

## Contributions

### 1. Protocolized research execution

Research workflows are represented as named protocols rather than loose prompt
recipes. Current protocol surfaces are `pipelines/*.pipeline.md` and
`templates/UNITS.*.csv`.

This lets the project describe a workflow by its intent, stages, artifacts,
checkpoints, and success criteria before any particular model run begins.

### 2. Artifact-centered continuity

Each run is written into `workspaces/<name>/` as an execution ledger. The
ledger contains the selected protocol, goal, unit graph, status, checkpoints,
decisions, outputs, reports, logs, and manifests.

The important design move is that state is not assumed to live inside the
conversation. It is externalized into files that future agents, scripts, and
humans can inspect.

### 3. Evidence-mediated improvement

The project distinguishes productive output from healthy execution. A draft,
brief, review, or tutorial is only one surface. The harness also produces
doctor reports, run audits, audit diffs, quality reports, and schema sidecars.

These evidence surfaces let the project answer questions such as:

- What workflow was actually selected?
- Which artifacts were required?
- Which units ran or remain blocked?
- Which target artifacts are missing?
- Did the run become healthier after a repair?

### 4. Bounded self-improvement

A first run may produce a weak deliverable. The harness value is that the run
should leave enough evidence to explain why: missing intermediate artifacts,
unclear skill contracts, weak workflow checkpoints, unstable schema surfaces,
or missing fallback behavior under model limits.

The improvement loop is therefore explicit:

```text
final defect -> intermediate diagnosis -> local repair -> validation evidence -> reusable asset
```

The detailed control model lives in `docs/HARNESS_IMPROVEMENT_LOOP.md`.

### 5. Governed learning

The project treats reusable lessons as architecture assets. Repeated failures
should become better skills, pipeline contracts, validation rules, ADRs,
glossary entries, pattern-register updates, or roadmap changes.

This is why the upper layer is called the Learning Layer rather than "docs":
the documents are not passive explanation; they are governance surfaces for
future execution.

## Abstract Layer Versus Implementation Layer

| Abstract construct | Research role | Current implementation |
|---|---|---|
| Research intent | The desired knowledge product or project outcome | User prompt plus `GOAL.md` |
| Capability Surface | Reusable semantic judgment and domain methods | `.codex/skills/`, `SKILLS_STANDARD.md`, `SKILL_INDEX.md`, references, assets, skill scripts |
| Workflow Protocol | A constrained method for producing a class of deliverables | `pipelines/*.pipeline.md`, `templates/UNITS.*.csv`, `docs/PIPELINE_TAXONOMY.md` |
| Execution Ledger | Durable record of one run | `workspaces/<name>/`, `PIPELINE.lock.md`, `UNITS.csv`, `STATUS.md`, `CHECKPOINTS.md`, `DECISIONS.md`, `output/*` |
| Evidence Loop | Diagnosis, audit, comparison, and quality checks | `pipeline.py doctor`, `pipeline.py audit`, `pipeline.py audit-diff`, quality gates, manifests, schema sidecars |
| Improvement Loop | Defect attribution and bounded repair | `docs/HARNESS_IMPROVEMENT_LOOP.md`, audit diffs, schema docs, validation tests, skill and pipeline edits |
| Learning Layer | Project-level memory and governance | `docs/PROJECT_LANGUAGE.md`, `docs/adr/`, `docs/PATTERN_REGISTER.md`, `docs/HARNESS_ROADMAP.md`, validation tests |

The abstract layer is stable language for readers and future architecture
work. The implementation layer is the current file-first mechanism. New
capabilities should first explain which abstract construct they deepen before
they add new files or commands.

## Reader-Centered Demonstration Path

A reader encountering the project should not have to start from the command
surface. The intended reading path is deliverable-first:

1. Inspect the target deliverable for a workflow.
2. Trace the deliverable back to the workflow protocol.
3. Inspect the execution ledger that produced or would produce it.
4. Read the evidence reports that decide whether the run is healthy.
5. Follow promoted lessons into ADRs, glossary terms, roadmap entries, or
   validation rules.

Two tracked exemplars follow this path:

- `example/research-brief/rag-evaluation-harness-demo/README.md` demonstrates a
  compact briefing lineage.
- `example/source-tutorial/robot-learning-harness-demo/README.md` demonstrates
  a richer tutorial lineage with article and slide delivery evidence.

They are curated documentation fixtures, not substitutes for live workspace
execution.

## Harness As Model Optimization

The harness does not optimize model weights. It optimizes the conditions under
which a model performs research work:

- it narrows ambiguous goals into workflow protocols
- it reduces context loss by externalizing state
- it blocks premature completion through artifact contracts
- it exposes failures through doctor and audit reports
- it compares run evidence through audit diffs
- it attributes final-deliverable defects to upstream artifact or contract
  problems
- it turns repeated failures into reusable assets

This is the sense in which the project is an Auto Research system with harness
constraints. Autonomy is not treated as the absence of structure. Autonomy is
treated as the ability to move through a structured research protocol while
leaving enough evidence for recovery, review, and improvement.

## Current Boundary

The repository currently provides a file-first harness. It does not yet provide:

- a full autonomous planner that invents arbitrary workflows
- a database-backed run store
- a distributed scheduler
- a semantic benchmark dashboard
- a completed corpus of comparable demonstration runs
- an executable `graduate-paper` pipeline contract

Those remain future extensions. They should be adopted only when the execution
ledger and evidence loop show repeated pressure for them.

## Design Standard For Future Work

Future changes should satisfy three questions:

1. What research capability or project workflow does this make more reliable?
2. Which harness layer does it deepen: capability, protocol, ledger, evidence,
   improvement, or learning?
3. What artifact, report, schema, test, or ADR proves the change exists?

If a proposed feature cannot answer those questions, it is probably a local
convenience rather than a harness upgrade.
