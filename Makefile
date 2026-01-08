.PHONY: help setup setup-dev setup-prod install install-dev clean test lint format typecheck check dev up down logs db-upgrade db-migrate docker-build

# デフォルトのPython実行コマンド
UV := uv
PYTHON := $(UV) run python
PYTEST := $(UV) run pytest
UVICORN := $(UV) run uvicorn
ALEMBIC := $(UV) run alembic
RUFF := $(UV) run ruff
MYPY := $(UV) run mypy

help: ## ヘルプを表示
	@echo "利用可能なコマンド:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ========================================
# セットアップコマンド
# ========================================

setup: setup-dev ## 開発環境の完全セットアップ（推奨）

setup-dev: check-uv install-dev create-env docker-up wait-db db-upgrade ## 開発環境のセットアップ
	@echo "✅ 開発環境のセットアップが完了しました！"
	@echo ""
	@echo "次のコマンドでサーバーを起動できます:"
	@echo "  make dev"
	@echo ""
	@echo "または:"
	@echo "  make up     # Docker起動のみ"
	@echo "  make test   # テスト実行"
	@echo ""
	@echo "Swagger UI: http://localhost:8000/docs"

setup-prod: check-uv install create-env db-upgrade ## 本番環境のセットアップ
	@echo "✅ 本番環境のセットアップが完了しました！"

check-uv: ## uvがインストールされているか確認
	@command -v uv >/dev/null 2>&1 || { \
		echo "⚠️  uvがインストールされていません。インストールしています..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "✅ uvをインストールしました"; \
		echo "⚠️  シェルを再起動するか、以下を実行してください:"; \
		echo "  export PATH=\"\$$HOME/.local/bin:\$$PATH\""; \
	}

install: ## 本番用依存関係をインストール
	@echo "📦 依存関係をインストール中..."
	$(UV) sync --no-dev

install-dev: ## 開発用依存関係も含めてインストール
	@echo "📦 依存関係（開発用含む）をインストール中..."
	$(UV) sync --all-extras
	@if [ -d .git ]; then \
		echo "🔧 pre-commitフックをインストール中..."; \
		$(UV) run pre-commit install; \
		echo "🔧 カスタムフックをインストール中..."; \
		$(MAKE) hooks-install; \
	fi

create-env: ## .envファイルを作成（存在しない場合）
	@if [ ! -f .env ]; then \
		echo "📝 .envファイルを作成中..."; \
		echo "# Database" > .env; \
		echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_template" >> .env; \
		echo "DATABASE_ECHO=false" >> .env; \
		echo "" >> .env; \
		echo "# Redis" >> .env; \
		echo "REDIS_URL=redis://localhost:6379/0" >> .env; \
		echo "" >> .env; \
		echo "# Security" >> .env; \
		echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env; \
		echo "ALGORITHM=HS256" >> .env; \
		echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env; \
		echo "" >> .env; \
		echo "# Application" >> .env; \
		echo "APP_NAME=FastAPI Template" >> .env; \
		echo "APP_VERSION=0.1.0" >> .env; \
		echo "DEBUG=true" >> .env; \
		echo "ENVIRONMENT=development" >> .env; \
		echo "" >> .env; \
		echo "# CORS" >> .env; \
		echo "CORS_ORIGINS=[\"http://localhost:3000\", \"http://localhost:8000\"]" >> .env; \
		echo "" >> .env; \
		echo "# Logging" >> .env; \
		echo "LOG_LEVEL=INFO" >> .env; \
		echo "✅ .envファイルを作成しました"; \
	else \
		echo "✓ .envファイルは既に存在します"; \
	fi

# ========================================
# Docker関連
# ========================================

docker-up: up ## Dockerコンテナを起動（upのエイリアス）

up: ## PostgreSQLとRedisを起動
	@echo "🐳 Dockerコンテナを起動中..."
	docker-compose up -d
	@echo "✅ コンテナを起動しました"

down: ## Dockerコンテナを停止
	@echo "🐳 Dockerコンテナを停止中..."
	docker-compose down
	@echo "✅ コンテナを停止しました"

logs: ## Dockerコンテナのログを表示
	docker-compose logs -f

ps: ## Dockerコンテナの状態を表示
	docker-compose ps

wait-db: ## データベースの準備完了を待つ
	@echo "⏳ データベースの準備を待っています..."
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		docker-compose exec -T postgres pg_isready -U postgres >/dev/null 2>&1 && break || sleep 1; \
	done
	@echo "✅ データベースの準備完了"

