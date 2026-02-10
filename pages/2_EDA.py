"""
Advanced Exploratory Data Analysis (EDA) Page

This page provides interactive visualizations for exploring air quality data patterns:
- Time-series trends: Track pollutant levels over time
- Histograms: Examine pollutant distributions
- Scatter plots: Explore relationships between pollutants
- Correlation heatmap: Identify strongly correlated variables

Features city-based filtering and multi-pollutant selection for customized analysis.

Author: Mohsina Zaman Mim
Student ID: St20336239
Course: CMP7005 - Practical Assignment
Date: February 10, 2026

Usage:
    1. First upload data in the "Data Overview" page
    2. Use sidebar filters to select city and pollutants
    3. Explore various visualizations to identify patterns
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page title
st.title("🔬 Advanced Exploratory Data Analysis")


def clean_numeric_column(series):
    """
    Clean numeric columns by removing commas and converting to numeric type.
    
    Many air quality datasets contain numbers with comma separators (e.g., "1,234.5")
    which prevent proper numeric operations. This function standardizes the format.
    
    Parameters
    ----------
    series : pd.Series
        Input series that may contain comma-separated numbers or strings
        
    Returns
    -------
    pd.Series
        Cleaned series with numeric dtype (float64)
        
    Examples
    --------
    >>> data = pd.Series(["125.5", "1,234", " 89.2 "])
    >>> cleaned = clean_numeric_column(data)
    >>> cleaned
    0     125.5
    1    1234.0
    2      89.2
    dtype: float64
    
    Notes
    -----
    - Removes comma separators: "1,234" → 1234
    - Strips whitespace: " 89.2 " → 89.2
    - Handles errors gracefully: "invalid" → NaN (using errors='coerce')
    - Converts to float64 for consistency
    """
    return pd.to_numeric(
        series.astype(str).str.replace(",", "").str.strip(), 
        errors="coerce"
    )


# Check if dataset exists in session state
# Session state is populated by the Data Overview page
if 'df' not in st.session_state:
    st.warning(" Please upload a dataset in the Data Overview page.")
    st.info(" Navigate to 'Data Overview' using the sidebar to upload your air quality data.")
else:
    # Retrieve dataframe from session state
    df = st.session_state['df'].copy()  # .copy() prevents modifying original data

    # Define numeric columns to process
    # These are standard pollutant measurements in air quality datasets
    numeric_cols = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3',
                    'Benzene', 'Toluene', 'Xylene', 'AQI']
    
    # Clean numeric columns
    # Loop through each column and apply cleaning function
    for col in numeric_cols:
        if col in df.columns:
            df[col] = clean_numeric_column(df[col])

    # Convert Date column to datetime for time-series analysis
    # errors='coerce' converts invalid dates to NaT (Not a Time)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Sidebar filters for interactive exploration
    st.sidebar.subheader(" Filters")
    
    # City selection dropdown
    # "All" option shows data from all cities combined
    city = st.sidebar.selectbox(
        "Select City", 
        ["All"] + sorted(df["City"].unique().tolist())
    )

    # Filter dataframe by selected city
    # Only applies filter if a specific city is selected (not "All")
    if city != "All":
        df = df[df["City"] == city]
        st.info(f" Showing data for: **{city}** ({len(df)} records)")

    # Multi-select widget for pollutant selection
    # Allows users to compare multiple pollutants on the same plot
    # Default selection: PM2.5 and AQI (most commonly monitored)
    pollutants_selected = st.sidebar.multiselect(
        "Select Pollutants to Plot",
        numeric_cols,
        default=["PM2.5", "AQI"]
    )

    # Visualization 1: Time-Series Trend
    st.subheader(" Time-Series Trend")
    
    # Check if Date column exists and is properly formatted
    if "Date" in df.columns and df["Date"].notna().any():
        # Create matplotlib figure and axis
        # figsize=(10,4) provides good aspect ratio for time-series
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Plot each selected pollutant as a separate line
        for col in pollutants_selected:
            if col in df.columns:
                # seaborn's lineplot handles missing values gracefully
                sns.lineplot(data=df, x="Date", y=col, label=col, ax=ax)
        
        # Rotate x-axis labels for readability
        # 45-degree rotation prevents label overlap
        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Concentration")
        plt.title(f"Pollutant Trends Over Time - {city}")
        plt.legend()
        plt.tight_layout()  # Adjust spacing to prevent label cutoff
        
        st.pyplot(fig)
    else:
        st.info(" Date column not available for time-series plot.")

    # Visualization 2: Histogram (Distribution Analysis)
    st.subheader(" Histogram")
    
    # Dropdown to select which pollutant to visualize
    selected_hist = st.selectbox("Select Column for Histogram", numeric_cols)

    if selected_hist in df.columns:
        fig, ax = plt.subplots()
        
        # Plot histogram with kernel density estimate (KDE)
        # kde=True overlays a smooth probability density curve
        # dropna() removes missing values before plotting
        sns.histplot(df[selected_hist].dropna(), kde=True, ax=ax)
        
        ax.set_xlabel(f"{selected_hist} Concentration")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Distribution of {selected_hist}")
        
        # Add vertical line for median value
        median_val = df[selected_hist].median()
        ax.axvline(median_val, color='red', linestyle='--', 
                   label=f'Median: {median_val:.2f}')
        ax.legend()
        
        st.pyplot(fig)

    # Visualization 3: Scatter Plot (Bivariate Analysis)
    st.subheader(" Scatter Plot")
    
    # Two dropdowns for X and Y axis selection
    x_scatter = st.selectbox("X-axis", numeric_cols, key='x_scatter')
    y_scatter = st.selectbox("Y-axis", numeric_cols, index=1, key='y_scatter')

    if x_scatter in df.columns and y_scatter in df.columns:
        fig, ax = plt.subplots()
        
        # Scatter plot to visualize relationship between two variables
        # alpha=0.6 adds transparency to see overlapping points
        sns.scatterplot(x=df[x_scatter], y=df[y_scatter], ax=ax, alpha=0.6)
        
        ax.set_xlabel(x_scatter)
        ax.set_ylabel(y_scatter)
        ax.set_title(f"{x_scatter} vs {y_scatter}")
        
        # Calculate and display correlation coefficient
        correlation = df[[x_scatter, y_scatter]].corr().iloc[0, 1]
        ax.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        st.pyplot(fig)

    # Visualization 4: Correlation Heatmap
    st.subheader(" Correlation Heatmap")
    
    # Filter to only include numeric columns that exist in the dataframe
    available_numeric_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(available_numeric_cols) > 1:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Calculate correlation matrix
        corr_matrix = df[available_numeric_cols].corr()
        
        # Create heatmap
        # annot=True displays correlation values in each cell
        # fmt='.2f' formats values to 2 decimal places
        # cmap='coolwarm' uses red for positive, blue for negative correlations
        # center=0 ensures 0 correlation is white
        sns.heatmap(
            corr_matrix, 
            annot=True, 
            fmt='.2f', 
            cmap="coolwarm", 
            center=0,
            square=True,  # Makes cells square-shaped
            linewidths=1,  # Adds gridlines between cells
            cbar_kws={"shrink": 0.8}  # Adjusts colorbar size
        )
        
        plt.title("Pollutant Correlation Matrix")
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Interpretation helper
        st.markdown("""
        **How to read the heatmap:**
        -  **Red (closer to 1)**: Strong positive correlation - variables increase together
        -  **Blue (closer to -1)**: Strong negative correlation - one increases as other decreases
        -  **White (near 0)**: Weak or no correlation
        """)
    else:
        st.warning("⚠️ Not enough numeric columns for correlation analysis.")