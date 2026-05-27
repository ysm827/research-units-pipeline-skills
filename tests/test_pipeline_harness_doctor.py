from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

from tooling.executor import run_one_unit


REPO_ROOT = Path(__file__).resolve().parents[1]
UNIT_FIELDS = [
    "unit_id",
    "title",
    "skill",
    "owner",
    "depends_on",
    "checkpoint",
    "inputs",
    "outputs",
    "status",
]


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def write_units(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=UNIT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in UNIT_FIELDS})


def test_doctor_reports_next_runnable_unit(tmp_path: Path) -> None:
    workspace = tmp_path / "ws"
    write_units(
        workspace / "UNITS.csv",
        [
            {
                "unit_id": "U001",
                "title": "Seed",
                "skill": "demo",
                "owner": "CODEX",
                "outputs": "output/seed.md",
                "status": "DONE",
            },
            {
                "unit_id": "U010",
                "title": "Write",
                "skill": "demo",
                "owner": "CODEX",
                "depends_on": "U001",
                "checkpoint": "C1",
                "outputs": "output/write.md",
                "status": "TODO",
            },
        ],
    )
    (workspace / "STATUS.md").write_text("# Status\n\n## Current checkpoint\n- `C1`\n", encoding="utf-8")
    (workspace / "PIPELINE.lock.md").write_text("pipeline: pipelines/tutorial.pipeline.md\n", encoding="utf-8")
    (workspace / "output").mkdir(parents=True)
    (workspace / "output" / "seed.md").write_text("seed\n", encoding="utf-8")

    result = run_command("scripts/pipeline.py", "doctor", "--workspace", str(workspace))

    assert result.returncode == 0, result.stderr or result.stdout
    assert "Next runnable: `U010` Write (`demo`)" in result.stdout
    assert "Current checkpoint: `C1`" in result.stdout
    assert "DONE: 1" in result.stdout
    assert "TODO: 1" in result.stdout


def test_doctor_flags_units_dependency_and_artifact_problems(tmp_path: Path) -> None:
    workspace = tmp_path / "ws"
    write_units(
        workspace / "UNITS.csv",
        [
            {
                "unit_id": "U001",
                "title": "Done but missing output",
                "skill": "demo",
                "owner": "CODEX",
                "outputs": "output/missing.md",
                "status": "DONE",
            },
            {
                "unit_id": "U010",
                "title": "Missing dep",
                "skill": "demo",
                "owner": "CODEX",
                "depends_on": "U999",
                "outputs": "output/next.md",
                "status": "TODO",
            },
            {
                "unit_id": "U020",
                "title": "Human gate",
                "skill": "human-checkpoint",
                "owner": "HUMAN",
                "status": "TODO",
            },
        ],
    )

    result = run_command("scripts/pipeline.py", "doctor", "--workspace", str(workspace))

    assert result.returncode == 2, result.stdout
    assert "ERROR `missing_dependency`: `U010` depends on missing `U999`" in result.stdout
    assert "ERROR `missing_done_output`: `U001` is DONE but `output/missing.md` is missing" in result.stdout
    assert "WARN `human_checkpoint_missing`: `U020` is HUMAN-owned but has no checkpoint" in result.stdout


def test_doctor_flags_units_cycles_and_invalid_statuses(tmp_path: Path) -> None:
    workspace = tmp_path / "ws"
    write_units(
        workspace / "UNITS.csv",
        [
            {
                "unit_id": "U001",
                "title": "A",
                "skill": "demo",
                "owner": "CODEX",
                "depends_on": "U020",
                "outputs": "output/a.md",
                "status": "DONE",
            },
            {
                "unit_id": "U020",
                "title": "B",
                "skill": "demo",
                "owner": "CODEX",
                "depends_on": "U001",
                "outputs": "output/b.md",
                "status": "WAITING",
            },
        ],
    )
    (workspace / "output").mkdir(parents=True)
    (workspace / "output" / "a.md").write_text("a\n", encoding="utf-8")

    result = run_command("scripts/pipeline.py", "doctor", "--workspace", str(workspace))

    assert result.returncode == 2, result.stdout
    assert "ERROR `invalid_status`: `U020` has invalid status `WAITING`" in result.stdout
    assert "ERROR `dependency_cycle`: `U001` -> `U020` -> `U001`" in result.stdout


def test_executor_writes_manifest_for_scripted_unit_outputs(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    workspace = tmp_path / "workspace"
    script_path = repo_root / ".codex" / "skills" / "demo-skill" / "scripts" / "run.py"
    script_path.parent.mkdir(parents=True)
    script_path.write_text(
        "\n".join(
            [
                "from __future__ import annotations",
                "import argparse",
                "from pathlib import Path",
                "parser = argparse.ArgumentParser()",
                "parser.add_argument('--workspace', required=True)",
                "parser.add_argument('--unit-id', required=True)",
                "parser.add_argument('--inputs', default='')",
                "parser.add_argument('--outputs', default='')",
                "parser.add_argument('--checkpoint', default='')",
                "args = parser.parse_args()",
                "output = [x for x in args.outputs.split(';') if x][0]",
                "path = Path(args.workspace) / output",
                "path.parent.mkdir(parents=True, exist_ok=True)",
                "path.write_text('demo output\\n', encoding='utf-8')",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    write_units(
        workspace / "UNITS.csv",
        [
            {
                "unit_id": "U001",
                "title": "Demo",
                "skill": "demo-skill",
                "owner": "CODEX",
                "outputs": "output/demo.md",
                "status": "TODO",
            }
        ],
    )

    result = run_one_unit(workspace=workspace, repo_root=repo_root)

    manifest_path = workspace / "output" / "unit_logs" / "U001.demo-skill.manifest.json"
    assert result.status == "DONE"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["unit_id"] == "U001"
    assert manifest["skill"] == "demo-skill"
    assert manifest["exit_code"] == 0
    assert manifest["outputs"][0]["path"] == "output/demo.md"
    assert manifest["outputs"][0]["exists"] is True
    assert manifest["outputs"][0]["sha256"]
