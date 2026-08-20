#!/bin/bash
# HOI4-Bakasekaitizu-MOD (BSM) 静的検証ハーネス
#
# 使い方:
#   ./verify.sh          静的検証 (validate_mod.py + loc_coverage.py)
#   ./verify.sh --check  ツール・パス存在確認とステップ表示のみ
#   ./verify.sh --full   静的検証 + bakasekai 全 .txt/.yml の構文検証 (重い)
#
# 出力契約: 各ステップ "[n/m] ステップ名" / 最後に "VERIFY PASS" or "VERIFY FAIL"(exit 1)
# bash 3.2 / BSDコマンド互換
#
# 呼び出すツールのCLI仕様 (実装読解で確認済み):
#   tools/validate_mod.py [MOD_ROOT]   位置引数1つ (既定 "bakasekai")。ERRORで exit 1、root不在で exit 2。
#       CI (.github/workflows/validate-mod.yml) と同じくリポジトリルートから相対実行する
#   tools/loc_coverage.py [MOD_ROOT] [--list] [--strict X]   既定は常に exit 0 の情報表示
#       (japanese loc 不在時のみ exit 2)。CIでも if: always() の非ブロッキング運用のため、
#       本スクリプトでも警告扱い (FAILにしない)
#   ~/dev/hoi4/tools/hoi4_precommit_validate.py  引数=ファイルパス列挙。pydantic依存 (venv優先)
set -euo pipefail

MOD_ROOT="$(cd "$(dirname "$0")" && pwd)"
BAKASEKAI_NAME="bakasekai"
BAKASEKAI_DIR="$MOD_ROOT/$BAKASEKAI_NAME"
VALIDATE_PY="$MOD_ROOT/tools/validate_mod.py"
LOC_COVERAGE_PY="$MOD_ROOT/tools/loc_coverage.py"
PRECOMMIT_PY="$HOME/dev/hoi4/tools/hoi4_precommit_validate.py"
SYNTAX_VENV_PY="$HOME/dev/hoi4/mcp-hoi4-syntax/.venv/bin/python"

usage() {
  echo "使い方: $0 [--check|--full]"
  echo "  (無印)   静的検証: validate_mod.py $BAKASEKAI_NAME + loc_coverage.py $BAKASEKAI_NAME (後者は警告扱い)"
  echo "  --check  ツール・パス存在確認とステップ表示のみ"
  echo "  --full   静的検証 + $BAKASEKAI_NAME 全 .txt/.yml 構文検証"
}

MODE="static"
case "${1:-}" in
  "")        MODE="static" ;;
  --check)   MODE="check" ;;
  --full)    MODE="full" ;;
  -h|--help) usage; exit 0 ;;
  *)         echo "不明な引数: $1" >&2; usage >&2; exit 2 ;;
esac

FAIL=0
STEP=0
TOTAL=0

step() {
  STEP=$((STEP + 1))
  echo ""
  echo "[$STEP/$TOTAL] $1"
}

mark_fail() {
  echo "-> NG: $1"
  FAIL=1
}

check_ok() {
  echo "-> OK: $1"
}

pick_python() {
  if [ -x "$SYNTAX_VENV_PY" ]; then
    echo "$SYNTAX_VENV_PY"
  else
    echo "python3"
  fi
}

finish() {
  echo ""
  if [ "$FAIL" -eq 0 ]; then
    echo "VERIFY PASS"
  else
    echo "VERIFY FAIL"
  fi
  echo "静的検証のみ。完了条件には起動テスト(error.logゼロ)と実機確認が必要"
  if [ "$FAIL" -ne 0 ]; then
    exit 1
  fi
  exit 0
}

run_validate_mod() {
  local rc=0
  # CI (validate-mod.yml) と同一の呼び出し形にする
  (cd "$MOD_ROOT" && python3 tools/validate_mod.py "$BAKASEKAI_NAME") || rc=$?
  if [ $rc -ne 0 ]; then
    mark_fail "validate_mod.py $BAKASEKAI_NAME (exit $rc)"
  fi
}

