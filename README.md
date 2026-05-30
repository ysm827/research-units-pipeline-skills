# research-units-pipeline-skills

> Languages: **English** | [简体中文](README.zh-CN.md)

This project is an Auto Research Harness.

It is a file-first system for converting open-ended research and writing goals into protocolized execution, durable artifacts, evaluable evidence surfaces, and reusable project knowledge. The model supplies semantic judgment; the harness supplies the constraints that make that judgment resumable, auditable, comparable, and improvable.

## Operating Model

The architecture is easiest to read as a five-layer pyramid:

| Layer | What it means here | Current repo surface |
|---|---|---|
| Learning Layer | reusable project memory | `docs/adr/`, `docs/PROJECT_LANGUAGE.md`, `docs/PATTERN_REGISTER.md`, roadmap, validation |
| Evidence Loop | proof that a run is healthy enough to continue | doctor, audit, audit-diff, quality gates, manifests |
| Execution Ledger | durable per-run state | `workspaces/<name>/`, `UNITS.csv`, `STATUS.md`, `DECISIONS.md`, outputs |
| Workflow Protocol | constrained task shape | `pipelines/*.pipeline.md`, `templates/UNITS.*.csv`, taxonomy |
| Capability Surface | reusable semantic judgment | `.codex/skills/`, references, skill scripts |

Read [docs/AUTO_RESEARCH_HARNESS.md](docs/AUTO_RESEARCH_HARNESS.md) first for the research-program framing, then [docs/HARNESS_OPERATING_MODEL.md](docs/HARNESS_OPERATING_MODEL.md) for the pyramid model. If you want to inspect an output before learning the machinery, start with [docs/HARNESS_SHOWCASE.md](docs/HARNESS_SHOWCASE.md).

The self-improvement story is intentionally bounded: a weak final deliverable should be traced back to intermediate artifacts, workflow protocols, skills, model limits, or harness fallbacks, then repaired through visible contracts and validation. See [docs/HARNESS_IMPROVEMENT_LOOP.md](docs/HARNESS_IMPROVEMENT_LOOP.md). The interface standard for intermediate artifacts lives in [docs/ARTIFACT_INTERFACE_STANDARD.md](docs/ARTIFACT_INTERFACE_STANDARD.md).

## What This Repo Covers

The codebase currently centers on eight workflow contracts:

| Workflow | Use it for | Default deliverable | English | 中文 |
|---|---|---|---|---|
| `arxiv-survey` | evidence-first literature surveys when you want the draft and evidence stack before PDF delivery | `output/DRAFT.md` | [Guide](readme/arxiv-survey.md) | [说明](readme/arxiv-survey.zh-CN.md) |
| `arxiv-survey-latex` | the same survey workflow when compile-ready LaTeX/PDF is part of the contract from the start | `output/DRAFT.md`, `latex/main.tex`, `latex/main.pdf` | [Guide](readme/arxiv-survey.md) | [说明](readme/arxiv-survey.zh-CN.md) |
| `research-brief` | fast topic understanding and reading-path briefs from a small paper set | `output/SNAPSHOT.md` | [Guide](readme/research-brief.md) | [说明](readme/research-brief.zh-CN.md) |
| `paper-review` | traceable single-paper critique, lab review, or referee-style assessment | `output/REVIEW.md` | [Guide](readme/paper-review.md) | [说明](readme/paper-review.zh-CN.md) |
| `evidence-review` | protocol-driven evidence synthesis with screening, extraction, and bounded conclusions | `output/SYNTHESIS.md` | [Guide](readme/evidence-review.md) | [说明](readme/evidence-review.zh-CN.md) |
| `idea-brainstorm` | literature-grounded research direction discovery and discussion memos | `output/REPORT.md` | [Guide](readme/idea-brainstorm.md) | [说明](readme/idea-brainstorm.zh-CN.md) |
| `source-tutorial` | transform multi-source materials into a reader-first tutorial with PDF and Beamer slides | `output/TUTORIAL.md`, `latex/main.pdf`, `latex/slides/main.pdf` | [Guide](readme/source-tutorial.md) | [说明](readme/source-tutorial.zh-CN.md) |
| `graduate-paper` | restructuring an existing Chinese graduation thesis project into a thesis engineering workflow | pipeline + thesis skill packages | [Guide](readme/graduate-paper.md) | [说明](readme/graduate-paper.zh-CN.md) |

These workflows share the same architecture:

- `pipelines/` defines stage contracts, artifact expectations, and required skills.
- `.codex/skills/` holds the reusable skills.
- `workspaces/` stores per-run artifacts and intermediate outputs.
- `readme/` contains feature-level documentation.

