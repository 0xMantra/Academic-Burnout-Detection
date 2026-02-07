# Installation & Setup Guide

## 🖥️ System Requirements

- **macOS 10.14+** (or Linux/Windows with Python)
- **Python 3.8+** (3.14+ recommended)
- **pip** or **conda** (for package management)
- **4GB RAM** (minimum for data analysis)
- **500MB disk space** (including dependencies)

---

## 📦 Installation Steps

### Step 1: Navigate to Project Directory
```bash
cd /Users/mantrazalawadia/Documents/P2P
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# The virtual environment already exists at .venv
# To recreate it:
python3 -m venv .venv

# Activate it:
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Option 1: Using requirements.txt
pip install -r requirements.txt

# Option 2: Install individually
pip install Flask==2.3.2
pip install pandas==2.0.3
pip install numpy==1.24.3
pip install scipy==1.11.1
pip install matplotlib==3.7.1
pip install seaborn==0.12.2
```

### Step 4: Create Data Directory
```bash
mkdir -p data
```

### Step 5: Verify Installation
```bash
python -c "import flask, pandas, numpy; print('✓ All packages installed')"
```

---

## 🚀 Quick Start Options

### Option 1: Run Web Interface (Recommended)
```bash
# Make script executable (first time only)
chmod +x run_web.sh

# Run the script
bash run_web.sh

# Then open: http://localhost:5000
```

### Option 2: Manual Flask Startup
```bash
python app.py

# Output:
# WARNING: This is a development server. Do not use it in production.
# * Running on http://127.0.0.1:5000
# Press CTRL+C to quit
```

### Option 3: Run Analysis Scripts
```bash
# Generate synthetic data
python data/generate_data.py

# Run statistical analysis
python analysis/run_analysis.py

# Create visualizations
python analysis/visualizations.py

# Interactive data input (CLI)
python analysis/input_student_data.py
```

---

## 📁 Project Structure

```
P2P/
├── app.py                           # Flask web application
├── requirements.txt                 # Python dependencies
├── run_web.sh                       # Quick start script
├── *.md                             # Documentation files
│
├── data/
│   ├── generate_data.py             # Synthetic data generator
│   ├── student_burnout_data.csv     # Main database
│   └── processed_burnout_data.csv   # Analysis output
│
├── analysis/
│   ├── run_analysis.py              # Main analysis runner
│   ├── statistical_analysis.py      # Analysis functions
│   ├── risk_thresholds.py           # Risk scoring logic
│   ├── visualizations.py            # Chart generation
│   └── input_student_data.py        # Interactive CLI input
│
├── templates/
│   ├── base.html                    # Base template
│   ├── index.html                   # Home page
│   ├── data.html                    # View records
│   └── dashboard.html               # Analytics
│
├── reports/
│   └── *.png                        # Generated charts
│
└── .venv/                           # Virtual environment
```

---

## ✅ Verification Checklist

After installation, verify:

```bash
# Check Python version
python --version
# Should show 3.8+

# Check pip packages
pip list | grep -E "Flask|pandas|numpy"
# Should show installed versions

# Test Flask app
python -c "from app import app; print('✓ Flask app loads')"

# Test data directory
ls data/
# Should show: generate_data.py

# Test analysis modules
python -c "from analysis.statistical_analysis import load_data; print('✓ Analysis modules load')"
```

---

## 🌐 Web Interface Access

### Local Machine
```
http://localhost:5000
```

### From Another Machine (same network)
```
# Find your machine's IP:
ipconfig getifaddr en0

# Access from other machine:
http://<your-ip>:5000
```

---

## 🔧 Configuration

### Change Flask Port
Edit `app.py` (line ~206):
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Change 5000 to 8000
```

### Disable Debug Mode (Production)
```python
app.run(debug=False)  # Faster, more secure
```

### Add HTTPS (Production)
```bash
pip install pyopenssl
# Generate certificates and update app.py
```

---

## 🐛 Troubleshooting

### Import Error: "No module named flask"
```bash
# Activate virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port in app.py
```

### CSV Permission Error
```bash
# Fix file permissions
chmod 644 data/student_burnout_data.csv
chmod 755 data/
```

### Template Not Found Error
```bash
# Ensure templates folder exists
mkdir -p templates

# Check file location relative to app.py
ls templates/index.html
```

### Memory Issues
```bash
# Check available memory
free -h

# For large datasets, reduce sample size in analysis scripts
```

---

## 📊 Data Generation

### Generate Synthetic Dataset (500 students)
```bash
python data/generate_data.py

