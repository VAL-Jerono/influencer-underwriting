# Influencer Underwriting — Capstone Master Plan

**Course:** DSA 8401 Applied Machine Learning · Strathmore University  
**Author:** Valerie Jerono  
**Presentation deadline:** 2 November 2026  
**Repo:** `VAL-Jerono/influencer-underwriting`  
**Principle:** A notebook is not a system. Logic lives in `src/` and `scripts/`. Notebooks call it and show results.

---

## 1. The data — what it is, where it comes from, what it contains

### 1.1 Provenance and realness

This project uses the **Kim et al. Instagram Influencer Dataset**, published at WWW 2020.

> *Multimodal Post Attentive Profiling for Influencer Marketing*, Seungbae Kim et al., The Web Conference 2020. [ACM DL](https://dl.acm.org/doi/fullHtml/10.1145/3366423.3380052)

**This is real, empirical, platform-collected data. It is not synthetic.**

The collection procedure, as described in the peer-reviewed paper:
- Researchers queried Instagram posts containing `#ad` over 92 days: **1 October 2018 → 1 January 2019**
- Obtained 828,045 posts from 107,656 candidate users
- Retained users with **≥ 1,000 followers AND ≥ 300 posts**
- Downloaded the **300 most recent posts** for each retained influencer
- Final corpus: **33,935 influencers · 10,180,500 posts**

The dataset has been independently used by subsequent peer-reviewed research: InfluencerRank (arXiv 2023), Springer fashion influencer study (2024), bot-detection work (ECML 2020), audience loyalty study (ICWSM 2021).

**What this data is and is not:**

| It IS | It IS NOT |
|---|---|
| Real Instagram observations | A random sample of Instagram |
| Verified through peer-reviewed publication | Representative of all influencers |
| Suitable for ML benchmarking and historical analysis | Evidence of current Instagram behavior |
| Defensible for disclosure, engagement, and niche research | Evidence of sales, conversions, or causal campaign lift |

**Important label caveat:** The 8–9 influencer category labels were produced by a pipeline — LDA topic modeling on bios → manual labeling of 1,600 training accounts → classifier applied across the corpus. They are **operational annotations, not platform-native facts.**

**Recommended wording for any written report:**
> "We analyze the Kim et al. Instagram Influencer Dataset, a controlled-access historical snapshot collected from public Instagram activity. The source study identified candidate accounts through posts containing `#ad` during 1 October 2018–1 January 2019, retained accounts meeting follower and posting-activity thresholds, and collected 300 recent posts per retained account. We treat the data as a purposive observational sample of advertising-active, high-activity Instagram accounts rather than a representative sample of Instagram users. Influencer categories are treated as derived labels produced through the source study's topic-modeling, manual-annotation, and classifier pipeline."

**Access and ethics:** Dataset access is via a request form requiring institutional affiliation and research/education use declaration. Raw data must not be redistributed. IRB/ethics review or exemption must be confirmed with Strathmore University before publication.

---

### 1.2 What the dataset actually contains (verified from our real audit)

Our audit ran on the actual files. These numbers are measured, not estimated.

#### Scale facts

| Metric | Value |
|---|---|
| Total posts | **1,601,074** |
| Post ID range | 0 → 1,601,073 (contiguous, zero gaps) |
| Duplicate post IDs | **0** |
| Unique posting users | **38,113** |
| Influencer profile files | **38,113** (perfect 1-to-1 match) |
| Duplicate JSON filenames | **0** |
| Organic posts | 1,379,364 |
| Sponsored posts | **221,710** |
| Sponsored rate | **13.85%** |

#### Sponsorship leakage (measured in our 600-post sample)

| Check | Result |
|---|---|
| Labeled sponsored posts containing a disclosure hashtag | ~97.3% |
| Labeled organic posts also containing a disclosure hashtag | ~3.0% |

This is the leakage problem. We handle it with two explicit tasks (A and B).

#### Creator profile distribution

| Metric | Value |
|---|---|
| Median followers | ~14,641 |
| 75th percentile followers | ~48,084 |
| Maximum followers | ~119,000,000 |
| Median posts per creator | ~24 |

#### Category distribution

| Category | Count |
|---|---|
| Creators & Celebrities | 24,487 |
| NULL / missing | **6,017** |
| Publishers | 1,830 |
| Personal Goods & General Merchandise | 1,510 |
| Restaurants | 51 |
| Auto Dealers | 30 |

The 6,017 NULL and 24,487 "Creators & Celebrities" accounts are the core challenge — profile labels alone cannot support niche matching.

#### Files on Google Drive

| File | Contents | Size |
|---|---|---|
| `post_info.txt` | 1.6M rows: post_id, username, sponsored, json_file, image_files | ~200 MB |
| `json_files.zip` | Per-post JSON: caption, likes, comments, timestamp, usertags | ~3 GB |
| `profiles_influencers.zip` | 38,113 influencer profile JSON files | large |
| `profiles_brands.zip` | Up to 26,910 brand profiles (1,628 unavailable) | varies |
| `img_fi01.zip` → `img_fi16.zip` | JPEG images | **~189 GB** |
| `sample_images.zip` | Small image sample (one family influencer only) | small |

---

## 2. The system — objective, decision, and framing

### 2.1 The stakeholder and the question

**Stakeholder:** A marketing agency assigning Instagram influencers to client campaigns.

**Clients:** kitchen-appliance retailers · restaurants · software companies · automobile sellers · fashion and beauty businesses.

**The agency's question:**
> Given a client, their product category, campaign objective, desired audience, timing, and risk tolerance — which influencers should we assign, why, and with what expected level of potential buyer exposure?

### 2.2 What we can and cannot claim

| We can estimate | We cannot claim |
|---|---|
| Which creators produce relevant, high-quality engagement in a given niche | Actual sales, conversions, or ROAS |
| Commercial behavior patterns and disclosure practices | Audience demographics — follower counts ≠ audience quality |
| A ranked shortlist with grounded explanations | Causal effects — data is observational |
| Risk signals for brand safety and content review | Current Instagram behavior — data is from 2018–2019 |

**The defensible target:**
> **Expected Qualified Engagement Exposure (EQEE):** an estimate of the potential for relevant, visible engagement from a creator's audience. A transparent proxy — not actual viewers, not buyers, not revenue. Reported with uncertainty and evidence count.

### 2.3 The underwriting metaphor

Underwriting = structured decision under uncertainty using available evidence.

- **Application:** client submits a campaign brief (product, niche, objective, timing, risk)
- **Dossier:** the system builds an evidence dossier for each creator
- **Decision output:** Recommended · Conditionally Recommended · Monitor/Review · Not Recommended
- **Explanation:** why this creator was selected, which evidence supports it, which risks reduce the score, where the model is uncertain

This is a **decision-support platform**, not an autonomous contracting system. A human agent makes the final call.

---

## 3. Architecture

### 3.1 Full data flow

```
Google Drive / raw (read-only, immutable)
    post_info.txt · json_files.zip · profiles_*.zip · img_fi*.zip
        │
        ▼
scripts/extract_metadata.py   [Colab CPU — run once, checkpointed]
        │
        ▼
Drive / artifacts / bronze/
    posts_metadata.parquet        one row per post, all JSON fields flattened
    profiles_influencers.parquet
    profiles_brands.parquet
    post_image_index.parquet      post_id → image_filename mapping
        │
        ▼
scripts/build_features.py   [DuckDB queries over Parquet — no RAM pressure]
        │
        ▼
Drive / artifacts / silver/
    creator_features.parquet      one row per creator, all aggregates
    posts_features.parquet        one row per post, text + engagement + commercial
    creator_brand_edges.parquet   bipartite graph edges
        │
        ┌─────────────────────────────────────┐
        ▼                                     ▼
[Gemini API — caption embeddings]   [Gemini Vision — image labels on 5K sample]
Drive / artifacts / embeddings/
    text/caption_embeddings.parquet        post_id · 768-dim · model_version
    image/gemini_vision_labels.parquet     post_id · structured labels
        │
        ▼
src/underwriting/models/   [Colab GPU — artifacts saved to Drive]
    sponsorship_classifier.py
    engagement_model.py
    niche_classifier.py
    anomaly_model.py
        │
        ▼
src/underwriting/scoring.py
    UnderwritingScore(i, c, t) — weighted combination of all model outputs
        │
        ▼
src/underwriting/api/   [FastAPI + Docker]
    POST /score   {brief, campaign_params}
    → ranked shortlist + score cards + Gemini explanation
        │
        ▼
Monitoring   [Evidently AI — HTML reports on Drive/reports/monitoring/]
```

### 3.2 Repository layout (target state)

```
influencer-underwriting/
├── README.md                         project page with badges + architecture
├── DECISIONS.md                      log of every non-trivial engineering decision
├── CHANGELOG.md                      milestone entries
├── CONTRIBUTING.md                   branch model, commit convention
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── configs/
│   ├── paths.example.yaml
│   ├── paths.yaml                    git-ignored
│   ├── features.yaml
│   ├── models.yaml
│   └── campaigns.yaml
├── src/underwriting/
│   ├── io/
│   │   ├── paths.py                  EXISTS
│   │   ├── stage.py                  EXISTS
│   │   ├── gemini.py                 Gemini client: embed + parse brief + explain
│   │   └── duckdb_utils.py           DuckDB helpers over Parquet
│   ├── schemas/
│   │   ├── post_schema.py            EXISTS
│   │   ├── profile_schema.py
│   │   └── feature_schema.py
│   ├── extraction/
│   │   ├── audit.py                  EXISTS
│   │   ├── post_info.py              EXISTS
│   │   ├── json_stream.py            EXISTS
│   │   ├── json_extractor.py         full 1.6M streaming extraction → Parquet
│   │   └── profile_extractor.py
│   ├── features/
│   │   ├── engagement.py
│   │   ├── commercial.py
│   │   ├── temporal.py
│   │   ├── profile.py
│   │   └── text.py
│   ├── models/
│   │   ├── sponsorship_classifier.py Task A + Task B
│   │   ├── engagement_model.py       Task C
│   │   ├── niche_classifier.py       Task D
│   │   └── anomaly_model.py
│   ├── evaluation/
│   │   ├── metrics.py
│   │   ├── splits.py
│   │   └── leakage_experiment.py     4-variant sponsorship experiment
│   ├── scoring.py                    UnderwritingScore(i, c, t)
│   ├── monitoring/
│   │   └── drift_report.py           Evidently AI wrapper
│   └── api/
│       ├── main.py                   FastAPI app
│       ├── schemas.py                Pydantic models
│       └── brief_parser.py           Gemini Flash brief → structured filters
├── scripts/
│   ├── audit_raw.py                  EXISTS
│   ├── extract_metadata.py           bronze Parquet from raw archives
│   ├── build_features.py             silver features from bronze via DuckDB
│   ├── embed_captions.py             Gemini caption embeddings, cached
│   ├── embed_images.py               Gemini Vision labels on stratified sample
│   ├── train_models.py               all training with MLflow logging
│   ├── evaluate.py                   full evaluation suite
│   ├── score_influencer.py           CLI: --brief "..." --top_k 10
│   └── monitor.py                    drift report generation
├── notebooks/
│   ├── 01_audit_report.ipynb         EXISTS, ran on real data
│   ├── 02_eda.ipynb
│   ├── 03_baseline_models.ipynb
│   ├── 04_unsupervised.ipynb
│   ├── 05_deep_multimodal.ipynb
│   ├── 06_scoring_and_rag.ipynb
│   └── 07_demo.ipynb                 live demo for presentation
├── tests/
│   ├── test_smoke.py                 EXISTS
│   ├── test_features.py
│   ├── test_models.py
│   └── test_api.py
└── docs/
    ├── CAPSTONE_MASTER_PLAN.md       this file
    ├── data_dictionary.md
    ├── model_card.md
    ├── data_card.md
    └── DECISIONS.md
```

---

## 4. The five ML tasks — what, why, and how

### Task A — Sponsored Post Disclosure Detector

**What:** Binary classifier. Given a post's text features, metadata, and profile context — is this post sponsored?

**Why it has a trap:** 97.3% of labeled sponsored posts contain `#ad`, `#sponsored`, or `#paidpartnership`. A model detecting these tokens achieves near-perfect performance on training distribution but has learned a rule, not commercial understanding. We report this explicitly.

**The leakage experiment — 4 variants, all reported:**

| Variant | Input | Purpose |
|---|---|---|
| 1 — Full text | Complete caption + metadata | Establishes the ceiling and confirms leakage magnitude |
| 2 — Disclosure tokens masked | `#ad`, `#sponsored`, `#paidpartnership` stripped | The model that matters for real compliance |
| 3 — Text only, no metadata | Caption text only | Isolates text contribution |
| 4 — Metadata only, no text | Follower tier, category, cadence, image count | Structural sponsorship signal |

**Models (in build order):**
1. Keyword rule baseline — sets the leakage ceiling
2. Logistic regression + TF-IDF
3. LightGBM + handcrafted features
4. LightGBM + Gemini caption embeddings
5. Masked-token version of best model — the scientifically meaningful result

**Evaluation:**
- **Primary metric: PR-AUC** (86% accuracy baseline exists by predicting "organic" always — never report accuracy here)
- Also: Precision · Recall · F1 · ROC-AUC · calibration error · confusion matrix
- Splits: creator-held-out AND time-held-out
- Subgroup analysis: by follower tier · by creator category

---

### Task B — Commercial Intent Beyond Disclosure

**What:** Same binary target as Task A but the model must operate on captions with disclosure tokens removed. Find commercial intent in product language, caption structure, and call-to-action patterns.

**Why:** A disclosure monitor is a rule system. A commercial-intent detector is real ML. This also has practical value: undisclosed advertising exists. Flagging it for human review is a compliance use case.

**Key result to report:** The difference in PR-AUC between Task A variant 1 (disclosure present) and Task B (disclosure masked) is the leakage magnitude finding. This turns a potential weakness into the central analytical result.

---

### Task C — Engagement Quality Model

**What:** Regression model. Predict expected log-normalized engagement relative to creator baseline.

**Why NOT raw engagement:** Raw likes reward large accounts. The agency needs creator-normalized, campaign-relevant engagement quality — not absolute counts.

**Target design:**
```
creator_relative_log_engagement =
    log(1 + observed_engagement) − log(1 + creator_median_engagement)
```

**Models (in build order):**
1. Follower-count-only baseline — must beat this to justify the model
2. Creator-median baseline — simplest contextual predictor
3. Linear regression on engagement features
4. Quantile regression — produces prediction intervals, not just point estimates
5. LightGBM on full feature set + Gemini embeddings

**Evaluation:**
- Spearman rank correlation (ranking quality matters more than absolute error)
- MAE on log-transformed engagement
- NDCG@K
- Prediction interval coverage (does the 90% interval contain 90% of outcomes?)
- Performance by follower tier and category (fairness check)

---

### Task D — Creator Niche Classifier

**What:** Multi-class probabilistic classifier. Given a creator's bio, caption topic distribution, hashtag patterns, and Gemini embeddings — assign soft probabilities across 9 niches + NULL class.

**Why:** The profile category is insufficient. 6,017 NULL creators. 24,487 "Creators & Celebrities" accounts (too broad). Content evidence fills the gap.

**Key design choices:**
- **Output: soft probabilities, not hard labels.** A food creator who sometimes posts interior content carries meaningful probability on both classes.
- **NULL is a class, not a missing value.** Genuinely unclear creators get high probability on NULL. We do not impute a niche where evidence is absent.
- **Creator-held-out evaluation only.** Random post split allows memorizing creator-specific language.

**Models:**
1. Profile bio TF-IDF → logistic regression (baseline)
2. Caption hashtag distribution → multinomial Naive Bayes (baseline)
3. Gemini caption embedding centroid → softmax layer (rich representation)
4. Ablation: bio-only vs. caption-only vs. combined

**Evaluation:**
- Macro-F1 (penalizes poor performance on minority classes: Pet, Restaurant, Auto Dealers)
- Calibration by class
- Confusion matrix heatmap (which niches are confused?)

---

### Task E — Creator Segmentation (Unsupervised)

**What:** Cluster creators into behavioral types using aggregate feature profiles. No labels used.

**Why:** Labels cover 9 broad categories. The real landscape has behavioral segments labels miss: high-volume low-engagement publishers · niche micro-influencers with high comment rates · brand-heavy commercial accounts · community builders. These are actionable for campaign planning.

**Method:**
1. Build standardized creator feature matrix (engagement aggregates, posting cadence, sponsorship rate, follower tier, niche probabilities from Task D)
2. PCA → explained variance plot
3. UMAP → 2D visualization
4. K-means (k by silhouette score) + HDBSCAN (density-based, handles noise)
5. Isolation Forest on same features → anomaly/suspicious engagement score

**Validation:** clusters are modeling choices, not natural facts. We inspect representative creators per cluster manually and confirm segments are useful for downstream ranking.

**Deliverable:** Creator Segment Map — labeled 2D UMAP scatter plot with cluster descriptions. This is a live demo visual.

---

## 5. Image data — what it tells and how we use it

### What images can tell that text cannot

| Signal in image | What it reveals | Role in system |
|---|---|---|
| Food / kitchens | Food/home creator — even if bio is blank or NULL | Supplements niche classifier for NULL-category accounts |
| Product packaging and brand logos | Commercial content without `#ad` in caption | Task B — undisclosed commercial intent |
| Cars and vehicles | Automotive niche | Bridges the 30-account Auto Dealer category gap |
| App/screen/UI visible | Tech and productivity creator | Software client matching |
| Faces and people count | Personal/lifestyle vs. product/object content | Authenticity vs. catalogue signal |
| Indoor home scenes | Interior / home-goods niche | Kitchen-appliance and furniture clients |
| Number of carousel images | Content production investment | Feature: `n_images` — already in post_info.txt |
| Image quality / editing style | Professional vs. amateur aesthetic | Brand safety for premium clients |

### The three-layer image strategy

**Layer 1 — Free, no images needed (built now)**  
`n_images` = count of filenames in `image_files` column.  
Already extractable from `post_info.txt`. Zero additional cost.

**Layer 2 — Gemini Vision on a stratified 5K sample (student plan, one API session)**  
Stratified across: all 9 categories · sponsored vs. organic · follower tiers.  
Structured JSON output per image: scene type · product visible · brand logo · face count · image quality · OCR text present.  
Saved to `embeddings/image/gemini_vision_labels.parquet`. Never re-processed.

**Layer 3 — CLIP embeddings on same sample (one GPU session)**  
`openai/clip-vit-base-patch32` (Hugging Face, free) → 512-dim visual embeddings.  
Saved to `embeddings/image/clip_sample.parquet`.  
Enables visual similarity search — "find creators whose visual style matches this mood board." Live demo moment.

**Why a sample, not the full 189 GB:**  
Documented in `DECISIONS.md`:  
> "Image pipeline scoped to a stratified 5K sample to: (a) demonstrate value before full-scale investment, (b) produce an ablation result — text-only vs. text+image PR-AUC comparison, (c) remain within free-tier compute constraints. This is both practically necessary and academically stronger."

**The ablation:** running models with and without image features lets us report the marginal contribution of images quantitatively. That is a publishable finding.

---

## 6. Full tool stack and real costs

| Tool | Role | Cost |
|---|---|---|
| **Google Drive** | Immutable raw source + durable Parquet artifacts + model checkpoints | Free (15 GB; dataset via external access grant) |
| **Google Colab** | CPU: extraction, DuckDB queries, classical ML. GPU: embedding extraction, deep models | Free tier. All outputs saved to Drive before session ends. |
| **DuckDB** | SQL over Parquet without loading into RAM. 1.6M posts in seconds. | Free. Python library, no server. |
| **PyArrow / Parquet + Zstd** | Columnar storage for bronze and silver tables | Free. |
| **Gemini API** (student plan) | `text-embedding-004` (768-dim caption embeddings) · Gemini Flash (brief parser) · Gemini 1.5 Pro Vision (image labels on sample) · Gemini Flash (RAG explanations) | Free tier via Google AI Studio. Rate limits managed with exponential backoff. **All embeddings cached — API called once per post, maximum.** |
| **CLIP** (`openai/clip-vit-base-patch32`) | 512-dim visual embeddings on stratified image sample | Free. Hugging Face. Runs on Colab GPU. |
| **scikit-learn** | Logistic regression, cross-validation, calibration, isolation forest, metrics | Free. |
| **LightGBM** | Gradient boosting for sponsorship classifier and engagement model | Free. |
| **Optuna** | Hyperparameter optimization for LightGBM | Free. |
| **MLflow** (local file backend) | Experiment tracking — logs to Drive artifact dir, no server | Free. |
| **FAISS** | Vector similarity search over caption embeddings for brief retrieval | Free. Facebook AI, Python library. |
| **FastAPI** | Scoring API endpoint | Free. |
| **Docker** | Reproducible containerized deployment (course requirement, Week 10) | Free. |
| **Evidently AI** | Data drift and model drift monitoring, HTML reports | Free. Python library. |
| **GitHub Actions** | CI: ruff lint + pytest on every push | Free (public repo). |
| **MkDocs + GitHub Pages** | Documentation site from docs/ | Free. |
| **Ruff** | Python linting (replaces flake8 + black) | Free. |
| **pre-commit** | Git hooks — enforces ruff on every commit | Free. |
| **Shields.io** | README badges: CI status, Python version, license | Free. |

**Total monetary cost: $0.**  
Every tool is free or covered by the student Gemini plan.

---

## 7. Repo expectations — step by step

### Step 0 — Declare Phase 0 complete (15 minutes, do today)

```bash
git tag -a v0.1.0-phase0-complete -m "Phase 0: raw audit passing on real data, CI green"
git push origin v0.1.0-phase0-complete
```

Then on GitHub:
- Create a release from the tag — paste audit key numbers as release notes
- Open 5 Issues: `Phase 1: Bronze extraction` · `Phase 2: Baseline models` · `Phase 3: Segmentation + embeddings` · `Phase 4: Scoring API + Docker` · `Phase 5: Monitoring + demo`

---

### Step 1 — Repo skeleton and CI hardening

Create `DECISIONS.md` — first entry:
```markdown
## 2026-09-30 — Phase 0 audit complete (real data)
- Confirmed: 38,113 perfect profile matches, zero duplicate post IDs
- Decision: sponsored encoding confirmed binary {0, 1}
- Decision: temporal train/val/test split — prevents creator-style leakage
- Decision: log1p transform on followers, likes, comments — heavy right-tail confirmed
- Decision: NULL category treated as its own class (6,017 creators), not imputed
- Decision: image pipeline scoped to stratified 5K sample (see image strategy section)
- Leakage finding: 97.3% of sponsored posts contain disclosure hashtag → two-task sponsorship experiment required
- Privacy: email and phone fields not extracted from profile JSON
```

Update `.github/workflows/ci.yml` — add ruff:
```yaml
- run: ruff check src/ scripts/ tests/
- run: pytest -q
```

Update `pyproject.toml`:
```toml
[project.optional-dependencies]
dev = ["pytest>=8", "ruff>=0.4"]
```

Rewrite `README.md` with CI badge · problem statement · architecture diagram · how to run.

Create `CONTRIBUTING.md`, `CHANGELOG.md`.

---

### Step 2 — Bronze extraction pipeline

Build:
- `src/underwriting/extraction/json_extractor.py` — streams `json_files.zip`, extracts fields in batches of 25,000 → Parquet shards, checkpointed
- `src/underwriting/extraction/profile_extractor.py` — streams both profile zips, no email/phone fields
- `scripts/extract_metadata.py` — CLI entry point
- `src/underwriting/io/duckdb_utils.py` — DuckDB helpers

Outputs:
- `artifacts/bronze/posts_metadata.parquet`
- `artifacts/bronze/profiles_influencers.parquet`
- `artifacts/bronze/profiles_brands.parquet`
- `artifacts/bronze/post_image_index.parquet`

Tests: `tests/test_extraction.py` — null-safe field handling, schema validation.

**Tag:** `v0.2.0-bronze-complete`

---

### Step 3 — Feature store

Build:
- `src/underwriting/features/engagement.py` — median_likes, median_comments, iqr, top_decile_rate, engagement_variance
- `src/underwriting/features/commercial.py` — sponsored_rate, disclosure_rate, n_distinct_brands, commercial_fatigue_score
- `src/underwriting/features/temporal.py` — posting_frequency, median_gap_days, burstiness, recency
- `src/underwriting/features/profile.py` — log_followers, follower_tier, null_category_flag, low_evidence_flag
- `src/underwriting/features/text.py` — caption_length, hashtag_count, mention_count, has_disclosure_hashtag
- `scripts/build_features.py` — DuckDB pipeline → silver Parquet

Notebook: `02_eda.ipynb` — distributions, leakage check, category breakdown. No modeling.

**Tag:** `v0.3.0-features-complete`

---

### Step 4 — Gemini client and caption embeddings

Build `src/underwriting/io/gemini.py`:
- `embed_texts(texts, cache_path)` — batch embedding with cache check + exponential backoff
- `parse_brief(brief_text)` — Gemini Flash → structured filter dict
- `explain_recommendation(creator_dossier, brief)` — RAG explanation with evidence grounding guardrail

Build `scripts/embed_captions.py` — idempotent, skips already-embedded posts.

**DECISIONS.md entry:** "Gemini text-embedding-004 chosen. 768-dim. All embeddings cached to Drive as Parquet. API called at most once per post across all Colab sessions."

---

### Step 5 — Baseline models and evaluation framework

Build:
- `src/underwriting/evaluation/splits.py` — creator-held-out split, time-held-out split
- `src/underwriting/evaluation/metrics.py` — PR-AUC, calibration, NDCG, Spearman
- `src/underwriting/evaluation/leakage_experiment.py` — 4-variant comparison table
- `src/underwriting/models/sponsorship_classifier.py` — LogReg → LightGBM → masked variant
- `src/underwriting/models/engagement_model.py` — follower-only baseline → quantile LightGBM

All training logged to MLflow.

Notebook: `03_baseline_models.ipynb` — evaluation tables, calibration curves, leakage experiment results.

Tests: `tests/test_models.py`

**Tag:** `v0.4.0-baselines-complete`

---

### Step 6 — Unsupervised, niche classifier, image sample

Build:
- `src/underwriting/models/niche_classifier.py` — softmax over 9 + NULL, Gemini embedding input
- `src/underwriting/models/anomaly_model.py` — isolation forest, z-score engagement residuals
- `scripts/embed_images.py` — Gemini Vision on stratified 5K sample → Parquet

Notebook: `04_unsupervised.ipynb` — PCA, UMAP, clusters, anomaly scores, Creator Segment Map.

**Tag:** `v0.5.0-unsupervised-complete`

---

### Step 7 — Scoring engine + FastAPI + Docker

Build:
- `src/underwriting/scoring.py` — `UnderwritingScore(i, c, t)` with configurable client weights
- `src/underwriting/api/main.py` — FastAPI: `POST /score`
- `src/underwriting/api/brief_parser.py` — Gemini Flash brief → structured filters
- `Dockerfile` + `docker-compose.yml`
- `scripts/score_influencer.py` — CLI entry point

The underwriting score formula:
```
UnderwritingScore(i, c, t) = D_i × [
    w_R·R_i + w_E·E_i + w_F·F_{i,c}
    + w_A·A_i + w_C·C_i + w_T·T_{i,t}
    + w_S·S_i − w_M·M_i
]
```

Where: R=reach proxy · E=engagement quality · F=content fit · A=authenticity · C=commercial readiness · T=timing · S=safety · M=fatigue penalty · D=data confidence.

Weights configurable per client type (restaurant vs. software vs. auto dealer).

Extend CI to build Docker image.

**Tag:** `v0.6.0-api-complete`

---

### Step 8 — Monitoring, documentation, demo, presentation

Build:
- `src/underwriting/monitoring/drift_report.py` — Evidently AI wrapper
- `docs/model_card.md` — training data, eval results, limitations, fairness analysis, what the model cannot predict
- `docs/data_card.md` — provenance, collection method, label caveats, ethics status, known inconsistencies
- `notebooks/07_demo.ipynb` — four campaign scenarios, API calls, Gemini explanation cards

Final README state: CI badge · Python badge · license badge · problem statement · Mermaid architecture diagram · links to model card + data card + DECISIONS.md · how to run locally + on Colab + via Docker.

**Tag:** `v1.0.0-capstone`

---

## 8. Evaluation matrix — what is reported for every model

| Task | Required split | Primary metric | Secondary metrics | Subgroup reporting |
|---|---|---|---|---|
| A — Disclosure detection | Creator-held-out + time-held-out | PR-AUC | Precision · Recall · F1 · Calibration | Follower tier · Category |
| B — Masked commercial intent | Creator-held-out + time-held-out | PR-AUC (vs. Task A delta) | Same as A | Same as A |
| Leakage experiment | Creator-held-out | ΔPR-AUC across 4 variants | — | — |
| C — Engagement quality | Creator-held-out + time-held-out | Spearman ρ · NDCG@10 | MAE · RMSE · PI coverage | Follower tier · Category |
| D — Niche classifier | Creator-held-out only | Macro-F1 | Calibration by class | All 10 classes |
| E — Segmentation | Internal validity | Silhouette score | UMAP visual + human inspection | — |
| Anomaly model | Manual review sample | Precision on flagged set | Coverage · False alarm rate | — |
| Underwriting score | Human eval — 4 campaigns | Pairwise agreement with expected rank | NDCG@K · Uplift vs. follower-count baseline | Client type |

---

## 9. Presentation narrative (2 November 2026, 12 minutes)

**Act 1 — The problem (2 minutes)**
> A marketing agency assigns 38,000 Instagram influencers to client campaigns. Today that decision is intuition-driven, opaque, and not reproducible. We build the decision system that makes it structured, transparent, and auditable.

**Act 2 — The system (8 minutes)**
1. Show the architecture diagram
2. Live demo: type a campaign brief → API returns ranked shortlist → show Gemini explanation card for top creator
3. Show the leakage experiment: "Why we have two sponsorship tasks, not one, and what the ΔPR-AUC tells us"
4. Show creator-held-out evaluation numbers — not just training accuracy
5. Show model card: "This is what the system explicitly cannot claim"

**Act 3 — The engineering (2 minutes)**
> "A notebook is not a system." Show: green CI badge · Docker running · MLflow experiment log · Evidently drift report. Clone it. Install it. Run it.

**Final statement:**
> This is a deployable system. It has tests, schemas, a documented API, a model card, and a data card. Every decision is logged. Every metric has an honest evaluation split. This is what production ML looks like.

---

## 10. What we will not do — and why (logged in DECISIONS.md)

| Excluded | Reason |
|---|---|
| Full 189 GB image pipeline | Not feasible on free tier; stratified sample produces the ablation we need |
| LSTM on post sequences | Simple temporal features produce equivalent signal; deep sequence model is future work |
| Fine-tuning HuggingFace BERT/RoBERTa | Gemini embeddings cover representation learning need without GPU fine-tuning time |
| Graph neural network | Brand-creator edges captured as tabular features; GNN is future work |
| Streamlit dashboard | FastAPI + demo notebook sufficient for presentation deadline |
| Synthetic data in model training | All model training uses real audit + real feature distributions; only smoke unit tests use synthetic data (established pattern) |
| Causal language in any report | Dataset is observational. All language uses "associated with", "predicted", "estimated proxy" — never "causes" or "proves" |
