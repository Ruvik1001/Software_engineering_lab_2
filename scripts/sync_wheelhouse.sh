#!/usr/bin/env bash
# Заполняет wheelhouse_linux колёсами под образ python:3.12-slim (manylinux, cp312, amd64).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
DEST="$ROOT/wheelhouse_linux"
mkdir -p "$DEST"
rm -f "$DEST"/*.whl

REQ="$ROOT/wheelhouse_requirements.txt"
if [[ ! -f "$REQ" ]]; then
  echo "Missing $REQ" >&2
  exit 1
fi

python3 -m pip download \
  --dest "$DEST" \
  --platform manylinux_2_17_x86_64 \
  --python-version 3.12 \
  --implementation cp \
  --abi cp312 \
  --only-binary=:all: \
  -r "$REQ"

echo "OK: wheels saved to $DEST"
