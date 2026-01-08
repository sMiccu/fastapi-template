# クイックスタートガイド

このガイドでは、最短で開発を始める方法を説明します。

## 🚀 30秒でセットアップ

```bash
# 1. リポジトリをクローン
git clone https://github.com/your-org/fastapi-template.git
cd fastapi-template

# 2. ワンコマンドセットアップ
make setup

# 3. 開発サーバー起動
make dev
```

**それだけです！** ブラウザで http://localhost:8000/docs を開いてください。

---

## 📋 セットアップ方法の比較

### 🥇 推奨: Makeコマンド（最も簡単）

```bash
make setup    # 全自動セットアップ
```

**含まれる処理:**
- ✅ uvのインストールチェック
- ✅ 依存関係のインストール
- ✅ .envファイル作成（ランダムなSECRET_KEY）
- ✅ Docker起動（PostgreSQL + Redis）
- ✅ DBマイグレーション
- ✅ テスト実行

### 🥈 シェルスクリプト（詳細な出力が欲しい場合）

```bash
./scripts/setup.sh
```

**オプション:**
```bash
./scripts/setup.sh --prod         # 本番環境用
./scripts/setup.sh --skip-tests   # テストスキップ
./scripts/setup.sh --help         # ヘルプ表示
```

### 🥉 手動セットアップ（学習目的）

```bash
# 1. uvインストール
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# 2. 依存関係インストール
uv sync --all-extras

# 3. .env作成
make create-env

# 4. Docker起動
docker-compose up -d

# 5. マイグレーション
uv run alembic upgrade head

# 6. サーバー起動
uv run uvicorn app.main:app --reload
```

---

## 🔧 トラブルシューティング

### エラーが出た場合

```bash
# 自動修正を試す
./scripts/quick-fix.sh

# それでも解決しない場合は完全クリーンアップ
make clean-all
make setup
```

### よくある問題

#### 1. `uv: command not found`

```bash
# uvをインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# PATHを設定
export PATH="$HOME/.local/bin:$PATH"

# シェルを再起動するか、設定ファイルに追加
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc  # zshの場合
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc # bashの場合
```

#### 2. `Docker daemon is not running`

```bash
# Docker Desktopを起動してください
# macOS: アプリケーション → Docker を起動
```

#### 3. `Port 5432 already in use`

```bash
# 既存のPostgreSQLを停止
brew services stop postgresql  # Homebrewでインストールした場合

# またはポートを変更
# docker-compose.ymlで5432を別のポート（例: 5433）に変更
```

#### 4. マイグレーションエラー

```bash
# データベースをリセット
make db-reset

# または手動で
docker-compose down -v
docker-compose up -d
make db-upgrade
```

---

## 📖 よく使うコマンド

### 開発中

```bash
make dev          # サーバー起動
make test         # テスト実行
make lint-fix     # コード自動修正
make shell        # IPythonシェル
```

### DBマイグレーション

```bash
# 新しいマイグレーション作成
make db-migrate msg="add user table"

# マイグレーション適用
make db-upgrade

# 履歴確認
make db-history
```

### Docker管理

```bash
make up           # Docker起動
make down         # Docker停止
make restart      # Docker再起動
make logs         # ログ表示
```

### コード品質

```bash
make check        # 全チェック（lint + typecheck + test）
make fix          # 自動修正（lint + format）
make ci           # CI相当のチェック
```

### その他

```bash
make help         # 全コマンド表示
make info         # プロジェクト情報表示
make clean        # キャッシュ削除
make rebuild      # 完全再構築
```

---

## 🎯 次のステップ

1. **ドキュメントを読む**
   - [README.md](README.md) - 全体概要
   - [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - アーキテクチャ設計
   - [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - 詳細な開発ガイド

2. **コードを確認**
   - `src/app/modules/catalog/` - シンプルな例（レイヤード）
   - `src/app/modules/orders/` - 複雑な例（DDD）

3. **Swagger UIで試す**
   - http://localhost:8000/docs

4. **テストを実行**
   ```bash
   make test
   ```

5. **新機能を追加**
   - `docs/PATTERNS.md` で実装パターンを参照

---

## 🌟 開発環境 vs 本番環境

### 開発環境

```bash
# セットアップ
make setup

# サーバー起動（ホットリロード有効）
make dev

# 特徴
- DEBUG=true
- ホットリロード
- 開発用依存関係インストール
- pre-commitフック有効
```

### 本番環境

```bash
# セットアップ
make setup-prod

# サーバー起動（ワーカー4つ）
make prod

# または直接
ENVIRONMENT=production ./scripts/setup.sh --prod

# 特徴
- DEBUG=false
- 本番用依存関係のみ
- 複数ワーカー
- 最適化された設定
```

---

## 💡 プロのTips

### 1. エイリアスを設定

```bash
# ~/.zshrc または ~/.bashrcに追加
alias dev='make dev'
alias test='make test'
alias fix='make fix'
```

### 2. Git hooksを活用

```bash
# pre-commitフックのインストール
uv run pre-commit install

# これにより、コミット前に自動でlint/formatが実行される
```

### 3. Watch modeでテスト

```bash
# ファイル変更時に自動でテスト実行
make test-watch
```

### 4. IPythonで実験

```bash
make shell

# IPython内で
from app.modules.orders.domain.entities.order import Order
from app.shared.domain.value_objects.money import Money
# ... 実験的にコードを試せる
```

---

## 🆘 サポート

問題が解決しない場合：

1. [GitHub Issues](https://github.com/your-org/fastapi-template/issues) を確認
2. [ドキュメント](docs/) を読む
3. `make info` でプロジェクト状態を確認
4. 新しいIssueを作成

---

**Happy Coding! 🚀**
