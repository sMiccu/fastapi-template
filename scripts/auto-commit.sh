#!/bin/bash
# 自動コミット＆プッシュスクリプト（Conventional Commits対応）

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 使い方を表示
show_help() {
    cat << EOF
自動コミット＆プッシュスクリプト

使い方:
  ./scripts/auto-commit.sh [type] [message] [options]

Type（必須）:
  feat       新機能
  fix        バグ修正
  docs       ドキュメント
  style      フォーマット（動作変更なし）
  refactor   リファクタリング
  test       テスト追加
  chore      雑務（依存関係更新等）
  perf       パフォーマンス改善
  ci         CI設定変更

Options:
  --no-push       プッシュしない
  --no-test       テストをスキップ
  --no-check      チェックをスキップ
  --breaking      破壊的変更
  --scope SCOPE   スコープを指定

例:
  ./scripts/auto-commit.sh feat "add user authentication"
  ./scripts/auto-commit.sh fix "resolve N+1 query" --scope orders
  ./scripts/auto-commit.sh docs "update architecture" --no-push
  ./scripts/auto-commit.sh feat "new API" --breaking

対話モード:
  ./scripts/auto-commit.sh --interactive

クイックコマンド（Makefileから）:
  make commit msg="your message"
  make commit-fix msg="bug fix message"
  make commit-docs msg="doc update"

EOF
}

# 対話モード
interactive_mode() {
    echo -e "${BLUE}📝 対話モードでコミットを作成${NC}"
    echo ""

    # Type選択
    echo "コミットタイプを選択してください:"
    echo "1) feat      - 新機能"
    echo "2) fix       - バグ修正"
    echo "3) docs      - ドキュメント"
    echo "4) refactor  - リファクタリング"
    echo "5) test      - テスト追加"
    echo "6) chore     - 雑務"
    read -p "選択 [1-6]: " type_choice

    case $type_choice in
        1) TYPE="feat" ;;
        2) TYPE="fix" ;;
        3) TYPE="docs" ;;
        4) TYPE="refactor" ;;
        5) TYPE="test" ;;
        6) TYPE="chore" ;;
        *) echo "無効な選択"; exit 1 ;;
    esac

    # スコープ
    read -p "スコープ（オプション、例: orders, catalog）: " SCOPE

    # メッセージ
    read -p "コミットメッセージ: " MESSAGE

    # 破壊的変更
    read -p "破壊的変更ですか？ [y/N]: " breaking
    if [ "$breaking" = "y" ]; then
        BREAKING=true
    fi

    # プッシュ
    read -p "リモートにプッシュしますか？ [Y/n]: " push
    if [ "$push" = "n" ]; then
        NO_PUSH=true
    fi
}

