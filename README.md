# 3D GLB Model Viewer

A static Three.js viewer for the included GLB models. It can be hosted directly on GitHub Pages without a build step.

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
