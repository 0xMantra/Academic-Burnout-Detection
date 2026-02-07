#!/usr/bin/env python3
"""
Risk Threshold Definition for Academic Burnout Detection
==========================================================
This module defines evidence-based risk thresholds for burnout predictors
and calculates sensitivity/specificity for different cutoffs.
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.optimize import minimize_scalar
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# RISK THRESHOLD DEFINITIONS
# ============================================================================

class BurnoutRiskThresholds:
    """
    Defines evidence-based risk thresholds for burnout predictors
    based on statistical analysis and literature-informed cutoffs.
    """
    
    def __init__(self, df):
        self.df = df.copy()
        self.thresholds = {}
        self.risk_weights = {}
        
    def define_thresholds(self):
        """
        Define risk thresholds for each predictor variable
        based on statistical distributions and evidence-based cutoffs
        """
        print("\n" + "="*80)
        print("RISK THRESHOLD DEFINITIONS")
        print("="*80)
        
        # STRESS LEVEL (1-10 scale)
        print("\n--- STRESS LEVEL (1-10 scale) ---")
        self.thresholds['stress_level'] = {
            'low': {'max': 4.0, 'weight': 0.0},
            'moderate': {'min': 4.0, 'max': 6.0, 'weight': 0.25},
            'high': {'min': 6.0, 'max': 7.5, 'weight': 0.50},
            'very_high': {'min': 7.5, 'max': 10.0, 'weight': 1.0}
        }
        self.risk_weights['stress_level'] = 0.35  # Highest contributor
        print("  Low (≤4):      Normal stress, minimal risk")
        print("  Moderate (4-6): Elevated stress, some concern")
        print("  High (6-75):   High stress, significant risk")
        print("  Very High (>7.5): Critical stress, immediate intervention needed")
        
        # SLEEP DURATION (hours)
        print("\n--- SLEEP DURATION (hours) ---")
        self.thresholds['sleep_duration'] = {
            'healthy': {'min': 7.0, 'max': 12.0, 'weight': 0.0},
            'mild_deprivation': {'min': 6.0, 'max': 7.0, 'weight': 0.25},
            'moderate_deprivation': {'min': 5.0, 'max': 6.0, 'weight': 0.50},
            'severe_deprivation': {'min': 0.0, 'max': 5.0, 'weight': 1.0}
        }
        self.risk_weights['sleep_duration'] = 0.25
        print("  Healthy (≥7):  Adequate sleep, low risk")
        print("  Mild (6-7):    Slight sleep deficit")
        print("  Moderate (5-6): Significant sleep deprivation")
        print("  Severe (<5):   Critical sleep deprivation")
        
        # STUDY HOURS (hours per day)
        print("\n--- STUDY HOURS (per day) ---")
        self.thresholds['study_hours'] = {
            'moderate': {'min': 0.0, 'max': 5.0, 'weight': 0.0},
            'high': {'min': 5.0, 'max': 8.0, 'weight': 0.25},
            'very_high': {'min': 8.0, 'max': 11.0, 'weight': 0.50},
            'excessive': {'min': 11.0, 'max': 24.0, 'weight': 1.0}
        }
        self.risk_weights['study_hours'] = 0.20
        print("  Moderate (≤5): Healthy study-load")
        print("  High (5-8):     Heavy workload")
        print("  Very High (8-11): Excessive study time")
        print("  Excessive (>11): Critical overload")
        
        # SCREEN TIME (hours per day)
        print("\n--- SCREEN TIME (hours per day) ---")
        self.thresholds['screen_time'] = {
            'healthy': {'min': 0.0, 'max': 4.0, 'weight': 0.0},
            'moderate': {'min': 4.0, 'max': 7.0, 'weight': 0.25},
            'high': {'min': 7.0, 'max': 10.0, 'weight': 0.50},
            'very_high': {'min': 10.0, 'max': 24.0, 'weight': 1.0}
        }
        self.risk_weights['screen_time'] = 0.20
        print("  Healthy (≤4):  Minimal excessive screen exposure")
        print("  Moderate (4-7): Elevated screen time")
        print("  High (7-10):   High screen exposure")
        print("  Very High (>10): Critical screen time")
        
        # PHYSICAL ACTIVITY (0-10 scale, inverted - lower is worse)
        print("\n--- PHYSICAL ACTIVITY (0-10 scale, LOWER = WORSE) ---")
        self.thresholds['physical_activity'] = {
            'healthy': {'min': 7.0, 'max': 10.0, 'weight': 0.0},
            'moderate': {'min': 4.5, 'max': 7.0, 'weight': 0.30},
            'low': {'min': 2.5, 'max': 4.5, 'weight': 0.60},
            'very_low': {'min': 0.0, 'max': 2.5, 'weight': 1.0}
        }
        self.risk_weights['physical_activity'] = 0.10
        print("  Healthy (≥7):  Regular physical activity")
        print("  Moderate (4.5-7): Some physical activity")
        print("  Low (2.5-4.5):  Sedentary lifestyle")
        print("  Very Low (<2.5): Highly sedentary")
        
        # SOCIAL INTERACTION (0-10 scale, LOWER = WORSE)
        print("\n--- SOCIAL INTERACTION (0-10 scale, LOWER = WORSE) ---")
        self.thresholds['social_interaction'] = {
            'healthy': {'min': 6.0, 'max': 10.0, 'weight': 0.0},
            'moderate': {'min': 3.5, 'max': 6.0, 'weight': 0.30},
            'low': {'min': 2.0, 'max': 3.5, 'weight': 0.60},
            'very_low': {'min': 0.0, 'max': 2.0, 'weight': 1.0}
        }
        self.risk_weights['social_interaction'] = 0.10
        print("  Healthy (≥6):  Good social connections")
        print("  Moderate (3.5-6): Some social engagement")
        print("  Low (2-3.5):   Social isolation risk")
        print("  Very Low (<2): Critical social isolation")
        
        return self.thresholds
    
    def calculate_risk_score(self, row):
        """
        Calculate weighted risk score for a single student
        """
        total_score = 0
        total_weight = 0
        
        for var, weight in self.risk_weights.items():
            value = row[var]
            thresholds = self.thresholds.get(var, {})
            
            # Find applicable risk level
            risk_level = 'low'
            for level, bounds in thresholds.items():
                if 'min' in bounds and 'max' in bounds:
                    if bounds['min'] <= value < bounds['max']:
                        risk_level = level
                        break
                elif 'min' in bounds:
                    if bounds['min'] <= value:
                        risk_level = level
                        break
                elif 'max' in bounds:
                    if value < bounds['max']:
                        risk_level = level
                        break
            
            # Get weight for risk level (invert for protective factors)
            if var in ['physical_activity', 'social_interaction']:
                risk_weight = thresholds.get(risk_level, {}).get('weight', 0.5)
            else:
                risk_weight = thresholds.get(risk_level, {}).get('weight', 0.5)
            
            total_score += risk_weight * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0
    
    def apply_risk_thresholds(self):
        """
        Apply thresholds to dataset and categorize students
        """
        print("\n" + "="*80)
        print("APPLYING RISK THRESHOLDS TO DATASET")
        print("="*80)
        
        # Define thresholds first
        self.define_thresholds()
        
        # Calculate risk scores
        self.df['risk_score'] = self.df.apply(self.calculate_risk_score, axis=1)
        
        # Categorize risk levels
        self.df['risk_category'] = pd.cut(
            self.df['risk_score'],
            bins=[0, 0.20, 0.40, 0.60, 1.0],
            labels=['Low', 'Moderate', 'High', 'Critical'],
            include_lowest=True
        )
        
        print("\nRisk Category Distribution:")
        print("-"*40)
        risk_counts = self.df['risk_category'].value_counts()
        print(risk_counts)
        
        # Cross-tabulation with actual burnout
        print("\n" + "-"*40)
        print("Risk Category vs Actual Burnout:")
        print("-"*40)
        crosstab = pd.crosstab(self.df['risk_category'], self.df['burnout_binary'],
                               margins=True, margins_name='Total')
        crosstab.columns = ['No Burnout', 'Burnout', 'Total']
        print(crosstab)
        
        # Calculate burnout rate by risk category
        print("\n" + "-"*40)
        print("Burnout Rate by Risk Category:")
        print("-"*40)
        burnout_rate = self.df.groupby('risk_category')['burnout_binary'].mean() * 100
        for cat, rate in burnout_rate.items():
            print(f"  {cat}: {rate:.1f}% burnout rate")
        
        return self.df
    
    def find_optimal_threshold(self):
        """
        Find optimal threshold using Youden's J statistic
        """
        print("\n" + "="*80)
        print("OPTIMAL THRESHOLD ANALYSIS (Youden's J)")
        print("="*80)
        
        best_threshold = 0.5
        best_j = 0
        results = []
        
        # Test different thresholds
        for threshold in np.arange(0.1, 0.9, 0.05):
            predicted = (self.df['risk_score'] >= threshold).astype(int)
            actual = self.df['burnout_binary']
            
            # Confusion matrix elements
            tp = ((predicted == 1) & (actual == 1)).sum()
            tn = ((predicted == 0) & (actual == 0)).sum()
            fp = ((predicted == 1) & (actual == 0)).sum()
            fn = ((predicted == 0) & (actual == 1)).sum()
            
            sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            youden_j = sensitivity + specificity - 1
            
            results.append({
                'threshold': threshold,
                'sensitivity': sensitivity,
                'specificity': specificity,
                'youden_j': youden_j,
                'accuracy': (tp + tn) / (tp + tn + fp + fn)
            })
            
            if youden_j > best_j:
                best_j = youden_j
                best_threshold = threshold
        
        results_df = pd.DataFrame(results)
        print("\nThreshold Analysis:")
        print(results_df.round(3).to_string(index=False))
        
        print(f"\nOptimal Threshold (Max Youden's J): {best_threshold:.2f}")
        print(f"Maximum Youden's J: {best_j:.4f}")
        
        # Best metrics at optimal threshold
        optimal = results_df[results_df['threshold'] == best_threshold].iloc[0]
        print(f"\nAt Optimal Threshold:")
        print(f"  Sensitivity: {optimal['sensitivity']:.4f}")
        print(f"  Specificity: {optimal['specificity']:.4f}")
        print(f"  Accuracy: {optimal['accuracy']:.4f}")
        
        return best_threshold, results_df
    
    def calculate_specific_risk_cutoffs(self):
        """
        Calculate optimal cutoffs for individual predictors
        """
        print("\n" + "="*80)
        print("INDIVIDUAL PREDICTOR OPTIMAL CUTOFFS")
        print("="*80)
        
        predictors = ['stress_level', 'sleep_duration', 'study_hours', 
                      'screen_time', 'physical_activity', 'social_interaction']
        
        print("\nROC-like Analysis for Individual Predictors:")
        print("-"*70)
        print(f"{'Variable':<20} {'Optimal Cutoff':>15} {'Sensitivity':>12} {'Specificity':>12}")
        print("-"*70)
        
        cutoff_results = []
        for var in predictors:
            # For positive predictors (higher = more risk)
            if var in ['stress_level', 'study_hours', 'screen_time']:
                best_cutoff = None
                best_j = 0
                for cutoff in np.linspace(self.df[var].min(), self.df[var].max(), 50):
                    predicted = (self.df[var] >= cutoff).astype(int)
                    actual = self.df['burnout_binary']
                    
                    tp = ((predicted == 1) & (actual == 1)).sum()
                    tn = ((predicted == 0) & (actual == 0)).sum()
                    fp = ((predicted == 1) & (actual == 0)).sum()
                    fn = ((predicted == 0) & (actual == 1)).sum()
                    
                    sens = tp / (tp + fn) if (tp + fn) > 0 else 0
                    spec = tn / (tn + fp) if (tn + fp) > 0 else 0
                    j = sens + spec - 1
                    
                    if j > best_j:
                        best_j = j
                        best_cutoff = cutoff
                
                # Calculate metrics at best cutoff
                pred = (self.df[var] >= best_cutoff).astype(int)
                act = self.df['burnout_binary']
                sens = ((pred == 1) & (act == 1)).sum() / max(((act == 1).sum()), 1)
                spec = ((pred == 0) & (act == 0)).sum() / max(((act == 0).sum()), 1)
                
                print(f"{var:<20} {best_cutoff:>15.2f} {sens:>12.4f} {spec:>12.4f}")
                cutoff_results.append({
                    'variable': var,
                    'optimal_cutoff': best_cutoff,
                    'sensitivity': sens,
                    'specificity': spec,
                    'youden_j': sens + spec - 1
                })
            
            # For negative predictors (lower = more risk)
            else:
                best_cutoff = None
                best_j = 0
                for cutoff in np.linspace(self.df[var].min(), self.df[var].max(), 50):
                    predicted = (self.df[var] <= cutoff).astype(int)
                    actual = self.df['burnout_binary']
                    
                    tp = ((predicted == 1) & (actual == 1)).sum()
                    tn = ((predicted == 0) & (actual == 0)).sum()
                    fp = ((predicted == 1) & (actual == 0)).sum()
                    fn = ((predicted == 0) & (actual == 1)).sum()
                    
                    sens = tp / (tp + fn) if (tp + fn) > 0 else 0
                    spec = tn / (tn + fp) if (tn + fp) > 0 else 0
                    j = sens + spec - 1
                    
                    if j > best_j:
                        best_j = j
                        best_cutoff = cutoff
                
                pred = (self.df[var] <= best_cutoff).astype(int)
                act = self.df['burnout_binary']
                sens = ((pred == 1) & (act == 1)).sum() / max(((act == 1).sum()), 1)
                spec = ((pred == 0) & (act == 0)).sum() / max(((act == 0).sum()), 1)
                
                print(f"{var:<20} {best_cutoff:>15.2f} {sens:>12.4f} {spec:>12.4f}")
                cutoff_results.append({
                    'variable': var,
                    'optimal_cutoff': best_cutoff,
                    'sensitivity': sens,
                    'specificity': spec,
                    'youden_j': sens + spec - 1
                })
        
        return cutoff_results
    
    def generate_risk_report(self):
        """
        Generate comprehensive risk assessment report
        """
        self.define_thresholds()
        self.df = self.apply_risk_thresholds()
        optimal_threshold, threshold_results = self.find_optimal_threshold()
        cutoff_results = self.calculate_specific_risk_cutoffs()
        
        print("\n" + "="*80)
        print("RISK THRESHOLD SUMMARY")
        print("="*80)
        
        print("\n1. RECOMMENDED RISK SCORE THRESHOLDS:")
        print("-"*40)
        print("   LOW RISK:        < 0.20")
        print("   MODERATE RISK:   0.20 - 0.40")
        print("   HIGH RISK:       0.40 - 0.60")
        print("   CRITICAL RISK:   > 0.60")
        
        print("\n2. PREDICTOR-SPECIFIC WARNING THRESHOLDS:")
        print("-"*40)
        print("   Stress Level:        > 6.0 (High)")
        print("   Sleep Duration:       < 6.0 hours (Warning)")
        print("   Study Hours:          > 8.0 hours (Warning)")
        print("   Screen Time:          > 7.0 hours (Warning)")
        print("   Physical Activity:    < 4.5 (Warning)")
        print("   Social Interaction:   < 3.5 (Warning)")
        
        print(f"\n3. OPTIMAL COMPOSITE SCORE THRESHOLD: {optimal_threshold:.2f}")
        
        # Save results
        self.df.to_csv('../data/risk_assessment_results.csv', index=False)
        print("\n4. FILES GENERATED:")
        print("   - risk_assessment_results.csv (full dataset with risk scores)")
        
        return self.df, optimal_threshold

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("ACADEMIC BURNOUT RISK THRESHOLD DEFINITIONS")
    print("Evidence-Based Risk Categorization")
    print("="*80)
    
    # Load data
    df = pd.read_csv('../data/student_burnout_data.csv')
    print(f"\nLoaded {len(df)} student records")
    
    # Initialize and run risk threshold analysis
    risk_analyzer = BurnoutRiskThresholds(df)
    results_df, optimal_threshold = risk_analyzer.generate_risk_report()
    
    print("\n" + "="*80)
    print("RISK THRESHOLD ANALYSIS COMPLETE")
    print("="*80)