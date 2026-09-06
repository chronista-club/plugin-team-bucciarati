---
name: santa-method
description: 多 agent 敵対的検証 (adversarial verification) と収束 loop。文脈を共有しない独立 2 reviewer
  — Moody Blues × Sticky Fingers — が両方 PASS するまで output を出荷しない。high-stakes な成果物の ship
  前最終ゲート。
metadata:
  version: 0.20.0
  origin: Ronald Skelton (RapportScore.ai) — chronista 適合 fork (via ECC)、team-bucciarati
    統合版
  tags: verification, adversarial, dual-review, convergence, quality-gate
---

## ホスト共通の読み方

このディレクトリが共有定義の正本。Claude Code は `.claude-plugin`、Codex は `.codex-plugin` から同じ skills を読む。Grok CLI は Claude 互換形式を対象とするが実機確認待ち。
本文中の `Agent`、`Bash`、`Read` や MCP の名前は Claude 表記の例。利用中のホストで提供された同等のツールを発見して使う。存在しないツール・モデル・実行結果を仮定しない。`${CLAUDE_PLUGIN_ROOT}` の資料パスは、この skill から辿れるプラグインルートに読み替える。

# Santa Method 🎅

> **「リストを作り、二度確認する。Naughty なら Nice になるまで直す。」**

**Core principle:** 単一 agent が自身の output を review しても、生成時と同じ bias で見るので盲点は埋まらない。**文脈を共有しない 2 reviewer が両方 PASS して初めて出荷。**

## The Iron Rule

```
1 reviewer の OK は、出荷判断の根拠にならない
```

Reviewer B の PASS + Reviewer C の PASS = 出荷。それ以外は naughty。例外は作らない。

## いつ使うか / 使わないか

**使う** — output が published / deployed / consumed by end users になるとき:

- human review なしで production に ship されるコード
- 顧客向け・外部公開のドキュメント、規制・compliance・brand 制約が効く成果物
- claim / 数値 / API reference を含む文書（hallucination リスク高）
- 大型設計 plan の確定前

**使わない** — 内部 draft・探索的 research（通常 review で足りる）/ build・lint・test で検証可能なもの（`verification`）/ 意思決定の合議（`council`）/ 日常のコミット前チェック（quick: Moody Blues 単騎）

## 4 フェーズ

```
Generate → Dual Review → Verdict Gate → Fix Until Nice
```

### 🎁 Generate（生成）

通常の生成 workflow を変えない。santa は **post-generation の検証 layer** であり、生成戦略ではない。

### 👀 Dual Review — Moody Blues × Sticky Fingers

`Agent` tool で 2 reviewer を **1 message 内で並列起動**する:

- **Reviewer B = Moody Blues**（品質ゲート視点: 実測チェック + 多視点レビュー）
- **Reviewer C = Sticky Fingers**（嘘の味: claim 分解 + 敵対的検証）

定義の異なる 2 体を使うことで、同一定義 ×2 で起きる「両者が同じ盲点を持つ」reviewer agreement bias を構造的に減らす。

Critical invariants:

1. **Context isolation** — 互いの評価を見せない。会話履歴も渡さない
2. **同 input・同 rubric** — spec + 成果物 + rubric のみを両者に渡す
3. **構造化 verdict** — prose ではなく PASS/FAIL + checks（テンプレは [reference/reviewer-template.md](reference/reviewer-template.md)）

rubric の第一ソースは**調査ブリーフ / spec**（[brief-format](../team-bucciarati/reference/brief-format.md)）。無ければ reference の rubric 設計表から起こす。**vague rubric は vague review しか生まない** — 全 criterion に objective pass/fail 条件を持たせる。

### 🎯 Verdict Gate（NICE or NAUGHTY）

```
両者 verdict == "PASS" → NICE (ship)
それ以外 → NAUGHTY (issue 集約 → fix → 再 review)
```

片方だけが捕捉した issue も **real な issue** — もう一方の盲点こそ santa が排除すべき failure mode。部分点なし。

### 🔧 Fix Until Nice（収束 loop）

- flagged issues **のみ**修正する: "**Fix ONLY the flagged issues. Do not refactor.**"
- 再 review は **fresh instance**（前 round の記憶を持たせない）
- **MAX 3 iteration** — 失敗したら human に escalate。絶対に勝手に ship しない

## Batch（50+ 件の生成物）

全件 santa は cost 過剰。stratified sampling で 10-15%（最少 5 件）→ failure を型分類 → 系統 pattern に targeted fix → 再 sample → clean pass で出荷。

## 他スキルとの住み分け

| スキル | 役割 | santa との関係 |
|---|---|---|
| `verification` | deterministic checks (build/lint/test) | verification が先、santa は semantic な最終 gate |
| quick / deep レビュー | 通常のコードレビュー（深度メニュー） | 深度メニューの最上段が santa（adversarial） |
| `council` | 決定の合議 | 直交 — council = 決める、santa = 検証する |
| `systematic-debugging` | バグ調査 | 別レイヤー |

## クイックリファレンス

| Phase | 主な活動 | 完了条件 |
|---|---|---|
| **Generate** | 通常生成 | output 完成 |
| **Dual Review** | Moody Blues × Sticky Fingers 並列・同 rubric | 両方の verdict 取得 |
| **Verdict Gate** | NICE or NAUGHTY 判定 | 両者 PASS or fix loop へ |
| **Fix Until Nice** | flagged のみ修正 → fresh 再 review | NICE 到達 or 3 iter で escalate |

詳細（reviewer prompt テンプレ、rubric 設計表、failure modes、metrics）: [reference/reviewer-template.md](reference/reviewer-template.md)

## ホスト差分

独立した2名の reviewer をホストのサブエージェント機能で起動する。Claude の Agent やモデル名は例であり、利用可能な既定モデルと対応する委譲ツールを使う。独立実行が利用できなければ、その制約を伝え、独立レビュー完了と判定しない。
