# 📑 Complete File Index & Reference Guide

## 🗂️ Project Directory Structure

```
/Users/mantrazalawadia/Documents/P2P/
│
├── 🎯 START HERE
│   ├── app.py                          # Flask web application (MAIN)
│   ├── run_web.sh                      # Quick start script
│   ├── QUICK_START_WEB.md              # User guide (READ THIS FIRST)
│   └── IMPLEMENTATION_SUMMARY.md       # What was created
│
├── 📚 DOCUMENTATION (Read as needed)
│   ├── README.md                       # Project overview
│   ├── INSTALLATION_GUIDE.md           # Setup instructions
│   ├── WEB_INTERFACE_README.md         # Technical docs
│   ├── WEB_INTERFACE_COMPLETE.md       # Complete reference
│   └── docs/methodology_report.md      # Statistical methodology
│
├── 🌐 WEB INTERFACE
│   └── templates/
│       ├── base.html                   # Base template + CSS styling
│       ├── index.html                  # Home page (form + results)
│       ├── data.html                   # View records page
│       └── dashboard.html              # Analytics dashboard
│
├── 🔧 CONFIGURATION & DEPENDENCIES
│   └── requirements.txt                # Python packages needed
│
├── 📊 DATA & ANALYSIS
│   ├── data/
│   │   ├── generate_data.py            # Synthetic data generator
│   │   ├── student_burnout_data.csv    # Main database (auto-created)
│   │   └── processed_burnout_data.csv  # Analysis output
│   │
│   └── analysis/
│       ├── run_analysis.py             # Entry point for analysis
│       ├── statistical_analysis.py     # Analysis functions
│       ├── risk_thresholds.py          # Risk scoring system
│       ├── visualizations.py           # Chart generation
│       └── input_student_data.py       # CLI data input tool
│
├── 📈 REPORTS & OUTPUTS
│   └── reports/                        # Generated PNG charts
│
└── .venv/                              # Virtual environment (hidden)
```

---

## 📄 File Guide by Use Case

### 🚀 "I want to start the web interface RIGHT NOW"
```bash
bash run_web.sh
# or
python app.py
# Then: http://localhost:5000
```
**Files involved:** `app.py`, `templates/`

---

### 📖 "I need to understand how the system works"
**Read in this order:**
1. `QUICK_START_WEB.md` - Overview (10 min)
2. `IMPLEMENTATION_SUMMARY.md` - What was built (10 min)
3. `WEB_INTERFACE_README.md` - Technical details (15 min)
4. `docs/methodology_report.md` - Statistics (20 min)

---

### 🛠️ "I need to set up the system"
**Read in this order:**
1. `INSTALLATION_GUIDE.md` - Complete setup (start to finish)
2. Install: `pip install -r requirements.txt`
3. Verify: `python -c "from app import app; print('OK')"`
4. Run: `bash run_web.sh`

---

### 📊 "I want to analyze data with scripts"
**Use these files:**
1. Generate data: `python data/generate_data.py`
2. Run analysis: `python analysis/run_analysis.py`
3. Add manual data: `python analysis/input_student_data.py`
4. Create charts: `python analysis/visualizations.py`

---

### 💻 "I want to modify the code"
**Edit these files:**
- Change risk thresholds: `app.py` → `classify_risk()` function
- Change formula weights: `app.py` → `calculate_burnout_score()`
- Modify UI colors: `templates/base.html` → `:root { colors }`
- Add new API endpoint: `app.py` → add `@app.route()`
- Modify form fields: `templates/index.html` → `<input>` elements

---

### 📱 "I want to change the web interface"
**Edit these files:**
- Home page layout: `templates/index.html`
- View data page: `templates/data.html`
- Dashboard: `templates/dashboard.html`
- Base styling: `templates/base.html` (CSS section)
- Colors/theme: `templates/base.html` → `:root { --variables }`

---

### 📚 "I need to understand the statistics"
**Read:**
- `docs/methodology_report.md` - Full statistical explanation
- `app.py` - Source code with comments
- `analysis/statistical_analysis.py` - Analysis functions

---

## 🔍 File Descriptions

### Core Application Files

#### `app.py` (9.7 KB)
**Purpose:** Main Flask web application  
**Contains:**
- Flask app initialization
- Burnout score calculation formula
- Risk classification logic
- Database statistics function
- 5 main routes: `/`, `/submit-data`, `/save-record`, `/data`, `/dashboard`
- CSV database management

