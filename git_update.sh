#!/bin/bash
# Simple Git update script
# Usage: ./git_update.sh [directory]

# Default directory
TARGET_DIR=${1:-/home/iot/workspace/transformers_as_jurr_ext}

echo "📂 Changing to directory: $TARGET_DIR"
cd "$TARGET_DIR" || { echo "❌ Directory not found: $TARGET_DIR"; exit 1; }

echo "🔄 Pulling latest changes..."
git pull

echo "➕ Adding all files..."
git add .

echo "💬 Committing changes..."
git commit -m "text generation in progress"

echo "🚀 Pushing to remote..."
git push

echo "✅ Done!"
