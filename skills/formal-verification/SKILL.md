---
name: formal-verification
description: Chronista 流の形式検証・定理証明（Lean 4 構造モデル / Charon・Aeneas 実 Rust 抽出証明 / Quint 状態機械モデル検査と比較モード反例検証）を設計・生成・検証するスキル。開発の前後で4体のスタンド（Purple Haze / Spice Girl / Moody Blues / Sticky Fingers）が連携し、テストと並行して強く美しいコードの数学的・構造的正しさを保証する。
metadata:
  triggers: Lean, Quint, Aeneas, 形式証明, 定理証明, 形式検証, formal, モデル検査
  version: 0.21.2
---

## ホスト共通の読み方

このディレクトリが共有定義の正本。Claude Code は `.claude-plugin`、Codex は `.codex-plugin` から同じ skills を読む。Grok CLI は Claude 互換形式を対象とするが実機確認待ち。
本文中の `Agent`、`Bash`、`Read` や MCP の名前は Claude 表記の例。利用中のホストで提供された同等のツールを発見して使う。存在しないツール・モデル・実行結果を仮定しない。`${CLAUDE_PLUGIN_ROOT}` の資料パスは、この skill から辿れるプラグインルートに読み替える。

# Formal Verification — Lean 4 / Aeneas / Quint 🔬

> **「テストは具体例の正しさを示し、形式検証は法則と状態空間の正しさを示す。」**

開発したものを安全に期待通りに動かしてユーザーに届けるため、テスト（Unit / Integration / E2E）と並行して **Lean 4**・**Charon / Aeneas**・**Quint** による形式検証を行う。

Simplicity（`data` / `calculations` / `actions`）の分類に沿って3つの層を使い分ける:

| 層 | 置き場 | 対象（Simplicity） | 検証するもの |
|---|---|---|---|
| **1. Lean 4 構造モデル** | `formal/lean/` | **Calculations / Data**（純粋関数・AST・認可核・ビット演算・変換規則） | 任意の入力に対する構造法則（往復定理・単調性・直交性・フィルタ順序）と、規則を外した誤実装が壊れる反例定理 |
| **2. Charon / Aeneas 実抽出** | `formal/aeneas/` | **Rust 実装の核メソッド**（実 Cargo crate から LLBC → Lean 抽出） | 手書きモデルではなく実 Rust コードのメソッドが期待仕様（`Result.ok` を含む正常終了と値一致）を満たすこと ＋ **mutation test** による感度検証 |
| **3. Quint 状態機械モデル** | `formal/quint/` | **Actions / State Machine**（状態遷移・プロトコル・handoff・同期・ライフサイクル） | 有限状態遷移の不変条件と、**設計規則（フラグ）を1つずつ外した比較モードで期待通り反例（`ng` = `Invariant violated`）が出ること** |

---

## 2つの導線（呼び出し方）

### 導線 ①：日々のコードレビューの一部（自動で効く）

特別なコマンドを覚えなくても、通常のレビュー深度メニュー（`quick` / `deep` / `santa`）の中で形式検証が機能する:

- **quick（Moody Blues 単騎）**:
  - `detect-ci.sh` が `formal/`（または `mise` の `formal:*` タスク）を検出し、ローカルチェックで Lean / Quint / Aeneas を自動実行する。
  - 実コード（Rust / TS 等）の分岐・定数・順序を変更した diff に対し、対応する `formal/` のモデルや対応表が更新されているか（モデル・実装ドリフト）を検査する。
  - 新しい状態機械や純粋な核を追加しているのに `formal/` が未導入なら、対象候補として提案する。
- **deep（8観点並列）**:
  - Pass 4（Spice Girl: testing）でテストピラミッドと合わせて **Formal Coverage**（構造法則・状態遷移の未検証ギャップ）を点検する。
