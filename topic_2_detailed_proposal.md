# Detailed Project Proposal: Mining Skill Demand from Online Job Postings

## 1. Project summary

**Project area:** Web Mining, text mining, information extraction, and network analysis  
**Proposed title:** *Mining Skill Demand from Online Job Postings: Extraction, Normalization, and Co-occurrence Analysis*  
**Study period:** A fixed, recent period determined by the selected dataset (ideally 6–12 months)  
**Unit of analysis:** One job-posting record  
**Primary output:** An interpretable analysis of skills requested in selected job families and how skill combinations vary by role, location, and time.

### Abstract

Employers describe job requirements in free text, using inconsistent spellings, abbreviations, and alternative names for related skills. This makes it difficult to compare skill demand across roles or to monitor how requirements change. This project will build a reproducible Web Mining pipeline that extracts skill mentions and selected attributes from a permitted public job-posting dataset, maps aliases to canonical skill names, and analyzes skill frequency and co-occurrence.

The study will focus on a small set of job families and a defined time window. Candidate skills will be identified with a documented vocabulary and phrase-matching rules; a lightweight named-entity recognition method may be added if time and data quality allow. A manually annotated sample will be used to evaluate extraction quality. The normalized skills will then be summarized by job family, location, and time period and represented as a co-occurrence network. The project will deliver a cleaned, privacy-conscious analysis dataset, an extraction pipeline, evaluation results, and visualizations. Findings will describe the sampled postings and will not be treated as a complete measure of the labor market.

## 2. Background and motivation

Online job advertisements are a useful source of evidence about how employers express role requirements. The text can mention technical tools, programming languages, methods, certifications, and interpersonal capabilities in the same paragraph. The same skill may appear under several surface forms—for example, an abbreviation, product name, or spelling variant—while one term may refer to different things in different contexts.

A simple count of words can therefore overstate some skills, miss aliases, and make comparisons between job families unreliable. This proposal addresses that problem by combining vocabulary-based extraction, documented normalization, manual quality assessment, and role-aware analysis. It emphasizes transparent and interpretable methods suitable for a course project.

## 3. Problem statement

Job requirements are mostly unstructured and vary in wording across employers and platforms. Without a consistent method for identifying and normalizing skills, comparisons of demand by role, location, or time can be misleading. The project will assess whether a practical extraction and normalization pipeline can produce sufficiently accurate skill data for descriptive analysis, and will show how skill combinations differ across selected job families.

## 4. Aim and objectives

### Aim

To develop and evaluate a reproducible pipeline for extracting, normalizing, and analyzing skills in online job postings.

### Objectives

1. Select a research-permitted job-posting dataset and define a focused sampling frame.
2. Identify skill mentions in posting text using a documented skill vocabulary and matching procedure.
3. Normalize aliases and spelling variants to canonical skill labels while preserving the original mentions for auditability.
4. Evaluate extraction quality against a manually annotated sample using precision, recall, and F1.
5. Compare skill frequencies and skill co-occurrence across selected job families, locations, and time intervals where the dataset supports those comparisons.
6. Produce visualizations and a reproducible workflow that clearly states its data and sampling limitations.

## 5. Research questions

**RQ1.** Which skills are most frequently requested in the selected job families during the study period?  
**RQ2.** Which skills tend to appear together, and how do these combinations differ between job families?  
**RQ3.** Where location and date coverage are adequate, how does observed skill demand vary across locations or time intervals?  
**RQ4.** How accurately does the proposed extraction and normalization method identify skill mentions in a manually reviewed sample?

### Working expectations

- Skill profiles will differ across job families, with some skills common across families and others concentrated in particular roles.
- Co-occurrence patterns will reveal recurring combinations that are not apparent from individual skill counts alone.
- Alias normalization will improve recall and consolidate counts, though ambiguous terms may reduce precision.

These are descriptive expectations, not claims about causality or future employment outcomes.

## 6. Scope and delimitations

To keep the project feasible:

- Select **two or three job families**, such as data analyst, software developer, and cybersecurity analyst, subject to available dataset labels.
- Use one dataset and a clearly defined date window, preferably 6–12 months if the dataset supports it.
- Limit the analysis to skills and a small set of posting attributes (job family, broad location, and posting date). Salary may be described only if coverage and units are sufficiently consistent.
- Do not attempt to infer a person's qualifications, predict hiring outcomes, or rank individual candidates.
- Do not treat job-ad counts as a direct measure of total employment or labor-market demand. They reflect the chosen source, collection process, and time window.

## 7. Data plan

### 7.1 Data source

Use a public dataset whose license and documentation permit the intended research use, or an official source/API whose terms allow the planned collection. Candidate datasets may include academic or public job-ad corpora, including datasets distributed through research repositories or platforms such as Kaggle; availability, provenance, completeness, and license must be verified before selection. A dataset is not automatically reusable merely because it is publicly downloadable.

The dataset selection checklist will record:

- Source and dataset version or retrieval date.
- License and permitted uses, including redistribution restrictions.
- Geographic and temporal coverage.
- Available fields and missingness.
- Whether records are original postings, deduplicated postings, or aggregated records.
- Known collection or platform sampling biases.

If no suitable downloadable dataset is available, use an official API or a small, low-rate collection only when the source terms and access conditions permit it. Do not bypass access controls, authentication, paywalls, or technical restrictions. Keep a copy of the source documentation and a brief record of the decision.

### 7.2 Proposed fields

| Field | Purpose | Handling |
|---|---|---|
| Posting ID | Deduplication and reference within the project | Replace with a generated project ID where practical |
| Job title | Assign or validate job family | Retain only as needed; normalize separately |
| Description or requirements text | Skill extraction | Process locally; exclude contact details and unrelated personal data |
| Posting date | Trend summaries | Convert to a consistent date or month; retain missingness |
| Location | Regional comparison | Normalize to a broad region where possible; avoid precise addresses |
| Salary range and currency | Optional descriptive analysis | Include only if sufficiently complete and comparable |
| Source/category metadata | Sampling and interpretation | Preserve source labels and document their meaning |

The minimum viable dataset consists of a posting identifier, title, description, and at least one useful grouping field. Salary is optional and will not be central to the research questions.

### 7.3 Sampling and data preparation

