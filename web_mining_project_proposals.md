# Web Mining Project Proposals

These five proposals are independent alternatives. Each is scoped as a Web Mining project and includes research questions, a practical methodology, and an evaluation plan.

## 1. Detecting Coordinated Fake Product Reviews Using Text and Reviewer–Product Networks

### Abstract

Online reviews influence purchasing decisions, but suspicious reviews can distort consumers’ perceptions. This project proposes a system for detecting potentially coordinated fake reviews by combining review text with behavioral and network signals. It will compare text-based classification with methods that also use relationships among reviewers, products, and review activity. The goal is to determine whether combining these signals improves detection over text-only approaches.

### Problem and objectives

A review may appear genuine when examined by itself, even if it was posted as part of a coordinated campaign. Text-only systems may also struggle with short, vague, or deliberately varied reviews. This project will:

- Classify reviews as suspicious or genuine using text features.
- Build reviewer–product graphs and extract network or behavioral features.
- Compare text-only, graph-based, and combined approaches.
- Identify which features contribute most to detection.

### Research questions

1. Do reviewer–product network features improve fake-review detection over text alone?
2. Which signals—text, posting patterns, or graph structure—are most useful?
3. How well do the models generalize to products or reviewers not seen during training?

### Methodology and evaluation

Use a labeled public benchmark such as YelpChi, subject to confirming its suitability and terms of use. Preprocess review text, then build a graph linking reviewers to businesses or products. Train and compare a text classifier, a model using behavioral and graph features, and a combined model. Evaluate using precision, recall, F1, and PR-AUC; report results for held-out reviewers or products as well as a standard test split.

### Expected outcomes and scope

The project will produce a reproducible comparison of review-detection strategies, a description of important signals, and a prototype for ranking suspicious reviews. The system should be presented as a research tool, not as definitive proof that a particular reviewer or review is fraudulent.

## 2. Mining Skill Demand from Online Job Postings

### Abstract

Job postings reveal how employers describe roles and which skills they seek. This project proposes a Web Mining pipeline to extract skills, locations, experience requirements, and salary information from online job-posting data. It will analyze which skills commonly appear together and how demand changes over time. The project aims to create an interpretable view of the relationship between job roles and skill demand.

### Problem and objectives

Job requirements are often written as unstructured text, with inconsistent names for similar skills. This makes it difficult to compare roles or track changing demand. The project will:

- Extract skills and job attributes from postings.
- Normalize spelling variants and aliases for the same skill.
- Analyze skill frequencies and co-occurrence patterns by role, location, and time.
- Identify skill clusters and changes in demand.

### Research questions

1. Which skills are most frequently requested for selected job families?
2. Which skills tend to appear together, and do these combinations vary by role?
3. How does skill demand change across locations or time periods?

### Methodology and evaluation

Start with a public job-posting dataset whose license permits research use, or a source/API whose terms allow collection. Extract candidate skills using phrase matching and, if time permits, a named-entity recognition model. Normalize extracted terms using a documented skill vocabulary such as O*NET, where applicable. Represent skills as a co-occurrence network and analyze its clusters and central skills. Manually annotate a sample of postings to evaluate extraction precision, recall, and F1; compare trend results against simple frequency-count baselines.

### Expected outcomes and scope

The project will produce a job-posting analysis pipeline, a skill co-occurrence graph, and visualizations of demand by role or location. To keep the work manageable, select a small number of job families and a defined time period. Avoid collecting personal information; use only posting content that is permitted by the dataset or source terms.

## 3. Mapping Third-Party Tracking Relationships Across Websites

### Abstract

Many websites load scripts and other resources from external domains. These connections can form a network of relationships between websites and third-party services, including analytics and advertising trackers. This project proposes crawling a limited set of public websites, recording their external connections, and analyzing the resulting website–domain graph. It will investigate how tracker prevalence and network structure vary across website categories.

### Problem and objectives

A website’s visible content does not reveal all of the external services it contacts. Mapping these connections can help describe the structure of the web and its dependence on third parties. This project will:

- Record external domains contacted by selected websites during page loads.
- Identify domains that match a maintained public tracker list.
- Build and analyze a bipartite graph of websites and external domains.
- Compare tracking patterns across website categories.

### Research questions

