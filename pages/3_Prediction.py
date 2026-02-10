"""
AQI Prediction Page

This page uses a pre-trained Random Forest machine learning model to predict
Air Quality Index (AQI) based on pollutant concentrations entered by the user.

The model takes 12 pollutant measurements as input and outputs:
1. Numerical AQI value (0-500+)
2. Categorical classification (Good, Satisfactory, Moderate, Poor, Very Poor, Severe)

Author: Mohsina Zaman Mim
Student ID: St20336239
Course: CMP7005 - Practical Assignment
Date: February 10, 2026

Model Details:
    - Algorithm: Random Forest Regressor
    - Features: 12 pollutant concentrations
    - Training: Based on historical Indian air quality data
    - Performance: ~87% R² score on test set

Usage:
    1. Enter concentration values for all 12 pollutants
    2. Click "Predict AQI" button
    3. View predicted AQI and health category
"""

import streamlit as st
import pandas as pd
import joblib

# Page title
st.title("🤖 AQI Prediction")

# Load pre-trained machine learning model
# Model was trained using Model_Development.ipynb
# Stored as .pkl file using joblib for efficient serialization
try:
    model = joblib.load("aqi_model.pkl")
except FileNotFoundError:
    st.error("❌ Model file 'aqi_model.pkl' not found. Please ensure it's in the project directory.")
    st.stop()

# Define required features for the model
# These match the features used during model training
# All 12 pollutants are required for accurate prediction
required_features = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 
                     'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']

# Instructions section
st.subheader("📝 Enter Pollutant Values")
st.markdown("""
Enter the concentration of each pollutant in the appropriate units.
All values must be **non-negative** (≥ 0).

**Units:**
- **Particulate Matter (PM2.5, PM10):** μg/m³ (micrograms per cubic meter)
- **Gases (NO, NO2, NOx, NH3, SO2, O3):** μg/m³
- **Carbon Monoxide (CO):** mg/m³ (milligrams per cubic meter)
- **VOCs (Benzene, Toluene, Xylene):** μg/m³
""")

# Create input fields for each pollutant
# Using dictionary to store user inputs
input_data = {}

# Organize inputs in a grid layout for better UX
col1, col2 = st.columns(2)

# Left column: Particulate matter and nitrogen compounds
with col1:
    st.markdown("**Particulate Matter & Nitrogen Compounds**")
    input_data['PM2.5'] = st.number_input(
        "PM2.5 (μg/m³)", 
        min_value=0.0, 
        max_value=1000.0,
        value=0.0,
        step=1.0,
        format="%.2f",
        help="Fine particulate matter with diameter < 2.5 micrometers"
    )
    input_data['PM10'] = st.number_input(
        "PM10 (μg/m³)", 
        min_value=0.0, 
        max_value=1000.0,
        value=0.0,
        step=1.0,
        format="%.2f",
        help="Particulate matter with diameter < 10 micrometers"
    )
    input_data['NO'] = st.number_input(
        "NO (μg/m³)", 
        min_value=0.0, 
        max_value=500.0,
        value=0.0,
        step=1.0,
        format="%.2f",
        help="Nitric Oxide"
    )
    input_data['NO2'] = st.number_input(
        "NO2 (μg/m³)", 
        min_value=0.0, 
        max_value=500.0,
        value=0.0,
        step=1.0,
        format="%.2f",
        help="Nitrogen Dioxide"
    )
    input_data['NOx'] = st.number_input(
        "NOx (μg/m³)", 
        min_value=0.0, 
        max_value=500.0,
        value=0.0,
        step=1.0,
        format="%.2f",
        help="Nitrogen Oxides (combined NO and NO2)"
    )
    input_data['NH3'] = st.number_input(
        "NH3 (μg/m³)", 
        min_value=0.0, 
        max_value=500.0,
        value=0.0,
        step=1.0,
        format="%.2f",
        help="Ammonia"
    )

# Right column: Other gases and VOCs
with col2:
    st.markdown("**Other Gases & VOCs**")
    input_data['CO'] = st.number_input(
        "CO (mg/m³)", 
        min_value=0.0, 
        max_value=50.0,
        value=0.0,
        step=0.1,
        format="%.2f",
        help="Carbon Monoxide"
    )
    input_data['SO2'] = st.number_input(
        "SO2 (μg/m³)", 
        min_value=0.0, 
        max_value=500.0,
        value=0.0,
        step=1.0,
        format="%.2f",
        help="Sulfur Dioxide"
    )
    input_data['O3'] = st.number_input(
        "O3 (μg/m³)", 
        min_value=0.0, 
        max_value=500.0,
        value=0.0,
        step=1.0,
        format="%.2f",
        help="Ozone (ground-level)"
    )
    input_data['Benzene'] = st.number_input(
        "Benzene (μg/m³)", 
        min_value=0.0, 
        max_value=100.0,
        value=0.0,
        step=0.1,
        format="%.2f",
        help="Volatile Organic Compound"
    )
    input_data['Toluene'] = st.number_input(
        "Toluene (μg/m³)", 
        min_value=0.0, 
        max_value=100.0,
        value=0.0,
        step=0.1,
        format="%.2f",
        help="Volatile Organic Compound"
    )
    input_data['Xylene'] = st.number_input(
        "Xylene (μg/m³)", 
        min_value=0.0, 
        max_value=100.0,
        value=0.0,
        step=0.1,
        format="%.2f",
        help="Volatile Organic Compound"
    )

