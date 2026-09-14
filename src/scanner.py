import pandas as pd 

def get_missingValues(df):
    c=df.isnull().sum()
    perc=(c/len(df)) * 100

    res=pd.DataFrame({
        "Column": c.index,
        "Missing Values": c.values,
        "Missing %": perc.round(2).values
    })
    return res[res["Missing Values"]>0]

def get_duplicates(df):
    return df.duplicated().sum()

def get_types(df):
    res=pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })
    return res

def get_summary(df):
    return{
        "rows": len(df),
        "columns": len(df.columns), "total missing": int(df.isnull().sum().sum()), "duplicates": int(df.duplicated().sum())
    }

def scan(df):
    return{
        "summary": get_summary(df),
        "missing_values":get_missingValues(df),
        "duplicates": get_duplicates(df),
        "data_types": get_types(df)
    }