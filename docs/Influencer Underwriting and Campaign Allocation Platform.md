# Influencer Underwriting and Campaign Allocation Platform

## Applied Machine Learning Capstone Blueprint

## 1. Project title

**Influencer Underwriting: A Multimodal Decision System for Matching Influencers to Brands and Estimating Potential Buyer Exposure**

### Stakeholder

A marketing agency assigns influencers to client companies at different times. Clients may include:

- kitchen-appliance retailers;
- restaurants and food businesses;
- software and mobile-app companies;
- automobile and second-hand-car sellers;
- fashion, beauty, fitness, travel, home, and consumer-product businesses.

### Stakeholder question

> Given a client, campaign objective, product category, desired audience, timing, and risk tolerance, which influencers should the agency assign, why, and with what expected level of potential buyer exposure?

### Important framing

This is not a sales-prediction system. The available data does not contain transaction records, conversion events, revenue, campaign spend, or impressions.

The defensible target is:

> **Potential buyer exposure and commercial suitability:** the probability that a creator’s content will reach relevant viewers, generate visible interaction, fit the client’s product, and communicate a sponsored message without excessive commercial fatigue or safety risk.

The system should explicitly report uncertainty and limitations rather than presenting potential exposure as actual sales.

---

## 2. Evidence from the current audit

The uploaded audit notebook provides several important facts.

### Dataset scale and integrity

- **1,601,074 posts** are present.
- Post IDs are contiguous from 0 to 1,601,073.
- There are **38,113 unique posting users**.
- There are **38,113 matching influencer profile files**, meaning every posting user in `post_info.txt` has a profile file in the audited archive.
- All listed post JSON files exist in `json_files.zip`.
- There are no duplicate JSON filenames in `post_info.txt`.
- No malformed influencer profiles were observed in the profile audit.
- The post-to-image mapping indicates that most posts have one image, but many have multiple images; 70 posts in the audit have no listed image.

### Sponsorship label

- Organic posts: **1,379,364**.
- Sponsored posts: **221,710**.
- Overall sponsored rate: approximately **13.85%**.

This is a useful but imbalanced binary target. A naïve classifier that predicts “organic” for every post would appear accurate, so evaluation must use precision, recall, F1, PR-AUC, calibration, and class-specific error analysis.

### Sponsorship leakage warning

In the audited sample of 600 posts:

- approximately **97.3% of labeled sponsored posts** contained a disclosure-style hashtag;
- approximately **3.0% of labeled organic posts** also contained one of the selected disclosure-style hashtags.

This means a caption model may achieve high performance by rediscovering explicit disclosure terms such as `#ad`, `#sponsored`, or `#paidpartnership`.

That is not useless: it is a valid disclosure-monitoring capability. But it is not sufficient evidence that the model understands deeper commercial intent.

The capstone should therefore report two sponsorship tasks:

1. **Disclosure detection:** Can the system identify explicit commercial disclosure?
2. **Commercial-intent detection beyond disclosure:** Can it identify likely sponsored/commercial content when disclosure tokens are removed or masked?

### Profile distribution and long-tail behavior

The audited influencer profiles show a heavy-tailed distribution:

- median followers: approximately **14,641**;
- 75th percentile: approximately **48,084**;
- maximum: approximately **119 million**;
- median profile post count: approximately **745**;
- maximum profile post count: approximately **127,520**.

The category field is broader than the original simplified list. In the audit, the largest groups include:

- Creators & Celebrities: 24,487;
- NULL: 6,017;
- Publishers: 1,830;
- Personal Goods & General Merchandise Stores: 1,510;
- General Interest: 1,421;
- Restaurants: 51;
- Auto Dealers: 30;
- Content & Apps: 131.

This is highly relevant to the proposed stakeholder use case. The data contains at least some direct business-relevant categories for restaurants, auto dealers, content/apps, home goods, personal goods, and services.

It also creates a modeling challenge: category imbalance and many NULL or broad-category profiles. The project should not silently treat all category values as equally reliable.

---

## 3. The underwriting metaphor

Underwriting means making a structured decision under uncertainty. The marketing agency can treat each campaign request like an application and each influencer like an opportunity being assessed.

