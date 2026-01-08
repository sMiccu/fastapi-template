# Cursor 開発ガイド

このガイドは、Cursor AIを最大限活用してこのプロジェクトで開発する方法を説明します。

## 🤖 Cursor が自動認識する設定

このプロジェクトには、Cursorが自動的に読み込む設定ファイルが含まれています：

### 1. `.cursorrules`（最重要）
Cursorがコード生成・レビュー時に**必ず従うルール**

**含まれる内容:**
- アーキテクチャパターンの選択基準
- コーディング規約
- 命名規則
- 禁止事項
- ドキュメントへの参照指示

### 2. `.cursor/context.md`
プロジェクトのコンテキスト情報

**含まれる内容:**
- プロジェクト構成
- 重要なファイル
- 技術スタック
- 実装時のチェックリスト

### 3. `.vscode/settings.json`
エディタ設定（Cursorと共有）

**含まれる内容:**
- Python設定
- Ruff（linter/formatter）設定
- フォーマット自動実行
- AI コンテキスト指定

## 💡 Cursor での開発フロー

### 1. 新機能追加

```
あなた: 「新しく商品レビュー機能を追加したい」

Cursor AI:
1. docs/ARCHITECTURE.mdを参照
2. 複雑度を判断（シンプル or 複雑）
3. 適切なパターンを選択
4. コード生成

あなた: 承認 → 実装

Cursor: テストコードも自動生成
```

**AIへの指示例:**
```
新しく商品レビュー機能を追加してください。
- modules/配下に新しいreviewsモジュールを作成
- DDDパターンを使用
- docs/ARCHITECTURE.mdとPATTERNS.mdを参照して実装
```

### 2. バグ修正

```
あなた: 「注文のN+1問題を修正したい」

Cursor AI:
1. 該当コードを特定
2. docs/CONVENTIONS.mdを参照
3. SQLAlchemy のEager Loadingを提案
4. 修正コード生成

あなた: 承認 → 修正
```

**AIへの指示例:**
```
orders モジュールでN+1問題が発生しています。
- repository実装を確認
- selectinloadを使用して修正
- docs/CONVENTIONS.mdの規約に従ってください
```

### 3. リファクタリング

```
あなた: 「価格計算ロジックをドメイン層に移動したい」

Cursor AI:
1. docs/ARCHITECTURE.mdを参照
2. ビジネスロジックはEntityに配置すべきと判断
3. リファクタリング案を提示
4. コード生成

あなた: 承認 → リファクタリング
```

**AIへの指示例:**
```
service層にある価格計算ロジックをドメイン層に移動してください。
- docs/ARCHITECTURE.mdのルールに従う
- OrderエンティティにCalculateTotalメソッドを追加
- テストも更新
```

## 🎯 効果的なAI指示の書き方

### ✅ Good Examples

**1. ドキュメント参照を明示**
```
docs/PATTERNS.mdを参照して、
新しいOrderItemエンティティを実装してください。
```

**2. パターンを指定**
```
catalog モジュールのレイヤードパターンに従って、
新しいCategoryエンドポイントを追加してください。
```

**3. 既存コードを参考にさせる**
```
modules/orders/と同じDDDパターンで、
新しいpaymentsモジュールを作成してください。
```

**4. 複数の要件を明示**
```
新しい機能を追加してください：
1. docs/ARCHITECTURE.mdのDDDパターンを使用
2. 型ヒントを全て付ける
3. docstringをGoogle Style で書く
4. テストも一緒に作成
```

### ❌ Bad Examples

**1. 曖昧すぎる**
```
注文機能を作って
→ 何をどう作るのか不明確
```

**2. パターン無視**
```
とりあえず動くコードを書いて
→ アーキテクチャ無視、保守性が低い
```

**3. ドキュメント無視**
```
適当に実装して
→ プロジェクトの規約に従わない
```

## 🔧 Cursor コマンド活用

### Cmd+K（エディタ内AI）

**よく使うプロンプト:**

```
# 型ヒント追加
「この関数に型ヒントを追加してください」

# docstring追加
「Google Styleのdocstringを追加してください」

# リファクタリング
「このメソッドをdocs/CONVENTIONS.mdに従ってリファクタリングしてください」

# テスト生成
「この関数のUnit Testを生成してください」
```

### Cmd+L（チャット）

**よく使う質問:**

```
# アーキテクチャ確認
「新しい決済機能を追加したいのですが、DDDパターンとレイヤードパターン
のどちらを使うべきですか？docs/ARCHITECTURE.mdを参照してください」

# コードレビュー
「このコードがdocs/CONVENTIONS.mdの規約に従っているかチェックしてください」

# デバッグ支援
「このN+1問題を解決する方法を、docs/CONVENTIONS.mdの規約に従って提案してください」
```

## 📚 AI が参照すべきドキュメント

