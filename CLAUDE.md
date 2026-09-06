# Team Bucciarati Plugin

JoJo Part 5 スタンドをモチーフにした Claude Code エージェントチームプラグイン。

**スコープ: 開発の前後（調査・テスト・レビュー・検証）で強く美しいコードに貢献するレイヤーまで。** チームの終点は「コミット可能な working tree」— 真ん中（実装）とコミット・PR・マージ・デプロイ（CI/CD 以降のフロー）はユーザーとメインセッションの領分。

## 構成

```
team.kdl            # ★ SSOT — ロスター/モデル配分/コミットライン境界の構造化ファクト
.claude-plugin/     # プラグインメタデータ (plugin.json)
agents/             # スタンドエージェント定義 (4体) — 散文の正はこちら
skills/             # スキル定義 (team-bucciarati, santa-method)
mcp-server/         # teamb-check — SSOT ドリフト検出器 (Rust)
scripts/            # 共有スクリプト (detect-ci.sh, check-teamdef.sh, nightly-release.sh)
```

## エージェント一覧

| Agent | 役割 |
|-------|------|
| Purple Haze | 前: 深層リサーチ・調査 |
| Spice Girl | 後: テスト生成 |
| Moody Blues | 後: ローカル品質チェック・コードレビュー |
| Sticky Fingers | 後: 敵対的検証 — 嘘の味（santa-method の独立レビュアー） |

## リリースフロー

nightly で開発・検証し、安定版を main + version tag + GitHub Release で配布する。旧 scripts/nightly-release.sh は過去の棚卸し手順であり、このリポジトリでは自動実行しない。

## 開発ルール

- **SSOT は `team.kdl`** — ロスター（モデル・カラー）・コミットライン境界を変更する時は必ず team.kdl から更新し、`scripts/check-teamdef.sh` でドキュメント群との整合を検証すること（コミット前必須）
- エージェント定義の散文は `agents/*.md` が正（team.kdl は構造化ファクトのみ持つ）
- スキルは `skills/<name>/SKILL.md` に配置
- バージョンは `.claude-plugin/plugin.json` で管理し、リリース時は `CHANGELOG.md` にエントリを追加すること
- どのスタンドも commit / push / PR / deploy をしない（コミットライン厳守）
- コミットメッセージは日本語