### 3.1 Campaign application

A client submits:

- product or service category;
- campaign objective;
- desired audience niche;
- preferred time window;
- geographic/language constraints, if available;
- minimum expected exposure;
- acceptable brand-safety risk;
- maximum sponsorship intensity;
- preference for mass reach or community interaction;
- campaign budget, if later supplied.

### 3.2 Influencer dossier

The platform constructs a dossier for every creator:

- follower scale;
- normalized engagement;
- post frequency;
- category and niche;
- caption topics;
- visual topics and style;
- sponsorship rate;
- disclosure behavior;
- engagement consistency;
- commercial-content fatigue;
- brand-safety flags;
- content recency;
- creator confidence and data coverage;
- historical fit with product categories.

### 3.3 Underwriting decision

The platform returns:

- recommended;
- conditionally recommended;
- monitor/review;
- not recommended for this campaign.

It must also explain the decision:

- why this influencer fits;
- which evidence supports expected exposure;
- which risks reduce the score;
- where the model is uncertain;
- what additional information is required.

The system is therefore a **decision-support platform**, not an autonomous contracting or purchasing system.

---

## 4. The projected problem flow

## Stage 1: Translate client requirements into a machine-readable campaign brief

### Problem

A marketing brief is often written in natural language, while the available creator data is a mixture of numbers, text, images, categories, labels, and historical behavior.

### Example brief

> A kitchen-appliance retailer wants creators who can demonstrate practical home products. The campaign should emphasize credible human feedback, not only advertisements. The retailer prefers creators with strong food, family, interior, home-goods, or lifestyle relevance, stable engagement, low brand-saturation risk, and good performance during the next month.

### Solution front

Convert the brief into structured constraints and preferences:

```text
campaign_category = kitchen_appliances
preferred_niches = [food, family, interior, home_goods, lifestyle]
objective = potential_buyer_exposure
preferred_content = demonstration + authentic_review
minimum_engagement_quality = medium
maximum_commercial_fatigue = medium
brand_safety = standard
recency_window = defined_by_client
```

This stage can use either rule-based parsing, a small language model, or an LLM/RAG layer later in the project. The final recommendation must still be converted into measurable features and constraints.

---

## Stage 2: Build the creator feature store

### Problem

Raw posts and profile files are not directly usable for campaign decisions.

### Solution front

Create one creator-level feature table and one post-level feature table.

### Creator-level features

#### Scale

- followers;
- followees;
- profile post count;
- log-transformed follower count;
- follower tier: nano, micro, mid-tier, macro, mega;
- followee-to-follower ratio.

#### Activity

- number of observed posts;
- posting frequency;
- average and median time between posts;
- posting burstiness;
- recency of last observed post;
- active-period length.

#### Engagement

- mean and median likes, if available;
- mean and median comments;
- normalized likes per follower;
- normalized comments per follower;
- top-decile post rate;
- engagement variance;
- creator-relative residual engagement;
- percentage of posts with disabled comments.

#### Commercial behavior

- sponsored-post rate;
- disclosure-hashtag rate;
- commercial language rate;
- number of distinct brands mentioned;
- category concentration of mentioned brands;
- consecutive sponsored-post streaks;
- ratio of organic to sponsored posts.

#### Authenticity/community proxy

The user’s “human feedback and sponsored part in almost equal measures” can be operationalized as a balance requirement:

- sufficient organic-post volume;
- sufficient visible interaction on organic posts;
- comments-per-follower or comments-per-like;
- low excessive-sponsorship score;
- similarity between organic and sponsored engagement;
- evidence that the creator produces personal, explanatory, or review-like content;
- stable engagement rather than isolated viral spikes.

This is a **community/authenticity proxy**, not a direct measurement of trust or human emotion.

#### Content and niche

- creator category;
- caption topic distribution;
- image topic distribution;
- text and visual embeddings;
- hashtags;
- detected products and brands;
- food, home, family, fashion, fitness, pet, travel, automobile, or software-related content indicators.

#### Risk and quality

