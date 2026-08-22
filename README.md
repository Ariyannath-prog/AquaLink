# AquaLink 3D Model Viewer

An interactive, static Three.js viewer for the AquaLink GLB models. It is designed to deploy on GitHub Pages without committing the large model binaries to Git.

## How the Google Drive models are published

The model IDs live in [models.json](models.json). The site does **not** load `drive.google.com` URLs directly in the browser: Drive's direct-download endpoint rejects cross-origin browser requests, so a Three.js loader can fail even when a person can open the public sharing link.

Instead, [the Pages workflow](.github/workflows/deploy-pages.yml) downloads the public `Anyone with the link` files from Drive while GitHub builds the site, validates that each result is a complete GLB 2.0 file, and publishes the files at `models/*.glb` beside the viewer. The final browser request is same-origin, which makes the models visible and interactive on GitHub Pages.

Keep every Drive file set to **Anyone with the link → Viewer** and leave downloading enabled. If a file changes, update its Drive ID or filename in `models.json` and push to `main`.

## Deploy to Vercel

Import the repository into Vercel and leave the framework preset as **Other**. The included [vercel.json](vercel.json) downloads and validates the public Drive models during each build, then deploys them as same-origin static assets. No environment variables are required.

Because model files are cached for one year, changing a model requires changing its filename in `models.json` before redeploying so browsers and Vercel do not reuse the old asset.

## Deploy to GitHub Pages

1. Push this project to the `main` branch of its GitHub repository.
2. In **Settings → Pages**, set **Build and deployment → Source** to **GitHub Actions**.
3. Open the **Actions** tab and wait for **Deploy AquaLink to GitHub Pages** to finish.
4. Open the URL shown by that workflow.

The deployed site contains the model bytes, so check that the combined asset size fits your GitHub Pages limits before adding more large models. The workflow fails instead of publishing an HTML error page as a model if Drive access, download quota, or a model file is invalid.

## Local preview

Download the models once (they are ignored by Git), then serve the project over HTTP:

```sh
python3 -m pip install "gdown==5.2.0"
python3 scripts/download_models.py
python3 -m http.server 4173
```

Open `http://localhost:4173/`. Drag to orbit, scroll or pinch to zoom, double-click to reframe, and use the controls for wireframe and auto-rotation.

## Model configuration

`models.json` is the single configuration list for the viewer and deployment downloader. Each item needs:

- `name`: a stable UI identifier
- `label`: the button label
- `file`: the emitted same-origin `.glb` filename
- `driveId`: the ID from the public Google Drive sharing URL

Use filenames containing only letters, numbers, hyphens, and the `.glb` extension.
