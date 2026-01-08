#!/bin/bash
# クイック修正スクリプト - よくある問題を自動修正

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 クイック修正スクリプト${NC}"
echo ""

# pyproject.tomlの修正
echo -e "${YELLOW}→${NC} pyproject.tomlを確認中..."
if ! grep -q "tool.hatch.build.targets.wheel" pyproject.toml; then
    echo "  hatchling設定を追加中..."
    cat >> pyproject.toml << 'EOF'

[tool.hatch.build.targets.wheel]
packages = ["src/app"]
EOF
    echo -e "  ${GREEN}✓${NC} pyproject.tomlを修正しました"
else
    echo -e "  ${GREEN}✓${NC} pyproject.tomlは正常です"
fi

# docker-compose.ymlの修正
echo -e "${YELLOW}→${NC} docker-compose.ymlを確認中..."
if grep -q "^version:" docker-compose.yml; then
    echo "  古いversion指定を削除中..."
    sed -i.bak '/^version:/d' docker-compose.yml
    rm -f docker-compose.yml.bak
    echo -e "  ${GREEN}✓${NC} docker-compose.ymlを修正しました"
else
    echo -e "  ${GREEN}✓${NC} docker-compose.ymlは正常です"
fi

# alembic versionsディレクトリの作成
echo -e "${YELLOW}→${NC} alembic設定を確認中..."
mkdir -p alembic/versions
echo -e "  ${GREEN}✓${NC} alembic/versions/ディレクトリを作成しました"

# alembic.iniのruff hook無効化
echo -e "${YELLOW}→${NC} alembic.iniを確認中..."
if grep -q "^hooks = ruff" alembic.ini; then
    echo "  ruff hookを無効化中..."
    sed -i.bak 's/^hooks = ruff/# hooks = ruff/' alembic.ini
    sed -i.bak 's/^ruff\./# ruff./' alembic.ini
    rm -f alembic.ini.bak
    echo -e "  ${GREEN}✓${NC} alembic.iniを修正しました"
else
    echo -e "  ${GREEN}✓${NC} alembic.iniは正常です"
fi

# .envファイルの確認
echo -e "${YELLOW}→${NC} .envファイルを確認中..."
if [ ! -f .env ]; then
    echo "  .envファイルを作成中..."
    SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo "change-this-in-production")
    cat > .env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_template
DATABASE_ECHO=false
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=FastAPI Template
APP_VERSION=0.1.0
DEBUG=true
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
LOG_LEVEL=INFO
EOF
    echo -e "  ${GREEN}✓${NC} .envファイルを作成しました"
else
    echo -e "  ${GREEN}✓${NC} .envファイルは存在します"
fi

echo ""
echo -e "${GREEN}✅ 全ての修正が完了しました！${NC}"
echo ""
echo "次のコマンドでセットアップを続行できます:"
echo "  make setup    # または"
echo "  make install-dev && make up && make db-upgrade"
