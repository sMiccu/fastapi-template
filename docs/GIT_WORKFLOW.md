# Git ワークフロー

このドキュメントでは、プロジェクトのGitワークフローとコミット規約を説明します。

## 🚀 クイックスタート

### 簡単なコミット（推奨）

```bash
# 対話モードで入力
make commit

# または直接指定
make commit-feat msg="add user authentication"
make commit-fix msg="resolve N+1 query issue"
make commit-docs msg="update architecture guide"
```

### 自動実行される処理

コミット時に以下が自動で実行されます：

1. ✅ **コード品質チェック**
   - Lint（ruff）
   - Format（ruff）
   - Type check（mypy）

2. ✅ **テスト実行**
   - Unit tests

3. ✅ **ドキュメント整合性チェック**
   - pyproject.toml変更 → TECH_STACK.mdチェック
   - domain層変更 → ARCHITECTURE.mdチェック
   - モジュール追加 → DOMAIN_MODEL.mdチェック

4. ✅ **自動コミット＆プッシュ**
   - Conventional Commits形式
   - リモートへ自動プッシュ

## 📋 コミットタイプ

| タイプ | 説明 | コマンド |
|--------|------|----------|
| `feat` | 新機能 | `make commit-feat msg="..."` |
| `fix` | バグ修正 | `make commit-fix msg="..."` |
| `docs` | ドキュメント | `make commit-docs msg="..."` |
| `refactor` | リファクタリング | `make commit-refactor msg="..."` |
| `test` | テスト追加 | `make commit-test msg="..."` |
| `chore` | 雑務 | `make commit-quick msg="..."` |
| `style` | フォーマット | - |
| `perf` | パフォーマンス | - |
| `ci` | CI設定 | - |

## 🔧 コミットコマンド

### 基本的な使い方

```bash
# 1. 対話モードで作成（初心者向け）
make commit

# 2. タイプ別コマンド（よく使う）
make commit-feat msg="add payment feature"
make commit-fix msg="fix memory leak"
make commit-docs msg="update setup guide"

# 3. オプション付き
./scripts/auto-commit.sh feat "add feature" --scope orders --no-push
```

### オプション

```bash
--scope SCOPE      # スコープを指定（例: orders, catalog）
--no-push          # プッシュしない
--no-test          # テストをスキップ
--no-check         # 全チェックをスキップ
--breaking         # 破壊的変更マーク
```

### 例

```bash
# スコープ付き
./scripts/auto-commit.sh feat "add price calculation" --scope orders

# プッシュなし（後で手動）
make commit-feat msg="WIP feature" --no-push

# 破壊的変更
./scripts/auto-commit.sh feat "change API response format" --breaking

# クイックコミット（チェックスキップ）
make commit-quick msg="update README"
```

## 🎯 Conventional Commits

### フォーマット

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 例

```
feat: add user authentication
feat(orders): add order cancellation
fix: resolve N+1 query in product list
docs: update architecture guide
refactor(catalog): extract pricing logic
test: add tests for order confirmation
chore: update dependencies
```

### 破壊的変更

```
feat!: change API response format

BREAKING CHANGE: Response structure changed from array to object
```

## 📚 ドキュメント自動チェック

### コミット前チェック（pre-commit）

以下の変更があると警告が表示されます：

| 変更ファイル | 確認すべきドキュメント |
|-------------|---------------------|
| `pyproject.toml` | docs/TECH_STACK.md |
| `domain/` | docs/ARCHITECTURE.md, DOMAIN_MODEL.md |
| `modules/` | docs/DOMAIN_MODEL.md |
| `Makefile`, `docker-compose.yml` | docs/DEVELOPMENT.md |
| 新モジュール追加 | 全ドキュメント |

### コミット後通知（post-commit）

コミット後、関連ドキュメントの更新提案が表示されます：

```bash
📦 pyproject.tomlが変更されました
   docs/TECH_STACK.mdの更新を検討してください

💡 Tip: 以下のコマンドでドキュメントを簡単に更新できます:
   make doc-check    # ドキュメント整合性チェック
   cursor docs/      # Cursorでドキュメントを開く
```

## 🔄 ワークフロー例

### 通常の開発フロー

```bash
# 1. ブランチ作成
git checkout -b feature/add-payment

# 2. コード実装
# ... 開発 ...

# 3. 自動コミット（lint, test, 自動プッシュ）
make commit-feat msg="add payment processing"

# 4. プルリクエスト作成
# GitHubでPR作成
```

