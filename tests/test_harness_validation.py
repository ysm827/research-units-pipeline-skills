from __future__ import annotations

from pathlib import Path

import scripts.audit_skills as audit_skills
import scripts.generate_skill_graph as generate_skill_graph
import scripts.validate_repo as validate_repo


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
