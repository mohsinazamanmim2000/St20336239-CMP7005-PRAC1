"""
Data Overview Page

This page allows users to upload air quality datasets in CSV or XLSX format
and provides an initial exploration of the data structure, including:
- Dataset preview (first 5 rows)
- Dataset dimensions (rows × columns)
- Column information (data types, non-null counts)
- Missing value analysis

The uploaded dataset is stored in Streamlit's session state to be accessible
across all pages of the dashboard.

Author: Mohsina Zaman Mim
Student ID: St20336239
Course: CMP7005 - Practical Assignment
Date: February 10, 2026

Usage:
    Navigate to this page in the Streamlit app and upload a CSV or XLSX file
    containing air quality measurements. The file should include columns for
    pollutants (PM2.5, PM10, NO, NO2, etc.) and optionally Date and City.
"""

import streamlit as st
import pandas as pd
from io import StringIO

# Page title with emoji for visual appeal
st.title("📊 Data Overview")

# File uploader widget
# Accepts both CSV and Excel formats for flexibility
uploaded = st.file_uploader("Upload Air Quality File", type=["csv", "xlsx"])

if uploaded:
    # Load data based on file extension
    # Using conditional logic to handle different file formats
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        # For .xlsx files, requires openpyxl library
        df = pd.read_excel(uploaded)

    # Store dataframe in session state for access across pages
    # Session state persists data throughout the user's session
    # This allows other pages (EDA, Prediction) to access the uploaded data
    st.session_state['df'] = df

    # Display dataset preview
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head())  # Shows first 5 rows by default

    # Display dataset dimensions
    st.subheader("📏 Shape")
    st.write(f"**Rows:** {df.shape[0]}, **Columns:** {df.shape[1]}")
    
    # Alternative: st.write(df.shape) shows as tuple

    # Display column information
    # Uses StringIO buffer to capture df.info() output
    # df.info() normally prints to console, but we redirect to a string
    st.subheader("ℹ️ Column Info")
    buffer = StringIO()
    df.info(buf=buffer)  # Redirect info output to buffer
    info_str = buffer.getvalue()  # Extract string from buffer
    st.text(info_str)  # Display as monospaced text for readability

    # Display missing value counts
    st.subheader("❓ Missing Values")
    missing_df = df.isnull().sum()
    
    # Filter to show only columns with missing values
    missing_df = missing_df[missing_df > 0]
    
    if len(missing_df) > 0:
        st.write(missing_df)
        
        # Calculate percentage of missing values
        missing_pct = (missing_df / len(df)) * 100
        st.write("**Percentage:**")
        st.write(missing_pct.apply(lambda x: f"{x:.2f}%"))
    else:
        st.success("✅ No missing values detected!")

else:
    # Informational message when no file is uploaded
    # Using st.info() instead of st.warning() for a friendlier tone
    st.info("📁 Please upload a CSV/XLSX dataset to continue.")
    
    # Helpful instructions for users
    st.markdown("""
    **Expected File Format:**
    - CSV or Excel file (.csv, .xlsx)
    - Required columns: PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene, AQI
    - Optional columns: Date (for time-series analysis), City (for filtering)  """)