import joblib

import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from data_preprocessing import (
    split_features_and_target,
    build_preprocessor,
)

DATA_PATH = "data/cars_cleaned_with_features.csv"
MODEL_PATH = "models/random_forest_final.joblib"

df = pd.read_csv(DATA_PATH)

X, y = split_features_and_target(df)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = Pipeline(
    steps=[
        ("preprocessor", build_preprocessor()),
        ("regressor", RandomForestRegressor(random_state=42)),
    ]
)

model.fit(X_train, y_train)

joblib.dump(model, MODEL_PATH)

print(f"Final model saved to: {MODEL_PATH}")