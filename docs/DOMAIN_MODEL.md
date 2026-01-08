# ドメインモデル設計

## 概要

このテンプレートでは、**ECサイト（オンラインショップ）**をドメイン例として採用しています。
シンプルかつ理解しやすく、DDDの概念を学ぶのに最適なドメインです。

## Bounded Context（境界付けられたコンテキスト）

システムを以下の4つのコンテキストに分割します：

```
┌─────────────────────────────────────────────────────────┐
│                    E-Commerce System                     │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Catalog    │  │    Order     │  │   Payment    │  │
│  │   Context    │  │   Context    │  │   Context    │  │
│  │              │  │              │  │              │  │
│  │  - Product   │  │  - Order     │  │  - Payment   │  │
│  │  - Category  │  │  - OrderItem │  │  - Invoice   │  │
│  │  - Inventory │  │  - Customer  │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                           │
│  ┌──────────────┐                                        │
│  │   Shipping   │                                        │
│  │   Context    │                                        │
│  │              │                                        │
│  │  - Shipment  │                                        │
│  │  - Delivery  │                                        │
│  └──────────────┘                                        │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Context Map（コンテキスト間の関係）

```
Catalog Context
    ↓ (provides product info)
Order Context
    ↓ (triggers payment)
Payment Context
    ↓ (triggers shipment)
Shipping Context
```

### 関係性の種類

- **Catalog → Order**: Customer-Supplier（カスタマー・サプライヤー）
  - Orderは商品情報を参照するが、Catalogは注文を知らない

- **Order → Payment**: Customer-Supplier
  - 注文完了後に決済を要求

- **Payment → Shipping**: Partnership（パートナーシップ）
  - 決済完了後に配送を開始

---

## 1. Catalog Context（商品カタログ）

### 概要
商品の管理、在庫確認、カテゴリ分類を扱う。
**シンプルなCRUD中心**のため、レイヤードアーキテクチャで実装。

### エンティティ

#### Product（商品）
```python
@dataclass
class Product:
    id: ProductId
    name: str
    description: str
    price: Money
    category_id: CategoryId
    stock_quantity: int
    is_active: bool

    def is_available(self) -> bool:
        """在庫があるか？"""
        return self.is_active and self.stock_quantity > 0

    def reduce_stock(self, quantity: int) -> None:
        """在庫を減らす"""
        if quantity > self.stock_quantity:
            raise InsufficientStockError()
        self.stock_quantity -= quantity
```

#### Category（カテゴリ）
```python
@dataclass
class Category:
    id: CategoryId
    name: str
    parent_id: CategoryId | None
    slug: str
```

### Value Objects

#### ProductId
```python
@dataclass(frozen=True)
class ProductId:
    value: UUID

    @classmethod
    def generate(cls) -> "ProductId":
        return cls(uuid4())
```

### リポジトリ

```python
class ProductRepository(ABC):
    @abstractmethod
    def find_by_id(self, product_id: ProductId) -> Product | None:
        pass

    @abstractmethod
    def find_by_category(self, category_id: CategoryId) -> list[Product]:
        pass

    @abstractmethod
    def save(self, product: Product) -> None:
        pass
```

### ユースケース（簡易版）

- 商品一覧取得
- 商品詳細取得
- カテゴリ別商品検索
- 在庫確認

---

## 2. Order Context（注文）

### 概要
注文処理、在庫確保、価格計算、状態管理を扱う。
**複雑なビジネスルール**があるため、DDDフル適用。

### エンティティ

#### Order（注文）- Aggregate Root
```python
class Order:
    def __init__(
        self,
        id: OrderId,
        customer_id: CustomerId,
        items: list[OrderItem],
        status: OrderStatus,
        created_at: datetime,
    ):
        self.id = id
        self.customer_id = customer_id
        self._items = items  # Aggregateの境界
        self.status = status
        self.created_at = created_at
        self._domain_events: list[DomainEvent] = []

    @classmethod
    def create(cls, customer_id: CustomerId) -> "Order":
        """注文を新規作成"""
        order = cls(
            id=OrderId.generate(),
            customer_id=customer_id,
            items=[],
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
        )
        order._add_event(OrderCreatedEvent(order.id))
        return order

    def add_item(
        self,
        product_id: ProductId,
        quantity: int,
        unit_price: Money,
    ) -> None:
        """商品を追加"""
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedException()

        if quantity <= 0:
            raise InvalidQuantityError()

        item = OrderItem(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        self._items.append(item)

    def confirm(self) -> None:
        """注文を確定"""
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedException()

        if not self._items:
            raise EmptyOrderError()

        self.status = OrderStatus.CONFIRMED
        self._add_event(OrderConfirmedEvent(self.id, self.calculate_total()))

    def cancel(self) -> None:
        """注文をキャンセル"""
        if self.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise OrderCannotBeCancelledError()

        self.status = OrderStatus.CANCELLED
        self._add_event(OrderCancelledEvent(self.id))

    def calculate_total(self) -> Money:
        """合計金額を計算"""
        total = Money(Decimal(0))
        for item in self._items:
            total = total.add(item.subtotal())
        return total

    @property
    def items(self) -> list[OrderItem]:
        """外部からは読み取り専用"""
        return self._items.copy()

    def _add_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)
