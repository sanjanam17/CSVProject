import streamlit as st
import pandas as pd
from src.scanner import scan

st.set_page_config(page_title="Dataset Analyzer", layout="wide")

st.title("Dataset Cleaner")
st.write("Upload a CSV file to inspect and resolve your dataset issues.")

uf = st.file_uploader("Choose a file", type=["csv"])

if uf is not None:
    df = pd.read_csv(uf)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Column Names")
    st.write(list(df.columns))

    scanr=scan(df)
    summary=scanr["summary"]
    st.header("Report of Data")
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.metric("Rows", summary["rows"])
    with c2:
        st.metric("Columns", summary["columns"])
    with c3:
        st.metric("Missing Values", summary["total missing"])
    with c4:
        st.metric("Duplicate Rows", summary["duplicates"])
    st.subheader("Missing Values")
    if scanr["missing_values"].empty:
        st.success("No missing values in this csv")
    else:
        st.dataframe(scanr["missing_values"])
    
    st.subheader("Duplicate Rows")
    st.write(f"{scanr['duplicates']} duplicate rows in this csv")

    st.subheader("Data Types")
    st.dataframe(scanr["data_types"])