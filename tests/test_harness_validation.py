from __future__ import annotations

import json
from pathlib import Path

import scripts.audit_skills as audit_skills
import scripts.generate_skill_graph as generate_skill_graph
import scripts.readiness_audit as readiness_audit
import scripts.showcase_audit as showcase_audit
import scripts.validate_repo as validate_repo
import tooling.harness_contracts as harness_contracts


def _write_minimal_harness_docs(repo_root: Path) -> None:
    docs_dir = repo_root / "docs"
    adr_dir = docs_dir / "adr"
    scripts_dir = repo_root / "scripts"
    adr_dir.mkdir(parents=True)
    scripts_dir.mkdir(parents=True)
    (docs_dir / "HARNESS_ARCHITECTURE.md").write_text(
        "See docs/AUTO_RESEARCH_HARNESS.md, docs/HARNESS_OPERATING_MODEL.md, "
        "docs/PIPELINE_TAXONOMY.md, docs/PROJECT_LANGUAGE.md, "
        "docs/HARNESS_ROADMAP.md, docs/HARNESS_READINESS.md, "
        "docs/HARNESS_READINESS_AUDIT.md, docs/PATTERN_REGISTER.md, "
        "docs/HARNESS_SYSTEM_MAP.md, docs/HARNESS_SHOWCASE.md, docs/HARNESS_RUN_WALKTHROUGH.md, "
        "docs/HARNESS_IMPROVEMENT_LOOP.md, "
        "docs/SKILL_AUDIT_SCHEMA.md, docs/DOCTOR_REPORT_SCHEMA.md, "
        "docs/RUN_AUDIT_SCHEMA.md, docs/RUN_AUDIT_DIFF_SCHEMA.md, "
        "and docs/SHOWCASE_AUDIT_SCHEMA.md.\n",
        encoding="utf-8",
    )
    (docs_dir / "HARNESS_OPERATING_MODEL.md").write_text("# Harness Operating Model\n", encoding="utf-8")
    (docs_dir / "HARNESS_SYSTEM_MAP.md").write_text("# Harness System Map\n", encoding="utf-8")
    (docs_dir / "HARNESS_SHOWCASE.md").write_text("# Harness Showcase\n", encoding="utf-8")
    (docs_dir / "HARNESS_RUN_WALKTHROUGH.md").write_text("# Harness Run Walkthrough\n", encoding="utf-8")
    (docs_dir / "HARNESS_IMPROVEMENT_LOOP.md").write_text("# Harness Improvement Loop\n", encoding="utf-8")
    (docs_dir / "AUTO_RESEARCH_HARNESS.md").write_text(
        "\n".join(validate_repo.AUTO_RESEARCH_REQUIRED_TERMS) + "\n",
        encoding="utf-8",
    )
    (docs_dir / "PIPELINE_TAXONOMY.md").write_text("# Pipeline Taxonomy\n", encoding="utf-8")
    (docs_dir / "PROJECT_LANGUAGE.md").write_text("# Project Language\n", encoding="utf-8")
    (docs_dir / "HARNESS_ROADMAP.md").write_text("# Harness Roadmap\n", encoding="utf-8")
    (docs_dir / "HARNESS_READINESS.md").write_text(
        "# Harness Readiness\n\n" + "\n".join(validate_repo.HARNESS_LOCAL_CHECKS) + "\n",
        encoding="utf-8",
    )
    (docs_dir / "HARNESS_READINESS_AUDIT.md").write_text(
        "harness-readiness-audit.v1\npython scripts/readiness_audit.py\ndocs/HARNESS_READINESS.md\n",
        encoding="utf-8",
    )
    (docs_dir / "PATTERN_REGISTER.md").write_text(
        "\n".join(
            [
                "# Pattern Register",
                "",
                "## Pattern Map",
                "",
                *validate_repo.PATTERN_REGISTER_REQUIRED_PATTERN_SOURCES,
                *validate_repo.PATTERN_REGISTER_REQUIRED_STATUSES,
                "",
                "## Reference Codebases To Learn From",
                "",
                *validate_repo.PATTERN_REGISTER_REQUIRED_REFERENCE_CODEBASES,
                "",
                "## Adoption Rules",
                "",
                *validate_repo.PATTERN_REGISTER_REQUIRED_ADOPTION_RULES,
                "",
                "## Source References",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (docs_dir / "DOCTOR_REPORT_SCHEMA.md").write_text(
        "\n".join(validate_repo.SCHEMA_REFERENCE_DOCS["docs/DOCTOR_REPORT_SCHEMA.md"].values()) + "\n",
        encoding="utf-8",
    )
    (docs_dir / "RUN_AUDIT_SCHEMA.md").write_text(
        "\n".join(validate_repo.SCHEMA_REFERENCE_DOCS["docs/RUN_AUDIT_SCHEMA.md"].values()) + "\n",
        encoding="utf-8",
    )
    (docs_dir / "RUN_AUDIT_DIFF_SCHEMA.md").write_text(
        "\n".join(validate_repo.SCHEMA_REFERENCE_DOCS["docs/RUN_AUDIT_DIFF_SCHEMA.md"].values()) + "\n",
        encoding="utf-8",
    )
    (docs_dir / "SKILL_AUDIT_SCHEMA.md").write_text(
        "\n".join(validate_repo.SCHEMA_REFERENCE_DOCS["docs/SKILL_AUDIT_SCHEMA.md"].values()) + "\n",
        encoding="utf-8",
    )
    (docs_dir / "SHOWCASE_AUDIT_SCHEMA.md").write_text(
        "\n".join(validate_repo.SCHEMA_REFERENCE_DOCS["docs/SHOWCASE_AUDIT_SCHEMA.md"].values()) + "\n",
        encoding="utf-8",
    )
    adr_files = [
        Path(rel_path).name
        for rel_path in validate_repo.HARNESS_DOC_ENTRYPOINTS
        if rel_path.startswith("docs/adr/") and rel_path != "docs/adr/README.md"
    ]
    for adr_file in adr_files:
        (adr_dir / adr_file).write_text(_minimal_adr(adr_file[:4]), encoding="utf-8")
    (adr_dir / "README.md").write_text(
        "\n".join(
            [
                "# ADR Index",
                "",
                *[f"- [{adr_file[:4]}]({adr_file})" for adr_file in adr_files],
                "",
            ]
        ),
        encoding="utf-8",
    )
    (scripts_dir / "readiness_audit.py").write_text("# readiness audit placeholder\n", encoding="utf-8")
    (scripts_dir / "showcase_audit.py").write_text("# showcase audit placeholder\n", encoding="utf-8")
    for rel_path in validate_repo.HARNESS_SHOWCASE_ASSET_PATHS:
        asset_path = repo_root / rel_path
        asset_path.parent.mkdir(parents=True, exist_ok=True)
        asset_path.write_text("<svg></svg>\n", encoding="utf-8")
    for rel_path in validate_repo.HARNESS_SHOWCASE_FIXTURE_PATHS:
        fixture_path = repo_root / rel_path
        fixture_path.parent.mkdir(parents=True, exist_ok=True)
        fixture_path.write_text(f"{rel_path}\n", encoding="utf-8")
    (docs_dir / "HARNESS_SHOWCASE.md").write_text(
        "\n".join(
            validate_repo.HARNESS_SHOWCASE_ASSET_PATHS
            + validate_repo.HARNESS_SHOWCASE_FIXTURE_PATHS
            + (
                "harness-showcase-audit.v1",
                "python scripts/showcase_audit.py --strict",
            )
        )
        + "\n",
        encoding="utf-8",
    )


def _write_minimal_showcase_audit_repo(repo_root: Path) -> None:
    doc_path = repo_root / showcase_audit.SHOWCASE_DOC
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text(
        "\n".join(
            showcase_audit.HARNESS_SHOWCASE_ASSET_PATHS
            + showcase_audit.HARNESS_SHOWCASE_FIXTURE_PATHS
            + showcase_audit.PIPELINE_PROTOCOLS
            + (
                showcase_audit.SCHEMA,
                "python scripts/showcase_audit.py --strict",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    for rel_path in showcase_audit.HARNESS_SHOWCASE_ASSET_PATHS:
        path = repo_root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "<svg><title>Harness Showcase Lineage</title>"
            "<text>Research-Brief Fixture</text><text>Source-Tutorial Fixture</text></svg>\n",
            encoding="utf-8",
        )
    for rel_path in showcase_audit.PIPELINE_PROTOCOLS:
        path = repo_root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {rel_path}\n", encoding="utf-8")
    for rel_path in showcase_audit.HARNESS_SHOWCASE_FIXTURE_PATHS:
        path = repo_root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{rel_path}\n", encoding="utf-8")

    research_root = repo_root / showcase_audit.RESEARCH_BRIEF_ROOT
    (research_root / "output" / "SNAPSHOT.md").write_text(
        "# Snapshot: RAG Evaluation\n\nHarness Implication\n",
        encoding="utf-8",
    )
    (research_root / "output" / "DELIVERABLE_SELFLOOP_TODO.md").write_text(
        "Status: PASS\n",
        encoding="utf-8",
    )
    (research_root / "output" / "CONTRACT_REPORT.md").write_text(
        "Status: PASS\n",
        encoding="utf-8",
    )

    tutorial_root = repo_root / showcase_audit.SOURCE_TUTORIAL_ROOT
    (tutorial_root / "output" / "TUTORIAL_EXCERPT.md").write_text(
        "# A Source-Grounded Introduction to Robot Learning\n",
        encoding="utf-8",
    )
    (tutorial_root / "output" / "TUTORIAL_SPEC_EXCERPT.md").write_text(
        "Learning Objectives\n",
        encoding="utf-8",
    )
    (tutorial_root / "evidence" / "TUTORIAL_SELFLOOP.md").write_text(
        "Status: PASS\n",
        encoding="utf-8",
    )
    (tutorial_root / "evidence" / "DELIVERY_EVIDENCE.md").write_text(
        "`latex/main.pdf`\n`latex/slides/main.pdf`\n",
        encoding="utf-8",
    )
    (tutorial_root / "evidence" / "CONTRACT_REPORT.md").write_text(
        "Status: PASS\n",
        encoding="utf-8",
    )
    (tutorial_root / "evidence" / "RUN_AUDIT_SUMMARY.md").write_text(
        "Audit verdict: PASS\n",
        encoding="utf-8",
    )


def _readme_with_harness_links() -> str:
    return "\n".join(validate_repo.HARNESS_README_LINKS) + "\n"


def _minimal_adr(number: str, title: str = "Example Decision") -> str:
    return f"""# ADR {number}: {title}

- Status: accepted
- Date: 2026-05-30

## Context

Context.

## Decision

Decision.

## Consequences

Consequences.

## Related Files

- `docs/adr/README.md`
"""


def _write_minimal_pipeline(path: Path, *, name: str, units_template: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
name: {name}
version: 1.0
units_template: {units_template}
target_artifacts: [output/demo.md]
default_checkpoints: [C0]
stages:
  C0:
    title: Init
    checkpoint: C0
    mode: no_prose
    required_skills: [demo-skill]
    optional_skills: []
    produces: [output/demo.md]
---

# Pipeline: {name}
""",
        encoding="utf-8",
    )


def test_skill_local_references_and_assets_are_not_workspace_artifacts() -> None:
    body = """
## Inputs

- `outline/table_schema.md`
- `references/table_cell_hygiene.md`
- `assets/table_cell_hygiene.json`
- Optional: `GOAL.md`

## Output

- `outline/tables_appendix.md`
"""

    validate_inputs, validate_outputs = validate_repo._parse_inputs_outputs(body)
    graph_inputs, graph_outputs = generate_skill_graph._parse_inputs_outputs(body)

    assert validate_inputs == {"GOAL.md", "outline/table_schema.md"}
    assert validate_outputs == {"outline/tables_appendix.md"}
    assert graph_inputs == validate_inputs
    assert graph_outputs == validate_outputs


def test_current_harness_docs_are_valid_entrypoints() -> None:
    findings = validate_repo._validate_harness_docs(
        repo_root=validate_repo.REPO_ROOT,
        docs_dir=validate_repo.DOCS_DIR,
    )

    assert findings == []


def test_readiness_audit_and_repo_validation_share_harness_contracts() -> None:
    assert validate_repo.HARNESS_README_LINKS is harness_contracts.HARNESS_README_LINKS
    assert readiness_audit.README_LINKS is harness_contracts.HARNESS_README_LINKS
    assert validate_repo.HARNESS_LOCAL_CHECKS is harness_contracts.HARNESS_LOCAL_CHECKS
    assert readiness_audit.LOCAL_CHECKS is harness_contracts.HARNESS_LOCAL_CHECKS
    assert validate_repo.HARNESS_SKILL_AUDIT_GATE == readiness_audit.SKILL_AUDIT_GATE
    assert validate_repo.HARNESS_SHOWCASE_AUDIT_GATE == readiness_audit.SHOWCASE_AUDIT_GATE
    assert "tooling/harness_contracts.py" in readiness_audit.VALIDATION_SURFACES
    assert "scripts/showcase_audit.py" in readiness_audit.VALIDATION_SURFACES


def test_harness_docs_validation_reports_missing_readme_links(tmp_path: Path) -> None:
    _write_minimal_harness_docs(tmp_path)
    (tmp_path / "README.md").write_text("docs/HARNESS_ARCHITECTURE.md\n", encoding="utf-8")
    (tmp_path / "README.zh-CN.md").write_text(_readme_with_harness_links(), encoding="utf-8")

    findings = validate_repo._validate_harness_docs(repo_root=tmp_path, docs_dir=tmp_path / "docs")

    assert [(item.level, item.message) for item in findings] == [
        (
            "WARN",
            "`README.md` is missing harness docs links: "
            "docs/AUTO_RESEARCH_HARNESS.md, docs/HARNESS_OPERATING_MODEL.md, "
            "docs/HARNESS_SYSTEM_MAP.md, docs/HARNESS_SHOWCASE.md, docs/HARNESS_RUN_WALKTHROUGH.md, "
            "docs/HARNESS_IMPROVEMENT_LOOP.md, "
            "docs/PIPELINE_TAXONOMY.md, docs/PROJECT_LANGUAGE.md, "
            "docs/HARNESS_ROADMAP.md, docs/HARNESS_READINESS.md, "
            "docs/HARNESS_READINESS_AUDIT.md, docs/PATTERN_REGISTER.md, "
            "docs/SKILL_AUDIT_SCHEMA.md, docs/DOCTOR_REPORT_SCHEMA.md, "
            "docs/RUN_AUDIT_SCHEMA.md, docs/RUN_AUDIT_DIFF_SCHEMA.md, "
            "docs/SHOWCASE_AUDIT_SCHEMA.md, docs/adr/.",
        )
    ]


def test_harness_docs_validation_reports_missing_local_harness_check(tmp_path: Path) -> None:
    _write_minimal_harness_docs(tmp_path)
    (tmp_path / "README.md").write_text(_readme_with_harness_links(), encoding="utf-8")
    (tmp_path / "README.zh-CN.md").write_text(_readme_with_harness_links(), encoding="utf-8")
    (tmp_path / "docs" / "HARNESS_READINESS.md").write_text(
        f"# Harness Readiness\n\n{validate_repo.HARNESS_SHOWCASE_AUDIT_GATE}\n",
        encoding="utf-8",
    )

    findings = validate_repo._validate_harness_docs(repo_root=tmp_path, docs_dir=tmp_path / "docs")

    assert [(item.level, item.message) for item in findings] == [
        (
            "WARN",
            "`docs/HARNESS_READINESS.md` should list local harness checks: "
            "`python scripts/audit_skills.py --fail-on WARN`.",
        )
    ]


def test_harness_docs_validation_reports_missing_readiness_audit_metadata(tmp_path: Path) -> None:
    _write_minimal_harness_docs(tmp_path)
    (tmp_path / "README.md").write_text(_readme_with_harness_links(), encoding="utf-8")
    (tmp_path / "README.zh-CN.md").write_text(_readme_with_harness_links(), encoding="utf-8")
    (tmp_path / "docs" / "HARNESS_READINESS_AUDIT.md").write_text(
        "# Harness Readiness Audit\n",
        encoding="utf-8",
    )

    findings = validate_repo._validate_harness_docs(repo_root=tmp_path, docs_dir=tmp_path / "docs")

    assert [(item.level, item.message) for item in findings] == [
        (
            "WARN",
            "`docs/HARNESS_READINESS_AUDIT.md` is missing readiness audit metadata: "
            "`harness-readiness-audit.v1`, `python scripts/readiness_audit.py`, "
            "`docs/HARNESS_READINESS.md`.",
        )
    ]


def test_readiness_audit_parses_iteration_progress() -> None:
    assert readiness_audit.parse_iteration_progress("- Iterations completed: 20 of at least 10\n") == (20, 10)
    assert readiness_audit.parse_iteration_progress("no count here") is None


def test_pipeline_taxonomy_validation_reports_missing_executable_metadata(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    _write_minimal_pipeline(
        tmp_path / "pipelines" / "demo.pipeline.md",
        name="demo",
        units_template="templates/UNITS.demo.csv",
    )
    (docs_dir / "PIPELINE_TAXONOMY.md").write_text("# Pipeline Taxonomy\n", encoding="utf-8")

    findings = validate_repo._validate_pipeline_taxonomy(
        repo_root=tmp_path,
        pipelines_dir=tmp_path / "pipelines",
        docs_dir=docs_dir,
    )

    assert [(item.level, item.message) for item in findings] == [
        (
            "WARN",
            "`docs/PIPELINE_TAXONOMY.md` is missing executable pipeline metadata for "
            "`demo`: pipeline name `demo`, contract path `pipelines/demo.pipeline.md`, "
            "unit template `templates/UNITS.demo.csv`.",
        )
    ]


def test_pipeline_taxonomy_validation_reports_graduate_paper_maturity_drift(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    pipelines_dir = tmp_path / "pipelines"
    pipelines_dir.mkdir()
    (pipelines_dir / "graduate-paper-pipeline.md").write_text(
        "# Pipeline: graduate-paper\n",
        encoding="utf-8",
    )
    (docs_dir / "PIPELINE_TAXONOMY.md").write_text(
        "`graduate-paper`\n`pipelines/graduate-paper-pipeline.md`\n",
        encoding="utf-8",
    )

    findings = validate_repo._validate_pipeline_taxonomy(
        repo_root=tmp_path,
        pipelines_dir=pipelines_dir,
        docs_dir=docs_dir,
    )

    assert [(item.level, item.message) for item in findings] == [
        (
            "WARN",
            "`docs/PIPELINE_TAXONOMY.md` is missing graduate-paper research-stage metadata: "
            "research-stage maturity `Research-stage`, missing unit template marker Unit template: none yet.",
        )
    ]


def test_adr_index_validation_reports_missing_and_dangling_entries(tmp_path: Path) -> None:
    adr_dir = tmp_path / "docs" / "adr"
    adr_dir.mkdir(parents=True)
    (adr_dir / "0001-first-decision.md").write_text(_minimal_adr("0001"), encoding="utf-8")
    (adr_dir / "0002-second-decision.md").write_text(_minimal_adr("0002"), encoding="utf-8")
    (adr_dir / "README.md").write_text(
        "- [0001](0001-first-decision.md)\n"
        "- [9999](9999-missing-decision.md)\n",
        encoding="utf-8",
    )

    findings = validate_repo._validate_adr_index(repo_root=tmp_path, docs_dir=tmp_path / "docs")

    assert [(item.level, item.message) for item in findings] == [
        (
            "WARN",
            "`docs/adr/README.md` is missing ADR index entry for `docs/adr/0002-second-decision.md`.",
        ),
        (
            "WARN",
            "`docs/adr/README.md` links missing ADR file `9999-missing-decision.md`.",
        ),
    ]


def test_adr_contract_validation_reports_missing_metadata(tmp_path: Path) -> None:
    adr_dir = tmp_path / "docs" / "adr"
    adr_dir.mkdir(parents=True)
    (adr_dir / "0001-first-decision.md").write_text(
        "# Decision\n\nStatus: proposed\n\n## Decision\n\nDecision.\n",
        encoding="utf-8",
    )

    findings = validate_repo._validate_adr_contracts(repo_root=tmp_path, docs_dir=tmp_path / "docs")

    assert [(item.level, item.message) for item in findings] == [
        (
            "WARN",
            "`docs/adr/0001-first-decision.md` has unsupported ADR status `proposed`; "
            "expected one of accepted, deprecated, superseded.",
        ),
        (
            "WARN",
            "`docs/adr/0001-first-decision.md` is missing ADR contract metadata: "
            "title `# ADR 0001: ...`, metadata `Date`, section `## Context`, "
            "section `## Consequences`, section `## Related Files`.",
        ),
    ]


def test_schema_reference_validation_reports_missing_metadata(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "DOCTOR_REPORT_SCHEMA.md").write_text("doctor-report.v1\n", encoding="utf-8")
    (docs_dir / "RUN_AUDIT_SCHEMA.md").write_text(
        "\n".join(validate_repo.SCHEMA_REFERENCE_DOCS["docs/RUN_AUDIT_SCHEMA.md"].values()) + "\n",
        encoding="utf-8",
    )

    findings = validate_repo._validate_schema_reference_docs(repo_root=tmp_path)

    assert [(item.level, item.message) for item in findings] == [
        (
            "WARN",
            "`docs/DOCTOR_REPORT_SCHEMA.md` is missing schema reference metadata: "
            "json_path `output/DOCTOR_REPORT.json`, "
            "producer `tooling.harness.build_doctor_payload`, "
            "validator `tooling.harness.validate_doctor_payload`, "
            "adr `docs/adr/0003-keep-doctor-report-as-markdown-plus-json.md`.",
        )
    ]


def test_pattern_register_validation_reports_missing_contract_metadata(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "PATTERN_REGISTER.md").write_text(
        "# Pattern Register\n\n## Pattern Map\n\nTemporal\n",
        encoding="utf-8",
    )

    findings = validate_repo._validate_pattern_register(repo_root=tmp_path)

    assert len(findings) == 1
    assert findings[0].level == "WARN"
    assert "`docs/PATTERN_REGISTER.md` is missing pattern-register contract metadata" in findings[0].message
    assert "reference codebases" in findings[0].message
    assert "DVC" in findings[0].message
    assert "adoption rules" in findings[0].message


def test_auto_research_harness_validation_reports_missing_framing(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "AUTO_RESEARCH_HARNESS.md").write_text(
        "# Auto Research Harness\n\nA short placeholder.\n",
        encoding="utf-8",
    )

    findings = validate_repo._validate_auto_research_harness_doc(repo_root=tmp_path)

    assert [(item.level, item.message) for item in findings] == [
        (
            "WARN",
            "`docs/AUTO_RESEARCH_HARNESS.md` is missing Auto Research Harness framing terms: "
            "`protocolizes work`, `externalizes state`, `audits evidence`, "
            "`reusable project knowledge`, `Abstract Layer Versus Implementation Layer`.",
        )
    ]


def test_harness_showcase_validation_reports_missing_fixture_evidence(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "HARNESS_SHOWCASE.md").write_text(
        "example/research-brief/rag-evaluation-harness-demo/output/SNAPSHOT.md\n",
        encoding="utf-8",
    )

    findings = validate_repo._validate_harness_showcase(repo_root=tmp_path)

    assert len(findings) == 1
    assert findings[0].level == "WARN"
    assert "`docs/HARNESS_SHOWCASE.md` is missing deliverable-first showcase evidence" in findings[0].message
    assert "example/research-brief/rag-evaluation-harness-demo/README.md" in findings[0].message
    assert "fixture paths" in findings[0].message


def test_showcase_audit_current_repo_passes() -> None:
    payload = showcase_audit.build_showcase_audit(repo_root=showcase_audit.REPO_ROOT)

    assert payload["schema"] == "harness-showcase-audit.v1"
    assert payload["verdict"] == "PASS"
    assert showcase_audit.validate_showcase_audit_payload(payload) == []
    assert {item["id"] for item in payload["checks"]} == {
        "showcase_doc",
        "lineage_assets",
        "pipeline_protocols",
        "research_brief_fixture",
        "source_tutorial_fixture",
    }


def test_showcase_audit_reports_placeholder_deliverable(tmp_path: Path) -> None:
    _write_minimal_showcase_audit_repo(tmp_path)
    snapshot = tmp_path / showcase_audit.RESEARCH_BRIEF_ROOT / "output" / "SNAPSHOT.md"
    snapshot.write_text(
        "# Snapshot: RAG Evaluation\n\nPlaceholder text.\n\nHarness Implication\n",
        encoding="utf-8",
    )

    payload = showcase_audit.build_showcase_audit(repo_root=tmp_path)

    assert payload["verdict"] == "ATTENTION"
    finding = next(item for item in payload["checks"] if item["id"] == "research_brief_fixture")
    assert finding["status"] == "WARN"
    assert "placeholder content" in finding["evidence"]


def test_showcase_audit_payload_validation_reports_shape_errors() -> None:
    issues = showcase_audit.validate_showcase_audit_payload(
        {
            "schema": "old-schema",
            "repo": 1,
            "verdict": "MAYBE",
            "showcase_doc": None,
            "note": [],
            "checks": [
                {
                    "id": 1,
                    "status": "MAYBE",
                    "evidence": [],
                    "next_action": None,
                }
            ],
        }
    )

    assert "`schema` must be `harness-showcase-audit.v1`." in issues
    assert "`repo` must be a string." in issues
    assert "`verdict` must be `PASS` or `ATTENTION`." in issues
    assert "`checks[0].status` must be `PASS` or `WARN`." in issues
    assert "`checks[0].next_action` must be a string." in issues


def test_reference_examples_with_ellipsis_are_informational_not_warnings(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(audit_skills, "REPO_ROOT", tmp_path)
    skills_dir = tmp_path / ".codex" / "skills"
    ref_path = skills_dir / "demo" / "references" / "examples.md"
    ref_path.parent.mkdir(parents=True)
    ref_path.write_text("- Bad example: `we propose ...`\n", encoding="utf-8")

    findings = audit_skills._audit_text_file("demo", ref_path, skills_dir)

    assert [(item.severity, item.rule_id) for item in findings] == [
        ("INFO", "reader_facing_ellipsis")
    ]
    assert findings[0].review_category == "reference_example_phrase"
    assert "promote to WARN" in findings[0].next_action


def test_reader_facing_ellipsis_info_categories_are_split(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(audit_skills, "REPO_ROOT", tmp_path)
    skills_dir = tmp_path / ".codex" / "skills"
    skill_dir = skills_dir / "demo"
    cases = [
        (
            skill_dir / "SKILL.md",
            "- `--inputs <a;b;...>`\n",
            "syntax_placeholder",
        ),
        (
            skill_dir / "assets" / "voice_palette.json",
            '"smell": "Outline narration (This subsection...)"\n',
            "asset_palette_reference",
        ),
        (
            skill_dir / "policy.md",
            "- No placeholders: no `TODO`, `...`, or `(placeholder)`.\n",
            "placeholder_policy",
        ),
        (
            skill_dir / "guidance.md",
            "- Avoid `This subsection ...` in generated prose.\n",
            "anti_pattern_guidance",
        ),
    ]
    for path, text, _category in cases:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    findings = []
    for path, _text, _category in cases:
        findings.extend(audit_skills._audit_text_file("demo", path, skills_dir))

    assert [(item.path, item.review_category) for item in findings] == [
        (path.relative_to(tmp_path).as_posix(), category)
        for path, _text, category in cases
    ]


def test_script_diagnostic_ellipsis_examples_are_not_warnings(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(audit_skills, "REPO_ROOT", tmp_path)
    skills_dir = tmp_path / ".codex" / "skills"
    script_path = skills_dir / "demo" / "scripts" / "run.py"
    script_path.parent.mkdir(parents=True)
    script_path.write_text(
        "\n".join(
            [
                "warnings.append(\"template narration opener remains (e.g., 'This subsection ...')\")",
                "blocking.append(\"draft contains unicode ellipsis (...)\")",
                "lines.append(\" - ...\")",
            ]
        ),
        encoding="utf-8",
    )

    findings = audit_skills._audit_text_file("demo", script_path, skills_dir)

    assert [(item.severity, item.rule_id, item.line) for item in findings] == [
        ("WARN", "reader_facing_ellipsis", 3)
    ]
    assert findings[0].review_category == "output_placeholder_leak"
    assert "omitted-item count" in findings[0].next_action


def test_skill_audit_report_groups_review_categories(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(audit_skills, "REPO_ROOT", tmp_path)
    skills_dir = tmp_path / ".codex" / "skills"
    skill_path = skills_dir / "demo" / "SKILL.md"
    ref_path = skills_dir / "demo" / "references" / "examples.md"
    ref_path.parent.mkdir(parents=True)
    skill_path.write_text("LLM agents\n", encoding="utf-8")
    ref_path.write_text("Bad example: `we propose ...`\n", encoding="utf-8")

    findings, stats = audit_skills.audit_skills(skills_dir)
    report = audit_skills.render_report(findings=findings, stats=stats, fmt="text")

    assert "- By review category: reference_example_phrase=1, routing_portability=1" in report
    assert "review_category: routing_portability" in report
    assert "next_action: Generalize skill routing text" in report


def test_skill_audit_report_can_focus_review_category_and_limit(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(audit_skills, "REPO_ROOT", tmp_path)
    skills_dir = tmp_path / ".codex" / "skills"
    skill_path = skills_dir / "demo" / "SKILL.md"
    ref_path = skills_dir / "demo" / "references" / "examples.md"
    ref_path.parent.mkdir(parents=True)
    skill_path.write_text("LLM agents\n", encoding="utf-8")
    ref_path.write_text(
        "\n".join(
            [
                "Bad example: `we propose ...`",
                "Bad example: `we evaluate ...`",
            ]
        ),
        encoding="utf-8",
    )

    findings, stats = audit_skills.audit_skills(skills_dir)
    focused = audit_skills._filter_findings_by_review_category(
        findings,
        ("reference_example_phrase",),
    )
    display = audit_skills._limit_findings(focused, 1)
    report = audit_skills.render_report(
        findings=focused,
        stats=stats,
        fmt="text",
        display_findings=display,
        filters=audit_skills._rendered_filters(
            review_categories=("reference_example_phrase",),
            limit=1,
            summary_only=False,
        ),
    )

    assert len(focused) == 2
    assert "- Findings: 2" in report
    assert "- Displayed findings: 1 of 2" in report
    assert "- Filters: review_category=reference_example_phrase, limit=1" in report
    assert report.count("[INFO] reader_facing_ellipsis") == 1


def test_skill_audit_summary_only_omits_details(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(audit_skills, "REPO_ROOT", tmp_path)
    skills_dir = tmp_path / ".codex" / "skills"
    skill_path = skills_dir / "demo" / "SKILL.md"
    skill_path.parent.mkdir(parents=True)
    skill_path.write_text("LLM agents\n", encoding="utf-8")

    findings, stats = audit_skills.audit_skills(skills_dir)
    report = audit_skills.render_report(
        findings=findings,
        stats=stats,
        fmt="text",
        display_findings=[],
        filters=audit_skills._rendered_filters(
            review_categories=(),
            limit=0,
            summary_only=True,
        ),
    )

    assert "- Findings: 1" in report
    assert "- Displayed findings: 0 of 1" in report
    assert "- Filters: summary_only=true" in report
    assert "Finding details omitted by filter settings." in report
    assert "[WARN]" not in report


def test_skill_audit_json_payload_has_schema_and_validates(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(audit_skills, "REPO_ROOT", tmp_path)
    skills_dir = tmp_path / ".codex" / "skills"
    skill_path = skills_dir / "demo" / "SKILL.md"
    skill_path.parent.mkdir(parents=True)
    skill_path.write_text("LLM agents\n", encoding="utf-8")

    findings, stats = audit_skills.audit_skills(skills_dir)
    rendered = audit_skills.render_report(findings=findings, stats=stats, fmt="json")
    payload = json.loads(rendered)

    assert payload["schema"] == "skill-audit-report.v1"
    assert payload["summary"]["displayed_findings"] == 1
    assert audit_skills.validate_skill_audit_payload(payload) == []


def test_skill_audit_payload_validation_reports_shape_errors() -> None:
    issues = audit_skills.validate_skill_audit_payload(
        {
            "schema": "old-schema",
            "summary": {
                "skills_scanned": "1",
                "files_scanned": 1,
                "findings": 1,
                "displayed_findings": 2,
                "by_severity": {},
                "by_rule": {},
                "by_review_category": {},
                "filters": {},
            },
            "findings": [
                {
                    "severity": "INFO",
                    "rule_id": "reader_facing_ellipsis",
                    "skill": "demo",
                    "path": "SKILL.md",
                    "line": "1",
                    "message": "message",
                    "excerpt": "excerpt",
                    "review_category": "template_placeholder",
                    "next_action": "next",
                }
            ],
        }
    )

    assert "`schema` must be `skill-audit-report.v1`." in issues
    assert "`summary.skills_scanned` must be an integer." in issues
    assert "`summary.displayed_findings` must match the number of displayed `findings`." in issues
    assert "`findings[0].line` must be an integer." in issues
