# Harness Readiness

This document is the current evidence ledger for the long-running harness
upgrade. It does not mark the project complete by itself. It explains what is
already grounded in repo files, what is validated, and what remains open before
the project should be treated as a mature research/workflow harness system.

## Current Readiness

Status: foundation is in place, completion still requires an explicit final
audit after the tenth substantive iteration.

The repo now has the main pieces of a file-first harness system:

- operating model in `docs/HARNESS_OPERATING_MODEL.md`
- Auto Research Harness thesis in `docs/AUTO_RESEARCH_HARNESS.md`
- architecture narrative in `docs/HARNESS_ARCHITECTURE.md`
- visual layer and execution map in `docs/HARNESS_SYSTEM_MAP.md`
- deliverable-first showcase in `docs/HARNESS_SHOWCASE.md`
- fixture refresh guide in `docs/SHOWCASE_FIXTURE_REFRESH.md`
- command-level run walkthrough in `docs/HARNESS_RUN_WALKTHROUGH.md`
- bounded self-improvement model in `docs/HARNESS_IMPROVEMENT_LOOP.md`
- artifact interface standard in `docs/ARTIFACT_INTERFACE_STANDARD.md`
- pipeline family catalog in `docs/PIPELINE_TAXONOMY.md`
- canonical language in `docs/PROJECT_LANGUAGE.md`
- staged upgrade path in `docs/HARNESS_ROADMAP.md`
- external pattern ledger in `docs/PATTERN_REGISTER.md`
- ADR set in `docs/adr/`
- `skill-audit-report.v1` field reference in `docs/SKILL_AUDIT_SCHEMA.md`
- workspace diagnosis through `python scripts/pipeline.py doctor`
- durable doctor handoff through `python scripts/pipeline.py doctor --write`
- `doctor-report.v1` field reference in `docs/DOCTOR_REPORT_SCHEMA.md`
- run audit through `python scripts/pipeline.py audit`
- `run-audit.v1` field reference in `docs/RUN_AUDIT_SCHEMA.md`
- run audit comparison through `python scripts/pipeline.py audit-diff`
- `run-audit-diff.v1` field reference in `docs/RUN_AUDIT_DIFF_SCHEMA.md`
- improvement report through `python scripts/pipeline.py improve`
- `improvement-report.v1` field reference in
  `docs/IMPROVEMENT_REPORT_SCHEMA.md`
- artifact pack manifest through `python scripts/pipeline.py pack`
- `artifact-pack.v1` field reference in `docs/ARTIFACT_PACK_SCHEMA.md`
- fast readiness evidence-surface audit through
  `python scripts/readiness_audit.py`
- portable showcase audit through `python scripts/showcase_audit.py --strict`
- `harness-showcase-audit.v1` field reference in
  `docs/SHOWCASE_AUDIT_SCHEMA.md`
- docs, taxonomy, pipeline, skill, and harness tests through `scripts/` and
  `tests/`

## Completion Evidence Matrix

