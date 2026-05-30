# Pattern Register

This register records external engineering patterns that are useful for this
repo, and how each pattern maps to current files. It is intentionally a
current-state and decision aid, not a claim that this repo already implements
the full external systems named here.
The high-level synthesis of these patterns is the five-layer operating model in
`docs/HARNESS_OPERATING_MODEL.md`.

Use this file when a future change says "borrow Temporal", "add evaluation
harness", "make this like DVC", or similar. The question should be: which
discipline is useful, what repo artifact should carry it, and what should stay
deferred?

This register should learn from useful external codebases and systems, but it
should not turn their names into a vague upgrade banner. Each borrowed idea
needs a repo-local mapping, a status, and a next action.

## How To Read This Register

- `Adopted` means the repo already has a local mechanism that embodies the
  pattern.
- `Partial` means the idea exists but needs more hardening before it should be
  described as complete.
- `Deferred` means the pattern is useful, but the repo does not yet have enough
  evidence to justify adding that mechanism.

## Pattern Map

| Pattern source | Useful discipline | Current repo mapping | Status | Next action |
|---|---|---|---|---|
| Temporal durable execution | Persist workflow progress so long-running work can resume after process or chat interruption | `UNITS.csv`, `STATUS.md`, stale `DOING` recovery, `CHECKPOINTS.md`, `DECISIONS.md`, `pipeline.py doctor` | `Adopted` | Keep recovery read-only by default; add repair automation only after repeated issue classes justify it |
| DVC pipelines | Make stage dependencies and outputs explicit instead of implied | `pipelines/*.pipeline.md`, `templates/UNITS.*.csv`, unit `inputs`, unit `outputs`, target artifacts, unit manifests, `RUN_AUDIT_DIFF.json` | `Adopted` | Use audit diffs before adding a heavier historical run store |
| Backstage software catalog | Present capabilities as a catalog instead of forcing users to navigate file trees | `docs/PIPELINE_TAXONOMY.md`, README workflow map, executable contract index | `Adopted` | Keep taxonomy drift validation narrow and factual |
| OpenTelemetry semantic conventions | Reuse stable names across tools, docs, and reports | `docs/PROJECT_LANGUAGE.md`, doctor issue fields, remediation categories, run-audit field names | `Adopted` | Pull recurring terms from skills into the glossary only when they affect routing or validation |
| LangGraph persistence | Treat resumable agent state as an explicit checkpointed asset | `PIPELINE.lock.md`, `UNITS.csv`, `DECISIONS.md`, workspace-local reports, `pipeline.py doctor --write` | `Partial` | Keep state file-first; do not introduce a graph runtime without concrete orchestration pressure |
| Prefect flow/task split | Separate workflow shape from task bodies | pipelines and unit templates define orchestration; skills own semantic work | `Adopted` | Preserve the skill-vs-harness split from ADR 0001 |
| MADR/ADR templates | Keep architecture decisions compact but structured enough for future readers and validators | `docs/adr/README.md`, ADR status/date/section contract, `scripts/validate_repo.py` ADR checks | `Adopted` | Keep ADRs short; add a new ADR only when a decision affects repo-level contracts or long-term maintenance |
| JSON Schema-style compatibility | Version machine-readable artifacts before external consumers rely on them | `skill-audit-report.v1`, `doctor-report.v1`, `run-audit.v1`, `run-audit-diff.v1`, `harness-showcase-audit.v1`, `improvement-report.v1`, `artifact-pack.v1`, `validate_skill_audit_payload`, `validate_doctor_payload`, `validate_run_audit_payload`, `validate_run_audit_diff_payload`, `validate_showcase_audit_payload`, `validate_improvement_payload`, `validate_artifact_pack_payload`, `docs/SKILL_AUDIT_SCHEMA.md`, `docs/DOCTOR_REPORT_SCHEMA.md`, `docs/RUN_AUDIT_SCHEMA.md`, `docs/RUN_AUDIT_DIFF_SCHEMA.md`, `docs/SHOWCASE_AUDIT_SCHEMA.md`, `docs/IMPROVEMENT_REPORT_SCHEMA.md`, `docs/ARTIFACT_PACK_SCHEMA.md` | `Partial` | Add formal JSON Schema files only if a non-Python consumer appears |
| SARIF static analysis interchange | Represent static-analysis findings with stable machine-readable records for tool interoperability | `skill-audit-report.v1`, finding records, severity/rule/category fields, and `validate_skill_audit_payload` | `Partial` | Keep repo-local JSON primary; consider SARIF export only if GitHub code scanning or another external static-analysis consumer appears |
| DVC / MLflow metrics and artifacts | Keep evaluation evidence as structured metrics and inspectable artifacts before adding dashboards | `harness-showcase-audit.v1` scorecard, tracked fixture files, required evidence markers, `docs/SHOWCASE_AUDIT_SCHEMA.md` | `Partial` | Keep current scorecard limited to coverage; add semantic metrics only after repeated completed workspaces expose stable criteria |
| Evaluation harnesses and benchmark dashboards | Compare runs over time with stable inputs, outputs, and scoring | run audit, audit diff, target artifact coverage, unit manifests, quality reports | `Partial` | Keep the lightweight diff; defer dashboards and semantic scoring until at least three representative completed workspaces exist |
| Database-backed run stores | Query many historical runs across workspaces | none; workspace files are the current run ledger | `Deferred` | Revisit only when file-based audit becomes painful |
| External workflow runtimes | Schedule, retry, and distribute concurrent runs | none; the harness is intentionally local and file-first | `Deferred` | Revisit when multiple concurrent or remote-worker runs are required |