1. Apply the dataset's documented filters and select records within the chosen period.
2. Identify job families using supplied labels where reliable; otherwise, define transparent title-based rules and manually inspect a sample.
3. Remove exact duplicates and flag near-duplicates where feasible. Report how many records were removed or excluded.
4. Standardize dates, broad location labels, and text encoding.
5. Remove or mask email addresses, phone numbers, names, and other irrelevant personal contact details if present.
6. Record row counts after each preparation step so the analysis is reproducible.

## 8. Methodology

### 8.1 Skill vocabulary and normalization

Create a versioned vocabulary of canonical skill labels and their aliases. The vocabulary may combine a suitable public occupational or skills taxonomy (for example, O*NET where its coverage and terms fit the selected data) with a small, documented set of aliases discovered during pilot review. Every added alias will include its canonical label, source or rationale, and any ambiguity notes.

Normalization rules will include:

- Case folding and whitespace normalization.
- Standard handling of punctuation, hyphens, and common abbreviations.
- Phrase matching with word boundaries to reduce substring errors.
- Canonical mapping of known aliases to one label.
- Context rules or exclusions for ambiguous terms where possible.
- Retention of the matched text span and rule that produced each match for manual audit.

The vocabulary will be frozen before final evaluation. Changes made after reviewing evaluation errors will be documented and, if substantial, evaluated on a separate holdout sample.

### 8.2 Skill extraction

The primary approach will use dictionary and phrase matching because it is interpretable and practical for a small project. Each posting will be represented as a set of canonical skills, with repeated mentions counted separately only for a supplementary mention-frequency analysis. The main demand measure will be the proportion of postings in a group that mention a skill, which reduces the influence of unusually long descriptions.

If time permits and the selected corpus is large enough, a named-entity recognition model may be tested as an additional method. It will be treated as an extension, not a dependency for completing the project.

### 8.3 Manual annotation and evaluation

Draw a stratified sample of postings across the selected job families and annotate skill mentions using a written annotation guide. Two annotators are preferred for at least part of the sample; disagreements will be reviewed and resolved under documented rules. If only one annotator is available, re-annotate a subset after a delay and report that inter-annotator agreement could not be estimated.

Compare extracted skill mentions with the adjudicated annotations using:

- **Precision:** share of extracted skill mentions that are correct.
- **Recall:** share of annotated skill mentions found by the pipeline.
- **F1:** harmonic mean of precision and recall.

Report both mention-level and, if feasible, posting-level results. Include overall results and results by skill category or job family when sample sizes permit. The annotation sample size will be set after a pilot, balancing workload with representation across families; the final proposal implementation should state the exact number.

### 8.4 Frequency and co-occurrence analysis

For each skill, calculate the number and proportion of postings in which it appears. Compare these measures across job families. For a posting-level skill set, count a skill pair as co-occurring when both canonical skills appear in the same posting. Report pair counts and normalized measures such as Jaccard similarity or lift, with a minimum support threshold to reduce unstable pairs.

Construct a weighted, undirected skill co-occurrence network:

- Nodes represent canonical skills.
- Edges represent skill pairs co-mentioned in postings.
- Edge weights represent co-occurrence strength or a normalized association score.

Use community detection and centrality measures only as exploratory summaries. State the selected algorithm and parameters, and interpret clusters through their constituent skills rather than presenting algorithmic groups as definitive categories.

### 8.5 Time and location comparisons

If dates are sufficiently complete, aggregate monthly or quarterly proportions and compare the same skill within each job family. If the period or sample size is too small, report counts and avoid claims of a trend. If locations are available and consistently coded, compare broad regions; suppress or combine groups with very few records. Check whether apparent differences could result from changing sample composition.

### 8.6 Baselines and robustness checks

Compare the normalized pipeline with a simple exact phrase-matching baseline without alias mapping. This will show whether normalization changes coverage and rankings. Where practical, perform these checks:

- Recalculate rankings using posting prevalence rather than raw mention counts.
- Vary the minimum support threshold for co-occurrence edges.
- Re-run summaries after excluding near-duplicates or records with very short descriptions.
- Compare results across job-family subsets and available time intervals.

## 9. Evaluation criteria

The project will be considered successful if it:

1. Produces a traceable and documented mapping from surface forms to canonical skills.
2. Reports extraction precision, recall, and F1 on a manually reviewed sample.
3. Provides interpretable comparisons of skill prevalence and co-occurrence for the selected families.
4. Makes the sampling frame, data limitations, and processing decisions clear enough for another student to reproduce the analysis.

No minimum accuracy threshold is assumed in advance. If evaluation shows weak performance, that result will be reported and the analysis will be narrowed to skill groups for which extraction is reliable.

## 10. Ethics, privacy, and responsible interpretation

- Follow the dataset license and source terms; document the basis for access and use.
- Prefer aggregated findings and avoid publishing raw posting text or identifiers unless explicitly permitted and necessary.
- Remove personal contact details and avoid collecting information about applicants or employees.
- Do not use the results to make decisions about individual people.
- Describe findings as patterns in the sampled postings, not as definitive rankings of skills across the whole economy.
- Report likely coverage, language, geographic, platform, and deduplication biases.
- Avoid interpreting an increase in posting mentions as proof of a causal change in employer needs; it may reflect source coverage or sample composition.

## 11. Tools and implementation

A practical implementation can use Python with:

- `pandas` for data preparation and summaries.
- Regular expressions or a phrase-matching library for extraction.
- A versioned CSV/JSON skill vocabulary for aliases and canonical names.
- `scikit-learn` for evaluation metrics and optional clustering utilities.
- `networkx` for co-occurrence graph analysis.
- `matplotlib` or `seaborn` for charts.

The project should store configuration, vocabulary version, and processing parameters alongside the code. A notebook may be used for exploration, with reusable extraction and evaluation steps placed in scripts or functions.

## 12. Work plan and timeline