```

#### OrderItem（注文明細）
```python
@dataclass
class OrderItem:
    product_id: ProductId
    quantity: int
    unit_price: Money

    def subtotal(self) -> Money:
        """小計を計算"""
        return Money(
            self.unit_price.amount * Decimal(self.quantity),
            self.unit_price.currency
        )
```

### Value Objects

#### OrderId
```python
@dataclass(frozen=True)
class OrderId:
    value: UUID

    @classmethod
    def generate(cls) -> "OrderId":
        return cls(uuid4())
```

#### OrderStatus（列挙型）
```python
class OrderStatus(Enum):
    PENDING = "pending"          # 作成中
    CONFIRMED = "confirmed"      # 確定
    PAID = "paid"                # 支払い済み
    SHIPPED = "shipped"          # 発送済み
    DELIVERED = "delivered"      # 配達完了
    CANCELLED = "cancelled"      # キャンセル
```

#### CustomerId
```python
@dataclass(frozen=True)
class CustomerId:
    value: UUID
```

### Domain Events（ドメインイベント）

```python
@dataclass
class OrderCreatedEvent:
    order_id: OrderId
    occurred_at: datetime = field(default_factory=datetime.now)

@dataclass
class OrderConfirmedEvent:
    order_id: OrderId
    total_amount: Money
    occurred_at: datetime = field(default_factory=datetime.now)

@dataclass
class OrderCancelledEvent:
    order_id: OrderId
    occurred_at: datetime = field(default_factory=datetime.now)
```

### Domain Services

#### PricingService（価格計算サービス）
```python
class PricingService:
    def calculate_with_discount(
        self,
        order: Order,
        discount_code: str | None = None,
    ) -> Money:
        """割引適用後の価格を計算"""
        total = order.calculate_total()

        if discount_code:
            discount = self._get_discount(discount_code)
            total = total.subtract(discount.calculate(total))

        return total
