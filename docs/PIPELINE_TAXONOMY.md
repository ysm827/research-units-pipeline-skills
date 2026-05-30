# Pipeline Taxonomy

This document groups the repository's workflows into product families and makes
their harness coverage explicit. It is a current-state map, not a promise that
every workflow is equally automated.

## Why A Taxonomy

The repo has many skills, but users choose outcomes. A pipeline taxonomy keeps
those outcomes legible by naming the family, entrypoint, default deliverable,
contract shape, maturity, and harness coverage for each workflow.

The structure borrows a useful idea from software catalogs such as Backstage:
document the system as a set of owned capabilities, not as a flat file tree.
Here the unit of cataloging is a pipeline family.

Source: https://backstage.io/docs/features/software-catalog/

## Maturity Levels

- `Executable`: has frontmatter contract, unit template, target artifacts,
  validation coverage, and normal workspace execution support.
- `Executable variant`: inherits from an executable base and changes a bounded
  part of the contract.
- `Research-stage`: documented workflow and skills exist, but it is not yet a
  strict executable pipeline contract.

## Family Overview

| Family | Pipelines | Primary user intent | Harness maturity | Default deliverables |
|---|---|---|---|---|
| Survey | `arxiv-survey`, `arxiv-survey-latex` | Build evidence-first literature surveys from retrieval through writing | `Executable` + `Executable variant` | `output/DRAFT.md`; variant also `latex/main.tex`, `latex/main.pdf` |
| Review | `research-brief`, `paper-review`, `evidence-review` | Understand a topic, assess one manuscript, or synthesize evidence under protocol | `Executable` | `output/SNAPSHOT.md`, `output/REVIEW.md`, `output/SYNTHESIS.md` |
| Ideation | `idea-brainstorm` | Convert literature signals into discussion-ready research directions | `Executable` | `output/REPORT.md`, `output/APPENDIX.md`, `output/REPORT.json` |
| Tutorial | `source-tutorial` | Rebuild existing sources into a reader-first tutorial with delivery artifacts | `Executable` | `output/TUTORIAL.md`, `latex/main.pdf`, `latex/slides/main.pdf` |
| Thesis | `graduate-paper` | Reconstruct existing Chinese thesis materials into a coherent thesis project | `Research-stage` | thesis pipeline + thesis skill packages; no strict `UNITS` contract yet |

## Executable Contract Index

This index is deliberately redundant with the family sections. It gives
`scripts/validate_repo.py` a cheap way to detect taxonomy drift when executable
pipeline contracts or unit templates change.

| Pipeline | Contract | Unit template | Maturity |
|---|---|---|---|
| `arxiv-survey` | `pipelines/arxiv-survey.pipeline.md` | `templates/UNITS.arxiv-survey.csv` | `Executable` |
| `arxiv-survey-latex` | `pipelines/arxiv-survey-latex.pipeline.md` | `templates/UNITS.arxiv-survey-latex.csv` | `Executable variant` |
| `research-brief` | `pipelines/research-brief.pipeline.md` | `templates/UNITS.research-brief.csv` | `Executable` |
| `paper-review` | `pipelines/paper-review.pipeline.md` | `templates/UNITS.paper-review.csv` | `Executable` |
| `evidence-review` | `pipelines/evidence-review.pipeline.md` | `templates/UNITS.evidence-review.csv` | `Executable` |
| `idea-brainstorm` | `pipelines/idea-brainstorm.pipeline.md` | `templates/UNITS.idea-brainstorm.csv` | `Executable` |
| `source-tutorial` | `pipelines/source-tutorial.pipeline.md` | `templates/UNITS.source-tutorial.csv` | `Executable` |

## Survey Family

### `arxiv-survey`

- Contract: `pipelines/arxiv-survey.pipeline.md`
- Unit template: `templates/UNITS.arxiv-survey.csv`
- Profile: `arxiv-survey`
- Checkpoints: `C0` through `C5`
- Default routing: true
- Harness maturity: `Executable`
- Human gate: `C2` scope and structure approval
- Primary artifact path: `output/DRAFT.md`

Lifecycle:

1. Init
2. Retrieval and core set
3. Structure
4. Evidence
5. Citations and evidence packs
6. Draft

Harness notes:

- Strongest and deepest workflow in the repo.
- Uses section-first structure, quality contracts, evidence self-loop, writer
  self-loop, argument self-loop, citation diversification, audit, and contract
  report.
- Best representative pipeline for testing large harness changes.

### `arxiv-survey-latex`

- Contract: `pipelines/arxiv-survey-latex.pipeline.md`
- Unit template: `templates/UNITS.arxiv-survey-latex.csv`
- Variant of: `arxiv-survey`
- Checkpoints: `C0` through `C5`
- Harness maturity: `Executable variant`
- Primary artifact paths: `output/DRAFT.md`, `latex/main.tex`,
  `latex/main.pdf`, `output/LATEX_BUILD_REPORT.md`

Lifecycle difference:

- Inherits the survey contract and makes LaTeX/PDF delivery mandatory in `C5`.

Harness notes:

- This is the best end-to-end delivery test for the survey family.
- Any change to survey pipeline semantics should be checked against this variant
  so PDF delivery does not silently drift.

