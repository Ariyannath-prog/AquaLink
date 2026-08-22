# 3D GLB Model Viewer

A static Three.js viewer for GLB models shared from Google Drive. It can be hosted directly on GitHub Pages without a build step.

## Google Drive models

The viewer uses each file's Google Drive ID to create a direct download URL. Every model must be shared as **Anyone with the link > Viewer**. The shared link itself is not used as the loader URL because it opens Google's HTML preview page instead of returning the GLB bytes.

Google Drive may show a confirmation page for very large or flagged files. If that happens, host those files on a static asset host such as GitHub Releases, Cloudflare R2, or an object-storage bucket instead.

## GitHub Pages

1. Push this folder to a GitHub repository.
2. Open **Settings > Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the branch containing `index.html` and the `/ (root)` folder, then save.

The viewer uses relative model paths, so it works for both user sites and project sites such as `https://username.github.io/repository-name/`.

## Local preview

Because browser modules and GLB files are loaded over HTTP, preview with a local server:

```sh
python3 -m http.server 4173
```

Then open `http://localhost:4173/`.
