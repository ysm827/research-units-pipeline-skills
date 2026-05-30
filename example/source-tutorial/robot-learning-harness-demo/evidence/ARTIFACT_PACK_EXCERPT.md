# Artifact Pack Excerpt

This portable excerpt shows how the `source-tutorial` showcase fixture would be
indexed by an `artifact-pack.v1` handoff manifest. It uses repo-relative paths
so the example remains portable across clones.

It is not a full `output/ARTIFACT_PACK.json` from a live workspace. Live
workspace manifests may include absolute `workspace` and `repo` fields. This
excerpt preserves the reader-facing shape: start from the tutorial deliverable,
then trace backward through source, teaching structure, delivery, audit, and
contract evidence.

| Category | Path | Exists | Role |
|---|---|---|---|
| `target_artifact` | `output/TUTORIAL_EXCERPT.md` | true | final tutorial excerpt |
| `target_artifact` | `output/TUTORIAL_SPEC_EXCERPT.md` | true | tutorial scope and learner contract |
| `unit_output` | `outline/module_plan.yml` | true | teaching structure |
| `unit_output` | `sources/manifest.summary.yml` | true | source-set evidence |
| `harness_report` | `evidence/TUTORIAL_SELFLOOP.md` | true | tutorial self-check |
| `harness_report` | `evidence/DELIVERY_EVIDENCE.md` | true | article and slide delivery evidence |
| `harness_report` | `evidence/CONTRACT_REPORT.md` | true | contract evidence |
| `harness_report` | `evidence/RUN_AUDIT_SUMMARY.md` | true | run audit evidence |
| `run_ledger` | `README.md` | true | fixture guide |
| `workflow_protocol` | `pipelines/source-tutorial.pipeline.md` | true | reusable pipeline contract |

Handoff verdict for this fixture excerpt: `PASS`.