**Key functions:**
```python
calculate_burnout_score()     # Formula: weighted sum
classify_risk()              # Thresholds: LOW/MOD/HIGH/CRIT
get_next_student_id()        # Auto-increment IDs
ensure_data_file()           # Create CSV if needed
```

#### `requirements.txt` (105 B)
**Purpose:** Python package list  
**Contains:**
```
Flask==2.3.2
pandas==2.0.3
numpy==1.24.3
scipy==1.11.1
matplotlib==3.7.1
seaborn==0.12.2
```

#### `run_web.sh` (1.2 KB)
**Purpose:** Quick start script for bash  
**Contains:**
- Checks Python installed
- Installs dependencies
- Creates directories
- Starts Flask server
- Shows helpful info

---

### Template Files

#### `templates/base.html`
**Purpose:** Base template for all pages  
**Contains:**
- Bootstrap CDN imports
- CSS styling block (gradients, colors, animations)
- Navigation bar
- Footer
- Chart.js library import
- Reusable blocks for content

#### `templates/index.html`
**Purpose:** Home page with input form  
**Contains:**
- Header (title + description)
- Input form with 6 sliders
- Real-time value badges
- Results section (hidden initially)
- Burnout score display
- Component breakdown charts
- Summary statistics
- Save/Reset buttons
- Success/error alerts
- JavaScript for form handling

#### `templates/data.html`
**Purpose:** View all student records  
**Contains:**
- Statistics cards (total, avg, at-risk, prevalence)
- Responsive data table with all metrics
- Color-coded risk levels
- Risk distribution pie chart
- Category breakdown
- Sortable columns

#### `templates/dashboard.html`
**Purpose:** Analytics and trends dashboard  
**Contains:**
- KPI metric cards (4 metrics)
- Risk distribution pie chart
- Risk categories progress bars
- Lifestyle metrics bar chart
- Summary statistics boxes
- Chart.js JavaScript for visualizations

---

### Data Files

#### `data/generate_data.py`
**Purpose:** Generate synthetic dataset  
**Creates:** 500 random students with realistic correlations  
**Output:** `data/student_burnout_data.csv`

#### `data/student_burnout_data.csv`
**Purpose:** Main database  
**Format:** CSV with 9 columns  
**Auto-created:** On first form submission  
**Columns:**
```
student_id, sleep_duration, study_hours, screen_time,
stress_level, burnout_score, burnout_binary,
physical_activity, social_interaction, date_added
```

#### `data/processed_burnout_data.csv`
**Purpose:** Analysis output after running `run_analysis.py`  
**Contains:** Processed data with calculated metrics

---

### Analysis Files

#### `analysis/run_analysis.py`
**Purpose:** Main analysis pipeline  
**Executes:** All statistical analyses in sequence  
**Output:** Reports to console + CSV files

#### `analysis/statistical_analysis.py`
**Purpose:** Statistical functions  
**Contains:**
- `load_data()` - Read CSV
- `descriptive_statistics()` - Mean, std, quartiles
- `correlation_analysis()` - Pearson correlation
- `multiple_linear_regression()` - Linear regression model
- `logistic_regression()` - Logistic for classification
- `check_multicollinearity()` - VIF analysis
- `anova_tests()` - Statistical significance
- `effect_size_analysis()` - Cohen's d

#### `analysis/risk_thresholds.py`
**Purpose:** Risk threshold classification system  
**Contains:** `BurnoutRiskThresholds` class with methods for:
- Defining thresholds
- Applying to data
- Finding optimal threshold
- Calculating risk cutoffs

#### `analysis/visualizations.py`
**Purpose:** Generate charts  
**Creates PNG files:**
- Correlation heatmap
- Distribution plots
- Box plots
- Scatter plots with regression lines

#### `analysis/input_student_data.py`
**Purpose:** Interactive CLI tool for data entry  
**Features:**
- Menu-based interface
- Input validation
- Real-time risk calculation
- Display results
- Save to CSV

---

### Documentation Files

#### `README.md`
- Project overview
- Quick links
- Installation summary
- Key features