# Prediction button
if st.button("🔮 Predict AQI", type="primary"):
    # Convert input dictionary to DataFrame
    # Model expects DataFrame with specific column order
    df_input = pd.DataFrame([input_data])
    
    # Ensure columns are in the correct order
    df_input = df_input[required_features]
    
    # Make prediction using the trained model
    # predict() returns numpy array, we take first element [0]
    prediction = model.predict(df_input)[0]
    
    # Display prediction result with success message
    st.success(f"### Predicted AQI: **{prediction:.2f}**")
    
    # Categorize AQI into health buckets
    # Based on Indian National Air Quality Index (NAQI) standards
    if prediction <= 50:
        bucket = "Good"
        color = "green"
        emoji = "😊"
        description = "Minimal impact. Air quality is satisfactory."
    elif prediction <= 100:
        bucket = "Satisfactory"
        color = "lightgreen"
        emoji = "🙂"
        description = "Minor breathing discomfort for sensitive individuals."
    elif prediction <= 200:
        bucket = "Moderate"
        color = "yellow"
        emoji = "😐"
        description = "Breathing discomfort for people with respiratory diseases."
    elif prediction <= 300:
        bucket = "Poor"
        color = "orange"
        emoji = "😷"
        description = "Breathing discomfort for most people on prolonged exposure."
    elif prediction <= 400:
        bucket = "Very Poor"
        color = "red"
        emoji = "😨"
        description = "Respiratory illness on prolonged exposure."
    else:
        bucket = "Severe"
        color = "darkred"
        emoji = "☠️"
        description = "Health alert: everyone may experience serious health effects."
    
    # Display AQI category with color coding
    st.markdown(f"### AQI Category: **:{color}[{bucket}]** {emoji}")
    st.info(description)
    
    # Health recommendations based on category
    st.markdown("---")
    st.subheader("🏥 Health Recommendations")
    
    if bucket == "Good":
        st.success("""
        - ✅ Ideal for outdoor activities
        - ✅ No health precautions needed
        - ✅ Enjoy fresh air!
        """)
    elif bucket == "Satisfactory":
        st.info("""
        - ⚠️ Sensitive groups (children, elderly, asthmatics) should monitor symptoms
        - ✅ General public can enjoy outdoor activities
        """)
    elif bucket == "Moderate":
        st.warning("""
        - ⚠️ Consider reducing prolonged outdoor exertion
        - 😷 Sensitive groups should wear masks outdoors
        - 🏠 Keep windows closed if possible
        """)
    elif bucket == "Poor":
        st.warning("""
        - 😷 Wear N95/N99 masks when going outside
        - 🚫 Avoid prolonged outdoor activities
        - 🏠 Use indoor air purifiers
        - 🚶‍♂️ Limit physical exertion
        """)
    elif bucket == "Very Poor":
        st.error("""
        - 🚫 Avoid all outdoor activities
        - 😷 Wear masks even indoors if necessary
        - 🏠 Keep all windows and doors closed
        - 💨 Use air purifiers on high setting
        - 👶 Keep children and elderly indoors
        """)
    else:  # Severe
        st.error("""
        - 🚨 **EMERGENCY CONDITIONS**
        - 🏠 Stay indoors at all times
        - 😷 Wear high-grade respiratory protection
        - 🏥 Seek medical attention if experiencing symptoms
        - 🚫 Avoid any outdoor exposure
        - 📞 Check on vulnerable family members
        """)
    
    # Additional information section
    with st.expander("ℹ️ About this prediction"):
        st.markdown(f"""
        **Model Information:**
        - Algorithm: Random Forest Regressor
        - Features used: {len(required_features)} pollutant measurements
        - Training data: Historical Indian air quality records
        
        **Input Summary:**
        - PM2.5: {input_data['PM2.5']:.2f} μg/m³
        - PM10: {input_data['PM10']:.2f} μg/m³
        - NO2: {input_data['NO2']:.2f} μg/m³
        - (+ {len(required_features)-3} other pollutants)
        
        **Note:** This is a predictive model and actual AQI may vary based on
        additional factors not included in the model (weather conditions, 
        geographic factors, etc.).
        """)

else:
    # Display helpful information when prediction hasn't been made yet
    st.info("👆 Enter pollutant values above and click 'Predict AQI' to get your result.")
    
    # Show sample values for testing
    with st.expander("📊 View Sample Values for Testing"):
        st.markdown("""
        **Example 1: Good Air Quality**
        - PM2.5: 25, PM10: 40, NO: 10, NO2: 20, NOx: 30, NH3: 5
        - CO: 0.5, SO2: 5, O3: 30, Benzene: 1, Toluene: 2, Xylene: 1.5
        
        **Example 2: Poor Air Quality (Delhi Winter)**
        - PM2.5: 250, PM10: 350, NO: 80, NO2: 120, NOx: 180, NH3: 40
        - CO: 3.5, SO2: 25, O3: 75, Benzene: 8, Toluene: 15, Xylene: 12
        
        **Example 3: Severe Air Quality**
        - PM2.5: 450, PM10: 550, NO: 150, NO2: 200, NOx: 300, NH3: 80
        - CO: 8.0, SO2: 50, O3: 120, Benzene: 20, Toluene: 35, Xylene: 28
        """)