from __future__ import annotations


HARNESS_DOC_ENTRYPOINTS = {
    "docs/AUTO_RESEARCH_HARNESS.md": "auto research harness program",
    "docs/HARNESS_OPERATING_MODEL.md": "harness operating model",
    "docs/HARNESS_ARCHITECTURE.md": "harness architecture",
    "docs/HARNESS_SYSTEM_MAP.md": "harness system map",
    "docs/HARNESS_SHOWCASE.md": "harness showcase",
    "docs/SHOWCASE_FIXTURE_REFRESH.md": "showcase fixture refresh guide",
    "docs/HARNESS_RUN_WALKTHROUGH.md": "harness run walkthrough",
    "docs/HARNESS_IMPROVEMENT_LOOP.md": "harness improvement loop",
    "docs/ARTIFACT_INTERFACE_STANDARD.md": "artifact interface standard",
    "docs/PIPELINE_TAXONOMY.md": "pipeline taxonomy",
    "docs/PROJECT_LANGUAGE.md": "project language",
    "docs/HARNESS_ROADMAP.md": "harness roadmap",
    "docs/HARNESS_READINESS.md": "harness readiness",
    "docs/HARNESS_READINESS_AUDIT.md": "harness readiness audit",
    "docs/PATTERN_REGISTER.md": "external pattern register",
    "docs/SKILL_AUDIT_SCHEMA.md": "skill audit schema reference",
    "docs/DOCTOR_REPORT_SCHEMA.md": "doctor report schema reference",
    "docs/RUN_AUDIT_SCHEMA.md": "run-audit schema reference",
    "docs/RUN_AUDIT_DIFF_SCHEMA.md": "run-audit diff schema reference",
    "docs/SHOWCASE_AUDIT_SCHEMA.md": "showcase audit schema reference",
    "docs/IMPROVEMENT_REPORT_SCHEMA.md": "improvement report schema reference",
    "docs/ARTIFACT_PACK_SCHEMA.md": "artifact-pack schema reference",
    "docs/adr/README.md": "ADR index",
    "docs/adr/0001-separate-semantic-skills-from-deterministic-harness.md": "skills-vs-harness ADR",
    "docs/adr/0002-keep-run-audit-as-markdown-plus-json.md": "run-audit sidecar ADR",
    "docs/adr/0003-keep-doctor-report-as-markdown-plus-json.md": "doctor report sidecar ADR",
    "docs/adr/0004-keep-skill-audit-as-repo-local-json-before-sarif.md": "skill-audit JSON/SARIF ADR",
    "docs/adr/0005-keep-run-audit-diff-as-json-backed-comparison.md": "run-audit diff ADR",
    "docs/adr/0006-keep-showcase-audit-as-repo-local-json-contract.md": "showcase-audit JSON ADR",
    "docs/adr/0007-keep-improvement-report-as-a-local-repair-map.md": "improvement report ADR",
    "docs/adr/0008-keep-artifact-pack-as-manifest-before-archive.md": "artifact-pack manifest ADR",
}

HARNESS_README_LINKS = (
    "docs/AUTO_RESEARCH_HARNESS.md",
    "docs/HARNESS_OPERATING_MODEL.md",
    "docs/HARNESS_ARCHITECTURE.md",
    "docs/HARNESS_SYSTEM_MAP.md",
    "docs/HARNESS_SHOWCASE.md",
    "docs/SHOWCASE_FIXTURE_REFRESH.md",
    "docs/HARNESS_RUN_WALKTHROUGH.md",
    "docs/HARNESS_IMPROVEMENT_LOOP.md",
    "docs/ARTIFACT_INTERFACE_STANDARD.md",
    "docs/PIPELINE_TAXONOMY.md",
    "docs/PROJECT_LANGUAGE.md",
    "docs/HARNESS_ROADMAP.md",
    "docs/HARNESS_READINESS.md",
    "docs/HARNESS_READINESS_AUDIT.md",
    "docs/PATTERN_REGISTER.md",
    "docs/SKILL_AUDIT_SCHEMA.md",
    "docs/DOCTOR_REPORT_SCHEMA.md",
    "docs/RUN_AUDIT_SCHEMA.md",
    "docs/RUN_AUDIT_DIFF_SCHEMA.md",
    "docs/SHOWCASE_AUDIT_SCHEMA.md",
    "docs/IMPROVEMENT_REPORT_SCHEMA.md",
    "docs/ARTIFACT_PACK_SCHEMA.md",
    "docs/adr/",
)

