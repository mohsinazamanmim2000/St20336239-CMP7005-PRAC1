import streamlit as st
import pandas as pd
from io import StringIO

st.title(" Data Overview")

uploaded = st.file_uploader("Upload Air Quality File", type=["csv", "xlsx"])

if uploaded:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.session_state['df'] = df

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Shape")
    st.write(df.shape)

    st.subheader("Column Info")
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    st.text(info_str)

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

else:
    st.info("Please upload a CSV/XLSX dataset to continue.")
