# フォルダ構造

このドキュメントでは、プロジェクト全体のフォルダ構造と、各ディレクトリ・ファイルの役割を説明します。

## 全体構成

```
fastapi-template/
├── .devcontainer/           # Dev Container設定
├── .github/                 # GitHub Actions（CI/CD）
├── alembic/                 # DBマイグレーション
├── docs/                    # プロジェクトドキュメント
├── src/                     # ソースコード
│   └── app/
├── tests/                   # テストコード
├── scripts/                 # ユーティリティスクリプト
├── docker-compose.yml       # ローカル開発環境
├── Dockerfile               # 本番用イメージ
├── pyproject.toml           # プロジェクト設定（uv）
├── Taskfile.yml             # タスクランナー設定
└── README.md                # プロジェクト説明
```

---

## ルートレベル

### 設定ファイル

#### `pyproject.toml`
プロジェクトの中心的な設定ファイル。

```toml
[project]
name = "fastapi-template"
version = "0.1.0"
dependencies = [...]

[tool.ruff]
# linter/formatter設定

[tool.mypy]
# 型チェック設定

[tool.pytest.ini_options]
# テスト設定
```

#### `Taskfile.yml`
タスクランナー（go-task）の設定。

```yaml
version: '3'

tasks:
  dev:
    desc: "開発サーバー起動"
    cmds:
      - uv run uvicorn app.main:app --reload

  test:
    desc: "テスト実行"
    cmds:
      - uv run pytest

  lint:
    desc: "Linting実行"
    cmds:
      - uv run ruff check .
```

#### `.env.example`
環境変数のテンプレート。

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
```

---

## `/docs` - ドキュメント

プロジェクトの設計思想や規約を記載。

```
docs/
├── TECH_STACK.md          # 技術スタック
├── ARCHITECTURE.md        # アーキテクチャ設計
├── DOMAIN_MODEL.md        # ドメインモデル
├── CONVENTIONS.md         # コーディング規約
├── FOLDER_STRUCTURE.md    # このファイル
├── DEVELOPMENT.md         # 開発ガイド
└── PATTERNS.md            # 実装パターン集
```

**目的**: AIや新しい開発者が常に参照し、一貫性のある開発を進めるため。

---

## `/src/app` - アプリケーションコード

### 全体構造

```
src/app/
├── __init__.py
├── main.py                 # FastAPIアプリケーションのエントリーポイント
├── core/                   # コア機能（全体で共有）
│   ├── config.py           # 設定管理
│   ├── database.py         # DB接続
│   ├── security.py         # 認証・セキュリティ
│   └── logging.py          # ロギング設定
├── shared/                 # 共有コード
│   ├── domain/
│   │   ├── value_objects/
│   │   │   ├── money.py
│   │   │   ├── email.py
│   │   │   └── address.py
│   │   └── events.py       # ドメインイベント基底クラス
│   ├── exceptions.py       # 共通例外
│   └── utils/              # ユーティリティ
├── modules/                # 機能モジュール（Bounded Context）
│   ├── catalog/            # 商品カタログ（レイヤード例）
│   └── orders/             # 注文（DDD例）
└── api/                    # API統合
    └── v1/
        └── router.py       # 全エンドポイント統合
```

---

## `/src/app/core` - コア機能

全体で共有する基盤機能。

### `core/config.py`
設定管理（pydantic-settings使用）。

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    # ...

settings = Settings()
```

### `core/database.py`
データベース接続設定。

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
```

### `core/security.py`
認証・認可の実装。

```python
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def create_access_token(data: dict) -> str:
    ...

def verify_password(plain: str, hashed: str) -> bool:
    ...
```

---

## `/src/app/shared` - 共有コード

### `shared/domain/value_objects/`
全コンテキストで使用できるValue Object。

```
shared/domain/value_objects/
├── money.py       # 金額
├── email.py       # メールアドレス
└── address.py     # 住所
```

### `shared/exceptions.py`
共通例外階層。

```python
class AppException(Exception):
    """アプリケーション全体の例外基底"""
    pass

class DomainException(AppException):
    """ドメイン層の例外"""
    pass

class InfrastructureException(AppException):
    """インフラ層の例外"""
    pass
```

---

## `/src/app/modules` - 機能モジュール

各Bounded Contextをモジュールとして配置。

### シンプルなモジュール例: `modules/catalog`（レイヤードアーキテクチャ）

```
modules/catalog/
├── __init__.py
├── router.py               # FastAPI router
├── schemas.py              # Pydanticスキーマ
├── service.py              # ビジネスロジック（薄い）
├── repository.py           # DB操作（具象クラス）
├── models.py               # SQLAlchemyモデル
├── dependencies.py         # 依存性注入
└── exceptions.py           # カタログ固有の例外
```

**特徴**:
- フラットな構造
- シンプルなCRUD
- ドメイン層とインフラ層の分離が緩い

---

### 複雑なモジュール例: `modules/orders`（DDDフル適用）

```
modules/orders/
├── __init__.py
├── domain/                          # ドメイン層
│   ├── entities/
│   │   ├── order.py                 # Orderエンティティ（Aggregate Root）
│   │   └── order_item.py            # OrderItemエンティティ
│   ├── value_objects/
│   │   ├── order_id.py
│   │   ├── order_status.py
│   │   └── customer_id.py
│   ├── repositories/
│   │   └── order_repository.py      # Interface（Port）
│   ├── services/
│   │   └── pricing_service.py       # Domain Service
│   ├── events/
│   │   ├── order_created.py
│   │   └── order_confirmed.py
│   └── exceptions.py                # ドメイン例外
│
├── application/                     # アプリケーション層
│   ├── use_cases/
│   │   ├── create_order.py          # Use Case
│   │   ├── add_item_to_order.py
│   │   └── confirm_order.py
│   └── dto/
│       ├── commands.py              # Command DTO
│       └── queries.py               # Query DTO
│
├── infrastructure/                  # インフラ層
│   ├── persistence/
│   │   ├── models.py                # SQLAlchemyモデル
│   │   └── order_repository_impl.py # Repository実装（Adapter）
│   └── external/
│       └── inventory_api.py         # 外部API連携
│
└── presentation/                    # プレゼンテーション層
    ├── api/
    │   └── v1/
    │       └── orders.py            # FastAPI router
    ├── schemas/
    │   ├── request.py               # リクエストスキーマ
    │   └── response.py              # レスポンススキーマ
    └── dependencies.py              # 依存性注入
