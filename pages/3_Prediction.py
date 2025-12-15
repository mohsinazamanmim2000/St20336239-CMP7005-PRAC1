import streamlit as st
import pandas as pd
import joblib

st.title("🤖 AQI Prediction")

model = joblib.load("aqi_model.pkl")

required_features = ['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3',
                     'Benzene','Toluene','Xylene']

st.subheader("Enter Pollutant Values")

input_data = {}
for col in required_features:
    input_data[col] = st.number_input(f"Enter {col}", min_value=0.0, format="%.2f")

if st.button("Predict AQI"):
    df_input = pd.DataFrame([input_data])
    prediction = model.predict(df_input)[0]
    st.success(f"Predicted AQI: **{prediction:.2f}**")

    if prediction <= 50: bucket = "Good"
    elif prediction <= 100: bucket = "Satisfactory"
    elif prediction <= 200: bucket = "Moderate"
    elif prediction <= 300: bucket = "Poor"
    elif prediction <= 400: bucket = "Very Poor"
    else: bucket = "Severe"

    st.write(f"AQI Category: **{bucket}**")