| Requirement | Current evidence | Current status | Remaining risk |
|---|---|---|---|
| At least ten substantive iterations | `workspaces/harness-upgrade/GOAL_STATUS.md` records the iteration history | In progress; verify the final count before closure | The progress ledger is workspace-local and must be read before marking complete |
| Clear harness architecture | `docs/AUTO_RESEARCH_HARNESS.md` defines the formal thesis; `docs/HARNESS_OPERATING_MODEL.md` defines the pyramid model and system story; `docs/HARNESS_ARCHITECTURE.md` maps abstraction to current implementation surfaces; `docs/HARNESS_SYSTEM_MAP.md` shows the layer relationships, execution loop, and evolution story; `docs/HARNESS_SHOWCASE.md` starts from deliverables; `docs/HARNESS_RUN_WALKTHROUGH.md` grounds the CLI in an initialized `research-brief` workspace; `docs/HARNESS_IMPROVEMENT_LOOP.md` defines the bounded self-improvement model | Substantial | Some skill docs may still use older language |
| Clear pipeline taxonomy | `docs/PIPELINE_TAXONOMY.md` groups workflows and includes an executable contract index | Substantial and validation-backed | Future workflows can still drift if taxonomy validation stays too narrow |
| Unified project language | `docs/PROJECT_LANGUAGE.md` defines canonical terms for docs, scripts, and reports | Substantial | High-frequency skills still need terminology cleanup if drift is found |
| README explains skills and harness | `README.md` and `README.zh-CN.md` introduce the operating model, explain Skills And Harness, and link architecture docs | Substantial | README should stay compact and not become a second architecture spec |
| ADRs record key architecture choices | `docs/adr/0001-...md`, `docs/adr/0002-...md`, `docs/adr/0003-...md`, `docs/adr/0004-...md`, `docs/adr/0005-...md`, `docs/adr/0006-...md`, `docs/adr/0007-...md`, `docs/adr/0008-...md`, `docs/adr/README.md`, ADR index drift validation, and ADR format-contract validation | Substantial and validation-backed | More ADRs may be needed if thesis promotion or benchmark dashboard decisions harden |
| Validation is real, not prose-only | `scripts/validate_repo.py`, `scripts/readiness_audit.py`, `tooling/harness_contracts.py`, schema reference metadata checks, readiness-audit metadata checks, `tests/test_harness_validation.py`, shared schema validation helpers in `tooling/harness.py`, and strict validation checks | Substantial | Validation is intentionally narrow and does not judge prose quality |
| Workspace diagnosis is inspectable | `tooling/harness.py`, `scripts/pipeline.py doctor`, `output/DOCTOR_REPORT.md`, `output/DOCTOR_REPORT.json`, `validate_doctor_payload`, shared schema validation helpers, schema reference metadata checks, `docs/DOCTOR_REPORT_SCHEMA.md`, `docs/HARNESS_RUN_WALKTHROUGH.md`, and doctor tests | Substantial | Doctor report now has a JSON sidecar; automatic repair planning is still deferred |
| Results are auditable | `pipeline.py audit --write`, `output/RUN_AUDIT.md`, `output/RUN_AUDIT.json`, `validate_run_audit_payload`, `pipeline.py audit-diff`, `RUN_AUDIT_DIFF.md`, `RUN_AUDIT_DIFF.json`, `validate_run_audit_diff_payload`, shared schema validation helpers, schema reference metadata checks, `docs/RUN_AUDIT_SCHEMA.md`, `docs/RUN_AUDIT_DIFF_SCHEMA.md`, and `docs/HARNESS_RUN_WALKTHROUGH.md` | Substantial | Broader trend dashboards are deferred until representative completed workspaces exist |
| Improvement loop is bounded | `docs/HARNESS_IMPROVEMENT_LOOP.md` maps final-deliverable defects to intermediate artifact diagnosis, local repair surfaces, validation evidence, and public repo memory; `pipeline.py improve --write` creates `IMPROVEMENT_REPORT.md/json`; `docs/IMPROVEMENT_REPORT_SCHEMA.md` documents `improvement-report.v1` | Substantial | Current report maps harness evidence to repair surfaces; semantic final-deliverable critique remains future evaluator work |
| Deliverable-first handoff is inspectable | `pipeline.py pack --write` creates `ARTIFACT_PACK.md/json`; `docs/ARTIFACT_PACK_SCHEMA.md` documents `artifact-pack.v1`; ADR 0008 keeps it as a manifest before archive export | Substantial | It indexes artifacts but does not yet copy, compress, publish, or render a dashboard |
| Intermediate artifacts have a declared interface | `docs/ARTIFACT_INTERFACE_STANDARD.md` defines artifact path, producer, consumer, format, human view, machine view, trace keys, repair surface, validation, and visibility; `scripts/validate_repo.py` checks the standard's required sections, fields, formats, and current repo mappings | Substantial and validation-backed | Future new artifact families still need local validation when drift becomes concrete |
| External patterns are adopted selectively | Architecture, roadmap, taxonomy, language, `docs/PATTERN_REGISTER.md`, ADR docs, and pattern-register contract validation map external patterns to repo mechanisms | Substantial and validation-backed | Avoid importing large runtime stacks before file-first pain justifies them |
| Existing workflows remain usable | Strict validation, smoke tests, doctor/audit tests, WARN-level skill audit checks, showcase audit checks, tracked `research-brief` and `source-tutorial` showcase fixtures, `scripts/showcase_audit.py`, `docs/SHOWCASE_AUDIT_SCHEMA.md`, `docs/SHOWCASE_FIXTURE_REFRESH.md`, and a local completed `source-tutorial` workspace exhibit when available | Partially proven | Full end-to-end runs are not part of the lightweight readiness gate |
| Skill audit signal is actionable | `scripts/audit_skills.py` distinguishes diagnostic/example ellipsis from likely generated-artifact leakage, emits fine-grained `review_category` values plus `next_action`, supports review-category filtering/limits/summary-only output, documents `skill-audit-report.v1` in `docs/SKILL_AUDIT_SCHEMA.md`, and is checked locally with `python scripts/audit_skills.py --fail-on WARN` | Improved and locally checkable | INFO-level findings remain review signals rather than blockers |

## Adopted Patterns And Repo Mapping

