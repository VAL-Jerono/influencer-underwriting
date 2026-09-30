# Instagram Influencer and Brand Dataset: Solvable Problems and Solution Frontiers

## 1. Executive conclusion

This dataset is unusually suitable for studying **Instagram content, influencer behavior, sponsorship disclosure, engagement, visual content, and influencer–brand relationships** at large scale.

The documented assets include:

- **38,113 influencer profiles** and up to **26,910 brands**;
- **1,601,074 posts** with a sponsorship label;
- post-level JSON metadata such as captions, likes, comments, timestamps, sponsorship, and usertags;
- post images, including a much smaller sample image package;
- influencer categories such as Beauty, Family, Fashion, Fitness, Food, Interior, Pet, Travel, and Other.

The strongest problem areas are:

1. detecting and understanding sponsored content;
2. predicting post engagement;
3. ranking influencers for campaigns;
4. understanding which content and creator characteristics are associated with engagement;
5. visual, textual, and multimodal content analysis;
6. influencer discovery, segmentation, and category classification;
7. brand–influencer relationship mining;
8. temporal analysis of posting and campaign behavior;
9. anomaly, fraud, and low-quality engagement screening;
10. building search, recommendation, and decision-support systems.

The dataset is **not sufficient by itself** for strong claims about sales, conversion, return on ad spend, true audience demographics, causal campaign lift, or long-term follower growth. Those problems require additional data such as impressions, reach, clicks, spend, conversions, audience geography, or an experiment/control design.

---

## 2. What the dataset appears to contain

### 2.1 Entity and relationship structure

The data can be modeled as a heterogeneous graph:

- **Influencer nodes:** username, category, followers, followees, post count, biography, contact fields, profile URL and profile image.
- **Brand nodes:** similar profile fields, with some missing brand profiles.
- **Post nodes:** post ID, creator, sponsorship label, JSON filename, image filename(s), timestamp, caption, likes, comments, usertags, and potentially additional Instagram metadata.
- **Image nodes:** one or more images associated with a post.
- **Edges:** influencer publishes post, post mentions or tags user/brand, influencer may be associated with a brand, and posts may contain multiple images.

This means the dataset supports not only ordinary tabular machine learning but also:

- natural-language processing;
- computer vision;
- multimodal learning;
- time-series analysis;
- graph analytics;
- recommender and information-retrieval systems.

### 2.2 Important scale and coverage facts

The stated scale is large enough for robust statistical analysis and modern machine-learning experiments:

- 1.6 million posts can support train/validation/test splits by time, creator, category, or post.
- 38k influencers support creator-level generalization experiments.
- 25k available brand profiles support brand classification and matching, but 1,628 brand profiles are unavailable.
- Images are resized, which is useful for efficient modeling but may remove small visual details.
- The sample image archive is only from one family influencer, so it cannot be treated as a representative image sample of the full corpus.

### 2.3 Fields that should be verified before modeling

The description says the JSON files contain “various information.” Before choosing a final problem, inspect the actual files to determine:

- exact like and comment fields and whether they are counts or lists;
- whether timestamps include timezone and whether they are publication timestamps;
- whether sponsorship is a reliable ground-truth label or a scraped/heuristic field;
- whether usertags identify brands, people, locations, or all account types;
- whether captions preserve hashtags, emojis, mentions, URLs, and language;
- whether deleted, private, unavailable, or duplicated posts exist;
- whether profile counts were collected at the same time as post metadata;
- whether images are present for every post or only a subset;
- whether the same account appears under multiple usernames;
- whether image files can be joined deterministically to JSON posts using the mapping file.

These checks affect the validity of every downstream solution.

---

## 3. Problem-to-solution map

The table below separates the **problem**, the **solution front**—the analytical or engineering approach—and the relevant data inputs.

