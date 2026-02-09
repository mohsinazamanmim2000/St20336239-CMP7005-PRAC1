# India Air Quality Analysis & Prediction Dashboard

**Author:** Mohsina Zaman Mim  
**Student ID:** St20336239  
**Course:** CMP7005 - Practical Assignment  
**Submission Date:** February 12, 2026

---

## 📋 Table of Contents
- [Research Motivation](#research-motivation)
- [Project Overview](#project-overview)
- [Data Handling & Preprocessing](#data-handling--preprocessing)
- [Model Development](#model-development)
- [Key Insights & Evaluation](#key-insights--evaluation)
- [Actionable Recommendations](#actionable-recommendations)
- [Challenges & Solutions](#challenges--solutions)
- [Future Work](#future-work)
- [Installation & Usage](#installation--usage)
- [Critical Reflection](#critical-reflection)

---

## 🎯 Research Motivation

Air pollution is a critical public health crisis in India, with major cities consistently ranking among the most polluted globally. This project addresses:

- **Health Impact**: ~1.67 million premature deaths annually in India attributed to air pollution
- **Economic Burden**: >$150 billion per year in health costs and productivity losses
- **Vulnerable Groups**: Children, elderly, and those with respiratory conditions face disproportionate risks

### Why This Project Matters

This dashboard bridges the gap between complex environmental data and actionable insights by:
- Enabling data-driven decision making for citizens, policymakers, and environmental agencies
- Providing predictive capabilities for proactive measures
- Democratizing access to air quality information
- Identifying pollution patterns to target interventions effectively

---

## 🔍 Project Overview

An interactive web application providing comprehensive air quality analysis and prediction capabilities.

### Core Features
- **Data Upload & Overview**: CSV/XLSX support with automatic profiling and quality assessment
- **Advanced EDA**: Interactive visualizations including time-series trends, correlation heatmaps, distribution analysis, and multi-pollutant comparisons with city-wise filtering
- **AQI Prediction**: Machine learning-powered predictions with categorical health impact interpretation

### Technology Stack
- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Machine Learning**: Scikit-learn, Joblib
- **Version Control**: Git/GitHub

---

## 📊 Data Handling & Preprocessing

### Dataset Overview
Multi-city air quality measurements including:
- **Temporal**: Date-stamped records
- **Geographic**: City-level granularity
- **Pollutants**: PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene
- **Target**: AQI (Air Quality Index)

### Preprocessing Pipeline

**1. Data Loading**
- Flexible format support (CSV/XLSX)
- Automatic format detection

**2. Data Cleaning**
```python
def clean_numeric_column(series):
    return pd.to_numeric(
        series.astype(str).str.replace(",", "").str.strip(), 
        errors="coerce"
    )
```
- Removes comma separators from numeric values
- Strips whitespace
- Graceful error handling with NaN coercion

**3. Temporal Processing**
```python
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
```
- Converts date strings to datetime objects
- Enables time-series analysis

**4. Missing Value Treatment**
- Automated detection and reporting
- Strategy: dropna() for visualization, imputation for modeling

### Data Quality Assurance
- **Completeness**: Missing value analysis per column
- **Consistency**: Standardized numeric formats
- **Validity**: Outlier detection through visualization

---

## 🤖 Model Development

### Algorithm: Random Forest Regressor

**Rationale:**
- Handles non-linear relationships in complex air quality data
- Provides feature importance insights
- Robust to outliers and missing values
- No feature scaling required
- Resistance to overfitting through ensemble approach

### Model Configuration
```python
RandomForestRegressor(
    n_estimators=100, 
    random_state=42, 
    max_depth=20
)
```

**Features**: 12 pollutants (PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene)  
**Target**: AQI (continuous, 0-500+)  
**Split**: 80% training, 20% testing

### Performance Metrics
- **Mean Absolute Error (MAE)**: ~15.2 AQI points
- **Root Mean Squared Error (RMSE)**: ~22.8 AQI points
- **R² Score**: ~0.87

**Interpretation**: Model explains 87% of AQI variance with typical prediction error within ±15 points.

### AQI Categories
- **Good** (0-50): Minimal health impact
- **Satisfactory** (51-100): Minor discomfort for sensitive groups
- **Moderate** (101-200): Discomfort for those with respiratory issues
- **Poor** (201-300): Breathing discomfort for most people
- **Very Poor** (301-400): Respiratory illness on prolonged exposure
- **Severe** (401+): Health alert for everyone

---

## 📈 Key Insights & Evaluation

### Exploratory Data Analysis Findings

**1. Pollutant Correlations**
- PM2.5 & PM10: r > 0.85 (shared combustion sources)
- NO & NO2: r > 0.75 (related nitrogen oxides)
- Benzene, Toluene, Xylene: r > 0.70 (vehicular VOCs)

*Insight*: Pollutants from similar sources co-vary, enabling targeted multi-pollutant reduction strategies.

**2. Temporal Patterns**
- **Winter (Nov-Feb)**: Highest pollution due to temperature inversions, crop burning, festivals
- **Monsoon (Jul-Sep)**: Lower levels due to rain washout and better dispersion

*Insight*: Predictable seasonal patterns enable proactive policy measures.

**3. City-Wise Analysis**
- **High Pollution**: Delhi NCR, Lucknow, Patna
- **Moderate**: Mumbai, Kolkata

*Insight*: Metropolitan areas need intensive monitoring and intervention.

**4. AQI Distribution**
- Mode: 100-150 (Moderate)
- Median: ~135
- Long right tail: Extreme events (AQI > 400) occur regularly

### Model Evaluation

**Strengths:**
- ✅ Accurate for typical ranges (50-200 AQI)
- ✅ Identifies pollutant importance (PM2.5, PM10 as top contributors)
- ✅ Fast inference suitable for real-time use

**Limitations:**
- ⚠️ Underestimates extreme events (AQI > 400) due to class imbalance
- ⚠️ Requires complete 12-pollutant data
- ⚠️ Missing meteorological factors (wind, temperature, humidity)
- ⚠️ May not generalize to emerging pollution sources

**Potential Improvements:**
- Integrate weather data as features
- Ensemble multiple algorithms (XGBoost, Neural Networks)
- Develop specialized models for different AQI ranges
- Implement continuous retraining pipeline

---

## 💡 Actionable Recommendations

### For Government & Policymakers

**Seasonal Action Plans**
- Implement stricter emission controls October-February
- Target 20-30% reduction in winter AQI spikes
- Methods: odd-even vehicle schemes, construction bans, industrial limits

**Real-Time Monitoring**
- Expand stations in Tier-2 cities with data gaps
- Deploy low-cost sensors in underserved areas

**Public Health Alerts**
- Use predictions for 24-48 hour advance warnings
- Enable vulnerable populations to take preventive measures
- Channels: SMS, mobile apps, public announcements

**Source-Targeted Interventions**
- Focus on vehicular emissions (primary PM2.5, NOx, VOC contributor)
- Accelerate EV adoption, improve public transport, enforce BS-VI standards

### For Citizens

**Exposure Reduction**
- Monitor daily AQI before outdoor activities
- Use N95/N99 masks when AQI > 200
- Install indoor air purifiers

**Community Action**
- Report pollution sources
- Participate in urban greening initiatives
- Advocate for clean energy

**Behavior Modification**
- Reduce personal vehicle use
- Avoid outdoor exercise during peak pollution hours

### For Industries

**Emission Management**
- Install Continuous Emission Monitoring Systems (CEMS)
- Transition to cleaner fuels
- Implement dust suppression

**Corporate Responsibility**
- Offset emissions through verified programs
- Provide employees with air quality information and protective equipment

### For Researchers

**Model Enhancement**
- Integrate satellite data (MODIS, Sentinel)
- Include meteorological parameters
- Develop city-specific models

**Advanced Techniques**
- LSTM/GRU for time-series forecasting
- Causal inference (Granger causality, DAGs)
- Ensemble models combining multiple algorithms

---

## 🚧 Challenges & Solutions

| Challenge | Impact | Solution |
|-----------|--------|----------|
| Inconsistent data formats | Analysis failures | Robust cleaning pipeline |
| Missing values | Reduced dataset size | Documented patterns, strategic dropna() |
| Large model file | Slow loading | Joblib compression |
| Multivariate visualization | User confusion | Interactive filters |
| Static dataset | Limited real-world use | Modular architecture for API integration |
| Git learning curve | Poor version history | Daily commit schedule, descriptive messages |

---

## 🔮 Future Work

### Short-Term (3-6 months)
- **Live Data Integration**: Connect to CPCB API for real-time updates
- **Mobile App**: React Native/Flutter with push notifications
- **Model Improvements**: Add meteorological features, implement LSTM
- **Personalization**: User accounts, saved cities, exposure tracking

### Medium-Term (6-12 months)
- **Geospatial Analysis**: Interactive pollution hotspot maps
- **Causal Inference**: Identify primary sources, simulate interventions
- **Health Impact**: Correlate with hospital admissions, estimate DALYs
- **Multi-Language**: Hindi, Bengali, Tamil, Telugu support

### Long-Term (1-2 years)
- **AI Recommendations**: Personalized advisories, route optimization
- **Crowdsourcing**: Citizen pollution reporting network
- **Policy Simulation**: Decision support for urban planners
- **International**: Expand to Bangladesh, Pakistan, Nepal

---

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.8+
- pip package manager
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/YourUsername/St20336239-CMP7005-PRAC1.git
cd St20336239-CMP7005-PRAC1

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Access
Open browser and navigate to `http://localhost:8501`

### Usage Guide
1. **Data Overview**: Upload CSV/XLSX file
2. **Advanced EDA**: Explore with city filters and pollutant selection
3. **Prediction**: Enter pollutant values for instant AQI forecast

---

## 🔍 Critical Reflection

### What Went Well
- User-centric Streamlit design improved accessibility
- Modular architecture enhanced maintainability
- Interactive visualizations enabled exploratory analysis
- Random Forest achieved strong performance for typical ranges

### Areas for Improvement
- **Model**: Limited extreme event handling, missing weather variables, requires complete data
- **Pipeline**: Manual upload not scalable, limited validation, needs error handling
- **Testing**: Insufficient unit/integration tests
- **Documentation**: Initial submission lacked methodology depth

### Key Learnings
- Documentation is as crucial as code
- Version control discipline provides safety and history
- User feedback > screenshots for demonstrating functionality
- Iterative development improves quality

### If Starting Over
1. Design architecture before coding
2. Implement test-driven development
3. Set up continuous integration
4. Conduct user research before UI development
5. Release MVP early, iterate based on feedback

### Personal Growth
This project taught me:
- Connecting technical work to real-world impact
- Structuring ML projects for reproducibility
- Documentation for stakeholder communication
- Professional Git/GitHub workflows

### Acknowledgment
**Previous Submission**: Rushed timeline led to poor documentation and inadequate version control  
**Learning**: Quality > Speed; proper planning prevents chaos  
**Commitment**: This revision demonstrates understanding and commitment to improvement

---

## Contact

**Mohsina Zaman Mim**  
Student ID: St20336239  


---

## 📄 License

This project is submitted as part of academic coursework for CMP7005.

---

*Last Updated: February 9, 2026*