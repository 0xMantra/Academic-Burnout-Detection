# Early Statistical Detection of Academic Burnout

## Project Overview

This project implements a comprehensive statistical analysis system for early detection of academic burnout among students using pure statistical methods (no machine learning).

## Directory Structure

```
P2P/
├── data/
│   ├── generate_data.py           # Synthetic data generator
│   ├── student_burnout_data.csv   # Generated dataset (500 students)
│   └── processed_burnout_data.csv # Dataset with risk scores
├── analysis/
│   ├── statistical_analysis.py    # Core statistical analysis
│   ├── risk_thresholds.py         # Risk threshold definitions
│   ├── visualizations.py           # Visualization generation
│   └── run_analysis.py            # Main analysis runner
├── docs/
│   └── methodology_report.md       # Comprehensive methodology report
├── reports/
│   ├── correlation_heatmap.png
│   ├── distribution_plots.png
│   ├── boxplots_burnout.png
│   ├── scatter_regression.png
│   ├── risk_distribution.png
│   ├── coefficients.png
│   └── summary_dashboard.png
└── README.md                       # This file
```

## Quick Start

### 1. Generate Data
```bash
python3 data/generate_data.py
```

### 2. Run Full Analysis
```bash
cd analysis
python3 run_analysis.py
```

### 3. Generate Visualizations
```bash
cd analysis
python3 visualizations.py
```

## Key Results

### Dataset
- **500 students** analyzed
- **22.8% burnout prevalence** (114 students)

### Model Performance
- **Linear Regression R²**: 0.839 (explains 83.9% of variance)
- **Logistic Regression Accuracy**: 92.2%
- **Optimal Threshold**: 0.40 (Youden's J = 0.72)

### Top Risk Factors
1. **Stress Level** (r = 0.865) - Each 1-point increase → 6.5x higher burnout odds
2. **Sleep Duration** (r = -0.649) - Each 1-hour increase → 4x lower burnout odds
3. **Study Hours** (r = 0.506) - Each 1-hour increase → 71% higher burnout odds
4. **Screen Time** (r = 0.493) - Each 1-hour increase → 63% higher burnout odds

### Risk Thresholds
| Category | Score | Burnout Rate |
|----------|-------|--------------|
| Low | <0.25 | 0.0% |
| Moderate | 0.25-0.45 | 7.2% |
| High | 0.45-0.65 | 59.5% |
| Critical | >0.65 | 90.9% |

## Methodology

### Statistical Techniques Used
1. **Descriptive Statistics**: Mean, SD, percentiles, distributions
2. **Correlation Analysis**: Pearson & Spearman correlations
3. **Multiple Linear Regression**: Continuous burnout score prediction
4. **Logistic Regression**: Binary burnout probability
5. **ANOVA**: Group mean comparisons
6. **Effect Size Analysis**: Cohen's d
7. **VIF Analysis**: Multicollinearity check

### Constraints
- ✅ Pure statistical methods only
- ✅ No machine learning (black-box automation prohibited)
- ✅ Interpretable models required
- ✅ Evidence-based risk thresholds

## Files Generated

### Data Files
- `data/student_burnout_data.csv` - Raw dataset
- `data/processed_burnout_data.csv` - With predictions

### Reports
- `docs/methodology_report.md` - Full methodology documentation

### Visualizations
- `reports/correlation_heatmap.png` - Variable correlations
- `reports/distribution_plots.png` - Variable distributions
- `reports/boxplots_burnout.png` - Group comparisons
- `reports/scatter_regression.png` - Regression relationships
- `reports/risk_distribution.png` - Risk score analysis

## Dependencies

```bash
pip install numpy pandas scipy statsmodels matplotlib seaborn
```

## Intervention Recommendations

| Priority | Focus Area | Target | Expected Impact |
|----------|------------|--------|-----------------|
| 1 | Stress Management | Stress <6.0 | 40% risk reduction |
| 2 | Sleep Hygiene | Sleep ≥7 hours | 30% risk reduction |
| 3 | Study Optimization | Study ≤8 hours | 25% risk reduction |
| 4 | Screen Time | Screen ≤7 hours | 15% risk reduction |

## License

Academic use only.

