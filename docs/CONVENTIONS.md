# コーディング規約

このドキュメントは、プロジェクト全体で一貫性のあるコードを書くための規約を定義します。

## 基本方針

1. **Explicit is better than implicit（明示的は暗黙的より良い）**
2. **Readability counts（可読性は重要）**
3. **型ヒントを必ず使用**
4. **ビジネスロジックはドメイン層に**

---

## Python コーディングスタイル

### ベースライン
- **PEP 8** に準拠
- **ruff** でフォーマット・lintingを自動化
- **mypy** で型チェック（strict mode）

### インポート順序

```python
# 1. 標準ライブラリ
import os
from datetime import datetime
from typing import Any

# 2. サードパーティ
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

# 3. ローカル（アプリケーション）
from app.core.config import settings
from app.shared.exceptions import DomainException
from app.modules.orders.domain.entities.order import Order
```

ruff が自動でソートします。

---

## 命名規則

### 一般原則
- **英語**を使用（日本語は不可）
- **意味のある名前**を付ける
- **略語は避ける**（一般的なものを除く: id, url, api等）

### ケースの使い分け

| 対象 | ケース | 例 |
|------|--------|-----|
| 変数・関数・メソッド | snake_case | `calculate_total`, `order_id` |
| クラス | PascalCase | `Order`, `OrderItem`, `OrderRepository` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` |
| プライベート変数 | _snake_case | `_domain_events`, `_items` |
| 型変数 | PascalCase | `T`, `EntityT` |

### ドメイン層の命名

#### Entity（エンティティ）
```python
# Good
class Order:
    pass

class OrderItem:
    pass

# Bad
class OrderEntity:  # "Entity"接尾辞は不要
    pass
```

#### Value Object
```python
# Good
class Money:
    pass

class OrderId:
    pass

# Bad
class MoneyVO:  # "VO"接尾辞は不要
    pass
```

#### Repository Interface
```python
# Good
class OrderRepository(ABC):
    pass

# Bad
class IOrderRepository(ABC):  # "I"接頭辞は不要（Pythonでは一般的でない）
    pass
```

#### Repository Implementation
```python
# Good
class OrderRepositoryImpl(OrderRepository):
    pass

# または
class SQLAlchemyOrderRepository(OrderRepository):
    pass

# Bad
class OrderRepositoryImplementation:  # 長すぎる
    pass
```

#### Use Case
```python
# Good
class CreateOrderUseCase:
    pass

class GetOrderByIdQuery:
    pass

# Bad
class CreateOrder:  # "UseCase"をつけて明示的に
    pass
```

#### Domain Service
```python
# Good
class PricingService:
    pass

class InventoryService:
    pass

# Bad
class PricingDomainService:  # "Domain"は不要（コンテキストで明確）
    pass
```

---

## ファイル・ディレクトリ命名

### ファイル名
- **snake_case** を使用
- **単数形**を基本とする（複数のクラスを含む場合は複数形も可）

```
# Good
order.py
order_repository.py
create_order.py
exceptions.py

# Bad
Order.py          # PascalCaseは不可
orders-repo.py    # ハイフンは不可
```

### ディレクトリ名
- **snake_case** を使用
- **複数形**を基本とする

```
entities/
repositories/
use_cases/
value_objects/
```

---

## 型ヒント

### 基本ルール
- **すべての関数・メソッドに型ヒントを付ける**
- **戻り値も必ず型指定**（voidの場合は`-> None`）

```python
# Good
def calculate_total(items: list[OrderItem]) -> Money:
    total = Money(Decimal(0))
    for item in items:
        total = total.add(item.subtotal())
    return total

# Bad
def calculate_total(items):  # 型ヒントなし
    ...
```

### Optional型

Python 3.10+ の Union 記法を使用：

```python
# Good (Python 3.10+)
def find_by_id(self, order_id: OrderId) -> Order | None:
    pass

# Old style (避ける)
from typing import Optional
def find_by_id(self, order_id: OrderId) -> Optional[Order]:
    pass
```

### 複雑な型

```python
from typing import Protocol, TypeVar

# Protocol（インターフェース）
class SupportsComparison(Protocol):
    def __lt__(self, other: Any) -> bool: ...

# TypeVar（ジェネリクス）
T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

---

## docstring

### 方式
**Google Style** を採用

```python
def create_order(customer_id: CustomerId, items: list[OrderItem]) -> Order:
    """注文を作成する。

    Args:
        customer_id: 顧客ID
        items: 注文明細のリスト

    Returns:
        作成された注文

    Raises:
        EmptyOrderError: 注文明細が空の場合
        CustomerNotFoundError: 顧客が見つからない場合
    """
    ...
```

### どこに書くか

- **Public API**: 必須
- **ドメイン層のメソッド**: 推奨（ビジネスルール説明）
- **Private メソッド**: 任意（複雑な場合のみ）

---

## クラス設計

### dataclass の活用

Entityや Value Object は `@dataclass` を使用：

```python
from dataclasses import dataclass, field
from datetime import datetime

# Value Object（不変）
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "JPY"

# Entity（可変）
@dataclass
class Order:
    id: OrderId
    customer_id: CustomerId
    items: list[OrderItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
```

### プロパティの可視性