1. Which third-party domains are most commonly contacted by the sampled websites?
2. Do website categories differ in the number or types of third parties they contact?
3. Are there highly connected third-party domains that link otherwise unrelated websites?

### Methodology and evaluation

Select a modest, predefined sample of public websites and record page-load network requests using a browser automation tool. Classify contacted domains using a public tracker list and keep unclassified domains distinct rather than labeling them automatically as trackers. Construct a bipartite graph and calculate measures such as domain frequency, website degree, and network communities. Validate the domain classification on a manually inspected sample and document browser settings and crawl conditions for reproducibility.

### Expected outcomes and scope

The project will produce a website–third-party relationship graph, category-level comparisons, and a summary of highly connected domains. Limit the crawl to public pages, use low request rates, respect robots.txt and applicable terms, and do not bypass access controls or collect user-specific data.

## 4. Comparing News Coverage of the Same Events Across Sources

### Abstract

News organizations may report on the same event while differing in the amount, timing, and topics of their coverage. This project proposes using public news metadata to identify events and compare their coverage across sources over time. It will apply Web Mining methods to group articles by event and analyze source–event relationships, rather than recommending articles to individual readers.

### Problem and objectives

Large volumes of news make it difficult to see how coverage of a topic varies between publishers or over time. This project will:

- Collect news records, such as headlines, timestamps, source names, and URLs.
- Group articles into event or topic clusters.
- Compare the volume and timing of coverage between selected sources.
- Visualize source–event relationships and changes over time.

### Research questions

1. Which events receive the most coverage from the selected sources?
2. How do coverage volume and publication timing differ between sources?
3. Can article clustering identify shared events more effectively than keyword matching alone?

### Methodology and evaluation

Use a public source such as the GDELT dataset or API, after checking access conditions and the fields available for the chosen period. Cluster articles using headline or available text features, with a keyword-based grouping method as a baseline. Build a graph connecting sources and event clusters, then compare coverage counts and timing. Manually label a sample of article pairs or clusters to evaluate grouping quality using precision, recall, and F1.

### Expected outcomes and scope

The project will provide event clusters, source–event visualizations, and a reproducible comparison of coverage patterns. To keep the analysis focused, choose a limited time period, a manageable set of sources, and one or two topics. Treat the results as a comparison of observed coverage, not as a definitive judgment of bias or journalistic intent.

## 5. Tracking Emerging Topics in Vietnamese Online Discussions

### Abstract

Public online discussions can reveal which issues attract attention and how conversations evolve. This project proposes a Web Mining pipeline to identify emerging topics in Vietnamese-language discussions and track their prevalence over time. It will compare topic-discovery methods and examine how topics grow, persist, or fade in a selected public corpus.

### Problem and objectives

Keyword searches can miss new topics when people use different wording, while static topic models may not capture changes over time. Vietnamese text also presents challenges such as word segmentation, slang, abbreviations, and spelling variation. This project will:

- Collect a research-permitted corpus of Vietnamese public discussions.
- Clean and normalize text while documenting each preprocessing step.
- Group posts into topics and track their frequency over time.
- Compare automatically discovered topics with manually labeled examples.

### Research questions

1. Which topics emerge or increase in activity during the selected period?
2. Do embedding-based topic methods produce more coherent topics than a keyword or traditional topic-modeling baseline?
3. How sensitive are the results to Vietnamese text normalization and preprocessing?

### Methodology and evaluation

First identify a dataset or platform that explicitly permits research use; confirm its access terms before collecting data. Preprocess Vietnamese text, then compare a frequency-based baseline with a topic-modeling or embedding-based approach. Track topic volume across fixed time intervals. Evaluate topic quality using human judgments on a small sample and quantitative measures such as topic coherence; report limitations caused by sampling, language variation, and platform coverage.

### Expected outcomes and scope

The project will produce a topic timeline, representative terms or posts for each topic, and a comparison of topic-discovery approaches. Restrict analysis to public content permitted by the source, minimize stored personal information, and avoid presenting individual users as representative of broader public opinion.

## Suggested choices

- **Topic 2** is a strong option for a practical, measurable project.
- **Topic 3** is a good choice if you want to emphasize web structure.
- **Topic 5** is a promising option if you can secure a permitted Vietnamese-language dataset.
