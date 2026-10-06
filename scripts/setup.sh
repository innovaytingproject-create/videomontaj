#!/bin/bash
# Restores the video toolchain in a fresh cloud container (node_modules and pip packages are not in git).
set -e
cd "$(dirname "$0")/.."
(cd remotion-studio && npm install --no-audit --no-fund --silent)
pip install -q faster-whisper 2>/dev/null || true