- missing profile fields;
- image coverage;
- low-data flag;
- duplicate-content rate;
- anomaly score;
- brand-safety flags;
- broad or NULL category flag;
- category-confidence score.

---

## Stage 3: Build the post feature table

Each post becomes a scored content object.

### Metadata features

- post ID;
- creator;
- timestamp;
- sponsorship label;
- number of images;
- likes;
- comments;
- location presence;
- tagged-user count;
- comment-disabled flag;
- post age at collection, if available.

### Text features

- caption length;
- token count;
- hashtag count;
- mention count;
- emoji count;
- disclosure terms;
- product terms;
- call-to-action terms;
- question count;
- sentiment and emotion;
- language;
- topic embedding;
- named brands and products.

### Image features

- image embedding;
- detected objects;
- people/faces;
- product or package presence;
- logos;
- OCR text;
- image quality;
- dominant colors;
- scene type;
- visual category;
- number and order of carousel images.

### Leakage controls

Some fields may be unavailable before a post is published or may directly encode the target. The feature table should maintain two views:

1. **Pre-publication view:** features available before publication.
2. **Post-publication diagnostic view:** features available after publication for monitoring and analysis.

Do not use post-publication likes or comments to claim that the system predicted them before publication.

---

## Stage 4: Define the targets

The project should not use one vague target called “successful influencer.” It should use multiple measurable targets.

### Target A: Sponsorship/disclosure

`is_sponsored`

Use the existing sponsorship label, but report the leakage-aware task:

- standard features;
- disclosure tokens masked;
- disclosure-only baseline;
- full multimodal model.

### Target B: Engagement potential

Possible targets:

- log likes;
- log comments;
- normalized like rate;
- normalized comment rate;
- top-decile engagement within creator/category/time;
- predicted engagement distribution rather than one point estimate.

### Target C: Engagement quality

Construct a quality proxy from:

- comments relative to likes;
- organic engagement;
- engagement consistency;
- creator-relative performance;
- non-sponsored content performance;
- absence of obvious anomaly signals.

Avoid naming this “human trust” unless human annotations support that claim.

### Target D: Commercial fit

For a campaign category, define whether a creator is suitable based on:

- category relevance;
- semantic similarity to the campaign brief;
- historical product/brand mentions;
- visual fit;
- engagement potential;
- commercial balance;
- safety and data confidence.

This target can be a ranking score or a human-labeled pairwise preference task.

### Target E: Potential buyer exposure

A defensible proxy could be:

```text
potential_buyer_exposure
  = predicted_relevant_viewer_proxy
    × predicted_interaction_quality
    × content_fit
    × commercial_readiness
    × confidence
```

Because actual impressions are absent, use a clearly labeled proxy rather than the word “viewers” as if exposure were directly observed.

A more defensible name is:

> **Expected Qualified Engagement Exposure (EQEE)**

It estimates the potential for relevant, visible engagement—not actual unique viewers or buyers.

---

## 5. The central decision score

The score should not be a single unexplained neural-network output. Use a transparent multi-objective formulation.

Let:

- `R_i`: normalized reach/scale proxy for influencer `i`;
- `E_i`: predicted engagement quality;
- `F_i,c`: content fit to client category `c`;
- `A_i`: authenticity/community balance proxy;
- `C_i`: commercial readiness;
- `T_i,t`: timing suitability for campaign time `t`;
- `S_i`: brand-safety score;
- `D_i`: data-confidence score;
- `M_i`: commercial-fatigue penalty.

One possible score is:

```text
UnderwritingScore(i, c, t)
  = D_i × [
      w_R R_i
    + w_E E_i
    + w_F F_i,c
    + w_A A_i
    + w_C C_i
    + w_T T_i,t
    + w_S S_i
    - w_M M_i
  ]
```

The weights should be configurable by the agency. A restaurant may prioritize food-fit and comments. A software company may prioritize explanation-oriented captions and technology affinity. An automobile dealer may prioritize local or automotive relevance if location data becomes available.

The score should be accompanied by:

- confidence interval or prediction interval;
- evidence summary;
- missing-data warnings;
- reason codes;
- hard constraint failures;
- alternative candidates.

---

## 6. Client-specific examples

