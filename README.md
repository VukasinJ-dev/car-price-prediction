# Car Price Prediction

## Opis projekta

Ovaj projekat predstavlja sistem za predikciju cene automobila na osnovu njegovih karakteristika. Za izgradnju modela korišćeni su podaci o automobilima, koji su prethodno analizirani, očišćeni i prošireni dodatnim karakteristikama.

Cilj projekta je da se na osnovu dostupnih informacija o automobilu predvidi njegova cena u američkim dolarima.

Projekat obuhvata kompletan proces razvoja modela mašinskog učenja:

- Exploratory Data Analysis (EDA)
- čišćenje podataka
- feature engineering
- preprocessing podataka
- poređenje različitih regresionih modela
- izbor najboljeg skupa karakteristika
- treniranje finalnog modela
- evaluaciju finalnog modela

## Skup podataka

Projekat koristi skup podataka o automobilima koji sadrži informacije kao što su:

- `make` – proizvođač automobila
- `model` – model automobila
- `condition` – stanje automobila
- `fuel_type` – tip goriva
- `color` – boja
- `transmission` – tip menjača
- `drive_unit` – pogon
- `segment` – segment automobila
- `volume(cm3)` – zapremina motora
- `mileage` – kilometraža
- `year` – godina proizvodnje
- `priceUSD` – cena automobila, odnosno ciljna promenljiva

Tokom feature engineering faze dodate su i nove karakteristike:

- `car_age` – starost automobila
- `mileage_per_year` – prosečna kilometraža po godini
- `brand_model` – kombinacija proizvođača i modela

Nakon eksperimenata utvrđeno je da `brand_model` ne doprinosi poboljšanju modela, pa je izostavljen iz finalnog skupa karakteristika.

## Obrada podataka

### Data cleaning

U početnoj fazi izvršena je analiza kvaliteta podataka i uklanjanje problema kao što su:

- nedostajuće vrednosti
- duplikati
- neispravne vrednosti
- ekstremne i nerealne vrednosti
- neujednačeni nazivi kolona i kategorija
- nerealne vrednosti zapremine motora
- placeholder vrednosti za kilometražu

Nakon čišćenja podaci su sačuvani u:

```text
data/cars_cleaned.csv
```

### Feature engineering

Nakon čišćenja kreirane su dodatne karakteristike koje mogu da pomognu modelu u predikciji cene.

Rezultat ove faze sačuvan je u:

```text
data/cars_cleaned_with_features.csv
```

### Data preprocessing

Numeričke karakteristike obrađuju se pomoću:

- `SimpleImputer(strategy="median")`
- `StandardScaler`

Kategorijske karakteristike obrađuju se pomoću:

- `SimpleImputer(strategy="most_frequent")`
- `OneHotEncoder(handle_unknown="ignore")`

Za obradu karakteristika koristi se `ColumnTransformer`, dok se preprocessing i model kombinuju u `Pipeline`.

## Modeli

Testirana su četiri regresiona modela:

1. Linear Regression
2. Ridge Regression
3. Random Forest Regressor
4. Gradient Boosting Regressor

Za poređenje modela korišćene su sledeće metrike:

- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R² (Coefficient of Determination)

Za sve eksperimente korišćen je isti train/test split:

```text
test_size = 0.2
random_state = 42
```

## Poređenje modela

Početno poređenje sa svim karakteristikama pokazalo je sledeće rezultate:

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Random Forest | 1081.63 | 2609.30 | 0.910111 |
| Gradient Boosting | 1557.42 | 2977.37 | 0.882963 |
| Ridge Regression | 2109.38 | 4329.71 | 0.752500 |
| Linear Regression | 2115.56 | 4353.19 | 0.749809 |

Random Forest je već u početnom eksperimentu ostvario najbolje rezultate.

## Izbor karakteristika

Pored poređenja modela, testirane su i različite kombinacije karakteristika kako bi se utvrdilo da li je moguće ukloniti neke karakteristike bez pogoršanja performansi.

Najbolji rezultat ostvaren je kada je izostavljena karakteristika:

```text
brand_model
```

Rezultati za Random Forest bili su:

| Feature set | MAE | RMSE | R² |
|---|---:|---:|---:|
| Bez `brand_model` | 1078.18 | 2590.68 | 0.911390 |
| Bez `brand_model` i `mileage_per_year` | 1078.60 | 2592.19 | 0.911286 |
| Bez `brand_model` i `car_age` | 1078.94 | 2591.00 | 0.911368 |
| Sve karakteristike | 1081.63 | 2609.30 | 0.910111 |

