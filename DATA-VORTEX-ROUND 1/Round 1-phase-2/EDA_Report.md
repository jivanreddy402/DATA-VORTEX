# DATA VORTEX — Round 1
## Rebuilding the Social Engine
### Exploratory Data Analysis Report

---

## 1. Objective

The objective of this analysis is to recover, clean and understand the corrupted social-media dataset provided for DATA VORTEX Round 1.

The analysis focuses on:

- Data quality assessment
- Duplicate detection and removal
- Missing-value analysis
- Anomaly identification and recovery
- Timestamp standardization
- Engagement analysis
- Platform-level comparison
- Temporal behavior analysis
- User-level behavioral analysis
- Correlation analysis

No values were artificially fabricated during preprocessing.

---

## 2. Dataset Overview

The original corrupted posts dataset contained:

- 12,360 rows
- 8 columns

The user profile dataset contained:

- 1,500 users
- 5 columns

The posts dataset contains information about:

- Post ID
- User ID
- Platform
- Text content
- Timestamp
- Likes
- Shares
- Comments

---

## 3. Data Quality Issues Identified

The following issues were identified in the corrupted dataset:

### Missing Values

Missing values were present in:

- Platform
- Text content
- Likes

No missing values were identified in the user dataset.

### Duplicate Records

The original dataset contained exact duplicate rows.

Duplicate `post_id` groups were investigated before removal.

Every duplicated `post_id` group contained identical values across the available columns. Therefore, removing the exact duplicate rows was considered safe and reproducible.

### Negative Likes

Negative values were found in the `likes` column.

The absolute values of these negative likes were within the valid engagement range of the dataset, strongly indicating a sign-flip corruption pattern.

Therefore, negative likes were converted to their absolute values.

The original values were retained in the audit dataset together with a flag indicating that the value was recovered.

### Mixed Timestamp Formats

The timestamp column contained multiple representations including:

- Day-Month-Year formatted dates
- Unix timestamps
- ISO timestamp strings

These values were successfully converted into a consistent datetime representation.

### HTML Encoded Text

HTML entities such as `&amp;` were present in text content.

These entities were decoded during preprocessing.

---

## 4. Cleaning Strategy

The following preprocessing decisions were applied:

| Issue | Treatment |
|---|---|
| Exact duplicate rows | Removed |
| Duplicate post IDs with identical records | Removed |
| Negative likes | Converted to absolute values |
| Missing likes | Preserved |
| Missing text | Preserved |
| Missing platform | Preserved unless deterministically recoverable |
| Mixed timestamps | Standardized to datetime |
| HTML entities | Decoded |
| User references | Validated against user dataset |

Missing values were not replaced with invented values because the available data did not provide sufficient evidence for reliable reconstruction.

---

## 5. Final Dataset Quality

After cleaning:

- Final posts: 12,000
- Duplicate rows: 0
- Duplicate post IDs: 0
- Negative likes: 0
- Invalid timestamps: 0
- Remaining HTML entities: 0

The cleaned dataset therefore provides a consistent foundation for exploratory analysis and the next SQL phase.

---

## 6. Engagement Metric

For meaningful engagement analysis, a complete engagement metric was created:

`likes + shares + comments`

Rows with missing engagement components were not treated as zero.

Instead, `engagement_complete` was calculated only when all three engagement components were available.

This prevents missing likes from being incorrectly interpreted as zero engagement.

The current analysis contains:

- 10,186 posts with complete engagement values
- 1,814 posts with incomplete engagement values

---

## 7. Platform Analysis

Among posts with complete engagement values:

| Platform | Posts | Complete Engagement Posts | Average Engagement |
|---|---:|---:|---:|
| Instagram | 1,989 | 1,693 | 4,040.02 |
| YouTube | 2,073 | 1,747 | 4,031.84 |
| Facebook | 2,074 | 1,755 | 4,015.99 |
| Reddit | 2,031 | 1,742 | 4,003.94 |
| Twitter | 2,049 | 1,725 | 3,951.91 |

### Insight

Instagram has the highest average engagement per post at approximately **4,040**.

Twitter has the lowest average among the five platforms at approximately **3,952**.

However, the difference between platforms is relatively small, suggesting that platform alone may not explain engagement behavior.

---

## 8. Engagement Components

The engagement data consists of:

- Likes
- Shares
- Comments

Likes represent the largest engagement component in the dataset.

This indicates that reactions through likes form a major part of overall social interaction.

However, missing likes exist in the original dataset, so engagement-component interpretation should be considered together with data completeness.

---

## 9. Correlation Analysis

The correlation analysis produced approximately:

| | Likes | Shares | Comments |
|---|---:|---:|---:|
| Likes | 1.000 | -0.001 | 0.010 |
| Shares | -0.001 | 1.000 | 0.024 |
| Comments | 0.010 | 0.024 | 1.000 |

### Insight

The engagement variables show extremely weak linear correlation.

In particular:

- Likes and shares: approximately -0.001
- Likes and comments: approximately 0.010
- Shares and comments: approximately 0.024

This suggests that receiving many likes does not necessarily mean that a post will also receive many shares or comments.

---

## 10. Temporal Analysis

The dataset was analyzed across:

- Month
- Day of week
- Hour of day
- Day-hour combinations

Wednesday showed the highest average engagement among the days of the week in the current analysis.

---

## 11. Best Posting Window

To avoid selecting a time slot based on a very small number of observations, only slots with at least 50 complete engagement records were considered reliable.

The strongest reliable posting window was:

### Wednesday — 7:00 PM

Average engagement:

**4,420.70**

Complete posts:

**56**

This provides a stronger basis for recommendation than selecting a slot with very few observations.

---

## 12. User Behaviour Analysis

Post-level engagement was combined with the user profile dataset to investigate behavioral patterns.

The analysis considered:

- Post frequency
- Average engagement
- Total engagement
- Average likes
- Average shares
- Average comments
- Follower count
- Location
- Language

This allows engagement behavior to be studied not only by platform and time, but also by user characteristics.

---

## 13. Key Findings

### Finding 1 — Instagram leads average engagement

Instagram recorded the highest average engagement per post among the analyzed platforms.

### Finding 2 — Platform differences are relatively small

The gap between the highest and lowest platform averages is limited.

Therefore, platform alone may not be the primary driver of engagement.

### Finding 3 — Engagement types behave independently

Likes, shares and comments show near-zero linear correlations.

A post performing well in one engagement type does not automatically perform well in another.

### Finding 4 — Wednesday performs strongly

Wednesday recorded the highest average engagement among the days of the week.

### Finding 5 — Wednesday 7 PM is the strongest reliable slot

After applying a minimum sample-size threshold, Wednesday at 7 PM produced the highest average engagement.

### Finding 6 — Data quality recovery was successful

The cleaned dataset contains no duplicate rows, no duplicate post IDs, no negative likes and no invalid timestamps.

---

## 14. Limitations

The following limitations should be considered:

1. Some engagement values are missing.
2. Missing text cannot be reliably reconstructed from the available data.
3. Missing platform values are preserved when deterministic recovery is not possible.
4. Correlation analysis measures linear relationships and does not establish causation.
5. Time-slot recommendations are based on the available historical dataset and should not automatically be interpreted as universal social-media behavior.
6. User-level conclusions depend on the completeness and representativeness of the supplied user dataset.

---

## 15. Reproducibility

All preprocessing and analysis steps are implemented using Python.

Main tools:

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

Notebook structure:

```text
notebooks/
├── 01_Data_Audit.ipynb
└── 02_EDA_Insights.ipynb