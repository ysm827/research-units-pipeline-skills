# research-units-pipeline-skills

> 语言： [English](README.md) | **简体中文**

这个项目是一套 Auto Research Harness。

它用 file-first 的方式，把开放式研究和写作目标转成协议化执行、持久化 artifacts、可评估 evidence surfaces 和可复用 project knowledge。模型负责语义判断；harness 负责提供约束，让这些判断可以恢复、审计、比较和持续改进。

## Operating Model

这个架构最好先看成一个五层金字塔：

| 层级 | 在本项目里的含义 | 当前 repo surface |
|---|---|---|
| Learning Layer | 可复用的项目记忆 | `docs/adr/`、`docs/PROJECT_LANGUAGE.md`、`docs/PATTERN_REGISTER.md`、roadmap、validation |
| Evidence Loop | 证明一次 run 是否健康到可以继续 | doctor、audit、audit-diff、quality gates、manifests |
| Execution Ledger | 可恢复、可检查、可交接的每次 run 状态 | `workspaces/<name>/`、`UNITS.csv`、`STATUS.md`、`DECISIONS.md`、outputs |
| Workflow Protocol | 被约束过的任务形态 | `pipelines/*.pipeline.md`、`templates/UNITS.*.csv`、taxonomy |
| Capability Surface | 可复用的语义判断能力 | `.codex/skills/`、references、skill scripts |

如果你想先理解研究纲领，请看 [docs/AUTO_RESEARCH_HARNESS.md](docs/AUTO_RESEARCH_HARNESS.md)；如果你想看金字塔模型，请看 [docs/HARNESS_OPERATING_MODEL.md](docs/HARNESS_OPERATING_MODEL.md)。如果你想先看最终交付物，再反向理解中间过程，请从 [docs/HARNESS_SHOWCASE.md](docs/HARNESS_SHOWCASE.md) 开始。

这里的 self-improve 是有边界的：最终交付物如果变差，不应该只是重写一遍，而是要反推到中间 artifact、workflow protocol、skill、模型能力限制或 harness fallback 的缺陷，再通过可见合同和验证来修复。详细模型见 [docs/HARNESS_IMPROVEMENT_LOOP.md](docs/HARNESS_IMPROVEMENT_LOOP.md)。中间产物的接口标准见 [docs/ARTIFACT_INTERFACE_STANDARD.md](docs/ARTIFACT_INTERFACE_STANDARD.md)。

## 这个仓库当前覆盖什么

目前代码库主要围绕 8 条 workflow 合同展开：

| 工作流 | 适用场景 | 默认交付物 | English | 中文 |
|---|---|---|---|---|
| `arxiv-survey` | 证据优先的文献综述写作，先拿 draft 和 evidence stack，不急着出 PDF | `output/DRAFT.md` | [Guide](readme/arxiv-survey.md) | [说明](readme/arxiv-survey.zh-CN.md) |
| `arxiv-survey-latex` | 同一条 survey 工作流，但从一开始就把 LaTeX/PDF 交付纳入合同 | `output/DRAFT.md`、`latex/main.tex`、`latex/main.pdf` | [Guide](readme/arxiv-survey.md) | [说明](readme/arxiv-survey.zh-CN.md) |
| `research-brief` | 快速理解一个主题，并产出可读的 research briefing / reading path | `output/SNAPSHOT.md` | [Guide](readme/research-brief.md) | [说明](readme/research-brief.zh-CN.md) |
| `paper-review` | 对单篇 paper / manuscript 做可追溯的评估、组会 review 或 referee-style critique | `output/REVIEW.md` | [Guide](readme/paper-review.md) | [说明](readme/paper-review.zh-CN.md) |
| `evidence-review` | 带 protocol、screening、extraction 的证据综述 / evidence synthesis | `output/SYNTHESIS.md` | [Guide](readme/evidence-review.md) | [说明](readme/evidence-review.zh-CN.md) |
| `idea-brainstorm` | 基于文献的研究方向发现与讨论备忘录 | `output/REPORT.md` | [Guide](readme/idea-brainstorm.md) | [说明](readme/idea-brainstorm.zh-CN.md) |
| `source-tutorial` | 把网页/PDF/笔记/repo docs 等多源资料重构成 reader-first tutorial，并输出 PDF 与 Beamer slides | `output/TUTORIAL.md`、`latex/main.pdf`、`latex/slides/main.pdf` | [Guide](readme/source-tutorial.md) | [说明](readme/source-tutorial.zh-CN.md) |
| `graduate-paper` | 将现有中文毕业论文材料重构为论文工程流程 | pipeline + thesis skills | [Guide](readme/graduate-paper.md) | [说明](readme/graduate-paper.zh-CN.md) |

