# 調査ブリーフ — 前→後の背骨

Purple Haze の**着手前調査**の出力フォーマット。実装後のレビュー（Moody Blues / santa-method）で、このブリーフが**そのまま rubric になる** — 前で立てた基準で後を裁く。

## フォーマット

```markdown
## Research Brief: <対象>

### 目的（Why）
[この変更/機能が解決する問題を1-3文で]

### 期待される挙動（Expectations）
[実装が満たすべき振る舞い。後で pass/fail 判定できる粒度で列挙]
- E1: ...
- E2: ...

### 制約（Constraints）
[守るべき境界 — アーキテクチャ / 互換性 / 性能 / セキュリティ / CLAUDE.md ルール]
- C1: ...

### 設計判断（Decisions）
[選んだ方針とその理由。棄却した代替案も1行で]
- D1: ...（棄却: ...）

### 非スコープ（Out of Scope）
[今回やらないこと — レビューで「無い」と指摘されないための明示]

### 検証観点（Verification）
[レビュー時に rubric の criterion になる項目。各項目に objective な pass 条件]
- V1: ...（pass 条件: ...）
```

## rubric への変換規則

- Expectations / Constraints / Verification の各項目 → rubric criterion（1:1）
- pass 条件が主観的な項目は書き直す（「きれいに」→「関数は50行以下」のように実測可能に）
- レビュー依頼時は**ブリーフを添付するだけでよい** — rubric を別途書き起こさない

## 運用

| 誰が | いつ | 何をする |
|------|------|---------|
| **Purple Haze** | 着手前調査（「実装前に調べて」系） | レポートをこの形式で締める |
| **Moody Blues** | ブリーフ付きでレビュー依頼されたら | 視点6「ブリーフ照合」として各項目を PASS/FAIL 判定 |
| **santa-method** | adversarial レビュー | rubric の第一ソースとして両レビュアーに渡す |

> ブリーフが無い場合も各レビューは通常通り動く — 背骨はあれば強くなる補助線であり、必須要件ではない。
