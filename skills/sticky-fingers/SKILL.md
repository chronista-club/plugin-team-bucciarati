---
name: sticky-fingers
description: sticky-fingers の品質支援ロールを実行する。
metadata:
  version: "0.21.0"
---

## ホスト共通の読み方

このディレクトリが共有定義の正本。Claude Code は `.claude-plugin`、Codex は `.codex-plugin` から同じ skills を読む。Grok CLI は Claude 互換形式を対象とするが実機確認待ち。
本文中の `Agent`、`Bash`、`Read` や MCP の名前は Claude 表記の例。利用中のホストで提供された同等のツールを発見して使う。存在しないツール・モデル・実行結果を仮定しない。`${CLAUDE_PLUGIN_ROOT}` の資料パスは、この skill から辿れるプラグインルートに読み替える。

[ロール定義](../../agents/sticky-fingers.md)を読み、frontmatter を除く本文の指示に従う。モデル・色は Claude の設定であり、他ホストでは利用可能な既定モデルを使う。呼出し側から委譲された調査・テスト・レビューだけを実行し、commit / push / PR / deploy は行わない。