# Output:
# Dataset generated successfully!
# Total students: 500
# Output: data/student_burnout_data.csv
```

### View Generated Data
```bash
# First 5 rows
head -6 data/student_burnout_data.csv

# Total records
wc -l data/student_burnout_data.csv

# Open in spreadsheet app
open data/student_burnout_data.csv
```

---

## 🔍 Running Analysis

### Full Statistical Analysis
```bash
python analysis/run_analysis.py

# Output includes:
# • Descriptive statistics
# • Correlation analysis
# • Regression models
# • Multicollinearity check
# • ANOVA tests
# • Risk threshold analysis
```

### Generate Charts
```bash
python analysis/visualizations.py

# Creates PNG files in reports/:
# • correlation_heatmap.png
# • distribution_plots.png
# • boxplots_burnout.png
# • scatter_regression.png
```

### Interactive Data Input
```bash
python analysis/input_student_data.py

# Menu:
# 1. Add new student data
# 2. View recent records
# 3. Exit
```

---

## 📝 Example Workflow

### 1. Fresh Start
```bash
cd /Users/mantrazalawadia/Documents/P2P
source .venv/bin/activate
python data/generate_data.py
```

### 2. Start Web Interface
```bash
python app.py
# Visit http://localhost:5000
```

### 3. Add Student Data
- Go to home page
- Fill out form
- Click "Calculate Burnout Risk"
- Click "Save Record"

### 4. Review Results
- Go to "View Data" page
- See table of records
- Check pie chart

### 5. Analyze Trends
- Go to "Dashboard"
- Review KPI cards
- Check charts

---

## 🚀 Production Deployment

### Deploy to Heroku
```bash
# Create Heroku app
heroku create burnout-detection

# Set up Procfile
echo "web: python app.py" > Procfile

# Deploy
git push heroku main
```

### Deploy to GitHub Pages (Static)
```bash
# Export as static HTML using Flask-Frozen
pip install Frozen-Flask
```

### Deploy Locally (Behind Reverse Proxy)
```bash
# Install nginx
brew install nginx

# Configure nginx to forward to Flask
# Then run: python app.py
```

---

## 📈 Performance Optimization

### For Large Datasets (>50,000 records)
1. Use database instead of CSV (SQLite, PostgreSQL)
2. Enable caching for dashboard queries
3. Paginate data views

### Code Changes
```python
# In app.py, replace CSV with SQLite:
import sqlite3
conn = sqlite3.connect('data/burnout.db')

# Read data:
df = pd.read_sql_query("SELECT * FROM students", conn)
```

### Memory Optimization
```python
# Process data in chunks
chunksize = 1000
for chunk in pd.read_csv('data/student_burnout_data.csv', chunksize=chunksize):
    # Process chunk
    pass
```

---

## 🔐 Security Hardening

### Add User Authentication
```bash
pip install Flask-Login Flask-SQLAlchemy
```

```python
# In app.py
from flask_login import LoginManager, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/data')
@login_required
def view_data():
    # Only logged-in users can view
```

### Enable HTTPS
```python
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with SSL
app.run(ssl_context=('cert.pem', 'key.pem'))
```

### Sanitize Input
```python
# Already implemented in app.py with validation
# But for production, also add:
from flask_wtf import FlaskForm
from wtforms import validators
```

---

## 📚 Learning Resources

### Python
- Official Python: https://docs.python.org/3/
- Pandas: https://pandas.pydata.org/docs/

### Flask
- Flask Official: https://flask.palletsprojects.com/
- Flask by Example: https://www.fullstackpython.com/flask.html

### Statistics
- Scipy Stats: https://docs.scipy.org/doc/scipy/reference/stats.html
- Statistical Modelling: https://statsmodels.readthedocs.io/

---

## 🎯 Next Steps

1. ✅ Installation complete
2. ✅ Run `bash run_web.sh`
3. ✅ Open http://localhost:5000
4. ✅ Add some student data
5. ✅ Review results on Dashboard
6. ✅ Export CSV for analysis

---

## 📞 Getting Help

For issues:
1. Check this file
2. Review `QUICK_START_WEB.md`
3. Read `WEB_INTERFACE_README.md`
4. Check `app.py` comments
5. Review error messages carefully

---

## ✨ Success!

Your web interface is ready to use. Start screening students for burnout today!

```bash
cd /Users/mantrazalawadia/Documents/P2P
bash run_web.sh
```

Then visit: **http://localhost:5000** 🎉

---

**Installation Guide v1.0** • February 2026
