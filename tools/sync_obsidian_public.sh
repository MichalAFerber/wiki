#!/usr/bin/env bash
set -Eeuo pipefail

# === Defaults (can still be overridden via environment) ===
OBSIDIAN_VAULT="${OBSIDIAN_VAULT:-/Users/michal/Documents/Obsidian Vault/Wiki}"
PUBLIC_FOLDER="${PUBLIC_FOLDER:-Public}"
ATTACHMENTS_FOLDER="${ATTACHMENTS_FOLDER:-Attachments/Public}"   # central attachments for PUBLIC notes

# === Derived paths ===
PUBLIC_SRC="${OBSIDIAN_VAULT}/${PUBLIC_FOLDER}"
ATTACH_SRC="${OBSIDIAN_VAULT}/${ATTACHMENTS_FOLDER}"

# Resolve repo root (directory containing this script, then up one if we're inside scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -d "${SCRIPT_DIR}/docs" ]]; then
  REPO_ROOT="${SCRIPT_DIR}"
elif [[ -d "${SCRIPT_DIR}/../docs" ]]; then
  REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
else
  # Fallback: assume current working dir is repo root
  REPO_ROOT="$(pwd)"
fi

DOCS_DST="${REPO_ROOT}/docs"
ATTACH_DST="${DOCS_DST}/assets/attachments"

# === Preflight ===
if [[ ! -d "${OBSIDIAN_VAULT}" ]]; then
  echo "ERROR: Vault not found: ${OBSIDIAN_VAULT}" >&2
  exit 1
fi
if [[ ! -d "${PUBLIC_SRC}" ]]; then
  echo "ERROR: Public folder not found: ${PUBLIC_SRC}" >&2
  exit 2
fi

mkdir -p "${DOCS_DST}"

echo "Vault:         ${OBSIDIAN_VAULT}"
echo "Public src:    ${PUBLIC_SRC}"
echo "Docs dest:     ${DOCS_DST}"
echo "Attachments:   ${ATTACH_SRC}  (optional)"
echo

# rsync options:
# -a archive, -v verbose, -h human, --delete to mirror deletions,
# --prune-empty-dirs to skip empty, --copy-links to copy linked files,
# excludes for common noise
RSYNC_OPTS=(-avh --delete --prune-empty-dirs --copy-links \
  --exclude '.obsidian' --exclude '.DS_Store' --exclude 'Thumbs.db')

# === Copy Public → docs/ ===
rsync "${RSYNC_OPTS[@]}" "${PUBLIC_SRC}/" "${DOCS_DST}/"

# === Copy central attachments (if present) → docs/assets/attachments/ ===
if [[ -d "${ATTACH_SRC}" ]]; then
  mkdir -p "${ATTACH_DST}"
  rsync "${RSYNC_OPTS[@]}" "${ATTACH_SRC}/" "${ATTACH_DST}/"
  echo "Copied attachments to: ${ATTACH_DST}"
else
  echo "Note: attachments folder not found at ${ATTACH_SRC} (skipping)"
fi

echo
echo "Sync complete."
echo "Next steps:"
echo "  mkdocs serve   # preview at http://127.0.0.1:8000"
echo "  git add -A && git commit -m 'Sync from Obsidian' && git push"