Use these workflow names directly. The old alias names have been removed from active routing.

## Skills And Harness

The repo has two layers:

- **Skills** are the semantic units. They describe the research judgment: what to read, what artifact to produce, what acceptance criteria apply, and what guardrails must not be violated.
- **The harness** is the deterministic support layer around those skills. It initializes workspaces, runs unit scripts, validates pipeline contracts, checks generated dependency docs, diagnoses workspace state, records per-unit output manifests, and recovers interrupted `DOING` units.

Keep that split when changing the project: put domain judgment and writing policy in skills; put repeatable checks, recovery, and orchestration in the harness.

## Core Concepts

- `Pipeline`: the contract for a workflow. It defines stages, artifacts, checkpoints, and required skills.
- `Skill`: a reusable capability with explicit inputs, outputs, acceptance criteria, and guardrails.
- `Workspace`: the working directory for a single run under `workspaces/<name>/`, where generated artifacts are written.

The important design choice is artifact-first execution. The model is not expected to keep the whole workflow in memory; it writes intermediate structure, evidence, and review outputs to disk so later stages can build on them.

## When To Use Which Workflow

Use `arxiv-survey` when the goal is a serious review paper with explicit retrieval, structure review, evidence packs, and writing loops, but PDF is not required yet.

Use `arxiv-survey-latex` when the same survey workflow must also deliver compile-ready LaTeX/PDF artifacts.

Use `research-brief` when the goal is to understand a topic quickly, surface the key themes, and produce a reading path rather than a full survey.

Use `paper-review` when the input is a single paper or manuscript and the goal is to assess its claims, evidence, novelty, and risks.

Use `evidence-review` when the goal is to synthesize a candidate pool under an explicit protocol with screening, extraction, and bounded conclusions.

Use `idea-brainstorm` when the goal is to generate a literature-backed memo of candidate research directions for discussion, not to write a paper yet.

Use `source-tutorial` when you already have webpages, PDFs, notes, repo docs, or documentation sites and want to turn them into a reader-first tutorial rather than a survey or memo.

Use `graduate-paper` when you already have thesis materials such as a template, existing TeX, Overleaf drafts, PDFs, figures, or prior papers, and need to reorganize them into a Chinese degree thesis workflow. This path is currently the least automated among the major workflows.

## Three Parallel Review Products

`research-brief`, `paper-review`, and `evidence-review` are now three parallel entry points rather than one workflow with light/heavy modes.

| Workflow | Typical input shape | Internal data flow | Deliverable |
|---|---|---|---|
| `research-brief` | topic prompt, small paper pool, or query seed | topic -> small core set -> outline -> compact briefing | `output/SNAPSHOT.md` |
| `paper-review` | one paper or manuscript | manuscript -> claims -> evidence gaps + novelty matrix -> review | `output/REVIEW.md` |
| `evidence-review` | review question plus candidate pool | question -> protocol -> screening -> extraction + bias -> synthesis | `output/SYNTHESIS.md` |

They are optimized for different user intents:

- `research-brief`: fast orientation and reading-path generation
- `paper-review`: single-paper assessment with traceable critique
- `evidence-review`: auditable many-paper synthesis under an explicit protocol

## How To Use The Repo

1. Start Codex in this repository.
2. Choose a workflow, or describe the outcome you want.
3. Let the selected pipeline write artifacts into a workspace.
4. Inspect the generated files at the relevant checkpoint before continuing.

Typical prompts:

```text
Write a LaTeX survey about embodied AI and show me the outline first.
```

```text
Use the research-brief workflow to give me a one-page briefing on test-time adaptation for robotics.
```

```text
Use the paper-review workflow to critique this manuscript and give me a lab-style review.
```

```text
Use the evidence-review workflow to run a PRISMA-style review on LLM agents for education.
```

```text
Brainstorm literature-grounded research ideas around embodied agents for home robotics.
```

```text
Use the source-tutorial pipeline to turn webpages and repo docs about robot learning into a tutorial with PDF and slides.
```

```text
Use the graduate-paper workflow to reorganize my Chinese thesis materials before rewriting chapters.
```

If you want tighter control, pin the pipeline directly:

