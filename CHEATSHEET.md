# FastAPI Template チートシート 🚀

**このファイル1つで全てがわかる！よく使うコマンドと使い方のまとめ**

---

## ⚡ 最初にやること（1回だけ）

```bash
# 1. セットアップ（これだけ！）
make setup

# 2. サーバー起動確認
make dev

# 3. ブラウザで確認
open http://localhost:8000/docs
```

---

## 📝 日常の開発コマンド

### サーバー起動・停止

```bash
make dev              # 開発サーバー起動
make restart          # Docker再起動
make down             # 全て停止
```

### コード編集後

```bash
make fix              # 自動修正（lint + format）
make test             # テスト実行
make check            # 全チェック（lint + type + test）
```

### コミット（これが一番簡単）

```bash
# 対話モードで選択
make commit

# または直接指定
make commit-feat msg="add user auth"      # 新機能
make commit-fix msg="fix N+1 query"       # バグ修正
make commit-docs msg="update readme"      # ドキュメント
```

**これで自動実行される:**
- ✅ コード修正（lint/format）
- ✅ テスト実行
- ✅ Git commit
- ✅ Git push
- ✅ ドキュメント整合性チェック

### データベース

```bash
make db-migrate msg="add user table"      # マイグレーション作成
make db-upgrade                           # マイグレーション適用
make db-reset                             # DBリセット（注意！）
```

---

## 🤖 Cursor AIの使い方

### コードを書いてもらう

```
あなた: 「docs/ARCHITECTURE.mdを参照して、
        新しく決済機能を追加してください」

Cursor: （自動でパターン選択して実装）
```

### よく使うプロンプト

```
# 新機能追加
「docs/PATTERNS.mdを参照して、〇〇機能を実装してください」

# バグ修正
「このN+1問題を、docs/CONVENTIONS.mdに従って修正してください」

# リファクタリング
「このコードをdocs/ARCHITECTURE.mdのルールに従ってリファクタリングしてください」

# テスト生成
「この関数のUnit Testを生成してください」
```

---

## 🏗️ 新機能の追加方法

### パターン1: シンプルな機能（CRUD中心）

```bash
# 例: カテゴリ管理機能

# 1. modules/catalog/ をコピー
cp -r src/app/modules/catalog src/app/modules/categories

# 2. Cursorで編集
cursor
# → 「catalog パターンに従ってcategories機能を実装」

# 3. コミット
make commit-feat msg="add categories management"
```

### パターン2: 複雑な機能（ビジネスロジックあり）

```bash
# 例: 決済機能

# Cursorに指示
「docs/ARCHITECTURE.mdを参照して、新しくpaymentsモジュールを作成してください。
- modules/orders/と同じDDDパターンを使用
- domain/entities/にPaymentエンティティ
- 外部決済APIとの連携はAdapterパターン」

# コミット
make commit-feat msg="add payment processing" --scope payments
```

---

## 📁 ファイル配置ルール

### シンプルなモジュール（レイヤード）

```
modules/catalog/
├── router.py         # API
├── schemas.py        # Pydantic
├── service.py        # ビジネスロジック
├── repository.py     # DB操作
└── models.py         # SQLAlchemy
```

**いつ使う？**
- 単純なCRUD
- ビジネスロジックが薄い
- 例: 商品一覧、カテゴリ管理

### 複雑なモジュール（DDD）

```
modules/orders/
├── domain/              # ビジネスルール
│   ├── entities/
│   ├── value_objects/
│   └── repositories/    # Interface
├── application/         # Use Cases
├── infrastructure/      # 実装
└── presentation/        # API
```

**いつ使う？**
- 複雑な状態遷移
- 重要なビジネスルール
- 外部連携が複数
- 例: 注文処理、決済

---

## 🔧 よくあるタスク

### 依存関係追加

```bash
# 1. pyproject.tomlに追加
vi pyproject.toml

# 2. インストール
uv sync

# 3. ドキュメント更新
cursor docs/TECH_STACK.md
make commit-docs msg="add new dependency"
```

### 環境変数追加

```bash
# 1. .envに追加
echo "NEW_CONFIG=value" >> .env

# 2. core/config.pyに追加
cursor src/app/core/config.py

# 3. 再起動
make restart
```

