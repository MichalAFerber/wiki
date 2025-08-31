#!/usr/bin/env bash
set -euo pipefail

# Config via env vars (override as needed)
OBSIDIAN_VAULT="${OBSIDIAN_VAULT:-/PATH/TO/YourObsidianVault}"
PUBLIC_FOLDER="${PUBLIC_FOLDER:-Public}"
ATTACHMENTS_FOLDER="${ATTACHMENTS_FOLDER:-}"   # e.g., "Attachments" if you use a central attachments dir

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DST="$REPO_ROOT/docs"
ASSETS_ATTACH_DST="$DOCS_DST/assets/attachments"

if [ ! -d "$OBSIDIAN_VAULT" ]; then
  echo "Vault not found: $OBSIDIAN_VAULT" >&2
  exit 1
fi

echo "Vault:         $OBSIDIAN_VAULT"
echo "Public folder: $PUBLIC_FOLDER"
echo "Docs dest:     $DOCS_DST"
echo

mkdir -p "$DOCS_DST"

RSYNC_OPTS=(-av --delete --prune-empty-dirs --copy-links)

# Copy Public → docs/
if [ -d "$OBSIDIAN_VAULT/$PUBLIC_FOLDER" ]; then
  rsync "${RSYNC_OPTS[@]}" "$OBSIDIAN_VAULT/$PUBLIC_FOLDER/" "$DOCS_DST/"
else
  echo "ERROR: Public folder not found in vault ($PUBLIC_FOLDER)" >&2
  exit 2
fi

# Optional: copy central attachments → docs/assets/attachments/
if [ -n "${ATTACHMENTS_FOLDER}" ]; then
  if [ -d "$OBSIDIAN_VAULT/$ATTACHMENTS_FOLDER" ]; then
    mkdir -p "$ASSETS_ATTACH_DST"
    rsync "${RSYNC_OPTS[@]}" "$OBSIDIAN_VAULT/$ATTACHMENTS_FOLDER/" "$ASSETS_ATTACH_DST/"
    echo "Copied central attachments to: $ASSETS_ATTACH_DST"
  else
    echo "Warning: central attachments folder not found: $ATTACHMENTS_FOLDER"
  fi
fi

echo
echo "Sync complete."
echo "Next: mkdocs serve   # preview locally"
