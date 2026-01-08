# プロジェクトコンテキスト

このファイルはCursorのAIがプロジェクトのコンテキストを理解するためのものです。

## プロジェクト構成

```
fastapi-template/
├── docs/                    # 📚 設計ドキュメント（最重要）
│   ├── ARCHITECTURE.md      # アーキテクチャ判断基準
│   ├── CONVENTIONS.md       # コーディング規約
│   ├── DOMAIN_MODEL.md      # ドメインモデル
│   └── PATTERNS.md          # 実装パターン
├── src/app/
│   ├── core/                # 共通基盤（config, database, security）
│   ├── shared/              # 共有Value Objects
│   ├── modules/             # 機能モジュール
│   │   ├── catalog/         # 📦 レイヤード例（シンプル）
│   │   └── orders/          # 🎯 DDD例（複雑）
│   └── main.py
└── tests/
```

## 重要なファイル

### 必ず参照すべきドキュメント

1. **docs/ARCHITECTURE.md**
   - いつレイヤードを使うか
   - いつDDDを使うか
   - 依存関係のルール

2. **docs/CONVENTIONS.md**
   - 命名規則
   - 型ヒントのルール
   - docstringの書き方

3. **docs/PATTERNS.md**
   - Entity実装パターン
   - Repository実装パターン
   - Use Case実装パターン

### 参考実装

- **シンプルな例**: `src/app/modules/catalog/`
- **複雑な例**: `src/app/modules/orders/`

## 実装時のチェックリスト

新しいコードを書く際は以下を確認：

- [ ] 適切なアーキテクチャパターンを選択したか？
- [ ] 全ての関数に型ヒントがあるか？
- [ ] ビジネスロジックはドメイン層にあるか？
- [ ] テストを書いたか？
- [ ] `docs/CONVENTIONS.md`に従っているか？

## データベース

- **ORM**: SQLAlchemy 2.0（同期）
- **マイグレーション**: Alembic
- **テスト**: SQLite（in-memory）

## 技術スタック

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Redis
- uv (パッケージマネージャー)
- ruff (linter/formatter)
- mypy (型チェック)

## 開発コマンド

```bash
make dev          # サーバー起動
make test         # テスト
make check        # 全チェック
make fix          # 自動修正
```
