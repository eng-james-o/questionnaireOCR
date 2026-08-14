# Analysis Suggestion Engine Specification

The **Analysis Suggestion Engine** is an intelligent subsystem within QuestionnaireOCR designed to bridge data collection and statistical analysis. By parsing research goals, objectives, and research questions alongside extracted questionnaire data schema, the engine automatically recommends appropriate statistical and machine learning methodologies.

---

## 🏛 Architecture & Key Components

```
 ┌───────────────────────────┐      ┌───────────────────────────┐
 │ Project Title &           │      │ Extracted Questionnaire   │
 │ Objectives / Questions    │      │ Data & Column Schemas     │
 └─────────────┬─────────────┘      └─────────────┬─────────────┘
               │                                  │
               ▼                                  ▼
 ┌───────────────────────────┐      ┌───────────────────────────┐
 │  NLU Processing Module    │      │ Data Variable Profiler    │
 │  (Intent & Scope Parsing) │      │ (Scale, Distribution, N)  │
 └─────────────┬─────────────┘      └─────────────┬─────────────┘
               │                                  │
               └────────────────┬─────────────────┘
                                │
                                ▼
               ┌─────────────────────────────────┐
               │     Goal Taxonomy Engine        │
               │   (Knowledge Base Matching)     │
               └────────────────┬────────────────┘
                                │
                                ▼
               ┌─────────────────────────────────┐
               │    Automated Recommendation     │
               │     & Report Generator          │
               └─────────────────────────────────┘
```

---

## 💡 Core Features

### 1. Goal Taxonomy Knowledge Base
Maintains a structured, extensible taxonomy mapping domain-specific research objectives to analytical techniques:

* **Descriptive & Exploratory Analysis**: Summary statistics, frequency distributions, cross-tabulations.
* **Comparative & Hypothesis Testing**:
  * *Two Groups*: Independent t-test, Mann-Whitney U test.
  * *Multiple Groups*: One-Way ANOVA, Kruskal-Wallis test.
  * *Paired / Repeated Measures*: Paired t-test, Wilcoxon signed-rank test.
* **Relational & Predictive Modeling**:
  * Pearson/Spearman Correlation, Linear Regression, Logistic Regression, Multiple Regression.
* **Dimensionality Reduction & Clustering**:
  * Principal Component Analysis (PCA), Exploratory Factor Analysis (EFA), K-Means Clustering.
* **Textual & Qualitative Analysis**:
  * Sentiment Analysis, Topic Modeling (LDA), Word Frequency Analysis for open-ended response fields.

### 2. Natural Language Understanding (NLU) Processing
Analyzes user inputs (Project Title, Research Objectives, Research Questions):
* **Keyword & Entity Extraction**: Identifies key verbs and intent indicators (e.g., "compare", "predict", "impact of", "relationship between", "evaluate satisfaction").
* **Variable Mapping**: Correlates research questions with specific survey variables extracted from the questionnaire schema.
* **Study Scope Categorization**: Classifies the study type (Exploratory, Explanatory, Descriptive, Causal, Evaluative).

### 3. Automated Recommendations System
Generates tailored, actionable analytical recommendations:
* **Technique Suitability Scoring**: Ranks statistical tests based on variable measurement scales (Nominal, Ordinal, Interval, Ratio) and sample size ($N$).
* **Assumption Checks Guidance**: Warns about underlying assumptions (e.g., normality testing, homoscedasticity) before applying parametric models.
* **Actionable Analytical Plan**: Generates a step-by-step report guiding the researcher on how to execute suggested tests in Python/R/SPSS to directly answer their research questions.
