"""Assemble the raw audit manifest and write raw_audit.json / raw_audit.md."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from underwriting.io.paths import REQUIRED_LIGHT_TIER, Paths
from .json_stream import summarise_json_sample, zip_members
from .post_info import audit_post_info


def _profile_coverage(zip_path: Path, usernames: set) -> dict:
    members = zip_members(zip_path)
    stems = {Path(m).stem for m in members}
    return {
        "archive_members": len(members),
        "example_members": members[:5],
        "usernames_matched_by_filename_stem": len(usernames & stems),
        "note": "Heuristic: assumes profile files are named <username>.json. Check example_members.",
    }


def build_audit(paths: Paths, post_rows_limit: int | None = None) -> dict:
    raw = paths.local_raw
    files = {n: {"bytes": (raw / n).stat().st_size} for n in REQUIRED_LIGHT_TIER}

    posts, json_names, usernames = audit_post_info(
        raw / "post_info.txt", image_sep=paths.image_sep,
        positive=paths.positive_labels, nrows=post_rows_limit,
    )

    json_members = zip_members(raw / "json_files.zip")
    member_basenames = {Path(m).name for m in json_members}
    files["json_files.zip"]["members"] = len(json_members)
    matched = len(json_names & member_basenames)

    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "post_rows_limit": post_rows_limit,
        "files": files,
        "posts": posts,
        "json_coverage": {
            "distinct_json_referenced": len(json_names),
            "found_in_archive": matched,
            "share_found": (matched / len(json_names)) if json_names else None,
        },
        "profile_coverage": {
            "influencers": _profile_coverage(raw / "profiles_influencers.zip", usernames),
            "brands": _profile_coverage(raw / "profiles_brands.zip", usernames),
            "distinct_post_usernames": len(usernames),
        },
        "json_layouts": summarise_json_sample(
            raw / "json_files.zip", json_members, paths.json_sample_size, paths.seed),
    }


def render_markdown(a: dict) -> str:
    p, j, L = a["posts"], a["json_coverage"], a["json_layouts"]
    rate = p["sponsored_rate"]
    lines = [
        "# Raw audit", f"Generated: {a['generated_utc']} (post rows limit: {a['post_rows_limit']})", "",
        "## Posts",
        f"- rows: {p['post_rows']:,}  | duplicate post IDs: {p['duplicate_post_ids']:,}",
        f"- post ID range: {p['post_id_min']} to {p['post_id_max']}",
        f"- sponsored value counts: {p['sponsored_value_counts']}",
        f"- sponsored rate: {rate:.2%}" if rate is not None else "- sponsored rate: n/a",
        f"- unique usernames: {p['unique_usernames']:,}  | median posts per creator: {p['median_posts_per_creator']}",
        f"- image count distribution (capped at 10): {p['image_count_distribution_capped_at_10']}",
        "", "## Gates",
        f"- creators with >=5 sponsored and >=5 organic: {p['gate_creators_5_sponsored_5_organic']:,}",
        f"- creators with >=3 sponsored and >=3 organic: {p['gate_creators_3_sponsored_3_organic']:,}",
        f"- creators with any sponsored post: {p['creators_with_any_sponsored']:,}",
        f"- JSON layouts in sample of {L['sampled']}: {L['layout_frequencies']}",
        f"- comment-like field non-empty share (heuristic): {L['comment_like_field_nonempty_share']}",
        "", "## Coverage",
        f"- JSON referenced and found in archive: {j['found_in_archive']:,} / {j['distinct_json_referenced']:,} ({j['share_found']})",
        f"- influencer profile matches (filename stem heuristic): {a['profile_coverage']['influencers']['usernames_matched_by_filename_stem']:,}"
        f" of {a['profile_coverage']['distinct_post_usernames']:,} usernames",
        f"- brand profile archive members: {a['profile_coverage']['brands']['archive_members']:,}",
        "", "## Verify by eye before trusting",
        f"- raw first lines of post_info.txt: {p['raw_first_lines']}",
        f"- influencer archive example members: {a['profile_coverage']['influencers']['example_members']}",
        "- Confirm the image separator, the sponsored encoding, and the profile file naming against these samples.",
    ]
    return "\n".join(lines) + "\n"


def write_reports(audit: dict, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    jp, mp = out_dir / "raw_audit.json", out_dir / "raw_audit.md"
    jp.write_text(json.dumps(audit, indent=2, default=str))
    mp.write_text(render_markdown(audit))
    return jp, mp
