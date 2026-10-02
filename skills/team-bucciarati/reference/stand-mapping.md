# Deep Review — 観点 ↔ Stand マッピング

レビュー深度メニューの **deep** 段の実行仕様。8観点（Pass）を複数スタンドに並列で割り振る。

## 回し方

1. メインセッションが下の割り振り表に従い、**1 message 内で並列に** Agent 呼び出しを出す
2. 各スタンドは担当 Pass の観点でレビューし、severity 付きで報告する
3. メインセッションが集約し、重複を統合して severity 順にユーザーへ報告する
4. 調査ブリーフ（[brief-format.md](brief-format.md)）があれば全スタンドに rubric として渡す

## 割り振りサマリー

| Stand | 担当 Pass |
|---|---|
| **Moody Blues** | Pass 1, 2, 4, 5, 7 |
| **Purple Haze** | Pass 3, 8 |
| **Spice Girl** | Pass 4 (testing) |
| **Sticky Fingers** | deep では使わない — adversarial（santa-method）専任 |

> Pass 6（UX / accessibility）は手動レビュー。UI 特化 Stand を将来追加する場合のホルダー。

---

## Pass 一覧 (8 観点)

### Pass 1: 全体アーキテクチャ — Moody Blues（俯瞰 pass）

- モジュール境界 / 責務分担
- 設計と実装の一致
- 依存関係 / 循環依存
- レイヤリング (data / logic / UI)

補助: 必要なら Purple Haze で個別領域を深掘り

### Pass 2: モジュールごと品質 — Moody Blues（5視点 review）

- 各 file の凝集度 / 過度な責務
- 命名の一貫性 / 公開 API の妥当性
- CLAUDE.md コンプライアンス、バグスキャン、diff 関連の変更履歴、TODO/FIXME の整合性
- 配置と再利用（追加物に既存の同等物がないか / 置き場の責務が合うか）— quick でも走る

### Pass 3: 実行時フロー / threading / IPC — Purple Haze（深掘り研究）

- thread 構成、event flow / message passing
- race condition、lock / mutex / channel の使い方
- async / await の依存関係

補助: Moody Blues（diff history で直近の変更が壊してないか）

### Pass 4: 横断的関心事 — Moody Blues + Spice Girl（testing）

- error handling（graceful fallback / silent fail）
- logging（level / verbosity / signal/noise 比）
- security（input validation / SSRF / XSS / IPC injection）
- testing（coverage gap / boundary condition）→ **Spice Girl**（t-wada 流テストピラミッド観点）

### Pass 5: 具体バグ / subtle issue — Moody Blues（信頼度スコア 75+ で報告）

- ロジックエラー / null チェック漏れ / 型不整合
- メモリリーク、競合状態、edge case（空入力 / overflow / 重複）

Severity 付け: 🔴 Major（機能破壊 / データ消失 / セキュリティ）/ 🟡 Minor / 💡 Idea

### Pass 6: UX / accessibility — 手動レビュー

- キーボードナビゲーション、screen reader 対応（aria 属性）
- フォーカス可視化、永続化、操作の一貫性

### Pass 7: ビルド / 配布 — Moody Blues（detect-ci.sh の範囲まで）

- bundle size、起動時間、hot reload 可否、開発体験（DX）
- release flow 自体は team-b の領分外（コミットライン以降）

### Pass 8: 長いモジュール / 分割整理 — Purple Haze（深掘り）+ Moody Blues（俯瞰）

- god file 検出（500+ 行で警告、800+ 行で分割推奨）
- 責務漂流（file 名と中身のズレ）、分割案の提案
