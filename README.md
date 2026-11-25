# AR Draw catalog

Drawing catalog for the AR Draw Android app. The app reads
`https://raw.githubusercontent.com/AllProject789/AR_Draw_Android/main/content/manifest.json`
and loads each image from `content/<path>`. Pushes reach users in about 5 minutes; no app update needed.

## Adding drawings

1. Put images in `content_src/<Category Name>/` (gitignored). Optional `content_src/categories.txt` sets chip order.
2. `pip3 install pillow && python3 tools/build_catalog.py`
3. Commit and push `content/`.

See `content/README.md` for manifest fields (premium, hide, rename, order).

## Lessons, video tutorials, AI prompt samples

`python3 tools/build_extras.py /path/to/export` rebuilds `content/lessons/`, `content/video_lessons/` and
`content/ai_prompts/` and their `lessons`, `video_lessons` and `ai_prompts` arrays in `manifest.json`.
Each lesson has a `cover` and ordered `steps` (PNG); each tutorial has a `full` video and ordered `steps` clips.
`build_catalog.py` keeps these arrays when it rebuilds the gallery.