### ドキュメント更新フロー

```bash
# 1. 機能実装＆コミット
make commit-feat msg="add order cancellation"

# 2. post-commitフックから通知
📂 モジュールに変更がありました
   docs/DOMAIN_MODEL.mdの更新を検討してください

# 3. ドキュメント更新
cursor docs/DOMAIN_MODEL.md
# ... ドキュメント更新 ...

# 4. ドキュメントをコミット
make commit-docs msg="add order cancellation to domain model"
```

### 複数ファイル編集フロー

```bash
# 1. アーキテクチャ変更
# - domain層修正
# - infrastructure層修正
# - テスト追加

# 2. 自動チェックで確認
make check

# 3. コミット（自動でドキュメントチェック）
make commit-refactor msg="extract pricing logic to domain service"

# 4. 警告確認
⚠️  Warning: ドメイン層に変更がありますが、
   ドキュメントは更新されていません。

   必要に応じて以下を更新してください:
   - docs/ARCHITECTURE.md
   - docs/DOMAIN_MODEL.md

# 5. 必要に応じてドキュメント更新
cursor docs/ARCHITECTURE.md
make commit-docs msg="update architecture for new pricing service"
```

## 🛠️ Gitフック管理

### フックのインストール

```bash
# 自動（setup時）
make setup

# 手動
make hooks-install
```

### フックのアンインストール

```bash
make hooks-uninstall
```

### カスタムフック

インストールされるフック：

1. **post-commit**
   - ドキュメント更新の提案
   - 関連ファイル変更の通知

2. **pre-commit-doc-check**
   - ドキュメント整合性チェック
   - 型ヒントチェック（簡易）

## 💡 ベストプラクティス

### 1. 小さなコミット

```bash
# ✅ Good - 1機能ずつ
make commit-feat msg="add order validation"
make commit-test msg="add order validation tests"

# ❌ Bad - まとめすぎ
make commit-feat msg="add order feature"  # 何が入っているか不明
```

### 2. わかりやすいメッセージ

```bash
# ✅ Good
make commit-fix msg="resolve N+1 query in order list"
make commit-feat msg="add email notification for order confirmation"

# ❌ Bad
make commit-fix msg="fix bug"
make commit-feat msg="update"
```

### 3. ドキュメントの同時更新

```bash
# アーキテクチャ変更時
make commit-refactor msg="introduce repository pattern"
make commit-docs msg="update architecture guide for repository pattern"
```

### 4. スコープの活用

```bash
# モジュール単位でスコープを指定
make commit-feat msg="add price calculation" --scope orders
make commit-fix msg="fix stock validation" --scope catalog
```

## 🚨 トラブルシューティング

### コミットが失敗する

```bash
# 原因1: Lintエラー
make lint-fix  # 自動修正
make commit-feat msg="your message"

# 原因2: 型チェックエラー
make typecheck  # エラー確認
# ... 修正 ...
make commit-feat msg="your message"

# 原因3: テスト失敗
make test  # テスト確認
# ... 修正 ...
make commit-feat msg="your message"
```

### チェックをスキップしたい

```bash
# テストのみスキップ
./scripts/auto-commit.sh feat "your message" --no-test

# 全チェックスキップ（非推奨）
make commit-quick msg="emergency fix"
```

### プッシュしたくない

```bash
# プッシュなしでコミットのみ
./scripts/auto-commit.sh feat "your message" --no-push

# 後で手動プッシュ
git push origin your-branch
```

## 📊 コミット履歴の確認

```bash
# 最近のコミット
git log --oneline -10

# 綺麗なログ表示
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

# 特定の作者
git log --author="your-name" --oneline

# 統計
git shortlog -sn
```

## 🔗 関連リンク

- [Conventional Commits](https://www.conventionalcommits.org/)
- [セマンティックバージョニング](https://semver.org/lang/ja/)
- [Git Best Practices](https://git-scm.com/book/ja/v2)

## 📖 参考

プロジェクト固有のルール：

- [CONVENTIONS.md](CONVENTIONS.md) - コーディング規約
- [DEVELOPMENT.md](DEVELOPMENT.md) - 開発ガイド
- [ARCHITECTURE.md](ARCHITECTURE.md) - アーキテクチャ設計
