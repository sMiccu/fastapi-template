# プロジェクト全体概要

このドキュメントでは、このFastAPIテンプレートプロジェクトの全体像、各ファイルの役割、動作の仕組みを包括的に説明します。

---

## 📊 プロジェクト全体像

```
このプロジェクトは3つの大きな柱で構成されています：

┌─────────────────────────────────────────────────────┐
│  1. アプリケーション本体（src/app/）                │
│     - ビジネスロジック                              │
│     - API実装                                       │
│     - データベース連携                              │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│  2. 開発基盤（設定・ツール）                        │
│     - 自動化スクリプト                              │
│     - コード品質管理                                │
│     - 開発環境                                      │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│  3. ドキュメント（docs/）                           │
│     - 設計方針                                      │
│     - コーディング規約                              │
│     - 実装パターン                                  │
└─────────────────────────────────────────────────────┘
```

---

## 🏗️ アーキテクチャ全体図

### レイヤー構造

```
┌─────────────────────────────────────────────────────────┐
│                   HTTP Request                          │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Presentation Layer (presentation/api/)                 │
│  - FastAPI Router                                       │
│  - Pydanticスキーマ（バリデーション）                   │
│  - HTTPリクエスト/レスポンス変換                         │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Application Layer (application/use_cases/)             │
│  - ユースケース実行                                     │
│  - トランザクション制御                                 │
│  - DTO（Command/Query）                                │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Domain Layer (domain/)                                 │
│  - Entities（ビジネスルール）                          │
│  - Value Objects（不変な値）                           │
│  - Repository Interface（Port）                        │
│  - Domain Services                                      │
│  ★ 外部技術に依存しない★                               │
└─────────────────────────────────────────────────────────┘
                        ↑ (実装)
┌─────────────────────────────────────────────────────────┐
│  Infrastructure Layer (infrastructure/)                 │
│  - Repository実装（Adapter）                            │
│  - SQLAlchemyモデル                                     │
│  - 外部API連携                                          │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              Database (PostgreSQL)                      │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 ディレクトリ構造と役割

### ルートレベル

```
fastapi-template/
├── 📖 ドキュメント（使い方・設計）
│   ├── CHEATSHEET.md          ⭐ 日常的に見る（コマンド一覧）
│   ├── QUICKSTART.md          初回セットアップ
│   ├── CURSOR_GUIDE.md        Cursor AI活用法
│   ├── PROJECT_OVERVIEW.md    このファイル（全体像）
│   └── README.md              プロジェクト説明
│
├── 📚 詳細ドキュメント
│   └── docs/
│       ├── ARCHITECTURE.md    アーキテクチャ設計判断
│       ├── CONVENTIONS.md     コーディング規約
│       ├── DOMAIN_MODEL.md    ドメインモデル設計
│       ├── PATTERNS.md        実装パターン集
│       ├── GIT_WORKFLOW.md    Git/コミット規約
│       ├── DEVELOPMENT.md     開発詳細ガイド
│       ├── FOLDER_STRUCTURE.md フォルダ構造
│       └── TECH_STACK.md      技術スタック
│
├── ⚙️ 設定ファイル
│   ├── pyproject.toml         Python設定（依存関係、ruff、mypy）
│   ├── Makefile               タスクランナー（50+コマンド）
│   ├── Taskfile.yml           代替タスクランナー
│   ├── .cursorrules           Cursor AIルール
│   ├── .pre-commit-config.yaml pre-commitフック設定
│   └── alembic.ini            DBマイグレーション設定
│
├── 🐳 コンテナ関連
│   ├── docker-compose.yml     開発環境（PostgreSQL + Redis）
│   ├── Dockerfile             本番用イメージ
│   └── .devcontainer/         VSCode Dev Container設定
│
├── 🤖 CI/CD
│   └── .github/workflows/ci.yml GitHub Actions設定
│
├── 🛠️ スクリプト
│   └── scripts/
│       ├── setup.sh           インテリジェントセットアップ
│       ├── auto-commit.sh     自動コミット＆プッシュ
│       ├── quick-fix.sh       よくある問題の自動修正
│       └── hooks/             Git hooks
│
├── 💻 アプリケーション本体
│   └── src/app/
│
└── 🧪 テスト
    └── tests/
```

---

## 💻 アプリケーション本体（src/app/）

### 構造

```
src/app/
├── main.py                    📌 エントリーポイント
│
├── core/                      🔐 コア機能（全体で共有）
│   ├── config.py              環境変数・設定管理
│   ├── database.py            DB接続・セッション管理
│   ├── security.py            JWT認証・パスワードハッシュ
│   └── logging.py             構造化ログ設定
│
├── shared/                    🌐 共有コード
│   ├── exceptions.py          共通例外階層
│   └── domain/
│       └── value_objects/     全モジュールで使える値オブジェクト
│           ├── money.py       金額（通貨計算）
│           ├── email.py       メールアドレス
│           └── address.py     住所
│
├── modules/                   📦 機能モジュール（Bounded Context）
│   ├── catalog/              【シンプルな例】レイヤードアーキテクチャ
│   └── orders/               【複雑な例】DDDフル適用
│
└── api/                       🌐 API統合
    └── v1/
        └── router.py          全エンドポイント集約