这八条工作流共享同一套基本架构：

- `pipelines/` 定义阶段合同、目标工件和所需 skills。
- `.codex/skills/` 存放可复用 skills。
- `workspaces/` 存放每次 run 的输出和中间产物。
- `readme/` 存放按功能拆分的说明文档。

现在请直接使用这些最新 workflow 名称。旧别名已经不再参与 active routing。

## Skills 和 Harness

这个仓库分两层：

- **Skills** 是语义执行单元。它们描述研究判断：该读什么、产出什么工件、验收标准是什么、哪些 guardrail 不能破。
- **Harness** 是围绕 skills 的确定性支撑层。它负责初始化 workspace、运行 unit scripts、验证 pipeline 合同、检查生成的依赖图、诊断 workspace 状态、记录每个 unit 的输出 manifest，并恢复中断后遗留的 `DOING` unit。

改项目时保持这个分工：领域判断和写作政策放在 skills；可重复的校验、恢复和编排放在 harness。

## 核心概念

- `Pipeline`：工作流合同，定义阶段、工件、检查点和所需 skills。
- `Skill`：可复用能力，带有明确的输入、输出、验收条件和 guardrails。
- `Workspace`：一次 run 的工作目录，位于 `workspaces/<name>/`，所有生成工件都写在这里。

这个仓库最重要的设计选择是 artifact-first。模型不是靠“记住整个流程”在工作，而是把中间结构、证据和 review 结果落盘，让后续阶段可以在这些工件上继续推进。

## 什么时候该用哪条工作流

当目标是写一篇严肃综述，并且需要显式检索、结构审阅、evidence packs 和写作自循环，但暂时不要求 PDF 时，用 `arxiv-survey`。

当同一条综述流程从一开始就要求最终给出 LaTeX/PDF 交付时，用 `arxiv-survey-latex`。

当目标是快速搞懂一个方向、整理关键主题，并给出后续阅读路径时，用 `research-brief`。

当输入是一篇单独的 paper / manuscript，目标是判断 claim、evidence、novelty 和风险时，用 `paper-review`。

当目标是在显式 protocol、screening 和 extraction 之上产出可审计的证据综述时，用 `evidence-review`。

当目标还不是写论文，而是把一个主题转成“适合和导师/PI 讨论的、由文献支撑的研究方向备忘录”时，用 `idea-brainstorm`。

当你已经有网页、PDF、笔记、repo docs 或文档站点，想把这些材料重构成一个更适合阅读和讲解的教程时，用 `source-tutorial`。

当你已经有毕业论文模板、现有 TeX、Overleaf 草稿、PDF、图表或已有 paper，需要把这些材料重组成一条中文学位论文工作流时，用 `graduate-paper`。这条路径目前也是主要工作流里自动化程度最低的一条。

## 三条并列的 Review 产品

`research-brief`、`paper-review` 和 `evidence-review` 现在是三条并列入口，不再是一个流程里的轻重档位。

| 工作流 | 常见输入形态 | 内部数据流 | 交付物 |
|---|---|---|---|
| `research-brief` | topic prompt、小论文池、queries seed | topic -> small core set -> outline -> compact briefing | `output/SNAPSHOT.md` |
| `paper-review` | 单篇 paper / manuscript | manuscript -> claims -> evidence gaps + novelty matrix -> review | `output/REVIEW.md` |
| `evidence-review` | review question + candidate pool | question -> protocol -> screening -> extraction + bias -> synthesis | `output/SYNTHESIS.md` |

