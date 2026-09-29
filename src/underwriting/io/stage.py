"""Copy light-tier raw files from Drive to fast local disk, safely and idempotently."""
from __future__ import annotations

import shutil
from pathlib import Path

from .paths import REQUIRED_LIGHT_TIER


def check_required(raw_dir: Path, names=REQUIRED_LIGHT_TIER) -> None:
    missing = [n for n in names if not (raw_dir / n).exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing in {raw_dir}: {missing}. "
            "Add a shortcut to the shared folder in My Drive, or fix raw_drive in configs/paths.yaml."
        )


def stage_light_tier(raw_drive: Path, local_raw: Path, names=REQUIRED_LIGHT_TIER) -> dict:
    """Copy each file via a .part file; skip if a .complete marker matches the source size.
    Never writes to raw_drive. Returns {name: 'copied' | 'cached'}."""
    check_required(raw_drive, names)
    local_raw.mkdir(parents=True, exist_ok=True)
    status = {}
    for name in names:
        src, dst = raw_drive / name, local_raw / name
        marker = Path(str(dst) + ".complete")
        part = Path(str(dst) + ".part")
        size = src.stat().st_size
        if marker.exists() and dst.exists() and marker.read_text().strip() == str(size):
            status[name] = "cached"
            continue
        part.unlink(missing_ok=True)
        shutil.copyfile(src, part)
        part.rename(dst)
        marker.write_text(str(size))
        status[name] = "copied"
    return status