| Problem that exists | Solution front | Inputs | Appropriate outputs | Main caveat |
|---|---|---|---|---|
| Identify whether a post is sponsored | Supervised sponsorship classification; multimodal text/image model; weak-label learning | Sponsorship label, caption, hashtags, mentions, images, usertags | Probability that a post is sponsored; explanation tokens or visual cues | Labels may reflect disclosure or dataset annotation rather than true commercial status |
| Detect undisclosed or ambiguously disclosed advertising | Compliance screening and anomaly detection | Sponsorship label, caption, hashtags, product/brand mentions, image | Review queue for likely undisclosed sponsorship | Cannot prove legal non-compliance without jurisdiction, contract, and disclosure context |
| Predict post engagement | Regression or ranking models | Likes, comments, followers, category, caption, image, timestamp, sponsorship | Expected likes/comments or engagement percentile | Likes/comments are not reach; follower count creates scale and leakage risks |
| Compare engagement fairly across creators | Normalized engagement modeling | Likes/comments, follower count, post history, creator ID | Rate or residual engagement relative to creator baseline | Public follower counts and engagement can be stale or inflated |
| Select influencers for a campaign | Influencer ranking and constrained optimization | Profile statistics, historical posts, engagement, category, brand mentions | Ranked shortlist under category, size, safety, or budget constraints | No campaign price, reach, audience quality, or conversion data is documented |
| Find creators similar to a target influencer | Embedding-based similarity search | Biography, category, captions, visual embeddings, engagement profile | Similar-influencer recommendations | Similarity depends heavily on the chosen representation |
| Identify creator segments | Clustering and mixture models | Followers, followees, posting volume, category, content, engagement, sponsorship rate | Segment labels such as niche specialist, high-volume creator, or brand-heavy account | Clusters are descriptive, not naturally meaningful unless validated |
| Classify influencers into categories | Text/image/profile classification | Existing category labels, bio, captions, images, profile picture | Predicted category for unknown or “Other” accounts | Existing categories may be coarse, subjective, or imbalanced |
| Discover what content performs well | Interpretable feature analysis and content mining | Captions, hashtags, images, time, likes, comments, category | Content patterns associated with high engagement | Association is not causal; popular creators can make weak content look strong |
| Recommend posting time | Temporal response modeling | Timestamp, post history, engagement, creator and category | Creator-specific recommended time windows | Timezone, audience online times, and platform algorithm changes may be missing |
| Detect engagement anomalies or possible fake engagement | Creator/post anomaly detection | Likes, comments, followers, posting time, historical distributions | Suspicious accounts/posts for investigation | No ground-truth fake-account labels; coordinated authentic activity can also look anomalous |
| Identify unusual growth or sudden campaign activity | Change-point and event detection | Post timestamps, sponsorship, engagement, profile counts if longitudinal | Periods of unusual activity | One-time profile snapshots limit true growth analysis |
| Detect brand mentions and product placement | Named-entity recognition, account linking, image recognition | Captions, hashtags, usertags, images, brand profiles | Brands, products, and placement locations in posts | Product names may be ambiguous; visual recognition needs labeled examples |
| Match influencers to brands | Content-based, graph-based, and learning-to-rank matching | Influencer content, brand bio/category, mentions, audience proxies | Compatibility score and candidate recommendations | Compatibility is not evidence of campaign effectiveness |
| Map the influencer–brand ecosystem | Bipartite graph analysis | Posts, usertags, mentions, sponsorship, profiles | Central brands, creator communities, category bridges, network structure | Mentions do not always imply endorsement or business relationship |
| Forecast future post engagement | Time-aware forecasting and hierarchical models | Historical post sequence, timestamps, creator, category, content | Expected engagement distribution for future posts | Forecast horizon and platform drift must be specified |
| Estimate probability a post becomes highly engaging | Classification/ranking | Post content and historical outcomes | Probability of top-decile or top-percentile engagement | Popularity thresholds should be defined within creator/category/time strata |
| Generate captions or campaign concepts | Retrieval-augmented generation or language modeling | High-performing captions, category, sponsorship, brand context | Draft caption ideas or content briefs | Requires human review; training on public content can reproduce stereotypes or copyrighted style |
| Search the corpus semantically | Multimodal embeddings plus vector search | Captions, bios, images, entities | Search by concept, product, mood, or visual style | Embedding quality and language coverage require evaluation |
| Moderate brand-safety risk | Taxonomy-based NLP/CV screening | Captions, images, profile bios, hashtags | Risk flags for violence, drugs, sexual content, hate, unsafe products, etc. | Risk categories and thresholds are normative and context-dependent |
| Measure sponsorship intensity by creator/category | Descriptive statistics and hierarchical modeling | Sponsorship label, creator, category, time | Sponsored-post rate, trends, category comparison | Label quality and creator activity differences matter |
| Study differences between sponsored and organic content | Matched observational comparison | Sponsorship, content, engagement, creator, time | Engagement/content differences after adjustment | Does not establish that sponsorship caused a difference |
| Study disclosure behavior | Compliance and communication analysis | Sponsorship label, disclosure terms, caption/hashtags, time | Disclosure rate, placement, wording, category differences | Need a precise disclosure definition and jurisdiction |
| Predict comment volume or discussion intensity | Count regression or ranking | Caption, image, likes, followers, category, timestamp | Expected comments or discussion score | Comments can be affected by moderation, bots, and controversy |
| Analyze sentiment, emotion, or topic | NLP classification/topic modeling | Captions and possibly comments if present | Sentiment, emotion, topics, language, trend curves | Captions may be short, multilingual, ironic, or promotional |
| Identify image styles associated with engagement | Computer vision plus statistical modeling | Images, engagement, category, timestamp | Visual feature importance, style clusters | Correlation can reflect creator identity or audience rather than image quality |
| Detect objects, scenes, products, faces, or logos | Object detection, image tagging, OCR, logo recognition | Post images, brand profiles/logos | Structured visual inventory per post | Requires validation; resized images may lose logo-level detail |
| Analyze carousel/multi-image strategy | Sequence and set modeling | Image-file lists, image order, engagement, captions | Effect of number/order/type of images | Need confirm image order and whether all images are available |
| Predict whether a post belongs to a category | Multimodal content classification | Images, captions, creator category | Post-level category labels | Creator category is not necessarily post category |
| Detect duplicate or near-duplicate content | Perceptual hashing and embeddings | Images, captions, post IDs | Repost/duplicate clusters | Similar content may be legitimate recurring branding |
| Identify repost networks or content diffusion | Image/text similarity graph | Images, captions, timestamps, accounts | Copying, diffusion, and trend pathways | Instagram data may not reveal original source or complete exposure path |
| Analyze creator professionalism and consistency | Reliability scoring and profile analytics | Posting frequency, sponsorship, captions, post metadata, profile fields | Consistency and activity indicators | “Professionalism” needs explicit operational definition |
| Predict creator retention/activity | Survival analysis | Posting history, category, sponsorship, profile count if longitudinal | Churn risk or next-post probability | A single collection window cannot support genuine long-term retention claims |
| Estimate content production patterns | Sequence mining | Post timestamps, image counts, captions, sponsorship | Cadence, burstiness, campaign waves, seasonal patterns | Collection gaps can create artificial patterns |
| Build a creator discovery marketplace prototype | Search, filters, ranking, and explainability | Profiles, categories, content and engagement | User-facing creator search and shortlist system | Operational marketplace needs current data and commercial terms |