```

---

## 🎯 2つのアーキテクチャパターン

このプロジェクトは**ハイブリッドアプローチ**を採用しています。

### パターン1: レイヤードアーキテクチャ（modules/catalog/）

**いつ使う？**
- シンプルなCRUD操作
- ビジネスロジックが薄い
- 例: 商品一覧、カテゴリ管理

**構造:**
```
modules/catalog/
├── router.py            # FastAPI routes（API層）
│   └── @router.get("/products")
│
├── schemas.py           # Pydanticモデル（バリデーション）
│   └── ProductResponse, ProductCreate
│
├── service.py           # ビジネスロジック層
│   └── ProductService.get_product()
│
├── repository.py        # データアクセス層（具象クラス）
│   └── ProductRepository.find_by_id()
│
├── models.py            # SQLAlchemyモデル
│   └── ProductModel (DBテーブル)
│
├── dependencies.py      # 依存性注入
│   └── get_product_service()
│
└── exceptions.py        # カタログ固有の例外
    └── ProductNotFoundException
```

**データの流れ:**
```
1. HTTP Request
     ↓
2. router.py（バリデーション）
     ↓
3. service.py（ビジネスロジック）
     ↓
4. repository.py（DB操作）
     ↓
5. models.py（SQLAlchemy）
     ↓
6. Database
```

**具体例:**
```python
# API呼び出し
GET /api/v1/products/{product_id}

# 処理の流れ
1. router.py:get_product()
   - リクエスト受信
   - product_id バリデーション

2. service.get_product(product_id)
   - ビジネスロジック実行（薄い）

3. repository.find_by_id(product_id)
   - SQLクエリ実行

4. ProductModel からデータ取得

5. ProductResponse に変換

6. JSON レスポンス返却
```

---

### パターン2: DDDフル適用（modules/orders/）

**いつ使う？**
- 複雑なビジネスルール
- 重要な状態遷移
- 外部連携が複数
- 例: 注文処理、決済

**構造:**
```
modules/orders/
├── domain/                        ドメイン層（ビジネスの核）
│   ├── entities/                  エンティティ
│   │   ├── order.py              Order（Aggregate Root）
│   │   └── order_item.py         OrderItem
│   │
│   ├── value_objects/            値オブジェクト
│   │   ├── order_id.py           OrderId（識別子）
│   │   ├── order_status.py       OrderStatus（状態）
│   │   ├── customer_id.py
│   │   └── product_id.py
│   │
│   ├── repositories/             リポジトリInterface（Port）
│   │   └── order_repository.py  「何が必要か」を定義
│   │
│   └── exceptions.py             ドメイン例外
│       └── EmptyOrderError, OrderAlreadyConfirmedError
│
├── application/                   アプリケーション層
│   ├── use_cases/                ユースケース
│   │   ├── create_order.py      注文作成
│   │   ├── add_item_to_order.py 商品追加
│   │   ├── confirm_order.py     注文確定
│   │   └── get_order.py         注文取得
│   │
│   └── dto/                      データ転送オブジェクト
│       └── commands.py           CreateOrderCommand等
│
├── infrastructure/               インフラ層（技術的詳細）
│   └── persistence/
│       ├── models.py             SQLAlchemyモデル
│       └── order_repository_impl.py  Repository実装（Adapter）
│
└── presentation/                 プレゼンテーション層
    ├── api/
    │   ├── router.py             FastAPI routes
    │   └── dependencies.py       DI設定
    │
    └── schemas/                  API用スキーマ
        ├── request.py            リクエストDTO
        └── response.py           レスポンスDTO
```

**データの流れ（DDDパターン）:**
```
1. HTTP Request
     ↓
2. presentation/api/router.py
   - CreateOrderRequest（Pydantic）でバリデーション
   - DTOに変換
     ↓
3. application/use_cases/create_order.py
   - CreateOrderCommand を受け取る
   - ビジネスフロー制御
     ↓
4. domain/entities/order.py
   - Order.create() でエンティティ生成
   - ビジネスルール実行（例: add_item()）
     ↓
5. domain/repositories/order_repository.py (Interface)
   - 「保存したい」という抽象的な要求
     ↓
6. infrastructure/persistence/order_repository_impl.py
   - 具体的な実装（SQLAlchemy使用）
   - Entity → Model 変換
     ↓
7. infrastructure/persistence/models.py
   - OrderModel（SQLAlchemyモデル）
     ↓
8. Database
```

**具体例:**
```python
# API呼び出し
POST /api/v1/orders/{order_id}/items
{
  "product_id": "uuid",
  "quantity": 2,
  "unit_price": 1000
}

# 処理の流れ（詳細）

1. presentation/api/router.py:add_item_to_order()
   リクエスト受信、AddItemRequest でバリデーション

2. AddItemToOrderCommand に変換
   {
     order_id: "uuid",
     product_id: "uuid",
     quantity: 2,
     unit_price: Decimal(1000),
     currency: "JPY"
   }

3. application/use_cases/add_item_to_order.py:execute()
   a. order_repository.find_by_id() で Order取得
   b. ProductId, Money を Value Object に変換
   c. order.add_item() を呼び出す ← ビジネスロジック

4. domain/entities/order.py:add_item()
   【ビジネスルール実行】
   - 状態チェック: status == PENDING?
   - 数量チェック: quantity > 0?
   - 失敗なら例外: OrderAlreadyConfirmedError
   - 成功なら: items に追加

5. order_repository.save(order) で永続化

6. infrastructure/persistence/order_repository_impl.py:save()
   a. Order Entity → OrderModel に変換
   b. session.add(model)
   c. session.commit()

7. Database に保存