SCHEMA_REFERENCE_DOCS = {
    "docs/SKILL_AUDIT_SCHEMA.md": {
        "schema": "skill-audit-report.v1",
        "json_output": "python scripts/audit_skills.py --format json",
        "producer": "scripts.audit_skills.build_report_payload",
        "validator": "scripts.audit_skills.validate_skill_audit_payload",
        "local_check": "python scripts/audit_skills.py --fail-on WARN",
        "adr": "docs/adr/0004-keep-skill-audit-as-repo-local-json-before-sarif.md",
    },
    "docs/DOCTOR_REPORT_SCHEMA.md": {
        "schema": "doctor-report.v1",
        "json_path": "output/DOCTOR_REPORT.json",
        "producer": "tooling.harness.build_doctor_payload",
        "validator": "tooling.harness.validate_doctor_payload",
        "adr": "docs/adr/0003-keep-doctor-report-as-markdown-plus-json.md",
    },
    "docs/RUN_AUDIT_SCHEMA.md": {
        "schema": "run-audit.v1",
        "json_path": "output/RUN_AUDIT.json",
        "producer": "tooling.harness.build_run_audit_payload",
        "validator": "tooling.harness.validate_run_audit_payload",
        "adr": "docs/adr/0002-keep-run-audit-as-markdown-plus-json.md",
    },
    "docs/RUN_AUDIT_DIFF_SCHEMA.md": {
        "schema": "run-audit-diff.v1",
        "json_path": "output/RUN_AUDIT_DIFF.json",
        "producer": "tooling.harness.build_run_audit_diff_payload",
        "validator": "tooling.harness.validate_run_audit_diff_payload",
        "adr": "docs/adr/0005-keep-run-audit-diff-as-json-backed-comparison.md",
    },
    "docs/SHOWCASE_AUDIT_SCHEMA.md": {
        "schema": "harness-showcase-audit.v1",
        "json_output": "python scripts/showcase_audit.py --format json",
        "producer": "scripts.showcase_audit.build_showcase_audit",
        "validator": "scripts.showcase_audit.validate_showcase_audit_payload",
        "local_check": "python scripts/showcase_audit.py --strict",
        "adr": "docs/adr/0006-keep-showcase-audit-as-repo-local-json-contract.md",
    },
    "docs/IMPROVEMENT_REPORT_SCHEMA.md": {
        "schema": "improvement-report.v1",
        "json_path": "output/IMPROVEMENT_REPORT.json",
        "producer": "tooling.harness.build_improvement_payload",
        "validator": "tooling.harness.validate_improvement_payload",
        "adr": "docs/adr/0007-keep-improvement-report-as-a-local-repair-map.md",
    },
    "docs/ARTIFACT_PACK_SCHEMA.md": {
        "schema": "artifact-pack.v1",
        "json_path": "output/ARTIFACT_PACK.json",
        "producer": "tooling.harness.build_artifact_pack_payload",
        "validator": "tooling.harness.validate_artifact_pack_payload",
        "adr": "docs/adr/0008-keep-artifact-pack-as-manifest-before-archive.md",
    },
}

ADR_ALLOWED_STATUSES = (
    "accepted",
    "deprecated",
    "superseded",
)

ADR_REQUIRED_METADATA = (
    "Status",
    "Date",
)

ADR_REQUIRED_SECTIONS = (
    "## Context",
    "## Decision",
    "## Consequences",
    "## Related Files",
)

PATTERN_REGISTER_REQUIRED_SECTIONS = (
    "## Pattern Map",
    "## Reference Codebases To Learn From",
    "## Adoption Rules",
    "## Source References",
)

PATTERN_REGISTER_REQUIRED_PATTERN_SOURCES = (
    "Temporal durable execution",
    "DVC pipelines",
    "Backstage software catalog",
    "OpenTelemetry semantic conventions",
    "LangGraph persistence",
    "Prefect flow/task split",
    "MADR/ADR templates",
    "JSON Schema-style compatibility",
    "SARIF static analysis interchange",
    "Evaluation harnesses and benchmark dashboards",
    "Database-backed run stores",
    "External workflow runtimes",
)

PATTERN_REGISTER_REQUIRED_REFERENCE_CODEBASES = (
    "| Temporal |",
    "| DVC |",
    "| Backstage |",
    "| OpenTelemetry |",
    "| LangGraph |",
    "| Prefect |",
    "| MADR/ADR templates |",
    "| JSON Schema |",
    "| SARIF/OASIS |",
)

PATTERN_REGISTER_REQUIRED_STATUSES = (
    "`Adopted`",
    "`Partial`",
    "`Deferred`",
)

PATTERN_REGISTER_REQUIRED_ADOPTION_RULES = (
    "Borrow the discipline, not the runtime",
    "Map every adopted idea to a real file, command, test, or artifact",
    "If adoption changes a repo-level contract, record the decision as an ADR",
)

