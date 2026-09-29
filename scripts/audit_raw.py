#!/usr/bin/env python
"""Stage light-tier files locally (optional) and write raw_audit.json / raw_audit.md."""
import argparse
import sys

from underwriting.extraction.audit import build_audit, write_reports
from underwriting.io.paths import load_paths
from underwriting.io.stage import stage_light_tier


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None, help="path to paths yaml")
    ap.add_argument("--stage", action="store_true", help="copy raw_drive -> local_raw first")
    ap.add_argument("--rows-limit", type=int, default=None, help="limit post rows (smoke test)")
    args = ap.parse_args()

    paths = load_paths(args.config)
    paths.ensure_dirs()
    print("raw_drive     =", paths.raw_drive)
    print("local_raw     =", paths.local_raw)
    print("artifact_root =", paths.artifact_root)
    if args.stage:
        print("staging:", stage_light_tier(paths.raw_drive, paths.local_raw))
    audit = build_audit(paths, post_rows_limit=args.rows_limit)
    jp, mp = write_reports(audit, paths.reports)
    print("wrote", jp)
    print("wrote", mp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
