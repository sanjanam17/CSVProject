import streamlit as st
import pandas as pd
from src.scanner import scan
from src.cleaner import remove_duplicates, fill_missing

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
    st.header("Clean Dataset")
    res=df.copy()
    rd=st.checkbox("Remove the duplicate rows")
    if rd:
        res=remove_duplicates(res)
        removed=len(df)-len(res)
        st.success(f"{removed} duplicate rows were removed")

    
    st.subheader("Handling the Missing Values")
    missingC=[]
    for col in res.columns:
        if res[col].isnull().sum()>0:
            missingC.append(col)
    if len(missingC)==0:
        st.success("No missing values")
    else:
        for col in missingC:
            st.write(f"**{col}**")

            if res[col].dtype != "object":
                choices = [
                    "Don't Change",
                    "Replace with Mean Value",
                    "Replace with Median Value",
                    "Replace with Mode Value"
                ]
            else:
                choices = [
                    "Don't Change",
                    "Replace with Mode Value"
                ]
            choice=st.selectbox(f"Choose how you wish to fill the missing value(s) in {col}", choices, key=f"missing_{col}")
            if choice=="Replace with Mean Value":
                value=res[col].mean()
                res=fill_missing(res, col, value)
            elif choice=="Replace with Median Value":
                value=res[col].median()
                res=fill_missing(res, col, value)
            elif choice=="Replace with Mode Value":
                value=res[col].mode()[0]
                res=fill_missing(res, col, value)
    

    st.header("Cleaned Dataset")
    st.dataframe(res.head())
    cleanr=scan(res)
    cleanSummary=cleanr["summary"]
    st.subheader("before and after cleaning")
    bef,aft=st.columns(2)
    with bef:
        st.write('**Original Datset**')
        st.metric("Rows", summary["rows"])
        st.metric("Missing Values", summary["total missing"])
        st.metric("DUplicate Rows", summary["duplicates"])
    with aft:
        st.write("**Cleaned Dataset**")
        st.metric("Rows", cleanSummary["rows"])
        st.metric("Missing Values", cleanSummary["total missing"])
        st.metric("Duplicate Rows", cleanSummary["duplicates"])
    
    csv = res.to_csv(index=False)
    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )



