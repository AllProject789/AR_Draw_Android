# Remote catalog

Every user's app downloads the catalog from
`https://raw.githubusercontent.com/AllProject789/AR_Draw_Android/main/content/`
(override with the `catalog_base_url` Remote Config key, e.g. a jsDelivr URL). It reads `manifest.json`,
then each image at `<base><path>`. New images appear in the app about 5 minutes after a push; no app update needed.

Only original or commercially licensed art belongs here. See `CONTENT_BRIEF.md` for what to make.

## Adding images

1. Put source images in `content_src/<Category Name>/` (PNG, JPG or WebP; any size). The folder name is the
   category name shown in the app. `content_src/` is gitignored, so originals stay local.
2. Optional: `content_src/categories.txt` with one category name per line sets the chip order.
3. Run:
   ```bash
   python3 tools/build_catalog.py --dry-run   # preview
   python3 tools/build_catalog.py
   ```
   Images are converted to WebP (max 1536 px) into `content/gallery/<category>/` and `manifest.json` is rebuilt.
   Empty folders are skipped, and deleting a source image removes it from the catalog.
4. Commit and push `content/`.

To mark an item premium, rename it, reorder it or hide it, edit its entry in `manifest.json`
(`is_premium`, `name`, `priority`, `available: false`). Re-running the script keeps those edits.

## manifest.json

```json
{
  "version": 3,
  "categories": ["Animals", "Cars"],
  "gallery": [
    { "id": "animals/cat", "name": "Cat", "category": "Animals",
      "is_premium": false, "priority": 0, "path": "gallery/animals/cat.webp" }
  ]
}
```

Optional top-level `lessons` (`id`, `name`, `category`, `level`, `steps_count`, `is_premium`, `cover`) and
`ai_prompts` (`style`, `prompt`, `is_premium`, `path`) arrays are shown in the catalog too.
