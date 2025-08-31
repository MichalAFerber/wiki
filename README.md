# Public Wiki (MkDocs Material)

[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

Write in **Obsidian**, publish only your **Public** notes to a MkDocs Material site on **GitHub Pages**. Your private notes stay in Obsidian.

## Folder structure

```bash
repo-root/
├─ docs/                      # MkDocs content (generated from Obsidian/Public)
│  ├─ index.md
│  ├─ 404.html
│  ├─ Applications/
│  │  ├─ GSA Manager/index.md
│  │  ├─ ModMan/index.md
│  │  └─ ipcow.com/index.md
│  └─ assets/
│     ├─ attachments/         # copied from Obsidian/Attachments/Public
│     ├─ img/                 # site images (logo, favicon, etc.)
│     └─ js/
│        └─ init-mermaid.js
├─ tools/
│  ├─ sync_obsidian_public.sh # Obsidian → docs sync (+ nav regeneration)
│  └─ gen_nav.py              # Generates mkdocs.yml "nav:" from docs/
├─ .github/workflows/
│  └─ deploy-gh-pages.yml     # CI: build & deploy to GitHub Pages
├─ build-mkdocs.sh            # wrapper: sync + build/serve locally
├─ mkdocs.yml                 # MkDocs configuration
└─ LICENSE
```

## How the sync works (Obsidian → MkDocs)

* **Source:** `~/Documents/Obsidian Vault/Wiki/Public`
* **Destination:** `repo/docs/`
* **Attachments:** If present, `~/Documents/Obsidian Vault/Wiki/Attachments/Public` is mirrored to `docs/assets/attachments/`

Defaults in `tools/sync_obsidian_public.sh`:

```bash
OBSIDIAN_VAULT="${OBSIDIAN_VAULT:-/Users/michal/Documents/Obsidian Vault/Wiki}"
PUBLIC_FOLDER="${PUBLIC_FOLDER:-Public}"
ATTACHMENTS_FOLDER="${ATTACHMENTS_FOLDER:-Attachments/Public}"
```

Override at runtime if needed:

```bash
OBSIDIAN_VAULT="/Volumes/Data/Vault" ./tools/sync_obsidian_public.sh
```

The sync:

* mirrors deletions (`rsync --delete`)
* ignores `.obsidian`, `.DS_Store`, etc.
* runs the nav generator (`tools/gen_nav.py`) after syncing so the sidebar matches the current `docs/`.

## Navigation: how it’s built

`tools/gen_nav.py` scans `docs/` and writes a **`nav:`** section into `mkdocs.yml`.

Rules:

* Uses each page’s **H1 text as-is** (preserves casing).
* For folders, it prefers `_index.md` or `index.md` as the section overview; the section title is that file’s H1 (or the folder name if no H1).
* If a file/folder name starts with a numeric prefix like `01-`, the numeric part is stripped for the label but still used for sorting.
* Skips common asset folders: `assets/`, `img/`, `js/`, etc.

Run it manually anytime:

```bash
python3 tools/gen_nav.py
```

## Local usage

### One-step wrapper

```bash
# Sync from Obsidian and build the site (strict)
./build-mkdocs.sh build

# Sync from Obsidian and run a local server
./build-mkdocs.sh serve
# e.g. custom port:
./build-mkdocs.sh serve -a 127.0.0.1:8001
```

### Direct commands

```bash
# Just sync (and auto-regenerate nav)
./tools/sync_obsidian_public.sh

# Preview locally
mkdocs serve

# Build locally (outputs to ./site)
mkdocs build --strict
```

> If `mkdocs` isn’t on PATH, the wrapper falls back to:
> `~/.local/pipx/venvs/mkdocs/bin/mkdocs`

## CI/CD (GitHub Actions)

Workflow: `.github/workflows/deploy-gh-pages.yml`

What it does:

1. Checks out the repo.
2. Sets up Python and installs:

   * `mkdocs`, `mkdocs-material`, `mkdocs-roamlinks-plugin`, `pyyaml`
3. **Generates `nav:`** from `docs/` using `tools/gen_nav.py`
   (ensures server-side builds match local even if someone didn’t run the local script)
4. Builds the site with `mkdocs build --strict`.
5. Uploads the artifact and deploys to **GitHub Pages**.

Repo settings:

* **Settings → Pages** → Source: **GitHub Actions**
* In `mkdocs.yml`, set `site_url` to your final URL (e.g., `https://USER.github.io/REPO/` or your custom domain). This ensures correct canonical links and sitemap.

## Adding / updating docs

1. **Write in Obsidian** under your Vault’s `Public/` folder.

   * Each **folder** can have an `_index.md` or `index.md` to act as the section overview.
   * Put images in the same folder as the note **or** in your central `Attachments/Public/…` (which syncs to `docs/assets/attachments/…`).

2. **Links & images**

   * Obsidian wikilinks like `[[Note Title]]` and header links `[[#Section]]` work via `mkdocs-roamlinks-plugin`.
   * For images:

     * If copied centrally: `![](assets/attachments/<path>/image.png)`
     * If next to the note: `![](image.png)` (relative path)
   * In-page anchors: MkDocs slugifies headings (lower-case). To preserve mixed-case anchors, add an explicit ID:

     ```md
     ## ModMan {#ModMan}
     [Back to top](#ModMan)
     ```

3. **Generate & preview**

   ```bash
   ./build-mkdocs.sh serve
   ```

   The sidebar nav updates automatically. Fix any warnings in the console.

4. **Commit & push**

   ```bash
   git add -A
   git commit -m "Sync from Obsidian"
   git push
   ```

   GitHub Actions builds and deploys.

## Site chrome (favicon, 404, Mermaid)

* **Favicon / logo**: place in `docs/assets/img/` and reference in `mkdocs.yml`:

  ```yaml
  theme:
    logo: assets/img/logo.png
    favicon: assets/img/favicon.png
  ```

* **Custom 404**: keep exactly one file named `docs/404.html`.
  (Don’t also keep `404.html.md`, which would render to the same path.)
* **Mermaid** diagrams:

  * `docs/assets/js/init-mermaid.js` initializes Mermaid.
  * Referenced from `mkdocs.yml`:

    ```yaml
    extra_javascript:
      - https://unpkg.com/mermaid@10.9.1/dist/mermaid.min.js
      - assets/js/init-mermaid.js
    ```

## Troubleshooting

* **“pages exist… not included in the nav”**: run `python3 tools/gen_nav.py` or `./build-mkdocs.sh build` to regenerate `nav:`.
* **Anchor warnings in `--strict`**: ensure your links match the actual anchor (lower-case by default) or add explicit IDs `{#YourAnchor}`.
* **Port already in use** (on `mkdocs serve`):
  `mkdocs serve -a 127.0.0.1:8001`
* **DeprecationWarning from `mkdocs_roamlinks_plugin`**: harmless. Hide locally with:

  ```bash
  PYTHONWARNINGS="ignore::DeprecationWarning:mkdocs_roamlinks_plugin.plugin" mkdocs serve
  ```

* **Sitemap**: no plugin needed. MkDocs emits `/sitemap.xml` when `site_url` is set.

## Requirements (local)

* Python 3.12+ recommended
* `mkdocs`, `mkdocs-material`, `mkdocs-roamlinks-plugin`, `pyyaml`

  * With pipx:

    ```bash
    pipx install mkdocs
    pipx inject mkdocs mkdocs-material mkdocs-roamlinks-plugin pyyaml
    ```

---

MIT © 2025 Michal Ferber
