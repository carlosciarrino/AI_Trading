#!/usr/bin/env bash

echo "=========================================="
echo " AI_Trading - Project Snapshot"
echo "=========================================="
echo

echo "Repository:"
git status --short

echo
echo "Python files:"
find . -name "*.py" | wc -l

echo "Core modules:"
find core -maxdepth 1 -name "*.py" | wc -l

echo "Documentation:"
find docs -maxdepth 1 -name "*.md" | wc -l

echo "Tests:"
find . -maxdepth 1 -name "test_*.py" | wc -l

echo
echo "Duplicate filenames:"
find . -name "*.py" -printf "%f\n" | sort | uniq -d

echo
echo "Snapshot complete."