---

## 4. Detailed solution fronts

## 4.1 Sponsorship and advertising intelligence

### Problem A: Sponsored-post classification

**Question:** Can we determine whether a post is sponsored from its available metadata and image?

**Solution front:**

1. Establish the existing sponsorship field as the initial target.
2. Train a text-only baseline using captions, hashtags, mentions, and bio/context.
3. Train an image-only model using visual embeddings.
4. Combine text, image, creator, and temporal features in a multimodal model.
5. Evaluate on creator-held-out and time-held-out splits so the model cannot memorize a creator’s usual behavior.
6. Produce calibrated probabilities, not just binary labels.

**Useful outputs:**

- `P(sponsored | post)`;
- top textual evidence such as ad-disclosure hashtags or brand mentions;
- visual evidence such as logo/product placement;
- uncertainty and human-review priority.

**Research value:** This is a strong benchmark task because the dataset contains both labeled posts and rich multimodal context.

### Problem B: Undisclosed advertising detection

**Question:** Are some posts likely to be commercial even when they are not labeled sponsored?

**Solution front:**

- detect commercial language and disclosure hashtags;
- identify repeated brand/product mentions;
- recognize logos and product packaging;
- compare a post with the creator’s sponsorship history;
- rank likely undisclosed cases for human review.

**Important distinction:** The model can flag **commercial-looking or disclosure-inconsistent content**. It cannot legally determine a violation without contractual and jurisdictional evidence.