```

### リポジトリ

```python
class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: OrderId) -> Order | None:
        pass

    @abstractmethod
    def find_by_customer(self, customer_id: CustomerId) -> list[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def next_id(self) -> OrderId:
        pass
```

### ユースケース

#### CreateOrderUseCase（注文作成）
```python
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

#### AddItemToOrderUseCase（商品追加）
```python
@dataclass
class AddItemToOrderCommand:
    order_id: str
    product_id: str
    quantity: int

class AddItemToOrderUseCase:
    def __init__(
        self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo

    def execute(self, command: AddItemToOrderCommand) -> None:
        # 注文を取得
        order_id = OrderId(UUID(command.order_id))
        order = self.order_repo.find_by_id(order_id)
        if not order:
            raise OrderNotFoundError()

        # 商品を取得
        product_id = ProductId(UUID(command.product_id))
        product = self.product_repo.find_by_id(product_id)
        if not product:
            raise ProductNotFoundError()

        # 在庫確認
        if not product.is_available():
            raise ProductNotAvailableError()

        # 商品を追加
        order.add_item(product_id, command.quantity, product.price)

        # 在庫を減らす
        product.reduce_stock(command.quantity)

        # 保存
        self.order_repo.save(order)
        self.product_repo.save(product)
```

---

## 3. Payment Context（決済）

### 概要
決済処理と外部決済サービス連携を扱う。
**外部連携が複雑**なため、ヘキサゴナルアーキテクチャで実装。

### エンティティ

#### Payment（決済）
```python
@dataclass
class Payment:
    id: PaymentId
    order_id: OrderId
    amount: Money
    status: PaymentStatus
    payment_method: PaymentMethod
    processed_at: datetime | None = None

    def process(self, gateway: PaymentGateway) -> None:
        """決済を実行"""
        if self.status != PaymentStatus.PENDING:
            raise PaymentAlreadyProcessedError()

        result = gateway.charge(self.amount, self.payment_method)

        if result.is_success:
            self.status = PaymentStatus.SUCCESS
            self.processed_at = datetime.now()
        else:
            self.status = PaymentStatus.FAILED
```

### Value Objects

#### PaymentStatus
```python
class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"
```

#### PaymentMethod
```python
class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    DIGITAL_WALLET = "digital_wallet"
```

### Ports（ポート）

#### PaymentGateway（決済ゲートウェイ）
```python
class PaymentGateway(ABC):
    """決済処理の抽象インターフェース（Port）"""

    @abstractmethod
    def charge(self, amount: Money, method: PaymentMethod) -> PaymentResult:
        pass

    @abstractmethod
    def refund(self, payment_id: PaymentId) -> PaymentResult:
        pass
```

### Adapters（アダプター）

```python
class StripePaymentAdapter(PaymentGateway):
    """Stripe実装（Adapter）"""

    def charge(self, amount: Money, method: PaymentMethod) -> PaymentResult:
        # Stripe API呼び出し
        ...

class PayPalPaymentAdapter(PaymentGateway):
    """PayPal実装（Adapter）"""

    def charge(self, amount: Money, method: PaymentMethod) -> PaymentResult:
        # PayPal API呼び出し
        ...
```

---

## 4. Shipping Context（配送）

### 概要
配送手配と配送業者連携を扱う。
Payment Contextと同様にヘキサゴナルアーキテクチャで実装。

### エンティティ

#### Shipment（配送）
```python
@dataclass
class Shipment:
    id: ShipmentId
    order_id: OrderId
    address: Address
    status: ShipmentStatus
    tracking_number: str | None = None
    shipped_at: datetime | None = None
    delivered_at: datetime | None = None

    def ship(self, carrier: ShippingCarrier) -> None:
        """配送を開始"""
        if self.status != ShipmentStatus.PENDING:
            raise ShipmentAlreadyShippedError()

        tracking = carrier.create_shipment(self.address)
        self.tracking_number = tracking.number
        self.status = ShipmentStatus.SHIPPED
        self.shipped_at = datetime.now()
```

---

## Shared Kernel（共有カーネル）

全コンテキストで共有される基本的なValue Objectsです。

### Money（金額）
```python
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "JPY"

    def add(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def multiply(self, multiplier: Decimal) -> "Money":
        return Money(self.amount * multiplier, self.currency)

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError()
```

### Email
```python
@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self._is_valid(self.value):
            raise InvalidEmailError(self.value)

    @staticmethod
    def _is_valid(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))
```

### Address（住所）
```python
@dataclass(frozen=True)
class Address:
    postal_code: str
    prefecture: str
    city: str
    street: str
    building: str | None = None

    def full_address(self) -> str:
        parts = [self.postal_code, self.prefecture, self.city, self.street]
        if self.building:
            parts.append(self.building)
        return " ".join(parts)
```

---

## ドメインモデル図

```
[Catalog Context]
  Product ──has_many──> Category

[Order Context]
  Order (Aggregate Root)
    ├── OrderItem (Entity)
    ├── CustomerId (VO)
    └── OrderStatus (VO)

[Payment Context]
  Payment ──references──> Order
  Payment ──uses──> PaymentGateway (Port)

[Shipping Context]
  Shipment ──references──> Order
  Shipment ──uses──> ShippingCarrier (Port)

[Shared Kernel]
  Money, Email, Address
```

---

## まとめ

このドメインモデルは：

✅ **学習しやすい**: 誰でも理解できるECサイト
✅ **実践的**: 実際のビジネスロジックを含む
✅ **スケーラブル**: 複雑度に応じたアーキテクチャ選択
✅ **拡張可能**: 新しいコンテキスト追加が容易

次のステップ：
- 各コンテキストの実装例を`src/app/modules/`に配置
- テストコードで動作を保証