| External pattern | Repo-local mapping | Why it is adopted this way |
|---|---|---|
| Durable execution | `UNITS.csv`, status recovery, `STATUS.md`, `pipeline.py doctor` | Long work should survive chat or process interruption |
| Explicit dependency/output tracking | unit inputs, unit outputs, target artifacts, manifests, run audit, audit diff | Later stages need inspectable artifacts rather than implied state |
| Capability catalog | `docs/PIPELINE_TAXONOMY.md` plus taxonomy drift validation | Users choose workflow capabilities, not file trees |
| Semantic conventions | `docs/PROJECT_LANGUAGE.md` | Stable terms reduce drift across skills, docs, and harness output |
| ADR-driven architecture | `docs/adr/` plus ADR index drift validation | Decisions that guide future tooling should not live only in chat history |
| Docs-as-contract | README link checks and harness doc entrypoint validation | Important architecture entrypoints should be protected by validation |

## Deferred Patterns

These remain intentionally out of scope until the repo has stronger evidence
that they are needed:

- external workflow runtime
- database-backed run store
- full benchmark dashboard
- automatic repair planner
- executable `graduate-paper` pipeline

The deferral rationale and revisit triggers live in `docs/HARNESS_ROADMAP.md`
and `docs/PATTERN_REGISTER.md`.

## Final Closure Gate

Before marking the long-running goal complete, perform a final audit with the
current worktree:

1. Read `workspaces/harness-upgrade/GOAL_STATUS.md` and verify at least ten
   substantive iterations are recorded.
2. Run the fast evidence-surface audit:
   `python scripts/readiness_audit.py --progress workspaces/harness-upgrade/GOAL_STATUS.md --strict`.
3. Run the portable showcase audit:
   `python scripts/showcase_audit.py --strict`.
4. Inspect `README.md`, `README.zh-CN.md`, `docs/AUTO_RESEARCH_HARNESS.md`,
   `docs/HARNESS_OPERATING_MODEL.md`, `docs/HARNESS_ARCHITECTURE.md`,
   `docs/HARNESS_SYSTEM_MAP.md`, `docs/HARNESS_SHOWCASE.md`,
   `docs/SHOWCASE_FIXTURE_REFRESH.md`,
   `docs/PIPELINE_TAXONOMY.md`, `docs/PROJECT_LANGUAGE.md`,
   `docs/HARNESS_RUN_WALKTHROUGH.md`, `docs/HARNESS_IMPROVEMENT_LOOP.md`,
   `docs/ARTIFACT_INTERFACE_STANDARD.md`,
   `docs/HARNESS_ROADMAP.md`, `docs/HARNESS_READINESS.md`,
   `docs/HARNESS_READINESS_AUDIT.md`, `docs/PATTERN_REGISTER.md`,
   `docs/SKILL_AUDIT_SCHEMA.md`, `docs/DOCTOR_REPORT_SCHEMA.md`,
   `docs/RUN_AUDIT_SCHEMA.md`, `docs/RUN_AUDIT_DIFF_SCHEMA.md`,
   `docs/SHOWCASE_AUDIT_SCHEMA.md`, `docs/IMPROVEMENT_REPORT_SCHEMA.md`,
   `docs/ARTIFACT_PACK_SCHEMA.md`,
   and `docs/adr/`.
5. Run strict repo validation.
6. Run focused harness tests.
7. Run the WARN-level blocking skill audit:
   `python scripts/audit_skills.py --fail-on WARN`.
8. Confirm the `run-audit.v1` compatibility check still passes through the
   focused harness tests.
9. Confirm the `doctor-report.v1` compatibility check still passes through the
   focused harness tests.
10. Confirm the `harness-showcase-audit.v1` compatibility check still passes
    through the focused harness tests.
11. Inspect `docs/DOCTOR_REPORT_SCHEMA.md` if recovery consumers depend on the
   JSON sidecar.
12. Inspect `docs/RUN_AUDIT_SCHEMA.md` if audit consumers depend on the JSON
    sidecar.
13. Inspect `docs/RUN_AUDIT_DIFF_SCHEMA.md` if comparison consumers depend on
    audit diff JSON output.
14. Inspect `docs/SKILL_AUDIT_SCHEMA.md` if audit consumers depend on skill
    audit JSON output.
15. Inspect `docs/SHOWCASE_AUDIT_SCHEMA.md` if exhibit consumers depend on
    showcase audit JSON output.
16. Inspect `docs/IMPROVEMENT_REPORT_SCHEMA.md` if repair-map consumers depend
    on improvement report JSON output.
17. Inspect `docs/ARTIFACT_PACK_SCHEMA.md` if handoff or dashboard consumers
    depend on artifact-pack JSON output.
18. Confirm generated local files such as `uv.lock` are not left behind unless
    intentionally tracked.
19. Check that remaining roadmap items are explicitly deferred rather than
    silently missing.

Only after that audit should completion be considered. Passing this readiness
document alone is not enough.
