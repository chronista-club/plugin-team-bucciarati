# 01. プロジェクトの品質ゲートを保つ

> **Status**: Active
> **Related**: mem_1Cfv9MWjUrXiHT8SMVVpaE
> **対象**: `scripts/detect-ci.sh`, `agents/moody-blues.md`

mise の `check` はリポジトリが定義する集約ゲートとして優先し、個別タスクと重複実行しない。
これにより chronista-style の validate / sync-check を落とさない。
`check` がない場合だけ既存の typecheck / lint / build / test を順に選ぶ。

JSON 出力が取得不能・不正なら非ゼロ終了とし、表示用テーブルから推測しない。
正常に取得できても既知のタスクがなければ `commands: []` を返す。
呼び手は空配列を成功の証拠とせず、プロジェクトの CI と開発規約を調べる。
Cargo / Node / Go の既存検出はこの修正では変更しない。

## やってはいけない

- 定義を確認せず `mise run test` を作る。
- `sem check` の結果だけで、プロジェクト固有の検証まで通ったと報告する。

## Status log

- 2026-10-11: 集約 check 優先、検出失敗と対象なしの区別を回帰テストで固定。