| Week | Activities | Milestone |
|---|---|---|
| 1 | Review project scope; identify candidate datasets; check license, fields, and coverage | Dataset decision and finalized research questions |
| 2 | Load data; profile quality; define job families and sampling rules | Data audit and sampling frame |
| 3 | Build initial skill vocabulary; inspect a pilot sample; write annotation guide | Vocabulary v1 and pilot annotation |
| 4 | Implement extraction and normalization; deduplicate and prepare analysis data | Working pipeline |
| 5 | Annotate evaluation sample; compute precision, recall, and F1; inspect errors | Evaluation results |
| 6 | Conduct frequency, co-occurrence, and supported location/time analyses | Analysis tables and graph |
| 7 | Run baselines and robustness checks; prepare visualizations | Final figures and findings |
| 8 | Write report; document limitations and reproducibility details; prepare presentation | Submitted report and presentation |

If the course schedule is shorter, omit the optional NER extension and salary analysis before reducing the evaluation work.

## 13. Expected outcomes and deliverables

1. A concise data statement covering source, license, coverage, sampling, and limitations.
2. A documented, versioned skill vocabulary with aliases and ambiguity notes.
3. A reproducible extraction and normalization pipeline.
4. A manually annotated evaluation sample and reported precision, recall, and F1, subject to source terms and course data-handling rules.
5. Tables and visualizations of skill prevalence by job family and, where supported, location and time.
6. A skill co-occurrence network and interpretation of its strongest associations or clusters.
7. A final written report and presentation describing methods, findings, limitations, and ethical considerations.

## 14. Risks and mitigation

| Risk | Likely effect | Mitigation |
|---|---|---|
| Dataset license or provenance is unclear | Dataset cannot be used as planned | Verify documentation before analysis; switch to a clearly permitted dataset or official API |
| Descriptions are missing, short, or duplicated | Biased frequency estimates | Profile coverage, deduplicate, define minimum-text rules, and report exclusions |
| Aliases and ambiguous terms cause extraction errors | Lower precision or recall | Use boundary-aware matching, document exclusions, manually evaluate, and report per-family performance |
| Job-family labels are inconsistent | Comparisons mix different roles | Use a small number of families and validate classification rules on a sample |
| Too few records in a region or time interval | Unstable comparisons | Merge broad groups, raise minimum support, or omit the comparison |
| Platform sample does not represent the labor market | Overgeneralized conclusions | Limit claims to the observed dataset and explain coverage bias |

## 15. Proposed report structure

1. Introduction and motivation
2. Related concepts and project context
3. Dataset, license, and sampling frame
4. Preprocessing, vocabulary, and extraction method
5. Annotation design and evaluation results
6. Skill demand and co-occurrence findings
7. Discussion, limitations, ethics, and reproducibility
8. Conclusion and possible future work

## 16. Short conclusion

This project turns unstructured job-ad text into an auditable dataset of normalized skills, evaluates how reliably those skills can be extracted, and uses Web Mining methods to describe demand and skill combinations across a focused set of roles. Its limited scope, manual quality check, and explicit account of data provenance make it feasible for a course project while still producing measurable results.

---

# Vietnam-focused implementation plan: IT and Business Analyst postings

This section specializes the proposal for IT and Business Analyst (BA) jobs in Vietnam. It replaces the generic job-family and time-window suggestions above for the implementation plan.

## A. Final recommended scope

**Study title:** *Skill Demand in Vietnam’s IT and Business Analyst Job Postings: A Text Mining Study, 2020–2025*

- **Geography:** Vietnam; summarize nationally and by broad location (e.g., Ho Chi Minh City, Hanoi, Da Nang, other/unspecified) when the data supports it.
- **Time:** Target January 2020–December 2025. Treat this as a six-year period. Extend toward ten years only if a source supplies comparable, permitted records back to 2016/2017. Do not imply that a source covers ten years until verified.
- **Job groups:** IT and BA, with subgroups where sample size permits:
  - IT: software/backend/frontend/full-stack, data/AI, QA/testing, infrastructure/cloud/security.
  - BA: business analyst, IT/business systems analyst, product/business process analyst. Decide whether product owner and project manager are excluded; document the decision to avoid mixing unlike roles.
- **Language:** Include Vietnamese and English postings from Vietnam if both are present. Record language and analyze coverage by language; do not assume an English-only skills vocabulary will capture Vietnamese descriptions.
- **Primary outcome:** Percentage of postings in each group that request each skill, plus co-occurring skill combinations.
- **Optional outcomes:** Experience level and salary only if consistently available. Salary should be converted to a common monthly VND basis only when pay period and currency are explicit; otherwise omit it.

A six-year study is a better initial target than an unsupported ten-year claim. A 2020–2025 window aligns with one currently advertised Vietnam historical feed, while free/public corpora may have different and narrower windows. The final start and end dates must follow the chosen source’s actual coverage.

## B. Candidate data sources

| Source | Potential use | Advantages | Checks and limitations |
|---|---|---|---|
| **VietJobs: A Vietnamese Job Advertisement Dataset** (research paper and released corpus) | First source to investigate for a research project | The paper describes 48,092 Vietnam job ads across provinces, with title, category, salary, skills, and employment-condition fields. It was designed for NLP and labor-market analysis. | Confirm the actual release location, license, date range, duplicate policy, and whether full descriptions are available before committing. The paper abstract alone does not establish that it covers 2016–2025 or that every field can be redistributed. |
| **VietJobs-37K / VieJobBERT release** | Candidate for a pilot, job-family/title classification benchmark, or supplementary Vietnamese text | Public release reports 37,274 Vietnamese-dominant postings, 60 occupation labels, macro-groups, and human-validation subsets. Labels are useful for role classification experiments. | This is an occupation-classification resource, not automatically a longitudinal skills-demand dataset. Check the Zenodo record’s data license and available dates/fields; silver labels are largely keyword-derived, so use the gold human-validated subset for evaluation where relevant. |
| **Techmap / JobDataFeeds Vietnam historical postings** | Possible source when historical depth and structured fields matter | Provider advertises Vietnam postings since January 2020, with fields such as title, description, location, skills, and source portal. | It is paid (the listed historical product is a one-time purchase); confirm the academic license, redistribution limits, exact date coverage, revisions, and cost before using it. It does not support a pre-2020 start based on the advertised history. |
| **University, lab, or instructor-provided archive** | Preferred route if available | May provide a permitted multi-year archive and local context. | Obtain written source, license/permission, collection dates, field definitions, and de-identification details. |
| **Direct collection from Vietnam job portals or employer career pages** | Fallback for a recent, narrow time window | Can provide locally relevant descriptions and source metadata. | Use only if the specific source terms, API, or written permission allow collection. Public visibility is not itself permission to scrape or republish. Historical postings are usually unavailable unless archived. Keep request rates low and do not bypass access controls. |

