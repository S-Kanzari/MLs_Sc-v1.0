# ==========================================
# SCENARIO SIMULATION
# ==========================================

import pandas as pd
import joblib
import os


models_folder = "Results_Output/Scenarios"

scenario_file = "scenario_predictors.xlsx"

data = pd.read_excel(scenario_file)

results = pd.DataFrame()

for file in os.listdir(models_folder):

    if file.endswith(".pkl"):

        model_name = file.replace(".pkl","")

        model = joblib.load(
            os.path.join(models_folder,file)
        )

        pred = model.predict(data)

        results[model_name] = pred


results.to_excel(
"Scenario_Predictions.xlsx",
index=False
)

print("Scenario simulation completed")