docker-build: ## Dockerイメージをビルド
	@echo "🏗️  Dockerイメージをビルド中..."
	docker build -t fastapi-template:latest .
	@echo "✅ ビルド完了"

# ========================================
# データベース関連
# ========================================

db-upgrade: ## マイグレーションを適用
	@echo "📊 マイグレーションを適用中..."
	@mkdir -p alembic/versions
	$(ALEMBIC) upgrade head
	@echo "✅ マイグレーション完了"

db-migrate: ## 新しいマイグレーションを作成
	@if [ -z "$(msg)" ]; then \
		echo "❌ エラー: メッセージを指定してください"; \
		echo "使用例: make db-migrate msg=\"add user table\""; \
		exit 1; \
	fi
	@mkdir -p alembic/versions
	$(ALEMBIC) revision --autogenerate -m "$(msg)"

db-downgrade: ## マイグレーションを1つ戻す
	@echo "📊 マイグレーションを戻しています..."
	$(ALEMBIC) downgrade -1

db-history: ## マイグレーション履歴を表示
	$(ALEMBIC) history

db-current: ## 現在のマイグレーションバージョンを表示
	$(ALEMBIC) current

db-reset: down ## データベースをリセット（注意！全データ削除）
	@echo "⚠️  データベースをリセットします（全データ削除）"
	@read -p "続行しますか？ [y/N]: " confirm && [ "$$confirm" = "y" ] || exit 1
	docker-compose down -v
	$(MAKE) up
	$(MAKE) wait-db
	$(MAKE) db-upgrade
	@echo "✅ データベースをリセットしました"

# ========================================
# 開発サーバー
# ========================================

dev: ## 開発サーバーを起動（ホットリロード有効）
	@echo "🚀 開発サーバーを起動中..."
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

dev-bg: ## 開発サーバーをバックグラウンドで起動
	@echo "🚀 開発サーバーをバックグラウンドで起動中..."
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &
	@echo "✅ サーバーを起動しました (PID: $$!)"

prod: ## 本番サーバーを起動
	@echo "🚀 本番サーバーを起動中..."
	$(UVICORN) app.main:app --host 0.0.0.0 --port 8000 --workers 4

shell: ## IPythonシェルを起動
	$(UV) run ipython

# ========================================
# テスト
# ========================================

test: ## 全テストを実行
	$(PYTEST)

test-unit: ## 単体テストのみ実行
	$(PYTEST) tests/unit/ -v

test-integration: ## 統合テストのみ実行
	$(PYTEST) tests/integration/ -v

test-e2e: ## E2Eテストのみ実行
	$(PYTEST) tests/e2e/ -v

test-cov: ## カバレッジ付きでテスト実行
	$(PYTEST) --cov=app --cov-report=html --cov-report=term

test-watch: ## テストをwatch modeで実行
	$(PYTEST) -f

# ========================================
# コード品質
# ========================================

lint: ## Lintチェックを実行
	@echo "🔍 Lintチェック中..."
	$(RUFF) check .

lint-fix: ## Lintエラーを自動修正
	@echo "🔧 Lintエラーを修正中..."
	$(RUFF) check --fix .

format: ## コードをフォーマット
	@echo "🎨 コードをフォーマット中..."
	$(RUFF) format .

format-check: ## フォーマットチェック（変更なし）
	$(RUFF) format --check .

typecheck: ## 型チェックを実行
	@echo "🔍 型チェック中..."
	$(MYPY) src/app

check: lint typecheck test ## 全チェック（lint + typecheck + test）を実行
	@echo "✅ 全チェック完了！"

pre-commit: ## pre-commitフックを手動実行
	$(UV) run pre-commit run --all-files

# ========================================
# クリーンアップ
# ========================================

clean: ## キャッシュファイルを削除
	@echo "🧹 キャッシュをクリーンアップ中..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "✅ クリーンアップ完了"

clean-all: clean down ## 全てクリーンアップ（Docker含む）
	@echo "🧹 全てクリーンアップ中..."
	docker-compose down -v
	rm -rf .venv
	@echo "✅ 完全にクリーンアップしました"

# ========================================
# ユーティリティ
# ========================================

deps-update: ## 依存関係を更新
	@echo "📦 依存関係を更新中..."
	$(UV) sync --upgrade

deps-show: ## インストール済み依存関係を表示
	$(UV) pip list

