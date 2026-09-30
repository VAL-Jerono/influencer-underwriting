# Kim et al. Instagram Influencer Dataset: Realness and Dissertation Suitability

**Assessment date:** 30 September 2026  
**Dataset assessed:** Kim et al., *Multimodal Post Attentive Profiling for Influencer Marketing* (WWW 2020)

## Bottom line

**Yes, the dataset is genuinely empirical and can be used in a dissertation, subject to institutional approval and the access conditions imposed by the dataset custodians.** I found no evidence that the 33,935 accounts, post metadata, captions, comments, engagement counts, or images are synthetic or generated for simulation. The original paper describes a direct collection of Instagram posts, and the author’s dataset page describes the release as data collected from Instagram for research. The paper’s collection procedure is specific enough to audit: researchers queried posts containing `#ad` over 92 days, identified candidate usernames, applied follower/post thresholds, and then downloaded 300 recent posts per retained influencer [1] [2].

That conclusion does **not** mean the dataset is a neutral or representative sample of Instagram. It is a **historical, purposive, influencer-oriented snapshot** collected from a `#ad` discovery stream. Its labels are partly human and partly model-derived. It is therefore defensible for questions about this sampled population and period, but not automatically defensible for claims about all Instagram users, all influencers, current Instagram behavior, or causal effects.

## Why it is real data rather than synthetic data

The strongest evidence is the original WWW 2020 paper. It states that the researchers collected `#ad` posts from 1 October 2018 through 1 January 2019, obtaining 828,045 posts from 107,656 candidate users. They retained users with at least 1,000 followers and at least 300 posts, then downloaded 300 recent posts for each of 33,935 influencers. The resulting dataset contained 10,180,500 posts with images, captions, hashtags, usertags, timestamps, likes, comments, and related metadata [1]. This is a description of direct platform observation, not a synthetic-data generation process.

The author-maintained dataset page independently repeats the same provenance and describes approximately 37 GB of JSON metadata and 189 GB of JPEG images. It reports 12,933,406 image files because a post can contain multiple images [2]. The associated GitHub repository describes itself as an “Influencer dataset collected from Instagram” and repeats the same counts and file structure [3].

The dataset has also been used by subsequent scholarly work as a real-world Instagram dataset. For example, *InfluencerRank* explicitly calls it a “real-world dataset collected from Instagram” and uses the original posts and metadata, restricting the data to a historical 2017 window for its own temporal experiment [4]. A later Springer study states that it obtained access to the Kim dataset and used it for empirical analysis of fashion influencers [5]. Other scholarly records cite the same dataset for bot detection, influencer ranking, and multimodal Instagram analysis [6] [7]. These later uses are not proof that every record is authentic, but they corroborate that the dataset is treated in the research literature as an observational platform dataset rather than as a synthetic benchmark.

## What is actually observed, and what is derived

The following components appear to be observations or platform-provided fields captured from Instagram:

- influencer account/profile information;
- captions, hashtags, usertags, and timestamps;
- likes and comments or comment-related data;
- sponsorship-related fields;
- downloaded JPEG image files and the JSON-to-image mapping.

The following components are **not raw ground truth in the same sense**:

- the influencer category labels;
- the post category labels used in the paper’s auxiliary task;
- any later variables calculated by downstream researchers, such as engagement rate, sentiment, clusters, nationality, or model-predicted attributes.

The original paper says that the eight main influencer categories were identified using LDA topic modeling on biographies, followed by manual selection of representative topics. It then manually labeled 1,600 influencers for training/validation and 1,142 for testing. The final classifier assigned labels across the larger dataset. Post labels were also manually created for a balanced sample of 10,000 posts and used for the auxiliary classifier [1]. Thus, the **content is observational**, while some labels are human annotations and some full-dataset labels are outputs of a proposed model. A dissertation must state this distinction explicitly.

## Sampling and validity limitations

### 1. Discovery through `#ad` creates selection bias

The dataset was discovered by querying posts containing `#ad`, because the researchers used advertising disclosure as a route to find potential influencers [1]. This makes the dataset especially relevant to influencer marketing and sponsored-content research, but it does not make it a random sample of Instagram. It may overrepresent users who disclose advertising, users whose posts were visible to the collection process, and accounts active during the collection window. It may underrepresent influencers who do not use `#ad`, use different disclosure conventions, are private, or were not surfaced by the collection process.

### 2. The threshold defines the study population

