# Machine Learning Regression Workflow

This repository provides Python scripts to train and evaluate multiple **Machine Learning (ML) regression models** using a dataset stored in an Excel file. It also allows running **predictive scenarios using trained models**.

The workflow is designed for datasets where:

* **Column 1 = Target variable**
* **Columns 2 → n = Predictor variables**

The scripts automatically train models, evaluate performance, export statistics, generate figures, and store trained models for scenario simulations.

---

# Features

The training script performs the following tasks automatically:

* Trains multiple **machine learning regression techniques**
* Splits dataset into **Calibration (70%)** and **Validation (30%)**
* Generates **Measured vs Predicted plots**
* Adds **Regression line**
* Adds **1:1 reference line**
* Displays **R² inside the figure**
* Displays **ML technique name inside the figure**
* Uses **Times New Roman font for publication-quality figures**
* Saves **each model output in a separate folder**
* Exports **statistics for calibration and validation**
* Saves trained models as **.pkl files** for scenario simulations

---

# Implemented Machine Learning Models

The workflow includes the following regression algorithms:

1. Linear Regression
2. Polynomial Regression
3. Support Vector Regression (SVR)
4. Decision Tree Regression
5. Random Forest Regression
6. Gradient Boosting Regression
7. Extreme Gradient Boosting (XGBoost)
8. Artificial Neural Networks (ANN)
9. K-Nearest Neighbors Regression (KNN)

---

# Required Python Libraries

Install the required packages before running the scripts.

Using **pip**:

```
pip install pandas numpy matplotlib scikit-learn xgboost openpyxl joblib
```

Or using **conda**:

```
conda install pandas numpy matplotlib scikit-learn openpyxl joblib
conda install -c conda-forge xgboost
```

---

# Input Data Format

The training dataset must be an Excel file named:

```
data.xlsx
```

Structure:

| Target | Predictor1 | Predictor2 | Predictor3 | ... |
| ------ | ---------- | ---------- | ---------- | --- |
| 120    | 45         | 24         | 60         | ... |
| 150    | 50         | 25         | 58         | ... |
| 170    | 60         | 23         | 55         | ... |

Rules:

* First row must contain **column names**
* All values must be **numeric**
* No missing values

---

# Scenario Input File

Scenario simulations use another Excel file:

```
scenario_predictors.xlsx
```

Example:

| Rain | Temp | Humidity | Wind |
| ---- | ---- | -------- | ---- |
| 45   | 24   | 60       | 3    |
| 50   | 25   | 58       | 2    |
| 60   | 23   | 55       | 2    |

Important:

* Predictor names must **exactly match the training dataset columns**

---

# Running the Training Script

Run the training script:

```
python ML_models_training_complete.py
```

The script will:

* Train all ML models
* Generate performance plots
* Export statistics
* Save trained models

---

# Running Scenario Simulations

Run:

```
python Run_Scenarios.py
```

The script will:

* Load all trained models (.pkl)
* Apply them to scenario predictors
* Export predictions to Excel

---

# Output Structure

After running the training script, a folder named:

```
Results_Output
```

will be created automatically.

Structure:

```
Results_Output
│
├── All_Model_Statistics.xlsx
├── Model_Performance.png
│
├── Linear_Regression
│   ├── results.xlsx
│   └── Measured_vs_Predicted.png
│
├── Random_Forest
│   ├── results.xlsx
│   └── Measured_vs_Predicted.png
│
├── Gradient_Boosting
│   ├── results.xlsx
│   └── Measured_vs_Predicted.png
│
└── Scenarios
    ├── Linear_Regression.pkl
    ├── Random_Forest.pkl
    ├── Gradient_Boosting.pkl
    └── ...
```

---

# Output Files

Each model produces:

**Figure**

Measured vs Predicted scatter plot including:

* Regression line
* 1:1 reference line
* R² value
* Model name

**Excel file**

Containing:

* Calibration results
* Validation results
* Observed values
* Predicted values

**Model file**

```
model_name.pkl
```

Used for scenario simulations.

---

# Model Comparison

A summary file is produced:

```
All_Model_Statistics.xlsx
```

Containing:

* R²
* RMSE
* MAE

for **Calibration and Validation** phases.

A figure is also generated:

```
Model_Performance.png
```

showing **validation R² for all models**.

---

# Scenario Prediction Script

## Overview

This script allows users to **apply previously trained machine learning models to new predictor datasets (scenarios)**.

The script loads trained models saved as `.pkl` files and generates predictions for each scenario contained in an Excel file.

---

# Input Requirements

## 1. Scenario Predictors File

The script requires an Excel file named:

```
scenario_predictors.xlsx
```

This file must contain **only predictor variables**, with the **same column names and order used during model training**.

### Example

| Rain | Temperature | Humidity | Wind |
| ---- | ----------- | -------- | ---- |
| 45   | 24          | 60       | 3    |
| 50   | 25          | 58       | 2    |
| 60   | 23          | 55       | 2    |

Rules:

* Column names must match the training dataset
* All values must be numeric
* No missing values are allowed

---

## 2. Trained Models Folder

The script loads models stored in:

```
Results_Output/Scenarios/
```

Example:

```
Results_Output/
│
└── Scenarios
    ├── Linear_Regression.pkl
    ├── Polynomial_Regression.pkl
    ├── SVR.pkl
    ├── Decision_Tree.pkl
    ├── Random_Forest.pkl
    ├── Gradient_Boosting.pkl
    ├── XGBoost.pkl
    ├── ANN.pkl
    └── KNN.pkl
```

These files are automatically generated by the **training script**.

---

# Required Python Libraries

Install the following libraries before running the script:

```
pip install pandas numpy joblib openpyxl
```

---

# Running the Scenario Script

Execute the script:

```
python Run_Scenarios.py
```

The script will:

1. Load all `.pkl` models from the `Scenarios` folder
2. Load predictor values from `scenario_predictors.xlsx`
3. Apply each machine learning model to the predictors
4. Generate predictions for each scenario

---

# Output

The script produces the file:

```
Scenario_Predictions.xlsx
```

Example output:

| Scenario | Linear Regression | Random Forest | XGBoost | ANN |
| -------- | ----------------- | ------------- | ------- | --- |
| 1        | 125               | 130           | 128     | 127 |
| 2        | 140               | 145           | 143     | 141 |
| 3        | 150               | 152           | 151     | 149 |

Each column corresponds to a **machine learning model prediction**.

---

# Workflow Summary

```
Training Data → Train Models → Save Models (.pkl)
                                   ↓
                         Scenario Predictors
                                   ↓
                           Scenario Script
                                   ↓
                        Scenario Predictions
```

---

# Notes

* Predictor columns must match the training dataset exactly.
* If column names differ, the script will return an error.
* Ensure the **working directory contains both the scenario file and the results folder**.

---
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18989371.svg)](https://doi.org/10.5281/zenodo.18989371)