## Reference Codebases To Learn From

These are reference systems for design discipline, not implementation
dependencies. A future change can add more, but it should map the lesson back
to a current repo file before changing the harness.

| Reference codebase | Useful idea to study | Repo-local question to ask first |
|---|---|---|
| Temporal | Durable execution histories and replay-safe workflow boundaries | Can `UNITS.csv`, `STATUS.md`, and doctor output explain resume state without chat memory? |
| DVC | Stage graphs with declared dependencies and outputs | Are unit inputs, outputs, manifests, and target artifacts explicit enough to compare runs? |
| Backstage | Capability cataloging around ownership and discoverability | Does `docs/PIPELINE_TAXONOMY.md` help users choose a workflow without reading the file tree? |
| OpenTelemetry | Stable semantic names that tools and humans can share | Should a repeated audit or doctor field become canonical project language? |
| LangGraph | Persistent agent state and resumable graph execution | Is file-first checkpointing enough, or is graph orchestration pressure now real? |
| Prefect | Flow/task separation and observable runs | Are pipelines still defining orchestration while skills own semantic work? |
| MADR/ADR templates | Minimal decision records with status, context, decision, consequences, and links | Do repo-level architecture decisions have enough structure for validation and future agents? |
| JSON Schema | Versioned machine-readable artifact contracts | Do `skill-audit-report.v1`, `doctor-report.v1`, and `run-audit.v1` need formal schemas beyond Python compatibility checks? |
| SARIF/OASIS | Static-analysis result interchange for external tooling | Does skill audit need GitHub code-scanning or third-party static-analysis ingestion, or is repo-local JSON enough? |
| DVC metrics / MLflow evaluation | Metrics and artifacts as structured outputs that can be compared without hiding the underlying evidence | Which counts are stable factual coverage signals, and which claims should stay out of the scorecard until semantic benchmarks exist? |

## Adoption Rules

1. Borrow the discipline, not the runtime, unless the current repo has a
   repeated operational problem that files and validation cannot solve.
2. Map every adopted idea to a real file, command, test, or artifact.
3. If an external pattern would create a new source of truth, first decide how
   it interacts with `UNITS.csv`, `STATUS.md`, `DECISIONS.md`, and run audit.
4. If adoption changes a repo-level contract, record the decision as an ADR.
5. Keep deferred patterns explicit so future agents do not rediscover and
   re-propose them as if they were missing by accident.

## Source References

- Temporal documentation: https://docs.temporal.io/temporal
- DVC data pipelines: https://dvc.org/doc/start/data-pipelines
- Backstage software catalog: https://backstage.io/docs/features/software-catalog/
- OpenTelemetry semantic conventions: https://opentelemetry.io/docs/specs/semconv/
- LangGraph persistence: https://docs.langchain.com/oss/python/langgraph/persistence
- Prefect flows and tasks: https://docs.prefect.io/
- MADR project: https://adr.github.io/madr/
- JSON Schema: https://json-schema.org/
- SARIF standard: https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html
- GitHub SARIF support for code scanning: https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning
- DVC metrics, plots, and parameters: https://dvc.org/doc/start/data-pipelines/metrics-parameters-plots
- MLflow model evaluation: https://mlflow.org/docs/latest/ml/evaluation/
