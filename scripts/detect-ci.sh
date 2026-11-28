#!/usr/bin/env bash
# プロジェクトの CI ツールチェーンを検出して JSON で返す
# Usage: ./scripts/detect-ci.sh [project-root]

set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

HAS_MISE_AGGREGATE_CHECK=0
HAS_MISE_FORMAL_LEAN=0
HAS_MISE_FORMAL_QUINT=0
HAS_MISE_FORMAL_AENEAS=0

if [ -f "mise.toml" ] || [ -f ".mise.toml" ]; then
  RUNNER="mise"
  CMDS=()
  # 検出失敗と「既知のタスクなし」を区別する。表示用テーブルから推測しない。
  if ! AVAILABLE_TASKS=$(mise task ls --json | jq -er '
    if type == "array" and all(.[]; type == "object" and (.name | type == "string"))
    then map(.name) | join("\n")
    else error("expected an array of tasks with string names") end'); then
    echo "detect-ci: mise task discovery failed; inspect the project check instructions" >&2
    exit 1
  fi
  # 集約された品質ゲートを優先し、独自の validate / sync-check も保つ。
  if echo "$AVAILABLE_TASKS" | grep -qx 'check'; then
    CMDS=("mise run check")
    HAS_MISE_AGGREGATE_CHECK=1
  else
    for task in typecheck lint build test formal:lean formal:quint formal:aeneas; do
      if echo "$AVAILABLE_TASKS" | grep -qx "$task"; then
        CMDS+=("mise run $task")
        case "$task" in
          formal:lean) HAS_MISE_FORMAL_LEAN=1 ;;
          formal:quint) HAS_MISE_FORMAL_QUINT=1 ;;
          formal:aeneas) HAS_MISE_FORMAL_AENEAS=1 ;;
        esac
      fi
    done
  fi
elif [ -f "Cargo.toml" ]; then
  RUNNER="cargo"
  CMDS=("cargo clippy -- -D warnings" "cargo build --release" "cargo test")
elif [ -f "package.json" ]; then
  RUNNER="node"
  # package manager 検出
  if [ -f "bun.lockb" ] || [ -f "bun.lock" ]; then
    PM="bun"
  elif [ -f "pnpm-lock.yaml" ]; then
    PM="pnpm"
  elif [ -f "yarn.lock" ]; then
    PM="yarn"
  else
    PM="npm"
  fi
  CMDS=()
  for script in typecheck lint build test; do
    if grep -q "\"$script\"" package.json 2>/dev/null; then
      CMDS+=("$PM run $script")
    fi
  done
  if [ ${#CMDS[@]} -eq 0 ]; then
    CMDS+=("$PM test")
  fi
  RUNNER="$PM"
elif [ -f "go.mod" ]; then
  RUNNER="go"
  CMDS=("go vet ./..." "go build ./..." "go test ./...")
else
  RUNNER="unknown"
  CMDS=()
fi

# mise の集約 check を使っていない場合、formal/ 配下の形式検証スイートも（対応する mise タスクが未定義なら）検出して追加する
if [ "$HAS_MISE_AGGREGATE_CHECK" -eq 0 ]; then
  if [ "$HAS_MISE_FORMAL_LEAN" -eq 0 ] && [ -d "formal/lean" ]; then
    for lean_file in formal/lean/*.lean; do
      if [ -f "$lean_file" ]; then
        CMDS+=("lean -DwarningAsError=true $lean_file")
      fi
    done
  fi
  if [ "$HAS_MISE_FORMAL_QUINT" -eq 0 ] && [ -f "formal/quint/check.ts" ]; then
    CMDS+=("bun formal/quint/check.ts")
  fi
  if [ "$HAS_MISE_FORMAL_AENEAS" -eq 0 ] && [ -f "formal/aeneas/check.ts" ]; then
    CMDS+=("bun formal/aeneas/check.ts")
  fi
  if [ "$RUNNER" = "unknown" ] && [ ${#CMDS[@]} -gt 0 ]; then
    RUNNER="formal"
  fi
fi

# macOS の Bash 3.2 でも nounset 下の空配列を展開できる形にする。
jq -n --arg runner "$RUNNER" --args '{"runner": $runner, "commands": $ARGS.positional}' -- ${CMDS[@]+"${CMDS[@]}"}
