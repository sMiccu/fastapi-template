# 技術スタック

## 概要
このテンプレートは、モダンなPython開発のベストプラクティスを取り入れた、実用的なFastAPIバックエンドテンプレートです。

## 言語・フレームワーク

### Python 3.12+
- **選定理由**:
  - 最新の型ヒント機能（PEP 695: Type Parameter Syntax等）
  - パフォーマンス改善
  - より良いエラーメッセージ

### FastAPI 0.110+
- **選定理由**:
  - 高速（Starlette + Pydantic）
  - 自動的なAPI ドキュメント生成（OpenAPI/Swagger）
  - Python型ヒントベースのバリデーション
  - 依存性注入システム
  - 同期・非同期両対応

### Pydantic v2
- **選定理由**:
  - バリデーションとシリアライゼーション
  - 設定管理（pydantic-settings）
  - FastAPIとのネイティブ統合
  - v2での大幅なパフォーマンス向上

## パッケージ管理

### uv
- **選定理由**:
  - Rust製で非常に高速（pip/poetry比で10-100倍）
  - pyproject.toml標準対応
  - lockファイル自動生成
  - pip互換コマンド
  - モダンで将来性がある

## データベース・ORM

### SQLAlchemy 2.0+
- **選定理由**:
  - Python de facto standardのORM
  - 2.0系での大幅な改善（型ヒント対応強化）
  - 同期・非同期両対応
  - リッチなクエリビルダー
  - **基本は同期処理で使用、必要に応じて非同期対応可能**

### PostgreSQL 16+
- **選定理由**:
  - エンタープライズグレードのRDB
  - JSON型サポート
  - 豊富な拡張機能
  - 優れたパフォーマンスとスケーラビリティ

### Redis 7+
- **選定理由**:
  - キャッシュ・セッション管理
  - 高速なKey-Valueストア
  - Pub/Sub機能

### Alembic
- **選定理由**:
  - SQLAlchemy公式のマイグレーションツール
  - 自動マイグレーション生成
  - バージョン管理

## 開発ツール

### mypy (型チェック)
- **選定理由**:
  - 静的型チェック
  - バグの早期発見
  - IDEの補完精度向上
  - コードの可読性向上

### ruff (linter/formatter)
- **選定理由**:
  - Rust製で非常に高速
  - flake8, black, isort等を統合
  - 設定がシンプル
  - 自動修正機能

### pytest + pytest-cov
- **選定理由**:
  - Python標準のテストフレームワーク
  - リッチなfixture機能
  - パラメトライズドテスト
  - カバレッジ計測

### pre-commit
- **選定理由**:
  - コミット前の自動チェック
  - チーム全体でコード品質を担保
  - CIの負荷軽減

## タスクランナー

### Task (go-task)
- **選定理由**:
  - makefileの現代的代替
  - YAML形式で読みやすい
  - クロスプラットフォーム
  - 依存関係管理
  - **代替**: GNU Make（よりシンプルな選択肢）

## コンテナ・開発環境

### Docker + Docker Compose
- **選定理由**:
  - 環境の再現性
  - PostgreSQL/Redisの簡単なセットアップ
  - 本番環境との整合性

### Dev Container
- **選定理由**:
  - VSCode/Cursor完全統合
  - チーム全員が同じ開発環境
  - セットアップの簡素化

## CI/CD

### GitHub Actions
- **選定理由**:
  - GitHubネイティブ統合
  - 無料枠が豊富
  - 豊富なマーケットプレイスアクション
  - YAML形式で管理

### CI項目
- Linting (ruff)
- Type checking (mypy)
- Testing (pytest)
- Build (Docker)

## セキュリティ

### python-jose (JWT)
- **選定理由**:
  - JWT認証の実装
  - FastAPIとの相性が良い

### passlib + bcrypt
- **選定理由**:
  - パスワードハッシュ化
  - 複数のハッシュアルゴリズム対応

## ロギング

### structlog
- **選定理由**:
  - 構造化ログ
  - JSON形式出力
  - コンテキスト管理
  - 本番環境での解析が容易

## その他のライブラリ

### python-dotenv
- 環境変数管理

### httpx
- HTTP クライアント（外部API連携）
- 同期・非同期両対応

### tenacity
- リトライ処理

## バージョン管理方針

- **Python**: 3.12以上を推奨
- **依存パッケージ**: セマンティックバージョニングで固定
- **定期的なアップデート**: 四半期ごとに依存関係を見直し

## 同期 vs 非同期の方針

### 基本方針
- **デフォルトは同期処理**: シンプルで理解しやすい
- **必要に応じて非同期**: 高負荷・I/O待機が多い場合

### 同期処理を選ぶケース
- シンプルなCRUD操作
- 管理画面系
- バッチ処理
- 開発初期フェーズ

### 非同期処理を検討するケース
- 高並行性が必要
- 外部API呼び出しが多い
- WebSocket/SSE
- リアルタイム処理

### 実装上の配慮
- リポジトリ層は同期・非同期の両インターフェースを提供可能な設計
- Use Case層で同期/非同期を選択できる柔軟性を確保

## 参考資料

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/)
- [uv公式ドキュメント](https://github.com/astral-sh/uv)
- [Ruff公式ドキュメント](https://docs.astral.sh/ruff/)