### Problem C: Sponsorship behavior and market structure

**Questions:**

- Which categories have the highest sponsored-post rate?
- Do creators with different audience sizes disclose differently?
- Are sponsored posts concentrated among a small number of creators or brands?
- How does sponsorship intensity change over time?

**Solution front:** descriptive statistics, concentration indexes, panel models, survival/change-point analysis, and category-stratified comparisons.

---

## 4.2 Engagement prediction and optimization

### Problem D: Predict likes and comments

**Question:** Before publication, can we estimate likely engagement?

**Target options:**

- raw likes;
- raw comments;
- log likes/comments;
- engagement rate normalized by follower count;
- probability of top-decile engagement within a creator or category;
- a multi-objective score combining likes and comments.

**Solution front:**

- Baseline: follower count, category, post time, sponsorship, post/image count.
- NLP: caption length, hashtags, mentions, sentiment, topic, language.
- Vision: objects, scene, colors, faces, text, logos, image embeddings.
- Multimodal: fusion of caption and image representations.
- Modeling: gradient boosting, generalized additive models, hierarchical regression, neural ranking, and calibrated classification.

**Recommended split:** split by time and creator. A random post-level split would allow the same creator’s style and popularity to leak into both train and test sets.

### Problem E: Fair comparison of influencers

Raw likes reward large accounts. A fairer analysis estimates engagement relative to the creator’s expected baseline:

\[
\text{relative engagement} = \log(1 + \text{observed engagement}) - \log(1 + \text{expected engagement for creator}
)
\]

The expected value should be modeled using follower count, creator history, category, and time. This supports:

- high-efficiency creator identification;
- niche creator discovery;
- creator benchmarking;
- detection of posts that over- or under-performed.

**Caveat:** This is a performance proxy, not a measure of reach or sales.

### Problem F: Recommend when to post

Use creator-specific and category-specific temporal models to estimate engagement by day and hour. A robust approach should:

- use local timezone when available;
- separate weekdays and weekends;
- model creator history rather than relying only on global averages;
- control for post type, sponsorship, and campaign periods;
- report uncertainty and minimum sample size.

The output should be a time window recommendation rather than a claim that a particular hour causes success.

---

## 4.3 Influencer selection and campaign planning

### Problem G: Find the right influencer for a brand

**Solution front:** build a constrained ranking system with separate dimensions:

1. content/category fit;
2. visual fit;
3. engagement efficiency;
4. audience-scale proxy;
5. brand-safety risk;
6. sponsorship load;
7. posting consistency;
8. geographic/language fit, if available or added;
9. relationship signals such as previous brand mentions.

A campaign planner can specify constraints such as:

- target category;
- minimum or maximum follower range;
- minimum historical engagement;
- acceptable sponsored-post ratio;
- content safety threshold;
- number of creators;
- diversity across categories or creator tiers.

**Solution format:** an explainable shortlist, not a single opaque score. For each creator, show why they were selected and which criteria are missing.

### Problem H: Creator–brand compatibility

Possible approaches:

- content similarity between creator captions/images and brand profile/bio;
- historical brand mentions and sponsorship edges;
- category compatibility;
- graph-based link prediction;
- learning-to-rank using past observed brand associations.

