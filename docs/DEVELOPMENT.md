# 開発ガイド

このドキュメントでは、プロジェクトのセットアップ方法、開発フロー、よく使うコマンドを説明します。

## 前提条件

### 必要なツール

| ツール | バージョン | 用途 |
|--------|-----------|------|
| Python | 3.12+ | プログラミング言語 |
| uv | latest | パッケージマネージャー |
| Docker | latest | コンテナ環境 |
| Task | latest | タスクランナー（オプション） |

### 推奨環境

- **OS**: macOS, Linux, Windows (WSL2)
- **エディタ**: VSCode / Cursor（Dev Container対応）

---

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-org/fastapi-template.git
cd fastapi-template
```

### 2. uv のインストール

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. 依存関係のインストール

```bash
uv sync
```

これで `pyproject.toml` に基づいて依存関係がインストールされます。

### 4. 環境変数の設定

```bash
cp .env.example .env
```

`.env` を編集して必要な値を設定：

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_template
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
```

### 5. Docker Compose でデータベース起動

```bash
docker-compose up -d
```

PostgreSQL と Redis が起動します。

### 6. データベースマイグレーション

```bash
uv run alembic upgrade head
```

---

## 開発フロー

### 開発サーバーの起動

#### uvicornで直接起動

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Taskfile を使う場合

```bash
task dev
```

サーバーが起動したら、以下にアクセス：

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## よく使うコマンド

### Taskfile（推奨）

```bash
# 開発サーバー起動
task dev

# テスト実行
task test

# カバレッジ付きテスト
task test:cov

# Linting
task lint

# フォーマット
task format

# 型チェック
task typecheck

# 全チェック（lint + typecheck + test）
task check

# DBマイグレーション作成
task migration:create -- "create_users_table"

# DBマイグレーション適用
task migration:upgrade

# DBマイグレーション巻き戻し
task migration:downgrade
```

### 直接コマンド

#### テスト

```bash
# 全テスト実行
uv run pytest

# カバレッジ付き
uv run pytest --cov=app --cov-report=html

# 特定のテストのみ
uv run pytest tests/unit/modules/orders/

# マーカー指定
uv run pytest -m "not slow"
```

#### Linting & Formatting

```bash
# Linting（チェックのみ）
uv run ruff check .

# 自動修正
uv run ruff check --fix .

# フォーマット
uv run ruff format .
```

#### 型チェック

```bash
uv run mypy src/app
```

#### Alembic（DBマイグレーション）

```bash
# マイグレーション作成
uv run alembic revision --autogenerate -m "create orders table"

# マイグレーション適用
uv run alembic upgrade head

# 1つ戻す
uv run alembic downgrade -1

# 履歴確認
uv run alembic history
```

---

## Dev Container を使った開発

### Dev Container とは？

VSCode/Cursorの機能で、Docker内で完全な開発環境を構築できます。

### 使い方

1. VSCode/Cursorで `fastapi-template` を開く
2. コマンドパレット（`Cmd+Shift+P`）を開く
3. `Dev Containers: Reopen in Container` を選択
4. 自動的にコンテナがビルドされ、開発環境が起動

**利点:**
- チーム全員が同じ環境
- Python, PostgreSQL, Redis がすべて含まれる
- 拡張機能も自動インストール

---

## テスト戦略

### テストの種類

#### 1. Unit Tests（単体テスト）

**対象**: ドメイン層、アプリケーション層
**特徴**: 外部依存なし、高速

```python
# tests/unit/modules/orders/domain/entities/test_order.py
def test_order_add_item_success():
    # Arrange
    order = Order.create(customer_id)
    item = OrderItem(product_id, 2, Money(Decimal(1000)))

    # Act
    order.add_item(item)

    # Assert
    assert len(order.items) == 1
    assert order.calculate_total() == Money(Decimal(2000))
```

#### 2. Integration Tests（統合テスト）

**対象**: インフラ層（Repository実装）
**特徴**: DBアクセスあり

```python
# tests/integration/modules/orders/infrastructure/test_order_repository.py
def test_order_repository_save_and_find(db_session):
    # Arrange
    repo = OrderRepositoryImpl(db_session)
    order = Order.create(customer_id)

    # Act
    repo.save(order)
    found = repo.find_by_id(order.id)

    # Assert
    assert found is not None
    assert found.id == order.id
```

#### 3. E2E Tests（エンドツーエンドテスト）

**対象**: API全体
**特徴**: HTTPリクエスト、実際のフロー

```python
# tests/e2e/api/v1/test_orders_api.py
def test_create_order_api(client):
    # Act
    response = client.post(
        "/api/v1/orders",
        json={"customer_id": str(customer_id)}
    )

    # Assert
    assert response.status_code == 201
    assert "order_id" in response.json()
```

