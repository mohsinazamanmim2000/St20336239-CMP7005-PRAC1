import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title(" Advanced Exploratory Data Analysis")

def clean_numeric_column(series):
    return pd.to_numeric(series.astype(str).str.replace(",", "").str.strip(), errors="coerce")

if 'df' not in st.session_state:
    st.warning("Please upload a dataset in the Data Overview page.")
else:
    df = st.session_state['df']

    # Clean numeric columns
    numeric_cols = ['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3',
                    'Benzene','Toluene','Xylene','AQI']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = clean_numeric_column(df[col])

    # Convert Date column
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.sidebar.subheader("🔍 Filters")
    city = st.sidebar.selectbox("Select City", ["All"] + sorted(df["City"].unique().tolist()))

    if city != "All":
        df = df[df["City"] == city]

    # MULTI-SELECT POLLUTANTS
    pollutants_selected = st.sidebar.multiselect(
        "Select Pollutants to Plot",
        numeric_cols,
        default=["PM2.5", "AQI"]
    )

    st.subheader("Time-Series Trend")
    if "Date" in df.columns:
        fig, ax = plt.subplots(figsize=(10,4))
        for col in pollutants_selected:
            sns.lineplot(data=df, x="Date", y=col, label=col, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("Date column not available for time-series plot.")

    st.subheader("Histogram")
    selected_hist = st.selectbox("Select Column for Histogram", numeric_cols)

    fig, ax = plt.subplots()
    sns.histplot(df[selected_hist].dropna(), kde=True, ax=ax)
    st.pyplot(fig)

    st.subheader("Scatter Plot")
    x_scatter = st.selectbox("X-axis", numeric_cols)
    y_scatter = st.selectbox("Y-axis", numeric_cols, index=1)

    fig, ax = plt.subplots()
    sns.scatterplot(x=df[x_scatter], y=df[y_scatter], ax=ax)
    st.pyplot(fig)

    st.subheader(" Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(df[numeric_cols].corr(), cmap="coolwarm")
    st.pyplot(fig)