### Docker再構築

```bash
make clean-all        # 完全クリーンアップ
make setup            # 再セットアップ
```

---

## 🐛 トラブルシューティング

### サーバーが起動しない

```bash
make restart          # Docker再起動
make logs             # ログ確認
```

### テストが失敗する

```bash
make test             # エラー確認
make fix              # 自動修正試行
make test             # 再実行
```

### マイグレーションエラー

```bash
make db-reset         # DB完全リセット（注意！）
```

### 依存関係エラー

```bash
make clean            # キャッシュ削除
uv sync              # 再インストール
```

### 全てリセット

```bash
make clean-all        # 完全削除
make setup            # 最初から
```

---

## 📊 プロジェクト情報確認

```bash
make info             # 現在の状態表示
make help             # 全コマンド表示
make ps               # Dockerコンテナ確認
```

---

## 🎯 よくある質問

### Q: 新機能を追加したい

```bash
# 1. ブランチ作成
git checkout -b feature/new-feature

# 2. Cursorで実装
cursor
# → AIに指示「docs/ARCHITECTURE.mdを参照して...」

# 3. コミット（自動でlint/test/push）
make commit-feat msg="add new feature"

# 4. PR作成
# GitHubでPR作成
```

### Q: バグを修正したい

```bash
# 1. 修正
cursor

# 2. テスト
make test

# 3. コミット
make commit-fix msg="fix bug description"
```

### Q: ドキュメントを更新したい

```bash
# 1. 編集
cursor docs/

# 2. コミット（テストスキップ）
make commit-docs msg="update documentation"
```

### Q: 急いで直したい（チェックスキップ）

```bash
make commit-quick msg="emergency fix"
```

---

## 📖 詳しく知りたい時

| やりたいこと | 見るドキュメント |
|-------------|----------------|
| 最初のセットアップ | [QUICKSTART.md](QUICKSTART.md) |
| Cursor AIの使い方 | [CURSOR_GUIDE.md](CURSOR_GUIDE.md) |
| コミットの詳細 | [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md) |
| アーキテクチャ判断 | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| コード例 | [docs/PATTERNS.md](docs/PATTERNS.md) |
| コーディング規約 | [docs/CONVENTIONS.md](docs/CONVENTIONS.md) |
| 全体を知りたい | [README.md](README.md) |

---

## 🎓 開発の流れ（実例）

```bash
# 朝、PCを開いたら
make dev                                    # サーバー起動

# Cursorで新機能実装
cursor
# → 「新しく〇〇機能を追加」とAIに指示

# コミット（全自動）
make commit-feat msg="add awesome feature"

# ランチ休憩前
make down                                   # 停止

# 午後、再開
make dev                                    # 再起動

# バグ修正
make test                                   # テスト確認
# → 修正
make commit-fix msg="fix issue"

# 1日の終わり
make down                                   # 停止
```

---

## 💡 プロのTips

### 1. エイリアスを設定（オプション）

```bash
# ~/.zshrc または ~/.bashrc
alias dev='make dev'
alias test='make test'
alias commit='make commit'
alias fix='make fix'
```

### 2. Cursorは常にドキュメント参照

```
❌ 「注文機能を作って」
✅ 「docs/ARCHITECTURE.mdとdocs/PATTERNS.mdを参照して、注文機能を作って」
```

### 3. 小さくコミット

```bash
# ✅ Good
make commit-feat msg="add validation"
make commit-test msg="add validation tests"

# ❌ Bad
make commit-feat msg="add feature"  # 大きすぎ
```

---

## 🚀 このチートシートの使い方

1. **最初**: 上から順番に読む
2. **日常**: 「日常の開発コマンド」だけ見る
3. **困った時**: 「よくある質問」を見る
4. **詳細が知りたい**: 各ドキュメントへのリンクをたどる

---

## 📌 最重要コマンド（これだけ覚えればOK）

```bash
make setup              # 初回のみ
make dev                # サーバー起動
make commit             # コミット（対話モード）
make test               # テスト
make fix                # 自動修正
make help               # 困ったら
```

---

**このチートシートをブックマークして、いつでも参照してください！** 📚

質問があれば、`make help` で全コマンドを確認するか、
各ドキュメントを参照してください。

**Happy Coding! 🎉**
