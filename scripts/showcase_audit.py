from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tooling.harness_contracts import (
    HARNESS_SHOWCASE_ASSET_PATHS,
    HARNESS_SHOWCASE_FIXTURE_PATHS,
)

SCHEMA = "harness-showcase-audit.v1"
SHOWCASE_DOC = "docs/HARNESS_SHOWCASE.md"
ARTIFACT_PACK_EXCERPT_TSV_HEADER = ("category", "path", "exists", "role")
ARTIFACT_PACK_EXCERPT_TSV_HEADER_LINE = "\t".join(ARTIFACT_PACK_EXCERPT_TSV_HEADER)
ABSOLUTE_LOCAL_PATH_PATTERNS = (
    re.compile(r"/Users/[^\s`)>,|]+"),
    re.compile(r"/home/[^\s`)>,|]+"),
    re.compile(r"/tmp/[^\s`)>,|]+"),
    re.compile(r"[A-Za-z]:\\Users\\[^\s`)>,|]+"),
    re.compile(r"file://[^\s`)>,|]+"),
)
PIPELINE_PROTOCOLS = (
    "pipelines/research-brief.pipeline.md",
    "pipelines/source-tutorial.pipeline.md",
)

RESEARCH_BRIEF_ROOT = "example/research-brief/rag-evaluation-harness-demo"
SOURCE_TUTORIAL_ROOT = "example/source-tutorial/robot-learning-harness-demo"

FIXTURE_GROUPS = (
    {
        "id": "research_brief_fixture",
        "label": "research-brief fixture",
        "root": RESEARCH_BRIEF_ROOT,
        "deliverables": ("output/SNAPSHOT.md",),
        "required_terms": {
            "output/SNAPSHOT.md": ("# Snapshot: RAG Evaluation", "Harness Implication"),
            "output/DELIVERABLE_SELFLOOP_TODO.md": ("Status: PASS",),
            "output/CONTRACT_REPORT.md": ("Status: PASS",),
            "output/ARTIFACT_PACK_EXCERPT.md": (
                "# Artifact Pack Excerpt",
                "artifact-pack.v1",
                "target_artifact",
                "run_ledger",
                "harness_report",
            ),
            "output/ARTIFACT_PACK_EXCERPT.tsv": (
                "category\tpath\texists\trole",
                "target_artifact\toutput/SNAPSHOT.md\ttrue\tfinal deliverable",
                "harness_report\toutput/CONTRACT_REPORT.md\ttrue\tcontract evidence",
            ),
        },
    },
    {
        "id": "source_tutorial_fixture",
        "label": "source-tutorial fixture",
        "root": SOURCE_TUTORIAL_ROOT,
        "deliverables": (
            "output/TUTORIAL_EXCERPT.md",
            "output/TUTORIAL_SPEC_EXCERPT.md",
        ),
        "required_terms": {
            "output/TUTORIAL_EXCERPT.md": ("# A Source-Grounded Introduction to Robot Learning",),
            "output/TUTORIAL_SPEC_EXCERPT.md": ("Learning Objectives",),
            "evidence/TUTORIAL_SELFLOOP.md": ("Status: PASS",),
            "evidence/DELIVERY_EVIDENCE.md": ("latex/main.pdf", "latex/slides/main.pdf"),
            "evidence/CONTRACT_REPORT.md": ("Status: PASS",),
            "evidence/RUN_AUDIT_SUMMARY.md": ("Audit verdict: PASS",),
            "evidence/ARTIFACT_PACK_EXCERPT.md": (
                "# Artifact Pack Excerpt",
                "artifact-pack.v1",
                "target_artifact",
                "unit_output",
                "harness_report",
            ),
            "evidence/ARTIFACT_PACK_EXCERPT.tsv": (
                "category\tpath\texists\trole",
                "target_artifact\toutput/TUTORIAL_EXCERPT.md\ttrue\tfinal tutorial excerpt",
                "harness_report\tevidence/RUN_AUDIT_SUMMARY.md\ttrue\trun audit evidence",
            ),
        },
    },
)


@dataclass(frozen=True)
class ShowcaseCheck:
    id: str
    status: str
    evidence: str
    next_action: str