**Recommended selection sequence:** Ask the supervisor/library for an existing permitted archive; inspect the VietJobs and VietJobs-37K releases and terms; request a sample and academic terms from the commercial historical provider if budget allows; otherwise narrow the study to a source and period that can be accessed lawfully. Do not combine sources until their fields, dates, and collection methods can be compared.

### Taxonomies and skill references

- Build a Vietnam-specific alias list from pilot postings and have a Vietnamese/IT-aware reviewer check it.
- Use **ESCO** as a supplementary structured skill/occupation vocabulary and export source, not as a definitive Vietnam taxonomy. Its current published language packs do not include Vietnamese, so adapt relevant English concepts and add locally used Vietnamese/English aliases with provenance.
- Use **O*NET** as a supplementary reference for occupation and technology-skill concepts. It is US-oriented; do not treat its occupation-to-skill links as Vietnam demand. Attribute and follow the applicable license for the exact O*NET files/API used.
- If the VietJobs-37K taxonomy aligns with the intended role families, use its labels as a candidate mapping and manually validate the IT/BA mapping. Do not assume a taxonomy crosswalk is expert-validated.

## C. Detailed work breakdown

### Phase 1 — Scope and research design (Week 1)

**Tasks**
1. Confirm the definitions of IT and BA jobs and list included/excluded titles.
2. Confirm the target period as 2020–2025, conditional on dataset coverage; set 2016–2025 only if a permitted source actually supports it.
3. Finalize questions, geography, language policy, and minimum sample requirements.
4. Write inclusion/exclusion criteria and a short data-provenance checklist.

**Deliverables**
- Scope statement and operational definitions.
- Final research questions.
- Dataset selection checklist and provisional analysis plan.

**Decision gate**
- Do not proceed to trend analysis until a source has verified dates and adequate records across the selected period.

### Phase 2 — Source audit and data acquisition (Weeks 1–2)

**Tasks**
1. Locate candidate datasets and record landing page, version/date, license, terms, citation, fields, and collection method.
2. Inspect a sample or data dictionary, checking dates, text availability, language, locations, role labels, and salary fields.
3. Estimate how many eligible IT and BA postings exist per year and source.
4. Select one primary source; document why alternatives were rejected.
5. Acquire data only through the permitted download/API or approved access route.

**Deliverables**
- Source and license register.
- Data dictionary for project fields.
- Short feasibility report with eligible posting counts by year and role.

**Decision gate**
- If the data does not cover the planned years comparably, shorten the time range or reframe the study as a snapshot. Do not fill missing historical years by scraping without authorization.

### Phase 3 — Data profiling and cleaning (Weeks 2–3)

**Tasks**
1. Load records and standardize encoding, dates, title, description, location, and source fields.
2. Remove exact duplicates; identify likely reposts using title/company/location/date/text similarity. Keep an audit trail of removals.
3. Detect language (Vietnamese, English, mixed, other) and retain the label for analysis.
4. Normalize province/city names into broad geographic categories; keep unknown separate.
5. Remove or mask email addresses, phone numbers, and personal names if present and unnecessary.
6. Inspect missingness and text length by year, role, and location to find coverage changes.

**Deliverables**
- Cleaned working dataset with generated project IDs.
- Cleaning script/notebook and exclusion log.
- Data quality report with counts and missingness.

### Phase 4 — Job-family identification (Weeks 3–4)

**Tasks**
1. Create title rules for IT and BA inclusion, including title synonyms (e.g., “Business Systems Analyst,” “System Analyst,” “Data Analyst” must be considered carefully because Data Analyst may not be a BA role).
2. Manually label a stratified title sample as IT, BA, other, or ambiguous.
3. Compare simple keyword rules to a machine-learning classifier if there are enough labeled examples.
4. Resolve ambiguous titles using description context; report uncertain cases separately.

**Candidate models**
- Baseline: transparent title keyword rules.
- Classical model: word/character TF–IDF + logistic regression or linear SVM.
- Vietnamese text model: fine-tuned PhoBERT for Vietnamese-dominant titles/descriptions; XLM-R for multilingual or mixed Vietnamese/English postings.
- For multi-label occupation tags, use one-vs-rest logistic regression or a sigmoid output layer; do not use softmax when a posting can belong to multiple groups.

**Deliverables**
- Job-family labeling guide and labeled sample.
- Role classifier with per-class precision, recall, F1, and confusion matrix, if trained.
- Final included-posting set.

### Phase 5 — Skill vocabulary and annotation (Weeks 4–5)

**Tasks**
1. Pilot-read postings from each role, year band, and language group.
2. Build a skill schema with categories such as programming/languages, frameworks, cloud/devops, data/AI, testing/security, databases, BA methods, requirements/process, tools, and communication/domain skills.
3. Record canonical label, alias, category, language, source, and ambiguity notes. Examples: “JS” → “JavaScript”; “BA” is not always the occupation; “SQL” is a skill; “Agile” may refer to methods and should be consistently defined.
4. Create annotation instructions that mark exact skill spans and distinguish required skills from preferred skills when the text indicates this explicitly.
5. Annotate a stratified sample across IT/BA, years, and language. Have a second annotator label a subset and resolve disagreements.

**Deliverables**
- Versioned bilingual skill vocabulary.
- Annotation guide and gold sample.
- Inter-annotator agreement report for the double-labeled portion.

### Phase 6 — Skill extraction model comparison (Weeks 5–7)

Use a controlled comparison, keeping the same training/evaluation split and annotation rules.

