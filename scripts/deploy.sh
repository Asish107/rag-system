#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

echo "========================================"
echo "1. Running Ruff"
echo "========================================"

uv run ruff check .

echo
echo "========================================"
echo "2. Running tests"
echo "========================================"

env -u DB_HOST uv run pytest -q

echo
echo "========================================"
echo "3. Building Search Lambda"
echo "========================================"

./scripts/build_search_lambda.sh

echo
echo "========================================"
echo "4. Building API Lambda"
echo "========================================"

./scripts/build_api_lambda.sh

echo
echo "========================================"
echo "5. Applying Terraform"
echo "========================================"

terraform -chdir=infra apply

echo
echo "========================================"
echo "Deployment complete"
echo "========================================"