8. HTTP 204 No Content レスポンス
```

---

## 🔑 重要な概念

### 1. ポート＆アダプターパターン

```
【Port（ポート）】= Interface（何が必要か）
domain/repositories/order_repository.py

class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: OrderId) -> Order | None:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass

↓ 実装

【Adapter（アダプター）】= 具体的な実装（どう実現するか）
infrastructure/persistence/order_repository_impl.py

class OrderRepositoryImpl(OrderRepository):
    def find_by_id(self, order_id: OrderId) -> Order | None:
        # SQLAlchemyで実装
        model = self.session.get(OrderModel, order_id.value)
        return self._to_entity(model)
```

**利点:**
- DB を PostgreSQL → MongoDB に変更しても、ドメイン層は影響なし
- テスト時にメモリリポジトリで代替可能
- ビジネスロジックが技術的詳細から隔離される

### 2. 依存性注入（DI）

```python
# dependencies.py
def get_db() -> Generator[Session, None, None]:
    """DBセッションを提供"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_order_repository(
    session: Annotated[Session, Depends(get_db)]
) -> OrderRepository:
    """Repository実装を提供"""
    return OrderRepositoryImpl(session)

def get_create_order_use_case(
    repo: Annotated[OrderRepository, Depends(get_order_repository)]
) -> CreateOrderUseCase:
    """Use Caseを提供"""
    return CreateOrderUseCase(repo)

# router.py
@router.post("/orders")
def create_order(
    request: CreateOrderRequest,
    use_case: Annotated[CreateOrderUseCase, Depends(get_create_order_use_case)]
):
    """FastAPIが自動でインジェクション"""
    command = CreateOrderCommand(...)
    order_id = use_case.execute(command)
    return {"order_id": str(order_id)}
```

**流れ:**
```
リクエスト
  ↓
FastAPIが依存関係を解決:
  1. get_db() → Session
  2. get_order_repository(Session) → OrderRepository
  3. get_create_order_use_case(OrderRepository) → CreateOrderUseCase
  ↓
create_order(use_case) が実行される
```

### 3. Entity と Value Object

#### Entity（エンティティ）
**特徴:** 識別子を持つ、可変、ライフサイクルがある

```python
# domain/entities/order.py
@dataclass
class Order:
    id: OrderId              # 識別子（同じIDなら同じOrder）
    customer_id: CustomerId
    status: OrderStatus      # 可変（状態が変わる）
    _items: list[OrderItem]

    def add_item(self, item: OrderItem) -> None:
        """ビジネスルールを含むメソッド"""
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedError()  # ビジネスルール
        self._items.append(item)

    def confirm(self) -> None:
        """状態遷移のビジネスルール"""
        if not self._items:
            raise EmptyOrderError()
        self.status = OrderStatus.CONFIRMED
```

#### Value Object（値オブジェクト）
**特徴:** 識別子なし、不変、値で比較

```python
# shared/domain/value_objects/money.py
@dataclass(frozen=True)  # 不変
class Money:
    amount: Decimal
    currency: str = "JPY"

    def add(self, other: Money) -> Money:
        """新しいMoneyインスタンスを返す（元は変更しない）"""
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

# 使用例
price1 = Money(Decimal(1000), "JPY")
price2 = Money(Decimal(1000), "JPY")
price1 == price2  # True（値が同じなら同じ）

# Entityとの違い
order1 = Order(id=OrderId(...))
order2 = Order(id=OrderId(...))  # 別のID
order1 == order2  # False（IDが違うので別物）
```

---

## ⚙️ 設定ファイル詳細

### pyproject.toml

**役割:** プロジェクトの中心的な設定ファイル

```toml
[project]
name = "fastapi-template"
version = "0.1.0"
dependencies = [
    "fastapi>=0.110.0",    # Webフレームワーク
    "sqlalchemy>=2.0.25",   # ORM
    # ... 本番依存関係
]

[project.optional-dependencies]
dev = [
    "ruff>=0.2.0",         # Linter/Formatter
    "mypy>=1.8.0",         # 型チェック
    "pytest>=8.0.0",       # テスト
    # ... 開発用依存関係
]

[tool.ruff]                # Linter設定
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B"]  # チェック項目

[tool.mypy]                # 型チェック設定
python_version = "3.12"
strict = true              # 厳格モード

[tool.pytest.ini_options]  # テスト設定
testpaths = ["tests"]
addopts = ["--cov=app"]    # カバレッジ測定
```

**使われる場面:**
- `uv sync` → dependencies をインストール
- `uv run ruff check .` → [tool.ruff] を参照
- `uv run mypy src/app` → [tool.mypy] を参照
- `uv run pytest` → [tool.pytest.ini_options] を参照

### Makefile

**役割:** 開発タスクの自動化

```makefile
# 主要なターゲット

setup: check-uv install-dev create-env docker-up wait-db db-upgrade
    # 複数のタスクを連鎖実行

dev:
    uv run uvicorn app.main:app --reload
    # 開発サーバー起動

test:
    uv run pytest
    # テスト実行

check: lint typecheck test
    # 複数のチェックを順次実行

commit:
    ./scripts/auto-commit.sh --interactive
    # スクリプトを呼び出す
```

**変数定義:**
```makefile
UV := uv
PYTHON := $(UV) run python
PYTEST := $(UV) run pytest

# $(PYTEST) と書くと uv run pytest に展開される
```

### .cursorrules

**役割:** Cursor AIが自動で読み込むルールファイル

```
コード生成時にAIが必ず従うルール:

1. アーキテクチャパターンの選択基準
   → シンプル or 複雑 で判断

2. コーディング規約
   → 型ヒント必須、命名規則等

3. ドメイン層のルール
   → ビジネスロジックはEntityに

4. Repository パターン
   → Interface（Port）と実装（Adapter）を分離

5. 禁止事項
   → グローバル変数禁止、循環依存禁止等
```

**動作:**
```
あなた: 「新しく決済機能を追加して」
         ↓
Cursor: 1. .cursorrules を読み込む
        2. docs/ARCHITECTURE.md を参照するよう指示される
        3. 複雑なビジネスロジックと判断
        4. DDDパターンを選択
        5. docs/PATTERNS.md のコード例に従う
        6. 型ヒントを全て付ける
        7. テストも一緒に生成
         ↓
結果: 一貫性のある高品質なコードが生成される
```

### docker-compose.yml

**役割:** 開発環境のサービスを定義

```yaml
services:
  postgres:
    image: postgres:16-alpine
    ports: ["5432:5432"]
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: fastapi_template
    volumes:
      - postgres_data:/var/lib/postgresql/data  # データ永続化
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    volumes:
      - redis_data:/data
```

**起動:**
```bash
docker-compose up -d

# 実行されること:
1. PostgreSQLコンテナ起動（ポート5432）
2. Redisコンテナ起動（ポート6379）
3. ヘルスチェック開始
4. データボリューム作成（永続化）
```

---

## 🛠️ スクリプト詳細

### scripts/setup.sh

**役割:** インテリジェントなセットアップスクリプト

```bash
処理フロー:

1. check_uv()
   - uvがインストール済みか確認
   - なければ自動インストール

2. check_docker()
   - Dockerが起動しているか確認
   - 停止していれば警告

3. install_dependencies()
   - uv sync (--all-extras)
   - pre-commit install

4. create_env_file()
   - .envファイルを作成
   - SECRET_KEY を自動生成（openssl rand）

5. start_docker()
   - docker-compose up -d
   - データベースの準備を30秒待つ

6. run_migrations()
   - alembic upgrade head
   - テーブル作成

7. run_tests()
   - pytest でテスト実行
   - 問題があれば早期検出

8. print_completion_message()
   - 完了メッセージ表示
   - 次のステップ案内
```

**実行:**
```bash
./scripts/setup.sh

# オプション
./scripts/setup.sh --prod         # 本番環境用
./scripts/setup.sh --skip-tests   # テストスキップ
```

### scripts/auto-commit.sh

**役割:** 自動コミット＆プッシュ

```bash
処理フロー:

1. check_changes()
   - git status で変更確認
   - 変更がなければ終了

2. run_checks()
   a. Lint
      - make lint でチェック
      - エラーあれば make lint-fix
      - 修正されたら自動で git add

   b. Format
      - make format でフォーマット
      - 修正されたら自動で git add

   c. Type check
      - make typecheck
      - エラーあれば終了（手動修正必要）

   d. Tests
      - make test-unit
      - 失敗すれば終了

3. generate_commit_message()
   - Conventional Commits形式に変換
   - 例: feat(orders): add cancellation

4. check_doc_updates()
   - 変更ファイルを分析
   - 関連ドキュメントの更新を提案
   - 例: pyproject.toml変更 → TECH_STACK.md更新提案

5. do_commit()
   - git add -A
   - git commit
   - pre-commitフック実行
   - ファイル修正されたら自動再試行（最大3回）

6. git push
   - origin/現在のブランチ へプッシュ

7. show_recent_commits()
   - 最近のコミット5件表示
```

**使用例:**
```bash
# 対話モード
make commit

# 直接指定
make commit-feat msg="add user auth"

# オプション付き
./scripts/auto-commit.sh feat "add feature" --scope orders --no-push
```

### scripts/hooks/pre-commit-doc-check

**役割:** コミット前のドキュメント整合性チェック

```bash
チェック内容:

1. pyproject.toml 変更
   → docs/TECH_STACK.md も更新すべきと警告

2. domain/ 層の変更
   → docs/ARCHITECTURE.md, DOMAIN_MODEL.md を確認すべきと警告

3. 新モジュール追加
   → 全ドキュメントの更新を提案

4. 型ヒント不足（簡易チェック）
   → docs/CONVENTIONS.md を参照するよう警告
```

**実行タイミング:**
```
git commit
  ↓
pre-commit フック自動実行
  ↓
このスクリプトが実行される
  ↓
警告表示（コミットは継続）
```

### scripts/hooks/post-commit

**役割:** コミット後の通知

```bash
最新コミットで変更されたファイルを分析:

📦 pyproject.tomlが変更されました
   docs/TECH_STACK.mdの更新を検討してください

🏗️  アーキテクチャ層に変更がありました
   docs/ARCHITECTURE.mdの確認をお勧めします

💡 Tip: 以下のコマンドでドキュメントを更新できます:
   make doc-check
   cursor docs/
```

---

## 🔄 開発フローの具体例

### シナリオ: 「注文キャンセル機能を追加」

#### ステップ1: 設計判断

```bash
# Cursorで確認
「docs/ARCHITECTURE.mdを参照して、
注文キャンセル機能はどのパターンで実装すべきですか？」

Cursor:
「複雑なビジネスルール（キャンセル可能状態の判定等）があるため、
modules/orders/ のDDDパターンを使用すべきです。」
```

#### ステップ2: ドメイン層の実装

```python
# domain/entities/order.py に追加

def cancel(self) -> None:
    """注文をキャンセルする

    Business Rules:
    - 発送済み・配達済みはキャンセル不可
    """
    if self.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
        raise OrderCannotBeCancelledError(self.status.value)

    self.status = OrderStatus.CANCELLED

# domain/exceptions.py に追加
class OrderCannotBeCancelledError(OrderException):
    def __init__(self, status: str) -> None:
        super().__init__(f"Cannot cancel order with status: {status}")
```

#### ステップ3: Use Case実装

```python
# application/use_cases/cancel_order.py（新規作成）

@dataclass(frozen=True)
class CancelOrderCommand:
    order_id: str

class CancelOrderUseCase:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    def execute(self, command: CancelOrderCommand) -> None:
        # 1. 注文取得
        order_id = OrderId(UUID(command.order_id))
        order = self.order_repo.find_by_id(order_id)
        if not order:
            raise OrderNotFoundException(command.order_id)

        # 2. ビジネスロジック実行（Entity内）
        order.cancel()

        # 3. 永続化
        self.order_repo.save(order)
```

#### ステップ4: API実装

```python
# presentation/api/router.py に追加

@router.post("/{order_id}/cancel", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(
    order_id: str,
    use_case: Annotated[CancelOrderUseCase, Depends(get_cancel_order_use_case)]
) -> None:
    try:
        command = CancelOrderCommand(order_id=order_id)
        use_case.execute(command)
    except OrderNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except OrderException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
```

#### ステップ5: テスト作成

```python
# tests/unit/test_order.py に追加

def test_cancel_order_success():
    order = Order.create(customer_id)
    order.add_item(product_id, 1, Money(Decimal(1000)))

    order.cancel()

    assert order.status == OrderStatus.CANCELLED

def test_cancel_shipped_order_raises_error():
    order = Order.create(customer_id)
    order.add_item(product_id, 1, Money(Decimal(1000)))
    order.confirm()
    order.status = OrderStatus.SHIPPED  # 発送済みに

    with pytest.raises(OrderCannotBeCancelledError):
        order.cancel()
```

#### ステップ6: コミット

```bash
# 自動で全チェック実行してコミット
make commit-feat msg="add order cancellation"

# 実行される処理:
1. ✅ Lint（ruff）
2. ✅ Format（ruff）
3. ✅ Type check（mypy）
4. ✅ Tests（pytest）
5. ✅ Pre-commit hooks
6. ⚠️  ドキュメント整合性チェック:
   「ドメイン層に変更があります
    docs/DOMAIN_MODEL.mdの更新を検討してください」
7. ✅ Git commit
8. ✅ Git push
```

#### ステップ7: ドキュメント更新

```bash
# ドキュメントを更新
cursor docs/DOMAIN_MODEL.md

# 追記内容:
「## Order Context

### cancel() メソッド
注文をキャンセルする機能。
ビジネスルール:
- 発送済み・配達済みはキャンセル不可
- ...」

# ドキュメントをコミット
make commit-docs msg="document order cancellation feature"
```

#### ステップ8: PR作成

```bash
# GitHubでPR作成
# CIが自動実行:
✅ Lint and Format Check
✅ Type Check
✅ Test
✅ Build

# レビュー・マージ
```

---

## 🔧 各ツールの役割

### uv（パッケージマネージャー）

```bash
# 依存関係のインストール
uv sync                    # 本番依存関係のみ
uv sync --all-extras       # 開発依存関係も含む

# コマンド実行
uv run python              # venv内のPythonを実行
uv run pytest              # venv内のpytestを実行
uv run uvicorn app.main:app # FastAPI起動

# 依存関係管理
uv add fastapi             # 依存関係追加
uv remove some-package     # 削除
uv sync --upgrade          # 全て更新
```

**なぜuv？**
- pip/poetryより10-100倍高速
- lockファイル自動生成
- モダンでシンプル

### ruff（Linter/Formatter）

```bash
# Lint（コードチェック）
uv run ruff check .           # チェックのみ
uv run ruff check --fix .     # 自動修正

# Format（整形）
uv run ruff format .          # フォーマット適用
uv run ruff format --check .  # チェックのみ

# チェック項目例:
- 未使用のimport
- インポート順序
- 命名規則違反
- セキュリティ問題
- 複雑度
```

**設定:** `pyproject.toml` の `[tool.ruff]`

### mypy（型チェック）

```bash
uv run mypy src/app

# チェック内容:
- 型ヒント不足
- 型の不一致
- 未定義変数
- 戻り値の型違反
```

**設定:** `pyproject.toml` の `[tool.mypy]`

```toml
[tool.mypy]
strict = true              # 厳格モード
disallow_untyped_defs = true  # 型ヒント必須
```

### pytest（テスト）

```bash
# 実行
uv run pytest                    # 全テスト
uv run pytest tests/unit/        # 単体テストのみ
uv run pytest --cov=app          # カバレッジ付き
uv run pytest -v                 # 詳細表示
uv run pytest -k test_order      # 特定のテストのみ

# マーカー
uv run pytest -m unit            # @pytest.mark.unit
uv run pytest -m e2e             # @pytest.mark.e2e
```

**設定:** `pyproject.toml` の `[tool.pytest.ini_options]`

### Alembic（DBマイグレーション）

```bash
# マイグレーション作成
uv run alembic revision --autogenerate -m "create users table"

# 処理:
1. 現在のDBスキーマを読み取る
2. models.py のSQLAlchemyモデルを読み取る
3. 差分を検出
4. alembic/versions/xxxxx_create_users_table.py を生成

# マイグレーション適用
uv run alembic upgrade head

# 処理:
1. 未適用のマイグレーションを検出
2. upgrade() 関数を順次実行
3. alembic_version テーブルに記録

# ロールバック
uv run alembic downgrade -1  # 1つ前に戻す
```

**設定:** `alembic.ini`, `alembic/env.py`

---

## 🔄 実際の処理フロー（具体例）

### 例1: APIリクエストの処理

```
【リクエスト】
POST /api/v1/orders
{
  "customer_id": "550e8400-e29b-41d4-a716-446655440000"
}

【処理フロー】

1. FastAPI（main.py）
   - リクエスト受信
   - CORS チェック
   - api/v1/router.py へルーティング

2. api/v1/router.py
   - orders router へ委譲

3. modules/orders/presentation/api/router.py:create_order()
   - CreateOrderRequest でバリデーション（Pydantic）
   - customer_id が UUID形式か自動チェック
   - Depends(get_create_order_use_case) で依存性注入

4. 依存性注入（自動）
   get_create_order_use_case()
     → get_order_repository()
       → get_db()
         → Session生成
       → OrderRepositoryImpl(session)
     → CreateOrderUseCase(repository)

5. CreateOrderUseCase.execute()
   - CreateOrderCommand に変換
   - Order.create(customer_id) でエンティティ生成
   - order_repository.save(order) で保存

6. OrderRepositoryImpl.save()
   - Order Entity → OrderModel（SQLAlchemy）に変換
   - session.add(model)
   - session.commit()

7. PostgreSQL
   - INSERT INTO orders (...) VALUES (...)
   - トランザクションコミット

8. レスポンス
   - {"order_id": "550e8400..."}
   - HTTP 201 Created

【所要時間】: 約10-50ms
```

### 例2: 開発者のコミット作業

```
【状況】新機能を実装した

1. 開発者
   $ make commit-feat msg="add payment feature"

2. scripts/auto-commit.sh 実行開始

3. 変更ファイル確認
   📊 変更されたファイル:
   M  src/app/modules/payments/...
   A  tests/unit/test_payment.py

4. コード品質チェック
   a. Lint実行
      → エラー検出（未使用import）
      → 自動修正
      → git add（自動）

   b. Format実行
      → インデント修正
      → git add（自動）

   c. Type check
      → Success: no issues found

   d. Tests
      → 20 passed

5. ドキュメント整合性チェック
   ⚠️  モジュールに変更があります
      docs/DOMAIN_MODEL.mdの更新を検討してください

6. Git commit
   試行1: git commit
   → pre-commit実行
   → ruff がインポート順序修正
   → ファイル変更検出

   試行2: git add & git commit --no-verify
   → 成功！

7. Git push
   → origin/main へプッシュ

8. GitHub Actions CI 自動起動
   - Lint and Format Check ✅
   - Type Check ✅
   - Test ✅
   - Build ✅

9. 完了通知
   🎉 全ての処理が完了しました！

   📋 最近のコミット:
   abc1234 feat: add payment feature

【所要時間】: 約30-60秒（テスト含む）
```

---

## 🎓 DDDの実践例

### Aggregate（集約）

```python
# Order = Aggregate Root（集約ルート）
# OrderItem = 集約内のEntity

class Order:  # Aggregate Root
    id: OrderId
    _items: list[OrderItem]  # 外部から直接触れない

    def add_item(self, item: OrderItem) -> None:
        """集約の境界を守る"""
        # ビジネスルール: 確定済みは追加不可
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedError()
        self._items.append(item)

    @property
    def items(self) -> list[OrderItem]:
        """読み取り専用で公開"""
        return self._items.copy()  # コピーを返す

# ❌ Bad: 集約の境界を破る
order.items.append(item)  # 直接操作はできない

# ✅ Good: メソッド経由
order.add_item(item)  # ビジネスルールがチェックされる
```

**なぜ重要？**
- 整合性を保証（ビジネスルール違反を防ぐ）
- トランザクション境界が明確
- テストしやすい

### Bounded Context（境界付けられたコンテキスト）

```
【Catalog Context】
商品の管理、在庫確認
→ modules/catalog/

【Order Context】
注文処理、状態管理
→ modules/orders/

【未実装だが追加可能】
- Payment Context（決済）
- Shipping Context（配送）
- Customer Context（顧客管理）

各コンテキストは独立:
- 独自のドメインモデル
- 独自のデータベーステーブル
- 独自のAPI
- コンテキスト間は明確なインターフェースで連携
```

---

## 🔍 デバッグ方法

### ログの見方

```python
# src/app/core/logging.py で設定

from app.core.logging import get_logger
logger = get_logger(__name__)

# ログ出力
logger.info(
    "order_created",
    order_id=str(order.id),
    customer_id=str(order.customer_id),
    total=float(order.calculate_total().amount)
)

# 出力（JSON形式）
{
  "event": "order_created",
  "order_id": "550e8400-...",
  "customer_id": "660e8400-...",
  "total": 2500.0,
  "timestamp": "2026-01-09T14:30:00Z",
  "logger": "app.modules.orders.application.use_cases.create_order"
}
```

### ブレークポイント

```python
# コード内に追加
def create_order(command: CreateOrderCommand) -> OrderId:
    customer_id = CustomerId(UUID(command.customer_id))

    breakpoint()  # ← ここで停止

    order = Order.create(customer_id)
    return order.id

# デバッガーが起動（IPython/pdb）
```

### IPythonでの検証

```bash
make shell

# IPython起動
from app.modules.orders.domain.entities.order import Order
from app.shared.domain.value_objects.money import Money
from decimal import Decimal
from uuid import uuid4

# インタラクティブに試す
order = Order.create(CustomerId(uuid4()))
order.add_item(ProductId(uuid4()), 2, Money(Decimal(1000)))
order.calculate_total()
# → Money(amount=Decimal('2000'), currency='JPY')
```

---

## 📊 データベースの仕組み

### SQLAlchemyモデル vs ドメインエンティティ

```python
【SQLAlchemyモデル】（infrastructure層）
技術的な詳細、DB構造に密結合

class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String(50), nullable=False)
    items = relationship("OrderItemModel")  # リレーション

【ドメインエンティティ】（domain層）
ビジネスロジック、DB構造とは無関係

@dataclass
class Order:
    id: OrderId
    customer_id: CustomerId
    status: OrderStatus
    _items: list[OrderItem]

    def add_item(self, item: OrderItem) -> None:
        # ビジネスルール
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedError()
        self._items.append(item)

【変換】（Repository実装）

class OrderRepositoryImpl:
    def _to_entity(self, model: OrderModel) -> Order:
        """ORM → Entity"""
        return Order(
            id=OrderId(model.id),
            customer_id=CustomerId(model.customer_id),
            status=OrderStatus(model.status),
        )

    def _to_model(self, entity: Order) -> OrderModel:
        """Entity → ORM"""
        return OrderModel(
            id=entity.id.value,
            customer_id=entity.customer_id.value,
            status=entity.status.value,
        )
```

**なぜ分離？**
- ドメイン層はDB構造変更の影響を受けない
- テスト時にDBなしでビジネスロジックをテスト可能
- ORMをMongoDBに変更してもドメイン層は不変

### マイグレーションの流れ

```bash
# 1. モデル定義
class ProductModel(Base):
    __tablename__ = "products"
    id: Mapped[UUID] = ...
    name: Mapped[str] = ...

# 2. マイグレーション生成
make db-migrate msg="add products table"

# 実行内容:
- alembic/env.py が Base.metadata を読み取る
- 現在のDBと比較
- 差分から upgrade()/downgrade() を生成

# 3. 生成されたファイル
alembic/versions/xxxxx_add_products_table.py

def upgrade() -> None:
    op.create_table('products',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('products')

# 4. 適用
make db-upgrade

# 実行内容:
- upgrade() 関数を実行
- CREATE TABLE products ...
- alembic_version テーブルに記録
```

---

## 🎯 実践的なTips

### Tip1: 新モジュールの追加

```bash
# シンプルな機能の場合
cp -r src/app/modules/catalog src/app/modules/reviews
# → catalog/ をベースに編集

# 複雑な機能の場合
cp -r src/app/modules/orders src/app/modules/payments
# → orders/ をベースに編集
```

### Tip2: Cursorでの効率的な開発

```
# プロンプト例

「docs/ARCHITECTURE.mdとdocs/PATTERNS.mdを参照して、
modules/orders/と同じ構造で新しいpaymentsモジュールを作成してください。

要件:
- Payment エンティティ
- PaymentGateway ポート
- Stripe/PayPal アダプター
- Use Cases: ProcessPayment, RefundPayment
- テストも一緒に生成」

→ Cursorが一貫性のあるコードを生成
```

### Tip3: トラブルシューティング

```bash
# パターン1: テストが失敗
make test
# → エラーメッセージ確認
# → 該当箇所修正
make test

# パターン2: 型チェックエラー
make typecheck
# → エラー箇所修正
# → 型ヒント追加
make typecheck

# パターン3: DBエラー
make db-reset     # DB完全リセット
make db-upgrade   # マイグレーション再適用

# パターン4: 全てリセット
make clean-all    # 完全削除
make setup        # 最初から
```

---

## 📚 ドキュメントの使い分け

| 状況 | 見るドキュメント | 理由 |
|------|----------------|------|
| **毎日** | CHEATSHEET.md | コマンドをすぐ確認 |
| 初回セットアップ | QUICKSTART.md | 30秒で始める |
| AI活用したい | CURSOR_GUIDE.md | 効率的なプロンプト |
| 新機能追加 | docs/ARCHITECTURE.md | パターン判断 |
| コードの書き方 | docs/PATTERNS.md | 実装例 |
| 命名規則 | docs/CONVENTIONS.md | 規約確認 |
| コミット方法 | docs/GIT_WORKFLOW.md | 詳細な手順 |
| プロジェクト全体 | PROJECT_OVERVIEW.md | このファイル |

---

## 🚀 開発サイクル（1日の流れ）

```
【朝】
$ make dev
→ サーバー起動（http://localhost:8000）

【午前】機能実装
Cursor で開発
→ 「docs/ARCHITECTURE.mdを参照して〇〇機能を実装」
→ AIが自動でパターン選択＆コード生成

【昼前】コミット
$ make commit
→ Lint/Test/Commit/Push 全自動
→ GitHub Actions CI 自動実行

【午後】レビュー指摘対応
$ make fix              # 自動修正
$ make test             # テスト確認
$ make commit-fix msg="address review comments"

【夕方】ドキュメント更新
$ cursor docs/DOMAIN_MODEL.md
$ make commit-docs msg="update domain model"

【終業】
$ make down             # Docker停止
```

---

## 💡 なぜこのアーキテクチャ？

### 問題: 従来のMVCアーキテクチャ

```python
# ❌ ビジネスロジックがController/Serviceに散在
class OrderService:
    def create_order(self, customer_id, items):
        # ビジネスルール1: 空注文チェック
        if not items:
            raise Exception("Empty order")

        # ビジネスルール2: 在庫チェック
        for item in items:
            if not self.check_stock(item):
                raise Exception("Out of stock")

        # ビジネスルール3: 価格計算
        total = sum(item.price * item.qty for item in items)

        # DB保存
        order = OrderModel(customer_id=customer_id, total=total)
        db.session.add(order)
        db.session.commit()

# 問題点:
- ビジネスルールがServiceに散在
- テストしにくい（DBモック必要）
- DB構造変更でビジネスロジックも影響
```

### 解決: DDDアーキテクチャ

```python
# ✅ ビジネスルールはEntityに集約
class Order:  # ドメイン層
    def add_item(self, item: OrderItem) -> None:
        """ビジネスルール: 確定済みは追加不可"""
        if self.status != OrderStatus.PENDING:
            raise OrderAlreadyConfirmedError()
        self._items.append(item)

    def confirm(self) -> None:
        """ビジネスルール: 空注文は確定不可"""
        if not self._items:
            raise EmptyOrderError()
        self.status = OrderStatus.CONFIRMED

    def calculate_total(self) -> Money:
        """ビジネスルール: 合計金額計算"""
        total = Money(Decimal(0))
        for item in self._items:
            total = total.add(item.subtotal())
        return total

# Use Caseはフロー制御のみ
class CreateOrderUseCase:  # アプリケーション層
    def execute(self, command: CreateOrderCommand) -> OrderId:
        order = Order.create(customer_id)  # Entity生成
        self.repository.save(order)        # 永続化
        return order.id

# 利点:
- ビジネスルールが1箇所に集約
- DBなしでテスト可能: order = Order.create(...); order.add_item(...)
- DB構造変更の影響なし
```

---

## 🔐 セキュリティの仕組み

### JWT認証

```python
# core/security.py

# 1. パスワードハッシュ化
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)  # bcrypt

# 保存: "password123" → "$2b$12$..."

# 2. パスワード検証
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# 3. JWTトークン生成
def create_access_token(data: dict) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.now() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# 使用例
@router.post("/login")
def login(credentials: LoginRequest):
    # 1. ユーザー取得
    user = get_user(credentials.email)

    # 2. パスワード検証
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    # 3. トークン生成
    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}

# 保護されたエンドポイント
@router.get("/protected")
def protected(token: str = Depends(verify_token)):
    return {"message": "You are authenticated"}
```

---

## 🧪 テスト戦略

### テストピラミッド

```
      /\       E2E Tests（少数、遅い）
     /  \      - API全体のテスト
    /────\     - 実際のHTTPリクエスト
   /      \
  /────────\   Integration Tests（中程度）
 /          \  - Repository実装のテスト
/────────────\ - DB接続あり
              \
Unit Tests（多数、高速）
- ドメインロジックのテスト
- 外部依存なし
```

### 具体例

```python
# Unit Test（ドメイン層）- 高速
def test_order_add_item():
    # Arrange
    order = Order.create(customer_id)
    item = OrderItem(product_id, 2, Money(Decimal(1000)))

    # Act
    order.add_item(item)

    # Assert
    assert len(order.items) == 1
    assert order.calculate_total() == Money(Decimal(2000))

# 特徴:
- DBなし
- 外部依存なし
- 高速（0.01秒）
- ビジネスロジックのみテスト

# Integration Test（インフラ層）- 中速
def test_order_repository_save(db_session):
    # Arrange
    repo = OrderRepositoryImpl(db_session)
    order = Order.create(customer_id)

    # Act
    repo.save(order)
    found = repo.find_by_id(order.id)

    # Assert
    assert found.id == order.id

# 特徴:
- SQLite（in-memory）使用
- Repository実装をテスト
- 中速（0.1秒）

# E2E Test（API全体）- 低速
def test_create_order_api(client):
    # Act
    response = client.post("/api/v1/orders", json={
        "customer_id": str(customer_id)
    })

    # Assert
    assert response.status_code == 201
    assert "order_id" in response.json()

# 特徴:
- HTTPリクエスト
- 全レイヤー通過
- 低速（0.5秒）
- 実際のAPIをテスト
```

---

## 🎓 まとめ

### このプロジェクトの強み

1. **段階的な複雑度対応**
   - シンプル → catalog/（レイヤード）
   - 複雑 → orders/（DDD）

2. **完全な自動化**
   - セットアップ: `make setup`
   - コミット: `make commit`
   - デプロイ: GitHub Actions

3. **AI完全統合**
   - .cursorrules で品質担保
   - ドキュメント参照で一貫性

4. **長期保守性**
   - ビジネスロジック保護
   - 技術的詳細から隔離
   - 豊富なドキュメント

### 使い方のコツ

1. **まずCHEATSHEET.mdを見る**
2. **Cursorに「docs/参照して」と指示**
3. **make commit で自動化**
4. **テストを書く**
5. **小さくコミット**

---

**このプロジェクトで、高品質なバックエンドを効率的に開発できます！🚀**