| Approach | Role in project | Strengths | Limits |
|---|---|---|---|
| Dictionary/phrase matching | Required baseline | Simple, interpretable, easy to audit | Misses unseen forms; can make substring/context errors |
| TF–IDF + logistic regression/SVM | Optional document-level skill-category baseline | Fast, strong small-data baseline | Predicts labels per posting, not exact mention spans; less useful for new skills |
| CRF or BiLSTM-CRF with word/character features | Sequence-labeling comparison | Learns skill boundaries from annotated spans | Needs tokenized training data; older architecture, may struggle with mixed language |
| PhoBERT token classification (BIO tagging) | Main neural model for Vietnamese text | Context-sensitive Vietnamese representation; predicts exact spans | Requires annotation; English technical terms and code-like strings may need special handling |
| XLM-R token classification | Multilingual comparison or fallback | Handles Vietnamese-English mixed text | May be heavier; can underperform a language-specific model on Vietnamese |
| Sentence embeddings + nearest-neighbor taxonomy linking | Optional normalization/linking stage | Can suggest canonical skills for aliases or unseen phrases | Similarity is not proof of equivalence; requires threshold tuning and human review |
| LLM-assisted annotation | Optional productivity aid only | Can propose labels or resolve candidate spans | Outputs can be inconsistent; check privacy/terms and never use unreviewed outputs as ground truth |

**Recommended minimum model set:** dictionary matching baseline + PhoBERT BIO tagger, with XLM-R added only if the data is substantially bilingual and the team has time. Compare on a manually annotated holdout set. A CRF/BiLSTM-CRF is a useful traditional architecture if a course requirement calls for a non-transformer model.

**Data split:** Split by posting (and preferably group near-duplicate postings together) so reposts do not appear across train and test. For time-trend generalization, reserve the latest year as a temporal test set if sample size permits. Keep a separate untouched test set for final reporting.

**Metrics:** Exact-span precision/recall/F1 and relaxed overlap F1; canonical-skill micro and macro F1; per-category and per-language results. Report support counts. For role classification report macro-F1 and per-class results to account for imbalance.

**Deliverables**
- Reproducible model training/evaluation notebook or scripts.
- Baseline and model comparison table.
- Error analysis with examples of missed skills, false matches, aliases, and mixed-language issues.

### Phase 7 — Demand, trend, and co-occurrence analysis (Weeks 7–8)

**Tasks**
1. Calculate posting prevalence for each skill: postings containing a skill divided by eligible postings in that group/time interval.
2. Compare IT with BA and, when counts allow, compare subfamilies (e.g., software vs data vs QA; IT BA vs process BA).
3. Summarize time series by quarter or year; show denominator and sample size for every period.
4. Compare broad locations only where sample sizes are adequate.
5. Build a skill co-occurrence graph separately for IT and BA. Use posting-level skill sets; apply minimum support and report normalized association (e.g., Jaccard or lift) alongside counts.
6. Identify high-frequency and emerging skills with a transparent rule (for example, a rise in posting prevalence over consecutive periods plus a minimum count). Treat this as descriptive, not forecasting.
7. Check sensitivity to duplicate removal, language group, threshold, and alternative skill extraction systems.

**Deliverables**
- Skill ranking tables by role and period.
- Trend charts with denominators.
- Separate IT and BA co-occurrence graphs.
- Robustness and limitations summary.

### Phase 8 — Interpretation, report, and presentation (Weeks 8–9)

**Tasks**
1. Answer each research question using the evaluated extraction output.
2. Separate observed results from interpretation; distinguish tool mentions from demonstrated competence.
3. Discuss source coverage, changing platform coverage, duplicates, language, taxonomy mismatch, and model error.
4. Document data license, citations, processing choices, and whether raw text can be shared.
5. Prepare report, figures, and a short presentation with reproducibility instructions.

**Deliverables**
- Final report and presentation.
- Code, configuration, vocabulary, and permitted aggregate outputs.
- README with environment, commands, source citation, and known limitations.

## D. Suggested division of work for a four-person team

| Team member | Primary responsibility | Concrete outputs |
|---|---|---|
| Member 1 — Data and provenance | Source search, permissions/license audit, acquisition, data dictionary, deduplication, cleaning | Source register, clean dataset, data quality report, cleaning code |
| Member 2 — Job-family classification | Define IT/BA boundaries, label titles, build rules and optional classifier, evaluate role classification | Annotation guide, title labels, role model and metrics |
| Member 3 — Skills and NLP | Build bilingual vocabulary, annotation, implement dictionary and PhoBERT/XLM-R extraction comparison | Skill vocabulary, gold spans, extraction code and model evaluation |
| Member 4 — Mining and communication | Frequency/trend/co-occurrence analysis, visualizations, robustness, integrate report and presentation | Tables, trend plots, networks, report/presentation draft |

**Shared responsibilities:** All members review the source terms and scope; at least two members double-label annotation samples; all members review error analysis and final claims. Member 4 coordinates integration but should not be solely responsible for verifying other members’ results.

For a smaller team, merge responsibilities as follows: a three-person team combines roles 1+2, while a two-person team combines 1+2 and 3+4. For an individual project, complete phases in sequence and omit optional models before omitting manual evaluation.

## E. Recommended minimum viable version

If time or compute is limited, complete this version:

1. One permitted Vietnam dataset with verified date coverage, ideally 2020–2025.
2. Two broad groups: IT and BA, with no more than a few validated subgroups.
3. A bilingual dictionary baseline and manually evaluated sample.
4. One neural extraction model (PhoBERT if Vietnamese dominates; XLM-R if mixed language dominates) only if annotation resources permit.
5. Posting-level skill prevalence, yearly or quarterly trends with denominators, and separate IT/BA co-occurrence graphs.
6. A clear report of source limitations and no unsupported claim about all Vietnamese vacancies.

## F. Recommended model stack

**Primary pipeline:** title rules → manually validated IT/BA labels → bilingual phrase matcher → PhoBERT BIO skill extractor → alias-to-canonical mapping → frequency/trend and co-occurrence analysis.

**Comparison pipeline:** TF–IDF + linear SVM or logistic regression for title classification; XLM-R token classifier as an optional bilingual comparison; dictionary-only skill extraction as the interpretable baseline.

Keep occupation classification and skill-span extraction as separate tasks: the first labels what kind of job a posting describes; the second finds skill mentions inside its text. This separation makes each model’s purpose and evaluation clear.

## G. Data-source and taxonomy references

