#!/usr/bin/env bash
set -u

MODULE="${1:-all}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAILURES=()

run_step() {
  local name="$1" dir="$2" cmd="$3"
  echo "==> $name"
  (cd "$ROOT/$dir" && eval "$cmd")
  local code=$?
  if [ "$code" -ne 0 ]; then
    echo "    FAIL: $name (exit $code)"
    FAILURES+=("$name")
  else
    echo "    OK: $name"
  fi
}

case "$MODULE" in
  frontend)
    run_step "frontend: lint" "frontend" "npm run lint"
    run_step "frontend: build" "frontend" "npm run build"
    ;;
  backend)
    run_step "backend: test" "backend" "./mvnw test"
    ;;
  ingestion)
    run_step "ingestion: build" "ingestion" "go build ./..."
    run_step "ingestion: test" "ingestion" "go test ./..."
    ;;
  all)
    run_step "frontend: lint" "frontend" "npm run lint"
    run_step "frontend: build" "frontend" "npm run build"
    run_step "backend: test" "backend" "./mvnw test"
    run_step "ingestion: build" "ingestion" "go build ./..."
    run_step "ingestion: test" "ingestion" "go test ./..."
    ;;
  *)
    echo "Modulo invalido: $MODULE (use all, frontend, backend, ingestion)"
    exit 2
    ;;
esac

echo ""
if [ "${#FAILURES[@]}" -gt 0 ]; then
  echo "HARNESS FALHOU - etapas com erro:"
  for f in "${FAILURES[@]}"; do
    echo "  - $f"
  done
  exit 1
fi

echo "HARNESS OK - todos os modulos validados"
exit 0