## 6.1 Kitchen-appliance retailer

### Desired creator profile

- food, interior, family, lifestyle, or home-goods relevance;
- demonstration or recipe content;
- captions that explain usage and benefits;
- stable organic engagement;
- moderate sponsorship load;
- images with visible kitchens, food, products, or household contexts.

### Model priorities

- image/product detection;
- food and interior embeddings;
- caption explanation score;
- comments and questions as engagement-quality signals;
- organic/sponsored balance;
- brand-safety screening.

### Recommendation output

Ranked creators with an explanation such as:

> Strong candidate: high home/food semantic fit, stable organic comments, frequent practical captions, moderate sponsorship rate, and low commercial-fatigue risk.

---

## 6.2 Restaurant

### Desired creator profile

- food category or local food content;
- strong food imagery;
- high comment interaction;
- captions that describe taste, location, or experience;
- evidence of genuine visits or recommendations;
- suitable timing around meal periods.

### Model priorities

- food-image detection;
- restaurant and location entity recognition;
- sentiment and review-like language;
- comment-quality proxy;
- timing suitability;
- potential local relevance if location fields support it.

### Limitation

Without reliable location and reservation data, the model cannot estimate actual footfall or bookings.

---

## 6.3 Software or mobile-app company

### Desired creator profile

- technology, productivity, education, gaming, business, or lifestyle-app content;
- explanatory captions;
- screen or product visual presence;
- audience engagement through questions and discussion;
- low confusion between personal and commercial recommendations.

### Model priorities

- text and OCR;
- app/product entity recognition;
- semantic matching between app description and creator content;
- comment-discussion intensity;
- disclosure quality;
- commercial-fit confidence.

### Limitation

The dataset does not contain installs, clicks, trials, subscriptions, or conversions.

---

## 6.4 Second-hand automobile seller

### Desired creator profile

- automobile, lifestyle, travel, finance, or local-market content;
- visible cars and vehicle-related topics;
- practical/review content;
- high-quality comments;
- low safety or controversy risk;
- audience relevance, ideally with location data.

### Model priorities

- vehicle/object detection;
- automobile-category classification;
- review/explanation language;
- product and model-name recognition;
- anomaly and brand-safety screening.

### Limitation

The present dataset may contain only a small explicit “Auto Dealers” profile category. The model should use multimodal content and not rely only on the profile category.

---

## 7. “Human feedback plus sponsored content” as a measurable concept

The stakeholder wants a creator who combines meaningful human-level feedback with commercial ability. This should be broken into measurable proxies instead of being left as an intuitive label.

### Human/community proxy

Possible components:

- organic comment rate;
- organic comment-to-like ratio;
- question and response language;
- post-level engagement consistency;
- personal-experience language;
- review/explanation language;
- non-sponsored content depth;
- low dependence on isolated viral posts;
- low anomaly score.

### Commercial readiness proxy

Possible components:

- sponsorship disclosure quality;
- prior sponsored-post engagement;
- product demonstration content;
- brand/product mention quality;
- commercial caption clarity;
- historical category fit;
- ability to integrate products without abrupt content mismatch.

### Balance score

A simple balance score could reward creators near a target range:

```text
BalanceScore_i
  = 1 - |commercial_readiness_i - target_commercial_level|
```

A more useful operational rule is a two-axis matrix:

| Community interaction | Commercial readiness | Interpretation |
|---|---|---|
| High | High | Preferred creator |
| High | Low | Strong organic creator; needs campaign-fit review |
| Low | High | Commercially experienced but possible audience-fatigue risk |
| Low | Low | Weak candidate for this objective |

The preferred creator is not necessarily the creator with the highest follower count. It is the creator with sufficient scale, strong relevant interaction, and credible commercial integration.

---

## 8. Modeling plan mapped to the course

## Module 1: Fundamentals of ML and end-to-end pipelines

Apply by building:

- data ingestion from `post_info.txt`, JSON archives, profiles, and image mappings;
- schema validation;
- entity resolution for usernames and post IDs;
- train/validation/test design;
- reproducible feature and target creation;
- baseline metrics and model cards.

### Demonstrated skill

