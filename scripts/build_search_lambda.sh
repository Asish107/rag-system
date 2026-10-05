#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAMBDA_DIR="$PROJECT_ROOT/lambda/search"

echo "Removing previous Lambda package..."
rm -rf "$LAMBDA_DIR"
mkdir -p "$LAMBDA_DIR"

echo "Installing Linux dependencies..."
uv pip install \
  --target "$LAMBDA_DIR" \
  --python-platform x86_64-manylinux2014 \
  --python-version 3.12 \
  "psycopg[binary]" \
  pgvector

echo "Copying latest application code..."
cp -R "$PROJECT_ROOT/rag" "$LAMBDA_DIR/rag"

echo "Removing Python cache files..."
find "$LAMBDA_DIR" -type d -name "__pycache__" -prune -exec rm -rf {} +

echo "Verifying packaged handler matches source..."
diff \
  "$PROJECT_ROOT/rag/handlers/search.py" \
  "$LAMBDA_DIR/rag/handlers/search.py"

echo "Build complete:"
du -sh "$LAMBDA_DIR"