The retained accounts had at least 1,000 followers and at least 300 posts at the filtering stage [1]. That is a defensible operational definition for the authors’ research question, but it excludes newer, smaller, less-active, private, and non-posting influencer accounts. The dataset should therefore be described as a sample of **high-activity public accounts identified through advertising-related posts**, not “Instagram influencers in general.”

### 3. It is a historical snapshot

The candidate-user collection occurred from October 2018 to January 2019. The 300 downloaded posts are the recent posts available for each retained influencer at the time of the final collection step, so the dataset is not a longitudinal panel in the ordinary sense. Platform design, disclosure norms, recommendation systems, creator behavior, and engagement mechanics have changed substantially since then. It is appropriate for historical analysis, methodological development, and theory testing that does not require current platform conditions. It is weak evidence for present-day prevalence or behavior unless the dissertation frames the study explicitly as historical or validates findings with newer data.

### 4. Engagement counts are not necessarily comparable across time

Likes, comments, and follower counts are snapshot measurements. Instagram has changed visibility rules, ranking systems, account behavior, and interaction patterns since collection. A dissertation should avoid treating raw counts as stable measures of influence across accounts without normalization and sensitivity analysis.

### 5. Labels are not unquestionable truth

The paper reports very high classification performance, but the labels are based on a modeling pipeline and a relatively small manually labeled set compared with the full 33,935-account corpus [1]. Category membership is therefore a construct operationalization, not an objective fact about identity or occupation. The dissertation should report the label-generation procedure, inspect class balance, assess inter-rater reliability if available, and avoid presenting the categories as platform-native labels.

## Access, licensing, and reproducibility status

The dataset is not openly downloadable from the GitHub repository. The repository contains a README and two illustrative PNG files; the raw 226 GB dataset is not stored there [3] [8]. The author’s request form asks for name, affiliation, email, agreement that the data will be used only for research or education, and agreement to follow copyright and license restrictions associated with the dataset/code and Instagram [9]. This is positive evidence of a controlled research-access process, but it is not the same as a clear open-source license.

The repository’s GitHub metadata currently reports **no declared repository license** [8]. The BERD@NFDI record calls the resource an open dataset and provides metadata, but its stated rights field is effectively “cite if used” and directs researchers to the author’s access page. The BERD record itself is metadata-only and reports zero downloadable bytes, so it should not be treated as an independent archival copy of the raw data [10].

For a dissertation, the practical implication is important: **access permission is not automatically permission to redistribute the raw images, captions, usernames, comments, or a full derivative dump.** Keep the custodian’s approval email/form record, preserve the exact terms, and ask the custodian or your institution’s research office whether thesis appendices, repository deposits, code releases, and derived tables are permitted.

## Platform and research-ethics considerations

The current Instagram Terms of Use state that users may not access or collect information through unauthorized automated means and may not publish another person’s private or confidential information without permission. The terms also distinguish users’ ownership of their content from Instagram’s license to operate the service [11]. Because the dataset was collected historically and distributed by the researchers for research or education, the current terms do not by themselves resolve whether every downstream use is permitted. The dissertation should document the dataset custodian’s permission and obtain institutional guidance rather than assume that “public” means unrestricted.

The Association of Internet Researchers’ ethics guidance treats automated collection of semi-public data as a specific ethical problem. It recommends considering consent, de-identification or pseudonymization, secure storage, data minimization, re-identification risk, and the risks introduced by dissemination or repository deposit [12]. This is especially relevant because the dataset contains usernames, usertags, captions, comments, images, and potentially personal or sensitive information.

A defensible protocol would normally include institutional ethics/IRB review or an exemption determination, restricted access to raw data, encrypted storage, removal or hashing of direct identifiers from analysis files where they are not needed, suppression of quotations that are searchable back to individuals, and publication of aggregated results rather than raw content. The exact requirements depend on the institution and jurisdiction.

## Internal inconsistencies to resolve before using it

There are two documentation inconsistencies that should be recorded rather than silently corrected.

First, the paper and the author’s page say **300 posts per influencer**, which exactly yields 33,935 × 300 = 10,180,500. The BERD metadata record contains a typographical inconsistency: it says “300 posts” but displays `33,935x330 = 10,180,500`, which is mathematically wrong [1] [2] [10]. Use 300 in the dissertation and note the BERD typo if the repository record is cited.

