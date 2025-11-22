#!/bin/bash
# Build script for upystar - syncs dependencies and builds the Rust extension

set -e  # Exit on error

echo "🔧 Syncing dependencies..."
unset CONDA_PREFIX && uv sync --extra dev

echo "🦀 Building Rust extension..."
unset CONDA_PREFIX && uv run maturin develop

echo "✅ Build complete!"