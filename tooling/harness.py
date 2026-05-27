from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tooling.common import UnitsTable, atomic_write_text, ensure_dir, now_iso_seconds, parse_semicolon_list


VALID_STATUSES = {"TODO", "DOING", "DONE", "BLOCKED", "SKIP"}
VALID_OWNERS = {"CODEX", "HUMAN"}


@dataclass(frozen=True)
class HarnessIssue:
    level: str
    code: str
    message: str


def validate_units_table(table: UnitsTable) -> list[HarnessIssue]:
    issues: list[HarnessIssue] = []
    required_fields = {"unit_id", "skill", "owner", "depends_on", "checkpoint", "outputs", "status"}
    missing_fields = sorted(required_fields.difference(table.fieldnames))
    for field in missing_fields:
        issues.append(HarnessIssue("ERROR", "missing_units_field", f"`UNITS.csv` is missing `{field}`"))

    ids: list[str] = []
    duplicate_ids: set[str] = set()
    for row in table.rows:
        unit_id = _unit_id(row)
        if not unit_id:
            issues.append(HarnessIssue("ERROR", "missing_unit_id", "A unit row is missing `unit_id`"))
            continue
        if unit_id in ids:
            duplicate_ids.add(unit_id)
        ids.append(unit_id)

    for unit_id in sorted(duplicate_ids):
        issues.append(HarnessIssue("ERROR", "duplicate_unit_id", f"`{unit_id}` appears more than once"))

    unit_ids = set(ids)
    for row in table.rows:
        unit_id = _unit_id(row) or "<missing>"
        status = _status(row)
        owner = _owner(row)
        if status not in VALID_STATUSES:
            issues.append(HarnessIssue("ERROR", "invalid_status", f"`{unit_id}` has invalid status `{status or '<blank>'}`"))
        if owner not in VALID_OWNERS:
            issues.append(HarnessIssue("WARN", "invalid_owner", f"`{unit_id}` has unexpected owner `{owner or '<blank>'}`"))
        if owner == "HUMAN" and not str(row.get("checkpoint") or "").strip():
            issues.append(
                HarnessIssue("WARN", "human_checkpoint_missing", f"`{unit_id}` is HUMAN-owned but has no checkpoint")
            )
        for dep_id in parse_semicolon_list(row.get("depends_on")):
            if dep_id not in unit_ids:
                issues.append(
                    HarnessIssue("ERROR", "missing_dependency", f"`{unit_id}` depends on missing `{dep_id}`")
                )

    issues.extend(_cycle_issues(table))
    return issues


def build_doctor_report(*, workspace: Path, repo_root: Path) -> tuple[int, str]:
    units_path = workspace / "UNITS.csv"
    lines = [
        "# Pipeline doctor",
        "",
        f"- Workspace: `{workspace}`",
        f"- Repo: `{repo_root}`",
    ]

    lock_summary = _pipeline_lock_summary(workspace / "PIPELINE.lock.md")
    if lock_summary:
        lines.append(f"- Pipeline lock: `{lock_summary}`")
    else:
        lines.append("- Pipeline lock: missing")

    checkpoint = _current_checkpoint(workspace / "STATUS.md")
    lines.append(f"- Current checkpoint: `{checkpoint}`")

    if not units_path.exists():
        issue = HarnessIssue("ERROR", "missing_units", f"Missing `{units_path}`")
        lines.extend(["", "## Harness issues", _format_issue(issue)])
        return 2, "\n".join(lines).rstrip() + "\n"

    table = UnitsTable.load(units_path)
    issues = validate_units_table(table)
    issues.extend(_workspace_artifact_issues(workspace=workspace, table=table))

    lines.extend(["", "## Unit status"])
    counts = Counter(_status(row) or "<blank>" for row in table.rows)
    if counts:
        for status in sorted(counts):
            lines.append(f"- {status}: {counts[status]}")
    else:
        lines.append("- No units found")

    next_row = find_next_runnable(table)
    lines.extend(["", "## Next runnable"])
    if next_row is None:
        lines.append("- No runnable unit found")
    else:
        unit_id = _unit_id(next_row)
        title = str(next_row.get("title") or "").strip() or "(untitled)"
        skill = str(next_row.get("skill") or "").strip() or "(no skill)"
        lines.append(f"- Next runnable: `{unit_id}` {title} (`{skill}`)")

    lines.extend(["", "## Harness issues"])
    if issues:
        for issue in issues:
            lines.append(_format_issue(issue))
    else:
        lines.append("- No harness issues")

    lines.extend(_recent_report_summaries(workspace))

    exit_code = 2 if any(issue.level == "ERROR" for issue in issues) else 0
    return exit_code, "\n".join(lines).rstrip() + "\n"


def find_next_runnable(table: UnitsTable) -> dict[str, str] | None:
    status_ok = {"DONE", "SKIP"}
    unit_by_id = {_unit_id(row): row for row in table.rows if _unit_id(row)}
    for row in table.rows:
        if _status(row) not in {"TODO", "BLOCKED"}:
            continue
        deps = parse_semicolon_list(row.get("depends_on"))
        if not deps:
            return row
        if all(dep_id in unit_by_id and _status(unit_by_id[dep_id]) in status_ok for dep_id in deps):
            return row
    return None


