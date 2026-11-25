#!/usr/bin/env python3
# Usage and folder layout: content/README.md
import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content_src"
OUT = ROOT / "content"
GALLERY = OUT / "gallery"
MANIFEST = OUT / "manifest.json"
EXTS = {".png", ".jpg", ".jpeg", ".webp"}
MAX_SIDE = 1536
QUALITY = 85
KEEP_FIELDS = ("name", "is_premium", "priority", "difficulty", "available")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_") or "item"


def title(stem):
    return re.sub(r"[_\-]+", " ", stem).strip().capitalize()


def convert(src, dst):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, "WEBP", quality=QUALITY, method=6)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not SRC.is_dir():
        sys.exit(f"Put images in {SRC.relative_to(ROOT)}/<Category>/ first.")

    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    old_items = {g["id"]: g for g in old.get("gallery", [])}

    order_file = SRC / "categories.txt"
    folders = [d for d in SRC.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if order_file.exists():
        wanted = [l.strip() for l in order_file.read_text().splitlines() if l.strip()]
        folders.sort(key=lambda d: (wanted.index(d.name) if d.name in wanted else len(wanted), d.name.lower()))
    else:
        folders.sort(key=lambda d: d.name.lower())

    gallery, categories, written, skipped = [], [], 0, []
    for folder in folders:
        files = sorted(f for f in folder.iterdir() if f.suffix.lower() in EXTS)
        if not files:
            continue
        categories.append(folder.name)
        cat_slug = slug(folder.name)
        for index, f in enumerate(files):
            item_id = f"{cat_slug}/{slug(f.stem)}"
            rel = f"gallery/{cat_slug}/{slug(f.stem)}.webp"
            dst = OUT / rel
            if not dst.exists() or dst.stat().st_mtime < f.stat().st_mtime:
                if not args.dry_run:
                    try:
                        convert(f, dst)
                    except Exception as e:
                        skipped.append(f"{f.relative_to(ROOT)}: {e}")
                        continue
                written += 1
            item = {
                "id": item_id,
                "name": title(f.stem),
                "category": folder.name,
                "is_premium": False,
                "priority": index,
                "path": rel,
            }
            prev = old_items.get(item_id)
            if prev:
                item.update({k: prev[k] for k in KEEP_FIELDS if k in prev})
            gallery.append(item)

    live = {OUT / g["path"] for g in gallery}
    stale = [p for p in GALLERY.rglob("*") if p.is_file() and p not in live] if GALLERY.exists() else []

    changed = gallery != old.get("gallery") or categories != old.get("categories")
    version = old.get("version", 0) + (1 if changed else 0)
    # Keep lessons / video_lessons / ai_prompts written by build_extras.py.
    manifest = {**old, "version": version, "categories": categories, "gallery": gallery}

    print(f"{len(gallery)} images in {len(categories)} categories; "
          f"{written} converted, {len(stale)} removed, manifest v{version}{' (unchanged)' if not changed else ''}")
    for c in categories:
        print(f"  {c}: {sum(1 for g in gallery if g['category'] == c)}")
    for s in skipped:
        print(f"  skipped {s}")

    if args.dry_run:
        return
    for p in stale:
        p.unlink()
    for d in sorted(GALLERY.rglob("*"), reverse=True) if GALLERY.exists() else []:
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    size = sum(p.stat().st_size for p in GALLERY.rglob("*") if p.is_file()) if GALLERY.exists() else 0
    print(f"content/gallery is {size / 1e6:.1f} MB. Commit and push content/ to publish.")


if __name__ == "__main__":
    main()
