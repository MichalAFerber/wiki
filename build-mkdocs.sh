#!/usr/bin/env bash
set -Eeuo pipefail

# 1) Sync Obsidian → docs (attachments too)
./tools/sync_obsidian_public.sh
echo "Sync from Obsidian/Wiki/Public to docs is complete."

# 2) Regenerate nav (so new root files like Affiliates.md appear)
if [[ -f tools/gen_nav.py ]]; then
  if [[ -x "${HOME}/.local/pipx/venvs/mkdocs/bin/python" ]]; then
    "${HOME}/.local/pipx/venvs/mkdocs/bin/python" tools/gen_nav.py || {
      # fallback to system python but ensure PyYAML is installed
      python3 - <<'PY'
import sys, subprocess
try:
    import yaml  # noqa
except Exception:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pyyaml"])
PY
      python3 tools/gen_nav.py
    }
  else
    python3 tools/gen_nav.py
  fi
  echo "Nav regenerated from docs/."
fi

# 3) Build or serve
CMD="${1:-build}"   # build | serve
if [[ "$CMD" == "serve" ]]; then
  shift
  if command -v mkdocs >/dev/null 2>&1; then
    mkdocs serve "$@"
  else
    "${HOME}/.local/pipx/venvs/mkdocs/bin/mkdocs" serve "$@"
  fi
  echo "MkDocs server stopped."
else
  shift || true
  if command -v mkdocs >/dev/null 2>&1; then
    mkdocs build --strict "$@"
  else
    "${HOME}/.local/pipx/venvs/mkdocs/bin/mkdocs" build --strict "$@"
  fi
  echo "MkDocs has been built."
fi
