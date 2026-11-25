# AR Draw catalog

Drawing catalog for the AR Draw Android app. The app reads
`https://raw.githubusercontent.com/AllProject789/AR_Draw_Android/main/content/manifest.json`
and loads each image from `content/<path>`. Pushes reach users in about 5 minutes; no app update needed.

## Adding drawings

1. Put images in `content_src/<Category Name>/` (gitignored). Optional `content_src/categories.txt` sets chip order.
2. `pip3 install pillow && python3 tools/build_catalog.py`
3. Commit and push `content/`.

See `content/README.md` for manifest fields (premium, hide, rename, order).
