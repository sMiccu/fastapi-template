#!/bin/bash
set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ロゴ表示
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   FastAPI Template - セットアップスクリプト           ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# 関数定義
log_info() {
    echo -e "${BLUE}ℹ ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# uvのインストールチェック
check_uv() {
    log_info "uvのインストールを確認中..."
    if ! command -v uv &> /dev/null; then
        log_warning "uvがインストールされていません。インストールしています..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
        log_success "uvをインストールしました"
        log_warning "シェルを再起動するか、以下を実行してください:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    else
        log_success "uv: $(uv --version)"
    fi
}

# Dockerのチェック
check_docker() {
    log_info "Dockerのインストールを確認中..."
    if ! command -v docker &> /dev/null; then
        log_error "Dockerがインストールされていません"
        log_info "Docker Desktop をインストールしてください: https://www.docker.com/products/docker-desktop"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        log_error "Dockerデーモンが起動していません"
        log_info "Docker Desktop を起動してください"
        exit 1
    fi

    log_success "Docker: $(docker --version)"
}

# 依存関係のインストール
install_dependencies() {
    log_info "依存関係をインストール中..."

    if [ "$ENVIRONMENT" = "production" ]; then
        uv sync --no-dev
    else
        uv sync --all-extras

        # pre-commitのインストール
        if [ -d ".git" ]; then
            log_info "pre-commitフックをインストール中..."
            uv run pre-commit install
            log_success "pre-commitフックをインストールしました"
        fi
    fi

    log_success "依存関係をインストールしました"
}

# .envファイルの作成
create_env_file() {
    if [ -f ".env" ]; then
        log_info ".envファイルは既に存在します"
        return
    fi

    log_info ".envファイルを作成中..."

    # ランダムなSECRET_KEYを生成
    SECRET_KEY=$(openssl rand -hex 32)

    cat > .env << EOF
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_template
DATABASE_ECHO=false

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=FastAPI Template
APP_VERSION=0.1.0
DEBUG=true
ENVIRONMENT=${ENVIRONMENT:-development}

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Logging
LOG_LEVEL=INFO
EOF

    log_success ".envファイルを作成しました"
}

# Dockerコンテナの起動
start_docker() {
    log_info "Dockerコンテナを起動中..."
    docker-compose up -d

    # データベースの準備を待つ
    log_info "データベースの準備を待っています..."
    for i in {1..30}; do
        if docker-compose exec -T postgres pg_isready -U postgres &> /dev/null; then
            log_success "データベースの準備完了"
            break
        fi
        sleep 1
        if [ $i -eq 30 ]; then
            log_error "データベースの起動タイムアウト"
            exit 1
        fi
    done
}

# マイグレーションの実行
run_migrations() {
    log_info "データベースマイグレーションを実行中..."

    # versionsディレクトリを作成
    mkdir -p alembic/versions

    # マイグレーションを適用
    uv run alembic upgrade head

    log_success "マイグレーション完了"
}

# テストの実行
run_tests() {
    log_info "テストを実行中..."
    uv run pytest tests/unit/ -v --tb=short
    log_success "テスト完了"
}

# セットアップ完了メッセージ
print_completion_message() {
    echo ""
    echo -e "${GREEN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║          ✓ セットアップが完了しました！               ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"

    echo "次のコマンドでサーバーを起動できます:"
    echo ""
    echo -e "  ${BLUE}make dev${NC}         # 開発サーバー起動"
    echo -e "  ${BLUE}make test${NC}        # テスト実行"
    echo -e "  ${BLUE}make help${NC}        # その他のコマンドを表示"
    echo ""
    echo "APIエンドポイント:"
    echo -e "  ${GREEN}http://localhost:8000${NC}          - API"
    echo -e "  ${GREEN}http://localhost:8000/docs${NC}     - Swagger UI"
    echo -e "  ${GREEN}http://localhost:8000/redoc${NC}    - ReDoc"
    echo -e "  ${GREEN}http://localhost:8000/health${NC}   - Health Check"
    echo ""
}

# メイン処理
main() {
    # 環境変数の設定
    ENVIRONMENT=${ENVIRONMENT:-development}
    SKIP_TESTS=${SKIP_TESTS:-false}

    log_info "環境: $ENVIRONMENT"
    echo ""

    # 各ステップの実行
    check_uv
    check_docker
    install_dependencies
    create_env_file

    if [ "$ENVIRONMENT" != "production" ]; then
        start_docker
        run_migrations

        if [ "$SKIP_TESTS" != "true" ]; then
            run_tests
        fi
    fi

    print_completion_message
}

# ヘルプメッセージ
show_help() {
    cat << EOF
FastAPI Template セットアップスクリプト

使い方:
  ./scripts/setup.sh [オプション]

オプション:
  -h, --help              このヘルプを表示
  -e, --env ENV           環境を指定 (development|production) [default: development]
  --skip-tests            テストをスキップ
  --prod                  本番環境モード (--env production のショートカット)

例:
  ./scripts/setup.sh                    # 開発環境セットアップ
  ./scripts/setup.sh --prod             # 本番環境セットアップ
  ./scripts/setup.sh --skip-tests       # テストをスキップしてセットアップ
  ./scripts/setup.sh -e production      # 本番環境セットアップ

EOF
}

# コマンドライン引数の解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --prod)
            ENVIRONMENT="production"
            shift
            ;;
        --skip-tests)
            SKIP_TESTS="true"
            shift
            ;;
        *)
            log_error "不明なオプション: $1"
            show_help
            exit 1
            ;;
    esac
done

# スクリプトの実行
main