- **adversarial（santa レビュー: Moody Blues × Sticky Fingers）**:
  - `formal/` を含む成果物に対し、Sticky Fingers が「嘘の証明（公理密輸・空虚な真・モデル捏造・比較モード八百長・mutation 感度不足）」を敵対的に味見し、両者 PASS まで出荷しない。

### 導線 ②：形式検証を新規導入・拡張する（4スタンドの一貫リレー）

自然文で各スタンドを直接、またはリレーで呼び出す:

1. **【前】Purple Haze（調査・ブリーフ）**:
   - 呼び方: *「Purple Haze で形式検証のブリーフ作って」「このモジュールで Lean と Quint に入れるべき法則を調べて」*
   - 出力: 対象コードを浸透調査し、**Lean で証明すべき構造定理**・**Aeneas で実抽出すべき Rust メソッド**・**Quint で検査すべき状態遷移と比較モード期待表**・**信頼境界（何を捨象するか）** を調査ブリーフ（[brief-format.md](../team-bucciarati/reference/brief-format.md)）にまとめる。
2. **【後】Spice Girl（形式モデル・証明の実装）**:
   - 呼び方: *「Spice Girl で Lean と Quint 書いて」「ブリーフに沿って formal を実装して」*
   - 出力: 下の3層の規律に従って `formal/lean/`・`formal/quint/`・（Rust の核なら）`formal/aeneas/` と各 `README.md` を実装し、全チェックが PASS する状態にする。
   - **モデル配分の注意**: 構成的 Lean 証明や比較モード設計は深い推論を要するため、呼び出し時に `opus` または `fable` へのエスカレーションを推奨する。
3. **【後】Moody Blues × Sticky Fingers（santa レビュー）**:
   - 呼び方: *「この formal を santa レビューして」「Sticky Fingers で証明の嘘を味見して」*
   - 出力: 実測 PASS と「嘘の証明」ゼロを独立2レビュアーで確認する。

---

## 各層の設計規律（Chronista 標準の型）

### 1. Lean 4 手書き構造モデル（`formal/lean/`）

- **ツールチェーン固定**: `formal/lean/lean-toolchain` で Lean バージョン（例: `leanprover/lean4:v4.36.0`）を固定する。外部 Lake パッケージには依存せず、単体で高速に走らせる:
  ```sh
  lean -DwarningAsError=true formal/lean/<Name>Core.lean
  ```
- **空公理（構成的証明）の鉄則**:
  - すべての構造定理・補助定理の直後に `#print axioms <theorem_name>` を置く。
  - 全定理が **`does not depend on any axioms`** と報告することを確認する。
  - **`sorry`、追加の `axiom`、`Classical.choice`、`propext`、`Quot.sound` は一切使わない。**
  - Lean 標準ライブラリの一部の補題や `String` 操作が `propext` / `Classical.choice` を引く場合は、`List Char` や構成的な補助関数で直接記述する。
- **反例定理（Negative Theorems）を含める**:
  - 「現在の規則なら成り立つ」だけでなく、「規則を外した誤実装（例: `None` の省略、辞書のシャドウイング、フィルタと rename の順序逆転）では壊れる」ことも定理として構成的に証明する。

### 2. Charon / Aeneas 実 Rust 抽出証明（`formal/aeneas/`）

Rust プロジェクトで、手書きモデルだけでなく実 Cargo crate のコードそのものを証明したい場合に導入する:

- **実 crate からの直接抽出**:
  - 別 crate に写した模造コードや手書き代替実装は使わない。`charon cargo --preset=aeneas ...` で実 Cargo crate から LLBC を抽出し、`aeneas` で Lean コードを生成する。
  - 生成定義を `lake build` し、`lake env lean -DwarningAsError=true <Name>Proof.lean` で期待仕様（`Result.ok` に包んだ期待値＝正常終了＋値一致）との一致を証明する。
  - 各定理に `#print axioms` を置き、`sorryAx`・`Classical.choice`・独自公理を拒否する（Aeneas 生成基盤が要求する `propext`, `Quot.sound` のみ許容）。
