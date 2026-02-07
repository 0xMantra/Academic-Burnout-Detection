# Academic Burnout Detection - Web Interface

A Flask-based web application for early statistical detection of academic burnout using measurable student lifestyle indicators.

## 🚀 Quick Start

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python app.py
```

3. **Open in browser:**
```
http://localhost:5000
```

## 📋 Features

### Home Page (`/`)
- **Interactive Form**: Input student lifestyle metrics with real-time slider feedback
  - Stress Level (1-10)
  - Sleep Duration (3-12 hours)
  - Study Hours (0.5-14 hours/day)
  - Screen Time (1-16 hours/day)
  - Physical Activity (0-10)
  - Social Interaction (0-10)

- **Instant Results**: 
  - Burnout score calculation (0-1 scale)
  - Risk classification (Low/Moderate/High/Critical)
  - Component breakdown showing each factor's contribution
  - Save results to database

- **Database Overview**: Stats panel showing total students and burnout prevalence

### View Data Page (`/data`)
- **Student Records Table**: Browse all entered assessments
- **Risk Distribution**: Pie chart showing risk category breakdown
- **Statistics**: Quick overview of database metrics

### Dashboard Page (`/dashboard`)
- **KPI Cards**: High-level statistics
- **Risk Distribution Chart**: Visual breakdown of risk levels
- **Risk Categories**: Detailed breakdown with percentage bars
- **Lifestyle Metrics**: Average values across all students
- **Detailed Metrics**: Summary statistics

## 🔍 How It Works

### Statistical Model
The burnout score is calculated using a weighted formula:

```
Burnout Score = (Stress/10) * 0.35 + 
                ((8.5 - Sleep)/9) * 0.25 + 
                (Study/14) * 0.20 + 
                (Screen/16) * 0.20
```

### Risk Thresholds
- **🟢 Low Risk**: Score < 0.25
- **🟡 Moderate Risk**: 0.25 ≤ Score < 0.45
- **🔴 High Risk**: 0.45 ≤ Score < 0.65
- **⛔ Critical Risk**: Score ≥ 0.65

### Data Storage
All submitted records are saved to `data/student_burnout_data.csv` with the following fields:
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

## 📊 API Endpoints

### POST `/submit-data`
Calculate burnout score for given metrics
- **Body**: JSON with student metrics
- **Response**: Burnout score, risk classification, component breakdown

### POST `/save-record`
Save a student record to CSV database
- **Body**: JSON with all student metrics
- **Response**: Student ID and confirmation

## 🎯 Use Cases

1. **School Counselor**: Screen multiple students and identify intervention priorities
2. **Research**: Collect and analyze burnout data using statistical models
3. **Student Self-Assessment**: Individual students can check their burnout risk
4. **Institutional Monitoring**: Track burnout trends across student population

## 📁 Project Structure

```
P2P/
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── data/
│   ├── generate_data.py            # Synthetic data generator
│   └── student_burnout_data.csv    # Database (auto-created)
├── templates/
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   ├── data.html                   # View records page
│   └── dashboard.html              # Analytics dashboard
└── analysis/
    ├── run_analysis.py             # Statistical analysis
    ├── statistical_analysis.py     # Analysis functions
    ├── risk_thresholds.py          # Risk threshold logic
    ├── visualizations.py           # Chart generation
    └── input_student_data.py       # CLI data input
```

## 🔧 Configuration

Edit `app.py` to change:
- **PORT**: `port=5000` (line ~206)
- **DEBUG MODE**: `debug=True` (line ~206)
- **DATA FILE**: `DATA_FILE = 'data/student_burnout_data.csv'` (line ~9)

## 📝 Example Usage

1. Go to http://localhost:5000
2. Adjust sliders to input student metrics
3. Click "Calculate Burnout Risk"
4. Review results and risk assessment
5. Click "Save Record" to add to database
6. View all records on the Data page
7. Monitor trends on the Dashboard

## ⚙️ Statistical Methodology

This tool uses pure statistical techniques:
- **Descriptive Statistics**: Mean, standard deviation, percentiles
- **Correlation Analysis**: Pearson correlation coefficient
- **Regression Models**: Linear and logistic regression
- **Threshold Analysis**: Data-driven risk boundaries

No machine learning algorithms are used; all decisions are based on interpretable statistical models.

## 📄 Notes

- All calculations use evidence-based statistical models
- Results should be used as screening tools, not diagnostic instruments
- Consider consulting with healthcare professionals for individual assessments
- Data is stored locally in CSV format

## ⚡ Performance

- Handles up to 10,000+ student records efficiently
- Sub-second response time for calculations
- Automatic CSV handling with pandas

## 🤝 Support

For issues or questions, refer to the main project documentation in the root directory.

---

**Academic Burnout Detection System** • Using Statistical Methods for Early Intervention
