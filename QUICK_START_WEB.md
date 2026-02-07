# Web Interface Setup & User Guide

## 📱 Quick Start (30 seconds)

```bash
cd /Users/mantrazalawadia/Documents/P2P

# Option 1: Using the bash script (recommended)
bash run_web.sh

# Option 2: Manual startup
python app.py
```

Then open: **http://localhost:5000**

---

## 🎯 Features & Pages

### 1. **Home Page** (`/`)
The main student assessment form.

**What you can do:**
- Input 6 lifestyle metrics using interactive sliders
- Get instant burnout risk calculation
- See risk assessment with visual indicators
- Review component breakdown (stress/sleep/study/screen impact)
- Save the record to database

**Metrics:**
- Stress Level: 1 (low) to 10 (extreme)
- Sleep Duration: 3-12 hours
- Study Hours: 0.5-14 hours per day
- Screen Time: 1-16 hours per day
- Physical Activity: 0 (none) to 10 (very active)
- Social Interaction: 0 (isolated) to 10 (very social)

**Results show:**
- Burnout Score (0-1)
- Risk Level: 🟢 LOW → 🟡 MODERATE → 🔴 HIGH → ⛔ CRITICAL
- Each factor's contribution percentage
- Summary statistics

---

### 2. **View Data Page** (`/data`)
Browse and analyze all student records.

**What you can see:**
- Complete table of all student assessments
- Risk level for each student with color coding
- Database statistics (total, at-risk, prevalence %)
- Visual risk distribution pie chart
- Student records with all metrics

**Use this to:**
- Monitor individual students
- Identify high-risk cases for intervention
- Track assessment history
- See trends across population

---

### 3. **Dashboard Page** (`/dashboard`)
High-level analytics and statistics.

**What you can see:**
- **KPI Cards**: Total students, average burnout score, at-risk count
- **Risk Distribution Chart**: Pie chart showing risk categories
- **Risk Categories**: Detailed breakdown with percentage bars
- **Lifestyle Metrics Chart**: Average stress, sleep, study, screen time
- **Summary Statistics**: Detailed average metrics

**Use this to:**
- Get institutional overview
- Identify systemic issues (overall stress, sleep deprivation, etc.)
- Monitor trends over time
- Make data-driven intervention decisions

---

## 🔢 The Statistical Model

### Burnout Score Calculation
```
Score = (Stress/10) × 0.35 + ((8.5-Sleep)/9) × 0.25 + (Study/14) × 0.20 + (Screen/16) × 0.20
```

**Weights:**
- 35% = Stress level
- 25% = Sleep deficit
- 20% = Study load
- 20% = Screen time

### Risk Thresholds
| Level | Score | Emoji | Action |
|-------|-------|-------|--------|
| LOW | < 0.25 | 🟢 | Monitor routinely |
| MODERATE | 0.25-0.45 | 🟡 | Preventive interventions |
| HIGH | 0.45-0.65 | 🔴 | Significant intervention |
| CRITICAL | ≥ 0.65 | ⛔ | Immediate intervention |

---

## 💾 Data Storage

All records saved to: `data/student_burnout_data.csv`

**Fields:**
- student_id
- sleep_duration
- study_hours
- screen_time
- stress_level
- burnout_score
- burnout_binary
- physical_activity
- social_interaction
- date_added

---

## 🎯 Use Cases

### Scenario 1: School Counselor Screening
1. Have students fill out the form
2. Review immediate burnout assessment
3. Click "View Data" to see all results
4. Use Dashboard to identify intervention priorities
5. Export CSV for follow-up

### Scenario 2: Research Study
1. Generate synthetic data: `python data/generate_data.py`
2. Run statistical analysis: `python analysis/run_analysis.py`
3. View visualizations: `python analysis/visualizations.py`
4. Use web UI to test threshold adjustments

### Scenario 3: Individual Student Self-Assessment
1. Student goes to http://localhost:5000
2. Inputs their metrics
3. Gets personalized feedback
4. Understands which areas need attention

### Scenario 4: Institutional Monitoring
1. Regularly add student records
2. Monitor Dashboard metrics
3. Track trends (is average stress increasing?)
4. Make policy decisions based on data

---

## 🔧 Configuration

**Change PORT:**
Edit `app.py` line ~206:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change 5000 to 8000
```

**Change DATA FILE:**
Edit `app.py` line ~9:
```python
DATA_FILE = 'data/student_burnout_data.csv'  # Change path here
```

**Disable DEBUG MODE (for production):**
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port in app.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### CSV File Permissions
```bash
chmod 644 data/student_burnout_data.csv
```

---

## 📊 Example Workflow

**Step 1: Start the server**
```bash
python app.py
# Output: Running on http://127.0.0.1:5000
```

**Step 2: Add a student**
- Click form inputs
- Adjust sliders (e.g., Stress=7, Sleep=6, Study=8, Screen=10)
- Click "Calculate Burnout Risk"
- Review results
- Click "Save Record"

**Step 3: Add more students**
- Repeat Step 2 for multiple assessments

**Step 4: Review data**
- Go to "View Data" page
- See all records in table
- Check risk distribution pie chart

**Step 5: Analyze trends**
- Go to "Dashboard"
- Check average metrics
- Identify problem areas
- Plan interventions

---

## 📈 Interpreting Results

### High Stress, Low Sleep = Very High Risk
Example: 7 stress, 5 hours sleep → Burnout score ≈ 0.52 (HIGH RISK)

### Good Habits Mitigate Risk
Example: 7 stress, 8 hours sleep, 4 study hours → Score ≈ 0.35 (MODERATE)

### Baseline Risk
Normal student: 5 stress, 8 hours sleep, 5 study → Score ≈ 0.25 (LOW RISK)

---

## 🚨 Important Notes

1. **Not a Diagnosis**: This is a screening tool, not medical diagnosis
2. **Supplementary**: Use alongside professional counseling
3. **Privacy**: Store data securely; don't share without consent
4. **Regular Updates**: Repeat assessments to track changes
5. **Holistic View**: Consider non-measured factors (family, relationships, etc.)

---

## 🎓 For Researchers

The statistical model uses only:
- ✅ Descriptive statistics
- ✅ Correlation analysis
- ✅ Regression model
- ❌ NO machine learning
- ❌ NO black-box algorithms

All models are interpretable and reproducible. Parameters are visible and can be adjusted in `app.py`.

---

## 📞 Support & Next Steps

For questions about:
- **Statistics**: See `docs/methodology_report.md`
- **Code**: See comments in `app.py` and `analysis/` files
- **Data**: CSV files in `data/` directory
- **CLI**: Use `python analysis/input_student_data.py`

---

**Happy screening! Early detection saves lives.** ❤️
