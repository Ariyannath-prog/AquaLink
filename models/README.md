# Downloaded model assets

GLB files are intentionally not committed to this repository. The shared deployment build downloads them from the public Google Drive links in `../models.json`, validates them, and writes them to `dist/models/` for Vercel or `_site/models/` for GitHub Pages.

For a local preview with the real models, build the static artifact:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build_site.py
```
