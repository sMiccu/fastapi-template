# アーキテクチャ設計

## 基本方針

このテンプレートは、**ドメイン駆動設計（DDD）**を基盤とし、**ヘキサゴナルアーキテクチャ**のパターンを適用しています。

### 核となる原則

1. **依存性逆転の原則（DIP）**
   - ビジネスロジックは外部技術に依存しない
   - インフラ層がドメイン層に依存する（逆ではない）

2. **関心の分離**
   - ドメインロジック、アプリケーションロジック、インフラを明確に分離
   - 各層は明確な責務を持つ

3. **テスタビリティ**
   - ドメインロジックは外部依存なしでテスト可能
   - モック化が容易な設計

4. **柔軟性**
   - 外部技術（DB、フレームワーク）を交換可能
   - シンプルな部分は過度に複雑化しない

## アーキテクチャパターンの選択

### ハイブリッドアプローチ

プロジェクトの複雑度に応じて、最適なパターンを選択します。

```
┌────────────────────────────────────────────┐
│          アーキテクチャ選択フロー           │
└────────────────────────────────────────────┘

機能の複雑度を評価
    ↓
┌─────────────────┐
│ シンプルなCRUD? │
└─────────────────┘
    │
    ├─ Yes → レイヤードアーキテクチャ
    │         - Router → Service → Repository → Model
    │         - ビジネスロジックが薄い
    │         - 例: 商品カタログ、マスタ管理
    │
    └─ No  → 以下を確認
              ├─ 複雑なビジネスルール？
              ├─ 外部システム連携が複数？
              ├─ 技術変更の可能性？
              └─ 高いテスタビリティ要求？
                    ↓
                  Yes → DDDフル適用（ヘキサゴナル）
                        - Domain層を分離
                        - Use Case層を明示
                        - Repository = Interface
                        - 例: 注文処理、決済
```

## レイヤー構成

### 4層アーキテクチャ

```
┌─────────────────────────────────────────┐
│      Presentation Layer (API)           │  ← FastAPIルーター、スキーマ
│      - 外界との入出力                    │
│      - HTTPリクエスト/レスポンス         │
└─────────────────────────────────────────┘
              ↓ (依存)
┌─────────────────────────────────────────┐
│      Application Layer                   │  ← Use Cases、DTOs
│      - ユースケースの実行                │
│      - トランザクション制御              │
└─────────────────────────────────────────┘
              ↓ (依存)
┌─────────────────────────────────────────┐
│      Domain Layer                        │  ← Entities、Value Objects
│      - ビジネスルール                    │     Domain Services、Repository Interface
│      - ドメインモデル                    │
│      - ★外部依存なし★                   │
└─────────────────────────────────────────┘
              ↑ (実装)
┌─────────────────────────────────────────┐
│      Infrastructure Layer                │  ← Repository実装、DB Models
│      - 技術的詳細の実装                  │     外部API Adapter
│      - DB、外部サービス                  │
└─────────────────────────────────────────┘
```

### 各層の責務

#### 1. Domain Layer（ドメイン層）
**責務**: ビジネスルールの表現

- **Entities**: 識別子を持つオブジェクト
  ```python
  class Order:
      def __init__(self, id: OrderId, ...):
          self.id = id

      def add_item(self, item: OrderItem) -> None:
          """ビジネスルール: 在庫があれば追加"""
          if not item.is_in_stock():
              raise OutOfStockError()
          self.items.append(item)
  ```

- **Value Objects**: 不変な値
  ```python
  @dataclass(frozen=True)
  class Money:
      amount: Decimal
      currency: str = "JPY"

      def add(self, other: Money) -> Money:
          if self.currency != other.currency:
              raise CurrencyMismatchError()
          return Money(self.amount + other.amount, self.currency)
  ```

- **Domain Services**: エンティティに属さないビジネスロジック
  ```python
  class PricingService:
      def calculate_total(self, order: Order) -> Money:
          """価格計算のビジネスロジック"""
  ```

- **Repository Interface**: データ永続化の抽象
  ```python
  class OrderRepository(ABC):
      @abstractmethod
      def find_by_id(self, order_id: OrderId) -> Order | None:
          pass
  ```

#### 2. Application Layer（アプリケーション層）
**責務**: ユースケースの実行

- **Use Cases**: ビジネスユースケースの実装
  ```python
  class CreateOrderUseCase:
      def __init__(self, order_repo: OrderRepository):
          self.order_repo = order_repo

      def execute(self, command: CreateOrderCommand) -> OrderId:
          # 1. ドメインオブジェクト生成
          order = Order.create(...)

          # 2. ビジネスルール実行
          order.add_item(...)

          # 3. 永続化
          self.order_repo.save(order)

          return order.id
  ```

- **DTOs (Commands/Queries)**: データ転送オブジェクト
  ```python
  @dataclass
  class CreateOrderCommand:
      customer_id: str
      items: list[OrderItemData]
  ```

#### 3. Infrastructure Layer（インフラ層）
**責務**: 技術的詳細の実装

- **Repository実装**: データベースアクセス
  ```python
  class OrderRepositoryImpl(OrderRepository):
      def __init__(self, session: Session):
          self.session = session

      def find_by_id(self, order_id: OrderId) -> Order | None:
          # ORMモデル → ドメインエンティティ変換
          model = self.session.get(OrderModel, order_id.value)
          return self._to_entity(model) if model else None
  ```