Second, the paper describes **eight influencer categories**—beauty, family, fashion, fitness, food, interior, pet, and travel—while the author’s landing page and repository describe **nine categories** by adding “other” [1] [2] [3]. The paper separately discusses “other” as a post category, so the status of “other” in the released influencer-level labels should be verified from the actual downloaded files. Do not assume that the landing-page category description and the paper’s experimental label space are identical.

## Dissertation suitability by research aim

**Strong fit:** historical influencer-marketing research; multimodal content analysis; image/text classification; disclosure and sponsored-content studies; descriptive studies of posting behavior; benchmarking models on a large real-world dataset; analyses explicitly restricted to the sampled accounts and collection period.

**Possible fit with additional safeguards:** studies of engagement, authenticity, category differences, or influencer effectiveness, if the dissertation treats engagement as an observational outcome, controls for account-level confounding, performs robustness checks, and avoids causal language.

**Poor fit as a sole dataset:** claims about all Instagram users; current Instagram behavior; population prevalence; causal effects of posting strategies; vulnerable-population or identity claims based on inferred categories; or claims that require representative sampling or verified ground-truth labels.

## Recommended dissertation wording

A careful methods description could say:

> “We analyze the Kim et al. Instagram Influencer Dataset, a controlled-access historical snapshot collected from public Instagram activity. The source study identified candidate accounts through posts containing `#ad` during 1 October 2018–1 January 2019, retained accounts meeting follower and posting-activity thresholds, and collected 300 recent posts per retained account. We treat the data as a purposive observational sample of advertising-active, high-activity Instagram accounts rather than a representative sample of Instagram users. Influencer categories are treated as derived labels produced through the source study’s topic-modeling, manual-annotation, and classifier pipeline.”

## Final judgment

**Authenticity:** High confidence that the released material is based on real Instagram observations and is not synthetic.

**Provenance:** Strong for the collection method and source authorship because the peer-reviewed paper, author page, GitHub repository, and later scholarly users agree on the core facts.

**Representativeness:** Limited. The `#ad` discovery procedure, thresholds, public-account dependence, and historical timing materially constrain generalization.

**Label validity:** Usable but derived. Labels should be analyzed as operational annotations, not unquestionable ground truth.

**Legal/ethical readiness:** Conditional. Obtain access, retain the written terms, seek institutional ethics/IRB guidance, minimize identifiable data, and do not redistribute raw content unless explicitly permitted.

**Overall recommendation:** Use it in the dissertation if the research question is aligned with this sampling frame and the thesis transparently reports the limitations. Do not describe it as synthetic, random, nationally representative, current, or ground truth. For high-stakes substantive claims, pair it with a second contemporary or independently sampled source if feasible.

## References

[1]: https://dl.acm.org/doi/fullHtml/10.1145/3366423.3380052 "Multimodal Post Attentive Profiling for Influencer Marketing"

[2]: https://sites.google.com/site/sbkimcv/dataset/instagram-influencer-dataset "Instagram Influencer Dataset — Seungbae Kim"

[3]: https://github.com/ksb2043/instagram_influencer_dataset "ksb2043/instagram_influencer_dataset — GitHub repository"

[4]: https://arxiv.org/html/2304.01897v2 "InfluencerRank: Discovering Effective Influencers via Graph Convolutional Attentive Recurrent Neural Networks"

[5]: https://link.springer.com/article/10.1007/s13278-024-01313-x "Characterizing fashion influencers’ behavior on Instagram"

[6]: https://link.springer.com/chapter/10.1007/978-3-030-60975-7_10 "Detecting Engagement Bots on Social Influencer Marketing"

[7]: https://ojs.aaai.org/index.php/ICWSM/article/view/18060 "Evaluating audience loyalty and authenticity in influencer marketing via multi-task multi-relational learning"

[8]: https://api.github.com/repos/ksb2043/instagram_influencer_dataset "GitHub repository metadata and license field"

[9]: https://docs.google.com/forms/d/1KBgy1oj-Pf3g187yQxIvzRwq6td0sgmGONS5058Flyc/ "Instagram Influencer Dataset Request Form"

[10]: https://berd-platform.de/records/e1nht-pxq21 "Instagram Influencer Posts and Image Dataset — BERD@NFDI metadata record"

[11]: https://help.instagram.com/581066165581870/ "Instagram Terms of Use"

[12]: https://aoir.org/reports/ethics3.pdf "Internet Research: Ethical Guidelines 3.0"