Cursorに指示を出す際、以下を明示的に参照させると効果的です：

### 必須ドキュメント

1. **docs/ARCHITECTURE.md**
   - いつどのパターンを使うか
   - 依存関係のルール

2. **docs/CONVENTIONS.md**
   - 命名規則
   - 型ヒントのルール
   - コーディングスタイル

3. **docs/PATTERNS.md**
   - 具体的な実装パターン
   - コード例

### 参照用ドキュメント

4. **docs/DOMAIN_MODEL.md**
   - ドメインモデルの設計
   - Bounded Contextの境界

5. **docs/DEVELOPMENT.md**
   - 開発環境の使い方
   - コマンド一覧

## 🎨 VSCode/Cursor タスク

`Cmd+Shift+P` → "Tasks: Run Task" で実行可能：

- **開発サーバー起動**
- **テスト実行**
- **コード品質チェック**
- **コード自動修正**
- **Docker起動/停止**
- **対話的コミット**
- **マイグレーション実行**

## 💻 ターミナル統合

Cursor のターミナルで `make` コマンドが使えます：

```bash
make dev          # サーバー起動
make test         # テスト
make commit       # 対話的コミット
make fix          # コード自動修正
```

PATHは自動設定されています（.vscode/settings.json）

## 🔄 AI 駆動の開発サイクル

### 理想的なフロー

```
1. 要件定義
   ↓
2. Cursorに指示「docs/ARCHITECTURE.mdを参照して実装パターンを提案」
   ↓
3. パターン選択
   ↓
4. Cursorに指示「docs/PATTERNS.mdを参照してコード生成」
   ↓
5. コード生成
   ↓
6. make fix（自動修正）
   ↓
7. make test（テスト実行）
   ↓
8. make commit（自動コミット）
   ↓
9. PR作成
```

### 具体例

```
【要件】注文キャンセル機能を追加したい

【指示1】
「注文キャンセル機能を追加したいです。
docs/ARCHITECTURE.mdを参照して、どのパターンを使うべきか教えてください。」

【Cursorの応答】
「複雑なビジネスルール（キャンセル可能状態の判定、在庫戻し等）があるため、
modules/orders/のDDDパターンを使用すべきです。」

【指示2】
「了解。docs/PATTERNS.mdとmodules/orders/domain/entities/order.pyを参照して、
Orderエンティティにcancel()メソッドを追加してください。
ビジネスルール：
- 発送済みはキャンセル不可
- キャンセル時にドメインイベント発行」

【Cursorの応答】
→ コード生成

【実行】
make fix    # 自動修正
make test   # テスト確認
make commit-feat msg="add order cancellation"  # 自動コミット
```

## 🎓 ベストプラクティス

### 1. 常にドキュメントを参照させる

```
❌ 「注文機能を作って」
✅ 「docs/ARCHITECTURE.mdとdocs/PATTERNS.mdを参照して、
   注文機能を作ってください」
```

### 2. 既存コードをお手本にさせる

```
❌ 「新しいモジュールを作って」
✅ 「modules/orders/と同じ構造で、
   新しいpaymentsモジュールを作ってください」
```

### 3. テストもセットで生成させる

```
❌ 「この関数を実装して」
✅ 「この関数を実装して、
   Unit Testも一緒に生成してください」
```

### 4. 段階的に進める

```
【ステップ1】「まず、Entityを作ってください」
【ステップ2】「次に、Repositoryインターフェースを作ってください」
【ステップ3】「次に、Use Caseを作ってください」
【ステップ4】「最後に、APIエンドポイントを作ってください」
```

## 🚀 高度なテクニック

### 1. マルチファイル編集

```
「以下のファイルを一括で修正してください：
1. src/app/modules/orders/domain/entities/order.py
   - cancel()メソッド追加
2. src/app/modules/orders/domain/exceptions.py
   - OrderCannotBeCancelledException追加
3. tests/unit/test_order.py
   - キャンセルのテスト追加

docs/PATTERNS.mdを参照してください」
```

### 2. リファクタリング提案

```
「このコードをレビューして、
docs/ARCHITECTURE.mdとdocs/CONVENTIONS.mdに基づいて
改善点を提案してください」
```

### 3. ドキュメント更新

```
「このアーキテクチャ変更に伴い、
docs/DOMAIN_MODEL.mdを更新してください」
```

## 📖 参考資料

- [.cursorrules](.cursorrules) - AI のルール
- [.cursor/context.md](.cursor/context.md) - プロジェクトコンテキスト
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - アーキテクチャ
- [docs/CONVENTIONS.md](docs/CONVENTIONS.md) - コーディング規約
- [docs/PATTERNS.md](docs/PATTERNS.md) - 実装パターン

---

**Cursor AIと一緒に、効率的で高品質なコードを書きましょう！🚀**