- **External Adapters**: 外部サービス連携
  ```python
  class StripePaymentAdapter(PaymentGateway):
      def process_payment(self, amount: Money) -> PaymentResult:
          # Stripe API呼び出し
  ```

#### 4. Presentation Layer（プレゼンテーション層）
**責務**: 外界とのインターフェース

- **API Routes**: HTTPエンドポイント
  ```python
  @router.post("/orders")
  def create_order(
      request: CreateOrderRequest,
      use_case: CreateOrderUseCase = Depends(get_create_order_use_case)
  ):
      command = CreateOrderCommand(...)
      order_id = use_case.execute(command)
      return {"order_id": str(order_id)}
  ```

- **Schemas**: リクエスト/レスポンスの型定義
  ```python
  class CreateOrderRequest(BaseModel):
      customer_id: str
      items: list[OrderItemRequest]
  ```

## ポート&アダプターパターン

### ポート（Port）
**インターフェース**: ドメイン層が定義する契約

```python
# domain/repositories/order_repository.py
class OrderRepository(ABC):  # ← Port
    @abstractmethod
    def save(self, order: Order) -> None:
        pass
```

### アダプター（Adapter）
**実装**: インフラ層が提供する具体的な実装

```python
# infrastructure/persistence/order_repository_impl.py
class OrderRepositoryImpl(OrderRepository):  # ← Adapter
    def save(self, order: Order) -> None:
        # PostgreSQL実装
```

### 利点
- DBをPostgreSQLからMongoDBに変更しても、ドメイン層は影響なし
- テスト時はメモリリポジトリで代替可能

## 依存性注入（DI）

### FastAPIのDependsを活用

```python
# api/dependencies.py
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

# api/v1/endpoints/orders.py
@router.post("/orders")
def create_order(
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case)
):
    ...
```

## DDD戦略的設計

### Bounded Context（境界付けられたコンテキスト）

各コンテキストは独立したドメインモデルを持ちます。

```
┌──────────────────┐  ┌──────────────────┐
│ Catalog Context  │  │  Order Context   │
│                  │  │                  │
│ - Product        │  │ - Order          │
│ - Category       │  │ - OrderItem      │
└──────────────────┘  └──────────────────┘
         │                      │
         └──────────┬───────────┘
                    │
         ┌──────────▼───────────┐
         │  Payment Context     │
         │                      │
         │  - Payment           │
         │  - Transaction       │
         └──────────────────────┘
```

### Context Map（コンテキストマップ）

コンテキスト間の関係：

- **Shared Kernel**: 共有される基本的な概念（例: Money、Email）
- **Customer-Supplier**: 上流・下流関係
- **Anti-Corruption Layer**: 外部システムとの境界を守る層

## トランザクション管理

### Unit of Work パターン

```python
class UnitOfWork:
    def __init__(self, session: Session):
        self.session = session
        self.order_repo = OrderRepositoryImpl(session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()
```

## エラーハンドリング

### ドメイン例外

```python
# shared/exceptions.py
class DomainException(Exception):
    """ドメイン層の例外基底クラス"""
    pass

class BusinessRuleViolation(DomainException):
    """ビジネスルール違反"""
    pass

# modules/order/domain/exceptions.py
class OutOfStockError(BusinessRuleViolation):
    """在庫切れエラー"""
    pass
```

### 例外ハンドラー

```python
# main.py
@app.exception_handler(BusinessRuleViolation)
async def business_rule_violation_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

## テスト戦略

### テストピラミッド

```
        /\
       /  \      E2E Tests (少数)
      /────\     - API全体のテスト
     /      \
    /────────\   Integration Tests (中程度)
   /          \  - Repository実装のテスト
  /────────────\
 /              \ Unit Tests (多数)
/────────────────\ - ドメインロジックのテスト
                   - Use Caseのテスト
```

### 各層のテスト

```python
# Unit Test (ドメイン層)
def test_order_add_item():
    order = Order.create(...)
    item = OrderItem(...)
    order.add_item(item)
    assert len(order.items) == 1

# Integration Test (インフラ層)
def test_order_repository_save(db_session):
    repo = OrderRepositoryImpl(db_session)
    order = Order.create(...)
    repo.save(order)
    found = repo.find_by_id(order.id)
    assert found.id == order.id

# E2E Test (API)
def test_create_order_api(client):
    response = client.post("/api/v1/orders", json={...})
    assert response.status_code == 201
```

## パフォーマンス考慮事項

### N+1問題の回避
- Eager Loading（joinedload）の活用
- クエリ最適化

### キャッシング戦略
- Repository層でRedisキャッシュ
- ドメイン層は意識しない

### ページネーション
- Cursor-based pagination推奨（大量データ）

## まとめ

このアーキテクチャの目的：

✅ **ビジネスロジックの保護**: 技術的変更の影響を最小化
✅ **テスタビリティ**: 各層を独立してテスト可能
✅ **保守性**: 明確な責務分離
✅ **拡張性**: 新機能追加が容易
✅ **柔軟性**: 複雑度に応じた適切なパターン選択

参考文献：
- Eric Evans『ドメイン駆動設計』
- Vaughn Vernon『実践ドメイン駆動設計』
- Robert C. Martin『Clean Architecture』