它们分别服务三种不同需求：

- `research-brief`：快速入门、快速读懂、快速拿到阅读路径
- `paper-review`：对单篇论文做可追溯评估
- `evidence-review`：对一批候选研究做可审计证据综合

## 怎么使用这个仓库

1. 在这个仓库里启动 Codex。
2. 选择一条工作流，或者直接描述你想要的结果。
3. 让对应 pipeline 把工件写入一个 workspace。
4. 在关键 checkpoint 打开对应文件检查，再决定是否继续。

典型 prompt：

```text
Write a LaTeX survey about embodied AI and show me the outline first.
```

```text
Use the research-brief workflow to give me a one-page briefing on test-time adaptation for robotics.
```

```text
Use the paper-review workflow to critique this manuscript and give me a lab-style review.
```

```text
Use the evidence-review workflow to run a PRISMA-style review on LLM agents for education.
```

```text
Brainstorm literature-grounded research ideas around embodied agents for home robotics.
```

```text
使用 source-tutorial pipeline，把关于 robot learning 的网页和 repo docs 重构成一个 tutorial，并输出 PDF 与 slides。
```

```text
Use the graduate-paper workflow to reorganize my Chinese thesis materials before rewriting chapters.
```

如果你想更明确地控制流程，也可以直接钉住 pipeline：

- [pipelines/arxiv-survey.pipeline.md](pipelines/arxiv-survey.pipeline.md)
- [pipelines/arxiv-survey-latex.pipeline.md](pipelines/arxiv-survey-latex.pipeline.md)
- [pipelines/research-brief.pipeline.md](pipelines/research-brief.pipeline.md)
- [pipelines/paper-review.pipeline.md](pipelines/paper-review.pipeline.md)
- [pipelines/evidence-review.pipeline.md](pipelines/evidence-review.pipeline.md)
- [pipelines/idea-brainstorm.pipeline.md](pipelines/idea-brainstorm.pipeline.md)
- [pipelines/source-tutorial.pipeline.md](pipelines/source-tutorial.pipeline.md)
- [pipelines/graduate-paper-pipeline.md](pipelines/graduate-paper-pipeline.md)

## Developer Harness

修改 pipeline 合同或 skill IO 前，建议先跑：

```bash
python -m pytest -q
python scripts/validate_repo.py
python scripts/audit_skills.py --fail-on WARN
python scripts/audit_skills.py --review-category template_placeholder --limit 20
python scripts/audit_skills.py --summary-only
python scripts/generate_skill_graph.py
python scripts/readiness_audit.py --progress workspaces/harness-upgrade/GOAL_STATUS.md
python scripts/showcase_audit.py --strict
python scripts/pipeline.py doctor --workspace workspaces/<name>
python scripts/pipeline.py doctor --workspace workspaces/<name> --write
python scripts/pipeline.py audit --workspace workspaces/<name> --write
python scripts/pipeline.py audit-diff --before workspaces/<name>/output/RUN_AUDIT.before.json --after workspaces/<name>/output/RUN_AUDIT.json --write
python scripts/pipeline.py improve --workspace workspaces/<name> --write
python scripts/pipeline.py pack --workspace workspaces/<name> --write
python scripts/pipeline.py pack --workspace workspaces/<name> --write-excerpt
```

