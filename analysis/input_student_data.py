#!/usr/bin/env python3
"""
Student Data Input Interface
============================
Interactive tool to collect student data and save to CSV
"""

import pandas as pd
import os
from pathlib import Path

# File path
DATA_FILE = '../data/student_burnout_data.csv'

def validate_input(prompt, input_type=float, min_val=None, max_val=None):
    """
    Validate user input with constraints
    
    Args:
        prompt: Input prompt message
        input_type: Type to convert to (int, float)
        min_val: Minimum allowed value
        max_val: Maximum allowed value
    
    Returns:
        Validated input value
    """
    while True:
        try:
            value = input_type(input(prompt))
            
            if min_val is not None and value < min_val:
                print(f"   ❌ Value must be >= {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"   ❌ Value must be <= {max_val}")
                continue
                
            return value
        except ValueError:
            print(f"   ❌ Invalid input. Please enter a valid {input_type.__name__}")

def calculate_burnout_score(stress_level, sleep_duration, study_hours, screen_time):
    """
    Calculate burnout score using the statistical model
    
    Formula:
    burnout_score = (stress/10)*0.35 + ((8.5-sleep)/9)*0.25 + (study/14)*0.20 + (screen/16)*0.20
    """
    burnout_score = (
        (stress_level / 10) * 0.35 +
        ((8.5 - sleep_duration) / 9) * 0.25 +
        (study_hours / 14) * 0.20 +
        (screen_time / 16) * 0.20
    )
    
    # Clip to 0-1 range
    burnout_score = max(0, min(1, burnout_score))
    return round(burnout_score, 3)

def classify_risk(burnout_score):
    """
    Classify risk level based on burnout score
    
    Thresholds:
    - LOW RISK: < 0.25
    - MODERATE RISK: 0.25 - 0.45
    - HIGH RISK: 0.45 - 0.65
    - CRITICAL RISK: > 0.65
    """
    if burnout_score < 0.25:
        return "LOW RISK", "🟢"
    elif burnout_score < 0.45:
        return "MODERATE RISK", "🟡"
    elif burnout_score < 0.65:
        return "HIGH RISK", "🔴"
    else:
        return "CRITICAL RISK", "🔴🔴"

def get_next_student_id(df):
    """Get the next available student ID"""
    if df is not None and len(df) > 0:
        return df['student_id'].max() + 1
    return 1

def input_student_data():
    """
    Main function to collect student data interactively
    """
    # Load existing data
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        print(f"✓ Loaded existing data: {len(df)} students")
    else:
        df = None
        print("⚠ No existing data file found. Creating new one.")
    
    print("\n" + "="*70)
    print("STUDENT BURNOUT DATA INPUT FORM")
    print("="*70)
    
    while True:
        print(f"\n--- New Student Record ---")
        
        # Get student ID
        next_id = get_next_student_id(df)
        print(f"Student ID: {next_id}")
        
        # Collect input with validation
        print("\n📋 LIFESTYLE METRICS:")
        stress_level = validate_input("  Stress Level (1-10): ", float, 1, 10)
        sleep_duration = validate_input("  Sleep Duration (hours, 3-12): ", float, 3, 12)
        study_hours = validate_input("  Study Hours (per day, 0.5-14): ", float, 0.5, 14)
        screen_time = validate_input("  Screen Time (hours, 1-16): ", float, 1, 16)
        
        print("\n🎯 WELL-BEING INDICATORS:")
        physical_activity = validate_input("  Physical Activity (0-10): ", float, 0, 10)
        social_interaction = validate_input("  Social Interaction (0-10): ", float, 0, 10)
        
        # Calculate burnout score
        burnout_score = calculate_burnout_score(stress_level, sleep_duration, study_hours, screen_time)
        burnout_binary = 1 if burnout_score > 0.5 else 0
        
        # Classify risk
        risk_level, emoji = classify_risk(burnout_score)
        
        # Display results
        print("\n" + "="*70)
        print("ANALYSIS RESULT")
        print("="*70)
        print(f"\n  Burnout Score: {burnout_score:.3f}")
        print(f"  Risk Category: {emoji} {risk_level}")
        print(f"  Burnout Status: {'YES' if burnout_binary == 1 else 'NO'}")
        
        # Show breakdown
        print(f"\n  📊 Component Breakdown:")
        stress_contrib = (stress_level / 10) * 0.35
        sleep_contrib = ((8.5 - sleep_duration) / 9) * 0.25
        study_contrib = (study_hours / 14) * 0.20
        screen_contrib = (screen_time / 16) * 0.20
        
        print(f"     • Stress Impact:    {stress_contrib:.3f} (35% weight)")
        print(f"     • Sleep Impact:     {sleep_contrib:.3f} (25% weight)")
        print(f"     • Study Impact:     {study_contrib:.3f} (20% weight)")
        print(f"     • Screen Impact:    {screen_contrib:.3f} (20% weight)")
        
        # Confirm save
        print("\n" + "-"*70)
        confirm = input("Save this record? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            # Create new record
            new_record = pd.DataFrame({
                'student_id': [next_id],
                'sleep_duration': [round(sleep_duration, 2)],
                'study_hours': [round(study_hours, 2)],
                'screen_time': [round(screen_time, 2)],
                'stress_level': [round(stress_level, 2)],
                'burnout_score': [burnout_score],
                'burnout_binary': [burnout_binary],
                'physical_activity': [round(physical_activity, 2)],
                'social_interaction': [round(social_interaction, 2)]
            })
            
            # Append to existing data or create new
            if df is not None:
                df = pd.concat([df, new_record], ignore_index=True)
            else:
                df = new_record
            
            # Save to CSV
            df.to_csv(DATA_FILE, index=False)
            print(f"\n✅ Record saved successfully!")
            print(f"   Total students in database: {len(df)}")
            
        elif confirm in ['no', 'n']:
            print("❌ Record discarded.")
        else:
            print("⚠ Invalid input. Record discarded.")
        
        # Ask if user wants to add another
        another = input("\nAdd another student? (yes/no): ").strip().lower()
        if another not in ['yes', 'y']:
            print("\n" + "="*70)
            print(f"✓ Session ended. Total students in database: {len(df)}")
            print("="*70)
            break

def view_recent_records(n=5):
    """View the most recent student records"""
    if not os.path.exists(DATA_FILE):
        print("No data file found.")
        return
    
    df = pd.read_csv(DATA_FILE)
    
    print("\n" + "="*70)
    print(f"RECENT {n} STUDENT RECORDS")
    print("="*70)
    
    recent = df.tail(n).copy()
    for idx, row in recent.iterrows():
        print(f"\nStudent ID: {int(row['student_id'])}")
        print(f"  Stress: {row['stress_level']}, Sleep: {row['sleep_duration']}h, "
              f"Study: {row['study_hours']}h, Screen: {row['screen_time']}h")
        print(f"  Burnout Score: {row['burnout_score']:.3f}")
        
        risk_level, emoji = classify_risk(row['burnout_score'])
        print(f"  Risk: {emoji} {risk_level}")

def main_menu():
    """Main menu for data input interface"""
    while True:
        print("\n" + "="*70)
        print("STUDENT DATA INPUT SYSTEM")
        print("="*70)
        print("\n1. Add new student data")
        print("2. View recent records")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            input_student_data()
        elif choice == '2':
            n = input("How many recent records to view? (default=5): ").strip()
            try:
                n = int(n) if n else 5
                view_recent_records(n)
            except ValueError:
                view_recent_records(5)
        elif choice == '3':
            print("\n✓ Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