**What this solves:** discovery and prioritization.

**What it does not prove:** that a partnership will generate conversions or positive lift.

### Problem I: Campaign portfolio optimization

If the user supplies campaign constraints and estimated creator costs, the dataset can support an optimization layer:

- maximize expected normalized engagement;
- maximize category coverage;
- minimize overlap or concentration;
- enforce brand-safety constraints;
- allocate a limited budget across creator tiers.

The dataset alone does not contain reliable prices, reach, conversions, or audience overlap, so those must be added before a real budget allocation system is used operationally.

---

## 4.4 Content understanding: text, images, and multimodal analysis

### Problem J: Caption topic and sentiment analysis

Possible outputs:

- topic categories;
- promotional versus personal language;
- sentiment and emotion;
- calls to action;
- question usage;
- hashtag themes;
- language and code-switching;
- caption readability and length.

**Solution front:** combine dictionary/rule baselines, supervised classifiers, multilingual transformer models, and topic models. Human annotation is recommended for a subset because social-media language is short, ironic, multilingual, and context-dependent.

### Problem K: Visual content taxonomy

The images enable analysis of:

- objects and products;
- indoor/outdoor scenes;
- food, pets, people, clothing, travel landmarks, rooms, and fitness activities;
- color palette and composition;
- text in images;
- logos and product packaging;
- face presence and approximate count;
- image quality and editing style;
- carousel structure.

**Solution front:** use pretrained image encoders for embeddings, object detectors for structured labels, OCR for text, logo/product recognition where appropriate, and human validation for the target taxonomy.

**Sample-image limitation:** the documented sample archive from one family influencer is useful for testing the pipeline but not for evaluating full-dataset visual generalization.

### Problem L: Multimodal content-to-engagement analysis

This is one of the most promising research fronts:

- fuse caption and image embeddings;
- add creator and time context;
- predict engagement or sponsorship;
- use explainability methods to identify whether language, visual style, product presence, or timing drove a prediction;
- evaluate separately by category and creator size.

The core challenge is separating **content effects** from creator popularity effects.

---

## 4.5 Influencer segmentation and classification

### Problem M: Segment creators into actionable types

Potential segments include:

- niche specialist;
- broad-reach celebrity;
- high-engagement micro-influencer;
- high-volume publisher;
- sponsorship-heavy commercial creator;
- lifestyle generalist;
- visual-first creator;
- community/conversation-focused creator;
- brand-affiliated or product-review creator.

**Solution front:** standardize profile and post aggregates, use clustering or mixture models, then validate segments with human interpretation and downstream usefulness.

**Do not overclaim:** a cluster is not a natural fact. It is a modeling choice whose stability should be checked across samples, time windows, and feature sets.

### Problem N: Classify accounts or posts into categories

The existing creator category labels can serve as:

- a supervised target;
- a weak label for posts;
- a benchmark for profile-based classification;
- a way to discover accounts currently marked “Other.”

A strong experiment compares:

1. bio-only classification;
2. caption-only classification;
3. image-only classification;
4. multimodal classification.

This reveals which data modality actually carries category information.

---

## 4.6 Fraud, quality, and anomaly analysis

### Problem O: Suspicious engagement detection

The dataset can support a **screening system**, not definitive fraud detection. Candidate signals include:

- unusually high likes relative to followers;
- abrupt engagement changes;
- low comments relative to likes or vice versa;
- repeated engagement patterns;
- activity bursts;
- accounts with unusual follow/follower ratios;
- duplicated or highly similar content;
- sponsorship and engagement combinations that depart from a creator’s normal pattern.

**Solution front:** robust statistics, isolation forests, autoencoders, change-point detection, graph anomalies, and human-labeled review samples.

**Main limitation:** no ground truth for fake followers, bot comments, paid likes, or coordinated campaigns is described. Without labels, outputs should be called “anomaly flags” or “risk scores.”

### Problem P: Data quality and integrity monitoring

The dataset itself can be audited for:

