# Snapshot: RAG Evaluation

## Scope

This brief frames retrieval-augmented generation (RAG) evaluation as a
multi-level measurement problem. The goal is not only to ask whether the final
answer is correct, but also to identify where quality is gained or lost across
retrieval, grounding, synthesis, and user-facing task success.

## Core Takeaways

- RAG evaluation should separate retrieval quality from answer quality. A
  system can retrieve relevant material and still hallucinate, or retrieve
  weak material and still produce a plausible but unsupported answer.
- Faithfulness is not identical to correctness. A faithful answer can be
  grounded in retrieved evidence yet still fail the user's actual task if the
  corpus is incomplete or the question requires synthesis beyond retrieved
  passages.
- End-to-end scores are useful for product comparison, but they hide repair
  signals. Harness-friendly evaluation should preserve component-level traces:
  query, retrieved documents, cited spans, answer, rubric result, and failure
  class.
- Human preference, citation accuracy, and task completion should be treated as
  complementary evidence surfaces rather than a single universal metric.

## Suggested Evaluation Axes

| Axis | What it tests | Typical artifact |
|---|---|---|
| Retrieval coverage | Whether the candidate evidence set contains the needed information | ranked document list, recall-oriented labels |
| Grounding and attribution | Whether answer claims are supported by retrieved evidence | claim-to-source links, citation audit |
| Answer utility | Whether the response satisfies the user task | rubric score, pairwise preference, task success |
| Robustness | Whether quality survives paraphrase, distractors, or corpus drift | stress set, regression comparison |

## Reading Path

1. Start with RAG and dense retrieval papers to understand the architecture
   that couples retrievers with generators.
2. Move to benchmark and evaluation work that distinguishes answer correctness,
   faithfulness, and citation support.
3. Inspect recent survey or benchmark papers only after the component-level
   questions are clear; otherwise the metric landscape looks flatter than it
   is.

## Harness Implication

A useful RAG evaluation workflow should not only emit a final score. It should
emit an execution ledger: retrieved candidates, selected evidence, claim
bindings, rubric outputs, and a run audit. That makes the result repairable
when a later reviewer asks whether the failure came from retrieval, grounding,
generation, or the evaluation rubric itself.
