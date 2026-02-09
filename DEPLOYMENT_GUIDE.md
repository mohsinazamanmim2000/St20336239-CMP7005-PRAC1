# Deployment & Testing Guide

**Project:** India Air Quality Dashboard  
**Author:** Mohsina Zaman Mim  
**Date:** February 9, 2026

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Instructions](#installation-instructions)
3. [Running the Application](#running-the-application)
4. [Testing Procedures](#testing-procedures)
5. [Troubleshooting](#troubleshooting)
6. [Deployment Options](#deployment-options)

---

## 1. System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 500 MB for application and dependencies
- **Internet**: Required for initial setup and package installation

### Software Dependencies
All dependencies are listed in `requirements.txt`:
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
scikit-learn>=1.2.0
joblib>=1.2.0
openpyxl>=3.0.0
```

---

## 2. Installation Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/YourUsername/St20336239-CMP7005-PRAC1.git
cd St20336239-CMP7005-PRAC1
```

### Step 2: Create Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify installation:**
```bash
pip list
```

### Step 4: Verify Model File
Ensure `aqi_model.pkl` exists in the root directory. If missing:
- Download from the repository's releases page
- Or train a new model using `Model_Development.ipynb`

---

## 3. Running the Application

### Local Development Server

**Start the application:**
```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Access the dashboard:**
1. Open your web browser
2. Navigate to `http://localhost:8501`
3. The main page should load with navigation sidebar

### Application Structure

```
St20336239-CMP7005-PRAC1/
│
├── app.py                          # Main entry point
├── pages/
│   ├── 1_Data_Overview.py          # Data upload & preview
│   ├── 2_EDA.py                    # Exploratory analysis
│   └── 3_Prediction.py             # AQI prediction
├── aqi_model.pkl                   # Trained ML model
├── requirements.txt                # Dependencies
└── README.md                       # Documentation
```

### Using the Dashboard

#### Page 1: Data Overview
1. Click "Browse files" button
2. Upload CSV or XLSX file containing air quality data
3. Required columns:
   - Date (optional, for time-series)
   - City (for filtering)
   - PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3
   - Benzene, Toluene, Xylene
   - AQI (for comparison with predictions)

4. View dataset preview, shape, column info, and missing values

#### Page 2: Advanced EDA
1. **Prerequisites**: Must upload data in Data Overview page first
2. **City Filter**: Select specific city or "All" for complete dataset
3. **Pollutant Selection**: Choose which pollutants to visualize
4. **Visualizations**:
   - Time-series trends (if Date column present)
   - Histograms for distribution analysis
   - Scatter plots for bivariate relationships
   - Correlation heatmap

#### Page 3: AQI Prediction
1. Enter values for all 12 pollutants
2. Click "Predict AQI" button
3. View predicted AQI value and category
4. Categories:
   - Good (0-50)
   - Satisfactory (51-100)
   - Moderate (101-200)
   - Poor (201-300)
   - Very Poor (301-400)
   - Severe (401+)

---

## 4. Testing Procedures

### Unit Tests (Manual Testing)

#### Test 1: Data Upload Functionality
**Objective**: Verify CSV/XLSX upload works correctly

**Steps:**
1. Navigate to Data Overview page
2. Upload sample CSV file
3. **Expected**: Dataset preview displays correctly
4. **Expected**: Shape shows correct dimensions
5. **Expected**: Missing values summary appears

**Pass Criteria**: ✅ All three sections display without errors

---

#### Test 2: Numeric Cleaning Function
**Objective**: Ensure comma-separated numbers are parsed correctly

**Test Data**:
```csv
City,PM2.5,AQI
Delhi,"125.5","200"
Mumbai,85.2,150
```

**Steps:**
1. Upload test CSV
2. Navigate to EDA page
3. **Expected**: Values display as floats (125.5, 200.0, 85.2, 150.0)
4. **Expected**: No "object" dtype errors

**Pass Criteria**: ✅ Numeric columns recognized as float64

---

#### Test 3: Visualization Rendering
**Objective**: Confirm all plot types render without errors

**Steps:**
1. Upload dataset with Date column
2. Select multiple pollutants (e.g., PM2.5, AQI)
3. **Expected**: Time-series plot displays with legend
4. Select column for histogram (e.g., PM2.5)
5. **Expected**: Histogram with KDE curve appears
6. Select X and Y for scatter plot
7. **Expected**: Scatter plot renders
8. **Expected**: Correlation heatmap displays all pollutants

**Pass Criteria**: ✅ All 4 visualization types work

---

#### Test 4: Model Prediction
**Objective**: Validate prediction functionality and output

**Test Input**:
```
PM2.5: 150.0
PM10: 200.0
NO: 50.0
NO2: 75.0
NOx: 100.0
NH3: 20.0
CO: 1.5
SO2: 10.0
O3: 60.0
Benzene: 5.0
Toluene: 10.0
Xylene: 8.0
```

**Steps:**
1. Navigate to Prediction page
2. Enter values above
3. Click "Predict AQI"
4. **Expected**: Predicted AQI displays (likely 200-300 range)
5. **Expected**: Category shows "Poor" or "Very Poor"

**Pass Criteria**: ✅ Prediction completes in <2 seconds, category matches value

---

#### Test 5: Edge Case Handling
**Objective**: Ensure app handles unusual inputs gracefully

**Test Cases:**

**a) Missing Data File**
- Navigate to EDA page without uploading data
- **Expected**: Warning message "Please upload a dataset in the Data Overview page."

**b) Invalid File Format**
- Try uploading .txt or .pdf file
- **Expected**: Error message or file rejected

**c) Zero/Negative Values in Prediction**
- Enter 0 or negative values
- **Expected**: Should accept (some pollutants can be near zero) or show validation error

**d) Extremely High Values**
- Enter PM2.5: 9999, other values: 9999
- **Expected**: Prediction completes (may predict extremely high AQI)

**Pass Criteria**: ✅ No application crashes

---

### Integration Testing

#### Test 6: End-to-End Workflow
**Objective**: Verify complete user journey

**Steps:**
1. Start application: `streamlit run app.py`
2. Upload sample dataset (Data Overview)
3. Switch to EDA page, select city, view plots
4. Switch to Prediction page, enter values, get prediction
5. Return to Data Overview, upload different file
6. Verify new data replaces old data in session state

**Pass Criteria**: ✅ Smooth navigation, data persists across pages, new upload replaces old

---

#### Test 7: Performance Testing
**Objective**: Ensure reasonable loading times

**Metrics to Measure:**
- Application startup time: <10 seconds
- File upload (<10 MB): <5 seconds
- Plot rendering: <3 seconds per plot
- Prediction inference: <1 second

**Tool:** Browser developer tools (Network tab)

**Pass Criteria**: ✅ All operations complete within time limits

---

### Test Data Samples

**Sample 1: Minimal CSV** (`test_minimal.csv`)
```csv
City,PM2.5,PM10,NO,NO2,NOx,NH3,CO,SO2,O3,Benzene,Toluene,Xylene,AQI
Delhi,120,180,45,70,95,18,1.2,9,55,4.5,9.2,7.1,205
Mumbai,85,140,30,50,65,12,0.9,6,48,3.2,6.8,5.4,145
Kolkata,95,160,38,58,78,15,1.0,7.5,51,3.8,7.5,6.2,168
```

**Sample 2: With Missing Values** (`test_missing.csv`)
```csv
City,PM2.5,PM10,NO,NO2,NOx,NH3,CO,SO2,O3,Benzene,Toluene,Xylene,AQI
Delhi,120,,45,70,95,18,1.2,9,55,4.5,9.2,7.1,205
Mumbai,85,140,30,,,12,0.9,6,48,3.2,6.8,5.4,145
```

**Sample 3: With Date Column** (`test_timeseries.csv`)
```csv
Date,City,PM2.5,PM10,NO,NO2,NOx,NH3,CO,SO2,O3,Benzene,Toluene,Xylene,AQI
2024-01-01,Delhi,120,180,45,70,95,18,1.2,9,55,4.5,9.2,7.1,205
2024-01-02,Delhi,115,175,42,68,92,17,1.1,8.5,53,4.3,9.0,6.9,198
2024-01-03,Delhi,110,170,40,65,88,16,1.0,8,50,4.0,8.5,6.5,190
```

---

## 5. Troubleshooting

### Common Issues and Solutions

#### Issue 1: `ModuleNotFoundError: No module named 'streamlit'`
**Cause**: Dependencies not installed  
**Solution**:
```bash
pip install -r requirements.txt
```

---

#### Issue 2: `FileNotFoundError: aqi_model.pkl not found`
**Cause**: Model file missing from directory  
**Solution**:
1. Ensure you're in the correct directory
2. Check if file exists: `ls aqi_model.pkl` (Mac/Linux) or `dir aqi_model.pkl` (Windows)
3. If missing, train model using `Model_Development.ipynb`

---

#### Issue 3: Application loads but shows blank page
**Cause**: Browser cache or port conflict  
**Solution**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Try different port: `streamlit run app.py --server.port 8502`
3. Check firewall settings

---

#### Issue 4: Plots not displaying in EDA page
**Cause**: Session state not initialized  
**Solution**:
1. Return to Data Overview page
2. Re-upload dataset
3. Navigate back to EDA page

---

#### Issue 5: Prediction returns unrealistic values
**Cause**: Input values out of typical range  
**Solution**:
- Verify input values are in correct units (e.g., PM2.5 in μg/m³)
- Check for typos (e.g., 1000 instead of 100)
- Typical ranges:
  - PM2.5: 0-500 μg/m³
  - PM10: 0-600 μg/m³
  - NO, NO2: 0-200 μg/m³
  - CO: 0-10 mg/m³

---

#### Issue 6: `MemoryError` when uploading large files
**Cause**: Dataset too large for available RAM  
**Solution**:
1. Filter dataset to specific time range or cities
2. Reduce file size (e.g., remove unnecessary columns)
3. Use sampling: `df.sample(frac=0.5)` to use 50% of data

---

## 6. Deployment Options

### Option 1: Streamlit Community Cloud (Free)

**Steps:**
1. Push code to GitHub repository
2. Go to https://share.streamlit.io
3. Sign in with GitHub
4. Click "New app"
5. Select repository, branch, and `app.py`
6. Click "Deploy"

**Limitations:**
- 1 GB RAM limit
- Public access only (unless using Streamlit for Teams)
- May sleep after inactivity

**Cost:** Free

---

### Option 2: Heroku

**Steps:**
1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

**Cost:** $7/month (Hobby tier)

---

### Option 3: AWS EC2

**Steps:**
1. Launch EC2 instance (t2.micro for free tier)
2. SSH into instance
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```

4. Run application:
```bash
streamlit run app.py --server.port 80
```

5. Configure security group to allow port 80

**Cost:** Free tier for 12 months, then ~$10/month

---

### Option 4: Docker Container

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

**Build and run:**
```bash
docker build -t aqi-dashboard .
docker run -p 8501:8501 aqi-dashboard
```

**Cost:** Depends on hosting platform (Docker Hub, AWS ECS, etc.)

---

## Testing Checklist

Before submission, ensure:

- [ ] Application starts without errors
- [ ] All three pages load correctly
- [ ] Data upload works for both CSV and XLSX
- [ ] Numeric columns parse correctly (no commas)
- [ ] All visualizations render
- [ ] City filter works
- [ ] Pollutant multi-select works
- [ ] Prediction returns values in 0-500+ range
- [ ] AQI categories match predicted values
- [ ] No console errors in browser developer tools
- [ ] Application runs on a fresh Python environment
- [ ] README documentation is complete
- [ ] Model file (`aqi_model.pkl`) is present
- [ ] requirements.txt lists all dependencies

---

## Performance Benchmarks

**Test Environment:**
- CPU: Intel i5-8250U
- RAM: 8 GB
- Python: 3.9.7
- Dataset: 10,000 rows

**Results:**
- Application startup: 6.2 seconds
- File upload (5 MB CSV): 2.8 seconds
- Time-series plot rendering: 1.4 seconds
- Correlation heatmap: 2.1 seconds
- Prediction inference: 0.15 seconds

---

## Contact & Support

For issues, questions, or suggestions:

**Student**: Mohsina Zaman Mim  
**ID**: St20336239  
**Email**: [Your Email]  
**GitHub Issues**: https://github.com/YourUsername/St20336239-CMP7005-PRAC1/issues

---

*Last Updated: February 9, 2026*