- duplicate posts;
- missing JSON or image files;
- broken mapping rows;
- inconsistent sponsorship values;
- impossible counts or timestamps;
- duplicate usernames;
- profile/post count inconsistencies;
- image-to-post cardinality errors;
- unavailable brand profiles;
- class imbalance and category leakage.

This is not merely preprocessing. A reproducible data-quality report is a valuable deliverable and is necessary before any model result can be trusted.

---

## 4.7 Network, search, and recommendation systems

### Problem Q: Map the influencer–brand network

Construct a bipartite graph:

- left side: influencers;
- right side: brands;
- edge: tagged, mentioned, or labeled sponsored relationship;
- edge weight: number of posts, recency, or normalized activity.

Possible analyses:

- most central brands and creators;
- communities and category bridges;
- brand concentration;
- creator overlap across brands;
- emerging or declining relationships;
- link prediction for likely future matches.

**Important semantic rule:** a tag or mention is not automatically a paid partnership. Keep edge types separate: mention, tag, sponsorship label, and inferred relationship.

### Problem R: Semantic search over creators and posts

Build a search engine allowing queries such as:

- “family creators with outdoor travel content”;
- “fitness posts showing home workouts”;
- “food creators with high comment rates”;
- “posts containing a particular product type.”

**Solution front:** structured filters plus text/image embeddings, with re-ranking based on engagement, category, recency, or safety.

This is a practical product direction because it uses nearly every data modality without requiring causal claims.

### Problem S: Similar-content and duplicate detection

Use perceptual hashes for exact/near-duplicate images and embeddings for semantic similarity. Extend to captions and hashtags to discover:

- reposts;
- recurring campaign templates;
- content copying;
- creator collaborations;
- trend diffusion.

The system must distinguish legitimate recurring brand templates from problematic copying.

---

## 5. Causal questions: what is and is not possible

The dataset is observational. It can answer **what is associated with what** much more reliably than **what caused what**.

### 5.1 Reasonably feasible observational questions

- Are sponsored posts associated with different like/comment levels after adjusting for creator size and category?
- Are certain caption or image features associated with high engagement?
- Do posting patterns differ between creator categories?
- Are brands connected to particular creator communities?
- Are certain disclosure terms associated with higher or lower interaction?

### 5.2 Questions requiring stronger design or additional data

- Did sponsorship cause an increase in engagement?
- Did a campaign increase brand sales?
- What would the same post have achieved if it had not been sponsored?
- Did an influencer create incremental reach beyond the brand’s existing audience?
- Which creator produces the highest return on ad spend?

For those questions, add campaign dates, spend, impressions, reach, clicks, conversions, sales, audience overlap, and preferably randomized or quasi-experimental variation. Suitable designs include matched panels, difference-in-differences, interrupted time series, holdouts, or randomized creator/post experiments.

---

## 6. Important limitations and invalid conclusions to avoid

### 6.1 No direct reach or impression measurement is documented

Likes and comments are visible interactions, not total exposure. A post with low visible engagement may have high reach, and the reverse may also occur.

### 6.2 No conversion or revenue outcome is documented

The dataset cannot directly estimate sales, leads, revenue, cost per acquisition, or ROAS.

### 6.3 Follower count is not audience quality

It does not prove that followers are real, active, relevant, geographically appropriate, or non-overlapping with another creator’s audience.

### 6.4 Cross-sectional profile fields may be stale

Followers, followees, and post counts can be snapshots taken at different times. They should not automatically be interpreted as growth or current values.

### 6.5 Sponsorship labels need validation

The label may reflect explicit annotation, disclosure, metadata, or a collection rule. It should be compared with textual disclosures and manually audited.

### 6.6 Missing brand profiles create selection bias

The 1,628 unavailable brand profiles may not be missing at random. Analyses involving brands should report coverage and missingness.

### 6.7 Images may not be available for every post

The image mapping file and archive integrity must be checked. Image-based conclusions may apply only to the image-covered subset.

### 6.8 Privacy, ethics, and platform terms matter

