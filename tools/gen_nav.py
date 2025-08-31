# tools/gen_nav.py
import re, yaml
from pathlib import Path

ROOT = Path('.')
DOCS = ROOT / 'docs'
MKDOCS = ROOT / 'mkdocs.yml'
EXCLUDE_DIRS = {'assets','images','img','javascripts','js','css','.obsidian'}
MD_EXTS = {'.md', '.markdown', '.mkd'}

def clean_title(name: str) -> str:
    n = re.sub(r'^\d+[-_ ]+', '', name)  # drop numeric prefixes like 01-
    return n.replace('_',' ').replace('-',' ').strip().title()

def read_h1(p: Path) -> str | None:
    try:
        for line in p.open(encoding='utf-8', errors='ignore'):
            m = re.match(r'^\s*#\s+(.+?)\s*$', line)
            if m:
                return m.group(1).strip()
    except Exception:
        pass
    return None

def sort_key(p: Path):
    m = re.match(r'^(\d+)[-_ ]*(.*)$', p.stem, re.I)
    return (int(m.group(1)), p.stem.lower()) if m else (10_000_000, p.stem.lower())

def build_nav(dir_path: Path, rel_dir: Path = Path('')) -> list:
    items = []

    # Section overview: prefer _index.md; fallback to index.md
    idx = dir_path / '_index.md'
    if not idx.exists():
        idx = dir_path / 'index.md'
    if idx.exists():
        t = read_h1(idx) or clean_title(dir_path.name)
        items.append({t: str(rel_dir / idx.name)})

    # Regular files (exclude index files)
    files = [p for p in dir_path.iterdir()
             if p.is_file() and p.suffix.lower() in MD_EXTS and p.name not in {'_index.md','index.md'}]
    files.sort(key=sort_key)
    for f in files:
        t = read_h1(f) or clean_title(f.stem)
        items.append({t: str(rel_dir / f.name)})

    # Subdirectories
    dirs = [d for d in dir_path.iterdir() if d.is_dir() and d.name not in EXCLUDE_DIRS and not d.name.startswith('.')]
    dirs.sort(key=sort_key)
    for d in dirs:
        sub = build_nav(d, rel_dir / d.name)
        if sub:
            items.append({clean_title(d.name): sub})

    return items

if not DOCS.exists():
    raise SystemExit("docs/ not found")

nav = []

# Home
home = DOCS / 'index.md'
if home.exists():
    home_title = read_h1(home) or 'Home'
    nav.append({home_title: 'index.md'})

# Top-level loose files
top_files = [p for p in DOCS.iterdir() if p.is_file() and p.suffix.lower() in MD_EXTS and p.name != 'index.md']
top_files.sort(key=sort_key)
for f in top_files:
    nav.append({(read_h1(f) or clean_title(f.stem)): f.name})

# Top-level dirs
top_dirs = [d for d in DOCS.iterdir() if d.is_dir() and d.name not in EXCLUDE_DIRS and not d.name.startswith('.')]
top_dirs.sort(key=sort_key)
for d in top_dirs:
    sub = build_nav(d, Path(d.name))
    if sub:
        nav.append({clean_title(d.name): sub})

cfg = yaml.safe_load(open(MKDOCS, encoding='utf-8'))
cfg['nav'] = nav
yaml.safe_dump(cfg, open(MKDOCS, 'w', encoding='utf-8'), sort_keys=False, allow_unicode=True, width=1000)
print("nav entries:", len(nav))
