# 実装パターン集

このドキュメントでは、よく使う実装パターンと具体的なコード例を提供します。

## 目次

1. [Entity実装パターン](#entity実装パターン)
2. [Value Object実装パターン](#value-object実装パターン)
3. [Repository実装パターン](#repository実装パターン)
4. [Use Case実装パターン](#use-case実装パターン)
5. [API実装パターン](#api実装パターン)
6. [依存性注入パターン](#依存性注入パターン)
7. [エラーハンドリングパターン](#エラーハンドリングパターン)
8. [テストパターン](#テストパターン)

---

## Entity実装パターン

### 基本的なEntity

```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

@dataclass
class Order:
    """注文エンティティ（Aggregate Root）"""
    id: OrderId
    customer_id: CustomerId
    items: list[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(cls, customer_id: CustomerId) -> "Order":
        """ファクトリメソッド"""
        return cls(
            id=OrderId.generate(),
            customer_id=customer_id,
        )

    def add_item(self, item: OrderItem) -> None:
        """ビジネスルールを含むメソッド"""
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedException()
        self.items.append(item)

    def calculate_total(self) -> Money:
        """集約内の計算"""
        total = Money(Decimal(0))
        for item in self.items:
            total = total.add(item.subtotal())
        return total
```

---

## Value Object実装パターン

### 不変なValue Object

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    """金額Value Object"""
    amount: Decimal
    currency: str = "JPY"

    def add(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError()
```

---

## Repository実装パターン

### Interface（Port）

```python
from abc import ABC, abstractmethod

class OrderRepository(ABC):
    """注文リポジトリのインターフェース"""

    @abstractmethod
    def find_by_id(self, order_id: OrderId) -> Order | None:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass
```

### 実装（Adapter）

```python
from sqlalchemy.orm import Session

class OrderRepositoryImpl(OrderRepository):
    """SQLAlchemyを使った実装"""

    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, order_id: OrderId) -> Order | None:
        model = self.session.get(OrderModel, order_id.value)
        return self._to_entity(model) if model else None

    def save(self, order: Order) -> None:
        model = self._to_model(order)
        self.session.add(model)
        self.session.commit()

    def _to_entity(self, model: OrderModel) -> Order:
        """ORMモデル → Entityへ変換"""
        return Order(
            id=OrderId(model.id),
            customer_id=CustomerId(model.customer_id),
            status=OrderStatus(model.status),
        )

    def _to_model(self, entity: Order) -> OrderModel:
        """Entity → ORMモデルへ変換"""
        return OrderModel(
            id=entity.id.value,
            customer_id=entity.customer_id.value,
            status=entity.status.value,
        )
```

---

## Use Case実装パターン

### Command（更新系）

```python
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

### Query（参照系）

```python
@dataclass
class GetOrderQuery:
    order_id: str

class GetOrderUseCase:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    def execute(self, query: GetOrderQuery) -> Order:
        order_id = OrderId(UUID(query.order_id))
        order = self.order_repo.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()
        return order
```

---

## API実装パターン

### Router

```python
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    request: CreateOrderRequest,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
) -> CreateOrderResponse:
    command = CreateOrderCommand(customer_id=request.customer_id)
    order_id = use_case.execute(command)
    return CreateOrderResponse(order_id=str(order_id.value))
```

### Schemas（Pydantic）

```python
from pydantic import BaseModel, Field

class CreateOrderRequest(BaseModel):
    customer_id: str = Field(..., description="顧客ID")

class CreateOrderResponse(BaseModel):
    order_id: str = Field(..., description="作成された注文ID")
```

---

## 依存性注入パターン

```python
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_order_repository(
    session: Session = Depends(get_db_session)
) -> OrderRepository:
    return OrderRepositoryImpl(session)

def get_create_order_use_case(
    repo: OrderRepository = Depends(get_order_repository)
) -> CreateOrderUseCase:
    return CreateOrderUseCase(repo)
```

---

## エラーハンドリングパターン

### カスタム例外

```python
class OrderException(DomainException):
    pass

class OrderNotFoundError(OrderException):
    pass

# FastAPIでのハンドリング
@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )
```

---

## テストパターン

### Unit Test

```python
def test_order_add_item():
    order = Order.create(customer_id)
    item = OrderItem(product_id, 1, Money(Decimal(1000)))

    order.add_item(item)

    assert len(order.items) == 1
```

### Integration Test

```python
def test_order_repository_save(db_session):
    repo = OrderRepositoryImpl(db_session)
    order = Order.create(customer_id)

    repo.save(order)
    found = repo.find_by_id(order.id)

    assert found.id == order.id
```

---

詳細な実装例は、`src/app/modules/` 配下のコードを参照してください。