Profile emails and phone fields are sensitive. Avoid exposing personal contact information, attempting identity resolution, or using the dataset for harassment, unsolicited outreach, or surveillance. Store access-controlled data and publish aggregates where possible.

### 6.9 Historical platform behavior may not generalize

Instagram ranking, disclosure practices, creator behavior, and audience norms change over time. Models should be dated and monitored for drift.

---

## 7. Recommended research and product roadmap

### Phase 0: Data audit

1. Unpack a small sample of JSON and profile files.
2. Verify schemas and field types.
3. Build a deterministic post–JSON–image join.
4. Quantify missingness, duplicates, malformed records, and category imbalance.
5. Check whether timestamps, counts, and sponsorship labels are internally consistent.
6. Produce a data dictionary and provenance record.

### Phase 1: High-value descriptive baseline

Create:

- post and creator counts by category;
- sponsored versus organic post rates;
- engagement distributions;
- follower-size bands;
- posting cadence and seasonality;
- brand and creator concentration;
- image availability coverage;
- missingness and data-quality dashboards.

### Phase 2: Strong baseline models

Implement:

1. sponsorship classifier;
2. engagement percentile classifier;
3. creator category classifier;
4. influencer–brand matching baseline;
5. anomaly screening baseline;
6. semantic search prototype.

Each should have a simple interpretable baseline before a deep-learning model.

### Phase 3: Multimodal and graph extensions

Add:

- caption/image fusion;
- visual object and logo features;
- creator and brand graph embeddings;
- temporal and creator-held-out evaluation;
- explainable ranking;
- uncertainty estimates and human review queues.

### Phase 4: Operational validation

Use human experts to label samples for:

- sponsorship/disclosure;
- product and brand mentions;
- content category;
- brand-safety risk;
- suspicious engagement.

Measure precision, recall, calibration, subgroup performance, and drift over time.

---

## 8. Best candidate projects by objective

### If the goal is a publishable machine-learning paper

Best choices:

1. multimodal sponsored-post detection;
2. engagement prediction with creator-held-out evaluation;
3. influencer category classification from text and images;
4. multimodal content-to-engagement modeling;
5. influencer–brand link prediction;
6. anomaly screening with a human-labeled evaluation set.

### If the goal is a business tool

Best choices:

1. creator discovery and semantic search;
2. explainable brand–influencer matching;
3. campaign shortlist and portfolio optimization;
4. sponsorship monitoring and disclosure review;
5. brand-safety screening;
6. creator benchmarking dashboard.

### If the goal is social-science research

Best choices:

1. commercialization differences across creator categories;
2. disclosure language and engagement association;
3. brand–creator network structure;
4. visual and textual norms of influencer marketing;
5. creator specialization and audience engagement;
6. temporal changes in sponsorship behavior.

### If the goal is a computer-vision project

Best choices:

1. product/logo detection;
2. image-style clustering;
3. visual feature prediction of engagement;
4. image duplicate/repost detection;
5. carousel composition analysis;
6. multimodal category classification.

### If the goal is a data-engineering project

Best choices:

1. scalable post–JSON–image lakehouse;
2. entity resolution for usernames and brands;
3. feature store for creator/post features;
4. data-quality and provenance monitoring;
5. vector search over 1.6 million posts;
6. incremental temporal analytics pipeline.

---

## 9. Suggested final framing

The most defensible overall framing is:

> **A multimodal, large-scale observational dataset for studying Instagram influencer content, sponsorship, engagement, and influencer–brand networks. It supports prediction, ranking, classification, search, recommendation, anomaly screening, and descriptive social-science analysis. It does not, without additional outcome and experimental data, establish sales impact, causal campaign lift, audience quality, or return on investment.**

If only one project is selected, the strongest balanced choice is an **explainable multimodal influencer–brand matching and sponsored-content intelligence system**, evaluated with creator- and time-held-out tests and supported by a manually audited sample. This combines practical value with text, image, profile, temporal, and graph information while remaining honest about the dataset’s observational limitations.