@dataclass(frozen=True)
class ShowcaseScore:
    id: str
    label: str
    status: str
    tracked_files: int
    present_files: int
    required_markers: int
    present_markers: int
    evidence_surface: str


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the tracked harness showcase fixtures. This checks whether "
            "the reader-facing examples expose deliverables, protocol links, "
            "visual lineage, and evidence reports."
        )
    )
    parser.add_argument("--repo-root", default=str(REPO_ROOT), help="Repository root to inspect.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--report", default="", help="Optional output report path.")
    parser.add_argument("--strict", action="store_true", help="Exit 2 when any showcase check is WARN.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    payload = build_showcase_audit(repo_root=repo_root)
    rendered = render_json(payload) if args.format == "json" else render_markdown(payload)

    if args.report:
        report_path = Path(args.report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(rendered, encoding="utf-8")

    sys.stdout.write(rendered)
    if not rendered.endswith("\n"):
        sys.stdout.write("\n")

    if args.strict and payload["verdict"] != "PASS":
        return 2
    return 0


def build_showcase_audit(*, repo_root: Path) -> dict[str, object]:
    checks = [
        _check_showcase_doc(repo_root=repo_root),
        _check_lineage_assets(repo_root=repo_root),
        _check_pipeline_protocols(repo_root=repo_root),
        _check_fixture_contracts(),
    ]
    checks.extend(_check_fixture_group(repo_root=repo_root, group=group) for group in FIXTURE_GROUPS)
    scorecard = [_score_fixture_group(repo_root=repo_root, group=group) for group in FIXTURE_GROUPS]
    verdict = "PASS" if all(check.status == "PASS" for check in checks) else "ATTENTION"
    return {
        "schema": SCHEMA,
        "repo": str(repo_root),
        "verdict": verdict,
        "showcase_doc": SHOWCASE_DOC,
        "checks": [asdict(check) for check in checks],
        "scorecard": [asdict(score) for score in scorecard],
        "note": (
            "This audit checks the portable showcase fixtures under example/. "
            "It does not rerun retrieval, LaTeX compilation, or semantic quality review."
        ),
    }


def validate_showcase_audit_payload(payload: dict[str, object]) -> list[str]:
    issues: list[str] = []
    if payload.get("schema") != SCHEMA:
        issues.append(f"`schema` must be `{SCHEMA}`.")
    for key in ("repo", "showcase_doc", "note"):
        if not isinstance(payload.get(key), str):
            issues.append(f"`{key}` must be a string.")
    verdict = payload.get("verdict")
    if verdict not in {"PASS", "ATTENTION"}:
        issues.append("`verdict` must be `PASS` or `ATTENTION`.")
    checks = payload.get("checks")
    if not isinstance(checks, list):
        issues.append("`checks` must be a list.")
        return issues
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            issues.append(f"`checks[{index}]` must be an object.")
            continue
        for key in ("id", "evidence", "next_action"):
            if not isinstance(check.get(key), str):
                issues.append(f"`checks[{index}].{key}` must be a string.")
        if check.get("status") not in {"PASS", "WARN"}:
            issues.append(f"`checks[{index}].status` must be `PASS` or `WARN`.")
    scorecard = payload.get("scorecard")
    if scorecard is None:
        return issues
    if not isinstance(scorecard, list):
        issues.append("`scorecard` must be a list when present.")
        return issues
    for index, score in enumerate(scorecard):
        if not isinstance(score, dict):
            issues.append(f"`scorecard[{index}]` must be an object.")
            continue
        for key in ("id", "label", "evidence_surface"):
            if not isinstance(score.get(key), str):
                issues.append(f"`scorecard[{index}].{key}` must be a string.")
        if score.get("status") not in {"PASS", "WARN"}:
            issues.append(f"`scorecard[{index}].status` must be `PASS` or `WARN`.")
        for key in ("tracked_files", "present_files", "required_markers", "present_markers"):
            value = score.get(key)
            if not isinstance(value, int) or value < 0:
                issues.append(f"`scorecard[{index}].{key}` must be a non-negative integer.")
    return issues


def _check_showcase_doc(*, repo_root: Path) -> ShowcaseCheck:
    doc_path = repo_root / SHOWCASE_DOC
    if not doc_path.exists():
        return ShowcaseCheck(
            "showcase_doc",
            "WARN",
            f"Missing `{SHOWCASE_DOC}`.",
            "Restore the deliverable-first showcase document.",
        )

    text = _read_text(doc_path)
    expected_paths = (
        tuple(HARNESS_SHOWCASE_ASSET_PATHS)
        + tuple(HARNESS_SHOWCASE_FIXTURE_PATHS)
        + tuple(PIPELINE_PROTOCOLS)
    )
    expected_terms = (SCHEMA, "python scripts/showcase_audit.py --strict")
    missing = [item for item in expected_paths + expected_terms if item not in text]
    if missing:
        return ShowcaseCheck(
            "showcase_doc",
            "WARN",
            f"`{SHOWCASE_DOC}` is missing showcase audit references: {', '.join(missing)}.",
            "Update the showcase document so readers can trace every fixture path and run the audit.",
        )
    return ShowcaseCheck(
        "showcase_doc",
        "PASS",
        f"`{SHOWCASE_DOC}` references {len(expected_paths)} artifact/protocol paths and the audit command.",
        "Keep the showcase doc aligned with tracked fixture paths.",
    )


def _check_lineage_assets(*, repo_root: Path) -> ShowcaseCheck:
    missing = [path for path in HARNESS_SHOWCASE_ASSET_PATHS if not (repo_root / path).exists()]
    if missing:
        return ShowcaseCheck(
            "lineage_assets",
            "WARN",
            f"Missing showcase visual assets: {', '.join(missing)}.",
            "Restore the lineage asset before presenting the showcase.",
        )

    svg_issues: list[str] = []
    required_terms = ("<svg", "Harness Showcase Lineage", "Research-Brief Fixture", "Source-Tutorial Fixture")
    for rel_path in HARNESS_SHOWCASE_ASSET_PATHS:
        if not rel_path.endswith(".svg"):
            continue
        text = _read_text(repo_root / rel_path)
        missing_terms = [term for term in required_terms if term not in text]
        if missing_terms:
            svg_issues.append(f"{rel_path} missing {', '.join(missing_terms)}")
    if svg_issues:
        return ShowcaseCheck(
            "lineage_assets",
            "WARN",
            "; ".join(svg_issues) + ".",
            "Regenerate or repair the showcase SVG so the fixture lineage remains visible.",
        )
    return ShowcaseCheck(
        "lineage_assets",
        "PASS",
        f"Found {len(HARNESS_SHOWCASE_ASSET_PATHS)} showcase visual asset(s) with expected fixture labels.",
        "Keep visual labels stable enough for doc and screenshot review.",
    )


def _check_pipeline_protocols(*, repo_root: Path) -> ShowcaseCheck:
    missing = [path for path in PIPELINE_PROTOCOLS if not (repo_root / path).exists()]
    if missing:
        return ShowcaseCheck(
            "pipeline_protocols",
            "WARN",
            f"Missing showcase pipeline protocol(s): {', '.join(missing)}.",
            "Restore the protocol files so fixture outputs can be traced to workflow contracts.",
        )
    return ShowcaseCheck(
        "pipeline_protocols",
        "PASS",
        f"Found {len(PIPELINE_PROTOCOLS)} pipeline protocol(s) used by the showcase fixtures.",
        "Keep showcase fixtures tied to current pipeline contracts.",
    )


def _check_fixture_contracts() -> ShowcaseCheck:
    issues: list[str] = []
    ids: set[str] = set()
    roots: set[str] = set()

    for group in FIXTURE_GROUPS:
        group_id = str(group["id"])
        root = str(group["root"])
        if group_id in ids:
            issues.append(f"duplicate fixture group id `{group_id}`")
        ids.add(group_id)
        if root in roots:
            issues.append(f"duplicate fixture root `{root}`")
        roots.add(root)

        tracked_paths = _fixture_paths_for_root(root)
        if not tracked_paths:
            issues.append(f"`{group_id}` root `{root}` has no tracked fixture paths")

        referenced_paths = [str(path) for path in group.get("deliverables", ())]
        referenced_paths.extend(str(path) for path in dict(group.get("required_terms", {})))
        for rel_path in referenced_paths:
            full_path = f"{root}/{rel_path}"
            if full_path not in HARNESS_SHOWCASE_FIXTURE_PATHS:
                issues.append(f"`{group_id}` references `{full_path}` outside HARNESS_SHOWCASE_FIXTURE_PATHS")

    unmatched = [
        path
        for path in HARNESS_SHOWCASE_FIXTURE_PATHS
        if not any(path.startswith(root + "/") for root in roots)
    ]
    if unmatched:
        issues.append("tracked fixture paths are not owned by a fixture group: " + ", ".join(unmatched))

    if issues:
        return ShowcaseCheck(
            "fixture_contracts",
            "WARN",
            "Showcase fixture contract drift: " + "; ".join(issues) + ".",
            "Update FIXTURE_GROUPS and HARNESS_SHOWCASE_FIXTURE_PATHS together.",
        )
    return ShowcaseCheck(
        "fixture_contracts",
        "PASS",
        f"{len(FIXTURE_GROUPS)} fixture group(s) cover {len(HARNESS_SHOWCASE_FIXTURE_PATHS)} tracked fixture paths.",
        "Keep fixture group definitions and tracked fixture paths synchronized.",
    )


def _check_fixture_group(*, repo_root: Path, group: dict[str, object]) -> ShowcaseCheck:
    root = str(group["root"])
    expected_paths = _fixture_paths_for_root(root)
    missing = [path for path in expected_paths if not (repo_root / path).exists()]
    issues = [f"missing files {', '.join(missing)}"] if missing else []

    for rel_path in group.get("deliverables", ()):
        full_path = repo_root / root / str(rel_path)
        if full_path.exists() and _has_placeholder_text(_read_text(full_path)):
            issues.append(f"`{root}/{rel_path}` still looks like placeholder content")

    required_terms = dict(group.get("required_terms", {}))
    for rel_path, terms in required_terms.items():
        full_path = repo_root / root / str(rel_path)
        if not full_path.exists():
            continue
        text = _read_text(full_path)
        missing_terms = [term for term in _as_terms(terms) if term not in text]
        if missing_terms:
            issues.append(f"`{root}/{rel_path}` missing {', '.join(missing_terms)}")

    for rel_path in expected_paths:
        full_path = repo_root / rel_path
        if full_path.exists():
            issues.extend(_fixture_portability_issues(full_path=full_path, rel_path=rel_path))
        if rel_path.endswith("ARTIFACT_PACK_EXCERPT.tsv"):
            if full_path.exists():
                issues.extend(_artifact_pack_excerpt_tsv_issues(full_path=full_path, rel_path=rel_path))

    if issues:
        return ShowcaseCheck(
            str(group["id"]),
            "WARN",
            f"{group['label']} has showcase evidence issues: {'; '.join(issues)}.",
            "Repair the tracked fixture so the deliverable-first exhibit remains concrete.",
        )
    return ShowcaseCheck(
        str(group["id"]),
        "PASS",
        f"{group['label']} exposes {len(expected_paths)} tracked files with deliverable and evidence markers.",
        "Refresh this fixture when the corresponding pipeline contract changes.",
    )


def _score_fixture_group(*, repo_root: Path, group: dict[str, object]) -> ShowcaseScore:
    root = str(group["root"])
    expected_paths = _fixture_paths_for_root(root)
    present_files = sum(1 for path in expected_paths if (repo_root / path).exists())

    required_terms = dict(group.get("required_terms", {}))
    required_markers = 0
    present_markers = 0
    for rel_path, terms in required_terms.items():
        term_set = _as_terms(terms)
        required_markers += len(term_set)
        full_path = repo_root / root / str(rel_path)
        if not full_path.exists():
            continue
        text = _read_text(full_path)
        present_markers += sum(1 for term in term_set if term in text)

    status = (
        "PASS"
        if present_files == len(expected_paths) and present_markers == required_markers
        else "WARN"
    )
    return ShowcaseScore(
        id=str(group["id"]),
        label=str(group["label"]),
        status=status,
        tracked_files=len(expected_paths),
        present_files=present_files,
        required_markers=required_markers,
        present_markers=present_markers,
        evidence_surface=(
            f"{present_files}/{len(expected_paths)} tracked files; "
            f"{present_markers}/{required_markers} required markers"
        ),
    )


def _has_placeholder_text(text: str) -> bool:
    return bool(re.search(r"\bplaceholder\b|\bTBD\b|\blorem ipsum\b", text, flags=re.IGNORECASE))


def _fixture_paths_for_root(root: str) -> list[str]:
    return [path for path in HARNESS_SHOWCASE_FIXTURE_PATHS if path.startswith(root + "/")]


def _fixture_portability_issues(*, full_path: Path, rel_path: str) -> list[str]:
    issues: list[str] = []
    for line_no, line in enumerate(_read_text(full_path).splitlines(), start=1):
        matches: list[str] = []
        for pattern in ABSOLUTE_LOCAL_PATH_PATTERNS:
            matches.extend(match.group(0) for match in pattern.finditer(line))
        if matches:
            sample = ", ".join(f"`{match}`" for match in matches[:3])
            suffix = " ..." if len(matches) > 3 else ""
            issues.append(f"`{rel_path}` line {line_no} contains absolute local path(s): {sample}{suffix}")
    return issues


def _artifact_pack_excerpt_tsv_issues(*, full_path: Path, rel_path: str) -> list[str]:
    lines = _read_text(full_path).splitlines()
    if not lines:
        return [f"`{rel_path}` is empty"]

    header = tuple(lines[0].split("\t"))
    issues: list[str] = []
    records: list[tuple[str, str, str, str]] = []
    if header != ARTIFACT_PACK_EXCERPT_TSV_HEADER:
        issues.append(
            f"`{rel_path}` has non-canonical header "
            f"`{lines[0]}`; expected `{ARTIFACT_PACK_EXCERPT_TSV_HEADER_LINE}`"
        )

    for line_no, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        cells = line.split("\t")
        if len(cells) != len(ARTIFACT_PACK_EXCERPT_TSV_HEADER):
            issues.append(f"`{rel_path}` line {line_no} has {len(cells)} column(s); expected 4")
            continue
        category, path, exists, role = (cell.strip() for cell in cells)
        if not category:
            issues.append(f"`{rel_path}` line {line_no} has empty category")
        if not path:
            issues.append(f"`{rel_path}` line {line_no} has empty path")
        if exists not in {"true", "false"}:
            issues.append(f"`{rel_path}` line {line_no} has non-boolean exists value `{exists}`")
        if not role:
            issues.append(f"`{rel_path}` line {line_no} has empty role")
        if category and path and exists in {"true", "false"} and role:
            records.append((category, path, exists, role))

    markdown_path = full_path.with_suffix(".md")
    if markdown_path.exists():
        markdown_rel = str(Path(rel_path).with_suffix(".md"))
        markdown_records = _artifact_pack_excerpt_markdown_records(_read_text(markdown_path))
        if records and not markdown_records:
            issues.append(f"`{markdown_rel}` has no parseable artifact-pack excerpt table rows")
        missing_in_markdown = [record for record in records if record not in markdown_records]
        missing_in_tsv = [record for record in markdown_records if record not in records]
        for category, path, exists, role in missing_in_markdown:
            issues.append(
                f"`{markdown_rel}` is missing TSV row `{category}\\t{path}\\t{exists}\\t{role}`"
            )
        for category, path, exists, role in missing_in_tsv:
            issues.append(
                f"`{rel_path}` is missing Markdown row `{category}\\t{path}\\t{exists}\\t{role}`"
            )
    return issues


def _artifact_pack_excerpt_markdown_records(text: str) -> set[tuple[str, str, str, str]]:
    records: set[tuple[str, str, str, str]] = set()
    pattern = re.compile(
        r"^\|\s*`(?P<category>[^`]+)`\s*"
        r"\|\s*`(?P<path>[^`]+)`\s*"
        r"\|\s*(?P<exists>true|false)\s*"
        r"\|\s*(?P<role>[^|]+?)\s*\|$"
    )
    for line in text.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        records.add(
            (
                match.group("category").strip(),
                match.group("path").strip(),
                match.group("exists").strip(),
                match.group("role").strip(),
            )
        )
    return records


def _as_terms(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Iterable):
        return tuple(str(item) for item in value)
    return (str(value),)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def render_json(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# Harness Showcase Audit",
        "",
        f"- Schema: `{payload['schema']}`",
        f"- Verdict: `{payload['verdict']}`",
        f"- Repo: `{payload['repo']}`",
        f"- Showcase doc: `{payload['showcase_doc']}`",
        "",
        str(payload["note"]),
        "",
        "| Check | Status | Evidence | Next action |",
        "|---|---|---|---|",
    ]
    for item in payload["checks"]:
        check = dict(item)
        lines.append(
            "| {id} | {status} | {evidence} | {next_action} |".format(
                id=_escape_cell(str(check["id"])),
                status=_escape_cell(str(check["status"])),
                evidence=_escape_cell(str(check["evidence"])),
                next_action=_escape_cell(str(check["next_action"])),
            )
        )
    scorecard = payload.get("scorecard")
    if isinstance(scorecard, list) and scorecard:
        lines.extend(
            [
                "",
                "## Fixture Scorecard",
                "",
                "| Fixture | Status | Files | Markers | Evidence surface |",
                "|---|---|---:|---:|---|",
            ]
        )
        for item in scorecard:
            score = dict(item)
            files = f"{score['present_files']}/{score['tracked_files']}"
            markers = f"{score['present_markers']}/{score['required_markers']}"
            lines.append(
                "| {label} | {status} | {files} | {markers} | {surface} |".format(
                    label=_escape_cell(str(score["label"])),
                    status=_escape_cell(str(score["status"])),
                    files=_escape_cell(files),
                    markers=_escape_cell(markers),
                    surface=_escape_cell(str(score["evidence_surface"])),
                )
            )
    return "\n".join(lines) + "\n"


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