#### `QUICK_START_WEB.md` (USER GUIDE)
- How to start server
- Page descriptions
- Feature explanations
- Use cases
- Workflow examples

#### `INSTALLATION_GUIDE.md` (SETUP)
- System requirements
- Step-by-step installation
- Dependency installation
- Verification checklist
- Troubleshooting

#### `WEB_INTERFACE_README.md` (TECHNICAL)
- Complete feature list
- API endpoint documentation
- Data format specifications
- Configuration options
- Performance notes

#### `WEB_INTERFACE_COMPLETE.md` (REFERENCE)
- Complete guide to all features
- Statistical model details
- Risk threshold explanations
- Use case scenarios
- Technical stack details

#### `IMPLEMENTATION_SUMMARY.md` (PROJECT SUMMARY)
- What was created
- File listing
- Feature overview
- How to start
- Next steps

#### `docs/methodology_report.md`
- Statistical methodology
- Formula derivation
- Threshold justification
- Research backing
- Limitations

---

## 🎯 Quick Reference

### To Start the Web App
```bash
bash run_web.sh
```

### To Run Analysis
```bash
python analysis/run_analysis.py
```

### To Input Data (CLI)
```bash
python analysis/input_student_data.py
```

### To Generate Synthetic Data
```bash
python data/generate_data.py
```

### To Create Visualizations
```bash
python analysis/visualizations.py
```

---

## 📊 Data Files Summary

| File | Records | Purpose | Auto-created |
|------|---------|---------|--------------|
| `student_burnout_data.csv` | Variable | Main database | ✅ Yes |
| `processed_burnout_data.csv` | Variable | Analysis output | ❌ No |
| Generated by `generate_data.py` | 500 | Sample data | ❌ No |

---

## 🔧 Configuration Files

| File | Setting | Edit Line |
|------|---------|-----------|
| `app.py` | Port | 206 |
| `app.py` | Debug mode | 206 |
| `app.py` | Data file | 9 |
| `app.py` | Risk thresholds | 40-50 |
| `app.py` | Formula weights | 25-32 |
| `templates/base.html` | Colors | 12-21 |
| `templates/base.html` | Fonts | CSS section |

---

## 📈 File Sizes

```
app.py                    ~9.7 KB
requirements.txt          ~0.1 KB
templates/base.html       ~8.5 KB
templates/index.html      ~17 KB
templates/data.html       ~9 KB
templates/dashboard.html  ~10 KB
analysis/run_analysis.py  ~7 KB
```

**Total code:** ~60 KB (excluding dependencies)

---

## ✅ Verification Checklist

- [ ] `app.py` exists and is readable
- [ ] `requirements.txt` is in root directory
- [ ] `templates/` folder has 4 HTML files
- [ ] `analysis/` folder has 5 Python files
- [ ] `data/generate_data.py` exists
- [ ] Virtual environment `.venv/` is created

---

## 🎓 File Dependencies

```
app.py (main)
├── templates/base.html (loaded by Flask)
├── templates/index.html
├── templates/data.html
├── templates/dashboard.html
├── pandas (data handling)
├── os (file operations)
└── datetime (timestamps)

analysis/run_analysis.py
├── statistical_analysis.py
├── risk_thresholds.py
└── visualizations.py

requirements.txt
└── (specifies all dependencies)
```

---

## 📞 "I'm looking for [X]"

| Looking For | File |
|-------------|------|
| How to start | `QUICK_START_WEB.md` |
| Setup help | `INSTALLATION_GUIDE.md` |
| Statistical details | `docs/methodology_report.md` |
| Code comments | `app.py` |
| Form layout | `templates/index.html` |
| Dashboard code | `templates/dashboard.html` |
| API endpoints | `app.py` |
| Risk calculation | `app.py` line 25-32 |
| Risk thresholds | `app.py` line 40-50 |
| CSS styling | `templates/base.html` |
| JavaScript logic | `templates/*.html` |
| Data entry | `analysis/input_student_data.py` |
| Analysis scripts | `analysis/run_analysis.py` |

---

## 🎉 Summary

**Total files created: 14 (+ 4 documentation)**

✅ Complete web application  
✅ Beautiful responsive UI  
✅ Comprehensive documentation  
✅ Ready to use immediately  

Start now:
```bash
bash run_web.sh
```

---

**File Index v1.0** • Complete Reference Guide • February 2026
