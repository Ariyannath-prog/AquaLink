#!/usr/bin/env python3
"""Build the minimal static AquaLink artifact for Vercel or GitHub Pages."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

from download_models import download_models, read_manifest, validate_glb


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "dist"
ALLOWED_OUTPUT_DIRS = {
    DEFAULT_OUTPUT_DIR,
    PROJECT_ROOT / "_site",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory that receives the deployable static site (default: dist).",
    )
    return parser.parse_args()


def prepare_output_dir(output_dir: Path) -> Path:
    resolved_output = output_dir.resolve()
    if resolved_output not in ALLOWED_OUTPUT_DIRS:
        allowed = ", ".join(str(path) for path in sorted(ALLOWED_OUTPUT_DIRS, key=str))
        raise ValueError(f"Build output must be one of: {allowed}")

    if resolved_output.exists():
        if not resolved_output.is_dir():
            raise ValueError(f"Build output exists but is not a directory: {resolved_output}")
        shutil.rmtree(resolved_output)
    resolved_output.mkdir(parents=True)
    return resolved_output


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint_models(models: list[dict[str, str]], model_dir: Path) -> tuple[list[dict[str, str]], int]:
    deployed_models: list[dict[str, str]] = []
    total_size = 0

    for model in models:
        downloaded_path = model_dir / model["file"]
        size = validate_glb(downloaded_path)
        fingerprint = sha256_file(downloaded_path)[:12]
        fingerprinted_file = f"{Path(model['file']).stem}-{fingerprint}.glb"
        fingerprinted_path = model_dir / fingerprinted_file
        if fingerprinted_path.exists() and fingerprinted_path != downloaded_path:
            raise ValueError(f"Fingerprint collision for model output: {fingerprinted_file}")
        downloaded_path.replace(fingerprinted_path)

        deployed_model = dict(model)
        deployed_model["file"] = fingerprinted_file
        deployed_models.append(deployed_model)
        total_size += size

    return deployed_models, total_size


def build_site(output_dir: Path) -> None:
    output_dir = prepare_output_dir(output_dir)
    shutil.copy2(PROJECT_ROOT / "index.html", output_dir / "index.html")

    models = read_manifest(PROJECT_ROOT / "models.json")
    model_dir = output_dir / "models"
    download_models(models, model_dir)
    deployed_models, total_size = fingerprint_models(models, model_dir)

    (output_dir / "models.json").write_text(
        json.dumps(deployed_models, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Built {output_dir} with {len(deployed_models)} validated models "
        f"({total_size / 1024 / 1024:.1f} MiB)."
    )


def main() -> int:
    try:
        build_site(parse_args().output_dir)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Site build failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