- [pipelines/arxiv-survey.pipeline.md](pipelines/arxiv-survey.pipeline.md)
- [pipelines/arxiv-survey-latex.pipeline.md](pipelines/arxiv-survey-latex.pipeline.md)
- [pipelines/research-brief.pipeline.md](pipelines/research-brief.pipeline.md)
- [pipelines/paper-review.pipeline.md](pipelines/paper-review.pipeline.md)
- [pipelines/evidence-review.pipeline.md](pipelines/evidence-review.pipeline.md)
- [pipelines/idea-brainstorm.pipeline.md](pipelines/idea-brainstorm.pipeline.md)
- [pipelines/source-tutorial.pipeline.md](pipelines/source-tutorial.pipeline.md)
- [pipelines/graduate-paper-pipeline.md](pipelines/graduate-paper-pipeline.md)

## Developer Harness

Use these checks before changing pipeline contracts or skill IO:

```bash
python -m pytest -q
python scripts/validate_repo.py
python scripts/audit_skills.py --fail-on WARN
python scripts/audit_skills.py --review-category template_placeholder --limit 20
python scripts/audit_skills.py --summary-only
python scripts/generate_skill_graph.py
python scripts/readiness_audit.py --progress workspaces/harness-upgrade/GOAL_STATUS.md
python scripts/showcase_audit.py --strict
python scripts/pipeline.py doctor --workspace workspaces/<name>
python scripts/pipeline.py doctor --workspace workspaces/<name> --write
python scripts/pipeline.py audit --workspace workspaces/<name> --write
python scripts/pipeline.py audit-diff --before workspaces/<name>/output/RUN_AUDIT.before.json --after workspaces/<name>/output/RUN_AUDIT.json --write
python scripts/pipeline.py improve --workspace workspaces/<name> --write
python scripts/pipeline.py pack --workspace workspaces/<name> --write
python scripts/pipeline.py pack --workspace workspaces/<name> --write-excerpt
```

`validate_repo.py --strict --no-check-quality` is the blocking contract gate for executable pipelines. `audit_skills.py --fail-on WARN` is the local skill hygiene check: WARN-level findings should be actionable repair targets, while INFO findings remain review signals grouped by `review_category` with a `next_action` such as syntax placeholder, reference example, placeholder policy, asset palette, or anti-pattern guidance. Use `--review-category` and `--limit` to inspect one review queue without printing the full report; use `--summary-only` when you only need grouped counts. `readiness_audit.py` checks the evidence surfaces needed before a final harness closure audit; it does not run tests or mark the goal complete. `showcase_audit.py` checks the portable examples under `example/` so the deliverable-first exhibit has real outputs, protocol links, evidence reports, a visual lineage asset, and a conservative coverage scorecard. `pipeline.py doctor` is the workspace-level harness check: it shows the current checkpoint, unit status counts, the next runnable unit, missing dependencies, missing DONE outputs, typed remediation categories, and next actions. Add `--write` to persist the same diagnosis to `output/DOCTOR_REPORT.md` and `output/DOCTOR_REPORT.json`. `pipeline.py audit --write` creates `output/RUN_AUDIT.md` and `output/RUN_AUDIT.json`, a compact run ledger covering workspace files, unit status, target artifact coverage, manifests, recent harness reports, and the audit verdict. Scripted units also write `output/unit_logs/<unit>.<skill>.manifest.json` with output hashes for traceability.

`pipeline.py audit-diff` compares two valid `RUN_AUDIT.json` payloads and, with `--write`, writes `RUN_AUDIT_DIFF.md` and `RUN_AUDIT_DIFF.json` beside the after payload. Use it when a repair or later unit should prove that target artifacts, unit status, manifests, or harness issues improved rather than merely changed. `pipeline.py improve --write` creates `output/IMPROVEMENT_REPORT.md` and `output/IMPROVEMENT_REPORT.json`, a local repair map that turns doctor/run-audit evidence into upstream interfaces, repair surfaces, and validation commands. `pipeline.py pack --write` creates `output/ARTIFACT_PACK.md` and `output/ARTIFACT_PACK.json`, a deliverable-first manifest that indexes target artifacts, unit outputs, run ledgers, harness reports, and unit manifests without exporting an archive. Add `--write-excerpt` when a portable Markdown/TSV handoff excerpt is useful for a fixture or review note.