`validate_repo.py --strict --no-check-quality` 是可执行 pipelines 的阻塞合同检查。`audit_skills.py --fail-on WARN` 是本地 skill hygiene check：WARN 级 finding 应当对应可执行修复，INFO 级 finding 保持为 review signal，并按 `review_category` 和 `next_action` 分组，例如 syntax placeholder、reference example、placeholder policy、asset palette、anti-pattern guidance。使用 `--review-category` 和 `--limit` 可以只查看一个 review queue，避免打印完整报告；只需要分组计数时用 `--summary-only`。`readiness_audit.py` 检查最终 harness closure audit 前需要的证据面；它不跑测试，也不会标记 goal 完成。`showcase_audit.py` 检查 `example/` 下的可移植示例，让先看交付物的展示路径同时具备真实输出、protocol link、evidence report、可视化 lineage asset 和保守的 coverage scorecard。`pipeline.py doctor` 是 workspace 级 harness 检查：它会展示当前 checkpoint、unit 状态计数、下一个可运行 unit、缺失依赖、DONE unit 缺失输出、typed remediation category 和 next action。加上 `--write` 后，同一份诊断会沉淀到 `output/DOCTOR_REPORT.md` 和 `output/DOCTOR_REPORT.json`。`pipeline.py audit --write` 会生成 `output/RUN_AUDIT.md` 和 `output/RUN_AUDIT.json`，作为 compact run ledger，覆盖 workspace 文件、unit 状态、target artifact coverage、manifests、近期 harness reports 和 audit verdict。脚本型 unit 还会写入 `output/unit_logs/<unit>.<skill>.manifest.json`，记录输出哈希，方便追踪。

`pipeline.py audit-diff` 会比较两个有效的 `RUN_AUDIT.json`，加上 `--write` 后会在 after payload 旁写入 `RUN_AUDIT_DIFF.md` 和 `RUN_AUDIT_DIFF.json`。当一次 repair 或后续 unit 应当证明 target artifacts、unit status、manifests 或 harness issues 真的改善，而不只是发生变化时，用这个命令。`pipeline.py improve --write` 会生成 `output/IMPROVEMENT_REPORT.md` 和 `output/IMPROVEMENT_REPORT.json`，把 doctor / run-audit evidence 转成上游接口、repair surface 和 validation command。`pipeline.py pack --write` 会生成 `output/ARTIFACT_PACK.md` 和 `output/ARTIFACT_PACK.json`，作为先看交付物的 manifest，索引 target artifacts、unit outputs、run ledger、harness reports 和 unit manifests，但不导出压缩包。如果要给 fixture 或 review note 生成可移植的 Markdown/TSV handoff excerpt，可以加 `--write-excerpt`。

如果要理解架构层，请先看 [docs/AUTO_RESEARCH_HARNESS.md](docs/AUTO_RESEARCH_HARNESS.md)，再看 [docs/HARNESS_OPERATING_MODEL.md](docs/HARNESS_OPERATING_MODEL.md)、[docs/HARNESS_ARCHITECTURE.md](docs/HARNESS_ARCHITECTURE.md)、可视化层级图 [docs/HARNESS_SYSTEM_MAP.md](docs/HARNESS_SYSTEM_MAP.md)、先看交付物的展示路径 [docs/HARNESS_SHOWCASE.md](docs/HARNESS_SHOWCASE.md)、命令级运行示例 [docs/HARNESS_RUN_WALKTHROUGH.md](docs/HARNESS_RUN_WALKTHROUGH.md)、有边界的 self-improvement 模型 [docs/HARNESS_IMPROVEMENT_LOOP.md](docs/HARNESS_IMPROVEMENT_LOOP.md)，以及中间产物接口标准 [docs/ARTIFACT_INTERFACE_STANDARD.md](docs/ARTIFACT_INTERFACE_STANDARD.md)。分阶段升级路径在 [docs/HARNESS_ROADMAP.md](docs/HARNESS_ROADMAP.md)，当前完成证据总账在 [docs/HARNESS_READINESS.md](docs/HARNESS_READINESS.md)，快速 readiness audit 合同在 [docs/HARNESS_READINESS_AUDIT.md](docs/HARNESS_READINESS_AUDIT.md)，外部模式到本 repo 的映射在 [docs/PATTERN_REGISTER.md](docs/PATTERN_REGISTER.md)，`skill-audit-report.v1` 字段合同在 [docs/SKILL_AUDIT_SCHEMA.md](docs/SKILL_AUDIT_SCHEMA.md)，`doctor-report.v1` 字段合同在 [docs/DOCTOR_REPORT_SCHEMA.md](docs/DOCTOR_REPORT_SCHEMA.md)，`run-audit.v1` 字段合同在 [docs/RUN_AUDIT_SCHEMA.md](docs/RUN_AUDIT_SCHEMA.md)，`run-audit-diff.v1` 字段合同在 [docs/RUN_AUDIT_DIFF_SCHEMA.md](docs/RUN_AUDIT_DIFF_SCHEMA.md)，`harness-showcase-audit.v1` 字段合同在 [docs/SHOWCASE_AUDIT_SCHEMA.md](docs/SHOWCASE_AUDIT_SCHEMA.md)，`improvement-report.v1` 字段合同在 [docs/IMPROVEMENT_REPORT_SCHEMA.md](docs/IMPROVEMENT_REPORT_SCHEMA.md)，`artifact-pack.v1` 字段合同在 [docs/ARTIFACT_PACK_SCHEMA.md](docs/ARTIFACT_PACK_SCHEMA.md)。架构决策记录放在 [docs/adr/](docs/adr/)，包括 skills 与 harness 的职责分层，以及 doctor / run-audit / audit-diff / showcase-audit / improvement-report / artifact-pack JSON 决策。

