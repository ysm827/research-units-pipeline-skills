# Research Brief Harness Demo: RAG Evaluation

This is a curated documentation fixture for the `research-brief` workflow. It
is designed for readers who want to see the final product first and then trace
how the harness would structure the intermediate evidence.

This fixture is not a claim that a full live retrieval run was completed. Live
run artifacts belong under `workspaces/<name>/`; this tracked example is a
compact exhibit for architecture review, documentation, and tests.

## Final Deliverable First

Start with:

- `output/SNAPSHOT.md`

That file is the reader-facing target of the `research-brief` workflow.

## Trace Back Through The Harness

| Question | Inspect |
|---|---|
| What did the workflow promise to produce? | `pipelines/research-brief.pipeline.md` |
| Which intermediate stages explain the final brief? | `outline/taxonomy.yml`, `outline/outline.yml`, `papers/core_set.csv` |
| What did the deliverable self-check conclude? | `output/DELIVERABLE_SELFLOOP_TODO.md` |
| Did the artifact contract pass for this fixture? | `output/CONTRACT_REPORT.md` |

## Why This Example Exists

The repository contains many contracts and reports. A new reader usually wants
to know the product shape before learning the machinery. This fixture therefore
shows a small but coherent path:

```text
final brief -> outline -> taxonomy -> core set -> self-check -> contract check
```

The live harness commands remain documented in `docs/HARNESS_RUN_WALKTHROUGH.md`.
