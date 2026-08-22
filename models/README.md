# Downloaded model assets

GLB files are intentionally not committed to this repository. They are downloaded from the public Google Drive links in `../models.json` during the GitHub Pages deployment.

For a local preview with the real models, install `gdown` and run:

```sh
python3 -m pip install "gdown==5.2.0"
python3 scripts/download_models.py
```