```python
class Order:
    def __init__(self):
        self._items: list[OrderItem] = []  # プライベート
        self._domain_events: list[DomainEvent] = []

    @property
    def items(self) -> list[OrderItem]:
        """外部には読み取り専用で公開"""
        return self._items.copy()

    def add_item(self, item: OrderItem) -> None:
        """変更はメソッド経由のみ"""
        self._items.append(item)
```

---

## 例外処理

### カスタム例外の階層

```python
# shared/exceptions.py
class AppException(Exception):
    """アプリケーション全体の例外基底クラス"""
    pass

class DomainException(AppException):
    """ドメイン層の例外"""
    pass

class InfrastructureException(AppException):
    """インフラ層の例外"""
    pass

# modules/orders/domain/exceptions.py
class OrderException(DomainException):
    """注文関連の例外"""
    pass

class OrderNotFoundError(OrderException):
    """注文が見つからない"""
    pass

class EmptyOrderError(OrderException):
    """注文明細が空"""
    pass
```

### 例外の使い分け

- **ビジネスルール違反**: カスタム例外
- **データが見つからない**: `NotFoundError`
- **予期しないエラー**: 標準例外（`ValueError`, `TypeError`等）

```python
# Good
if not order.items:
    raise EmptyOrderError("注文明細が必要です")

# Bad
if not order.items:
    raise Exception("Error")  # 汎用的すぎる
```

---

## 依存性注入

### FastAPI Depends の活用

```python
# Good: 依存性を明示的に注入
@router.post("/orders")
def create_order(
    request: CreateOrderRequest,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
) -> CreateOrderResponse:
    ...

# Bad: グローバル変数や直接インスタンス化
use_case = CreateOrderUseCase(...)  # アンチパターン
```

### Dependency関数の命名

```python
# dependencies.py

# Good
def get_db_session() -> Generator[Session, None, None]:
    pass

def get_order_repository(session: Session = Depends(get_db_session)) -> OrderRepository:
    pass

# Bad
def db_session():  # "get_"接頭辞を推奨
    pass
```

---

## テストコード

### テスト関数の命名

```python
# Good: test_{対象}_{条件}_{期待結果}
def test_order_add_item_success():
    pass

def test_order_add_item_when_already_confirmed_raises_error():
    pass

# Bad
def test1():  # 何をテストしているか不明
    pass
```

### Arrange-Act-Assert パターン

```python
def test_order_calculate_total():
    # Arrange（準備）
    order = Order.create(customer_id)
    item1 = OrderItem(product_id, 2, Money(Decimal(1000)))
    item2 = OrderItem(product_id2, 1, Money(Decimal(500)))
    order.add_item(item1)
    order.add_item(item2)

    # Act（実行）
    total = order.calculate_total()

    # Assert（検証）
    assert total == Money(Decimal(2500))
```

---

## コメント

### 原則
- **コードで表現できることはコメント不要**
- **WHY（なぜ）を書く、WHAT（何を）は書かない**

```python
# Good: なぜこうするのかを説明
# NOTE: 在庫確保のタイミングで二重予約を防ぐため、楽観的ロックを使用
order.reserve_inventory()

# Bad: コードを読めばわかることを繰り返す
# 在庫を予約する
order.reserve_inventory()
```

### コメントの種類

```python
# TODO: 後で実装する必要がある
# FIXME: 既知のバグ、修正が必要
# NOTE: 重要な注意事項
# HACK: 暫定的な対応、リファクタリング推奨
```

---

## ロギング

### ログレベルの使い分け

```python
import structlog

logger = structlog.get_logger()

# DEBUG: 開発時のデバッグ情報
logger.debug("order_details", order_id=order.id, items=len(order.items))

# INFO: 通常の動作ログ
logger.info("order_created", order_id=order.id)

# WARNING: 警告（継続可能）
logger.warning("low_stock", product_id=product.id, stock=product.stock)

# ERROR: エラー（処理失敗）
logger.error("payment_failed", order_id=order.id, reason=str(e))

# CRITICAL: 致命的エラー
logger.critical("database_connection_lost")
```

### 構造化ログ

```python
# Good: 構造化（検索・集計しやすい）
logger.info(
    "order_confirmed",
    order_id=str(order.id),
    customer_id=str(order.customer_id),
    total_amount=float(order.calculate_total().amount),
)

# Bad: フリーテキスト
logger.info(f"Order {order.id} confirmed for customer {order.customer_id}")
```

---

## 設定管理

### pydantic-settings を使用

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str
    database_echo: bool = False

    # Redis
    redis_url: str

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()
```

---

## SQL・クエリ

### N+1問題の回避

```python
# Good: Eager Loading
from sqlalchemy.orm import selectinload

def find_orders_with_items(self) -> list[Order]:
    stmt = (
        select(OrderModel)
        .options(selectinload(OrderModel.items))
    )
    result = self.session.execute(stmt)
    return [self._to_entity(model) for model in result.scalars()]

# Bad: Lazy Loading（N+1問題発生）
def find_orders_with_items(self) -> list[Order]:
    orders = self.session.query(OrderModel).all()
    # この後、order.itemsにアクセスすると毎回クエリが発行される
    return [self._to_entity(model) for model in orders]
```

---

## まとめ

このコーディング規約は：

✅ **一貫性**: チーム全体で統一されたコード
✅ **可読性**: 誰が読んでも理解しやすい
✅ **保守性**: 長期的なメンテナンスが容易
✅ **自動化**: ruff/mypyで機械的にチェック

新しいコードを書く際は、常にこのドキュメントを参照してください。