def write_unit_manifest(
    *,
    workspace: Path,
    unit_id: str,
    skill: str,
    outputs: list[str],
    exit_code: int,
    status: str,
) -> Path:
    manifest_path = workspace / "output" / "unit_logs" / f"{unit_id}.{skill}.manifest.json"
    payload = {
        "schema": "unit-output-manifest.v1",
        "generated_at": now_iso_seconds(),
        "unit_id": unit_id,
        "skill": skill,
        "status": status,
        "exit_code": exit_code,
        "outputs": [_artifact_record(workspace=workspace, relpath=rel) for rel in outputs if str(rel or "").strip()],
    }
    ensure_dir(manifest_path.parent)
    atomic_write_text(manifest_path, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return manifest_path


def _workspace_artifact_issues(*, workspace: Path, table: UnitsTable) -> list[HarnessIssue]:
    issues: list[HarnessIssue] = []
    for row in table.rows:
        if _status(row) != "DONE":
            continue
        unit_id = _unit_id(row) or "<missing>"
        for raw_output in parse_semicolon_list(row.get("outputs")):
            if raw_output.strip().startswith("?"):
                continue
            relpath = _strip_optional_marker(raw_output)
            if relpath and not (workspace / relpath).exists():
                issues.append(
                    HarnessIssue(
                        "ERROR",
                        "missing_done_output",
                        f"`{unit_id}` is DONE but `{relpath}` is missing",
                    )
                )
    return issues


def _cycle_issues(table: UnitsTable) -> list[HarnessIssue]:
    dep_map = {_unit_id(row): parse_semicolon_list(row.get("depends_on")) for row in table.rows if _unit_id(row)}
    issues: list[HarnessIssue] = []
    temporary: set[str] = set()
    permanent: set[str] = set()
    stack: list[str] = []
    seen_cycles: set[tuple[str, ...]] = set()

    def visit(unit_id: str) -> None:
        if unit_id in permanent:
            return
        if unit_id in temporary:
            try:
                start = stack.index(unit_id)
            except ValueError:
                start = 0
            cycle = tuple(stack[start:] + [unit_id])
            if cycle not in seen_cycles:
                seen_cycles.add(cycle)
                issues.append(HarnessIssue("ERROR", "dependency_cycle", "`" + "` -> `".join(cycle) + "`"))
            return
        temporary.add(unit_id)
        stack.append(unit_id)
        for dep_id in dep_map.get(unit_id, []):
            if dep_id in dep_map:
                visit(dep_id)
        stack.pop()
        temporary.remove(unit_id)
        permanent.add(unit_id)

    for unit_id in dep_map:
        visit(unit_id)
    return issues


def _artifact_record(*, workspace: Path, relpath: str) -> dict[str, Any]:
    relpath = _strip_optional_marker(relpath)
    path = workspace / relpath
    record: dict[str, Any] = {"path": relpath, "exists": path.exists()}
    if not path.exists():
        return record
    if path.is_dir():
        files = [item for item in path.rglob("*") if item.is_file()]
        record.update({"type": "directory", "file_count": len(files)})
        return record
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    record.update({"type": "file", "size": path.stat().st_size, "sha256": digest.hexdigest()})
    return record


def _recent_report_summaries(workspace: Path) -> list[str]:
    report_paths = [
        workspace / "output" / "RUN_ERRORS.md",
        workspace / "output" / "QUALITY_GATE.md",
        workspace / "output" / "CONTRACT_REPORT.md",
    ]
    lines: list[str] = ["", "## Recent harness reports"]
    found = False
    for path in report_paths:
        if not path.exists() or path.stat().st_size == 0:
            continue
        found = True
        preview = _first_nonempty_content_line(path)
        rel = path.relative_to(workspace)
        suffix = f": {preview}" if preview else ""
        lines.append(f"- `{rel}`{suffix}")
    if not found:
        lines.append("- No recent harness reports found")
    return lines


def _first_nonempty_content_line(path: Path) -> str:
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        return line[:160]
    return ""


def _pipeline_lock_summary(path: Path) -> str:
    if not path.exists():
        return ""
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if line:
            return line
    return ""


def _current_checkpoint(path: Path) -> str:
    if not path.exists():
        return "unknown"
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for idx, line in enumerate(lines):
        if line.strip() != "## Current checkpoint":
            continue
        for candidate in lines[idx + 1 :]:
            value = candidate.strip()
            if not value:
                continue
            if value.startswith("#"):
                break
            return value.lstrip("- ").strip().strip("`") or "unknown"
    return "unknown"


def _format_issue(issue: HarnessIssue) -> str:
    return f"- {issue.level} `{issue.code}`: {issue.message}"


def _unit_id(row: dict[str, str]) -> str:
    return str(row.get("unit_id") or "").strip()


def _status(row: dict[str, str]) -> str:
    return str(row.get("status") or "").strip().upper()


def _owner(row: dict[str, str]) -> str:
    return str(row.get("owner") or "").strip().upper()


def _strip_optional_marker(relpath: str) -> str:
    relpath = str(relpath or "").strip()
    if relpath.startswith("?"):
        return relpath[1:].strip()
    return relpath
