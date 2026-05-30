# Source Tutorial Harness Demo: Robot Learning

This tracked fixture is a deliverable-first exhibit for the `source-tutorial`
workflow. It is derived from the completed local workspace
`workspaces/source-tutorial-real-e2e-20260412/`, but it is intentionally smaller
than a full workspace so it can remain portable in the repository.

The fixture demonstrates how the harness turns mixed sources into a reader-first
tutorial, then verifies delivery and artifact completeness.

## Final Deliverable First

Start with:

- `output/TUTORIAL_EXCERPT.md`

That file is an excerpt of the reader-facing tutorial. In the completed local
workspace, the full workflow also produced:

- `output/TUTORIAL.md`
- `latex/main.pdf`
- `latex/slides/main.pdf`

PDF binaries are not copied into this tracked fixture. Their existence and build
status are summarized in `evidence/DELIVERY_EVIDENCE.md`.

## Trace Back Through The Harness

| Question | Inspect |
|---|---|
| What tutorial did the workflow produce? | `output/TUTORIAL_EXCERPT.md` |
| What learner profile and scope constrained it? | `output/TUTORIAL_SPEC_EXCERPT.md` |
| What teaching modules explain its structure? | `outline/module_plan.yml` |
| What source types were ingested? | `sources/manifest.summary.yml` |
| Did the tutorial self-check pass? | `evidence/TUTORIAL_SELFLOOP.md` |
| Did article and slide delivery succeed? | `evidence/DELIVERY_EVIDENCE.md` |
| Did the artifact contract pass? | `evidence/CONTRACT_REPORT.md` |
| What would a portable handoff manifest index first? | `evidence/ARTIFACT_PACK_EXCERPT.md`, `evidence/ARTIFACT_PACK_EXCERPT.tsv` |
| Which workflow protocol defines the target artifacts? | `pipelines/source-tutorial.pipeline.md` |

## Why This Example Exists

The `research-brief` fixture shows a compact evidence chain. This fixture shows
a richer product chain:

```text
source set
-> tutorial spec
-> module plan
-> tutorial article
-> article PDF + Beamer slides
-> self-check + contract evidence
-> run audit + artifact-pack excerpt
```

That makes it a better first exhibit for readers who want to see the final
deliverable goal before learning the harness machinery.
