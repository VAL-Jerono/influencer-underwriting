import json
import zipfile
from pathlib import Path

import pytest

from underwriting.extraction.audit import build_audit, write_reports
from underwriting.extraction.post_info import sniff_columns
from underwriting.io.paths import Paths
from underwriting.io.stage import check_required, stage_light_tier


def make_raw(d: Path, n_users=3, posts_each=12):
    d.mkdir(parents=True, exist_ok=True)
    rows, jsons = [], {}
    pid = 1
    for u in range(n_users):
        for i in range(posts_each):
            spons = "1" if i < 6 else "0"
            jf = f"{pid}.json"
            rows.append(f"{pid}\tuser{u}\t{spons}\t{jf}\t{pid}_a.jpg,{pid}_b.jpg")
            jsons[jf] = {"caption": "hi", "comments": [{"text": "nice"}]} if i % 2 else {"caption": "hi"}
            pid += 1
    rows.append(f"{pid}\tuser0\t0\tmissing.json\t")  # json absent from archive
    (d / "post_info.txt").write_text("\n".join(rows) + "\n")
    with zipfile.ZipFile(d / "json_files.zip", "w") as z:
        for k, v in jsons.items():
            z.writestr(f"json/{k}", json.dumps(v))
    for name, users in (("profiles_influencers.zip", ["user0", "user1"]), ("profiles_brands.zip", ["brandx"])):
        with zipfile.ZipFile(d / name, "w") as z:
            for u in users:
                z.writestr(f"{u}.json", "{}")


@pytest.fixture
def paths(tmp_path):
    raw = tmp_path / "drive"
    make_raw(raw)
    return Paths(raw_drive=raw, local_raw=tmp_path / "local", artifact_root=tmp_path / "art",
                 checkpoint_root=tmp_path / "ckpt", json_sample_size=20)


def test_stage_is_idempotent_and_never_touches_source(paths):
    before = {p.name: p.stat().st_mtime for p in paths.raw_drive.iterdir()}
    assert set(stage_light_tier(paths.raw_drive, paths.local_raw).values()) == {"copied"}
    assert set(stage_light_tier(paths.raw_drive, paths.local_raw).values()) == {"cached"}
    assert before == {p.name: p.stat().st_mtime for p in paths.raw_drive.iterdir()}


def test_missing_files_fail_clearly(tmp_path):
    with pytest.raises(FileNotFoundError, match="Missing"):
        check_required(tmp_path)


def test_bad_schema_fails_clearly(tmp_path):
    f = tmp_path / "post_info.txt"
    f.write_text("1\tonly\ttwo\n")
    with pytest.raises(ValueError, match="Expected 5"):
        sniff_columns(f)


def test_audit_numbers(paths):
    stage_light_tier(paths.raw_drive, paths.local_raw)
    a = build_audit(paths)
    p = a["posts"]
    assert p["post_rows"] == 37
    assert p["unique_usernames"] == 3
    assert p["duplicate_post_ids"] == 0
    assert p["sponsored_value_counts"] == {"1": 18, "0": 19}
    assert p["gate_creators_5_sponsored_5_organic"] == 3
    assert a["json_coverage"]["found_in_archive"] == 36
    assert a["json_coverage"]["distinct_json_referenced"] == 37
    assert a["profile_coverage"]["influencers"]["usernames_matched_by_filename_stem"] == 2
    assert a["json_layouts"]["parsed"] == 20
    assert 0 < a["json_layouts"]["comment_like_field_nonempty_share"] < 1
    jp, mp = write_reports(a, paths.reports)
    assert json.loads(jp.read_text())["posts"]["post_rows"] == 37
    assert "Raw audit" in mp.read_text()
