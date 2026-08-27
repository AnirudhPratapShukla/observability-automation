#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$BASE_DIR" || exit 1

python3 monitor.py >> "$BASE_DIR/logs/errors/monitor.log" 2>&1
STATUS=$?

if [ "$STATUS" -eq 0 ]; then
    mv "$BASE_DIR"/output/*.json "$BASE_DIR/logs/output/" 2>/dev/null
fi

exit "$STATUS"