You show that you can turn raw multimodal data into an operational ML problem rather than jumping directly to a model.

---

## Module 2: Advanced preprocessing and feature engineering

Apply by handling:

- malformed or missing values;
- skewed follower and engagement counts;
- long-tail creator behavior;
- multi-image posts;
- caption cleaning and language detection;
- hashtags, mentions, emojis, OCR text;
- category normalization;
- temporal features;
- leakage prevention;
- creator-level aggregation;
- missingness and confidence features.

### Demonstrated skill

You show production-aware feature engineering for noisy social data.

---

## Module 3: Supervised learning, classical and ensemble

Use several model families:

- logistic regression for sponsorship/disclosure baseline;
- regularized linear regression for engagement;
- random forest and gradient boosting;
- XGBoost, LightGBM, or CatBoost if available;
- ranking models for creator selection;
- calibrated classifiers;
- quantile regression for prediction intervals.

### Demonstrated skill

You show that deep learning is not automatically the right first model and that strong baselines matter.

---

## Module 4: Unsupervised learning and dimensionality reduction

Apply to:

- creator segmentation;
- content-topic discovery;
- image-style clusters;
- brand–influencer network communities;
- anomaly detection;
- creator similarity search.

Methods may include:

- PCA;
- UMAP or t-SNE for exploration;
- K-means or HDBSCAN;
- Gaussian mixture models;
- isolation forests;
- graph community detection.

### Demonstrated skill

You show discovery of structure without relying only on preexisting labels.

---

## Module 5: Deep learning: FNN, CNN, RNN, and Transformers

### FNN

Use tabular creator/post features for the first neural baseline.

### CNN or pretrained vision encoder

Use post images for:

- category recognition;
- product/logo/object detection;
- visual embeddings;
- image-to-engagement analysis.

### RNN

Use post sequences for:

- creator activity forecasting;
- temporal engagement sequences;
- sponsorship streaks;
- next-post or activity prediction.

RNNs are useful pedagogically, but a strong capstone should compare them with simpler temporal features and transformer-based sequence models.

### Transformers

Use text transformers for:

- caption embeddings;
- sponsorship/disclosure classification;
- topic and sentiment analysis;
- semantic creator–brand matching.

Use multimodal fusion for:

- post engagement prediction;
- commercial-intent detection;
- creator–campaign compatibility.

### Demonstrated skill

You show awareness of the progression from tabular baselines to pretrained multimodal systems instead of using neural models without a control experiment.

---

## Module 6: Modern GenAI, LLMs, and RAG

The LLM should not be used to replace the predictive system. It should sit above the structured models as an explanation and interaction layer.

### RAG use case

Retrieve:

- creator profile summaries;
- historical content examples;
- category definitions;
- past recommendation evidence;
- model cards and limitations;
- brand-safety policies;
- campaign constraints.

Then allow an agency user to ask:

> “Which food-oriented creators are suitable for a restaurant that wants authentic review-style content next month, with moderate sponsorship and strong comment quality?”

The LLM converts the question into structured filters, calls the ranking system, retrieves evidence, and generates a grounded recommendation report.

### Required guardrail

The LLM must not invent follower counts, engagement, sales, reach, or reasons that are not present in retrieved evidence.

### GenAI deliverables

- campaign-brief parser;
- creator dossier summarizer;
- recommendation explanation generator;
- natural-language comparison of shortlisted creators;
- question-answering over audit reports and model limitations.

---

## Module 7: MLOps, serving, containerization, and monitoring

### Serving architecture

A practical architecture can contain:

```text
Client brief
   ↓
Brief parser / constraint validator
   ↓
Feature store and vector search
   ↓
Candidate retrieval
   ↓
Engagement, fit, sponsorship, and risk models
   ↓
Multi-objective underwriting scorer
   ↓
Explanation and evidence layer
   ↓
API + dashboard
```

### Recommended components

- Python data and modeling pipeline.
- Parquet or DuckDB for analytical storage.
- PostgreSQL or a lightweight metadata store for application data.
- FAISS, Qdrant, or another vector index for embeddings.
- FastAPI for serving.
- Streamlit or a React dashboard for demonstration.
- Docker for reproducible deployment.
- MLflow or an equivalent experiment tracker.
- Evidently or custom monitoring for drift and data quality.
- PyTorch or TensorFlow for deep models.

