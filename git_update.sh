#!/bin/bash
# Simple Git update script with safety check
# Usage: ./git_update.sh [directory]
# Default: /home/iot/workspace/transformers_as_jurr_ext


echo "🕒 Run started at $(date)" >> /home/iot/scripts/git_update.log

# Set target directory (use default if not provided)
TARGET_DIR=${1:-/home/iot/workspace/transformers_as_jurr_ext}

echo "📂 Changing to directory: $TARGET_DIR"
cd "$TARGET_DIR" || { echo "❌ Directory not found: $TARGET_DIR"; exit 1; }

echo "🔄 Pulling latest changes..."
git pull

echo "➕ Adding all files..."
git add .

# 🛡️ Commit only if there are changes
if ! git diff-index --quiet HEAD --; then
  echo "💬 Committing changes..."
  git commit -m "text generation in progress"
  echo "🚀 Pushing to remote..."
  git push
  echo "✅ Done!"
else
  echo "🟢 No changes to commit. Skipping commit and push."
fi
