def remove_duplicates(df):
    res=df.drop_duplicates().copy()
    return res

#def remove_missing(df):
    #res=df.dropna().copy()  #removes the row containing at least one missing value and then creates a seperate DataFrame
    #return res
def fill_missing(df, col, value):
    res=df.copy()
    res[col]=res[col].fillna(value)
    return res


