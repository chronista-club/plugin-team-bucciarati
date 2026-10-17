# 02. ロール本文の参照を既存検査へ含める

> **Status**: Active
> **Related**: `mem_1Cg7qNf32jB4JLHHGHfnYH`（前提の再検証と構造による改善）
> **対象**: `agents/moody-blues.md`, `tests/test_distribution.py`

## 判断

Moody Blues の配置レビューに残っていた旧ツール名を、既存の [MCP tools reference](../../skills/team-bucciarati/reference/mcp-tools.md) への相対リンクに置き換える。本文にツール一覧を複写せず、接続中の仕様を確かめる手順は既存referenceで管理する。

既存のローカルMarkdownリンク検査に `agents/` を含める。新しい汎用lintや全MCPの固定レジストリは作らない。検査対象のリンクを持つ最小fixtureで、リンク先がある時は通り、消すと既存検査が失敗することを回帰テストにする。

## 保証する範囲

ファイルへのMarkdownリンクが解決できることを検査する。リンク先本文の意味、現行APIとの一致、見出しアンカーの存在は保証しない。旧ツール名が復活しないという自然言語の意味検査でもない。説明の正本を一箇所に寄せ、参照切れだけを機械で防ぐ。

## Status log

- 2026-10-17: 既存検査ではagentsの欠落参照を検出できないREDを確認。agentsを対象に含めてGREENを確認。未リリース。

- 2026-10-17: v0.21.2 でロール参照の整理と検査を出荷。
