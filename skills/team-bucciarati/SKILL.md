---
name: team-bucciarati
description: JoJo Part 5 Stand-themed quality team for strong, beautiful code — research
  before development, tests and reviews after, with a three-level review depth menu
  (quick / deep / adversarial). Use this skill when asked about team composition,
  review depth, or how to call the stands.
metadata:
  triggers: チーム, ブチャラティ, スタンド, team, deep レビュー, santa レビュー
  version: 0.21.0
---

## ホスト共通の読み方

このディレクトリが共有定義の正本。Claude Code は `.claude-plugin`、Codex は `.codex-plugin` から同じ skills を読む。Grok CLI は Claude 互換形式を対象とするが実機確認待ち。
本文中の `Agent`、`Bash`、`Read` や MCP の名前は Claude 表記の例。利用中のホストで提供された同等のツールを発見して使う。存在しないツール・モデル・実行結果を仮定しない。`${CLAUDE_PLUGIN_ROOT}` の資料パスは、この skill から辿れるプラグインルートに読み替える。

# Team Bucciarati

JoJo Part 5「チーム・ブチャラティ」をモチーフにした4体のスタンド・エージェントチーム。

**開発の前後を支える品質チーム。** 前（調査）と後（テスト・レビュー・検証）で強く美しいコードに貢献する。真ん中（実装）はユーザーとメインセッションの領分。

**チームの終点は「コミット可能な working tree」。** コミット・PR・マージ・デプロイもユーザーとメインセッションの領分（team-b はコミットラインを越えない）。

## チームロスター

| Stand | User | Role | Model | 能力 |
|-------|------|------|-------|------|
| **Purple Haze** | Fugo | Research | opus | 前: 深掘り調査、副作用なし。着手前調査は調査ブリーフで締める |
| **Spice Girl** | Trish | Test Generation | sonnet | 後: t-wada流テストピラミッド |
| **Moody Blues** | Abbacchio | Quality Gate | opus | 後: ローカルチェック + 多角的コードレビュー |
| **Sticky Fingers** | Bucciarati | Adversarial Verification | opus | 後: 嘘の味 — claim 分解と敵対的検証（santa の独立レビュアー） |

> **モデル配分の考え方**: 失敗が沈黙する仕事（調査・レビュー・敵対的検証）= opus。失敗が音を立てて自己検証される仕事（テスト生成）= sonnet。さらに深い思考が必要な場面では、呼び出し時に fable へのエスカレーションを指定できる。

## レビュー深度メニュー

変更の重さに応じてレビューの厚みを選ぶ。**迷ったら quick。**

| 深度 | 呼び方 | 何が起きるか | 使いどころ |
|------|--------|------------|-----------|
| **quick**（デフォルト） | 「Moody Blues でレビューして」 | Moody Blues 単騎 — ローカルチェック + 多視点レビュー | 日常のコミット前 |
| **deep** | 「deep レビューして」 | 8観点を複数スタンドに並列割り振り（[reference/stand-mapping.md](reference/stand-mapping.md)） | 大きめの diff、リリース前の総点検 |
| **adversarial** | 「santa レビューして」 | [santa-method](../santa-method/SKILL.md) — Moody Blues × Sticky Fingers の独立 dual review。両者 PASS まで出荷しない | 本番直行・外部公開の high-stakes |

どの深度でも、調査ブリーフ / spec（[reference/brief-format.md](reference/brief-format.md)）があれば rubric として渡す — **前で立てた基準で後を裁く。**

## 使い方

各スタンドは独立したエージェントとして直接呼び出す:

- 「Purple Haze で調べて」→ 深掘り調査（副作用なし）。着手前調査なら調査ブリーフ形式で締める
- 「Spice Girl でテスト書いて」→ テストリスト設計・テスト生成
- 「Moody Blues でレビューして」→ コミット前のローカル品質ゲート（quick）
- 「santa レビューして」→ Moody Blues × Sticky Fingers の敵対的検証（adversarial）

## MCP ツール連携

各スタンドは利用可能な MCP ツールを活用して能力を強化する。詳細は [reference/mcp-tools.md](reference/mcp-tools.md) を参照。

| MCP | 用途 | 使うスタンド |
|-----|------|-------------|
| **gitnexus** | コードベースナレッジグラフ | 全スタンド |
| **sem** | エンティティレベルのコードインテリジェンス | Purple Haze, Moody Blues, Spice Girl, Sticky Fingers |
| **context7** | ライブラリドキュメント | Purple Haze, Spice Girl |

> 全て**オプショナル** — MCP が利用不可でも各スタンドは動作する。

- 副作用ガード（コミットライン・破壊コマンド）のフック定義: [reference/hooks.md](reference/hooks.md)
- deep レビューの実行仕様（観点 ↔ Stand 割り振り）: [reference/stand-mapping.md](reference/stand-mapping.md)
- 調査ブリーフのフォーマット: [reference/brief-format.md](reference/brief-format.md)
- スタンドパラメータ（JoJo フレーバー）: [reference/stand-params.md](reference/stand-params.md)

## 連携ルール

1. **責務分離** — 各スタンドは自分の責務のみ実行し、他のスタンドの領域に踏み込まない
2. **コミットラインを越えない** — どのスタンドも commit / push / PR / deploy をしない
3. **santa の独立性** — dual review 中、Moody Blues と Sticky Fingers は互いの評価を見ない（メインセッションが集約する）

## Claude 以外でのチーム実行

ロスター表の opus / sonnet と agents frontmatter は Claude の配分。他ホストでは既定モデルを使い、対応モデルを捏造しない。サブエージェント機能があれば `agents/<role>.md` 本文を指示として渡す。無ければ同名の共有 role skill を直接使い、単一セッションの検証であることを明記する。独立レビューとは扱わない。
