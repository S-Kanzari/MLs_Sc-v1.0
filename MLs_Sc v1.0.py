# ===============================================
# MACHINE LEARNING REGRESSION WORKFLOW
# ===============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor

from xgboost import XGBRegressor

# ===============================================
# FIGURE STYLE
# ===============================================
plt.rcParams["font.family"] = "Times New Roman"

# ===============================================
# OUTPUT FOLDERS
# ===============================================
main_folder = "Results_Output"
scenario_folder = os.path.join(main_folder, "Scenarios")

os.makedirs(main_folder, exist_ok=True)
os.makedirs(scenario_folder, exist_ok=True)

# ===============================================
# LOAD DATA
# ===============================================
df = pd.read_excel("data.xlsx")
y = df.iloc[:,0]
X = df.iloc[:,1:]

# ===============================================
# SPLIT DATA
# ===============================================
X_cal, X_val, y_cal, y_val = train_test_split(
    X, y, test_size=0.3, random_state=1
)

# ===============================================
# STAT FUNCTION
# ===============================================
def stats(obs, sim):
    r2 = r2_score(obs, sim)
    rmse = np.sqrt(mean_squared_error(obs, sim))
    mae = mean_absolute_error(obs, sim)
    return r2, rmse, mae

# ===============================================
# MODELS
# ===============================================
models = {
    "Linear_Regression": LinearRegression(),
    "Polynomial_Regression": Pipeline([("poly", PolynomialFeatures(2)), ("linear", LinearRegression())]),
    "SVR": Pipeline([("scaler", StandardScaler()), ("svr", SVR())]),
    "Decision_Tree": DecisionTreeRegressor(),
    "Random_Forest": RandomForestRegressor(n_estimators=300),
    "Gradient_Boosting": GradientBoostingRegressor(),
    "XGBoost": XGBRegressor(objective='reg:squarederror'),
    "ANN": Pipeline([("scaler", StandardScaler()), ("ann", MLPRegressor(hidden_layer_sizes=(50,50), max_iter=2000))]),
    "KNN": Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsRegressor(5))])
}

# ===============================================
# GLOBAL STATISTICS
# ===============================================
global_stats = []

# ===============================================
# RUN MODELS
# ===============================================
for name, model in models.items():
    print("Running:", name)

    # create model folder
    model_folder = os.path.join(main_folder, name)
    os.makedirs(model_folder, exist_ok=True)

    # train model
    model.fit(X_cal, y_cal)

    # predictions
    pred_cal = model.predict(X_cal)
    pred_val = model.predict(X_val)

    r2_cal, rmse_cal, mae_cal = stats(y_cal, pred_cal)
    r2_val, rmse_val, mae_val = stats(y_val, pred_val)

    global_stats.append([name, r2_cal, rmse_cal, mae_cal, r2_val, rmse_val, mae_val])

    # ===========================================
    # EXPORT MODEL DATA
    # ===========================================
    df_cal = pd.DataFrame({"Observed": y_cal, "Predicted": pred_cal})
    df_val = pd.DataFrame({"Observed": y_val, "Predicted": pred_val})

    writer = pd.ExcelWriter(os.path.join(model_folder, "results.xlsx"))
    df_cal.to_excel(writer, "Calibration", index=False)
    df_val.to_excel(writer, "Validation", index=False)
    writer.close()

    # ===========================================
    # REGRESSION LINE
    # ===========================================
    coef = np.polyfit(y_cal, pred_cal, 1)
    poly = np.poly1d(coef)
    x_line = np.linspace(min(y), max(y), 100)

    # ===========================================
    # SCATTER FIGURE
    # ===========================================
    plt.figure(figsize=(6,6))
    plt.scatter(y_cal, pred_cal, label="Calibration")
    plt.scatter(y_val, pred_val, label="Validation")

    # regression line
    plt.plot(x_line, poly(x_line), color="red", label="Regression Line")
    plt.plot(x_line, x_line, "--", color="black", label="1:1 Line")

    plt.xlabel("Measured")
    plt.ylabel("Predicted")

    # R² inside figure
    plt.text(0.05, 0.95, f"R² = {r2_cal:.3f}", transform=plt.gca().transAxes,
             verticalalignment='top', fontsize=12, fontweight='bold', color='blue')

    # ML technique name inside figure
    plt.text(0.05, 0.88, name, transform=plt.gca().transAxes,
             fontsize=12, fontweight='bold', color='darkgreen')

    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(model_folder, "Measured_vs_Predicted.png"), dpi=300)
    plt.close()

    # ===========================================
    # SAVE MODEL FOR SCENARIOS
    # ===========================================
    joblib.dump(model, os.path.join(scenario_folder, f"{name}.pkl"))

# ===============================================
# GLOBAL MODEL STATISTICS
# ===============================================
stats_df = pd.DataFrame(global_stats,
                        columns=["Model", "R2_cal", "RMSE_cal", "MAE_cal",
                                 "R2_val", "RMSE_val", "MAE_val"])
stats_df = stats_df.sort_values(by="R2_val", ascending=False)
stats_df.to_excel(os.path.join(main_folder, "All_Model_Statistics.xlsx"), index=False)

# ===============================================
# MODEL COMPARISON FIGURE
# ===============================================
plt.figure(figsize=(8,5))
plt.bar(stats_df["Model"], stats_df["R2_val"], color="skyblue")
plt.xticks(rotation=45)
plt.ylabel("R² (Validation)")
plt.title("Model Comparison")
plt.tight_layout()
plt.savefig(os.path.join(main_folder, "Model_Performance.png"), dpi=300)
plt.close()

print("All models finished successfully!")