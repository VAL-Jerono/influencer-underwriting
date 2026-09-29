"""Stream zip archives without extracting them to disk."""
from __future__ import annotations

import hashlib
import json
import random
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterator


def zip_members(path: Path) -> list[str]:
    """Member names only; does not decompress anything."""
    with zipfile.ZipFile(path) as z:
        return [i.filename for i in z.infolist() if not i.is_dir()]


def iter_json_sample(path: Path, members: list[str], n: int, seed: int = 42) -> Iterator[tuple[str, object]]:
    json_members = [m for m in members if m.lower().endswith(".json")]
    picks = random.Random(seed).sample(json_members, min(n, len(json_members)))
    with zipfile.ZipFile(path) as z:
        for name in picks:
            try:
                with z.open(name) as f:
                    yield name, json.load(f)
            except Exception:  # corrupt member: count it, do not crash the audit
                yield name, None


def field_paths(obj, prefix: str = "", depth: int = 0, max_depth: int = 4) -> dict[str, bool]:
    """Map dotted field path -> whether the value is non-empty. Lists are collapsed to '[]'."""
    out: dict[str, bool] = {}
    if depth > max_depth:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(field_paths(v, f"{prefix}.{k}" if prefix else str(k), depth + 1, max_depth))
    elif isinstance(obj, list):
        out[prefix + "[]"] = len(obj) > 0
        for item in obj[:2]:
            out.update(field_paths(item, prefix + "[]", depth + 1, max_depth))
    else:
        out[prefix] = obj not in (None, "", 0)
    return out


def layout_id(obj) -> str:
    keys = sorted(obj.keys()) if isinstance(obj, dict) else [type(obj).__name__]
    return hashlib.md5("|".join(keys).encode()).hexdigest()[:8]


def summarise_json_sample(path: Path, members: list[str], n: int, seed: int = 42) -> dict:
    layouts: Counter = Counter()
    layout_keys: dict[str, list[str]] = {}
    path_counts: Counter = Counter()
    comment_like_nonempty = 0
    parsed = failed = 0
    for _, obj in iter_json_sample(path, members, n, seed):
        if obj is None:
            failed += 1
            continue
        parsed += 1
        lid = layout_id(obj)
        layouts[lid] += 1
        if isinstance(obj, dict):
            layout_keys.setdefault(lid, sorted(obj.keys())[:40])
        paths = field_paths(obj)
        path_counts.update(p for p, nonempty in paths.items() if nonempty)
        if any("comment" in p.lower() and ne for p, ne in paths.items()):
            comment_like_nonempty += 1
    return {
        "sampled": parsed + failed,
        "parsed": parsed,
        "failed_to_parse": failed,
        "layout_frequencies": {k: v for k, v in layouts.most_common()},
        "layout_top_level_keys": layout_keys,
        "comment_like_field_nonempty_share": (comment_like_nonempty / parsed) if parsed else None,
        "top_field_paths": dict(path_counts.most_common(60)),
        "note": "comment_like is a heuristic: any non-empty field path containing 'comment'. Inspect top_field_paths to confirm.",
    }
