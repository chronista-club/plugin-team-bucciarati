# Team Bucciarati

JoJo's Bizarre Adventure Part 5 "Vento Aureo" をモチーフにした、Claude Code / Codex 向け品質支援プラグイン。

4体のスタンド・エージェントが**開発の前後**を支える — 前（調査）と後（テスト・レビュー）で強く美しいコードに貢献する品質チーム。真ん中（実装）はユーザーとメインセッションの領分。

**チームの終点は「コミット可能な working tree」。** コミット・PR・マージ・デプロイはユーザーとメインセッションの領分 — team-b はコミットラインを越えない。

## Install

```bash
claude plugin marketplace add chronista-club/chronista-plugins
claude plugin install team-bucciarati@chronista-plugins
```

## Team Roster

| Stand | User | Role | Model |
|-------|------|------|-------|
| Purple Haze | Fugo | Research | opus |
| Spice Girl | Trish | Test Generation | sonnet |
| Moody Blues | Abbacchio | Quality Gate | opus |
| Sticky Fingers | Bucciarati | Adversarial Verification | opus |

> Claude model policy: work whose failures are silent (research / review / adversarial verification) runs on opus; self-verifying work (test generation) runs on sonnet.

## Usage

Call any Stand agent directly:

```
Purple Haze で調べて
Spice Girl でテスト書いて
Moody Blues でレビューして
santa レビューして（Moody Blues × Sticky Fingers の敵対的 dual review）
```

Review depth menu — quick (Moody Blues solo) / deep (8-pass parallel) / adversarial (santa-method). See `skills/team-bucciarati/SKILL.md`.

## License

MIT

## 共通配布

Claude Code / Codex は同じ `skills/` を使います。[ホスト対応と検証範囲](docs/host-support.md)を参照してください。カタログは [chronista-plugins](https://github.com/chronista-club/chronista-plugins)。

Codex はカタログ追加後 `codex plugin add team-bucciarati@chronista-plugins` で登録する。共有 skills はホストのスキル一覧から呼び出す。