## 推荐阅读路径

1. 先看这个首页，理解仓库级别的定位。
2. 先看 [docs/AUTO_RESEARCH_HARNESS.md](docs/AUTO_RESEARCH_HARNESS.md)，理解 Auto Research Harness 的核心论点。
3. 再看 [docs/HARNESS_SHOWCASE.md](docs/HARNESS_SHOWCASE.md)，先看最终交付物，再反向追溯中间 artifacts。
4. 再看 [docs/HARNESS_OPERATING_MODEL.md](docs/HARNESS_OPERATING_MODEL.md)，理解金字塔模型和系统故事。
5. 再看 [docs/HARNESS_SYSTEM_MAP.md](docs/HARNESS_SYSTEM_MAP.md)，理解层级关系和执行闭环。
6. 再看 [docs/HARNESS_RUN_WALKTHROUGH.md](docs/HARNESS_RUN_WALKTHROUGH.md)，理解一个真实初始化 workspace、doctor report、run audit、improvement report 和 artifact-pack manifest 如何串起来。
7. 再看 [docs/HARNESS_IMPROVEMENT_LOOP.md](docs/HARNESS_IMPROVEMENT_LOOP.md)，理解最终交付物的问题如何反向修复中间 artifacts 和合同。
8. 如果要新增中间 report、表格、sidecar 或 artifact pack，再看 [docs/ARTIFACT_INTERFACE_STANDARD.md](docs/ARTIFACT_INTERFACE_STANDARD.md)。
9. 如果你要改系统而不是只运行流程，再看 [docs/HARNESS_ARCHITECTURE.md](docs/HARNESS_ARCHITECTURE.md)。
10. 用 [docs/HARNESS_ROADMAP.md](docs/HARNESS_ROADMAP.md) 判断哪些升级已采纳、暂缓或下一步要做。
11. 再打开与你任务和语言对应的功能说明。
12. 然后去看 `pipelines/` 下对应的 pipeline 合同。
13. 如果你要改行为而不是只运行，再去看 `.codex/skills/` 里的相关 skills。

## 文档导航

功能说明：

| 工作流 | English | 中文 |
|---|---|---|
| `arxiv-survey` / `arxiv-survey-latex` | [readme/arxiv-survey.md](readme/arxiv-survey.md) | [readme/arxiv-survey.zh-CN.md](readme/arxiv-survey.zh-CN.md) |
| `research-brief` | [readme/research-brief.md](readme/research-brief.md) | [readme/research-brief.zh-CN.md](readme/research-brief.zh-CN.md) |
| `paper-review` | [readme/paper-review.md](readme/paper-review.md) | [readme/paper-review.zh-CN.md](readme/paper-review.zh-CN.md) |
| `evidence-review` | [readme/evidence-review.md](readme/evidence-review.md) | [readme/evidence-review.zh-CN.md](readme/evidence-review.zh-CN.md) |
| `idea-brainstorm` | [readme/idea-brainstorm.md](readme/idea-brainstorm.md) | [readme/idea-brainstorm.zh-CN.md](readme/idea-brainstorm.zh-CN.md) |
| `source-tutorial` | [readme/source-tutorial.md](readme/source-tutorial.md) | [readme/source-tutorial.zh-CN.md](readme/source-tutorial.zh-CN.md) |
| `graduate-paper` | [readme/graduate-paper.md](readme/graduate-paper.md) | [readme/graduate-paper.zh-CN.md](readme/graduate-paper.zh-CN.md) |

