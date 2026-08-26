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

MISSING_LIKE_VALUES = {
    "",
    " ",
    "nan",
    "NaN",
    "NAN",
    "null",
    "Null",
    "NULL",
    "none",
    "None",
    "NONE",
    "unknown",
    "Unknown",
    "UNKNOWN"
}

def _replace_missing_like_values(df: pd.DataFrame) -> pd.DataFrame:
 
    df = df.copy()
 
    df = df.replace(list(MISSING_LIKE_VALUES), pd.NA)
 
    return df

def _fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df['volume_cm3'] = df['volume_cm3'].fillna(
        df['volume_cm3'].median()
    )

    df['drive_unit'] = df['drive_unit'].fillna(
        df['drive_unit'].mode()[0]
    )

    df['segment'] = df['segment'].fillna(
        df['segment'].mode()[0]
    )

    return df

def _convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
 
    df = df.copy()
 
    numeric_columns = [
    "price_usd",
    "year",
    "mileage_kilometers",
    "volume_cm3"
    ]
 
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
 
    return df

def _clean_volume(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.copy()
    
    df.loc[df['volume_cm3'] >= 10000, 'volume_cm3'] = pd.NA
    
    return df

def _clean_mileage(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.copy()
    
    mileage = df['mileage_kilometers']
    mileage_str = mileage.astype(int).astype(str)
    
    repeated_digit = (
        (mileage >= 100000) &
        mileage_str.str.match(r'^(\d)\1+$')
    )
    
    zero_placeholder = (
        (mileage >= 1000000) &
        mileage_str.str.match(r'^[1-9]0+$')
    )
    
    df.loc[
        repeated_digit | zero_placeholder,
        'mileage_kilometers'
    ] = pd.NA
    
    return df

def _clean_categorical_values(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.copy()
    
    categorical_columns = [
    'make',
    'model',
    'condition',
    'fuel_type',
    'color',
    'transmission',
    'drive_unit',
    'segment'
    ]
    
    for col in categorical_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype("string")
                .str.strip()
                .str.lower()
            )
    
    return df

def clean(df: pd.DataFrame) -> pd.DataFrame:
 
    df_clean = (
        df
        .pipe(_standardize_column_names)
        .pipe(_convert_numeric_columns)
        .pipe(_clean_categorical_values)
        .pipe(_clean_volume)
        .pipe(_clean_mileage)
        .pipe(_replace_missing_like_values)
        .pipe(_fill_missing_values)
        .pipe(_remove_duplicates)
        .reset_index(drop=True)
    )
 
    return df_clean


def main() -> None:
    df_raw = pd.read_csv(RAW_DATA_PATH)
    
    df_cleaned = clean(df_raw)
    
    df_cleaned.to_csv(CLEANED_DATA_PATH, index=False)

if __name__ == "__main__":
    main()