# 変更の確認
check_changes() {
    if [ -z "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}⚠️  コミットする変更がありません${NC}"
        exit 0
    fi

    echo -e "${BLUE}📊 変更されたファイル:${NC}"
    git status --short
    echo ""
}

# コードチェック
run_checks() {
    if [ "$NO_CHECK" = true ]; then
        echo -e "${YELLOW}⏭  チェックをスキップ${NC}"
        return
    fi

    echo -e "${BLUE}🔍 コード品質チェック中...${NC}"

    # Lint & Fix
    if ! make lint > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Lintエラーがあります。自動修正を試みます...${NC}"
        make lint-fix
        # 修正されたファイルを自動でステージング
        if [ -n "$(git diff)" ]; then
            git add -A
            echo -e "${GREEN}✓ 修正されたファイルを自動追加しました${NC}"
        fi
    fi

    # Format
    make format > /dev/null 2>&1
    # フォーマット後、変更があれば追加
    if [ -n "$(git diff)" ]; then
        git add -A
        echo -e "${GREEN}✓ フォーマットされたファイルを自動追加しました${NC}"
    fi

    # Type check
    if ! make typecheck > /dev/null 2>&1; then
        echo -e "${RED}✗ 型チェックエラー${NC}"
        make typecheck
        exit 1
    fi

    # Test
    if [ "$NO_TEST" = true ]; then
        echo -e "${YELLOW}⏭  テストをスキップ${NC}"
    else
        echo -e "${BLUE}🧪 テスト実行中...${NC}"
        if ! make test-unit > /dev/null 2>&1; then
            echo -e "${RED}✗ テスト失敗${NC}"
            make test-unit
            exit 1
        fi
    fi

    echo -e "${GREEN}✓ 全てのチェック完了${NC}"
}

# コミットメッセージの生成
generate_commit_message() {
    local msg=""

    if [ -n "$SCOPE" ]; then
        msg="${TYPE}(${SCOPE})"
    else
        msg="${TYPE}"
    fi

    if [ "$BREAKING" = true ]; then
        msg="${msg}!"
    fi

    msg="${msg}: ${MESSAGE}"

    echo "$msg"
}

# ドキュメント更新チェック
check_doc_updates() {
    echo -e "${BLUE}📚 ドキュメントの整合性チェック...${NC}"

    # pyproject.tomlが変更されていたらTECH_STACK.mdの更新を促す
    if git diff --cached --name-only | grep -q "pyproject.toml"; then
        echo -e "${YELLOW}⚠️  pyproject.tomlが変更されています${NC}"
        echo -e "   docs/TECH_STACK.mdの更新が必要かもしれません"
    fi

    # src/app/modules/に変更があればDOMAIN_MODEL.mdの確認を促す
    if git diff --cached --name-only | grep -q "src/app/modules/"; then
        echo -e "${YELLOW}⚠️  モジュールに変更があります${NC}"
        echo -e "   docs/DOMAIN_MODEL.mdの更新が必要かもしれません"
    fi

    # アーキテクチャ関連の大きな変更があれば
    if git diff --cached --name-only | grep -qE "(domain|application|infrastructure)/"; then
        echo -e "${YELLOW}⚠️  アーキテクチャ層に変更があります${NC}"
        echo -e "   docs/ARCHITECTURE.mdの確認をお勧めします"
    fi
}

# コミット実行
do_commit() {
    local commit_msg=$(generate_commit_message)

    echo -e "${BLUE}📝 コミットメッセージ: ${NC}${commit_msg}"

    # 全ての変更をステージング
    git add -A

    # ドキュメント整合性チェック
    check_doc_updates

    # コミット（pre-commitフックが実行される）
    MAX_RETRIES=3
    for i in $(seq 1 $MAX_RETRIES); do
        if git commit -m "$commit_msg"; then
            break
        else
            # pre-commitフックでファイルが修正された場合
            if [ -n "$(git diff)" ] && [ $i -lt $MAX_RETRIES ]; then
                echo -e "${YELLOW}⚠️  pre-commitフックがファイルを修正しました。再試行中... ($i/$MAX_RETRIES)${NC}"
                git add -A
            else
                echo -e "${RED}✗ コミット失敗${NC}"
                exit 1
            fi
        fi
    done

    echo -e "${GREEN}✓ コミット完了${NC}"

    # 現在のブランチを取得
    BRANCH=$(git branch --show-current)

    # プッシュ
    if [ "$NO_PUSH" != true ]; then
        echo -e "${BLUE}🚀 リモートにプッシュ中... (${BRANCH})${NC}"
        git push origin "$BRANCH"
        echo -e "${GREEN}✓ プッシュ完了${NC}"
    else
        echo -e "${YELLOW}⏭  プッシュはスキップされました${NC}"
        echo "   後でプッシュする場合: git push origin $BRANCH"
    fi
}

# 最近のコミットを表示
show_recent_commits() {
    echo ""
    echo -e "${BLUE}📋 最近のコミット:${NC}"
    git log --oneline -5
}

# メイン処理
main() {
    # 引数解析
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_help
        exit 0
    fi

    if [ "$1" = "--interactive" ] || [ "$1" = "-i" ]; then
        interactive_mode
    else
        TYPE=$1
        MESSAGE=$2
        shift 2

        # 引数チェック
        if [ -z "$TYPE" ] || [ -z "$MESSAGE" ]; then
            echo -e "${RED}エラー: typeとmessageは必須です${NC}"
            echo ""
            show_help
            exit 1
        fi

        # オプション解析
        while [[ $# -gt 0 ]]; do
            case $1 in
                --no-push)
                    NO_PUSH=true
                    shift
                    ;;
                --no-test)
                    NO_TEST=true
                    shift
                    ;;
                --no-check)
                    NO_CHECK=true
                    shift
                    ;;
                --breaking)
                    BREAKING=true
                    shift
                    ;;
                --scope)
                    SCOPE=$2
                    shift 2
                    ;;
                *)
                    echo "不明なオプション: $1"
                    exit 1
                    ;;
            esac
        done
    fi

    # 実行
    check_changes
    run_checks
    do_commit
    show_recent_commits

    echo ""
    echo -e "${GREEN}🎉 全ての処理が完了しました！${NC}"
}

# スクリプト実行
main "$@"