```

**特徴**:
- 明確な層分離
- ドメインロジックが保護されている
- 複雑なビジネスルールに対応

---

## 各層の詳細

### Domain Layer（ドメイン層）

#### `domain/entities/`
ビジネスの中心的なオブジェクト。

```python
# domain/entities/order.py
from dataclasses import dataclass, field

@dataclass
class Order:
    id: OrderId
    customer_id: CustomerId
    items: list[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING

    def add_item(self, item: OrderItem) -> None:
        """ビジネスルール: 商品を追加"""
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedException()
        self.items.append(item)
```

#### `domain/value_objects/`
不変な値オブジェクト。

```python
# domain/value_objects/order_id.py
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class OrderId:
    value: UUID

    @classmethod
    def generate(cls) -> "OrderId":
        return cls(uuid4())
```

#### `domain/repositories/`
リポジトリのインターフェース（Port）。

```python
# domain/repositories/order_repository.py
from abc import ABC, abstractmethod

class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: OrderId) -> Order | None:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass
```

#### `domain/services/`
エンティティに属さないドメインロジック。

```python
# domain/services/pricing_service.py
class PricingService:
    def calculate_total_with_tax(self, order: Order) -> Money:
        """税込み合計を計算"""
        subtotal = order.calculate_total()
        tax = subtotal.multiply(Decimal("0.1"))  # 10%
        return subtotal.add(tax)
```

---

### Application Layer（アプリケーション層）

#### `application/use_cases/`
ユースケースの実装。

```python
# application/use_cases/create_order.py
from dataclasses import dataclass

@dataclass
class CreateOrderCommand:
    customer_id: str

class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    def execute(self, command: CreateOrderCommand) -> OrderId:
        customer_id = CustomerId(UUID(command.customer_id))
        order = Order.create(customer_id)
        self.order_repo.save(order)
        return order.id
```

---

### Infrastructure Layer（インフラ層）

#### `infrastructure/persistence/`
データベース関連の実装。

```python
# infrastructure/persistence/models.py
from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String, nullable=False)
```

```python
# infrastructure/persistence/order_repository_impl.py
class OrderRepositoryImpl(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, order_id: OrderId) -> Order | None:
        model = self.session.get(OrderModel, order_id.value)
        return self._to_entity(model) if model else None

    def save(self, order: Order) -> None:
        model = self._to_model(order)
        self.session.add(model)
        self.session.commit()
```

---

### Presentation Layer（プレゼンテーション層）

#### `presentation/api/v1/`
FastAPI router。

```python
# presentation/api/v1/orders.py
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=CreateOrderResponse)
def create_order(
    request: CreateOrderRequest,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
):
    command = CreateOrderCommand(customer_id=request.customer_id)
    order_id = use_case.execute(command)
    return CreateOrderResponse(order_id=str(order_id.value))
```

#### `presentation/schemas/`
リクエスト/レスポンスのPydanticモデル。

```python
# presentation/schemas/request.py
from pydantic import BaseModel

class CreateOrderRequest(BaseModel):
    customer_id: str

# presentation/schemas/response.py
class CreateOrderResponse(BaseModel):
    order_id: str
```

---

## `/tests` - テストコード

ソースコードと同じ構造でテストを配置。

```
tests/
├── unit/                    # 単体テスト（外部依存なし）
│   └── modules/
│       └── orders/
│           └── domain/
│               └── entities/
│                   └── test_order.py
│
├── integration/             # 統合テスト（DB接続あり）
│   └── modules/
│       └── orders/
│           └── infrastructure/
│               └── test_order_repository.py
│
└── e2e/                     # E2Eテスト（API全体）
    └── api/
        └── v1/
            └── test_orders_api.py
```

---

## `/alembic` - DBマイグレーション

Alembicによるマイグレーションスクリプト。

```
alembic/
├── versions/
│   ├── 001_create_orders_table.py
│   └── 002_add_status_column.py
├── env.py
└── alembic.ini
```

---

## まとめ

### シンプルな機能
`modules/catalog/` のようなフラットな構造。

### 複雑な機能
`modules/orders/` のような4層構造。

### 判断基準
- CRUD中心 → レイヤード
- 複雑なビジネスルール → DDD

このフォルダ構造は、拡張性と保守性を両立させるために設計されています。
