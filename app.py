import streamlit as st


# Author: Mohsina Zaman Mim
# Project: India Air Quality App


st.set_page_config(page_title="India Air Quality App by Mohsina Zaman Mim", layout="wide")

# App Title
st.title("India Air Quality Dashboard")
st.subheader("Developed by **Mohsina Zaman Mim**")

# App Description
st.markdown("""
Welcome to the **India Air Quality Analysis & Prediction App**,  
designed and developed by **Mohsina Zaman Mim**.

Use the sidebar to navigate through the sections:

###  Data Overview  
Upload your Air Quality CSV/XLSX dataset and preview structure & missing values.

### Advanced EDA  
Explore interactive visualizations such as:
- City-wise filtering  
- Time-series pollutant trends  
- Correlation heatmaps  
- Histograms and scatter plots  

### AQI Prediction  
Input pollutant values and receive an AI-powered AQI prediction.

---

This dashboard was created to help users **understand pollution patterns in India**  
and make data-driven decisions using modern data science techniques.

---
""")