项目参考：

- [docs/AUTO_RESEARCH_HARNESS.md](docs/AUTO_RESEARCH_HARNESS.md)
- [docs/HARNESS_ARCHITECTURE.md](docs/HARNESS_ARCHITECTURE.md)
- [docs/HARNESS_OPERATING_MODEL.md](docs/HARNESS_OPERATING_MODEL.md)
- [docs/HARNESS_SYSTEM_MAP.md](docs/HARNESS_SYSTEM_MAP.md)
- [docs/HARNESS_SHOWCASE.md](docs/HARNESS_SHOWCASE.md)
- [docs/HARNESS_RUN_WALKTHROUGH.md](docs/HARNESS_RUN_WALKTHROUGH.md)
- [docs/HARNESS_IMPROVEMENT_LOOP.md](docs/HARNESS_IMPROVEMENT_LOOP.md)
- [docs/ARTIFACT_INTERFACE_STANDARD.md](docs/ARTIFACT_INTERFACE_STANDARD.md)
- [docs/PIPELINE_TAXONOMY.md](docs/PIPELINE_TAXONOMY.md)
- [docs/PROJECT_LANGUAGE.md](docs/PROJECT_LANGUAGE.md)
- [docs/HARNESS_ROADMAP.md](docs/HARNESS_ROADMAP.md)
- [docs/HARNESS_READINESS.md](docs/HARNESS_READINESS.md)
- [docs/HARNESS_READINESS_AUDIT.md](docs/HARNESS_READINESS_AUDIT.md)
- [docs/PATTERN_REGISTER.md](docs/PATTERN_REGISTER.md)
- [docs/SKILL_AUDIT_SCHEMA.md](docs/SKILL_AUDIT_SCHEMA.md)
- [docs/DOCTOR_REPORT_SCHEMA.md](docs/DOCTOR_REPORT_SCHEMA.md)
- [docs/RUN_AUDIT_SCHEMA.md](docs/RUN_AUDIT_SCHEMA.md)
- [docs/RUN_AUDIT_DIFF_SCHEMA.md](docs/RUN_AUDIT_DIFF_SCHEMA.md)
- [docs/SHOWCASE_AUDIT_SCHEMA.md](docs/SHOWCASE_AUDIT_SCHEMA.md)
- [docs/IMPROVEMENT_REPORT_SCHEMA.md](docs/IMPROVEMENT_REPORT_SCHEMA.md)
- [docs/ARTIFACT_PACK_SCHEMA.md](docs/ARTIFACT_PACK_SCHEMA.md)
- [docs/adr/](docs/adr/)
- [SKILL_INDEX.md](SKILL_INDEX.md)
- [SKILLS_STANDARD.md](SKILLS_STANDARD.md)

多语言文档入口页放在 `readme/README.*.md` 下，并已同步到当前这版 workflow 结构。

## 当前状态

- `arxiv-survey` / `arxiv-survey-latex` 是当前最完整的写作路径；是否需要 PDF 决定具体走哪条 survey 合同。
- `research-brief`、`paper-review` 和 `evidence-review` 现在构成 review-oriented 产品族：分别对应快速理解、单篇评估和 protocol 驱动的证据综述。
- `idea-brainstorm` 已经结构化并可执行，但它面向的是讨论型 idea memo，不是论文草稿。
- `source-tutorial` 现在就是教程类任务的主路径：以 source-grounded 的 reader-first tutorial 为主产品，同时把 article PDF 和 Beamer slides 作为正式交付层。
- `graduate-paper` 现在已经有更清晰的 pipeline 设计和第一批 thesis skills，但目前更适合作为引导式工作流框架，而不是一键全自动毕业论文生成器。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WILLOSCAR/research-units-pipeline-skills&type=Date)](https://star-history.com/#WILLOSCAR/research-units-pipeline-skills&Date)