For the architecture view, start with [docs/AUTO_RESEARCH_HARNESS.md](docs/AUTO_RESEARCH_HARNESS.md), then use [docs/HARNESS_OPERATING_MODEL.md](docs/HARNESS_OPERATING_MODEL.md), [docs/HARNESS_ARCHITECTURE.md](docs/HARNESS_ARCHITECTURE.md), the visual layer map in [docs/HARNESS_SYSTEM_MAP.md](docs/HARNESS_SYSTEM_MAP.md), the deliverable-first exhibit in [docs/HARNESS_SHOWCASE.md](docs/HARNESS_SHOWCASE.md), the command-level run walkthrough in [docs/HARNESS_RUN_WALKTHROUGH.md](docs/HARNESS_RUN_WALKTHROUGH.md), the bounded self-improvement model in [docs/HARNESS_IMPROVEMENT_LOOP.md](docs/HARNESS_IMPROVEMENT_LOOP.md), and the artifact interface standard in [docs/ARTIFACT_INTERFACE_STANDARD.md](docs/ARTIFACT_INTERFACE_STANDARD.md). The staged upgrade path lives in [docs/HARNESS_ROADMAP.md](docs/HARNESS_ROADMAP.md), the current completion evidence ledger lives in [docs/HARNESS_READINESS.md](docs/HARNESS_READINESS.md), the fast readiness audit contract lives in [docs/HARNESS_READINESS_AUDIT.md](docs/HARNESS_READINESS_AUDIT.md), the external pattern mapping lives in [docs/PATTERN_REGISTER.md](docs/PATTERN_REGISTER.md), the `skill-audit-report.v1` field contract lives in [docs/SKILL_AUDIT_SCHEMA.md](docs/SKILL_AUDIT_SCHEMA.md), the `doctor-report.v1` field contract lives in [docs/DOCTOR_REPORT_SCHEMA.md](docs/DOCTOR_REPORT_SCHEMA.md), the `run-audit.v1` field contract lives in [docs/RUN_AUDIT_SCHEMA.md](docs/RUN_AUDIT_SCHEMA.md), the `run-audit-diff.v1` field contract lives in [docs/RUN_AUDIT_DIFF_SCHEMA.md](docs/RUN_AUDIT_DIFF_SCHEMA.md), the `harness-showcase-audit.v1` field contract lives in [docs/SHOWCASE_AUDIT_SCHEMA.md](docs/SHOWCASE_AUDIT_SCHEMA.md), the `improvement-report.v1` field contract lives in [docs/IMPROVEMENT_REPORT_SCHEMA.md](docs/IMPROVEMENT_REPORT_SCHEMA.md), and the `artifact-pack.v1` field contract lives in [docs/ARTIFACT_PACK_SCHEMA.md](docs/ARTIFACT_PACK_SCHEMA.md). Architectural decisions live under [docs/adr/](docs/adr/), including the skills-vs-harness split and the doctor/run-audit/audit-diff/showcase-audit/improvement-report/artifact-pack JSON decisions.

## Recommended Reading Path

1. Read this file for the repo-level picture.
2. Read [docs/AUTO_RESEARCH_HARNESS.md](docs/AUTO_RESEARCH_HARNESS.md) for the Auto Research Harness thesis.
3. Read [docs/HARNESS_SHOWCASE.md](docs/HARNESS_SHOWCASE.md) to inspect a final deliverable first and trace it backward.
4. Read [docs/HARNESS_OPERATING_MODEL.md](docs/HARNESS_OPERATING_MODEL.md) for the pyramid model and system story.
5. Read [docs/HARNESS_SYSTEM_MAP.md](docs/HARNESS_SYSTEM_MAP.md) for the visual layer and execution loop.
6. Read [docs/HARNESS_RUN_WALKTHROUGH.md](docs/HARNESS_RUN_WALKTHROUGH.md) for a real initialized workspace, doctor report, run audit, improvement report, and artifact-pack manifest.
7. Read [docs/HARNESS_IMPROVEMENT_LOOP.md](docs/HARNESS_IMPROVEMENT_LOOP.md) to understand how final-deliverable defects should repair intermediate artifacts and contracts.
8. Read [docs/ARTIFACT_INTERFACE_STANDARD.md](docs/ARTIFACT_INTERFACE_STANDARD.md) before adding a new intermediate report, table, sidecar, or artifact pack.
9. Read [docs/HARNESS_ARCHITECTURE.md](docs/HARNESS_ARCHITECTURE.md) if you are changing the system rather than only running it.
10. Use [docs/HARNESS_ROADMAP.md](docs/HARNESS_ROADMAP.md) to see which upgrades are adopted, deferred, or next.
11. Open the feature guide that matches your task and language.
12. Open the matching pipeline contract under `pipelines/`.
13. Inspect the relevant skills under `.codex/skills/` if you need to change behavior rather than just run it.

## Documentation Map

Feature guides:

