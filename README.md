# AquaLink 3D Model Viewer

An interactive, static Three.js viewer for AquaLink GLB models. It deploys as a small HTML application plus same-origin model assets, without committing the large binaries to Git.

## Model delivery architecture

[models.json](models.json) is the source manifest. Google Drive is used only during a deployment build; the browser never loads a Drive download URL directly. The shared build script:

1. Downloads each public `Anyone with the link → Viewer` Drive file.
2. Validates that it is a complete GLB 2.0 binary.
3. Adds a content hash to its deployed filename.
4. Produces a minimal static artifact containing only `index.html`, `models.json`, and `models/*.glb`.

The viewer therefore requests same-origin assets on either Vercel or GitHub Pages. Content-hashed model URLs may be cached for a year without serving stale models after a Drive file is replaced.

Keep Drive downloading enabled. A failed download, quota issue, or invalid file fails the deployment rather than publishing an HTML error page as a model.

## Deploy to Vercel

1. Push the latest commit to the branch connected to Vercel.
2. Import the repository with the project root set to this repository. `vercel.json` explicitly selects the static/Other preset, runs the build, and deploys `dist/`.
3. Do not override the build command or output directory in the dashboard. No environment variables are required.

The Vercel build log should end with `Built ... with 7 validated models`. The deployment exposes only the contents of `dist/`, so source scripts and workflow files do not become public static files.

Vercel caches each fingerprinted GLB for one year and revalidates `models.json` on every visit. On the next deployment, a changed model gets a new URL automatically; you do not need to rename `file` in the source manifest.

The current model set is about 572 MiB in total, so each build downloads a substantial amount of data. This is suitable as a short-term Drive ingestion path. For a high-traffic production deployment, compress the models (Draco/Meshopt and texture compression) and move them to a dedicated object store/CDN such as Vercel Blob, R2, or S3.

## Deploy to GitHub Pages

1. Push this project to the `main` branch of its GitHub repository.
2. In **Settings → Pages**, set **Build and deployment → Source** to **GitHub Actions**.
3. Open the **Actions** tab and wait for **Deploy AquaLink to GitHub Pages** to finish.
4. Open the URL shown by that workflow.

The workflow invokes the same static builder as Vercel, so it has the same same-origin asset behavior and validation.

## Local preview

Build the deployable artifact, then serve it over HTTP:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build_site.py
python3 -m http.server 4173 --directory dist
```

Open `http://localhost:4173/`. Drag to orbit, scroll or pinch to zoom, double-click to reframe, and use the controls for wireframe and auto-rotation.

## Model configuration

`models.json` is the source configuration list for the viewer and deployment downloader. Each item needs:

- `name`: a stable UI identifier
- `label`: the button label
- `file`: a stable source `.glb` filename; the build appends the deployed content hash
- `driveId`: the ID from the public Google Drive sharing URL

Use filenames containing only letters, numbers, hyphens, and the `.glb` extension.
