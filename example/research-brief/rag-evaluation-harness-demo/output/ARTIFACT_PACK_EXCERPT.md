# Artifact Pack Excerpt

This portable excerpt shows how the `research-brief` showcase fixture would be
indexed by an `artifact-pack.v1` handoff manifest. It uses repo-relative paths
so the example remains portable across clones.

It is not a full `output/ARTIFACT_PACK.json` from a live workspace. Live
workspace manifests may include absolute `workspace` and `repo` fields. This
excerpt preserves the reader-facing shape: start from the final deliverable,
then trace backward through the evidence surfaces.

| Category | Path | Exists | Role |
|---|---|---|---|
| `target_artifact` | `output/SNAPSHOT.md` | true | final deliverable |
| `target_artifact` | `outline/outline.yml` | true | structure evidence |
| `target_artifact` | `outline/taxonomy.yml` | true | topic boundary evidence |
| `target_artifact` | `papers/core_set.csv` | true | source-set evidence |
| `harness_report` | `output/DELIVERABLE_SELFLOOP_TODO.md` | true | deliverable self-check |
| `harness_report` | `output/CONTRACT_REPORT.md` | true | contract evidence |
| `run_ledger` | `README.md` | true | fixture guide |
| `workflow_protocol` | `pipelines/research-brief.pipeline.md` | true | reusable pipeline contract |

Handoff verdict for this fixture excerpt: `PASS`.