- VietJobs dataset paper: [VietJobs: A Vietnamese Job Advertisement Dataset](https://arxiv.org/abs/2603.05262). Its abstract reports 48,092 postings from Vietnam and structured job fields; inspect the release itself for exact dates, license, and field availability.
- VietJobs-37K release and benchmark code: [VieJobBERT repository](https://github.com/kaldlabs/VieJobBERT). The repository describes 37,274 Vietnamese-dominant postings and links to its canonical Zenodo dataset record. Check the dataset record’s terms and field documentation before reuse.
- Vietnam historical-feed option: [Techmap Vietnam job posting data](https://jobdatafeeds.com/data/countries/vn). The provider advertises records since January 2020, and lists a paid historical product; confirm academic use terms and exact coverage.
- ESCO download/API: [European Commission ESCO access](https://esco.ec.europa.eu/en/use-esco). ESCO is available as linked open data and downloadable files, but the listed language packs do not include Vietnamese.
- O*NET licensing: [O*NET license agreements](https://www.onetcenter.org/license_agreements.html). Check the specific database or API license and attribution requirements for the material used.

---

# Execution checklist and parallel-work plan

This checklist turns the phases above into assignable tasks. Task IDs are used in the dependency column. Tasks can run in parallel only when their listed prerequisites are complete and the team agrees on shared definitions and file formats.

## 1. Task dependency overview

```text
A. Scope and feasibility
        ↓
B. Dataset verification and acquisition
        ↓
C. Data profiling and cleaning
   ┌────┴────────┐
   ↓             ↓
D. IT/BA labels  E. Skill vocabulary + annotation guide
   ↓             ↓
F. Role model    G. Skill extraction models
   └──────┬──────┘
          ↓
H. Final validated analysis dataset
          ↓
I. Trends + co-occurrence + robustness (parallel analyses)
          ↓
J. Interpretation, report, presentation, reproducibility review
```

D and E can proceed at the same time after the first data sample is available. F and G can proceed in parallel after their respective labels are ready. The analysis branches in I can run in parallel after H. Do not begin final trend interpretation before checking source coverage by year, role, and language.

## 2. Detailed task register

### Step A — Scope and feasibility

| ID | Task | Detailed work | Depends on | Can run in parallel? | Completion evidence |
|---|---|---|---|---|---|
| A1 | Define target population | Define an eligible posting as a job advertised for work in Vietnam, with title/description sufficient to classify. Decide treatment of remote roles, internships, contract roles, staffing agencies, and reposts. | — | Yes, with A2–A4 | Inclusion/exclusion rules |
| A2 | Define role families | List IT subgroups and BA subgroups. Decide whether Data Analyst, Product Owner, Systems Analyst, Project Manager, and Business Intelligence Analyst count as IT, BA, both, or outside scope. | — | Yes, with A1, A3, A4 | Role mapping table |
| A3 | Define time and geography | Set intended period to 2020–2025. Define fallback if data does not cover all years. Select province/city grouping and decide whether national results are primary. | — | Yes, with A1, A2, A4 | Time/geography specification |
| A4 | Finalize research questions | Confirm questions on skill prevalence, skill combinations, changes over time/location, and extraction accuracy. Define which are primary versus optional. | — | Yes, with A1–A3 | Final question list |
| A5 | Define feasibility thresholds | Agree on minimum usable postings per year and role, minimum text length, and minimum support for reporting a skill or co-occurrence edge. These are analysis rules, not performance targets. | A1–A4 | No; needs scope alignment | Written thresholds |
| A6 | Freeze scope version 1 | Combine A1–A5 in a short scope memo; log later changes with reasons. | A1–A5 | No | Approved scope memo |

**Parallel work in Step A:** A1–A4 can be drafted concurrently by different team members. A5 and A6 require a short shared review because their choices affect sampling and analysis.

### Step B — Dataset verification and acquisition

| ID | Task | Detailed work | Depends on | Can run in parallel? | Completion evidence |
|---|---|---|---|---|---|
| B1 | Search candidate sources | Check academic releases, university/lab archives, instructor resources, commercial historical feeds, and permitted APIs. Record stable source links and retrieval date. | A1–A4 | Yes, with B2–B4 | Candidate source list |
| B2 | Check license and access terms | Inspect dataset license, API terms, redistribution limits, attribution, and whether derived aggregate results may be published. Do not infer permission from public visibility. | B1 | Yes, each source can be checked separately | Source permissions register |
| B3 | Check schema and provenance | Record fields, source portals, collection method, duplicate handling, language, date coverage, geographic coverage, and whether full text is provided. | B1 | Yes, with B2 | Dataset field/provenance notes |
| B4 | Inspect sample or data dictionary | Load a small permitted sample, if available; estimate eligible IT/BA records per year and identify missing fields. | B2–B3 | Yes, across sources | Feasibility counts and sample audit |
| B5 | Select primary source | Compare sources against scope, period, permissions, cost, field quality, and reproducibility. Choose one primary source; list any supplementary source separately. | B2–B4 | No | Source decision record |
| B6 | Acquire and preserve raw data | Download or query through the permitted route. Preserve an unchanged raw copy where terms allow; record version, date, query, and checksum. Restrict access if the license requires it. | B5 | No | Raw data or reproducible access record |
| B7 | Decide time-window fallback | If historical years are missing or inconsistent, shorten the window or reframe as a snapshot; update the scope memo and research questions. | B4–B6 | No | Final study period decision |

**Parallel work in Step B:** B2 and B3 can be performed at the same time for each candidate. B4 can be carried out for multiple candidates concurrently. B5–B7 are decision points and should happen after the evidence is assembled.

### Step C — Data profiling and cleaning

| ID | Task | Detailed work | Depends on | Can run in parallel? | Completion evidence |
|---|---|---|---|---|---|
| C1 | Build a raw-data inventory | Count records/files, fields, date range, source portals, languages, and file sizes. | B6 | Yes, with C2 | Inventory table |
| C2 | Profile field quality | Measure missingness, invalid dates, text lengths, malformed encoding, salary-field completeness, and location/title consistency. Break down by year and source. | B6 | Yes, with C1 | Profiling report |
| C3 | Standardize core fields | Create consistent names/types for posting ID, title, description, date, location, source, language, salary, and role label. Preserve raw fields separately if allowed. | C1–C2 | Yes, different fields can be mapped in parallel | Field mapping script |
| C4 | Deduplicate postings | Remove exact duplicate records; flag likely reposts using normalized title, company/source, location, date proximity, and text similarity. Define which records remain and why. | C1–C2 | No; use shared deduplication rules | Duplicate report and clean IDs |
| C5 | Normalize dates and locations | Parse dates into ISO format and derive year/quarter. Map locations to broad regions; retain unknown/ambiguous values. | C3 | Yes, with C4 | Standardized date/location fields |
| C6 | Detect language and mixed text | Apply a language detector or documented rules; manually review a sample of Vietnamese, English, and mixed postings. | C3 | Yes, with C4–C5 | Language labels and audit |
| C7 | Remove unnecessary personal data | Detect contact details and personal names where practical; remove/mask only fields not needed for analysis and permitted by the data terms. | C3 | Yes, with C4–C6 | Privacy-cleaning log |
| C8 | Produce cleaning audit | Record row counts after each filter, missingness, duplicate decisions, exclusions, and known data limitations. | C4–C7 | No | Clean dataset v1 and audit report |

**Parallel work in Step C:** C1 and C2; then C4, C5, C6, and C7 can be divided across team members once C3’s field map is stable. C8 integrates all outputs.

### Step D — IT and BA job-family identification

| ID | Task | Detailed work | Depends on | Can run in parallel? | Completion evidence |
|---|---|---|---|---|---|
| D1 | Draft title taxonomy | Build candidate title groups and aliases, with rules for ambiguous roles such as data/business intelligence analyst, systems analyst, product analyst, and QA analyst. | A2, C3 | Yes, with E1 | Taxonomy v1 |
| D2 | Sample and label titles | Stratify titles across years, sources, and languages. Label IT, BA, both, other, or uncertain using the agreed guide. | D1, C8 | Yes, with E2 | Labeled title sample |
| D3 | Measure label agreement | Have a second reviewer label a subset; calculate agreement and resolve disagreements. Revise guidance if needed. | D2 | No | Agreement and adjudication notes |
| D4 | Implement transparent rules | Build keyword/title rules and context checks for the baseline role classifier. | D1–D3 | Yes, with D5 after labels exist | Rule-based labels |
| D5 | Train optional role classifier | Compare TF–IDF with logistic regression/linear SVM; optionally fine-tune PhoBERT or XLM-R if labeled data is sufficient. Use grouped or temporal splits. | D2–D3 | Yes, with D4 | Trained model and predictions |
| D6 | Evaluate and finalize role labels | Report macro-F1, per-class precision/recall/F1, confusion matrix, and uncertain cases. Correct only through documented adjudication. | D4–D5 | No | Final role-labeled dataset |

### Step E — Skill vocabulary and annotation

| ID | Task | Detailed work | Depends on | Can run in parallel? | Completion evidence |
|---|---|---|---|---|---|
| E1 | Pilot-read postings | Review postings from IT/BA, multiple years, locations, and languages. Note skill phrases, aliases, spelling variants, and context traps. | A2, C8 | Yes, with D1 | Pilot notes |
| E2 | Define skill categories | Agree categories for technical skills, tools, methods, platforms, BA practices, domain skills, and soft skills. State whether certifications/education are in or out. | E1 | No | Category schema |
| E3 | Prepare taxonomy references | Inspect relevant ESCO/O*NET or VietJobs taxonomy entries. Use as references; record source/license and known geographic/language mismatch. | E1 | Yes, with E2 | Reference mapping file |
| E4 | Build canonical vocabulary | Add canonical label, aliases, language, category, source/rationale, and ambiguity notes. Have a domain-aware reviewer inspect it. | E2–E3 | No | Vocabulary v1 |
| E5 | Write span annotation guide | Specify what counts as a skill, span boundary rules, required vs preferred distinction, negation, lists, acronyms, and ambiguous mentions. | E2–E4 | No | Annotation guide v1 |
| E6 | Sample and annotate postings | Stratify by IT/BA, period, and language. Label exact skill spans and canonical labels; double-label a subset. | E5, C8 | Annotation can be divided among members | Gold annotation dataset |
| E7 | Adjudicate annotations | Resolve disagreements, measure agreement, update the guide, and freeze a gold evaluation subset. | E6 | No | Adjudicated gold set and agreement report |

**Parallel work between D and E:** D1 and E1 may start together. After initial profiling, team members can label titles and pilot-read descriptions concurrently. Keep job family and skill categories distinct so title decisions do not silently change skill annotation rules.

### Step F — Skill extraction models

| ID | Task | Detailed work | Depends on | Can run in parallel? | Completion evidence |
|---|---|---|---|---|---|
| F1 | Create data splits | Split by posting and group likely duplicates together. Keep an untouched evaluation set; optionally reserve the latest year for temporal testing. | C8, D6, E7 | No | Split IDs and rationale |
| F2 | Implement dictionary baseline | Use canonical vocabulary and aliases, boundary-aware matching, context exclusions, and matched-span logging. | E4–E5 | Yes, with F3 | Baseline predictions |
| F3 | Prepare tokenized model data | Convert gold spans to BIO tags; define tokenization/alignment rules for Vietnamese accents, punctuation, acronyms, and English technology terms. | E7 | Yes, with F2 | Model-ready train/dev/test data |
| F4 | Train traditional sequence model (optional) | Train CRF or BiLSTM-CRF with word/character features if the course requires a traditional neural/statistical sequence model. | F1, F3 | Yes, with F5 | Traditional-model predictions |
| F5 | Fine-tune transformer | Train PhoBERT for Vietnamese-dominant postings or XLM-R for substantially multilingual text. Use the same split and tuning budget; record parameters and seeds. | F1, F3 | Yes, with F4 | Transformer predictions and model card |
| F6 | Normalize extracted forms | Map extracted surface spans to canonical labels with exact alias rules; optionally rank unresolved candidates using embeddings, then manually validate. | F2 and/or F4–F5, E4 | Can start for baseline while model training runs | Canonicalized predictions |
| F7 | Evaluate extraction | Calculate exact-span and overlap precision/recall/F1, canonical-skill micro/macro F1, per-role and per-language performance, and support. | F6, F1 | No | Evaluation table |
| F8 | Error analysis and freeze model | Review false positives/negatives, identify errors by skill/language/role, make only documented changes, then freeze chosen predictions for mining. | F7 | No | Error report and final predictions |

**Parallel work in Step F:** F2 and F3 can run concurrently. F4 and F5 can be developed in parallel if compute/time permits. Do not compare final metrics until data splits, annotation rules, and normalization rules are shared and frozen.

### Step G — Demand, trend, and network analysis

| ID | Task | Detailed work | Depends on | Can run in parallel? | Completion evidence |
|---|---|---|---|---|---|
| G1 | Build analysis table | One row per posting-skill with canonical skill, role, period, location, language, and source metadata; keep posting-level presence for prevalence. | F8, D6, C8 | No | Analysis-ready table |
| G2 | Overall and role frequency | Calculate unique-posting counts and posting prevalence for each skill overall, IT, BA, and supported subgroups. | G1 | Yes, with G3–G5 | Ranked tables and charts |
| G3 | Time comparison | Aggregate by year or quarter; show denominators, missingness, and source composition. Check whether a change in source coverage explains apparent movement. | G1, B7 | Yes, with G2, G4, G5 | Trend table and plots |
| G4 | Location comparison | Compare broad locations only when sample sizes pass A5 thresholds; keep unknown separate. | G1 | Yes, with G2, G3, G5 | Location tables/plots |
| G5 | Co-occurrence networks | Build separate IT and BA graphs. Count posting-level pairs; calculate support plus Jaccard or lift; test a documented minimum threshold; label/interpret clusters. | G1 | Yes, with G2–G4 | Pair tables and network figures |
| G6 | Robustness checks | Repeat key results with dictionary-only versus selected final extractor, alternate duplicate filters, language subsets, and edge thresholds. | G2–G5, F8 | Different checks can run in parallel | Robustness comparison |
| G7 | Synthesize findings | Answer each research question, note uncertainty and extraction errors, and avoid generalizing beyond source coverage. | G2–G6 | No | Findings memo |

### Step H — Report, presentation, and reproducibility

| ID | Task | Detailed work | Depends on | Can run in parallel? | Completion evidence |
|---|---|---|---|---|---|
| H1 | Draft methods and data sections | Document source, license, time window, sampling, cleaning, labels, models, splits, metrics, and tools. | B5–B7, C8, D6, E7, F8 | Yes, with H2 | Methods draft |
| H2 | Prepare figures and result narratives | Create final charts/tables with clear denominators and captions; document network thresholds and interpretation. | G2–G7 | Yes, with H1 | Figure set and results draft |
| H3 | Write limitations and ethics | Cover source and temporal coverage, language, occupational taxonomy, privacy, duplicate handling, model bias, and permitted sharing. | B2, C8, F7, G7 | Yes, with H1–H2 | Limitations section |
| H4 | Integrate report | Combine sections, check that every claim matches a table/figure and every method is reproducible. | H1–H3 | No | Complete report draft |
| H5 | Reproducibility review | A teammate follows README from a clean environment or reruns core analysis; verify source citations, versions, fixed random seeds, and output paths. | H4 | No | Reproduction checklist |
| H6 | Prepare presentation | Summarize question, data, approach, evaluation, findings, and limits; rehearse timing. | H4–H5 | Slides can be drafted while H5 runs, final facts depend on H4 | Presentation deck |
| H7 | Final consistency review and submission | Check terminology, dates, source permissions, metric values, figure labels, citations, and required course format. | H5–H6 | No | Final submission package |

## 3. Explicit parallel-work schedule

| Work window | Tasks that can be done in parallel | Shared dependency or coordination point |
|---|---|---|
| Week 1 | A1–A4; B1 source search can begin once provisional scope exists | Meet to freeze A6 before selecting data |
| Week 2 | B2 license checks and B3 schema/provenance checks for each source; inspect candidate samples in parallel | B5 source choice requires all evidence; one person records decisions centrally |
| Week 3 | C1/C2 profiling; after field mapping, divide C4 deduplication, C5 location/date work, C6 language audit | Agree common IDs, schemas, and exclusion rules before branches merge |
| Week 4 | D1 role taxonomy and E1 skill pilot can proceed concurrently; D2 and E annotation prep can be divided after sample selection | Shared posting sample and annotation formats |
| Week 5 | D4 rule baseline and E4 vocabulary review; E6 annotation can be divided across annotators | Final role/skill definitions and versioned labels |
| Week 6 | F2 dictionary baseline and F3 BIO data preparation; optional F4/F5 model implementations can run concurrently | Freeze splits and gold annotations first |
| Week 7 | G2 frequency, G3 trends, G4 location, and G5 network analyses can be assigned to different people | Use one frozen analysis table and shared thresholds |
| Week 8 | G6 robustness checks; H1 methods writing, H2 figures, and H3 limitations can be drafted concurrently | Freeze final predictions and results before final report integration |
| Week 9 | H4 integration, H5 reproducibility review, H6 presentation | Final values/claims must be synchronized before submission |

## 4. Suggested four-person assignment by task ID

| Person | Main tasks | Backup/review tasks |
|---|---|---|
| 1 — Data lead | B1–B7, C1–C8, G1 | Review source claims and final data limitations |
| 2 — Occupation classification lead | A2, D1–D6 | Double-label role sample; review IT/BA boundary cases |
| 3 — NLP and annotation lead | E1–E7, F1–F8 | Coordinate second annotator and model error review |
| 4 — Analysis and writing lead | A4–A6, G2–G7, H1–H7 | Integrate report and figures; verify denominator and claim consistency |

All members should participate in scope freeze, sample annotation, results review, and final presentation. The named leads own implementation and documentation, not unilateral decisions about ambiguous labels or conclusions.

## 5. Coordination rules to keep parallel work compatible

1. Keep one shared scope memo, one data dictionary, one role-label guide, one skill-label guide, and one versioned vocabulary.
2. Use generated posting IDs in every derived file; never rely on row order to join team outputs.
3. Store each task’s input version, output version, code/notebook, and decisions in a simple task log.
4. Freeze annotation rules and train/dev/test IDs before comparing models.
5. Give each analysis branch the same frozen analysis table and record its own filtering thresholds.
6. Merge outputs only after the task owner has supplied the artifact and another member has reviewed it.
7. When data access or license checks fail, pause dependent acquisition/analysis tasks and use the scope fallback in B7; independent work on taxonomy design, annotation guides, and report structure may continue.