### Fixture の活用

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def db_session():
    """テスト用DBセッション"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()

@pytest.fixture
def client():
    """テスト用HTTPクライアント"""
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)
```

---

## デバッグ

### ログ出力

```python
import structlog

logger = structlog.get_logger()

logger.debug("debug_info", value=123)
logger.info("order_created", order_id=order.id)
logger.error("payment_failed", error=str(e))
```

### ブレークポイント

```python
# コード内にブレークポイント設置
breakpoint()
```

または VSCode/Cursor のデバッガーを使用。

### iPython

```bash
uv run ipython
```

```python
from app.modules.orders.domain.entities.order import Order
from app.shared.domain.value_objects.money import Money

order = Order.create(customer_id)
# インタラクティブに検証
```

---

## コードレビューのポイント

### チェックリスト

- [ ] 型ヒントがすべてのメソッドに付いている
- [ ] docstringがPublic APIに付いている
- [ ] テストが書かれている
- [ ] ビジネスロジックがドメイン層にある
- [ ] 依存性が正しい方向（外側→内側）
- [ ] 例外処理が適切
- [ ] ログが適切に出力されている
- [ ] N+1問題がない（Eager Loading使用）

---

## CI/CD

### GitHub Actions

`.github/workflows/ci.yml` で自動テスト・デプロイを実行。

#### CI パイプライン

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run mypy src/app
      - run: uv run pytest --cov
```

#### プルリクエストのフロー

1. ブランチ作成: `git checkout -b feature/add-payment`
2. コミット: `git commit -m "feat: add payment module"`
3. プッシュ: `git push origin feature/add-payment`
4. GitHub でPR作成
5. CIが自動実行（lint, typecheck, test）
6. レビュー・承認
7. マージ

---

## トラブルシューティング

### uv sync が失敗する

```bash
# キャッシュクリア
uv cache clean

# 再度同期
uv sync
```

### データベースに接続できない

```bash
# Docker Composeが起動しているか確認
docker-compose ps

# ログ確認
docker-compose logs postgres
```

### マイグレーションが失敗する

```bash
# 現在のリビジョン確認
uv run alembic current

# 履歴確認
uv run alembic history

# 強制的にリビジョン設定（注意！）
uv run alembic stamp head
```

### テストが失敗する

```bash
# 詳細なログ出力
uv run pytest -vv

# 特定のテストのみ実行
uv run pytest tests/unit/modules/orders/domain/entities/test_order.py::test_order_add_item_success

# デバッグモード
uv run pytest --pdb
```

---

## パフォーマンス最適化

### N+1問題の回避

```python
# Bad: N+1問題
orders = session.query(OrderModel).all()
for order in orders:
    print(order.items)  # 毎回クエリ発行

# Good: Eager Loading
from sqlalchemy.orm import selectinload

orders = (
    session.query(OrderModel)
    .options(selectinload(OrderModel.items))
    .all()
)
```

### Redisキャッシュ

```python
import redis

cache = redis.Redis.from_url(settings.redis_url)

def get_product(product_id: str) -> Product:
    # キャッシュ確認
    cached = cache.get(f"product:{product_id}")
    if cached:
        return Product.from_json(cached)

    # DB取得
    product = repo.find_by_id(product_id)

    # キャッシュ保存（TTL: 1時間）
    cache.setex(f"product:{product_id}", 3600, product.to_json())

    return product
```

---

## ベストプラクティス

### 1. 小さなコミット

```bash
# Good
git commit -m "feat: add Order.add_item method"
git commit -m "test: add test for Order.add_item"

# Bad
git commit -m "add order feature"  # 変更が大きすぎる
```

### 2. ブランチ戦略

```
main          ← 本番環境
  ├─ develop  ← 開発環境
      ├─ feature/payment
      └─ feature/shipping
```

### 3. コミットメッセージ

Conventional Commits形式を推奨：

```
feat: 新機能
fix: バグ修正
docs: ドキュメント
refactor: リファクタリング
test: テスト追加
chore: 雑務（依存関係更新等）
```

例：
```bash
git commit -m "feat: add payment processing"
git commit -m "fix: resolve N+1 query issue in order list"
git commit -m "docs: update DEVELOPMENT.md"
```

---

## 参考資料

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [uv公式ドキュメント](https://github.com/astral-sh/uv)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

## サポート

質問や問題があれば、以下を確認してください：

1. このドキュメント
2. `/docs` 内の他のドキュメント
3. GitHub Issues
4. チームのSlack/Discordチャンネル
