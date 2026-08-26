import pandas as pd
from datetime import datetime

def _create_car_age(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    current_year = datetime.now().year
    df['car_age'] = current_year - df['year']
    
    return df

def _create_mileage_per_year(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.copy()
    
    df['mileage_per_year'] = df['mileage_kilometers'] / df['car_age'].replace(0, pd.NA)
    
    return df

def _create_brand_model(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.copy()
    
    df['brand_model'] = df['make'] + '_' + df['model']
    
    return df

def build_features(df: pd.DataFrame) -> pd.DataFrame:
 
    df_features = (
        df
        .pipe(_create_car_age)
        .pipe(_create_mileage_per_year)
        .pipe(_create_brand_model)
        .reset_index(drop=True)
    )
 
    return df_features

CLEANED_DATA_PATH = "data/cars_cleaned.csv"
FEATURES_DATA_PATH = "data/cars_cleaned_with_features.csv"

def main() -> None:
    
    df_cleaned = pd.read_csv(CLEANED_DATA_PATH)

    df_features = build_features(df_cleaned)

    df_features.to_csv(FEATURES_DATA_PATH, index=False)
 
if __name__ == "__main__":
    main() 