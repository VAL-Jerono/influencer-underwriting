"""Single source of truth for where data and artifacts live."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
REQUIRED_LIGHT_TIER = [
    "post_info.txt",
    "json_files.zip",
    "profiles_influencers.zip",
    "profiles_brands.zip",
]


@dataclass(frozen=True)
class Paths:
    raw_drive: Path
    local_raw: Path
    artifact_root: Path
    checkpoint_root: Path
    image_sep: str = ","
    positive_labels: tuple = ("1", "true", "True")
    json_sample_size: int = 1000
    seed: int = 42

    @property
    def reports(self) -> Path:
        return self.artifact_root / "reports"

    @property
    def bronze(self) -> Path:
        return self.artifact_root / "bronze"

    def ensure_dirs(self) -> None:
        for p in (self.local_raw, self.reports, self.bronze,
                  self.artifact_root / "silver", self.checkpoint_root):
            p.mkdir(parents=True, exist_ok=True)


def load_paths(config: str | Path | None = None) -> Paths:
    """Load configs/paths.yaml, falling back to paths.example.yaml."""
    if config is None:
        cfg_dir = REPO_ROOT / "configs"
        config = cfg_dir / "paths.yaml"
        if not config.exists():
            config = cfg_dir / "paths.example.yaml"
    cfg = yaml.safe_load(Path(config).read_text())
    pi, au = cfg.get("post_info", {}), cfg.get("audit", {})
    return Paths(
        raw_drive=Path(cfg["raw_drive"]),
        local_raw=Path(cfg["local_raw"]),
        artifact_root=Path(cfg["artifact_root"]),
        checkpoint_root=Path(cfg["checkpoint_root"]),
        image_sep=pi.get("image_sep", ","),
        positive_labels=tuple(pi.get("positive_labels", ["1", "true", "True"])),
        json_sample_size=au.get("json_sample_size", 1000),
        seed=au.get("seed", 42),
    )