# 非ブロッキング: 失敗しても警告表示のみ (CIの if: always() 非ブロッキング運用に合わせる)
run_loc_coverage() {
  local rc=0
  (cd "$MOD_ROOT" && python3 tools/loc_coverage.py "$BAKASEKAI_NAME") || rc=$?
  if [ $rc -ne 0 ]; then
    echo "-> WARN: loc_coverage.py が exit $rc (非ブロッキング扱い、FAILにはしない)"
  fi
}

run_syntax_full() {
  local pybin rc=0 tmp n
  pybin="$(pick_python)"
  tmp="$(mktemp /tmp/bsm_verify_all.XXXXXX)"
  find "$BAKASEKAI_DIR" -type f \( -name '*.txt' -o -name '*.yml' \) -print0 > "$tmp"
  n=$(tr -dc '\000' < "$tmp" | wc -c | tr -d ' ')
  echo "検証対象: $n ファイル (python: $pybin)"
  if [ "$n" -gt 0 ]; then
    xargs -0 "$pybin" "$PRECOMMIT_PY" < "$tmp" || rc=$?
    if [ $rc -ne 0 ]; then
      mark_fail "hoi4_precommit_validate.py 全ファイル検証 (exit $rc)"
    fi
  fi
  rm -f "$tmp"
}

run_check() {
  TOTAL=6

  step "コマンド存在確認 (python3 / xargs)"
  local c missing=""
  for c in python3 xargs; do
    if ! command -v "$c" >/dev/null 2>&1; then
      missing="$missing $c"
    fi
  done
  if [ -n "$missing" ]; then
    mark_fail "コマンドが見つからない:$missing"
  else
    check_ok "python3 / xargs"
  fi

  step "mod本体ディレクトリの存在 ($BAKASEKAI_DIR)"
  if [ -d "$BAKASEKAI_DIR/common" ]; then
    check_ok "実在 (common/ あり)"
  else
    mark_fail "$BAKASEKAI_DIR/common が無い"
  fi

  step "validate_mod.py の存在 ($VALIDATE_PY)"
  if [ -f "$VALIDATE_PY" ]; then check_ok "実在"; else mark_fail "ファイルが無い"; fi

  step "loc_coverage.py の存在 ($LOC_COVERAGE_PY)"
  if [ -f "$LOC_COVERAGE_PY" ]; then check_ok "実在"; else mark_fail "ファイルが無い"; fi

  step "共有構文バリデータと実行環境 ($PRECOMMIT_PY) [--full用]"
  if [ ! -f "$PRECOMMIT_PY" ]; then
    mark_fail "ファイルが無い"
  elif [ -x "$SYNTAX_VENV_PY" ]; then
    check_ok "実在 + venv python 実在"
  elif python3 -c "import pydantic" >/dev/null 2>&1; then
    check_ok "実在 (venv不在だが python3 に pydantic あり)"
  else
    mark_fail "venvが無く python3 にも pydantic が無い"
  fi

  step "実行ステップ一覧"
  echo "  無印   : [1] validate_mod.py $BAKASEKAI_NAME (ERRORで失敗)"
  echo "           [2] loc_coverage.py $BAKASEKAI_NAME (非ブロッキング=警告扱い)"
  echo "  --full : [3] hoi4_precommit_validate.py ($BAKASEKAI_NAME 全 .txt/.yml)"
  check_ok "表示完了"
}

echo "== HOI4-Bakasekaitizu-MOD verify ($MODE) =="
echo "mod root: $MOD_ROOT"
echo "branch  : $(git -C "$MOD_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '不明')"

case "$MODE" in
  check)
    run_check
    ;;
  static)
    TOTAL=2
    step "mod静的検証 (validate_mod.py $BAKASEKAI_NAME)"
    run_validate_mod
    step "ローカライズカバレッジ (loc_coverage.py $BAKASEKAI_NAME) [非ブロッキング]"
    run_loc_coverage
    ;;
  full)
    TOTAL=3
    step "mod静的検証 (validate_mod.py $BAKASEKAI_NAME)"
    run_validate_mod
    step "ローカライズカバレッジ (loc_coverage.py $BAKASEKAI_NAME) [非ブロッキング]"
    run_loc_coverage
    step "HOI4構文検証: 全ファイル (hoi4_precommit_validate.py)"
    run_syntax_full
    ;;
esac

finish
