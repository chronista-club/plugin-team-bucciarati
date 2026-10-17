# MCP Tools Reference

Team Bucciarati の各スタンドが活用できる MCP ツール。
全てオプショナル — ツールが利用不可でもスタンドは動作する。

## gitnexus — コードベースナレッジグラフ

Tree-sitter でコードを解析し、依存関係・呼び出しチェーン・シンボル関係をグラフ化。
事前に `gitnexus analyze` でリポジトリをインデックスする必要がある。

### 主なツール
| ツール | 用途 |
|--------|------|
| `query` | 自然言語/キーワードで実行フローを検索（BM25 + セマンティック） |
| `context` | シンボルの360度ビュー（呼び出し元/先、参照、プロセス参加） |
| `impact` | 変更の blast radius 分析（depth 別リスク分類） |
| `detect_changes` | git diff から影響を受ける実行フローを特定 |
| `cypher` | Cypher クエリでナレッジグラフを直接検索 |

### スタンド別活用
- **Purple Haze**: `query` で全体像把握 → `context` でシンボル深堀り → `impact` で影響範囲特定
- **Moody Blues**: `detect_changes` で diff の影響フロー検出 → `impact` で blast radius 確認
- **Spice Girl**: `context` でテスト対象の依存関係把握
- **Sticky Fingers**: `context` / `query` で成果物の claim をコード実体と突き合わせ

## sem — エンティティレベルのコードインテリジェンス

関数・クラス単位の実体と、ファイル横断の呼び出し / import グラフ。
構造的な質問（「何が呼んでいるか」「変えたら何が壊れるか」）は grep より先に sem。

### 現行 API と CLI（sem 0.27.0 で確認）

接続中の MCP の `tools/list` を正本にする。旧 `sem_context` / `sem_entities` は
`sem_find` に、旧 `sem_blame` / `sem_log` は `sem_history` に統合された。
異なる版では引数も確認し、MCP がなければ CLI の `--help` に従う。

| 用途 | MCP | CLI の例 |
|------|-----|----------|
| 定義・呼び出し元・文脈 | `sem_find`（`mode`: `callers` / `context` 等） | `sem find parseConfig --context --json` |
| 本文・パスから実体を探す | `sem_find`（`text` / `in`） | `sem find --text 'retry budget' --in src --json` |
| 変更の影響範囲 | `sem_impact`（`entity_name` + `file_path`、テストは `mode: "tests"`） | `sem impact --diff HEAD --tests --json` |
| エンティティ単位の差分 | `sem_diff` | `sem diff --json` |
| 履歴・最終変更者 | `sem_history`（最終変更者は `blame: true` + `file_path`） | `sem history parseConfig --json` / `sem history --blame src/config.ts --json` |
| コミット範囲のレビュー補助 | `sem_certify`（`range`） | `sem certify main..HEAD --json` |
| プロジェクトの検証 | `sem_check` | `sem check --json` |

CLI と MCP の引数は同一ではない。特に差分全体の `impact --diff` は上記 CLI を使う。
文字列検索は `rg`、構造を知りたいときは `sem find` / `impact` を使い分ける。
`certify` の結果はレビューの手がかりであり、人間・スタンドのレビューを置き換えない。

### スタンド別活用
- **Purple Haze**: `sem_find` の文脈 → `sem_impact` → `sem_history` で設計の来歴
- **Moody Blues**: `sem_diff` → `sem_impact`。コミット済みの範囲は `sem_certify` も補助に使う
- **Spice Girl**: `sem_find` で API と依存関係、`sem_impact` で関連テストを探す
- **Sticky Fingers**: `sem_history` の履歴 / blame で来歴に関する claim を実測検証

### 検証との境界
- `sem check` の終了コードは 0=pass、1=fail、2=判定不能。2 を成功にしない。
- リポジトリの `mise run check` / CI / 検証規約を先に確認する。`sem check` を採用する場合も
  実行した checker と対象範囲を読み、独自の validate・同期チェック等を落とさない。
- `sem check --promises` は一時的にコードを変更する。読み取り専用レビューでは実行しない。
- インデックス・影響解析だけでは安全性の証明にならない。実際の差分・ソース・テストで確かめる。

公式: [sem](https://github.com/Ataraxy-Labs/sem#using-sem-with-agents)

## context7 — ライブラリドキュメント

ライブラリの最新ドキュメントとコード例を取得。

### 主なツール
| ツール | 用途 |
|--------|------|
| `resolve-library-id` | ライブラリ ID の解決 |
| `query-docs` | ドキュメント・コード例の取得 |

### スタンド別活用
- **Purple Haze**: 技術調査でライブラリの API 仕様・ベストプラクティスを確認
- **Spice Girl**: テストフレームワークの API・パターンを確認