| Workflow | English | 中文 |
|---|---|---|
| `arxiv-survey` / `arxiv-survey-latex` | [readme/arxiv-survey.md](readme/arxiv-survey.md) | [readme/arxiv-survey.zh-CN.md](readme/arxiv-survey.zh-CN.md) |
| `research-brief` | [readme/research-brief.md](readme/research-brief.md) | [readme/research-brief.zh-CN.md](readme/research-brief.zh-CN.md) |
| `paper-review` | [readme/paper-review.md](readme/paper-review.md) | [readme/paper-review.zh-CN.md](readme/paper-review.zh-CN.md) |
| `evidence-review` | [readme/evidence-review.md](readme/evidence-review.md) | [readme/evidence-review.zh-CN.md](readme/evidence-review.zh-CN.md) |
| `idea-brainstorm` | [readme/idea-brainstorm.md](readme/idea-brainstorm.md) | [readme/idea-brainstorm.zh-CN.md](readme/idea-brainstorm.zh-CN.md) |
| `source-tutorial` | [readme/source-tutorial.md](readme/source-tutorial.md) | [readme/source-tutorial.zh-CN.md](readme/source-tutorial.zh-CN.md) |
| `graduate-paper` | [readme/graduate-paper.md](readme/graduate-paper.md) | [readme/graduate-paper.zh-CN.md](readme/graduate-paper.zh-CN.md) |

Project references:

- [docs/AUTO_RESEARCH_HARNESS.md](docs/AUTO_RESEARCH_HARNESS.md)
- [docs/HARNESS_ARCHITECTURE.md](docs/HARNESS_ARCHITECTURE.md)
- [docs/HARNESS_OPERATING_MODEL.md](docs/HARNESS_OPERATING_MODEL.md)
- [docs/HARNESS_SYSTEM_MAP.md](docs/HARNESS_SYSTEM_MAP.md)
- [docs/HARNESS_SHOWCASE.md](docs/HARNESS_SHOWCASE.md)
- [docs/HARNESS_RUN_WALKTHROUGH.md](docs/HARNESS_RUN_WALKTHROUGH.md)
- [docs/HARNESS_IMPROVEMENT_LOOP.md](docs/HARNESS_IMPROVEMENT_LOOP.md)
- [docs/ARTIFACT_INTERFACE_STANDARD.md](docs/ARTIFACT_INTERFACE_STANDARD.md)
- [docs/PIPELINE_TAXONOMY.md](docs/PIPELINE_TAXONOMY.md)
- [docs/PROJECT_LANGUAGE.md](docs/PROJECT_LANGUAGE.md)
- [docs/HARNESS_ROADMAP.md](docs/HARNESS_ROADMAP.md)
- [docs/HARNESS_READINESS.md](docs/HARNESS_READINESS.md)
- [docs/HARNESS_READINESS_AUDIT.md](docs/HARNESS_READINESS_AUDIT.md)
- [docs/PATTERN_REGISTER.md](docs/PATTERN_REGISTER.md)
- [docs/SKILL_AUDIT_SCHEMA.md](docs/SKILL_AUDIT_SCHEMA.md)
- [docs/DOCTOR_REPORT_SCHEMA.md](docs/DOCTOR_REPORT_SCHEMA.md)
- [docs/RUN_AUDIT_SCHEMA.md](docs/RUN_AUDIT_SCHEMA.md)
- [docs/RUN_AUDIT_DIFF_SCHEMA.md](docs/RUN_AUDIT_DIFF_SCHEMA.md)
- [docs/SHOWCASE_AUDIT_SCHEMA.md](docs/SHOWCASE_AUDIT_SCHEMA.md)
- [docs/IMPROVEMENT_REPORT_SCHEMA.md](docs/IMPROVEMENT_REPORT_SCHEMA.md)
- [docs/ARTIFACT_PACK_SCHEMA.md](docs/ARTIFACT_PACK_SCHEMA.md)
- [docs/adr/](docs/adr/)
- [SKILL_INDEX.md](SKILL_INDEX.md)
- [SKILLS_STANDARD.md](SKILLS_STANDARD.md)

Multi-language documentation hubs live under `readme/README.*.md` and mirror the current workflow map.

## Current Status

- `arxiv-survey` / `arxiv-survey-latex` are the most complete writing path in the repo and the main survey route, depending on whether PDF is required.
- `research-brief`, `paper-review`, and `evidence-review` now form the review-oriented product family: quick understanding, single-paper assessment, and protocol-driven synthesis.
- `idea-brainstorm` is structured and executable, but optimized for discussion-ready idea memos rather than paper drafting.
- `source-tutorial` is the tutorial path: source-grounded, tutorial-first, with article PDF and Beamer slides as first-class delivery artifacts.
- `graduate-paper` now has a clearer pipeline design and a first batch of thesis-oriented skills, but it should currently be treated as a guided workflow framework rather than a fully automated thesis runner.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)
