#!/usr/bin/env python3
"""
Main Analysis Runner for Academic Burnout Detection
=====================================================
Executes all statistical analyses and generates comprehensive reports.
"""

import sys
import os

# Add analysis directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from statistical_analysis import (
    load_data, descriptive_statistics, correlation_analysis,
    multiple_linear_regression, logistic_regression, 
    check_multicollinearity, anova_tests, effect_size_analysis
)

from risk_thresholds import BurnoutRiskThresholds

def run_full_analysis():
    """
    Execute complete burnout analysis pipeline
    """
    print("="*80)
    print("ACADEMIC BURNOUT DETECTION - STATISTICAL ANALYSIS")
    print("Early Detection Using Statistical Methods")
    print("="*80)
    
    # Load data
    print("\n[1/6] Loading data...")
    df = load_data('../data/student_burnout_data.csv')
    
    # Descriptive statistics
    print("\n[2/6] Computing descriptive statistics...")
    desc_stats = descriptive_statistics(df)
    
    # Correlation analysis
    print("\n[3/6] Performing correlation analysis...")
    corr_results, corr_matrix = correlation_analysis(df)
    
    # Regression analysis
    print("\n[4/6] Running regression models...")
    ols_model, coef_results = multiple_linear_regression(df)
    logit_model, df = logistic_regression(df)
    
    # Multicollinearity check
    print("\n[5/6] Checking multicollinearity...")
    vif_data = check_multicollinearity(df)
    
    # Statistical tests
    print("\n[6/6] Performing ANOVA and effect size analysis...")
    anova_results = anova_tests(df)
    effect_sizes = effect_size_analysis(df)
    
    # Risk threshold analysis
    print("\n" + "="*80)
    print("RISK THRESHOLD ANALYSIS")
    print("="*80)
    
    risk_analyzer = BurnoutRiskThresholds(df)
    df_with_risk = risk_analyzer.define_thresholds()
    df_with_risk = risk_analyzer.apply_risk_thresholds()
    optimal_threshold, threshold_results = risk_analyzer.find_optimal_threshold()
    cutoff_results = risk_analyzer.calculate_specific_risk_cutoffs()
    
    # Summary
    print("\n" + "="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    
    print("\n📊 DATASET OVERVIEW:")
    print(f"   • Total students: {len(df)}")
    print(f"   • Burnout prevalence: {df['burnout_binary'].mean()*100:.1f}%")
    
    print("\n📈 KEY CORRELATIONS WITH BURNOUT:")
    for result in corr_results[:4]:  # Top 4 predictors
        direction = "↑" if result['pearson_r'] > 0 else "↓"
        print(f"   • {result['variable']}: r = {result['pearson_r']:+.3f} {direction}")
    
    print("\n🔬 REGRESSION MODEL:")
    print(f"   • R² (linear model): {ols_model.rsquared:.4f}")
    print(f"   • Pseudo R² (logistic): {logit_model.prsquared:.4f}")
    
    print("\n⚠️ TOP RISK FACTORS (by standardized coefficient):")
    sorted_coef = sorted(coef_results, key=lambda x: abs(x['coefficient']), reverse=True)
    for i, coef in enumerate(sorted_coef[:3], 1):
        sign = "+" if coef['coefficient'] > 0 else "-"
        print(f"   {i}. {coef['variable']}: {sign}{abs(coef['coefficient']):.4f}")
    
    print("\n🎯 RECOMMENDED RISK THRESHOLDS:")
    print("   • LOW RISK:        < 0.25")
    print("   • MODERATE RISK:    0.25 - 0.45")
    print("   • HIGH RISK:        0.45 - 0.65")
    print("   • CRITICAL RISK:    > 0.65")
    print(f"   • Optimal threshold: {optimal_threshold:.2f}")
    
    # Save processed data
    df.to_csv('../data/processed_burnout_data.csv', index=False)
    print("\n📁 OUTPUT FILES:")
    print("   • data/processed_burnout_data.csv")
    
    return df, ols_model, logit_model, coef_results

if __name__ == "__main__":
    run_full_analysis()

