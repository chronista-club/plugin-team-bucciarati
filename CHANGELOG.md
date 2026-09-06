# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.20.0] - 2026-09-06

- 新しい plugin-team-bucciarati リポジトリを正本とし、Claude Code / Codex の共有 skills と配布定義を追加。
- ホスト固有の前提を明記し、検証・CI・安定配布経路を整備。

## [Unreleased]

## [0.19.0] - 2026-09-02

### Added
- **スキル `santa-method` (v1.0.0)** を claude-plugin-chronista-style から移設: 多 agent 敵対的検証 — 独立した 2 reviewer (文脈非共有の並列 subagent) が両方 PASS するまで出荷しない収束 loop。「レビュー系は agent team プラグインに凝集させる」裁定 (2026-09-01) による。中身は無改変で移動、chronista 流の slim 化は本 repo の次回棚卸しで行う
- `skills/team-bucciarati/reference/stand-mapping.md`: レビュー観点 (Pass 1〜8) ↔ Stand の対応表。chronista-style の code-review スキル削除 (汎用レビューは Claude Code 標準 /code-review へ) に伴い、Stand 固有の知識だけをこちらへ移設

- **Phase 2 レビュー・調査・テスト再設計**:
  - **Sticky Fingers 復活・転身**: 「嘘の味」敵対的検証スタンド（Adversarial Verification / opus）として新規定義 — santa-method の Reviewer C。ロスター 3 → 4 体。定義の異なる 2 レビュアー（Moody Blues × Sticky Fingers）で reviewer agreement bias を構造的に低減
  - **レビュー深度メニュー**: quick（Moody Blues 単騎）/ deep（8観点並列）/ adversarial（santa dual）を SKILL.md に設置。自然文で呼び分け、オーケストレーター無しでメインセッションが dispatch
  - **調査ブリーフ（前→後の背骨）**: `reference/brief-format.md` を新設。Purple Haze の着手前調査がそのままレビューの rubric になる（Moody Blues に視点5「ブリーフ照合」を追加）
  - **santa-method v2.0.0**: 326 → 98 行に slim 化し、Moody Blues × Sticky Fingers の dual review に正式接続。reviewer テンプレ・rubric 設計・failure modes は `reference/reviewer-template.md` へ分割
  - `reference/stand-mapping.md` を deep レビューの実行仕様として本格改稿（割り振りサマリー + 回し方を明記）
  - `reference/mcp-tools.md` の現実合わせ: serena → sem（エンティティレベルのコードインテリジェンス）

