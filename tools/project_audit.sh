#!/usr/bin/env bash

echo "========================================"
echo " AI_Trading - Project Audit"
echo "========================================"
echo

echo "[1] Repository"
git status --short

echo
echo "[2] Python cache"
find . -type d -name "__pycache__"

echo
echo "[3] Python compiled files"
find . -type f -name "*.pyc"

echo
echo "[4] Documentation"
find docs -maxdepth 1 -type f | sort

echo
echo "[5] Core modules"
find core -maxdepth 1 -type f | sort

echo
echo "[6] Tests"
find . -maxdepth 1 -name "test_*.py" | sort

echo
echo "Audit completed."
