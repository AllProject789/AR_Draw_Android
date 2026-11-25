#!/usr/bin/env python3
# Imports lessons, video lessons and AI prompt samples from a reference export into content/.
# Usage: python3 tools/build_extras.py /path/to/export   (the folder holding manifest.json, lessons/, ...)
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content"
MANIFEST = OUT / "manifest.json"
MAX_SIDE = 1536
QUALITY = 85


def slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_") or "item"


JOBS = []


def to_webp(src, rel):
    JOBS.append((src, rel))
    return rel


# Lesson steps are palette PNGs, already smaller than WebP for line art, so they are copied as-is.
def copy_png(src, rel):
    JOBS.append((src, rel))
    return rel


def convert(job):
    src, rel = job
    dst = OUT / rel
    if rel.endswith(".png"):
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        return
    if dst.exists() and dst.stat().st_size > 0 and dst.stat().st_mtime >= src.stat().st_mtime:
        return
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, "WEBP", quality=QUALITY, method=4)


def lessons(src, ref):
    out, per_cat = [], Counter()
    for lesson in sorted(ref["lessons"], key=lambda l: (l["category"], l["level"], l["id"])):
        per_cat[lesson["category"]] += 1
        n = per_cat[lesson["category"]]
        lid = f"{slug(lesson['category'])}_{n:02d}"
        steps = sorted(p for p in (src / lesson["steps_dir"]).iterdir() if p.suffix.lower() == ".png")
        out.append({
            "id": lid,
            "name": f"{lesson['category']} lesson {n}",
            "category": lesson["category"],
            "level": lesson["level"],
            "steps_count": len(steps),
            "is_premium": False,
            "cover": copy_png(src / lesson["cover"], f"lessons/{lid}/cover.png"),
            "steps": [copy_png(p, f"lessons/{lid}/step_{i:02d}.png") for i, p in enumerate(steps, 1)],
        })
    return out


def videos(src):
    out = []
    dirs = sorted((src / "video_lessons").iterdir(), key=lambda d: int(d.name.split("_")[-1]))
    for d in dirs:
        n = int(d.name.split("_")[-1])
        clips = sorted(d.glob("*.mp4"))
        full = next((c for c in clips if "full_lesson" in c.name), None)
        steps = [c for c in clips if c is not full]

        def copy(c, name):
            rel = f"video_lessons/tutorial_{n:02d}/{name}"
            (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(c, OUT / rel)
            return rel

        out.append({
            "id": f"tutorial_{n:02d}",
            "name": f"Tutorial {n}",
            "is_premium": False,
            "full": copy(full, "full.mp4") if full else None,
            "steps": [copy(c, f"step_{i:02d}.mp4") for i, c in enumerate(steps, 1)],
        })
    return out


def ai_prompts(src, ref):
    out, per_style = [], defaultdict(int)
    for p in sorted(ref["ai_prompts"], key=lambda a: (a["style"], a["path"])):
        per_style[p["style"]] += 1
        rel = f"ai_prompts/{slug(p['style'])}/{slug(p['style'])}_{per_style[p['style']]:02d}.webp"
        out.append({"style": p["style"], "prompt": p["prompt"], "is_premium": False,
                    "path": to_webp(src / p["path"], rel)})
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 tools/build_extras.py /path/to/export")
    src = Path(sys.argv[1]).resolve()
    ref = json.loads((src / "manifest.json").read_text())
    shutil.rmtree(OUT / "video_lessons", ignore_errors=True)

    manifest = json.loads(MANIFEST.read_text())
    manifest["lessons"] = lessons(src, ref)
    manifest["video_lessons"] = videos(src)
    manifest["ai_prompts"] = ai_prompts(src, ref)
    manifest["version"] = manifest.get("version", 0) + 1

    with ProcessPoolExecutor() as pool:
        list(pool.map(convert, JOBS, chunksize=8))
    wanted = {OUT / rel for _, rel in JOBS}
    for name in ("lessons", "ai_prompts"):
        for f in (OUT / name).rglob("*") if (OUT / name).exists() else []:
            if f.is_file() and f not in wanted:
                f.unlink()
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    steps = sum(len(l["steps"]) for l in manifest["lessons"])
    clips = sum(len(v["steps"]) + (1 if v["full"] else 0) for v in manifest["video_lessons"])
    print(f"{len(manifest['lessons'])} lessons ({steps} steps), {len(manifest['video_lessons'])} video tutorials "
          f"({clips} clips), {len(manifest['ai_prompts'])} AI prompts; manifest v{manifest['version']}")


if __name__ == "__main__":
    main()
