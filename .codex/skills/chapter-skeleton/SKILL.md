---
name: chapter-skeleton
description: |
  Build a retrieval-informed chapter skeleton (`outline/chapter_skeleton.yml`) from taxonomy/core scope before stable H3 decomposition.
  **Trigger**: chapter skeleton, chapter-level outline, H2 skeleton, section-first survey, 章节骨架, 章级骨架.
  **Use when**: survey structure should stabilize chapter-level intent before subsection mapping and writing cards.
  **Skip if**: `outline/chapter_skeleton.yml` already exists and is refined.
  **Network**: none.
  **Guardrail**: NO PROSE; do not invent papers; keep output chapter-level only.
---

# Chapter Skeleton

## Load Order

Always read:
- `references/overview.md`

Use `scripts/run.py` only for deterministic materialization:
- read `outline/taxonomy.yml` for retrieval-informed topic structure
- read `GOAL.md` when present for scope hints
- emit `outline/chapter_skeleton.yml`
- preserve existing non-placeholder user work

## Inputs

- `outline/taxonomy.yml`
- Optional: `GOAL.md`

## Outputs

- `outline/chapter_skeleton.yml`

## Asset contract

- `assets/output_contract.json`

## Script

### Quick Start

- `python .codex/skills/chapter-skeleton/scripts/run.py --workspace <workspace_dir>`

### All Options

- `--workspace <dir>`: workspace containing `outline/taxonomy.yml`
- `--unit-id <id>`: optional harness metadata
- `--inputs <semicolon-separated>`: optional override from `UNITS.csv`
- `--outputs <semicolon-separated>`: optional output override; default is `outline/chapter_skeleton.yml`
- `--checkpoint <C*>`: optional harness metadata

### Examples

- Generate the chapter skeleton after taxonomy:
  - `python .codex/skills/chapter-skeleton/scripts/run.py --workspace workspaces/<ws> --inputs 'outline/taxonomy.yml;GOAL.md' --outputs 'outline/chapter_skeleton.yml'`
