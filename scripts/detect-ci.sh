#!/usr/bin/env bash
# プロジェクトの CI ツールチェーンを検出して JSON で返す
# Usage: ./scripts/detect-ci.sh [project-root]

set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

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
  else
    for task in typecheck lint build test; do
      if echo "$AVAILABLE_TASKS" | grep -qx "$task"; then
        CMDS+=("mise run $task")
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
  echo '{"runner":"unknown","commands":[]}'
  exit 0
fi

# macOS の Bash 3.2 でも nounset 下の空配列を展開できる形にする。
jq -n --arg runner "$RUNNER" --args '{"runner": $runner, "commands": $ARGS.positional}' -- ${CMDS[@]+"${CMDS[@]}"}
