# Santa Method — Reviewer テンプレートと rubric 設計

## Reviewer prompt テンプレート

Moody Blues / Sticky Fingers を Agent tool で起動する際、それぞれに以下を渡す（相手の存在・評価には触れない）:

```text
You are an independent quality reviewer. You have NOT seen any other review of this output.

## Task Specification
{task_spec}

## Output Under Review
{output}

## Evaluation Rubric
{rubric}

## Instructions
Evaluate the output against EACH rubric criterion. For each:
- PASS: criterion fully met, no issues
- FAIL: specific issue found (cite the exact problem)

Return your assessment as structured JSON:
{
  "verdict": "PASS" | "FAIL",
  "checks": [
    {"criterion": "...", "result": "PASS|FAIL", "detail": "..."}
  ],
  "critical_issues": ["..."],
  "suggestions": ["..."]
}

Be rigorous. Your job is to find problems, not to approve.
```

## Rubric 設計（最重要 input）

調査ブリーフ / spec があれば、その Expectations / Constraints / Verification を criterion に 1:1 変換する。無ければこの表から起こす:

| Criterion | Pass Condition | Failure Signal |
|---|---|---|
| 事実精度 | 全 claim が出典で検証可能 | 捏造数値、存在しない version、存在しない API |
| Hallucination-free | 捏造 entity/quote/URL/reference なし | 存在しないリンク、出典のない quote |
| 完全性 | spec の全要件をカバー | section 抜け、edge case 欠落 |
| Compliance | project 制約（CLAUDE.md 等）を pass | 禁止用語、tone 違反、規約違反 |
| 内部一貫性 | output 内で矛盾なし | section A と B が食い違う |
| 技術的正しさ | code がコンパイル/動作、algorithm 健全 | syntax error、logic bug、複雑度誤認 |

**領域特化の拡張**:

- **コード**: type safety / error handling / security（secret 露出、injection）/ 新 path のテストカバレッジ
- **形式検証（Lean 4 / Aeneas / Quint）**: [formal-verification スキル](../../formal-verification/SKILL.md) の基準 — 全定理 `#print axioms` による空公理（手書き Lean は `does not depend on any axioms`、Aeneas は `sorryAx`/`Classical.choice` 不使用）/ 空虚な真（vacuous truth）の排除 / 実コードとモデルの分岐一致 / Quint 比較モード期待表の `ng` が明示的な `Invariant violated` で出ること / Aeneas `--mutation-test` の感度 / README 対応表と信頼境界の正確性
- **コンテンツ/マーケ**: brand voice / SEO / 商標誤用 / CTA
- **規制対応**: 結果保証なし / 必須 disclaimer / 認可用語 / 司法管轄言語

## Failure Modes と緩和策

| Failure Mode | 症状 | 緩和 |
|---|---|---|
| 無限 loop | reviewer が新 issue を出し続ける | MAX 3 iter で escalate |
| Rubber stamp | 両者が全部 PASS を連発 | adversarial prompt: "find problems, not approve" |
| Subjective drift | スタイル好みを fail 化 | rubric を objective に絞る |
| Fix regression | A 修正で B 発生 | fresh reviewer が次 round で検出 |
| Agreement bias | 両者が同じ盲点 | 定義の異なる 2 体（MB × SF）で軽減。critical なら 3 人目 or human |
| Cost 爆発 | 大型 output で iter 過多 | batch sampling、budget cap |

## Metrics（振り返り用）

- **First-pass 率**: round 1 で NICE になる %（target: >70%）
- **平均 iter to convergence**（target: <1.5）
- **Reviewer agreement 率**: 両者一致 issue / 片方だけ issue（低 = rubric が緩い）
- **Escape 率**: ship 後に発見された santa がキャッチすべき issue（target: 0）

## creo-memories 連携

- 系統的 failure pattern（hallucination 多発等）→ `learning` として記録
- rubric 改善 → `process` として記録