## Review Family

The review family has three separate entrypoints. They are not light/heavy modes
of one pipeline.

| Pipeline | Input shape | Core flow | Human gate | Deliverable | Maturity |
|---|---|---|---|---|---|
| `research-brief` | Topic prompt, small paper pool, query seed | retrieval -> taxonomy/outline -> snapshot | `C2` scope + outline | `output/SNAPSHOT.md` | `Executable` |
| `paper-review` | One manuscript or paper | manuscript -> claims -> evidence/novelty audit -> review | none in current contract | `output/REVIEW.md` | `Executable` |
| `evidence-review` | Review question plus candidate pool | protocol -> retrieval -> screening -> extraction -> synthesis | `C1` protocol approval | `output/SYNTHESIS.md` | `Executable` |

Harness notes:

- `research-brief` is optimized for fast orientation and a compact output.
- `paper-review` is traceability-first and does not keep a full deduped paper
  pool by default.
- `evidence-review` is the most protocol-driven review workflow and should be
  the reference point for future screening/extraction harness improvements.

## Ideation Family

### `idea-brainstorm`

- Contract: `pipelines/idea-brainstorm.pipeline.md`
- Unit template: `templates/UNITS.idea-brainstorm.csv`
- Profile: `idea-brainstorm`
- Checkpoints: `C0` through `C5`
- Harness maturity: `Executable`
- Human gates: `C0` brainstorm brief, `C2` focus clusters/lenses
- Primary artifact paths: `output/REPORT.md`, `output/APPENDIX.md`,
  `output/REPORT.json`

Lifecycle:

1. Init and idea brief
2. Retrieval and core set
3. Idea landscape and focus
4. Evidence signals
5. Direction pool and screening
6. Shortlist, memo synthesis, and self-loop

Harness notes:

- This workflow is designed for discussion-ready research direction memos, not
  paper drafting.
- It is the best place to test traceability from literature signals to final
  idea claims.

## Tutorial Family

### `source-tutorial`

- Contract: `pipelines/source-tutorial.pipeline.md`
- Unit template: `templates/UNITS.source-tutorial.csv`
- Profile: `source-tutorial`
- Checkpoints: `C0` through `C4`
- Harness maturity: `Executable`
- Human gate: `C2` source scope, learner profile, and tutorial structure
- Primary artifact paths: `output/TUTORIAL.md`, `latex/main.pdf`,
  `latex/slides/main.pdf`

Lifecycle:

1. Init
2. Source intake
3. Pedagogical structure
4. Tutorial writing
5. Delivery

Harness notes:

- This is the reference workflow for source-grounded, non-survey generation.
- It should remain distinct from `arxiv-survey`: its input is a bounded source
  manifest, not an open literature retrieval task.

## Thesis Family

### `graduate-paper`

- Contract document: `pipelines/graduate-paper-pipeline.md`
- Unit template: none yet
- Profile: thesis workflow framework
- Harness maturity: `Research-stage`
- Primary artifact layer: thesis repository files plus `codex_md/`,
  `claude_md/`, and `output/THESIS_BUILD_REPORT.md`

Lifecycle described by the document:

1. Engineering init and material intake
2. Restore existing materials into Markdown
3. Lock the question list and iteration target
4. Map source roles to thesis chapters
5. Reconstruct chapters around the thesis throughline
6. Align Markdown, terminology, symbols, metrics, and figures
7. Write back to TeX
8. Sync front matter
9. Enhance and verify citations
10. Compile, review layout, and polish style

Harness notes:

- This path is intentionally not presented as a strict executable contract yet.
- It has thesis-specific skills, but should not be counted with the seven
  executable `*.pipeline.md` contracts until a unit template and frontmatter
  contract are added.
- A future upgrade should decide whether to keep it as a guided framework or
  promote it to an executable pipeline.

## Harness Coverage Matrix

| Capability | Survey | Review | Ideation | Tutorial | Thesis |
|---|---|---|---|---|---|
| Frontmatter pipeline contract | yes | yes | yes | yes | no |
| `UNITS.*.csv` template | yes | yes | yes | yes | no |
| `pipeline.py init` support | yes | yes | yes | yes | no |
| Human checkpoints | yes | partial | yes | yes | described, not executable |
| Quality contract | yes | yes | yes | yes | described, not executable |
| Doctor compatibility after workspace init | yes | yes | yes | yes | not applicable yet |
| Delivery artifacts beyond Markdown | latex variant | no | JSON sidecar | PDF + slides | TeX thesis project |
| Best validation representative | `arxiv-survey-latex` | `evidence-review` | `idea-brainstorm` | `source-tutorial` | future decision needed |

## Upgrade Implications

- Use `arxiv-survey-latex` and `source-tutorial` as the first two
  representative pipelines for broad harness checks because they cover complex
  delivery.
- Treat `evidence-review` as the reference for protocol, screening, and
  extraction semantics.
- Treat `idea-brainstorm` as the reference for traceable memo generation from
  intermediate signal tables.
- Treat `graduate-paper` carefully: its documentation and skills are valuable,
  but current validation should not pretend it has an executable unit contract.
