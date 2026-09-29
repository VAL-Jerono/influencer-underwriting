# influencer-underwriting

Decision-intelligence pipeline for underwriting Instagram influencers for brand campaigns.
DSA 8401 Applied Machine Learning capstone.

## Principle
A notebook is not a system. Logic lives in `src/` and `scripts/`; notebooks only call it and show results.

| Where | Role |
|---|---|
| GitHub (this repo) | code, config, tests, docs. Never data. |
| Drive `Influencer brand dataset` | immutable raw source (read-only) |
| Drive `InfluencerUnderwriting/artifacts` | durable Parquet, reports, models |
| Colab `/content` | temporary fast compute |

## Phase 0 (current)
1. Stage the four light-tier files (post_info.txt, json_files.zip, profiles_influencers.zip, profiles_brands.zip). Images are not touched.
2. Run the raw audit -> `artifacts/reports/raw_audit.json` and `raw_audit.md`.
3. Review the three gates (rich-layout/comment coverage, creators with >=5 sponsored and >=5 organic posts, vertical coverage) before any modeling.

## Run locally (tests only, no real data)
    pip install -e ".[dev]"
    pytest -q

## Run on Colab
Open `notebooks/01_audit_report.ipynb`, or:

    !python scripts/audit_raw.py --stage

Config: copy `configs/paths.example.yaml` to `configs/paths.yaml` if your Drive paths differ.

## Layout
    src/underwriting/io          paths and safe staging
    src/underwriting/extraction  chunked post_info audit, zip streaming, audit report
    src/underwriting/schemas     column contracts
    scripts/audit_raw.py         CLI entry point
    notebooks/                   thin orchestration only
    tests/                       synthetic-data tests (run in CI)