### Monitoring metrics

#### Data quality

- missing profiles;
- broken image mappings;
- schema changes;
- null rates;
- duplicate rates;
- category distribution shifts;
- timestamp range changes.

#### Model quality

- sponsorship PR-AUC and recall;
- calibration error;
- engagement MAE/RMSE or ranking metrics;
- creator-held-out performance;
- category-specific performance;
- false-positive review rate;
- retrieval relevance.

#### Operational

- API latency;
- feature generation latency;
- vector-search latency;
- model version;
- failed requests;
- recommendation coverage;
- percentage of recommendations with sufficient evidence.

#### Drift

- follower distribution drift;
- sponsorship-rate drift;
- caption-language drift;
- topic drift;
- image embedding drift;
- engagement baseline drift;
- performance drift by creator tier and category.

---

## 9. Train/test design that makes the project credible

A random row split is not enough because many posts belong to the same creator.

### Required evaluations

#### Random post split

Useful only as a fast baseline. It may overestimate real-world performance.

#### Creator-held-out split

Hold out entire creators. This tests whether the model generalizes to new influencers.

#### Time-held-out split

Train on earlier posts and test on later posts. This approximates deployment.

#### Creator-and-time-held-out split

The strongest setting for a new-campaign scenario.

#### Category-held-out analysis

Assess whether the model works equally across food, home, fashion, fitness, and smaller categories such as auto dealers or restaurants.

### Leakage tests

Run sponsorship classification with:

1. disclosure hashtags included;
2. disclosure hashtags masked;
3. all direct disclosure words removed;
4. creator identity excluded;
5. post metadata only;
6. text only;
7. image only;
8. multimodal features.

This turns a potential weakness into a strong scientific analysis.

---

## 10. Evaluation framework

## 10.1 Sponsorship/disclosure model

Report:

- precision;
- recall;
- F1;
- PR-AUC;
- ROC-AUC;
- calibration;
- confusion matrix;
- performance with disclosure terms masked;
- creator-held-out performance.

Prioritize recall if the system is intended to flag posts for review, but avoid overwhelming reviewers with false positives.

## 10.2 Engagement model

Report:

- MAE or RMSE on log-transformed engagement;
- Spearman rank correlation;
- top-k ranking precision;
- NDCG or Recall@K;
- calibration of high-engagement probabilities;
- performance by follower tier;
- performance by category;
- error intervals.

## 10.3 Creator recommendation system

For a capstone, create a small human-evaluation protocol:

- ask domain reviewers to rank candidate creators for sample campaign briefs;
- compare the model ranking with human ranking;
- measure pairwise agreement;
- record disagreements and analyze why they occur.

If no domain experts are available, construct an explicit annotation guide and label a manageable sample with multiple annotators.

## 10.4 Search and RAG system

Evaluate:

- Recall@K;
- precision of retrieved creators/posts;
- evidence completeness;
- hallucination rate;
- groundedness of explanations;
- user task completion time.

---

## 11. Free or accessible resource strategy

Assuming GPU resources are available, use the project to demonstrate efficient resource selection rather than spending compute indiscriminately.

### CPU-first work

- ingestion;
- schema audit;
- data-quality checks;
- aggregation;
- classical baselines;
- DuckDB/Parquet transformations;
- profile and post statistics.

### GPU-appropriate work

- image embedding extraction;
- OCR at scale;
- fine-tuning text classifiers;
- multimodal fusion;
- image/product classifiers;
- transformer-based embedding generation.

### Reuse pretrained models

For a capstone, start with pretrained encoders and fine-tune only where labels or compute justify it. The strongest engineering demonstration is often a well-evaluated frozen-embedding system compared with a fine-tuned model.

### Avoid unnecessary full-corpus image extraction initially

The dataset contains an extremely large image archive. Begin with:

1. a representative stratified sample;
2. a small image pipeline proof of concept;
3. cached embeddings;
4. incremental processing;
5. a full-corpus run only after the pipeline is validated.