- **Mutation Test（感度検証）**:
  - `bun formal/aeneas/check.ts --mutation-test` を用意する。
  - 一時コピー上で対象メソッドを1つずつ意図的に壊し（例: `Some` の代わりに `None` を返す、スライスを空にする）、再抽出・再証明して **「壊した対象定理だけが `sorryAx` で失敗し、残りの定理は通ること」** を確認する。元の作業ツリーは `finally` で無傷に保つ。

### 3. Quint 状態機械モデル検査（`formal/quint/`）

- **ランナーの標準化**:
  - `bun formal/quint/check.ts` から `bunx @informalsystems/quint@0.33.1`（バージョン固定）を呼び出す。乱数 `SEED`・`SAMPLES`・`STEPS` を環境変数で上書き可能にし、既定値で再現性を保つ。
- **比較モードと期待表（`ok` / `ng`）の鉄則**:
  - 現行設計のモード（例: `<project>Current`）が全不変条件で `ok`（反例なし）になるだけでは不十分。
  - 守りたい設計規則を `const` フラグ（例: `WAIT_FOR_QUIESCE`, `NO_ALIAS_SHADOWING`, `ENFORCE_REVOCATION_CUTOFF`）として切り出し、**規則を1つずつ `false` にした比較モード（および全部外した `naive` モード）** を定義する。
  - `check.ts` に **期待表（モード × 不変条件 → `ok` or `ng`）** を持たせ、比較モードでは対応する不変条件が期待通り **`ng`（`Invariant violated` かつ exit 1）** になることを機械的に検証する。
  - **注意**: 構文エラー・型エラー・実行時エラー・タイムアウト・燃料切れ（FuelExhausted）を `ng`（期待した反例）として扱ってはならない。明示的な `Invariant violated` のみを反例成功と判定する。

### 4. 実装との対応表と信頼境界（`formal/*/README.md`）

各 `formal/{lean,aeneas,quint}/README.md` には必ず以下の3節を含める:

1. **実行コマンドと合格条件**（空公理確認、期待表のシナリオ数・不変条件数）
2. **実装との対応表**（実コードの `path::function` ↔ モデルの関数・定理・シナリオ・比較モード）
3. **保証の範囲と信頼境界（Trust Boundary）**:
   - モデルが何を証明し、**何を捨象しているか**（例: UTF-8 バイト境界、I/O、有限深さ、暗号学的ハッシュ衝突、コンパイラ/ABI 等）を明記する。誇大な完全性主張（「すべてのバグが存在しないことを証明した」等）は書かない。

---

## Sticky Fingers の「証明の嘘の味」チェックリスト

`formal/` をレビューするとき、Sticky Fingers（および Moody Blues）は以下の欺瞞を暴く:

1. **公理の密輸**: `#print axioms` が抜けている定理はないか。`sorry` / `sorryAx` / `axiom` / `Classical.choice`（手書き Lean では `propext` / `Quot.sound` も）が混入していないか。
2. **空虚な真（Vacuous Truth）**: 前提条件が矛盾または強すぎて中身を検証せずに成立していないか。定数フラグの値そのものを不変条件の判定式に使っていないか。
3. **モデルの捏造（Model-Code Drift）**: 証明を通すために、実コードには存在しないガードや正規化をモデル側にだけ都合よく足していないか。実コードの分岐順とモデルの分岐順が一致しているか。
4. **比較モードの八百長と Mutation 感度**: Quint の `ng` 期待モードが、本当にその設計規則を外した反例（`Invariant violated`）で落ちているか。無関係なエラーや自明な定数判定で落ちたふりをしていないか。Aeneas の `--mutation-test` で壊した対象定理だけが `sorryAx` で落ちて残り定理が通るか。
5. **信頼境界の欺瞞**: README の対応表に存在しない関数・定理が書かれていないか。捨象した前提を隠して過剰な保証を謳っていないか。
