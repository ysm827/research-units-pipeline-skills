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
        },
    },
)


@dataclass(frozen=True)
class ShowcaseCheck:
    id: str
    status: str
    evidence: str
    next_action: str


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
    ]
    checks.extend(_check_fixture_group(repo_root=repo_root, group=group) for group in FIXTURE_GROUPS)
    verdict = "PASS" if all(check.status == "PASS" for check in checks) else "ATTENTION"
    return {
        "schema": SCHEMA,
        "repo": str(repo_root),
        "verdict": verdict,
        "showcase_doc": SHOWCASE_DOC,
        "checks": [asdict(check) for check in checks],
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


def _check_fixture_group(*, repo_root: Path, group: dict[str, object]) -> ShowcaseCheck:
    root = str(group["root"])
    expected_paths = [path for path in HARNESS_SHOWCASE_FIXTURE_PATHS if path.startswith(root + "/")]
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


def _has_placeholder_text(text: str) -> bool:
    return bool(re.search(r"\bplaceholder\b|\bTBD\b|\blorem ipsum\b", text, flags=re.IGNORECASE))


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
    return "\n".join(lines) + "\n"


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