- **`team.kdl` SSOT 化 + `teamb_check` ドリフト検出器**: ロスター・境界の構造化ファクトを team.kdl に一本化し、`scripts/check-teamdef.sh` で全ドキュメントとの整合を機械検証 (#10)
- **nightly 積み方式のリリースフロー**: 昼は main に積み、毎晩 23:30 に品質ゲート付きで nightly prerelease を自動棚卸し。安定版のみが marketplace 経由でユーザーに届く (#13)

### Changed
- **Moody Blues を sonnet → opus に格上げ**: レビューの失敗は沈黙する（見逃しは誰も拾わない）ため、主役の仕事に主力モデルを充てる。テスト生成（Spice Girl）は失敗が音を立てて自己検証されるので sonnet 継続
- **Phase 1 減量リファクタリング**: 半年の使用実態（ほぼレビュー、たまに調査・テスト）に合わせ、チームを「開発の前後（調査・テスト・レビュー）を支える品質チーム」に再編。ロスターを 7 体 → 3 体（Purple Haze / Spice Girl / Moody Blues）に縮小。実装（真ん中）はユーザーとメインセッションの領分
- `team.kdl`: pipelines ブロックを撤去し、scope を新スコープに更新。teamb_check からパイプライン検証（旧 Section 3）を削除し、frontmatter / CHANGELOG 抽出のユニットテストを追加
- Rust crate を `teamb-metrics` → `teamb-check` にリネームし、依存を 3 つ（anyhow / club-kdl / serde_json）に削減

### Removed
- **実装系スタンド 3 体**: Gold Experience（実装）/ Sticky Fingers（リファクタリング）/ Sex Pistols（並列コード作業）— 「SF を敵対的レビュアーに転身」案は Phase 2 の設計カードとして温存
- **Aerosmith（オーケストレーター）**: /dispatch コマンド、パイプライン定義（Finish / Forge / Polish / Barrage / Research）、VP Radar 連携ごと削除。スタンドは直接呼び出しに一本化
- **teamb-metrics MCP サーバー + improve スキル**: main.rs（teamb_measure / teamb_decide / teamb_log）、4.9MB の追跡バイナリ、.mcp.json を削除（`${CLAUDE_PLUGIN_ROOT}` 未展開による起動失敗も解消）
- reference の孤児 4 ファイル: pipelines.md / worker-conventions.md / vp-canvas.md / stand-context.md

### Fixed
- teamb_check が CHANGELOG の `## [Unreleased]` を最新版として誤認し、nightly 品質ゲート（check-teamdef）が恒常的に失敗するバグを修正 (#15)

## [0.18.0] - 2026-07-09

### Changed
- **スコープ再定義**: team-b を「強く美しいコードに貢献するレイヤーまで」に限定。チームの終点は「コミット可能な working tree」— commit / push / PR / merge / deploy はどのスタンドも行わない（コミットライン厳守）
- **Sticky Fingers**: Shipping (commit → PR → merge) → **Refactoring** に転身。ジッパー = 分解・移動・再結合。挙動を変えずに構造を美しくする（安全網確認 → 一手ずつ → 再結合検証）
- **Gold Experience**: Deploy (build → migrate → deploy → health check) → **Implementation** に転身。仕様・Issue という無機物に生命を吹き込み、コードベースの流儀に沿った生きたコードを実装する（全 green までローカル検証）
- **Sex Pistols**: 並列ワーカー管理（vp lane / ccwire / TUI 等のセッションインフラ）→ **並列コード作業**に再スコープ。Agent ツールの並列サブエージェントで一斉 codemod・独立リファクタを実行し、統合検証で締める
- **Moody Blues**: ローカル品質ゲートに純化。PR コメント投稿を廃止（レポートはユーザーへの報告のみ）、Verdict を SHIP IT → COMMIT READY に変更
- **Aerosmith / /dispatch**: パイプラインを再定義 — Finish（デフォルト・仕上げ）/ Forge（実装一式）/ Polish(構造改善) / Barrage（並列一斉）/ Research。Issue は要件ソースとして読み取りのみ（ステータス更新・クローズ廃止）
- **StandContext**: artifacts を diff_summary / tests_status / checks_status に変更（pr_number / deploy_url / ci_status を削除）
- **hooks**: スタンド別ガード → 全スタンド共通の「コミットライン・ガード」（git commit/push/merge, gh pr をブロック）+ 破壊コマンド・ガードに再編
- **CLAUDE.md**: 構成図の stale 記述を修正（marketplace.json / skills.txt への言及を削除、mcp-server / scripts を追記）
- **モデル配分**: Gold Experience（実装）と Sticky Fingers（リファクタ）を sonnet → opus に格上げ。思考の深さが質を決める仕事 = opus、規律が質を決める頻出の仕事 = sonnet の方針。さらに深い思考が必要な場面は呼び出し時に fable を指定

## [0.17.2] - 2026-05-02

### Fixed
- **Install error 修正**: plugin.json の `mcpServers` を string path (`"${CLAUDE_PLUGIN_ROOT}/.mcp.json"`) で指定していたため schema validation で `Invalid input` エラー。string path 形式は公式仕様で未サポート。フィールドを削除し、`.mcp.json` の auto-discovery に任せる形に修正
  - 公式仕様: https://code.claude.com/docs/en/mcp.md (`.mcp.json` at plugin root or inline object in `plugin.json`)
- **0.17.0 / 0.17.1 はインストール不可**。0.17.2 へ更新してください

## [0.17.1] - 2026-05-02 [BROKEN — install fails]

### Removed
- Redundant inner `.claude-plugin/marketplace.json` (single-plugin self-referential、 公式 spec 準拠で plugin.json のみに統一)

> ⚠️ このリリースは plugin.json schema 違反でインストール不可。0.17.2 で修正済み。

## [0.17.0] - 2026-05-02

### Changed
- Spec compliance: separated mcpServers to .mcp.json, added homepage, CHANGELOG, .gitignore
- Dropped legacy skills.txt
