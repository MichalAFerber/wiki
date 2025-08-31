# tools/gen_nav.py
from pathlib import Path
import re, yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

EXCLUDE_DIRS = {"assets","images","img","javascripts","js","css",".obsidian"}
MD_EXTS = {".md",".markdown",".mkd"}

def strip_prefix(name: str) -> str:
    return re.sub(r"^\d+[-_ ]+", "", name)

def humanize_fs_name(name: str) -> str:
    n = strip_prefix(name)
    return n.replace("_"," ").replace("-"," ")

def read_h1(p: Path) -> str | None:
    try:
        for line in p.open(encoding="utf-8", errors="ignore"):
            m = re.match(r"^\s*#\s+(.+?)\s*$", line)
            if m:
                return m.group(1).strip()
    except Exception:
        pass
    return None

def sort_key(p: Path):
    m = re.match(r"^(\d+)[-_ ]*(.*)$", p.stem, re.I)
    return (int(m.group(1)), p.stem.lower()) if m else (10_000_000, p.stem.lower())

def build_section(dir_path: Path, rel_dir: Path = Path("")) -> list:
    items = []

    # Section overview: prefer _index.md; fallback to index.md
    idx = dir_path / "_index.md"
    if not idx.exists():
        idx = dir_path / "index.md"
    if idx.exists():
        t = read_h1(idx) or humanize_fs_name(dir_path.name)
        items.append({t: str(rel_dir / idx.name)})

    # Files (exclude index files)
    files = [p for p in dir_path.iterdir()
             if p.is_file() and p.suffix.lower() in MD_EXTS and p.name not in {"_index.md","index.md"}]
    files.sort(key=sort_key)
    for f in files:
        t = read_h1(f) or humanize_fs_name(f.stem)
        items.append({t: str(rel_dir / f.name)})

    # Subdirs
    dirs = [d for d in dir_path.iterdir()
            if d.is_dir() and d.name not in EXCLUDE_DIRS and not d.name.startswith(".")]
    dirs.sort(key=sort_key)
    for d in dirs:
        sub = build_section(d, rel_dir / d.name)
        if sub:
            items.append({humanize_fs_name(d.name): sub})

    return items

def build_nav():
    if not DOCS.exists():
        raise SystemExit("docs/ not found")

    nav = []

    # Home
    home = DOCS / "index.md"
    if home.exists():
        nav.append({(read_h1(home) or "Home"): "index.md"})

    # Top-level files (e.g. Affiliates.md)
    top_files = [p for p in DOCS.iterdir()
                 if p.is_file() and p.suffix.lower() in MD_EXTS and p.name != "index.md"]
    top_files.sort(key=sort_key)
    for f in top_files:
        nav.append({(read_h1(f) or humanize_fs_name(f.stem)): f.name})

    # Top-level dirs
    top_dirs = [d for d in DOCS.iterdir()
                if d.is_dir() and d.name not in EXCLUDE_DIRS and not d.name.startswith(".")]
    top_dirs.sort(key=sort_key)
    for d in top_dirs:
        sub = build_section(d, Path(d.name))
        if sub:
            nav.append({humanize_fs_name(d.name): sub})

    return nav

def is_top_key(line: str) -> bool:
    # e.g., "plugins:", "theme:", "nav:", etc., at column 0 (allow leading spaces)
    return re.match(r"^\s*[A-Za-z_][\w-]*\s*:\s*(#.*)?$", line) is not None

def is_nav_key(line: str) -> bool:
    return re.match(r"^\s*nav\s*:\s*(#.*)?$", line) is not None

def splice_nav(nav_obj):
    text = MKDOCS.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Dump just the nav mapping
    nav_yaml = yaml.safe_dump({"nav": nav_obj}, sort_keys=False, allow_unicode=True, width=1000)
    if not nav_yaml.endswith("\n"):
        nav_yaml += "\n"

    # Find the first 'nav:' key
    start = None
    for i, ln in enumerate(lines):
        if is_nav_key(ln):
            start = i
            break

    if start is None:
        # Append at end
        new_text = text + ("" if text.endswith("\n") else "\n") + nav_yaml
        MKDOCS.write_text(new_text, encoding="utf-8")
        return

    # Consume ALL consecutive top-level 'nav:' blocks (handles duplicates from earlier runs)
    end = start + 1
    n = len(lines)
    while end < n:
        ln = lines[end]
        if is_top_key(ln) and not is_nav_key(ln):
            break
        end += 1

    # Replace [start:end) with fresh nav
    new_lines = lines[:start] + [nav_yaml] + lines[end:]
    MKDOCS.write_text("".join(new_lines), encoding="utf-8")

def main():
    nav = build_nav()
    splice_nav(nav)
    print("nav entries:", len(nav))

if __name__ == "__main__":
    main()