info: ## プロジェクト情報を表示
	@echo "📊 プロジェクト情報"
	@echo "===================="
	@echo "Python: $$(python3 --version)"
	@echo "uv: $$(uv --version 2>/dev/null || echo 'not installed')"
	@echo ""
	@echo "📦 Docker コンテナ:"
	@docker-compose ps 2>/dev/null || echo "Docker is not running"
	@echo ""
	@echo "🌐 エンドポイント:"
	@echo "  API:        http://localhost:8000"
	@echo "  Swagger UI: http://localhost:8000/docs"
	@echo "  ReDoc:      http://localhost:8000/redoc"
	@echo "  Health:     http://localhost:8000/health"

quick-start: setup dev ## クイックスタート（セットアップ→サーバー起動）

# ========================================
# Git & Commit
# ========================================

commit: ## 対話モードでコミット（推奨）
	./scripts/auto-commit.sh --interactive

commit-feat: ## 新機能のコミット (make commit-feat msg="message")
	@if [ -z "$(msg)" ]; then \
		echo "❌ エラー: メッセージを指定してください"; \
		echo "使用例: make commit-feat msg=\"add authentication\""; \
		exit 1; \
	fi
	./scripts/auto-commit.sh feat "$(msg)"

commit-fix: ## バグ修正のコミット (make commit-fix msg="message")
	@if [ -z "$(msg)" ]; then \
		echo "❌ エラー: メッセージを指定してください"; \
		echo "使用例: make commit-fix msg=\"resolve N+1 query\""; \
		exit 1; \
	fi
	./scripts/auto-commit.sh fix "$(msg)"

commit-docs: ## ドキュメントのコミット (make commit-docs msg="message")
	@if [ -z "$(msg)" ]; then \
		echo "❌ エラー: メッセージを指定してください"; \
		exit 1; \
	fi
	./scripts/auto-commit.sh docs "$(msg)" --no-test

commit-refactor: ## リファクタリングのコミット (make commit-refactor msg="message")
	@if [ -z "$(msg)" ]; then \
		echo "❌ エラー: メッセージを指定してください"; \
		exit 1; \
	fi
	./scripts/auto-commit.sh refactor "$(msg)"

commit-test: ## テスト追加のコミット (make commit-test msg="message")
	@if [ -z "$(msg)" ]; then \
		echo "❌ エラー: メッセージを指定してください"; \
		exit 1; \
	fi
	./scripts/auto-commit.sh test "$(msg)" --no-test

commit-quick: ## クイックコミット（チェックなし）
	@if [ -z "$(msg)" ]; then \
		echo "❌ エラー: メッセージを指定してください"; \
		echo "使用例: make commit-quick msg=\"quick fix\""; \
		exit 1; \
	fi
	./scripts/auto-commit.sh chore "$(msg)" --no-check --no-test

hooks-install: ## Gitフックをインストール
	@echo "🔧 Gitフックをインストール中..."
	@mkdir -p .git/hooks
	@ln -sf ../../scripts/hooks/post-commit .git/hooks/post-commit
	@ln -sf ../../scripts/hooks/pre-commit-doc-check .git/hooks/pre-commit-doc-check
	@chmod +x .git/hooks/*
	@echo "✅ Gitフックをインストールしました"
	@echo ""
	@echo "インストールされたフック:"
	@echo "  - post-commit: ドキュメント更新の提案"
	@echo "  - pre-commit-doc-check: ドキュメント整合性チェック"

hooks-uninstall: ## Gitフックをアンインストール
	@echo "🔧 Gitフックをアンインストール中..."
	@rm -f .git/hooks/post-commit
	@rm -f .git/hooks/pre-commit-doc-check
	@echo "✅ Gitフックをアンインストールしました"

doc-check: ## ドキュメント整合性チェック
	@echo "📚 ドキュメントの整合性チェック中..."
	@./scripts/hooks/pre-commit-doc-check
	@echo "✅ チェック完了"

# ========================================
# CI/CD
# ========================================

ci: lint typecheck test ## CIで実行されるチェック
	@echo "✅ CI チェック完了！"

deploy-build: docker-build ## デプロイ用イメージをビルド
	@echo "✅ デプロイ用イメージをビルドしました"

# ========================================
# 開発者向けショートカット
# ========================================

fix: lint-fix format ## コードを自動修正（lint + format）
	@echo "✅ コードを修正しました"

restart: down up wait-db ## Dockerを再起動
	@echo "✅ 再起動完了"

rebuild: clean-all setup ## 完全に再構築
	@echo "✅ 再構築完了"