Uklanjanje `brand_model` je izabrano kao najbolja opcija jer je dalo najbolje rezultate. Karakteristika predstavlja kombinaciju `make` i `model`, koji su već zasebno dostupni modelu, pa nije bilo potrebe da se ova informacija dodatno predstavlja kroz novu kategoriju.

Testirano je i uklanjanje pojedinačnih karakteristika kao što su `volume`, `make` i `model`, ali je njihovo uklanjanje dovelo do pogoršanja rezultata. Zbog toga su zadržane u finalnom skupu.

`car_age` i `mileage_per_year` su takođe zadržane, jer njihovo uklanjanje nije donelo poboljšanje u odnosu na najbolju kombinaciju.

## Finalni model

Na osnovu sprovedenih eksperimenata izabran je:

```text
RandomForestRegressor
```

sa svim odabranim karakteristikama osim:

```text
brand_model
```

Finalni model koristi isti preprocessing kao i modeli tokom eksperimentisanja i treniran je na trening skupu.

Finalni model je sačuvan u:

```text
models/random_forest_final.joblib
```

## Rezultati

Najbolji rezultat tokom poređenja modela ostvaren je pomoću Random Forest modela bez `brand_model` karakteristike:

```text
MAE  = 1078.18 USD
MSE  = 6,711,611
RMSE = 2590.68 USD
R²   = 0.911390
```

R² rezultat od `0.911390` znači da model objašnjava približno 91.1% varijacije cena u test skupu.

MAE od približno `1078 USD` znači da je prosečna apsolutna greška predikcije bila oko 1,078 američkih dolara na korišćenom test skupu.

Random Forest je izabran zato što je ostvario značajno bolje rezultate od Linear Regression, Ridge Regression i Gradient Boosting modela, kao i zato što je dao najbolju kombinaciju MAE, RMSE i R² metrike.

## Pokretanje projekta

### 1. Kloniranje repozitorijuma

Nakon kloniranja projekta potrebno je instalirati potrebne biblioteke.

### 2. Instalacija dependencies

```bash
pip install -r requirements.txt
```

### 3. Pokretanje EDA analize

EDA analiza nalazi se u:

```text
notebooks/EDA_analysis.ipynb
```

Notebook se može otvoriti u Jupyter Notebook-u ili JupyterLab-u.

### 4. Pokretanje poređenja modela

Eksperimenti i poređenje različitih modela dokumentovani su u:

```text
notebooks/model_comparasion.ipynb
```

Skripta za automatsko poređenje modela nalazi se u:

```text
src/model_comparasion.py
```

### 5. Treniranje početnog modela

Početni Linear Regression model može se trenirati pomoću:

```text
src/model_training.py
```

Model se čuva kao:

```text
models/linear_regression_model.joblib
```

### 6. Treniranje finalnog modela

Nakon izbora modela i karakteristika, finalni model se trenira pomoću:

```text
src/final_model_training.py
```

Finalni model se čuva kao:

```text
models/random_forest_final.joblib
```

### 7. Evaluacija finalnog modela

Finalni model se evaluira pomoću:

```text
src/final_model_evaluation.py
```

Skripta učitava sačuvani finalni model i izračunava MAE, MSE, RMSE i R² na test skupu.

## Struktura projekta

```text
car-price-prediction/
│
├── data/
│   ├── cars.csv
│   ├── cars_cleaned.csv
│   └── cars_cleaned_with_features.csv
│
├── models/
│   ├── linear_regression_model.joblib
│   └── random_forest_final.joblib
│
├── notebooks/
│   ├── EDA_analysis.ipynb
│   └── model_comparasion.ipynb
│
├── src/
│   ├── data_clean.py
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   ├── model_evaluation.py
│   ├── model_comparasion.py
│   ├── final_model_training.py
│   └── final_model_evaluation.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Zaključak

Projekat je obuhvatio kompletan proces razvoja modela za predikciju cene automobila, od analize i čišćenja podataka do izbora i evaluacije finalnog modela.

Testirana su četiri regresiona algoritma, pri čemu je **Random Forest Regressor** ostvario najbolje rezultate. Eksperimentima sa različitim skupovima karakteristika utvrđeno je da se najbolji rezultat dobija kada se izostavi `brand_model`, dok se ostale karakteristike zadržavaju.

Konačni model je zato **Random Forest Regressor bez `brand_model` karakteristike**, sa ostvarenim R² rezultatom od **0.911390** i MAE od približno **1,078 USD** na test skupu.

Ovaj model predstavlja finalni rezultat projekta i sačuvan je u `models/random_forest_final.joblib`.
