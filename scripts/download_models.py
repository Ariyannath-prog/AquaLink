#!/usr/bin/env python3
"""Download the public Drive models used by the AquaLink static viewer."""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any


GLB_FILE_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*\.glb$", re.IGNORECASE)
DRIVE_ID = re.compile(r"^[a-zA-Z0-9_-]{20,}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("models.json"),
        help="Path to the JSON model manifest (default: models.json).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("models"),
        help="Directory that receives the downloaded GLB files (default: models).",
    )
    return parser.parse_args()


def read_manifest(path: Path) -> list[dict[str, str]]:
    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to read {path}: {error}") from error

    if not isinstance(data, list) or not data:
        raise ValueError("The model manifest must contain at least one model.")

    models: list[dict[str, str]] = []
    names: set[str] = set()
    files: set[str] = set()
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Every model manifest entry must be an object.")

        name = item.get("name")
        label = item.get("label")
        file_name = item.get("file")
        drive_id = item.get("driveId")
        if not all(isinstance(value, str) and value for value in (name, label, file_name, drive_id)):
            raise ValueError("Every model needs name, label, file, and driveId strings.")

        if not GLB_FILE_NAME.fullmatch(file_name):
            raise ValueError(f"Invalid GLB filename in manifest: {file_name}")
        if not DRIVE_ID.fullmatch(drive_id):
            raise ValueError(f"Invalid Google Drive ID in manifest: {drive_id}")
        if name in names or file_name in files:
            raise ValueError(f"Duplicate model name or filename in manifest: {name}")

        names.add(name)
        files.add(file_name)
        models.append(
            {"name": name, "label": label, "file": file_name, "driveId": drive_id}
        )

    return models


def validate_glb(path: Path) -> int:
    size = path.stat().st_size
    with path.open("rb") as file_handle:
        header = file_handle.read(12)

    if len(header) != 12:
        raise ValueError(f"{path} is too small to be a GLB file.")

    magic, version, declared_size = struct.unpack("<4sII", header)
    if magic != b"glTF" or version != 2:
        raise ValueError(f"{path} is not a binary glTF 2.0 file.")
    if declared_size != size:
        raise ValueError(
            f"{path} is incomplete (GLB header says {declared_size:,} bytes; found {size:,})."
        )

    return size


def download_models(models: list[dict[str, str]], output_dir: Path) -> None:
    try:
        import gdown
    except ImportError as error:
        raise RuntimeError(
            "Missing dependency: install it with `python3 -m pip install gdown==5.2.0`."
        ) from error

    output_dir.mkdir(parents=True, exist_ok=True)
    for model in models:
        output_path = output_dir / model["file"]
        source_url = f"https://drive.google.com/file/d/{model['driveId']}/view?usp=sharing"
        print(f"Downloading {model['label']}…")
        result = gdown.download(source_url, str(output_path), quiet=False, fuzzy=True)
        if result is None:
            raise RuntimeError(f"Google Drive did not download {model['label']}.")

        size = validate_glb(output_path)
        print(f"Validated {output_path} ({size / 1024 / 1024:.1f} MiB)")


def main() -> int:
    args = parse_args()
    try:
        download_models(read_manifest(args.manifest), args.output_dir)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Model download failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
