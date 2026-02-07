#!/usr/bin/env python3
"""
Statistical Analysis for Early Detection of Academic Burnout
=============================================================
This module performs comprehensive statistical analysis on student burnout data
using descriptive statistics, correlation analysis, and regression modeling.
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.stats import pearsonr, spearmanr, f_oneway, chi2_contingency
import statsmodels.api as sm
from statsmodels.formula.api import logit, ols
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATA LOADING
# ============================================================================

def load_data(filepath='../data/student_burnout_data.csv'):
    """Load the student burnout dataset"""
    df = pd.read_csv(filepath)
    print(f"Loaded dataset with {len(df)} students and {len(df.columns)} variables")
    return df

# ============================================================================
# DESCRIPTIVE STATISTICS
# ============================================================================

def descriptive_statistics(df):
    """
    Compute comprehensive descriptive statistics for all variables
    """
    print("\n" + "="*80)
    print("DESCRIPTIVE STATISTICS")
    print("="*80)
    
    # Numeric columns (excluding student_id)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'student_id' in numeric_cols:
        numeric_cols.remove('student_id')
    
    # Create detailed statistics
    desc_stats = df[numeric_cols].describe(percentiles=[.01, .05, .25, .50, .75, .95, .99])
    
    # Add additional statistics
    desc_stats.loc['variance'] = df[numeric_cols].var()
    desc_stats.loc['skewness'] = df[numeric_cols].skew()
    desc_stats.loc['kurtosis'] = df[numeric_cols].kurtosis()
    desc_stats.loc['IQR'] = desc_stats.loc['75%'] - desc_stats.loc['25%']
    desc_stats.loc['range'] = desc_stats.loc['max'] - desc_stats.loc['min']
    
    print("\nDetailed Descriptive Statistics:")
    print(desc_stats.round(3).to_string())
    
    # Burnout status comparison
    print("\n" + "-"*60)
    print("Statistics by Burnout Status:")
    print("-"*60)
    
    burnout_stats = df.groupby('burnout_binary').agg(['mean', 'std', 'median'])
    print(burnout_stats.round(3).to_string())
    
    return desc_stats

# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================

def correlation_analysis(df):
    """
    Perform Pearson and Spearman correlation analyses
    """
    print("\n" + "="*80)
    print("CORRELATION ANALYSIS")
    print("="*80)
    
    # Predictor variables
    predictors = ['sleep_duration', 'study_hours', 'screen_time', 'stress_level',
                  'physical_activity', 'social_interaction']
    
    # Correlation with burnout_score
    print("\nCorrelations with Burnout Score:")
    print("-"*60)
    print(f"{'Variable':<20} {'Pearson r':>12} {'p-value':>12} {'Spearman ρ':>12} {'p-value':>12}")
    print("-"*60)
    
    correlation_results = []
    for var in predictors:
        if var in df.columns:
            pearson_r, pearson_p = pearsonr(df[var], df['burnout_score'])
            spearman_r, spearman_p = spearmanr(df[var], df['burnout_score'])
            print(f"{var:<20} {pearson_r:>12.4f} {pearson_p:>12.4e} {spearman_r:>12.4f} {spearman_p:>12.4e}")
            correlation_results.append({
                'variable': var,
                'pearson_r': pearson_r,
                'pearson_p': pearson_p,
                'spearman_r': spearman_r,
                'spearman_p': spearman_p
            })
    
    # Full correlation matrix
    print("\n" + "-"*60)
    print("Pearson Correlation Matrix:")
    print("-"*60)
    
    all_vars = predictors + ['burnout_score']
    corr_matrix = df[all_vars].corr(method='pearson')
    print(corr_matrix.round(3).to_string())
    
    return correlation_results, corr_matrix

# ============================================================================
# MULTIPLE LINEAR REGRESSION (Continuous Burnout Score)
# ============================================================================

def multiple_linear_regression(df):
    """
    Perform multiple linear regression to predict burnout score
    """
    print("\n" + "="*80)
    print("MULTIPLE LINEAR REGRESSION (Burnout Score)")
    print("="*80)
    
    # Define predictors
    X_vars = ['stress_level', 'sleep_duration', 'study_hours', 'screen_time',
              'physical_activity', 'social_interaction']
    X = df[X_vars]
    y = df['burnout_score']
    
    # Add constant for intercept
    X = sm.add_constant(X)
    
    # Fit OLS model
    model = sm.OLS(y, X).fit()
    
    print("\nModel Summary:")
    print("-"*60)
    print(model.summary())
    
    # Extract key statistics
    print("\n" + "-"*60)
    print("Key Regression Results:")
    print("-"*60)
    print(f"R-squared:            {model.rsquared:.4f}")
    print(f"Adjusted R-squared:   {model.rsquared_adj:.4f}")
    print(f"F-statistic:          {model.fvalue:.4f}")
    print(f"F-statistic p-value:  {model.f_pvalue:.4e}")
    print(f"AIC:                  {model.aic:.2f}")
    print(f"BIC:                  {model.bic:.2f}")
    
    # Coefficient interpretation
    print("\n" + "-"*60)
    print("Coefficient Interpretation:")
    print("-"*60)
    print(f"{'Variable':<20} {'Coef':>10} {'Std Err':>10} {'t-value':>10} {'p-value':>12} {'95% CI':>20}")
    print("-"*60)
    
    coef_results = []
    for var in X_vars:
        if var in model.params.index:
            coef = model.params[var]
            std_err = model.bse[var]
            t_val = model.tvalues[var]
            p_val = model.pvalues[var]
            ci_low = model.conf_int().loc[var, 0]
            ci_high = model.conf_int().loc[var, 1]
            ci_str = f"[{ci_low:.4f}, {ci_high:.4f}]"
            print(f"{var:<20} {coef:>10.4f} {std_err:>10.4f} {t_val:>10.4f} {p_val:>12.4e} {ci_str:>20}")
            coef_results.append({
                'variable': var,
                'coefficient': coef,
                'std_error': std_err,
                't_value': t_val,
                'p_value': p_val,
                'ci_low': ci_low,
                'ci_high': ci_high
            })
    
    return model, coef_results

# ============================================================================
# LOGISTIC REGRESSION (Binary Burnout)
# ============================================================================

def logistic_regression(df):
    """
    Perform logistic regression to predict burnout probability
    """
    print("\n" + "="*80)
    print("LOGISTIC REGRESSION (Burnout Binary)")
    print("="*80)
    
    # Define predictors
    X_vars = ['stress_level', 'sleep_duration', 'study_hours', 'screen_time',
              'physical_activity', 'social_interaction']
    
    # Fit logistic model
    formula = 'burnout_binary ~ stress_level + sleep_duration + study_hours + screen_time + physical_activity + social_interaction'
    model = logit(formula, data=df).fit(disp=0)
    
    print("\nModel Summary:")
    print("-"*60)
    print(model.summary())
    
    # Odds ratios
    print("\n" + "-"*60)
    print("Odds Ratios and Confidence Intervals:")
    print("-"*60)
    print(f"{'Variable':<20} {'Odds Ratio':>12} {'95% CI':>20} {'p-value':>12}")
    print("-"*60)
    
    odds_ratios = np.exp(model.params)
    ci_low = np.exp(model.conf_int()[0])
    ci_high = np.exp(model.conf_int()[1])
    
    for var in X_vars:
        if var in model.params.index:
            or_val = odds_ratios[var]
            ci = f"[{ci_low[var]:.4f}, {ci_high[var]:.4f}]"
            p_val = model.pvalues[var]
            print(f"{var:<20} {or_val:>12.4f} {ci:>20} {p_val:>12.4e}")
    
    # Model fit statistics
    print("\n" + "-"*60)
    print("Model Fit Statistics:")
    print("-"*60)
    print(f"Pseudo R-squared (McFadden): {model.prsquared:.4f}")
    print(f"Log-Likelihood:              {model.llf:.4f}")
    print(f"AIC:                        {model.aic:.4f}")
    print(f"BIC:                        {model.bic:.4f}")
    
    # Calculate predicted probabilities
    df['predicted_prob'] = model.predict(df)
    
    # Classification table at 0.5 threshold
    df['predicted_class'] = (df['predicted_prob'] >= 0.5).astype(int)
    confusion = pd.crosstab(df['burnout_binary'], df['predicted_class'],
                           rownames=['Actual'], colnames=['Predicted'])
    print("\nConfusion Matrix (Threshold=0.5):")
    print(confusion)
    
    # Calculate accuracy
    accuracy = (df['predicted_class'] == df['burnout_binary']).mean()
    print(f"\nClassification Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
    
    return model, df

# ============================================================================
# VARIANCE INFLATION FACTOR (Multicollinearity Check)
# ============================================================================

def check_multicollinearity(df):
    """
    Calculate VIF to check for multicollinearity among predictors
    """
    print("\n" + "="*80)
    print("MULTICOLLINEARITY CHECK (VIF)")
    print("="*80)
    
    X_vars = ['stress_level', 'sleep_duration', 'study_hours', 'screen_time',
              'physical_activity', 'social_interaction']
    X = df[X_vars]
    X = sm.add_constant(X)
    
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X_vars
    vif_data["VIF"] = [variance_inflation_factor(X.values, i+1) for i in range(len(X_vars))]
    
    print("\nVariance Inflation Factors:")
    print("(VIF > 10 indicates severe multicollinearity)")
    print("-"*40)
    print(vif_data.to_string(index=False))
    
    return vif_data

# ============================================================================
# ANOVA TESTS
# ============================================================================

def anova_tests(df):
    """
    Perform ANOVA tests to compare groups
    """
    print("\n" + "="*80)
    print("ANOVA TESTS")
    print("="*80)
    
    # Split into burnout groups
    burned_out = df[df['burnout_binary'] == 1]
    not_burned_out = df[df['burnout_binary'] == 0]
    
    variables = ['stress_level', 'sleep_duration', 'study_hours', 'screen_time',
                 'physical_activity', 'social_interaction']
    
    print("\nOne-way ANOVA (Burnout vs Non-Burnout Groups):")
    print("-"*60)
    print(f"{'Variable':<20} {'F-statistic':>12} {'p-value':>15} {'Significant':>12}")
    print("-"*60)
    
    anova_results = []
    for var in variables:
        f_stat, p_value = f_oneway(burned_out[var], not_burned_out[var])
        significant = "Yes ***" if p_value < 0.001 else ("Yes **" if p_value < 0.01 else ("Yes *" if p_value < 0.05 else "No"))
        print(f"{var:<20} {f_stat:>12.4f} {p_value:>15.4e} {significant:>12}")
        anova_results.append({
            'variable': var,
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        })
    
    return anova_results

# ============================================================================
# EFFECT SIZE CALCULATIONS
# ============================================================================

def effect_size_analysis(df):
    """
    Calculate Cohen's d effect sizes for burnout vs non-burnout groups
    """
    print("\n" + "="*80)
    print("EFFECT SIZE ANALYSIS (Cohen's d)")
    print("="*80)
    
    burned_out = df[df['burnout_binary'] == 1]
    not_burned_out = df[df['burnout_binary'] == 0]
    
    variables = ['stress_level', 'sleep_duration', 'study_hours', 'screen_time',
                 'physical_activity', 'social_interaction']
    
    print("\nEffect Sizes (Cohen's d):")
    print("(Small: 0.2, Medium: 0.5, Large: 0.8)")
    print("-"*60)
    print(f"{'Variable':<20} {'Cohen\'s d':>12} {'Effect Size':>15}")
    print("-"*60)
    
    effect_sizes = []
    for var in variables:
        # Cohen's d calculation
        n1, n2 = len(burned_out), len(not_burned_out)
        mean1, mean2 = burned_out[var].mean(), not_burned_out[var].mean()
        std1, std2 = burned_out[var].std(), not_burned_out[var].std()
        
        # Pooled standard deviation
        pooled_std = np.sqrt(((n1-1)*std1**2 + (n2-1)*std2**2) / (n1+n2-2))
        cohens_d = (mean1 - mean2) / pooled_std if pooled_std > 0 else 0
        
        # Interpret effect size
        abs_d = abs(cohens_d)
        if abs_d < 0.2:
            effect = "Negligible"
        elif abs_d < 0.5:
            effect = "Small"
        elif abs_d < 0.8:
            effect = "Medium"
        else:
            effect = "Large"
        
        print(f"{var:<20} {cohens_d:>12.4f} {effect:>15}")
        effect_sizes.append({
            'variable': var,
            'cohens_d': cohens_d,
            'effect_size': effect
        })
    
    return effect_sizes

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("ACADEMIC BURNOUT STATISTICAL ANALYSIS")
    print("Early Detection Using Statistical Methods")
    print("="*80)
    
    # Load data
    df = load_data()
    
    # Run all analyses
    desc_stats = descriptive_statistics(df)
    corr_results, corr_matrix = correlation_analysis(df)
    lr_model, df = logistic_regression(df)
    ols_model, coef_results = multiple_linear_regression(df)
    vif_data = check_multicollinearity(df)
    anova_results = anova_tests(df)
    effect_sizes = effect_size_analysis(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    
    # Save processed data with predictions
    df.to_csv('../data/processed_burnout_data.csv', index=False)
    print("\nProcessed data saved to: data/processed_burnout_data.csv")