ARTIFACT_INTERFACE_REQUIRED_SECTIONS = (
    "## Interface Thesis",
    "## Required Interface Fields",
    "## Format Selection",
    "## Current Repo Mappings",
    "## Repair Protocol",
    "## Anti-Patterns",
    "## Extension Rule",
)

ARTIFACT_INTERFACE_REQUIRED_FIELDS = (
    "`artifact_path`",
    "`producer`",
    "`consumer`",
    "`format`",
    "`human_view`",
    "`machine_view`",
    "`trace_keys`",
    "`repair_surface`",
    "`validation`",
    "`visibility`",
)

ARTIFACT_INTERFACE_REQUIRED_FORMATS = (
    "Markdown",
    "CSV",
    "TSV",
    "YAML",
    "Versioned JSON",
    "PDF",
    "TeX",
    "SVG",
)

ARTIFACT_INTERFACE_REQUIRED_MAPPINGS = (
    "Workflow protocol",
    "Execution ledger",
    "Workspace diagnosis",
    "Run audit",
    "Audit comparison",
    "Skill hygiene",
    "Showcase",
    "Artifact pack",
    "Learning layer",
)

HARNESS_RUN_WALKTHROUGH_REQUIRED_TERMS = (
    "python scripts/pipeline.py kickoff",
    "python scripts/pipeline.py doctor --workspace",
    "python scripts/pipeline.py audit --workspace",
    "python scripts/pipeline.py improve --workspace",
    "python scripts/pipeline.py pack --workspace",
    "output/DOCTOR_REPORT.json",
    "output/RUN_AUDIT.json",
    "output/IMPROVEMENT_REPORT.json",
    "output/ARTIFACT_PACK.json",
    "doctor-report.v1",
    "run-audit.v1",
    "improvement-report.v1",
    "artifact-pack.v1",
)

HARNESS_SKILL_AUDIT_GATE = "python scripts/audit_skills.py --fail-on WARN"
HARNESS_READINESS_AUDIT_SCRIPT = "scripts/readiness_audit.py"
HARNESS_SHOWCASE_AUDIT_SCRIPT = "scripts/showcase_audit.py"
HARNESS_SHOWCASE_AUDIT_GATE = "python scripts/showcase_audit.py --strict"
HARNESS_LOCAL_CHECKS = (
    HARNESS_SKILL_AUDIT_GATE,
    HARNESS_SHOWCASE_AUDIT_GATE,
)

SHOWCASE_FIXTURE_REFRESH_REQUIRED_TERMS = (
    "Refresh Boundary",
    "workspaces/",
    "example/",
    'WS=workspaces/<completed-workspace>',
    'python scripts/pipeline.py doctor --workspace "$WS" --write',
    'python scripts/pipeline.py audit --workspace "$WS" --write',
    'python scripts/pipeline.py improve --workspace "$WS" --write',
    'python scripts/pipeline.py pack --workspace "$WS" --write --write-excerpt',
    "ARTIFACT_PACK_EXCERPT.md",
    "ARTIFACT_PACK_EXCERPT.tsv",
    "docs/HARNESS_SHOWCASE.md",
    "docs/ARTIFACT_PACK_SCHEMA.md",
    "docs/SHOWCASE_AUDIT_SCHEMA.md",
    "python scripts/showcase_audit.py --strict",
    "python scripts/showcase_audit.py --format json",
    "python scripts/validate_repo.py --no-check-quality --strict",
)

READINESS_AUDIT_SCHEMA = "harness-readiness-audit.v1"
READINESS_PROGRESS_PATH = "workspaces/harness-upgrade/GOAL_STATUS.md"
READINESS_MIN_ITERATIONS = 10

READINESS_REQUIRED_DOCS = (
    "README.md",
    "README.zh-CN.md",
    "docs/AUTO_RESEARCH_HARNESS.md",
    "docs/HARNESS_OPERATING_MODEL.md",
    "docs/HARNESS_ARCHITECTURE.md",
    "docs/HARNESS_SYSTEM_MAP.md",
    "docs/HARNESS_SHOWCASE.md",
    "docs/SHOWCASE_FIXTURE_REFRESH.md",
    "docs/HARNESS_RUN_WALKTHROUGH.md",
    "docs/HARNESS_IMPROVEMENT_LOOP.md",
    "docs/ARTIFACT_INTERFACE_STANDARD.md",
    "docs/PIPELINE_TAXONOMY.md",
    "docs/PROJECT_LANGUAGE.md",
    "docs/HARNESS_ROADMAP.md",
    "docs/HARNESS_READINESS.md",
    "docs/HARNESS_READINESS_AUDIT.md",
    "docs/PATTERN_REGISTER.md",
    "docs/SKILL_AUDIT_SCHEMA.md",
    "docs/DOCTOR_REPORT_SCHEMA.md",
    "docs/RUN_AUDIT_SCHEMA.md",
    "docs/RUN_AUDIT_DIFF_SCHEMA.md",
    "docs/SHOWCASE_AUDIT_SCHEMA.md",
    "docs/IMPROVEMENT_REPORT_SCHEMA.md",
    "docs/ARTIFACT_PACK_SCHEMA.md",
    "docs/adr/README.md",
)

