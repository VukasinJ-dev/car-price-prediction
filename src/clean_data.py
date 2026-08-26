import pandas as pd

RAW_DATA_PATH = "data/cars.csv"
CLEANED_DATA_PATH = "data/cars_cleaned.csv"

def _standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
 
    df = df.copy()
 
    new_columns = []
 
    for col in df.columns:
        clean_col = col.strip().lower()
 
        clean_col = clean_col.replace("(", "_")
        clean_col = clean_col.replace(")", "")
        new_columns.append(clean_col)
 
    df.columns = new_columns
 
    if "priceusd" in df.columns:
        df = df.rename(columns={"priceusd": "price_usd"})
 
    return df

def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.copy()
    df = df.drop_duplicates().reset_index(drop=True)
    
    return df
    

df = pd.read_csv(RAW_DATA_PATH)
df = _standardize_column_names(df)
df.info()
df = _remove_duplicates(df)
df.info()