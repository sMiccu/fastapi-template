# FastAPI Template

モダンなFastAPIバックエンドテンプレート - DDDとヘキサゴナルアーキテクチャを採用

[![CI](https://github.com/your-org/fastapi-template/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/fastapi-template/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/uv-latest-orange.svg)](https://github.com/astral-sh/uv)

## 📋 特徴

- ✅ **モダンな技術スタック**: Python 3.12+, FastAPI, SQLAlchemy 2.0, uv
- ✅ **DDDアーキテクチャ**: ドメイン駆動設計とヘキサゴナルアーキテクチャ
- ✅ **ハイブリッドアプローチ**: シンプルな機能はレイヤード、複雑な機能はDDDフル適用
- ✅ **型安全**: mypy strictモード対応
- ✅ **高速な開発体験**: ruffによるlint/format、uvによる高速なパッケージ管理
- ✅ **テスト完備**: Unit/Integration/E2Eテスト
- ✅ **Dev Container対応**: VSCode/Cursorで即座に開発環境構築
- ✅ **CI/CD**: GitHub Actionsによる自動テスト・ビルド

## 🏗️ アーキテクチャ

このテンプレートは2つのアーキテクチャパターンを提供します：

### 1. レイヤードアーキテクチャ（シンプルなCRUD向け）
```
📁 modules/catalog/
  ├── router.py        # API
  ├── service.py       # ビジネスロジック
  ├── repository.py    # DB操作
  └── models.py        # SQLAlchemy
```

### 2. DDDヘキサゴナル（複雑なビジネスロジック向け）
```
📁 modules/orders/
  ├── domain/              # ドメイン層（ビジネスルール）
  │   ├── entities/
  │   ├── value_objects/
  │   └── repositories/    # Interface (Port)
  ├── application/         # アプリケーション層（ユースケース）
  │   └── use_cases/
  ├── infrastructure/      # インフラ層（実装）
  │   └── persistence/     # Repository実装 (Adapter)
  └── presentation/        # プレゼンテーション層（API）
```

## 🚀 クイックスタート

> **💡 急いでいる方へ**: [QUICKSTART.md](QUICKSTART.md) を参照してください（30秒でセットアップ）

### 必須要件

- Python 3.12+
- Docker & Docker Compose
- [uv](https://github.com/astral-sh/uv) (推奨)
- [Task](https://taskfile.dev/) (オプション)

### セットアップ（3つの方法）

#### 🚀 方法1: ワンコマンドセットアップ（最も簡単！推奨）

```bash
# リポジトリをクローン
git clone https://github.com/your-org/fastapi-template.git
cd fastapi-template

# 1コマンドで全自動セットアップ
make setup
```

これだけで以下が全て自動実行されます：
- ✅ uvのインストールチェック
- ✅ 依存関係のインストール
- ✅ .envファイルの作成（ランダムなSECRET_KEY生成）
- ✅ Docker起動（PostgreSQL + Redis）
- ✅ マイグレーション実行
- ✅ テスト実行

#### 🔧 方法2: シェルスクリプト

```bash
# より詳細な出力が欲しい場合
./scripts/setup.sh

# 本番環境用
./scripts/setup.sh --prod

# テストをスキップ
./scripts/setup.sh --skip-tests
```

#### 📝 方法3: 手動セットアップ

```bash
# 1. uvをインストール（未インストールの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 依存関係をインストール
uv sync --all-extras

# 3. 環境変数を設定
make create-env  # または手動で.envを作成

# 4. データベースを起動
docker-compose up -d

# 5. マイグレーションを実行
uv run alembic upgrade head

# 6. 開発サーバーを起動
uv run uvicorn app.main:app --reload
```

### クイック修正

エラーが出た場合、以下で自動修正：

```bash
./scripts/quick-fix.sh
```

アプリケーションが起動したら、以下にアクセス：
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📖 ドキュメント

### 🌟 まずこれを見る！
- **[CHEATSHEET.md](CHEATSHEET.md)** - よく使うコマンド一覧（これだけでOK）📋

### クイックリンク
- **[QUICKSTART.md](QUICKSTART.md)** - 30秒でセットアップ ⚡
- **[CURSOR_GUIDE.md](CURSOR_GUIDE.md)** - Cursor AI 活用ガイド 🤖

### 詳細ドキュメント ([`docs/`](docs/))

- [技術スタック](docs/TECH_STACK.md) - 使用技術と選定理由
- [アーキテクチャ設計](docs/ARCHITECTURE.md) - DDDとヘキサゴナルアーキテクチャの詳細
- [ドメインモデル](docs/DOMAIN_MODEL.md) - ECサイトを例にしたドメイン設計
- [コーディング規約](docs/CONVENTIONS.md) - 命名規則、型ヒント等
- [フォルダ構造](docs/FOLDER_STRUCTURE.md) - プロジェクト構造の詳細
- [開発ガイド](docs/DEVELOPMENT.md) - セットアップ、コマンド、デバッグ方法
- [実装パターン集](docs/PATTERNS.md) - よく使うコードパターン
- [Git ワークフロー](docs/GIT_WORKFLOW.md) - コミット規約、自動化

## 🛠️ よく使うコマンド

### セットアップ・管理

```bash
make setup          # 完全セットアップ（初回実行推奨）
make quick-start    # セットアップ→サーバー起動
make info           # プロジェクト情報表示
make help           # 全コマンド表示
```

### コミット・Git

```bash
make commit                    # 対話モードでコミット（推奨）
make commit-feat msg="..."     # 新機能のコミット
make commit-fix msg="..."      # バグ修正のコミット
make commit-docs msg="..."     # ドキュメント更新
make hooks-install             # Gitフックをインストール
```

> 詳細は [Git ワークフロー](docs/GIT_WORKFLOW.md) を参照

### 開発

```bash
make dev            # 開発サーバー起動（ホットリロード）
make dev-bg         # バックグラウンドで起動
make shell          # IPythonシェル起動
make restart        # Docker再起動
```

### テスト

```bash
make test           # 全テスト実行
make test-unit      # 単体テストのみ
make test-cov       # カバレッジ付きテスト
make test-e2e       # E2Eテストのみ
```

### コード品質

```bash
make lint           # Lintチェック
make lint-fix       # 自動修正
make format         # フォーマット
make typecheck      # 型チェック
make check          # 全チェック（lint + typecheck + test）
make fix            # 自動修正（lint + format）
```

### データベース

```bash
make db-upgrade                      # マイグレーション適用
make db-migrate msg="create users"   # マイグレーション作成
make db-history                      # マイグレーション履歴
make db-reset                        # DB完全リセット（注意！）
```

### Docker

```bash
make up             # Docker起動
make down           # Docker停止
make logs           # ログ表示
make ps             # コンテナ状態表示
```

### クリーンアップ

```bash
make clean          # キャッシュ削除
make clean-all      # 完全クリーンアップ（Docker + venv）
make rebuild        # 完全再構築
```

## 📁 プロジェクト構造

```
fastapi-template/
├── docs/                   # ドキュメント
├── src/app/               # アプリケーションコード
│   ├── core/              # コア機能（設定、DB、セキュリティ）
│   ├── shared/            # 共有コード（Value Objects等）
│   ├── modules/           # 機能モジュール
│   │   ├── catalog/       # レイヤードアーキテクチャ例
│   │   └── orders/        # DDDフル適用例
│   ├── api/               # API統合
│   └── main.py            # エントリーポイント
├── tests/                 # テストコード
├── alembic/               # DBマイグレーション
├── docker-compose.yml     # ローカル開発環境
├── Dockerfile             # 本番用イメージ
├── pyproject.toml         # プロジェクト設定
├── Taskfile.yml           # タスク定義
└── README.md              # このファイル
```

## 🧪 テスト

3種類のテストを用意：

### 1. Unit Tests（単体テスト）
```bash
# ドメインロジックのテスト（外部依存なし）
uv run pytest tests/unit/ -m unit
```

### 2. Integration Tests（統合テスト）
```bash
# DB接続を含むテスト
uv run pytest tests/integration/ -m integration
```

### 3. E2E Tests（エンドツーエンドテスト）
```bash
# API全体のテスト
uv run pytest tests/e2e/ -m e2e
```

## 🐳 Dev Container

VSCode/Cursorで開発コンテナを使用：

1. プロジェクトを開く
2. `Cmd+Shift+P` → "Dev Containers: Reopen in Container"
3. 自動的に環境構築が完了

**含まれるもの:**
- Python 3.12
- PostgreSQL
- Redis
- 必要な拡張機能

## 🔄 CI/CD

GitHub Actionsで自動化：

- ✅ Linting（ruff）
- ✅ 型チェック（mypy）
- ✅ テスト（pytest）
- ✅ Dockerイメージビルド

プルリクエストごとに自動実行されます。

## 🤝 開発フロー

1. **ブランチ作成**: `git checkout -b feature/new-feature`
2. **コード実装**: ドキュメントを参照しながら実装
3. **自動コミット**: `make commit-feat msg="add new feature"`
   - 自動で lint/format/test 実行
   - Conventional Commits形式で自動コミット
   - リモートに自動プッシュ
   - ドキュメント整合性チェック
4. **プルリクエスト作成**: GitHub上でPR作成
5. **CIチェック**: 自動的に実行
6. **レビュー・マージ**

> 詳細は [Git ワークフロー](docs/GIT_WORKFLOW.md) を参照

## 📝 コミットメッセージ規約

Conventional Commits形式を推奨：

```
feat: 新機能
fix: バグ修正
docs: ドキュメント
refactor: リファクタリング
test: テスト追加
chore: 雑務（依存関係更新等）
```

## 🎯 使用例

### シンプルなCRUD（Catalogモジュール）

```python
# 商品一覧取得
GET /api/v1/products

# 商品作成
POST /api/v1/products
{
  "name": "Product Name",
  "price": 1000,
  "stock_quantity": 10
}
```

### 複雑なビジネスロジック（Orderモジュール）

```python
# 1. 注文作成
POST /api/v1/orders
{
  "customer_id": "uuid-here"
}

# 2. 商品追加
POST /api/v1/orders/{order_id}/items
{
  "product_id": "uuid-here",
  "quantity": 2,
  "unit_price": 1000
}

# 3. 注文確定
POST /api/v1/orders/{order_id}/confirm
```

## 🔧 トラブルシューティング

### データベース接続エラー
```bash
# Docker Composeが起動しているか確認
docker-compose ps

# ログ確認
docker-compose logs postgres
```

### テストが失敗する
```bash
# キャッシュをクリア
task clean

# 依存関係を再インストール
uv sync

# 詳細なログで実行
uv run pytest -vv
```

詳細は [DEVELOPMENT.md](docs/DEVELOPMENT.md) を参照してください。

## 📄 ライセンス

このプロジェクトは[Apache License 2.0](LICENSE)の下でライセンスされています。

## 🙏 謝辞

このテンプレートは以下の優れたプロジェクトとリソースに影響を受けています：

- [FastAPI](https://fastapi.tiangolo.com/)
- [uv](https://github.com/astral-sh/uv)
- Eric Evans『ドメイン駆動設計』
- Vaughn Vernon『実践ドメイン駆動設計』
- Robert C. Martin『Clean Architecture』

## 📧 サポート

質問や問題があれば、以下を確認してください：

1. [ドキュメント](docs/)
2. [GitHub Issues](https://github.com/your-org/fastapi-template/issues)
3. [GitHub Discussions](https://github.com/your-org/fastapi-template/discussions)

---

**Happy Coding! 🚀**