CURRENT_WORKFLOWS = (
    "arxiv-survey",
    "arxiv-survey-latex",
    "research-brief",
    "paper-review",
    "evidence-review",
    "idea-brainstorm",
    "source-tutorial",
    "graduate-paper",
)

EXECUTABLE_PIPELINE_CONTRACTS = (
    "pipelines/arxiv-survey.pipeline.md",
    "pipelines/arxiv-survey-latex.pipeline.md",
    "pipelines/research-brief.pipeline.md",
    "pipelines/paper-review.pipeline.md",
    "pipelines/evidence-review.pipeline.md",
    "pipelines/idea-brainstorm.pipeline.md",
    "pipelines/source-tutorial.pipeline.md",
)

EXECUTABLE_UNIT_TEMPLATES = (
    "templates/UNITS.arxiv-survey.csv",
    "templates/UNITS.arxiv-survey-latex.csv",
    "templates/UNITS.research-brief.csv",
    "templates/UNITS.paper-review.csv",
    "templates/UNITS.evidence-review.csv",
    "templates/UNITS.idea-brainstorm.csv",
    "templates/UNITS.source-tutorial.csv",
)

READINESS_VALIDATION_SURFACES = (
    "scripts/validate_repo.py",
    "scripts/audit_skills.py",
    "scripts/pipeline.py",
    "scripts/generate_skill_graph.py",
    "scripts/readiness_audit.py",
    "scripts/showcase_audit.py",
    "tooling/harness_contracts.py",
    "tests/test_harness_smoke.py",
    "tests/test_harness_validation.py",
    "tests/test_pipeline_harness_doctor.py",
)

HARNESS_SHOWCASE_FIXTURE_PATHS = (
    "example/research-brief/rag-evaluation-harness-demo/README.md",
    "example/research-brief/rag-evaluation-harness-demo/output/SNAPSHOT.md",
    "example/research-brief/rag-evaluation-harness-demo/outline/outline.yml",
    "example/research-brief/rag-evaluation-harness-demo/outline/taxonomy.yml",
    "example/research-brief/rag-evaluation-harness-demo/papers/core_set.csv",
    "example/research-brief/rag-evaluation-harness-demo/output/DELIVERABLE_SELFLOOP_TODO.md",
    "example/research-brief/rag-evaluation-harness-demo/output/CONTRACT_REPORT.md",
    "example/research-brief/rag-evaluation-harness-demo/output/ARTIFACT_PACK_EXCERPT.md",
    "example/research-brief/rag-evaluation-harness-demo/output/ARTIFACT_PACK_EXCERPT.tsv",
    "example/source-tutorial/robot-learning-harness-demo/README.md",
    "example/source-tutorial/robot-learning-harness-demo/output/TUTORIAL_EXCERPT.md",
    "example/source-tutorial/robot-learning-harness-demo/output/TUTORIAL_SPEC_EXCERPT.md",
    "example/source-tutorial/robot-learning-harness-demo/outline/module_plan.yml",
    "example/source-tutorial/robot-learning-harness-demo/sources/manifest.summary.yml",
    "example/source-tutorial/robot-learning-harness-demo/evidence/TUTORIAL_SELFLOOP.md",
    "example/source-tutorial/robot-learning-harness-demo/evidence/DELIVERY_EVIDENCE.md",
    "example/source-tutorial/robot-learning-harness-demo/evidence/CONTRACT_REPORT.md",
    "example/source-tutorial/robot-learning-harness-demo/evidence/RUN_AUDIT_SUMMARY.md",
    "example/source-tutorial/robot-learning-harness-demo/evidence/ARTIFACT_PACK_EXCERPT.md",
    "example/source-tutorial/robot-learning-harness-demo/evidence/ARTIFACT_PACK_EXCERPT.tsv",
)

HARNESS_SHOWCASE_ASSET_PATHS = (
    "docs/assets/harness-showcase-lineage.svg",
)

AUTO_RESEARCH_REQUIRED_TERMS = (
    "Auto Research",
    "protocolizes work",
    "externalizes state",
    "audits evidence",
    "reusable project knowledge",
    "Abstract Layer Versus Implementation Layer",
)
