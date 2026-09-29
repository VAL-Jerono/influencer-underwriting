"""Chunked, memory-safe audit of post_info.txt."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
from statistics import median

import pandas as pd

from underwriting.schemas.post_schema import POST_COLUMNS


def sniff_columns(path: Path, n_lines: int = 5) -> list[str]:
    """Fail clearly if the file does not have the expected number of tab-separated fields."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = [next(f, "") for _ in range(n_lines)]
    lines = [l.rstrip("\n") for l in lines if l.strip()]
    if not lines:
        raise ValueError(f"{path} is empty")
    widths = {len(l.split("\t")) for l in lines}
    if widths != {len(POST_COLUMNS)}:
        raise ValueError(
            f"Expected {len(POST_COLUMNS)} tab-separated fields {POST_COLUMNS}, "
            f"found widths {sorted(widths)}. First line: {lines[0][:200]!r}"
        )
    return lines[:3]


def iter_chunks(path: Path, chunksize: int = 200_000, nrows: int | None = None):
    return pd.read_csv(
        path, sep="\t", header=None, names=POST_COLUMNS, dtype=str,
        quoting=3, keep_default_na=False, chunksize=chunksize, nrows=nrows,
    )


def audit_post_info(path: Path, image_sep: str = ",", positive=("1", "true", "True"),
                    nrows: int | None = None) -> tuple[dict, set, set]:
    """Return (summary dict, json basenames referenced, usernames seen)."""
    raw_head = sniff_columns(path)
    n = 0
    ids_seen: set[str] = set()
    dup_ids = 0
    id_min = id_max = None
    sponsored_values: Counter = Counter()
    per_user: dict[str, list[int]] = {}
    img_counts: Counter = Counter()
    json_names: set[str] = set()
    empty_json = 0

    for chunk in iter_chunks(path, nrows=nrows):
        n += len(chunk)
        sponsored_values.update(chunk["sponsored"].tolist())
        for pid, user, spons, jf, imgs in chunk.itertuples(index=False, name=None):
            if pid in ids_seen:
                dup_ids += 1
            else:
                ids_seen.add(pid)
            if pid.isdigit():
                v = int(pid)
                id_min = v if id_min is None else min(id_min, v)
                id_max = v if id_max is None else max(id_max, v)
            rec = per_user.setdefault(user, [0, 0])
            rec[0 if spons in positive else 1] += 1
            k = 0 if not imgs.strip() else len(imgs.split(image_sep))
            img_counts[min(k, 10)] += 1
            if jf.strip():
                json_names.add(Path(jf).name)
            else:
                empty_json += 1

    n_spons = sum(c for v, c in sponsored_values.items() if v in positive)
    per_creator_posts = [s + o for s, o in per_user.values()]

    def n_with(k: int) -> int:
        return sum(1 for s, o in per_user.values() if s >= k and o >= k)

    summary = {
        "raw_first_lines": raw_head,
        "post_rows": n,
        "duplicate_post_ids": dup_ids,
        "post_id_min": id_min,
        "post_id_max": id_max,
        "sponsored_value_counts": dict(sponsored_values),
        "sponsored_rate": (n_spons / n) if n else None,
        "unique_usernames": len(per_user),
        "median_posts_per_creator": median(per_creator_posts) if per_creator_posts else None,
        "image_count_distribution_capped_at_10": dict(sorted(img_counts.items())),
        "posts_with_empty_json_field": empty_json,
        "gate_creators_5_sponsored_5_organic": n_with(5),
        "gate_creators_3_sponsored_3_organic": n_with(3),
        "creators_with_any_sponsored": sum(1 for s, _ in per_user.values() if s > 0),
    }
    return summary, json_names, set(per_user)
