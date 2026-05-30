# Showcase Fixture Refresh

This document defines how a maintainer should refresh tracked showcase
fixtures from a completed local workspace. It keeps the deliverable-first
showcase useful without turning ignored workspaces into hidden dependencies.

The current showcase lives in `docs/HARNESS_SHOWCASE.md`. Its machine-readable
health contract is `harness-showcase-audit.v1`, documented in
`docs/SHOWCASE_AUDIT_SCHEMA.md`. Artifact-pack manifests are documented in
`docs/ARTIFACT_PACK_SCHEMA.md`.

## Refresh Boundary

Tracked showcase fixtures are curated exhibits under `example/`. They are not
full workspace archives.

Keep these boundaries:

- `workspaces/` remains ignored and private by default.
- `example/` contains only portable excerpts, summaries, and small evidence
  files that help readers trace a result backward.
- Do not copy absolute local paths from a workspace into tracked fixtures.
- Do not copy PDFs, TeX build directories, caches, downloaded corpora, or large
  binaries unless the repo explicitly decides that the file is part of the
  portable exhibit.
- Summarize binary delivery evidence in Markdown when the binary itself should
  stay workspace-local.
- Do not treat a refreshed fixture as a semantic benchmark. The fixture proves
  inspectable lineage and contract coverage, not broad research quality.

## Preconditions

Refresh from a workspace only when it is completed enough to teach a reader
something specific:

- the final deliverable exists or the fixture is intentionally demonstrating a
  partial run state
- `UNITS.csv`, `PIPELINE.lock.md`, and the workspace ledgers are present
- relevant harness reports have been regenerated from the current tooling
- any copied excerpt has been reviewed for local paths and stale claims

Use a real workspace path in place of the placeholder:

```bash
WS=workspaces/<completed-workspace>
```

## Regenerate Workspace Evidence

Run the workspace-level harness reports before copying anything into
`example/`:

```bash
python scripts/pipeline.py doctor --workspace "$WS" --write
python scripts/pipeline.py audit --workspace "$WS" --write
python scripts/pipeline.py improve --workspace "$WS" --write
python scripts/pipeline.py pack --workspace "$WS" --write --write-excerpt
```

The last command writes:

- `output/ARTIFACT_PACK.md`
- `output/ARTIFACT_PACK.json`
- `output/ARTIFACT_PACK_EXCERPT.md`
- `output/ARTIFACT_PACK_EXCERPT.tsv`

The full `ARTIFACT_PACK.json` remains the compatibility surface. The excerpt
Markdown and TSV files are derived handoff views that are easier to curate into
a tracked fixture.

## Curate Into `example/`

Copy only the surfaces that support the exhibit story. The fixture should let a
reader start with a deliverable and walk backward into evidence:

1. Copy a final deliverable excerpt or compact summary into the fixture's
   `output/` directory.
2. Copy the smallest useful intermediate artifacts: outline, taxonomy, source
   summary, evidence table, self-check, or contract report.
3. Copy `ARTIFACT_PACK_EXCERPT.md` and `ARTIFACT_PACK_EXCERPT.tsv` into the
   same fixture area as the other evidence.
4. Preserve workspace-relative paths in excerpt rows when they still describe
   the fixture layout. Edit only fixture-specific role labels or paths that no
   longer match after curation.
5. Update the fixture `README.md` so it explains the inspection order and
   points back to the relevant `pipelines/*.pipeline.md` file.
6. Update `docs/HARNESS_SHOWCASE.md` when the fixture adds, removes, or
   renames a reader-facing surface.

If a copied Markdown excerpt and TSV sidecar describe the same rows, keep them
paired. The showcase audit compares `ARTIFACT_PACK_EXCERPT.md` against
`ARTIFACT_PACK_EXCERPT.tsv` for tracked fixtures.

## Required Validation

After refreshing a fixture, run:

```bash
python scripts/showcase_audit.py --strict
python scripts/showcase_audit.py --format json
python scripts/validate_repo.py --no-check-quality --strict
```

Run the focused or full test suite when the refresh also changes scripts,
schema docs, fixture validation, pipeline contracts, or artifact-pack writer
logic.

## Maintenance Checklist

Before committing fixture changes, check:

- `docs/HARNESS_SHOWCASE.md` references every tracked fixture surface that the
  showcase audit expects.
- `ARTIFACT_PACK_EXCERPT.tsv` has the canonical
  `category	path	exists	role` header.
- TSV `exists` values are `true` or `false`.
- the paired Markdown and TSV excerpt rows stay synchronized.
- copied files do not contain local absolute paths.
- binary evidence is summarized unless the binary is intentionally tracked.
- the fixture remains small enough for review.

## Relation To Other Contracts

Use this guide with these docs:

- `docs/HARNESS_SHOWCASE.md` explains the reader-facing exhibit path.
- `docs/SHOWCASE_AUDIT_SCHEMA.md` explains the portable showcase audit payload.
- `docs/ARTIFACT_PACK_SCHEMA.md` explains `artifact-pack.v1` and the derived
  excerpt files.
- `docs/ARTIFACT_INTERFACE_STANDARD.md` explains how human-readable and
  machine-readable artifact surfaces should be paired.

This keeps showcase refreshes local, reviewable, and repeatable. A fixture is
good when a new reader can inspect the final output first, then follow the
stored evidence without needing access to the original private workspace.