This reduces wasted GPU time and makes the work reproducible.

---

## 12. Recommended capstone milestones

### Milestone 1: Data contract and audit

Deliver:

- data dictionary;
- entity model;
- join validation;
- missingness report;
- sponsorship-label audit;
- category audit;
- leakage-risk register.

### Milestone 2: Baseline underwriting score

Deliver a transparent score using:

- profile size;
- normalized engagement;
- sponsorship rate;
- category fit;
- posting activity;
- basic risk checks.

### Milestone 3: Classical ML models

Deliver:

- sponsored/disclosure classifier;
- engagement model;
- creator category model;
- first creator ranking model.

### Milestone 4: Unsupervised discovery

Deliver:

- creator clusters;
- post-topic clusters;
- visual-style clusters;
- anomaly report;
- brand–creator network graph.

### Milestone 5: Deep multimodal models

Deliver:

- text embeddings;
- image embeddings;
- multimodal engagement or fit model;
- comparison against classical baselines;
- ablation study.

### Milestone 6: GenAI and RAG layer

Deliver:

- campaign brief parser;
- grounded creator-dossier summarizer;
- evidence-based recommendation explanation;
- hallucination checks.

### Milestone 7: Deployment and monitoring

Deliver:

- containerized API;
- dashboard;
- model registry or experiment log;
- monitoring dashboard;
- model card;
- data card;
- demo campaign scenarios.

### Milestone 8: Final capstone demonstration

Demonstrate at least four campaigns:

1. kitchen appliances;
2. restaurant/food;
3. software/app;
4. second-hand automobile.

For each, show:

- campaign brief;
- candidate retrieval;
- ranking;
- feature evidence;
- risk warnings;
- predicted potential exposure;
- alternative candidates;
- uncertainty;
- what the model cannot know.

---

## 13. What this proves about your skills

A successful implementation would demonstrate skills applicable to advanced AI and ML organizations because it includes:

### Research and problem formulation

- converting a vague business need into measurable objectives;
- distinguishing prediction from causal inference;
- defining valid proxies;
- identifying label leakage;
- designing credible evaluation splits.

### Data engineering

- processing millions of records;
- joining heterogeneous archives;
- handling multi-image posts;
- building reproducible feature tables;
- tracking data quality and provenance.

### Classical machine learning

- interpretable baselines;
- ensemble models;
- imbalance handling;
- calibration;
- ranking and recommendation;
- hyperparameter tuning.

### Representation learning

- text embeddings;
- vision embeddings;
- multimodal fusion;
- similarity search;
- fine-tuning and ablation studies.

### Unsupervised learning

- creator segmentation;
- topic discovery;
- anomaly detection;
- graph communities.

### Generative AI

- structured brief parsing;
- RAG over model evidence;
- grounded summaries;
- explanation generation;
- hallucination prevention.

### Production ML

- API serving;
- containerization;
- reproducible environments;
- model monitoring;
- drift detection;
- model and data cards.

### Responsible AI

- privacy-aware handling of profile contact fields;
- no unsupported sales claims;
- fairness analysis across creator tiers and categories;
- uncertainty reporting;
- human review for high-impact decisions;
- transparent reasons for recommendations.

---

## 14. Final capstone thesis

The project should be presented as follows:

> **We develop an underwriting-style multimodal decision-support system for a marketing agency. The system converts a client’s campaign brief into measurable requirements, retrieves suitable influencers, estimates qualified engagement exposure, assesses commercial readiness and community interaction, identifies risk, and explains the recommendation. It does not predict actual sales because the dataset lacks conversions and revenue. Instead, it estimates a transparent proxy for potential buyer exposure and category-specific campaign suitability.**

The central contribution is not simply a classifier. It is an end-to-end system that connects:

```text
business brief
→ data audit
→ feature store
→ content understanding
→ engagement prediction
→ creator–brand fit
→ risk assessment
→ multi-objective underwriting score
→ explanation and recommendation
→ API/dashboard deployment
→ monitoring and human review
```

This framing is ambitious enough for a serious applied ML capstone, yet scientifically honest about what the available data can and cannot support.
