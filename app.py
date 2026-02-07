#!/usr/bin/env python3
"""
Flask Web Interface for Academic Burnout Detection
===================================================
Web application for student data input and burnout risk assessment
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import os
from datetime import datetime
import json
from scipy import stats as scipy_stats

# Ensure a specific instance path to avoid pkgutil.get_loader issues on startup
INSTANCE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(INSTANCE_PATH, exist_ok=True)
app = Flask(__name__, instance_path=INSTANCE_PATH)

# Configuration
DATA_FILE = 'data/student_burnout_data.csv'
UPLOAD_FOLDER = 'data'

def ensure_data_file():
    """Ensure data directory and file exist"""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        # Create with headers
        df = pd.DataFrame(columns=[
            'student_id', 'sleep_duration', 'study_hours', 'screen_time', 
            'stress_level', 'burnout_score', 'burnout_binary', 
            'physical_activity', 'social_interaction', 'date_added'
        ])
        df.to_csv(DATA_FILE, index=False)

def calculate_burnout_score(stress_level, sleep_duration, study_hours, screen_time):
    """Calculate burnout score using statistical model"""
    burnout_score = (
        (stress_level / 10) * 0.35 +
        ((8.5 - sleep_duration) / 9) * 0.25 +
        (study_hours / 14) * 0.20 +
        (screen_time / 16) * 0.20
    )
    burnout_score = max(0, min(1, burnout_score))
    return round(burnout_score, 3)

def classify_risk(burnout_score):
    """Classify risk level based on burnout score"""
    if burnout_score < 0.25:
        return {
            'level': 'LOW RISK',
            'emoji': '🟢',
            'color': 'success',
            'description': 'Student appears to have healthy coping mechanisms'
        }
    elif burnout_score < 0.45:
        return {
            'level': 'MODERATE RISK',
            'emoji': '🟡',
            'color': 'warning',
            'description': 'Monitor student; recommend preventive interventions'
        }
    elif burnout_score < 0.65:
        return {
            'level': 'HIGH RISK',
            'emoji': '🔴',
            'color': 'danger',
            'description': 'Significant intervention recommended'
        }
    else:
        return {
            'level': 'CRITICAL RISK',
            'emoji': '⛔',
            'color': 'danger',
            'description': 'Immediate intervention required'
        }

def get_next_student_id():
    """Get next available student ID"""
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if len(df) > 0:
            return int(df['student_id'].max()) + 1
    return 1

def get_statistics():
    """Get database statistics"""
    if not os.path.exists(DATA_FILE):
        return None
    
    df = pd.read_csv(DATA_FILE)
    if len(df) == 0:
        return None
    
    # Calculate statistics
    stats = {
        'total_students': len(df),
        'avg_burnout_score': round(df['burnout_score'].mean(), 3),
        'burnout_count': int(df['burnout_binary'].sum()),
        'burnout_percentage': round((df['burnout_binary'].sum() / len(df)) * 100, 1),
        'avg_stress': round(df['stress_level'].mean(), 2),
        'avg_sleep': round(df['sleep_duration'].mean(), 2),
        'avg_study': round(df['study_hours'].mean(), 2),
        'avg_screen': round(df['screen_time'].mean(), 2),
    }
    
    # Risk distribution
    risk_dist = {
        'low': len(df[df['burnout_score'] < 0.25]),
        'moderate': len(df[(df['burnout_score'] >= 0.25) & (df['burnout_score'] < 0.45)]),
        'high': len(df[(df['burnout_score'] >= 0.45) & (df['burnout_score'] < 0.65)]),
        'critical': len(df[df['burnout_score'] >= 0.65])
    }
    
    stats['risk_distribution'] = risk_dist
    return stats

@app.route('/')
def index():
    """Home page with input form"""
    ensure_data_file()
    student_id = get_next_student_id()
    stats = get_statistics()
    
    return render_template('index.html', student_id=student_id, stats=stats)

@app.route('/submit-data', methods=['POST'])
def submit_data():
    """Handle form submission and calculate burnout"""
    try:
        ensure_data_file()
        
        # Get form data
        data = request.get_json()
        
        stress_level = float(data['stress_level'])
        sleep_duration = float(data['sleep_duration'])
        study_hours = float(data['study_hours'])
        screen_time = float(data['screen_time'])
        physical_activity = float(data['physical_activity'])
        social_interaction = float(data['social_interaction'])
        
        # Validate ranges
        if not (1 <= stress_level <= 10):
            return jsonify({'error': 'Stress level must be between 1-10'}), 400
        if not (3 <= sleep_duration <= 12):
            return jsonify({'error': 'Sleep duration must be between 3-12 hours'}), 400
        if not (0.5 <= study_hours <= 14):
            return jsonify({'error': 'Study hours must be between 0.5-14'}), 400
        if not (1 <= screen_time <= 16):
            return jsonify({'error': 'Screen time must be between 1-16 hours'}), 400
        if not (0 <= physical_activity <= 10):
            return jsonify({'error': 'Physical activity must be between 0-10'}), 400
        if not (0 <= social_interaction <= 10):
            return jsonify({'error': 'Social interaction must be between 0-10'}), 400
        
        # Calculate burnout score
        burnout_score = calculate_burnout_score(
            stress_level, sleep_duration, study_hours, screen_time
        )
        burnout_binary = 1 if burnout_score > 0.5 else 0
        
        # Get risk classification
        risk_info = classify_risk(burnout_score)
        
        # Calculate component breakdown
        components = {
            'stress': round((stress_level / 10) * 0.35, 3),
            'sleep': round(((8.5 - sleep_duration) / 9) * 0.25, 3),
            'study': round((study_hours / 14) * 0.20, 3),
            'screen': round((screen_time / 16) * 0.20, 3)
        }
        
        return jsonify({
            'success': True,
            'burnout_score': burnout_score,
            'burnout_binary': burnout_binary,
            'risk': risk_info,
            'components': components
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save-record', methods=['POST'])
def save_record():
    """Save student record to CSV"""
    try:
        ensure_data_file()
        
        data = request.get_json()
        
        # Get next student ID
        student_id = get_next_student_id()
        
        # Prepare record
        new_record = pd.DataFrame({
            'student_id': [student_id],
            'sleep_duration': [round(float(data['sleep_duration']), 2)],
            'study_hours': [round(float(data['study_hours']), 2)],
            'screen_time': [round(float(data['screen_time']), 2)],
            'stress_level': [round(float(data['stress_level']), 2)],
            'burnout_score': [float(data['burnout_score'])],
            'burnout_binary': [int(data['burnout_binary'])],
            'physical_activity': [round(float(data['physical_activity']), 2)],
            'social_interaction': [round(float(data['social_interaction']), 2)],
            'date_added': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })
        
        # Load existing data
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_record], ignore_index=True)
        else:
            df = new_record
        
        # Save to CSV
        df.to_csv(DATA_FILE, index=False)
        
        return jsonify({
            'success': True,
            'student_id': student_id,
            'message': 'Record saved successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data')
def view_data():
    """View all student records"""
    ensure_data_file()
    
    if not os.path.exists(DATA_FILE):
        records = []
    else:
        df = pd.read_csv(DATA_FILE)
        records = df.to_dict('records')
        # Add risk classification to each record
        for record in records:
            risk_info = classify_risk(record['burnout_score'])
            record['risk_level'] = risk_info['level']
            record['risk_emoji'] = risk_info['emoji']
            record['risk_color'] = risk_info['color']
    
    stats = get_statistics()
    return render_template('data.html', records=records, stats=stats)

@app.route('/dashboard')
def dashboard():
    """Dashboard with statistics and visualizations"""
    ensure_data_file()
    stats = get_statistics()
    
    if not os.path.exists(DATA_FILE):
        return render_template('dashboard.html', stats=None)
    
    df = pd.read_csv(DATA_FILE)
    
    # Prepare data for charts
    if len(df) > 0:
        # Risk distribution for pie chart
        risk_dist = stats['risk_distribution']
        
        # Convert to chart-friendly format
        chart_data = {
            'risk_labels': ['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk'],
            'risk_values': [risk_dist['low'], risk_dist['moderate'], risk_dist['high'], risk_dist['critical']],
            'risk_colors': ['#28a745', '#ffc107', '#dc3545', '#721c24'],
            'avg_metrics': {
                'stress': stats['avg_stress'],
                'sleep': stats['avg_sleep'],
                'study': stats['avg_study'],
                'screen': stats['avg_screen']
            }
        }
        
        return render_template('dashboard.html', stats=stats, chart_data=chart_data)
    
    return render_template('dashboard.html', stats=stats)

def calculate_correlation(x, y):
    """Calculate Pearson correlation coefficient"""
    if len(x) < 2 or len(y) < 2:
        return 0
    try:
        corr, _ = scipy_stats.pearsonr(x, y)
        return round(corr, 3)
    except:
        return 0

def generate_student_progress(student_id=None):
    """Generate progress data for a student"""
    ensure_data_file()
    
    if not os.path.exists(DATA_FILE):
        return None
    
    df = pd.read_csv(DATA_FILE)
    
    if len(df) == 0:
        return None
    
    # If specific student, filter; otherwise use all data and group by week
    if student_id:
        student_data = df[df['student_id'] == student_id].sort_values('student_id')
    else:
        # Use last 4 records as "weekly" snapshots for demo
        student_data = df.tail(4).reset_index(drop=True)
    
    if len(student_data) == 0:
        return None
    
    # Create weekly view
    weeks = []
    stress_values = []
    sleep_values = []
    burnout_values = []
    screen_values = []
    study_values = []
    
    for idx, row in student_data.iterrows():
        week_num = idx + 1
        weeks.append(f"Week {week_num}")
        stress_values.append(float(row['stress_level']))
        sleep_values.append(float(row['sleep_duration']))
        burnout_values.append(float(row['burnout_score']))
        screen_values.append(float(row['screen_time']))
        study_values.append(float(row['study_hours']))
    
    # Calculate trends
    if len(stress_values) > 1:
        stress_trend = 'improving' if stress_values[-1] < stress_values[0] else 'worsening'
        stress_change = round(stress_values[0] - stress_values[-1], 2)
    else:
        stress_trend = 'stable'
        stress_change = 0
    
    if len(burnout_values) > 1:
        burnout_change = round(burnout_values[0] - burnout_values[-1], 3)
        burnout_pct = round((burnout_change / burnout_values[0] * 100) if burnout_values[0] != 0 else 0, 1)
    else:
        burnout_change = 0
        burnout_pct = 0
    
    if len(sleep_values) > 1:
        sleep_trend = 'improving' if sleep_values[-1] > sleep_values[0] else 'declining'
    else:
        sleep_trend = 'stable'
    
    # Calculate correlations
    sleep_stress_corr = calculate_correlation(sleep_values, stress_values)
    screen_stress_corr = calculate_correlation(screen_values, stress_values)
    study_burnout_corr = calculate_correlation(study_values, burnout_values)
    
    # Generate insights
    insights = []
    
    if burnout_pct > 0:
        insights.append(f"🎉 Your burnout risk has decreased by {abs(burnout_pct)}% compared to your first week.")
    elif burnout_pct < 0:
        insights.append(f"⚠️ Your burnout risk has increased by {abs(burnout_pct)}% — consider interventions.")
    
    if sleep_trend == 'improving':
        insights.append(f"😴 Your sleep pattern has stabilized — this contributes to reduced stress and better coping.")
    elif len(sleep_values) > 1 and sleep_values[-1] < 7:
        insights.append(f"💤 Your sleep is below 7 hours — increasing sleep could significantly reduce burnout.")
    
    if abs(sleep_stress_corr) > 0.5:
        direction = "negative" if sleep_stress_corr < 0 else "positive"
        insights.append(f"📊 Strong {direction} correlation detected: Sleep hours and stress levels are linked in your data.")
    
    if abs(screen_stress_corr) > 0.4:
        insights.append(f"📱 High screen time is associated with your stress levels — consider digital wellness practices.")
    
    if stress_trend == 'improving':
        insights.append(f"✨ Your stress has improved by {abs(stress_change)} points — great progress!")
    elif stress_values[-1] > 7:
        insights.append(f"⚡ Your current stress level ({stress_values[-1]}) is high — prioritize relaxation techniques.")
    
    # Status classification
    current_burnout = burnout_values[-1]
    if current_burnout < 0.35:
        status = "Thriving 🌟"
        status_color = "success"
    elif current_burnout < 0.5:
        status = "Improving 📈"
        status_color = "info"
    elif current_burnout < 0.65:
        status = "Needs Support 🤝"
        status_color = "warning"
    else:
        status = "Critical ⛔"
        status_color = "danger"
    
    return {
        'weeks': weeks,
        'stress_values': stress_values,
        'sleep_values': sleep_values,
        'burnout_values': burnout_values,
        'screen_values': screen_values,
        'study_values': study_values,
        'status': status,
        'status_color': status_color,
        'current_burnout': round(current_burnout, 3),
        'prev_burnout': round(burnout_values[0], 3) if len(burnout_values) > 0 else 0,
        'burnout_change': burnout_change,
        'burnout_change_pct': burnout_pct,
        'stress_trend': stress_trend,
        'sleep_trend': sleep_trend,
        'correlations': {
            'sleep_stress': sleep_stress_corr,
            'screen_stress': screen_stress_corr,
            'study_burnout': study_burnout_corr
        },
        'insights': insights[:5]  # Limit to 5 insights
    }

@app.route('/progress')
def progress():
    """My Progress - Student Journey Dashboard"""
    ensure_data_file()
    
    progress_data = generate_student_progress()
    
    if progress_data is None:
        # Generate sample data for demo
        progress_data = {
            'weeks': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'stress_values': [8.0, 7.5, 6.5, 5.5],
            'sleep_values': [5.5, 6.0, 6.8, 7.2],
            'burnout_values': [0.62, 0.57, 0.50, 0.45],
            'screen_values': [6.0, 5.5, 5.0, 4.8],
            'study_values': [7.0, 6.8, 6.5, 6.2],
            'status': 'Improving 📈',
            'status_color': 'info',
            'current_burnout': 0.45,
            'prev_burnout': 0.62,
            'burnout_change': 0.17,
            'burnout_change_pct': 27.4,
            'insights': [
                "🎉 Your burnout risk has decreased by 27.4% compared to your first week.",
                "😴 Your sleep pattern has stabilized — this contributes to reduced stress.",
                "📊 Strong negative correlation: Better sleep = Lower stress in your data.",
                "💤 You're approaching recommended sleep hours — keep it up!",
                "✨ Your stress has improved by 2.5 points — great progress!"
            ]
        }
    
    stats = get_statistics()
    return render_template('progress.html', progress_data=progress_data, stats=stats)

if __name__ == '__main__':
    # Allow overriding port via PORT env var; default to 5001 to avoid system-reserved 5000
    port = int(os.environ.get('PORT', '5001'))
    app.run(debug=True, host='0.0.0.0', port=port)
