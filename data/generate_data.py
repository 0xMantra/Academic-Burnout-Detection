#!/usr/bin/env python3
"""
Synthetic Student Burnout Dataset Generation
Generates realistic student lifestyle and study data for burnout analysis
"""

import numpy as np
import pandas as pd
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
n_students = 500
np.random.seed(42)

# Generate base variables
stress_levels = np.random.normal(loc=5.5, scale=2.0, size=n_students)
stress_levels = np.clip(stress_levels, 1, 10)

# Sleep duration (inversely related to stress)
sleep_duration = 8.5 - (stress_levels * 0.3) + np.random.normal(0, 1, n_students)
sleep_duration = np.clip(sleep_duration, 3, 12)

# Study hours (positively related to stress)
study_hours = 3 + (stress_levels * 0.4) + np.random.normal(0, 1.5, n_students)
study_hours = np.clip(study_hours, 0.5, 14)

# Screen time (positively related to stress and study hours)
screen_time = 5 + (stress_levels * 0.25) + (study_hours * 0.15) + np.random.normal(0, 1.5, n_students)
screen_time = np.clip(screen_time, 1, 16)

# Burnout indicator (composite of all factors)
# Burnout risk increases with: high stress, low sleep, high study hours, high screen time
burnout_score = (
    (stress_levels / 10) * 0.35 +
    ((8.5 - sleep_duration) / 9) * 0.25 +
    (study_hours / 14) * 0.20 +
    (screen_time / 16) * 0.20
)

# Add some random variation
burnout_score = burnout_score + np.random.normal(0, 0.05, n_students)
burnout_score = np.clip(burnout_score, 0, 1)

# Create burnout binary classification (threshold at 0.5)
burnout_binary = (burnout_score > 0.5).astype(int)

# Create DataFrame
data = pd.DataFrame({
    'student_id': range(1, n_students + 1),
    'sleep_duration': np.round(sleep_duration, 2),
    'study_hours': np.round(study_hours, 2),
    'screen_time': np.round(screen_time, 2),
    'stress_level': np.round(stress_levels, 2),
    'burnout_score': np.round(burnout_score, 3),
    'burnout_binary': burnout_binary
})

# Add engagement and well-being indicators
data['physical_activity'] = np.random.uniform(0, 10, n_students) - (stress_levels * 0.15)
data['physical_activity'] = np.clip(np.round(data['physical_activity'], 2), 0, 10)

data['social_interaction'] = np.random.uniform(0, 10, n_students) - (stress_levels * 0.2)
data['social_interaction'] = np.clip(np.round(data['social_interaction'], 2), 0, 10)

# Save to CSV
output_path = 'data/student_burnout_data.csv'
data.to_csv(output_path, index=False)

print(f"Dataset generated successfully!")
print(f"Total students: {len(data)}")
print(f"Output: {output_path}")
print(f"\nDataset Summary:")
print(data.describe())
print(f"\nBurnout Distribution:")
print(data['burnout_binary'].value_counts())
print(f"\nFirst 5 rows:")
print(data.head())